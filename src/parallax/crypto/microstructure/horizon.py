"""Does book state predict forward mid returns, at what horizon, and does it beat cost?

This is deliberately a conditional-expectation study rather than a backtest. Fitting
``E[forward return | book state]`` on every sampled instant uses orders of magnitude more
observations than counting discretionary trades, so the horizon at which any predictability decays
can be measured in a day of data instead of a season of trading. If the conditional mean is flat,
no execution scheme rescues it, and the idea can be discarded cheaply.

Five guards keep the answer honest:

* the split is time-ordered, never random, because random splits leak the future into the past;
* training rows whose label window reaches past the split are purged, because a time-ordered split
  alone still lets the last horizon of training labels be computed from test-period prices;
* the signal executes an ``execution_lag_s`` after the last observation it uses, because a
  predictor that trades at the mid it just measured is not one anybody can run;
* every number that matters is out-of-sample, fitted on train statistics only;
* confidence intervals come from a moving-block bootstrap, because overlapping forward-return
  labels are strongly autocorrelated and ordinary standard errors would be far too small.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from parallax.crypto.microstructure.features import FeatureConfig, feature_columns
from parallax.crypto.microstructure.labels import forward_return_with_window

DEFAULT_HORIZONS_S = (1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 300.0, 900.0)
CONFIDENT_FRACTION = 0.1
BOOTSTRAP_SAMPLES = 500
DEFAULT_EXECUTION_LAG_S = 1.0


@dataclass(frozen=True)
class HorizonResult:
    """Out-of-sample predictability at one horizon, priced against round-trip cost."""

    horizon_s: float
    execution_lag_s: float
    n_train: int
    n_test: int
    n_purged: int
    in_sample_r2: float
    out_of_sample_r2: float
    rank_ic: float
    long_decile_bps: float
    short_decile_bps: float
    gross_edge_bps: float
    gross_edge_ci_low_bps: float
    gross_edge_ci_high_bps: float
    round_trip_cost_bps: float

    @property
    def net_edge_bps(self) -> float:
        return self.gross_edge_bps - self.round_trip_cost_bps

    @property
    def survives_cost(self) -> bool:
        """True only when the *lower* bootstrap bound clears cost.

        The point estimate clearing cost is not enough to promote anything.
        """
        return self.gross_edge_ci_low_bps > self.round_trip_cost_bps

    def as_dict(self) -> dict[str, float | bool]:
        return {
            "horizon_s": self.horizon_s,
            "execution_lag_s": self.execution_lag_s,
            "n_train": self.n_train,
            "n_test": self.n_test,
            "n_purged": self.n_purged,
            "in_sample_r2": self.in_sample_r2,
            "out_of_sample_r2": self.out_of_sample_r2,
            "rank_ic": self.rank_ic,
            "long_decile_bps": self.long_decile_bps,
            "short_decile_bps": self.short_decile_bps,
            "gross_edge_bps": self.gross_edge_bps,
            "gross_edge_ci_low_bps": self.gross_edge_ci_low_bps,
            "gross_edge_ci_high_bps": self.gross_edge_ci_high_bps,
            "round_trip_cost_bps": self.round_trip_cost_bps,
            "net_edge_bps": self.net_edge_bps,
            "survives_cost": self.survives_cost,
        }


def load_feature_table(path: Path) -> dict[str, np.ndarray]:
    """Read a feature parquet into column arrays, sorted by timestamp."""
    import pyarrow.parquet as pq

    table = pq.read_table(Path(path))
    columns = {
        name: table[name].to_numpy(zero_copy_only=False).astype(float)
        for name in table.column_names
    }
    order = np.argsort(columns["ts_ns"], kind="stable")
    return {name: values[order] for name, values in columns.items()}


def sweep(
    columns: dict[str, np.ndarray],
    round_trip_cost_bps: float,
    horizons_s: Sequence[float] = DEFAULT_HORIZONS_S,
    config: FeatureConfig | None = None,
    train_fraction: float = 0.7,
    sample_seconds: float = 1.0,
    seed: int = 0,
    execution_lag_s: float = DEFAULT_EXECUTION_LAG_S,
) -> list[HorizonResult]:
    """Fit and evaluate the book-state predictor at each horizon.

    ``execution_lag_s`` is the delay between the last observation a signal uses and the price it
    trades at. It defaults to one sample rather than zero: a zero-lag result is not reachable by
    any participant, so it belongs in a sensitivity check, never in the headline sweep.
    """
    config = config or FeatureConfig()
    names = [name for name in feature_columns(config) if name in columns]
    if not names:
        raise ValueError("feature table contains none of the expected feature columns")
    if not 0.0 < train_fraction < 1.0:
        raise ValueError("train_fraction must lie strictly between 0 and 1")
    if execution_lag_s < 0.0:
        raise ValueError("execution_lag_s must be non-negative")

    ts_ns = columns["ts_ns"]
    mid = columns["mid"]
    design = np.column_stack([columns[name] for name in names])

    results: list[HorizonResult] = []
    for horizon in horizons_s:
        label, label_end_ns = forward_return_with_window(
            ts_ns, mid, horizon, execution_lag_s=execution_lag_s
        )
        keep = np.isfinite(label) & np.all(np.isfinite(design), axis=1)
        result = _evaluate(
            design[keep],
            label[keep],
            ts_ns[keep],
            label_end_ns[keep],
            horizon_s=horizon,
            execution_lag_s=execution_lag_s,
            round_trip_cost_bps=round_trip_cost_bps,
            train_fraction=train_fraction,
            sample_seconds=sample_seconds,
            seed=seed,
        )
        if result is not None:
            results.append(result)
    return results


def _evaluate(
    design: np.ndarray,
    label: np.ndarray,
    ts_ns: np.ndarray,
    label_end_ns: np.ndarray,
    horizon_s: float,
    execution_lag_s: float,
    round_trip_cost_bps: float,
    train_fraction: float,
    sample_seconds: float,
    seed: int,
) -> HorizonResult | None:
    total = design.shape[0]
    split = int(total * train_fraction)
    if split < 50 or total - split < 50:
        return None

    # Purge the boundary. A training row observed before the split whose label closes at or after
    # the first test observation was scored on test-period prices; keeping it trains the model on
    # the very window it is about to be judged on. At a 900 s horizon that is ~900 rows.
    test_start_ns = ts_ns[split]
    train_rows = np.flatnonzero(label_end_ns[:split] < test_start_ns)
    n_purged = split - train_rows.shape[0]
    if train_rows.shape[0] < 50:
        return None

    train_x, test_x = design[train_rows], design[split:]
    train_y, test_y = label[train_rows], label[split:]

    mean = train_x.mean(axis=0)
    scale = train_x.std(axis=0)
    scale[scale <= 0.0] = 1.0
    train_z = (train_x - mean) / scale
    test_z = (test_x - mean) / scale

    train_design = np.column_stack([np.ones(train_z.shape[0]), train_z])
    test_design = np.column_stack([np.ones(test_z.shape[0]), test_z])
    coefficients, *_ = np.linalg.lstsq(train_design, train_y, rcond=None)

    train_prediction = train_design @ coefficients
    test_prediction = test_design @ coefficients

    in_sample_r2 = _r2(train_y, train_prediction, train_y.mean())
    out_of_sample_r2 = _r2(test_y, test_prediction, train_y.mean())
    rank_ic = _rank_correlation(test_prediction, test_y)

    long_decile_bps, short_decile_bps = _decile_returns(test_prediction, test_y)
    contribution = test_y * np.sign(test_prediction)
    threshold = np.quantile(np.abs(test_prediction), 1.0 - CONFIDENT_FRACTION)
    confident = np.abs(test_prediction) >= threshold
    gross_edge_bps = float(contribution[confident].mean()) if confident.any() else 0.0

    block = max(int(np.ceil(horizon_s / max(sample_seconds, 1e-9))) * 2, 10)
    low, high = _block_bootstrap_interval(contribution, confident, block, seed)

    return HorizonResult(
        horizon_s=horizon_s,
        execution_lag_s=execution_lag_s,
        n_train=train_rows.shape[0],
        n_test=total - split,
        n_purged=n_purged,
        in_sample_r2=in_sample_r2,
        out_of_sample_r2=out_of_sample_r2,
        rank_ic=rank_ic,
        long_decile_bps=long_decile_bps,
        short_decile_bps=short_decile_bps,
        gross_edge_bps=gross_edge_bps,
        gross_edge_ci_low_bps=low,
        gross_edge_ci_high_bps=high,
        round_trip_cost_bps=round_trip_cost_bps,
    )


def _r2(actual: np.ndarray, predicted: np.ndarray, baseline: float) -> float:
    residual = float(np.sum((actual - predicted) ** 2))
    total = float(np.sum((actual - baseline) ** 2))
    if total <= 0.0:
        return 0.0
    return 1.0 - residual / total


def _rank_correlation(left: np.ndarray, right: np.ndarray) -> float:
    """Spearman correlation with tie-aware ranks.

    Ties are the common case here, not an edge case: queue imbalance is exactly zero whenever the
    touch is symmetric, and traded quantity is exactly zero in any quiet sample. Ranking by plain
    ``argsort`` would break those ties by array position, which manufactures correlation out of
    time order. A degenerate input has zero rank variance and correctly scores zero.
    """
    if left.size < 2:
        return 0.0
    left_ranks = _average_ranks(left)
    right_ranks = _average_ranks(right)
    left_ranks -= left_ranks.mean()
    right_ranks -= right_ranks.mean()
    denominator = float(np.sqrt(np.sum(left_ranks**2) * np.sum(right_ranks**2)))
    if denominator <= 0.0:
        return 0.0
    return float(np.sum(left_ranks * right_ranks) / denominator)


def _average_ranks(values: np.ndarray) -> np.ndarray:
    """Ranks in ``[0, n - 1]``, with tied values sharing the average of their positions."""
    size = values.shape[0]
    order = np.argsort(values, kind="stable")
    ordered = values[order]

    starts_group = np.empty(size, dtype=bool)
    starts_group[0] = True
    np.not_equal(ordered[1:], ordered[:-1], out=starts_group[1:])

    group_start = np.flatnonzero(starts_group)
    group_size = np.diff(np.append(group_start, size))
    group_rank = group_start + (group_size - 1) / 2.0

    ranks = np.empty(size, dtype=float)
    ranks[order] = group_rank[np.cumsum(starts_group) - 1]
    return ranks


def _decile_returns(prediction: np.ndarray, actual: np.ndarray) -> tuple[float, float]:
    if prediction.size < 10:
        return (0.0, 0.0)
    upper = np.quantile(prediction, 1.0 - CONFIDENT_FRACTION)
    lower = np.quantile(prediction, CONFIDENT_FRACTION)
    top = actual[prediction >= upper]
    bottom = actual[prediction <= lower]
    return (
        float(top.mean()) if top.size else 0.0,
        float(bottom.mean()) if bottom.size else 0.0,
    )


def _block_bootstrap_interval(
    contribution: np.ndarray,
    confident: np.ndarray,
    block: int,
    seed: int,
    samples: int = BOOTSTRAP_SAMPLES,
) -> tuple[float, float]:
    """Moving-block bootstrap over time-ordered rows, preserving label overlap."""
    n = contribution.shape[0]
    if n <= block or not confident.any():
        return (0.0, 0.0)
    rng = np.random.default_rng(seed)
    blocks_needed = int(np.ceil(n / block))
    starts_high = n - block + 1

    estimates = np.empty(samples, dtype=float)
    for index in range(samples):
        starts = rng.integers(0, starts_high, size=blocks_needed)
        rows = (starts[:, None] + np.arange(block)[None, :]).reshape(-1)[:n]
        selected = confident[rows]
        estimates[index] = contribution[rows][selected].mean() if selected.any() else np.nan
    finite = estimates[np.isfinite(estimates)]
    if finite.size == 0:
        return (0.0, 0.0)
    return (float(np.quantile(finite, 0.05)), float(np.quantile(finite, 0.95)))


def format_results(results: Sequence[HorizonResult]) -> str:
    """Render the sweep as a fixed-width table for the CLI."""
    header = (
        f"{'horizon_s':>10} {'lag_s':>7} {'n_test':>9} {'purged':>8} {'oos_r2':>9} {'rank_ic':>8} "
        f"{'gross_bps':>10} {'ci_low':>8} {'ci_high':>8} {'net_bps':>9} {'verdict':>8}"
    )
    lines = [header, "-" * len(header)]
    for result in results:
        verdict = "survives" if result.survives_cost else "dead"
        lines.append(
            f"{result.horizon_s:>10.1f} {result.execution_lag_s:>7.2f} {result.n_test:>9d} "
            f"{result.n_purged:>8d} {result.out_of_sample_r2:>9.5f} "
            f"{result.rank_ic:>8.4f} {result.gross_edge_bps:>10.3f} "
            f"{result.gross_edge_ci_low_bps:>8.3f} {result.gross_edge_ci_high_bps:>8.3f} "
            f"{result.net_edge_bps:>9.3f} {verdict:>8}"
        )
    return "\n".join(lines)
