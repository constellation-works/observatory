"""Forward-return labels, including the guard that stops a data gap becoming a fake label."""

from __future__ import annotations

import math

import numpy as np
import pytest

from parallax.crypto.microstructure.labels import forward_return_bps, forward_return_with_window

SECOND = 1_000_000_000


def test_forward_return_looks_one_horizon_ahead() -> None:
    ts = np.arange(4, dtype=np.int64) * SECOND
    mid = np.array([100.0, 101.0, 102.0, 103.0])
    result = forward_return_bps(ts, mid, horizon_s=1.0)
    assert result[0] == pytest.approx(math.log(101 / 100) * 10_000)
    assert result[2] == pytest.approx(math.log(103 / 102) * 10_000)
    assert np.isnan(result[3])


def test_longer_horizons_skip_intermediate_rows() -> None:
    ts = np.arange(5, dtype=np.int64) * SECOND
    mid = np.array([100.0, 101.0, 102.0, 103.0, 104.0])
    result = forward_return_bps(ts, mid, horizon_s=2.0)
    assert result[0] == pytest.approx(math.log(102 / 100) * 10_000)
    assert np.isnan(result[3])
    assert np.isnan(result[4])


def test_a_capture_gap_produces_nan_rather_than_a_hour_long_label() -> None:
    ts = np.array([0, SECOND, 100 * SECOND], dtype=np.int64)
    mid = np.array([100.0, 101.0, 120.0])
    result = forward_return_bps(ts, mid, horizon_s=1.0)
    assert result[0] == pytest.approx(math.log(101 / 100) * 10_000)
    assert np.isnan(result[1]), "the 99-second hole must not masquerade as a 1-second return"


def test_staleness_tolerance_is_configurable() -> None:
    ts = np.array([0, SECOND, 100 * SECOND], dtype=np.int64)
    mid = np.array([100.0, 101.0, 120.0])
    result = forward_return_bps(ts, mid, horizon_s=1.0, max_staleness_s=200.0)
    assert not np.isnan(result[1])


def test_irregular_sampling_takes_the_first_observation_past_the_horizon() -> None:
    ts = np.array([0, int(0.4 * SECOND), int(1.3 * SECOND)], dtype=np.int64)
    mid = np.array([100.0, 100.5, 101.0])
    result = forward_return_bps(ts, mid, horizon_s=1.0)
    assert result[0] == pytest.approx(math.log(101 / 100) * 10_000)


def test_invalid_inputs_are_rejected() -> None:
    ts = np.arange(3, dtype=np.int64) * SECOND
    with pytest.raises(ValueError):
        forward_return_bps(ts, np.array([1.0, 2.0]), horizon_s=1.0)
    with pytest.raises(ValueError):
        forward_return_bps(ts, np.ones(3), horizon_s=0.0)
    with pytest.raises(ValueError):
        forward_return_bps(np.array([2, 1, 0], dtype=np.int64), np.ones(3), horizon_s=1.0)
    with pytest.raises(ValueError, match="execution_lag_s"):
        forward_return_bps(ts, np.ones(3), horizon_s=1.0, execution_lag_s=-1.0)


def test_execution_lag_moves_both_ends_of_the_label_forward() -> None:
    """The label must price the round trip a participant could actually start.

    With a one-second lag, the row observed at t buys at t+1 and sells at t+2 — it never touches
    the move between t and t+1, which is the move it was looking at when it decided.
    """
    ts = np.arange(4, dtype=np.int64) * SECOND
    mid = np.array([100.0, 101.0, 102.0, 103.0])

    instant = forward_return_bps(ts, mid, horizon_s=1.0, execution_lag_s=0.0)
    lagged = forward_return_bps(ts, mid, horizon_s=1.0, execution_lag_s=1.0)

    assert instant[0] == pytest.approx(math.log(101 / 100) * 10_000)
    assert lagged[0] == pytest.approx(math.log(102 / 101) * 10_000)
    assert np.isnan(lagged[2]), "no observation two seconds past row 2 exists"


def test_the_lagged_entry_obeys_the_same_staleness_guard() -> None:
    """A gap between decision and execution is as disqualifying as a gap in the label."""
    ts = np.array([0, 100 * SECOND, 101 * SECOND], dtype=np.int64)
    mid = np.array([100.0, 120.0, 121.0])
    result = forward_return_bps(ts, mid, horizon_s=1.0, execution_lag_s=1.0)
    assert np.isnan(result[0]), "row 0 could not have executed 100 seconds later at that price"


def test_the_window_end_marks_where_each_label_stops_being_usable() -> None:
    """The split purge depends on this: it is the instant a training label stops leaking."""
    ts = np.arange(5, dtype=np.int64) * SECOND
    mid = np.array([100.0, 101.0, 102.0, 103.0, 104.0])

    label, end_ns = forward_return_with_window(ts, mid, horizon_s=2.0, execution_lag_s=1.0)
    assert end_ns[0] == pytest.approx(3 * SECOND), "observe at 0, execute at 1, close at 3"
    assert np.isnan(end_ns[np.isnan(label)]).all(), "an unusable label has no window"
