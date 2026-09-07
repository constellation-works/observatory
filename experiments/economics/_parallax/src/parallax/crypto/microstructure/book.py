"""Offline reconstruction of a level-2 book from a verbatim capture.

Binance publishes depth as a diff stream keyed by update ids, anchored by REST snapshots. The
documented synchronisation procedure is implemented here in full, including the failure branch:
when the update-id chain breaks, the assembler declares itself unsynced and refuses to serve book
states until the next snapshot re-anchors it. Silently continuing over a gap would manufacture
liquidity that never existed, which is exactly the artefact this research is trying not to trade.
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Trade:
    """One aggregated trade. ``buyer_is_maker`` follows Binance's ``m`` flag."""

    ts_ns: int
    price: float
    qty: float
    buyer_is_maker: bool

    @property
    def signed_qty(self) -> float:
        """Positive when the aggressor bought (lifted the ask), negative when it sold."""
        return -self.qty if self.buyer_is_maker else self.qty

    @property
    def notional(self) -> float:
        return self.price * self.qty


@dataclass(frozen=True, slots=True)
class BookState:
    """An immutable book snapshot: bids descending by price, asks ascending."""

    ts_ns: int
    bids: tuple[tuple[float, float], ...]
    asks: tuple[tuple[float, float], ...]

    @property
    def best_bid(self) -> float | None:
        return self.bids[0][0] if self.bids else None

    @property
    def best_ask(self) -> float | None:
        return self.asks[0][0] if self.asks else None

    @property
    def mid(self) -> float | None:
        if not self.bids or not self.asks:
            return None
        return (self.bids[0][0] + self.asks[0][0]) / 2.0

    @property
    def spread_bps(self) -> float | None:
        mid = self.mid
        if mid is None or mid <= 0.0:
            return None
        return (self.asks[0][0] - self.bids[0][0]) / mid * 10_000.0

    def depth_within_bps(self, bps: float) -> tuple[float, float]:
        """Resting base-asset quantity within ``bps`` of mid, as ``(bid_qty, ask_qty)``."""
        mid = self.mid
        if mid is None:
            return (0.0, 0.0)
        floor = mid * (1.0 - bps / 10_000.0)
        ceiling = mid * (1.0 + bps / 10_000.0)
        bid_qty = 0.0
        for price, qty in self.bids:
            if price < floor:
                break
            bid_qty += qty
        ask_qty = 0.0
        for price, qty in self.asks:
            if price > ceiling:
                break
            ask_qty += qty
        return (bid_qty, ask_qty)

    def notional_within_bps(self, bps: float) -> tuple[float, float]:
        """Resting quote-asset notional within ``bps`` of mid, as ``(bid, ask)``."""
        mid = self.mid
        if mid is None:
            return (0.0, 0.0)
        floor = mid * (1.0 - bps / 10_000.0)
        ceiling = mid * (1.0 + bps / 10_000.0)
        bid = sum(price * qty for price, qty in self.bids if price >= floor)
        ask = sum(price * qty for price, qty in self.asks if price <= ceiling)
        return (bid, ask)


class DesyncError(RuntimeError):
    """Raised when a book state is requested while the assembler is unsynced."""


