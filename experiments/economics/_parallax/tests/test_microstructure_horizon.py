"""The horizon sweep, checked on synthetic data where the right answer is known in advance.

Two cases matter and they are symmetric: a planted edge must be recovered, and a random walk must
be reported as dead. A pipeline that only passes the first test is a pipeline that finds edges in
noise.

The planted edge lives entirely in the next second, so recovering it requires ``execution_lag_s=0``
— the estimator tests pass it explicitly. That the default lag destroys this edge is not a defect
in the fixture; it is the property asserted in ``test_execution_lag_destroys_a_same_instant_edge``.
"""

from __future__ import annotations

import numpy as np
import pytest

from parallax.crypto.microstructure.features import FeatureConfig, feature_columns
from parallax.crypto.microstructure.horizon import (
    DEFAULT_EXECUTION_LAG_S,
    format_results,
    sweep,
)

SECOND = 1_000_000_000


def synthetic_table(
    rows: int = 6_000,
    beta_bps: float = 5.0,
    noise_bps: float = 5.0,
    seed: int = 7,
) -> dict[str, np.ndarray]:
    """Rows on a one-second grid where ``queue_imbalance`` drives the next-second return."""
    rng = np.random.default_rng(seed)
    config = FeatureConfig()
    columns = {name: rng.normal(0.0, 1.0, size=rows) for name in feature_columns(config)}
    signal = rng.uniform(-1.0, 1.0, size=rows)
    columns["queue_imbalance"] = signal

    returns_bps = beta_bps * signal + rng.normal(0.0, noise_bps, size=rows)
    mid = np.empty(rows, dtype=float)
    mid[0] = 100.0
    # Row i predicts the return realised between row i and row i + 1.
    mid[1:] = 100.0 * np.exp(np.cumsum(returns_bps[:-1]) / 10_000.0)

    columns["ts_ns"] = (np.arange(rows, dtype=np.int64) * SECOND).astype(float)
    columns["mid"] = mid
    return columns


def test_a_planted_edge_is_recovered_out_of_sample() -> None:
    results = sweep(
        synthetic_table(), round_trip_cost_bps=0.0, horizons_s=(1.0,), execution_lag_s=0.0
    )
    assert len(results) == 1
    result = results[0]
    assert result.out_of_sample_r2 > 0.1
    assert result.rank_ic > 0.3
    assert result.gross_edge_bps > 2.0
    assert result.long_decile_bps > 0.0 > result.short_decile_bps
    assert result.survives_cost is True


def test_a_planted_edge_dies_once_cost_exceeds_it() -> None:
    results = sweep(
        synthetic_table(), round_trip_cost_bps=50.0, horizons_s=(1.0,), execution_lag_s=0.0
    )
    result = results[0]
    assert result.gross_edge_bps > 0.0
    assert result.net_edge_bps < 0.0
    assert result.survives_cost is False


def test_a_random_walk_is_reported_as_dead() -> None:
    rng = np.random.default_rng(11)
    rows = 6_000
    config = FeatureConfig()
    columns = {name: rng.normal(size=rows) for name in feature_columns(config)}
    columns["ts_ns"] = (np.arange(rows, dtype=np.int64) * SECOND).astype(float)
    columns["mid"] = 100.0 * np.exp(np.cumsum(rng.normal(0.0, 5.0, size=rows)) / 10_000.0)

    results = sweep(columns, round_trip_cost_bps=2.0, horizons_s=(1.0, 5.0))
    assert results
    for result in results:
        assert result.out_of_sample_r2 < 0.01
        assert result.survives_cost is False


def test_the_bootstrap_interval_brackets_the_point_estimate() -> None:
    result = sweep(
        synthetic_table(), round_trip_cost_bps=0.0, horizons_s=(1.0,), execution_lag_s=0.0
    )[0]
    assert result.gross_edge_ci_low_bps <= result.gross_edge_bps <= result.gross_edge_ci_high_bps


def test_horizons_with_too_few_rows_are_skipped_not_faked() -> None:
    columns = synthetic_table(rows=300)
    results = sweep(columns, round_trip_cost_bps=0.0, horizons_s=(1.0, 900.0))
    assert [result.horizon_s for result in results] == [1.0]


def test_split_is_time_ordered() -> None:
    columns = synthetic_table()
    result = sweep(columns, round_trip_cost_bps=0.0, horizons_s=(1.0,), train_fraction=0.5)[0]
    assert result.n_train == pytest.approx(result.n_test, rel=0.01)


