"""Verbatim capture of Binance level-2 depth diffs, trades, and touch quotes.

The recorder deliberately does the dumbest reliable thing it can: it appends every message it
receives, unparsed, tagged with a local receive timestamp, and never reconstructs a book. Book
assembly is an offline concern (:mod:`parallax.crypto.microstructure.book`), so a reconstruction
bug can be fixed and replayed. The capture itself cannot be recovered once the moment has passed,
which is why it carries as little logic as possible.

Every disconnection, error, and resynchronisation is written into the capture as a record of its
own. A hole in the data that nobody can see is worse than a hole that is labelled.
"""

from __future__ import annotations

import asyncio
import gzip
import json
import signal
from collections.abc import Sequence
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

CAPTURE_VERSION = 2

MARKETS: dict[str, dict[str, Any]] = {
    "spot": {
        "ws_base": "wss://data-stream.binance.vision/stream",
        "rest_depth": "https://data-api.binance.vision/api/v3/depth",
        "suffixes": ("depth@100ms", "aggTrade", "bookTicker"),
        "max_depth_limit": 5_000,
        "exchange": "binance-spot",
        "label_suffix": "",
    },
    # USDT-margined perpetuals. forceOrder is the liquidation stream and markPrice@1s carries
    # the funding rate — both exist only here, which is why the futures capture exists at all.
    "futures": {
        "ws_base": "wss://fstream.binance.com/stream",
        "rest_depth": "https://fapi.binance.com/fapi/v1/depth",
        "suffixes": ("depth@100ms", "aggTrade", "bookTicker", "forceOrder", "markPrice@1s"),
        "max_depth_limit": 1_000,
        "exchange": "binance-usdm-futures",
        "label_suffix": "-PERP",
    },
}

MAX_BACKOFF_SECONDS = 30.0
USER_AGENT = "parallax-recorder/2"


@dataclass(frozen=True)
class CaptureConfig:
    """Everything that determines the shape of a capture, recorded into its manifest."""

    symbol: str
    root: Path = Path("data/R01-crypto/raw/book")
    market: str = "spot"
    stream_suffixes: tuple[str, ...] | None = None
    depth_limit: int | None = None
    snapshot_seconds: float = 300.0
    flush_seconds: float = 5.0

    def __post_init__(self) -> None:
        if not self.symbol or not self.symbol.isalnum():
            raise ValueError("symbol must be a non-empty alphanumeric ticker, e.g. BTCUSDT")
        if self.market not in MARKETS:
            raise ValueError(f"market must be one of {sorted(MARKETS)}")
        if self.stream_suffixes is not None and not self.stream_suffixes:
            raise ValueError("at least one stream suffix is required")
        if self.depth_limit is not None:
            if self.depth_limit <= 0:
                raise ValueError("depth_limit must be positive")
            if self.depth_limit > MARKETS[self.market]["max_depth_limit"]:
                raise ValueError(
                    f"depth_limit exceeds the {self.market} REST maximum "
                    f"({MARKETS[self.market]['max_depth_limit']})"
                )
        if self.snapshot_seconds <= 0.0 or self.flush_seconds <= 0.0:
            raise ValueError("intervals must be positive")

    @property
    def symbol_upper(self) -> str:
        return self.symbol.upper()

    @property
    def capture_label(self) -> str:
        """Directory name for this capture; perp data never mixes with spot data."""
        return self.symbol_upper + MARKETS[self.market]["label_suffix"]

    @property
    def effective_suffixes(self) -> tuple[str, ...]:
        if self.stream_suffixes is not None:
            return self.stream_suffixes
        return MARKETS[self.market]["suffixes"]

    @property
    def effective_depth_limit(self) -> int:
        if self.depth_limit is not None:
            return self.depth_limit
        return int(MARKETS[self.market]["max_depth_limit"])

    @property
    def streams(self) -> tuple[str, ...]:
        lower = self.symbol.lower()
        return tuple(f"{lower}@{suffix}" for suffix in self.effective_suffixes)

    @property
    def ws_url(self) -> str:
        return f"{MARKETS[self.market]['ws_base']}?streams={'/'.join(self.streams)}"

    @property
    def rest_url(self) -> str:
        base = MARKETS[self.market]["rest_depth"]
        return f"{base}?symbol={self.symbol_upper}&limit={self.effective_depth_limit}"

    def manifest(self) -> dict[str, Any]:
        return {
            "kind": "manifest",
            "capture_version": CAPTURE_VERSION,
            "exchange": MARKETS[self.market]["exchange"],
            "market": self.market,
            "symbol": self.symbol_upper,
            "streams": list(self.streams),
            "ws_url": self.ws_url,
            "rest_url": self.rest_url,
            "depth_limit": self.effective_depth_limit,
            "snapshot_seconds": self.snapshot_seconds,
        }


