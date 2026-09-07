"""The estimator is only worth running if it recovers exponents that were planted deliberately.

Each test generates data from a known scaling law and asks the fitter to find it back. A fitter
that cannot tell 0.5 from 1.0 on synthetic data cannot adjudicate the fluid model on real data.
"""

from __future__ import annotations

import numpy as np
import pytest

from parallax.crypto.microstructure.impact import (
    aggregate_windows,
    fit_exponents,
    format_fits,
    sweep_windows,
)

SECOND = 1_000_000_000


def planted(
    delta: float,
    gamma: float,
    rows: int = 40_000,
    noise_bps: float = 2.0,
    seed: int = 5,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Windows drawn from ``response = flow**delta * resistance**-gamma`` plus zero-mean noise."""
    rng = np.random.default_rng(seed)
    flow = np.exp(rng.normal(11.0, 1.2, size=rows))  # notional, spanning ~2 decades
    resistance = np.exp(rng.normal(13.0, 0.8, size=rows))
    scale = 3.0 * np.exp(-11.0 * delta + 13.0 * gamma)
    response = scale * flow**delta * resistance ** (-gamma)
    response = response + rng.normal(0.0, noise_bps, size=rows)
    return flow, resistance, response


def test_a_square_root_law_is_recovered() -> None:
    fit = fit_exponents(*planted(delta=0.5, gamma=1.0), window_s=10.0)
    assert fit is not None
    assert fit.delta == pytest.approx(0.5, abs=0.08)
    assert fit.gamma == pytest.approx(1.0, abs=0.12)
    assert fit.supports_square_root is True
    assert fit.supports_linear is False
    assert fit.verdict() == "square-root"


def test_a_linear_law_is_recovered_and_distinguished() -> None:
    fit = fit_exponents(*planted(delta=1.0, gamma=1.0), window_s=10.0)
    assert fit is not None
    assert fit.delta == pytest.approx(1.0, abs=0.08)
    assert fit.supports_linear is True
    assert fit.supports_square_root is False
    assert fit.verdict() == "linear"


def test_depth_that_does_no_work_yields_a_gamma_interval_containing_zero() -> None:
    fit = fit_exponents(*planted(delta=0.5, gamma=0.0), window_s=10.0)
    assert fit is not None
    assert fit.gamma == pytest.approx(0.0, abs=0.1)
    assert fit.depth_matters is False


def test_depth_that_does_work_is_detected() -> None:
    fit = fit_exponents(*planted(delta=0.5, gamma=1.0), window_s=10.0)
    assert fit is not None
    assert fit.depth_matters is True


def test_the_bootstrap_interval_brackets_the_estimate() -> None:
    fit = fit_exponents(*planted(delta=0.5, gamma=1.0), window_s=10.0)
    assert fit is not None
    assert fit.delta_ci_low <= fit.delta <= fit.delta_ci_high
    assert fit.gamma_ci_low <= fit.gamma <= fit.gamma_ci_high
    assert fit.delta_ci_high > fit.delta_ci_low


def test_a_kinked_law_is_flagged_as_not_a_power_law() -> None:
    """Two different exponents spliced together must not be reported as one clean scaling."""
    flow, resistance, _ = planted(delta=0.5, gamma=1.0)
    median = np.median(flow)
    exponent = np.where(flow <= median, 0.2, 1.4)
    response = 3.0 * np.exp(-11.0 * exponent + 13.0) * flow**exponent * resistance**-1.0
    fit = fit_exponents(flow, resistance, response, window_s=10.0)
    assert fit is not None
    assert fit.single_power_law is False
    assert fit.verdict() == "not-a-power-law"


def test_pure_noise_does_not_produce_a_confident_exponent() -> None:
    rng = np.random.default_rng(2)
    rows = 40_000
    flow = np.exp(rng.normal(11.0, 1.2, size=rows))
    resistance = np.exp(rng.normal(13.0, 0.8, size=rows))
    response = rng.normal(0.0, 2.0, size=rows)
    fit = fit_exponents(flow, resistance, response, window_s=10.0)
    if fit is not None:
        assert fit.delta_ci_low <= 0.0 <= fit.delta_ci_high or fit.r_squared < 0.2


def test_a_tight_interval_does_not_make_the_verdict_a_hair_trigger() -> None:
    """Regression: a correct 0.513 with a +/-0.005 interval was reported as neither exponent."""
    fit = fit_exponents(*planted(delta=0.5, gamma=1.0, rows=200_000, seed=9), window_s=1.0)
    assert fit is not None
    assert fit.delta_ci_high - fit.delta_ci_low < 0.05, "this test needs a tight interval"
    assert fit.supports_square_root is True
    assert fit.supports_linear is False
    assert fit.verdict() == "square-root"


def test_the_tolerance_cannot_confuse_the_two_candidate_exponents() -> None:
    square_root = fit_exponents(*planted(delta=0.5, gamma=1.0), window_s=10.0)
    linear = fit_exponents(*planted(delta=1.0, gamma=1.0), window_s=10.0)
    assert square_root is not None and linear is not None
    assert square_root.supports_linear is False
    assert linear.supports_square_root is False


def test_an_exponent_between_the_candidates_matches_neither() -> None:
    fit = fit_exponents(*planted(delta=0.75, gamma=1.0), window_s=10.0)
    assert fit is not None
    assert fit.supports_square_root is False
    assert fit.supports_linear is False
    assert fit.verdict() == "other"


def test_too_little_data_returns_none_rather_than_a_fit() -> None:
    assert fit_exponents(*planted(delta=0.5, gamma=1.0, rows=100), window_s=10.0) is None


def test_mismatched_input_shapes_are_rejected() -> None:
    with pytest.raises(ValueError):
        fit_exponents(np.ones(10), np.ones(9), np.ones(10))
    with pytest.raises(ValueError):
        fit_exponents(np.ones(100), np.ones(100), np.ones(100), flow_bins=2)


def feature_columns_for_windows(rows: int = 4_000, seed: int = 1) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    returns_bps = rng.normal(0.0, 3.0, size=rows)
    return {
        "ts_ns": (np.arange(rows, dtype=np.int64) * SECOND).astype(float),
        "mid": 100.0 * np.exp(np.cumsum(returns_bps) / 10_000.0),
        "trade_qty": np.abs(rng.normal(2.0, 0.5, size=rows)),
        "trade_imbalance": rng.uniform(-1.0, 1.0, size=rows),
        "depth_bid_25": np.abs(rng.normal(500_000.0, 50_000.0, size=rows)),
        "depth_ask_25": np.abs(rng.normal(500_000.0, 50_000.0, size=rows)),
    }


def test_windows_are_non_overlapping_and_sized_correctly() -> None:
    columns = feature_columns_for_windows(rows=4_000)
    sample = aggregate_windows(columns, window_s=10.0, sample_seconds=1.0)
    assert len(sample) == pytest.approx(399, abs=2)
    assert sample.window_s == 10.0
    assert np.all(sample.flow >= 0.0)
    assert np.all(sample.resistance > 0.0)


def test_windows_spanning_a_capture_gap_are_dropped() -> None:
    columns = feature_columns_for_windows(rows=1_000)
    columns["ts_ns"] = columns["ts_ns"].copy()
    columns["ts_ns"][500:] += 3_600 * SECOND  # an hour-long hole
    sample = aggregate_windows(columns, window_s=10.0, sample_seconds=1.0)
    assert sample.dropped_windows >= 1
    intact = aggregate_windows(feature_columns_for_windows(rows=1_000), window_s=10.0)
    assert len(sample) < len(intact)


def test_resistance_is_taken_from_the_side_opposing_the_flow() -> None:
    rows = 200
    columns = {
        "ts_ns": (np.arange(rows, dtype=np.int64) * SECOND).astype(float),
        "mid": np.full(rows, 100.0),
        "trade_qty": np.ones(rows),
        "trade_imbalance": np.ones(rows),  # every window is net buying
        "depth_bid_25": np.full(rows, 111.0),
        "depth_ask_25": np.full(rows, 999.0),
    }
    buying = aggregate_windows(columns, window_s=10.0)
    assert np.all(buying.resistance == 999.0), "net buying must be resisted by ask depth"

    columns["trade_imbalance"] = -np.ones(rows)
    selling = aggregate_windows(columns, window_s=10.0)
    assert np.all(selling.resistance == 111.0), "net selling must be resisted by bid depth"


def test_missing_columns_are_rejected() -> None:
    columns = feature_columns_for_windows(rows=200)
    with pytest.raises(ValueError, match="depth band"):
        aggregate_windows(columns, window_s=10.0, depth_band="999")
    del columns["trade_qty"]
    with pytest.raises(ValueError, match="trade_qty"):
        aggregate_windows(columns, window_s=10.0)


def test_sweep_returns_a_fit_per_viable_window_and_renders() -> None:
    columns = feature_columns_for_windows(rows=60_000)
    fits = sweep_windows(columns, windows_s=(1.0, 5.0), sample_seconds=1.0)
    assert fits
    rendered = format_fits(fits)
    assert "window_s" in rendered
    assert len(rendered.splitlines()) == len(fits) + 2
