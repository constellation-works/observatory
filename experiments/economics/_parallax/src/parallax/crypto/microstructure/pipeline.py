"""Raw capture to sampled feature table.

Sampling runs on a fixed wall-clock grid rather than per event, so that busy periods do not
dominate the sample purely by producing more rows. Rows are emitted only while the book is
synchronised and recently updated; every skipped sample is counted and reported.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from parallax.crypto.microstructure.book import (
    BookAssembler,
    DesyncError,
    Trade,
    iter_records,
    parse_trade,
)
from parallax.crypto.microstructure.features import DecayState, FeatureConfig, compute_features

NANOS_PER_SECOND = 1_000_000_000


@dataclass
class BuildSummary:
    rows: int = 0
    samples_skipped_desync: int = 0
    samples_skipped_stale: int = 0
    snapshots: int = 0
    gaps: int = 0
    applied_diffs: int = 0
    skipped_diffs: int = 0
    trades: int = 0
    output: Path | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "samples_skipped_desync": self.samples_skipped_desync,
            "samples_skipped_stale": self.samples_skipped_stale,
            "snapshots": self.snapshots,
            "gaps": self.gaps,
            "applied_diffs": self.applied_diffs,
            "skipped_diffs": self.skipped_diffs,
            "trades": self.trades,
            "output": str(self.output) if self.output else None,
        }


@dataclass
class _SamplerState:
    sample_ns: int
    max_stale_ns: int
    config: FeatureConfig
    decay: DecayState
    next_sample_ns: int | None = field(default=None, init=False)
    previous_state: Any = field(default=None, init=False)
    pending_trades: list[Trade] = field(default_factory=list, init=False)


def iter_feature_rows(
    records: Iterable[dict[str, Any]],
    config: FeatureConfig | None = None,
    sample_seconds: float = 1.0,
    max_staleness_seconds: float = 5.0,
    depth_levels: int | None = 200,
    summary: BuildSummary | None = None,
) -> Iterator[dict[str, float]]:
    """Replay capture records and yield one feature row per sample instant."""
    config = config or FeatureConfig()
    summary = summary if summary is not None else BuildSummary()
    assembler = BookAssembler()
    state = _SamplerState(
        sample_ns=int(sample_seconds * NANOS_PER_SECOND),
        max_stale_ns=int(max_staleness_seconds * NANOS_PER_SECOND),
        config=config,
        decay=DecayState(config.flow_half_lives_s),
    )
    last_update_ns = 0

    for record in records:
        kind = record.get("kind")
        local_ns = int(record.get("local_ns") or 0)

        if kind == "snapshot":
            yield from _drain(state, assembler, summary, last_update_ns, local_ns, depth_levels)
            assembler.apply_snapshot(record.get("data") or {})
            last_update_ns = max(last_update_ns, local_ns)
            continue
        if kind != "ws":
            continue

        data = record.get("data") or {}
        event = data.get("e")
        # Every sample instant is drained *before* the event at that instant is applied. Draining
        # afterwards would let an update timestamped at T leak into the sample taken at T, and
        # would measure book freshness against a clock the event had already advanced.
        if event == "depthUpdate":
            event_ns = _event_ns(data.get("E"), local_ns)
            yield from _drain(state, assembler, summary, last_update_ns, event_ns, depth_levels)
            assembler.apply_diff(data)
            last_update_ns = max(last_update_ns, event_ns)
        elif event == "aggTrade":
            trade = parse_trade(data, local_ns)
            summary.trades += 1
            yield from _drain(state, assembler, summary, last_update_ns, trade.ts_ns, depth_levels)
            state.pending_trades.append(trade)
            last_update_ns = max(last_update_ns, trade.ts_ns)

    summary.snapshots = assembler.snapshots
    summary.gaps = assembler.gaps
    summary.applied_diffs = assembler.applied_diffs
    summary.skipped_diffs = assembler.skipped_diffs


def _drain(
    state: _SamplerState,
    assembler: BookAssembler,
    summary: BuildSummary,
    last_update_ns: int,
    now_ns: int,
    depth_levels: int | None,
) -> Iterator[dict[str, float]]:
    """Emit every sample instant that ``now_ns`` has passed."""
    if state.next_sample_ns is None:
        if not assembler.synced:
            return
        state.next_sample_ns = _ceil_to(now_ns, state.sample_ns)

    while state.next_sample_ns is not None and now_ns >= state.next_sample_ns:
        sample_ns = state.next_sample_ns
        state.next_sample_ns = sample_ns + state.sample_ns

        if not assembler.synced:
            summary.samples_skipped_desync += 1
            state.previous_state = None
            state.pending_trades.clear()
            continue
        if sample_ns - last_update_ns > state.max_stale_ns:
            summary.samples_skipped_stale += 1
            state.previous_state = None
            state.pending_trades.clear()
            continue

        try:
            current = assembler.state(sample_ns, depth_levels=depth_levels)
        except DesyncError:
            summary.samples_skipped_desync += 1
            state.previous_state = None
            state.pending_trades.clear()
            continue

        trades = [trade for trade in state.pending_trades if trade.ts_ns <= sample_ns]
        state.pending_trades = [trade for trade in state.pending_trades if trade.ts_ns > sample_ns]

        if state.previous_state is not None:
            row = compute_features(state.previous_state, current, trades, state.config, state.decay)
            if row is not None:
                summary.rows += 1
                yield row
        state.previous_state = current


def build_features(
    paths: Iterable[Path],
    output: Path,
    config: FeatureConfig | None = None,
    sample_seconds: float = 1.0,
    max_staleness_seconds: float = 5.0,
) -> BuildSummary:
    """Build a parquet feature table from capture files."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    summary = BuildSummary()
    rows = list(
        iter_feature_rows(
            iter_records(paths),
            config=config,
            sample_seconds=sample_seconds,
            max_staleness_seconds=max_staleness_seconds,
            summary=summary,
        )
    )
    if not rows:
        raise ValueError(
            "no feature rows produced; counters for diagnosis: "
            f"snapshots={summary.snapshots} gaps={summary.gaps} "
            f"applied_diffs={summary.applied_diffs} skipped_diffs={summary.skipped_diffs} "
            f"trades={summary.trades} skipped_desync={summary.samples_skipped_desync} "
            f"skipped_stale={summary.samples_skipped_stale}"
        )

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pylist(rows)
    pq.write_table(table, output, compression="zstd")
    summary.output = output
    return summary


def _event_ns(exchange_ms: Any, local_ns: int) -> int:
    if exchange_ms is None:
        return local_ns
    return int(exchange_ms) * 1_000_000


def _ceil_to(value: int, step: int) -> int:
    return ((value + step - 1) // step) * step