def test_execution_lag_destroys_a_same_instant_edge() -> None:
    """The planted edge is only reachable by trading at the mid the signal just measured.

    `synthetic_table` puts all the predictability in the second immediately following each
    observation. A participant who needs even one second to act captures none of it. A sweep that
    reported this edge as tradeable would be reporting an artefact of zero-latency execution.
    """
    columns = synthetic_table()
    instant = sweep(columns, round_trip_cost_bps=0.0, horizons_s=(1.0,), execution_lag_s=0.0)[0]
    lagged = sweep(columns, round_trip_cost_bps=0.0, horizons_s=(1.0,), execution_lag_s=1.0)[0]

    assert instant.survives_cost is True
    assert lagged.rank_ic < 0.05
    assert lagged.gross_edge_bps < 1.0
    assert lagged.survives_cost is False


def test_the_default_lag_is_not_zero() -> None:
    """A default of zero would make the untradeable configuration the one nobody has to ask for."""
    assert DEFAULT_EXECUTION_LAG_S > 0.0
    result = sweep(synthetic_table(), round_trip_cost_bps=0.0, horizons_s=(1.0,))[0]
    assert result.execution_lag_s == DEFAULT_EXECUTION_LAG_S


def test_a_negative_execution_lag_is_rejected() -> None:
    with pytest.raises(ValueError, match="execution_lag_s"):
        sweep(synthetic_table(rows=200), round_trip_cost_bps=0.0, execution_lag_s=-1.0)


def test_training_rows_whose_label_crosses_the_split_are_purged() -> None:
    """Without this, the last horizon of training labels is computed from test-period prices.

    On a one-second grid the leaking region is exactly the horizon plus the execution lag, so the
    purge count is predictable and must scale with the horizon rather than staying constant.
    """
    columns = synthetic_table()
    short, long = sweep(
        columns,
        round_trip_cost_bps=0.0,
        horizons_s=(1.0, 60.0),
        execution_lag_s=1.0,
    )

    assert short.n_purged == pytest.approx(2, abs=1)
    assert long.n_purged == pytest.approx(61, abs=2)
    assert long.n_train < short.n_train, "a longer label window purges more of the training set"


def test_purging_is_subtracted_from_the_training_side_only() -> None:
    """The holdout keeps every labelled row past the split; only the train side pays for the purge.

    Quietly shrinking the holdout instead would buy a cleaner boundary with less evidence, and the
    reported ``n_test`` would no longer describe the partition the metrics came from.
    """
    for result in sweep(
        synthetic_table(), round_trip_cost_bps=0.0, horizons_s=(1.0, 60.0), execution_lag_s=1.0
    ):
        labelled = result.n_train + result.n_purged + result.n_test
        assert result.n_train + result.n_purged == int(labelled * 0.7)
        assert result.n_test == labelled - int(labelled * 0.7)


def test_missing_feature_columns_are_rejected() -> None:
    columns = {
        "ts_ns": (np.arange(100, dtype=np.int64) * SECOND).astype(float),
        "mid": np.full(100, 100.0),
    }
    with pytest.raises(ValueError, match="none of the expected feature columns"):
        sweep(columns, round_trip_cost_bps=0.0)


def test_invalid_train_fraction_is_rejected() -> None:
    with pytest.raises(ValueError):
        sweep(synthetic_table(rows=200), round_trip_cost_bps=0.0, train_fraction=1.0)


def test_a_flat_market_scores_zero_rather_than_a_perfect_rank_ic() -> None:
    """Regression: argsort ranks made a constant label correlate perfectly with a constant fit."""
    rng = np.random.default_rng(3)
    rows = 2_000
    config = FeatureConfig()
    columns = {name: rng.normal(size=rows) for name in feature_columns(config)}
    columns["ts_ns"] = (np.arange(rows, dtype=np.int64) * SECOND).astype(float)
    columns["mid"] = np.full(rows, 100.0)  # price never moves

    result = sweep(columns, round_trip_cost_bps=1.0, horizons_s=(1.0,))[0]
    assert result.rank_ic == 0.0
    assert result.gross_edge_bps == 0.0
    assert result.survives_cost is False


def test_ties_are_ranked_by_average_position_not_by_array_order() -> None:
    from parallax.crypto.microstructure.horizon import _average_ranks

    ranks = _average_ranks(np.array([5.0, 1.0, 5.0, 1.0]))
    assert list(ranks) == [2.5, 0.5, 2.5, 0.5]
    assert list(_average_ranks(np.full(4, 7.0))) == [1.5, 1.5, 1.5, 1.5]


def test_results_render_as_a_table() -> None:
    results = sweep(synthetic_table(), round_trip_cost_bps=1.0, horizons_s=(1.0, 5.0))
    rendered = format_results(results)
    assert "horizon_s" in rendered
    assert "survives" in rendered or "dead" in rendered
    assert len(rendered.splitlines()) == len(results) + 2