@dataclass
class BookAssembler:
    """Applies snapshots and depth diffs, tracking synchronisation explicitly.

    Binance's synchronisation procedure requires buffering diffs from *before* the snapshot and
    replaying them across it: the REST fetch takes long enough that, in receive order, the diffs
    covering ``lastUpdateId + 1`` onward land in the capture ahead of the snapshot record. While
    unsynced, incoming diffs are therefore buffered, and each snapshot replays the buffer after
    anchoring. Without this, every anchor attempt sees a spurious gap and no diff ever applies.
    """

    buffer_limit: int = 200_000
    _bids: dict[float, float] = field(default_factory=dict, init=False, repr=False)
    _asks: dict[float, float] = field(default_factory=dict, init=False, repr=False)
    _pending: list[dict[str, Any]] = field(default_factory=list, init=False, repr=False)
    _last_update_id: int | None = field(default=None, init=False)
    synced: bool = field(default=False, init=False)
    applied_diffs: int = field(default=0, init=False)
    skipped_diffs: int = field(default=0, init=False)
    gaps: int = field(default=0, init=False)
    snapshots: int = field(default=0, init=False)

    def apply_snapshot(self, payload: dict[str, Any]) -> bool:
        """Anchor on a REST snapshot, then replay any buffered diffs across it."""
        last_update_id = int(payload["lastUpdateId"])
        if self.synced and self._last_update_id is not None:
            if last_update_id <= self._last_update_id:
                return False
        self._bids = {float(p): float(q) for p, q in payload.get("bids", ()) if float(q) > 0.0}
        self._asks = {float(p): float(q) for p, q in payload.get("asks", ()) if float(q) > 0.0}
        self._last_update_id = last_update_id
        self.synced = True
        self.snapshots += 1
        pending, self._pending = self._pending, []
        for diff in pending:
            self._apply_diff_synced(diff)
            if not self.synced:  # the buffer itself had a real hole; stay desynced honestly
                break
        return True

    def apply_diff(self, payload: dict[str, Any]) -> bool:
        """Apply one ``depthUpdate``. Returns whether it was applied to the book."""
        if not self.synced:
            self._buffer(payload)
            return False
        return self._apply_diff_synced(payload)

    def _apply_diff_synced(self, payload: dict[str, Any]) -> bool:
        assert self._last_update_id is not None
        first_id = int(payload["U"])
        final_id = int(payload["u"])
        if final_id <= self._last_update_id:
            self.skipped_diffs += 1
            return False
        if not self._chains(payload, first_id, final_id):
            self.synced = False
            self.gaps += 1
            self._buffer(payload)
            return False
        _apply_levels(self._bids, payload.get("b", ()))
        _apply_levels(self._asks, payload.get("a", ()))
        self._last_update_id = final_id
        self.applied_diffs += 1
        return True

    def _chains(self, payload: dict[str, Any], first_id: int, final_id: int) -> bool:
        """Does this diff extend the chain? Spot and futures declare continuity differently.

        Spot diffs are id-contiguous: the next diff starts at the previous ``u + 1``. USDT-M
        futures diffs instead carry ``pu``, the previous diff's ``u``, and continuity means
        ``pu == last_update_id`` (Binance's documented futures sync rule). Both markets share the
        snapshot-straddle case, where the first usable diff spans the snapshot's id.
        """
        assert self._last_update_id is not None
        if first_id <= self._last_update_id + 1 <= final_id:
            return True  # straddles the anchor (spot: lastUpdateId + 1; futures spans it too)
        previous_u = payload.get("pu")
        if previous_u is not None:
            return int(previous_u) == self._last_update_id
        return first_id == self._last_update_id + 1

    def _buffer(self, payload: dict[str, Any]) -> None:
        self.skipped_diffs += 1
        self._pending.append(payload)
        if len(self._pending) > self.buffer_limit:
            self._pending = self._pending[-self.buffer_limit :]

    def state(self, ts_ns: int, depth_levels: int | None = None) -> BookState:
        """Materialise a sorted, immutable book state."""
        if not self.synced:
            raise DesyncError("book is unsynced; wait for the next snapshot")
        bids = sorted(self._bids.items(), key=lambda item: -item[0])
        asks = sorted(self._asks.items())
        if depth_levels is not None:
            bids = bids[:depth_levels]
            asks = asks[:depth_levels]
        return BookState(ts_ns=ts_ns, bids=tuple(bids), asks=tuple(asks))


def _apply_levels(side: dict[float, float], updates: Iterable[Sequence[Any]]) -> None:
    for price_raw, qty_raw in updates:
        price = float(price_raw)
        qty = float(qty_raw)
        if qty <= 0.0:
            side.pop(price, None)
        else:
            side[price] = qty


def iter_records(paths: Iterable[Path]) -> Iterator[dict[str, Any]]:
    """Yield capture records in file order, skipping malformed lines.

    A capture being written right now ends in a truncated gzip member — the recorder has not
    closed the stream yet. That is the normal analyze-while-recording case, so a truncated tail
    ends that file quietly instead of aborting the replay.
    """
    for path in paths:
        opener = gzip.open if str(path).endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8") as handle:  # type: ignore[operator]
            try:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(record, dict):
                        yield record
            except (EOFError, gzip.BadGzipFile, OSError):
                continue


def parse_trade(data: dict[str, Any], local_ns: int) -> Trade:
    """Build a :class:`Trade` from an ``aggTrade`` payload.

    The exchange trade time ``T`` is authoritative for ordering; ``local_ns`` is the fallback for
    payloads that omit it.
    """
    exchange_ms = data.get("T")
    ts_ns = int(exchange_ms) * 1_000_000 if exchange_ms is not None else local_ns
    return Trade(
        ts_ns=ts_ns,
        price=float(data["p"]),
        qty=float(data["q"]),
        buyer_is_maker=bool(data["m"]),
    )