@dataclass
class CaptureWriter:
    """Append-only, hourly-rotated, gzip JSON-lines sink.

    Each rotated file repeats the manifest as its first line so that a single hour of capture is
    independently interpretable without the rest of the day.
    """

    config: CaptureConfig
    _handle: gzip.GzipFile | None = field(default=None, init=False, repr=False)
    _slot: str | None = field(default=None, init=False, repr=False)
    _path: Path | None = field(default=None, init=False, repr=False)
    lines_written: int = field(default=0, init=False)

    @property
    def path(self) -> Path | None:
        return self._path

    def write(self, record: dict[str, Any]) -> None:
        now = datetime.now(UTC)
        slot = now.strftime("%Y-%m-%d/%H")
        if slot != self._slot:
            self._rotate(slot)
        assert self._handle is not None
        self._handle.write((json.dumps(record, separators=(",", ":")) + "\n").encode("utf-8"))
        self.lines_written += 1

    def flush(self) -> None:
        if self._handle is not None:
            self._handle.flush()

    def close(self) -> None:
        if self._handle is not None:
            self._handle.close()
            self._handle = None
            self._slot = None

    def _rotate(self, slot: str) -> None:
        self.close()
        path = self.config.root / self.config.capture_label / f"{slot}.jsonl.gz"
        path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = gzip.open(path, "ab")
        self._slot = slot
        self._path = path
        manifest = self.config.manifest() | {"local_ns": _now_ns(), "rotated_to": str(path)}
        self._handle.write((json.dumps(manifest, separators=(",", ":")) + "\n").encode("utf-8"))


def fetch_depth_snapshot(config: CaptureConfig, timeout: float = 15.0) -> dict[str, Any]:
    """Fetch a REST depth snapshot. Snapshots anchor offline book reconstruction."""
    request = Request(config.rest_url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed https endpoint
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict) or "lastUpdateId" not in payload:
        raise ValueError("unexpected depth snapshot response")
    return payload


async def run_capture(config: CaptureConfig, stop: asyncio.Event | None = None) -> int:
    """Run the capture until cancelled or ``stop`` is set. Returns lines written."""
    try:
        import websockets
    except ModuleNotFoundError as error:  # pragma: no cover - environment guard
        raise RuntimeError(
            "the recorder needs the 'websockets' package: uv sync --group capture"
        ) from error

    stop = stop or asyncio.Event()
    _install_signal_handlers(stop)

    writer = CaptureWriter(config)
    resync = asyncio.Event()
    resync.set()  # always open a capture with a snapshot

    snapshots = asyncio.create_task(_snapshot_loop(config, writer, resync, stop))
    flusher = asyncio.create_task(_flush_loop(writer, config.flush_seconds, stop))
    try:
        await _stream_loop(websockets, config, writer, resync, stop)
    finally:
        stop.set()
        resync.set()
        for task in (snapshots, flusher):
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
        writer.write({"kind": "event", "local_ns": _now_ns(), "event": "capture_stopped"})
        writer.close()
    return writer.lines_written


