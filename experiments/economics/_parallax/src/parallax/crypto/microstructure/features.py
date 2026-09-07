"""Book-state features for the liquidity-void hypothesis.

Four families, each mapping to a claim that can fail on its own:

``void_*``
    Asymmetry of resting liquidity within a band of mid. The hypothesis is that a move which
    outruns its resting liquidity reverts toward the side that still has depth. Note that the
    queue-imbalance literature (Gould & Bonart, 2016) documents the opposite sign at the touch:
    price tends to move *toward* the thin side. Both are here; which dominates at which horizon is
    an empirical question, not something to assume.

``maker_flow_*``
    Net posting minus cancelling, computed by removing executed volume from the observed depth
    change. This is the "wall dissipating" term. A level-2 feed gives the *net* of additions and
    cancellations, never the gross of either; separating them needs level-3 data. Measured over a
    price band anchored on the previous mid so that mid drift cannot masquerade as cancellation.

``ofi``
    Best-level order flow imbalance in the sense of Cont, Kukanov & Stoikov (2014).

``flow_*`` / ``drift_*``
    Exponentially decayed signed trade volume and past returns: the "ammo" term, in the shape of a
    transient-impact propagator (Bouchaud et al., 2004). Provided at several half-lives because the
    decay constant is the thing being measured, not something known in advance.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

from parallax.crypto.microstructure.book import BookState, Trade

DEFAULT_DEPTH_GRID_BPS = (5.0, 10.0, 25.0, 50.0, 100.0)
DEFAULT_HALF_LIVES_S = (5.0, 30.0, 120.0, 600.0)


@dataclass(frozen=True)
class FeatureConfig:
    depth_grid_bps: tuple[float, ...] = DEFAULT_DEPTH_GRID_BPS
    flow_half_lives_s: tuple[float, ...] = DEFAULT_HALF_LIVES_S
    maker_flow_band_bps: float = 25.0

    def __post_init__(self) -> None:
        if not self.depth_grid_bps or any(value <= 0.0 for value in self.depth_grid_bps):
            raise ValueError("depth grid must be non-empty and positive")
        if not self.flow_half_lives_s or any(value <= 0.0 for value in self.flow_half_lives_s):
            raise ValueError("half lives must be non-empty and positive")
        if self.maker_flow_band_bps <= 0.0:
            raise ValueError("maker flow band must be positive")


@dataclass
class DecayState:
    """Exponentially weighted accumulators for signed flow, gross volume, and past returns."""

    half_lives_s: tuple[float, ...]
    _signed: dict[float, float] = field(default_factory=dict, init=False, repr=False)
    _gross: dict[float, float] = field(default_factory=dict, init=False, repr=False)
    _drift: dict[float, float] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        for half_life in self.half_lives_s:
            self._signed[half_life] = 0.0
            self._gross[half_life] = 0.0
            self._drift[half_life] = 0.0

    def update(self, dt_s: float, signed_qty: float, gross_qty: float, log_return: float) -> None:
        dt_s = max(dt_s, 0.0)
        for half_life in self.half_lives_s:
            decay = math.exp(-math.log(2.0) * dt_s / half_life)
            self._signed[half_life] = self._signed[half_life] * decay + signed_qty
            self._gross[half_life] = self._gross[half_life] * decay + gross_qty
            self._drift[half_life] = self._drift[half_life] * decay + log_return

    def features(self) -> dict[str, float]:
        row: dict[str, float] = {}
        for half_life in self.half_lives_s:
            tag = _tag(half_life)
            signed = self._signed[half_life]
            gross = self._gross[half_life]
            row[f"flow_signed_{tag}"] = signed
            row[f"flow_ratio_{tag}"] = signed / gross if gross > 0.0 else 0.0
            row[f"drift_bps_{tag}"] = self._drift[half_life] * 10_000.0
        return row


def compute_features(
    previous: BookState,
    current: BookState,
    trades: Sequence[Trade],
    config: FeatureConfig,
    decay: DecayState,
) -> dict[str, float] | None:
    """One feature row for the interval ``(previous, current]``.

    Returns ``None`` when either book state is one-sided, since mid is undefined there.
    ``decay`` is mutated: it carries the propagator state across rows.
    """
    previous_mid = previous.mid
    current_mid = current.mid
    if previous_mid is None or current_mid is None or previous_mid <= 0.0 or current_mid <= 0.0:
        return None

    dt_s = max(current.ts_ns - previous.ts_ns, 0) / 1e9
    log_return = math.log(current_mid / previous_mid)

    buy_qty = sum(trade.qty for trade in trades if not trade.buyer_is_maker)
    sell_qty = sum(trade.qty for trade in trades if trade.buyer_is_maker)
    gross_qty = buy_qty + sell_qty
    decay.update(dt_s, buy_qty - sell_qty, gross_qty, log_return)

    row: dict[str, float] = {
        "ts_ns": float(current.ts_ns),
        "mid": current_mid,
        "spread_bps": current.spread_bps or 0.0,
        "dt_s": dt_s,
        "trade_qty": gross_qty,
        "trade_imbalance": _imbalance(buy_qty, sell_qty),
        "queue_imbalance": _queue_imbalance(current),
        "ofi": order_flow_imbalance(previous, current),
    }

    for bps in config.depth_grid_bps:
        bid_notional, ask_notional = current.notional_within_bps(bps)
        tag = _tag(bps)
        row[f"void_imbalance_{tag}"] = _imbalance(bid_notional, ask_notional)
        row[f"depth_bid_{tag}"] = bid_notional
        row[f"depth_ask_{tag}"] = ask_notional

    row.update(_maker_flow(previous, current, buy_qty, sell_qty, config.maker_flow_band_bps))
    row.update(decay.features())
    return row


def order_flow_imbalance(previous: BookState, current: BookState) -> float:
    """Best-level order flow imbalance (Cont, Kukanov & Stoikov, 2014). Positive is buy pressure."""
    if not (previous.bids and previous.asks and current.bids and current.asks):
        return 0.0
    bid_price_prev, bid_qty_prev = previous.bids[0]
    ask_price_prev, ask_qty_prev = previous.asks[0]
    bid_price_cur, bid_qty_cur = current.bids[0]
    ask_price_cur, ask_qty_cur = current.asks[0]

    contribution = 0.0
    if bid_price_cur >= bid_price_prev:
        contribution += bid_qty_cur
    if bid_price_cur <= bid_price_prev:
        contribution -= bid_qty_prev
    if ask_price_cur <= ask_price_prev:
        contribution -= ask_qty_cur
    if ask_price_cur >= ask_price_prev:
        contribution += ask_qty_prev
    return contribution


def _maker_flow(
    previous: BookState,
    current: BookState,
    buy_qty: float,
    sell_qty: float,
    band_bps: float,
) -> dict[str, float]:
    """Net posting minus cancelling per side, with executed volume removed.

    The band is anchored on the *previous* mid and applied as fixed absolute prices to both
    states, so a mid that drifts out of the band cannot be mistaken for cancellation.
    """
    anchor = previous.mid
    if anchor is None:
        return {"maker_flow_bid": 0.0, "maker_flow_ask": 0.0, "maker_flow_imbalance": 0.0}
    floor = anchor * (1.0 - band_bps / 10_000.0)
    ceiling = anchor * (1.0 + band_bps / 10_000.0)

    bid_before = _qty_in_range(previous.bids, floor, anchor)
    bid_after = _qty_in_range(current.bids, floor, anchor)
    ask_before = _qty_in_range(previous.asks, anchor, ceiling)
    ask_after = _qty_in_range(current.asks, anchor, ceiling)

    # depth_after - depth_before = additions - cancellations - executions
    maker_flow_bid = (bid_after - bid_before) + sell_qty
    maker_flow_ask = (ask_after - ask_before) + buy_qty
    return {
        "maker_flow_bid": maker_flow_bid,
        "maker_flow_ask": maker_flow_ask,
        "maker_flow_imbalance": _imbalance_signed(maker_flow_bid, maker_flow_ask),
    }


def _qty_in_range(levels: tuple[tuple[float, float], ...], low: float, high: float) -> float:
    return sum(qty for price, qty in levels if low <= price <= high)


def _queue_imbalance(state: BookState) -> float:
    if not (state.bids and state.asks):
        return 0.0
    return _imbalance(state.bids[0][1], state.asks[0][1])


def _imbalance(bid: float, ask: float) -> float:
    total = bid + ask
    if total <= 0.0:
        return 0.0
    return (bid - ask) / total


def _imbalance_signed(bid: float, ask: float) -> float:
    """Imbalance for quantities that may be negative; scaled by summed magnitude."""
    total = abs(bid) + abs(ask)
    if total <= 0.0:
        return 0.0
    return (bid - ask) / total


def _tag(value: float) -> str:
    return f"{value:g}".replace(".", "p")


def feature_columns(config: FeatureConfig) -> tuple[str, ...]:
    """Names of the predictive columns, excluding bookkeeping and raw depth levels."""
    columns = [
        "spread_bps",
        "trade_qty",
        "trade_imbalance",
        "queue_imbalance",
        "ofi",
        "maker_flow_bid",
        "maker_flow_ask",
        "maker_flow_imbalance",
    ]
    columns += [f"void_imbalance_{_tag(bps)}" for bps in config.depth_grid_bps]
    for half_life in config.flow_half_lives_s:
        tag = _tag(half_life)
        columns += [f"flow_signed_{tag}", f"flow_ratio_{tag}", f"drift_bps_{tag}"]
    return tuple(columns)
