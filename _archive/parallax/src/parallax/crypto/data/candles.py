"""Canonical candle contract shared by exchange adapters."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from hashlib import sha256
from math import isfinite
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Candle:
    venue: str
    symbol: str
    interval: str
    open_time_ms: int
    close_time_ms: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    quote_volume: float | None = None
    trade_count: int | None = None

    def __post_init__(self) -> None:
        if not self.venue or not self.symbol or not self.interval:
            raise ValueError("venue, symbol, and interval are required")
        if self.open_time_ms < 0 or self.close_time_ms <= self.open_time_ms:
            raise ValueError("candle timestamps are invalid")
        prices = (self.open, self.high, self.low, self.close)
        if any(not isfinite(value) or value <= 0.0 for value in prices):
            raise ValueError("candle prices must be finite and positive")
        if not isfinite(self.volume) or self.volume < 0.0:
            raise ValueError("candle volume must be finite and non-negative")
        if self.quote_volume is not None and (
            not isfinite(self.quote_volume) or self.quote_volume < 0.0
        ):
            raise ValueError("quote volume must be finite and non-negative")
        if self.trade_count is not None and self.trade_count < 0:
            raise ValueError("trade count must be non-negative")
        if self.low > min(self.open, self.close) or self.high < max(self.open, self.close):
            raise ValueError("open and close must fall within low and high")
        if self.low > self.high:
            raise ValueError("candle low must not exceed high")

    @property
    def utc_date(self) -> str:
        return datetime.fromtimestamp(self.open_time_ms / 1000, tz=UTC).date().isoformat()

    def record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WriteSummary:
    rows: int
    files: tuple[Path, ...]
    missing_minutes: int


def write_candle_stream(
    root: Path,
    pages: Iterable[tuple[Candle, ...]],
    *,
    expected_start_ms: int | None = None,
    expected_end_ms: int | None = None,
) -> WriteSummary:
    """Write immutable, deterministic daily Parquet partitions from sorted candle pages.

    A repeated identical backfill is idempotent. If an existing UTC-day partition differs, the
    write fails instead of silently rewriting historical raw data.
    """

    pending: list[Candle] = []
    current_date: str | None = None
    files: list[Path] = []
    rows = 0
    missing_minutes = 0

    for page in pages:
        for candle in page:
            if current_date is not None and candle.utc_date != current_date:
                path, unique_count, missing = _write_day(root, pending)
                files.append(path)
                rows += unique_count
                missing_minutes += missing
                pending = []
            current_date = candle.utc_date
            pending.append(candle)

    if pending:
        path, unique_count, missing = _write_day(root, pending)
        files.append(path)
        rows += unique_count
        missing_minutes += missing

    if expected_start_ms is not None or expected_end_ms is not None:
        if expected_start_ms is None or expected_end_ms is None:
            raise ValueError("expected start and end must be provided together")
        expected_rows = (expected_end_ms - expected_start_ms) // 60_000
        missing_minutes = max(0, expected_rows - rows)

    return WriteSummary(rows=rows, files=tuple(files), missing_minutes=missing_minutes)


def _write_day(root: Path, candles: list[Candle]) -> tuple[Path, int, int]:
    unique = _deduplicate(candles)
    first = unique[0]
    date = datetime.fromtimestamp(first.open_time_ms / 1000, tz=UTC)
    directory = root / first.venue / first.symbol / first.interval / f"{date:%Y}" / f"{date:%m}"
    target = directory / f"{date:%d}.parquet"
    records = [candle.record() for candle in unique]
    digest = _content_digest(records)

    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError as error:  # pragma: no cover - exercised by the installed CLI environment
        raise RuntimeError("Parquet output requires `uv sync --group dev`") from error

    metadata = {
        b"parallax.schema": b"candles.v1",
        b"parallax.content_sha256": digest.encode(),
        b"parallax.rows": str(len(records)).encode(),
        b"parallax.utc_date": first.utc_date.encode(),
    }
    if target.exists():
        existing = pq.read_metadata(target).metadata or {}
        if existing.get(b"parallax.content_sha256") == digest.encode():
            return target, len(records), _missing_minutes(unique)
        raise FileExistsError(f"immutable candle partition differs: {target}")

    directory.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(records).replace_schema_metadata(metadata)
    temporary = target.with_suffix(".parquet.tmp")
    pq.write_table(table, temporary, compression="zstd")
    temporary.replace(target)
    return target, len(records), _missing_minutes(unique)


def _deduplicate(candles: list[Candle]) -> list[Candle]:
    by_time: dict[int, Candle] = {}
    for candle in candles:
        existing = by_time.get(candle.open_time_ms)
        if existing is not None and existing != candle:
            raise ValueError(f"conflicting candles at {candle.open_time_ms}")
        by_time[candle.open_time_ms] = candle
    return [by_time[key] for key in sorted(by_time)]


def _missing_minutes(candles: list[Candle]) -> int:
    if not candles or candles[0].interval != "1m":
        return 0
    return max(0, 1_440 - len(candles))


def _content_digest(records: list[dict[str, Any]]) -> str:
    import json

    payload = json.dumps(records, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(payload.encode()).hexdigest()