async def _stream_loop(
    websockets: Any,
    config: CaptureConfig,
    writer: CaptureWriter,
    resync: asyncio.Event,
    stop: asyncio.Event,
) -> None:
    backoff = 1.0
    while not stop.is_set():
        try:
            async with websockets.connect(config.ws_url, ping_interval=20) as socket:
                backoff = 1.0
                writer.write({"kind": "event", "local_ns": _now_ns(), "event": "ws_connected"})
                resync.set()
                while not stop.is_set():
                    raw = await asyncio.wait_for(socket.recv(), timeout=60.0)
                    writer.write(_ws_record(raw))
        except asyncio.CancelledError:
            raise
        except Exception as error:  # noqa: BLE001 - any failure must be logged, then retried
            writer.write(
                {
                    "kind": "event",
                    "local_ns": _now_ns(),
                    "event": "ws_disconnected",
                    "detail": f"{type(error).__name__}: {error}",
                }
            )
            writer.flush()
            with suppress(TimeoutError, asyncio.TimeoutError):
                await asyncio.wait_for(stop.wait(), timeout=backoff)
            backoff = min(backoff * 2.0, MAX_BACKOFF_SECONDS)


async def _snapshot_loop(
    config: CaptureConfig,
    writer: CaptureWriter,
    resync: asyncio.Event,
    stop: asyncio.Event,
) -> None:
    while not stop.is_set():
        with suppress(TimeoutError, asyncio.TimeoutError):
            await asyncio.wait_for(resync.wait(), timeout=config.snapshot_seconds)
        resync.clear()
        if stop.is_set():
            return
        try:
            payload = await asyncio.to_thread(fetch_depth_snapshot, config)
        except asyncio.CancelledError:
            raise
        except Exception as error:  # noqa: BLE001 - a failed snapshot is data, not a crash
            writer.write(
                {
                    "kind": "event",
                    "local_ns": _now_ns(),
                    "event": "snapshot_failed",
                    "detail": f"{type(error).__name__}: {error}",
                }
            )
            continue
        writer.write({"kind": "snapshot", "local_ns": _now_ns(), "data": payload})


async def _flush_loop(writer: CaptureWriter, interval: float, stop: asyncio.Event) -> None:
    while not stop.is_set():
        with suppress(TimeoutError, asyncio.TimeoutError):
            await asyncio.wait_for(stop.wait(), timeout=interval)
        writer.flush()


def _ws_record(raw: str | bytes) -> dict[str, Any]:
    local_ns = _now_ns()
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"kind": "unparsed", "local_ns": local_ns, "raw": text}
    if isinstance(payload, dict) and "stream" in payload:
        return {
            "kind": "ws",
            "local_ns": local_ns,
            "stream": payload["stream"],
            "data": payload.get("data"),
        }
    return {"kind": "ws", "local_ns": local_ns, "stream": None, "data": payload}


def _install_signal_handlers(stop: asyncio.Event) -> None:
    loop = asyncio.get_running_loop()
    for signal_name in ("SIGINT", "SIGTERM"):
        handle = getattr(signal, signal_name, None)
        if handle is None:  # pragma: no cover - platform dependent
            continue
        with suppress(NotImplementedError):
            loop.add_signal_handler(handle, stop.set)


def _now_ns() -> int:
    return int(datetime.now(UTC).timestamp() * 1_000_000_000)


def capture_paths(root: Path, symbol: str, market: str = "spot") -> Sequence[Path]:
    """Every capture file for ``symbol`` on ``market`` under ``root``, in chronological order."""
    if market not in MARKETS:
        raise ValueError(f"market must be one of {sorted(MARKETS)}")
    directory = Path(root) / (symbol.upper() + MARKETS[market]["label_suffix"])
    if not directory.exists():
        return ()
    return tuple(sorted(directory.glob("*/*.jsonl.gz")))
