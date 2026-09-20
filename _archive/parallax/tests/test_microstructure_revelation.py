"""Each revelation test must find a planted effect and must not find an absent one."""

from __future__ import annotations

import numpy as np
import pytest

from parallax.crypto.microstructure.revelation import (
    decompose_trade_coincidence,
    detection_profile,
    format_revelation,
    withdrawal_amplification,
)

SECOND = 1_000_000_000


def base_columns(rows: int, seed: int = 0) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    return {
        "ts_ns": (np.arange(rows, dtype=np.int64) * SECOND).astype(float),
        "mid": np.full(rows, 100.0),
        "trade_qty": np.abs(rng.normal(2.0, 0.5, size=rows)),
        "trade_imbalance": rng.uniform(-1.0, 1.0, size=rows),
        "depth_bid_25": np.full(rows, 5e5),
        "depth_ask_25": np.full(rows, 5e5),
        "maker_flow_bid": np.zeros(rows),
        "maker_flow_ask": np.zeros(rows),
    }


class TestTradeCoincidence:
    def test_moves_are_attributed_to_the_correct_side_of_the_split(self) -> None:
        columns = base_columns(rows=5)
        columns["mid"] = np.array([100.0, 101.0, 101.0, 102.0, 102.0])
        columns["trade_qty"] = np.array([1.0, 0.0, 1.0, 1.0, 0.0])
        # Moves land at samples 1..4; zero-volume samples are 1 and 4; only sample 1 moved.
        result = decompose_trade_coincidence(columns)
        assert result.n_samples == 4
        assert result.zero_volume_sample_share == pytest.approx(0.5)
        assert result.abs_move_share_zero_volume == pytest.approx(0.5, abs=0.01)

    def test_all_movement_with_trades_scores_zero(self) -> None:
        columns = base_columns(rows=100, seed=3)
        rng = np.random.default_rng(1)
        columns["mid"] = 100.0 * np.exp(np.cumsum(rng.normal(0, 3e-4, 100)))
        result = decompose_trade_coincidence(columns)  # trade_qty is never zero
        assert result.zero_volume_sample_share == 0.0
        assert result.abs_move_share_zero_volume == 0.0

    def test_too_short_input_is_rejected(self) -> None:
        with pytest.raises(ValueError):
            decompose_trade_coincidence(base_columns(rows=1))


def planted_amplification(rows: int, lam: float, seed: int = 4) -> dict[str, np.ndarray]:
    """Per-sample returns follow ``flow^0.5 * exp(lam * withdrawal_state)`` in the flow's sign."""
    rng = np.random.default_rng(seed)
    columns = base_columns(rows, seed=seed)
    qty = np.abs(rng.normal(2.0, 0.8, size=rows)) + 0.1
    imbalance = rng.uniform(-1.0, 1.0, size=rows)
    withdrawn = rng.random(rows) < 0.5  # half the samples have the opposing wall pulling
    pull = np.where(withdrawn, 50.0, 0.0)

    signed_flow = imbalance * qty * 100.0
    magnitude = 0.05 * np.abs(signed_flow) ** 0.5 * np.exp(lam * withdrawn)
    returns_bps = magnitude * np.sign(signed_flow) + rng.normal(0.0, 0.02, size=rows)

    mid = np.empty(rows)
    mid[0] = 100.0
    mid[1:] = 100.0 * np.exp(np.cumsum(returns_bps[:-1]) / 10_000.0)

    columns["mid"] = mid
    columns["trade_qty"] = qty
    columns["trade_imbalance"] = imbalance
    columns["maker_flow_ask"] = np.where(imbalance > 0, -pull, 0.0)
    columns["maker_flow_bid"] = np.where(imbalance <= 0, -pull, 0.0)
    return columns


class TestWithdrawalAmplification:
    def test_a_planted_amplification_is_detected(self) -> None:
        columns = planted_amplification(rows=20_000, lam=1.0)
        result = withdrawal_amplification(columns, window_s=1.0)
        assert result is not None
        assert result.log_ratio == pytest.approx(1.0, abs=0.3)
        assert result.amplifies is True

    def test_no_amplification_is_not_invented(self) -> None:
        columns = planted_amplification(rows=20_000, lam=0.0)
        result = withdrawal_amplification(columns, window_s=1.0)
        assert result is not None
        assert abs(result.log_ratio) < 0.2
        assert result.amplifies is False

    def test_absent_withdrawal_yields_none(self) -> None:
        columns = base_columns(rows=2_000, seed=6)
        rng = np.random.default_rng(2)
        columns["mid"] = 100.0 * np.exp(np.cumsum(rng.normal(0, 3e-4, 2_000)))
        assert withdrawal_amplification(columns, window_s=1.0) is None


def planted_detection(rows: int, lag: int, coupled: bool, seed: int = 8) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    columns = base_columns(rows, seed=seed)
    qty = np.abs(rng.normal(2.0, 0.8, size=rows)) + 0.1
    imbalance = rng.uniform(-1.0, 1.0, size=rows)
    columns["trade_qty"] = qty
    columns["trade_imbalance"] = imbalance

    signed_flow = imbalance * qty * 100.0
    buy = np.maximum(signed_flow, 0.0)
    sell = np.maximum(-signed_flow, 0.0)
    noise_a = np.abs(rng.normal(0.0, 1.0, size=rows))
    noise_b = np.abs(rng.normal(0.0, 1.0, size=rows))
    pulled_ask = noise_a.copy()
    pulled_bid = noise_b.copy()
    if coupled:  # makers pull the challenged side `lag` samples after the flow arrives
        pulled_ask[lag:] += 0.05 * buy[:-lag]
        pulled_bid[lag:] += 0.05 * sell[:-lag]
    columns["maker_flow_ask"] = -pulled_ask
    columns["maker_flow_bid"] = -pulled_bid
    return columns


class TestDetection:
    def test_a_planted_lag_is_found_with_positive_asymmetry(self) -> None:
        columns = planted_detection(rows=30_000, lag=3, coupled=True)
        result = detection_profile(columns, max_lag_s=10.0)
        assert result is not None
        assert result.peak_lag_s == pytest.approx(3.0)
        assert result.makers_detect is True

    def test_uncoupled_series_show_no_asymmetry(self) -> None:
        columns = planted_detection(rows=30_000, lag=3, coupled=False)
        result = detection_profile(columns, max_lag_s=10.0)
        assert result is not None
        assert result.asymmetry_ci_low <= 0.0 <= result.asymmetry_ci_high

    def test_missing_maker_flow_columns_yield_none(self) -> None:
        columns = base_columns(rows=5_000)
        del columns["maker_flow_ask"]
        assert detection_profile(columns) is None

    def test_pairs_straddling_a_gap_are_dropped_not_correlated(self) -> None:
        columns = planted_detection(rows=30_000, lag=3, coupled=True)
        columns["ts_ns"] = columns["ts_ns"].copy()
        columns["ts_ns"][15_000:] += 3_600 * SECOND
        result = detection_profile(columns, max_lag_s=10.0)
        assert result is not None  # both halves still contribute; the seam does not
        assert result.peak_lag_s == pytest.approx(3.0)


def test_report_renders_all_three_sections() -> None:
    columns = planted_amplification(rows=20_000, lam=1.0)
    report = format_revelation(
        decompose_trade_coincidence(columns),
        withdrawal_amplification(columns, window_s=1.0),
        detection_profile(columns, max_lag_s=5.0),
    )
    assert "trade coincidence" in report
    assert "withdrawal amplification" in report
    assert "detection" in report
