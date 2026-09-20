"""Forward mid-price returns, the only labels this research uses.

Mid price, never trade price. A series of executed prices carries bid-ask bounce, which induces
negative serial correlation (Roll, 1984) that looks exactly like the mean reversion this project is
hunting and is not tradeable. Labelling on mid removes that artefact by construction.
"""

from __future__ import annotations

import numpy as np

NANOS_PER_SECOND = 1_000_000_000


def forward_return_bps(
    ts_ns: np.ndarray,
    mid: np.ndarray,
    horizon_s: float,
    max_staleness_s: float | None = None,
    execution_lag_s: float = 0.0,
) -> np.ndarray:
    """Log return in basis points over ``horizon_s``, starting ``execution_lag_s`` after each row.

    Rows whose forward observation is missing, or is staler than ``max_staleness_s`` past the
    target time, are ``NaN``. Without that guard a capture gap silently converts a one-second
    label into an hour-long one, which is how a data outage becomes a fictional edge.
    """
    label, _ = forward_return_with_window(
        ts_ns,
        mid,
        horizon_s,
        max_staleness_s=max_staleness_s,
        execution_lag_s=execution_lag_s,
    )
    return label


def forward_return_with_window(
    ts_ns: np.ndarray,
    mid: np.ndarray,
    horizon_s: float,
    max_staleness_s: float | None = None,
    execution_lag_s: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """The label and the instant that closes it, for callers that must purge across a split.

    ``execution_lag_s`` separates the last observation a signal may use from the price it trades
    at. With a lag of zero a predictor buys at the same mid it just measured, which no participant
    can do; that alone can turn a decaying quote into an apparent edge.

    Returns ``(label_bps, end_ts_ns)``. ``end_ts_ns`` is the timestamp of the observation that
    closes each label, and is ``NaN`` wherever the label is — so a train/test split can drop every
    training row whose label window reaches into the test period.
    """
    if ts_ns.ndim != 1 or ts_ns.shape != mid.shape:
        raise ValueError("ts_ns and mid must be 1-D arrays of the same length")
    if horizon_s <= 0.0:
        raise ValueError("horizon must be positive")
    if execution_lag_s < 0.0:
        raise ValueError("execution_lag_s must be non-negative")
    if np.any(np.diff(ts_ns) < 0):
        raise ValueError("ts_ns must be non-decreasing")

    size = ts_ns.shape[0]
    label = np.full(size, np.nan, dtype=float)
    end_ns = np.full(size, np.nan, dtype=float)
    if size == 0:
        return label, end_ns

    staleness_ns = (
        max_staleness_s if max_staleness_s is not None else max(horizon_s * 0.5, 1.0)
    ) * NANOS_PER_SECOND

    # The signal is observed at ts_ns, executes at entry_target, and is closed one horizon later.
    entry_target = ts_ns + execution_lag_s * NANOS_PER_SECOND
    if execution_lag_s == 0.0:
        # Trade on the observing row itself, so repeated timestamps resolve to their own row
        # rather than collapsing onto the first observation sharing that instant.
        entry = np.arange(size)
        entry_ok = np.ones(size, dtype=bool)
    else:
        entry, entry_ok = _first_observation_at_or_after(ts_ns, entry_target, staleness_ns)
    exit_index, exit_ok = _first_observation_at_or_after(
        ts_ns, entry_target + horizon_s * NANOS_PER_SECOND, staleness_ns
    )

    usable = entry_ok & exit_ok & (mid[entry] > 0.0) & (mid[exit_index] > 0.0)
    label[usable] = np.log(mid[exit_index[usable]] / mid[entry[usable]]) * 10_000.0
    end_ns[usable] = ts_ns[exit_index[usable]]
    return label, end_ns


def _first_observation_at_or_after(
    ts_ns: np.ndarray, target_ns: np.ndarray, staleness_ns: float
) -> tuple[np.ndarray, np.ndarray]:
    """Index of the first observation at or after each target, and whether it is fresh enough."""
    index = np.searchsorted(ts_ns, target_ns, side="left")
    within_range = index < ts_ns.shape[0]
    clipped = np.minimum(index, ts_ns.shape[0] - 1)
    fresh = (ts_ns[clipped] - target_ns) <= staleness_ns
    return clipped, within_range & fresh
