"""Is impact mechanical pressure or information revelation? Three tests of the withdrawal story.

The revelation view (Glosten & Milgrom, 1985) says price moves because liquidity providers update
beliefs and withdraw, not because volume pushes. Its observable signature is threefold, and each
part gets its own measurement here:

``decompose_trade_coincidence``
    If flow does the work, mid movement should coincide with volume. The revelation view predicts
    a large share of movement in samples with *no trades at all* — pure quote events.

``withdrawal_amplification``
    At the same flow, windows where the opposing side was pulling depth should move further than
    windows where it held. The mechanical view predicts no difference once flow is controlled.

``detection_profile``
    If makers detect eagerness, withdrawal should *follow* aggressive flow with a consistent lag,
    and the lead-lag relation should be asymmetric: flow leads withdrawal more than withdrawal
    leads flow. This is the closest of the three to a forecast, because withdrawal that begins
    before the move completes is observable in time to act on.

All three are descriptive measurements of coupling, not trading signals. They discipline the form
of the governing equation; the predictive question stays with ``parallax book sweep``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from parallax.crypto.microstructure.impact import aggregate_windows

NANOS_PER_SECOND = 1_000_000_000
AMPLIFICATION_BOOTSTRAP = 200
FLOW_ONLY_BINS = 8


@dataclass(frozen=True)
class TradeCoincidence:
    """How much mid movement happens with no trades in the same sample."""

    n_samples: int
    zero_volume_sample_share: float
    abs_move_share_zero_volume: float
    variance_share_zero_volume: float

    def as_dict(self) -> dict[str, float]:
        return {
            "n_samples": self.n_samples,
            "zero_volume_sample_share": self.zero_volume_sample_share,
            "abs_move_share_zero_volume": self.abs_move_share_zero_volume,
            "variance_share_zero_volume": self.variance_share_zero_volume,
        }


def decompose_trade_coincidence(columns: dict[str, np.ndarray]) -> TradeCoincidence:
    """Split per-sample |mid move| by whether any volume traded in that sample."""
    mid = columns["mid"]
    qty = columns["trade_qty"]
    if mid.shape[0] < 2:
        raise ValueError("need at least two samples")
    move = np.abs(np.diff(np.log(mid))) * 10_000.0
    zero_volume = qty[1:] == 0.0  # the move from t-1 to t belongs to sample t's trades

    total_abs = float(move.sum())
    total_var = float((move**2).sum())
    return TradeCoincidence(
        n_samples=int(move.shape[0]),
        zero_volume_sample_share=float(zero_volume.mean()),
        abs_move_share_zero_volume=float(move[zero_volume].sum() / total_abs)
        if total_abs > 0.0
        else 0.0,
        variance_share_zero_volume=float((move[zero_volume] ** 2).sum() / total_var)
        if total_var > 0.0
        else 0.0,
    )


@dataclass(frozen=True)
class Amplification:
    """Impact per unit flow, low-withdrawal windows against high-withdrawal windows."""

    window_s: float
    n_low: int
    n_high: int
    response_low_bps: float
    response_high_bps: float
    log_ratio: float
    log_ratio_ci_low: float
    log_ratio_ci_high: float

    @property
    def amplifies(self) -> bool:
        """True when high-withdrawal windows move more at the same flow, beyond noise."""
        return self.log_ratio_ci_low > 0.0

    def as_dict(self) -> dict[str, float | bool]:
        return {
            "window_s": self.window_s,
            "n_low": self.n_low,
            "n_high": self.n_high,
            "response_low_bps": self.response_low_bps,
            "response_high_bps": self.response_high_bps,
            "log_ratio": self.log_ratio,
            "log_ratio_ci_low": self.log_ratio_ci_low,
            "log_ratio_ci_high": self.log_ratio_ci_high,
            "amplifies": self.amplifies,
        }


def withdrawal_amplification(
    columns: dict[str, np.ndarray],
    window_s: float = 5.0,
    sample_seconds: float = 1.0,
    depth_band: str = "25",
    seed: int = 0,
) -> Amplification | None:
    """Compare the flow-impact curve between low- and high-withdrawal window terciles.

    Both terciles are evaluated at the *pooled* median flow, so the comparison controls for flow
    rather than confounding "more withdrawal" with "more volume". Returns ``None`` when the data
    cannot support the two fits.
    """
    sample = aggregate_windows(columns, window_s, sample_seconds, depth_band)
    flow, response, withdrawal = sample.flow, sample.response, sample.withdrawal
    if len(sample) < 90 or float(withdrawal.max(initial=0.0)) <= 0.0:
        return None

    low_cut, high_cut = np.quantile(withdrawal, (1.0 / 3.0, 2.0 / 3.0))
    reference = float(np.log(np.median(flow)))

    estimate = _tercile_gap(flow, response, withdrawal, low_cut, high_cut, reference)
    if estimate is None:
        return None
    gap, low_bps, high_bps, n_low, n_high = estimate

    rng = np.random.default_rng(seed)
    block = 20
    gaps = []
    if flow.shape[0] > block:
        blocks_needed = int(np.ceil(flow.shape[0] / block))
        for _ in range(AMPLIFICATION_BOOTSTRAP):
            starts = rng.integers(0, flow.shape[0] - block + 1, size=blocks_needed)
            rows = (starts[:, None] + np.arange(block)[None, :]).reshape(-1)[: flow.shape[0]]
            resampled = _tercile_gap(
                flow[rows], response[rows], withdrawal[rows], low_cut, high_cut, reference
            )
            if resampled is not None:
                gaps.append(resampled[0])
    spread = np.asarray(gaps)

    return Amplification(
        window_s=window_s,
        n_low=n_low,
        n_high=n_high,
        response_low_bps=low_bps,
        response_high_bps=high_bps,
        log_ratio=gap,
        log_ratio_ci_low=float(np.quantile(spread, 0.05)) if spread.size else gap,
        log_ratio_ci_high=float(np.quantile(spread, 0.95)) if spread.size else gap,
    )


def _tercile_gap(
    flow: np.ndarray,
    response: np.ndarray,
    withdrawal: np.ndarray,
    low_cut: float,
    high_cut: float,
    reference_log_flow: float,
) -> tuple[float, float, float, int, int] | None:
    from parallax.crypto.microstructure.impact import _fit_once

    low = withdrawal <= low_cut
    high = withdrawal >= high_cut
    fit_low = _fit_once(flow[low], np.ones(int(low.sum())), response[low], FLOW_ONLY_BINS, 1)
    fit_high = _fit_once(flow[high], np.ones(int(high.sum())), response[high], FLOW_ONLY_BINS, 1)
    if fit_low is None or fit_high is None:
        return None
    log_low = fit_low[0] + fit_low[1] * reference_log_flow
    log_high = fit_high[0] + fit_high[1] * reference_log_flow
    return (
        log_high - log_low,
        float(np.exp(log_low)),
        float(np.exp(log_high)),
        int(low.sum()),
        int(high.sum()),
    )


@dataclass(frozen=True)
class DetectionProfile:
    """Lead-lag structure between aggressive flow and opposing-side withdrawal."""

    lags_s: tuple[float, ...]
    flow_leads_withdrawal: tuple[float, ...]
    withdrawal_leads_flow: tuple[float, ...]
    asymmetry: float
    asymmetry_ci_low: float
    asymmetry_ci_high: float
    peak_lag_s: float

    @property
    def makers_detect(self) -> bool:
        """True when flow leads withdrawal distinctly more than the reverse."""
        return self.asymmetry_ci_low > 0.0

    def as_dict(self) -> dict[str, object]:
        return {
            "lags_s": list(self.lags_s),
            "flow_leads_withdrawal": list(self.flow_leads_withdrawal),
            "withdrawal_leads_flow": list(self.withdrawal_leads_flow),
            "asymmetry": self.asymmetry,
            "asymmetry_ci_low": self.asymmetry_ci_low,
            "asymmetry_ci_high": self.asymmetry_ci_high,
            "peak_lag_s": self.peak_lag_s,
            "makers_detect": self.makers_detect,
        }


def detection_profile(
    columns: dict[str, np.ndarray],
    sample_seconds: float = 1.0,
    max_lag_s: float = 30.0,
    seed: int = 0,
    bootstrap_samples: int = 200,
) -> DetectionProfile | None:
    """Cross-correlate aggressive flow with subsequent opposing-side withdrawal, both directions.

    Buy pressure is paired with ask-side withdrawal and sell pressure with bid-side withdrawal;
    the two orientations are pooled. Pairs that straddle a sampling gap are dropped.
    """
    for name in ("maker_flow_ask", "maker_flow_bid"):
        if name not in columns:
            return None
    ts_ns = columns["ts_ns"]
    mid = columns["mid"]
    signed = columns["trade_imbalance"] * columns["trade_qty"] * mid

    buy = np.maximum(signed, 0.0)
    sell = np.maximum(-signed, 0.0)
    pulled_ask = np.maximum(0.0, -columns["maker_flow_ask"]) * mid
    pulled_bid = np.maximum(0.0, -columns["maker_flow_bid"]) * mid

    step_ns = int(sample_seconds * NANOS_PER_SECOND)
    max_lag = int(round(max_lag_s / sample_seconds))
    if max_lag < 1 or ts_ns.shape[0] < 10 * max_lag:
        return None

    def profile(
        ts: np.ndarray, series: list[tuple[np.ndarray, np.ndarray]]
    ) -> tuple[np.ndarray, np.ndarray]:
        forward = np.empty(max_lag)
        backward = np.empty(max_lag)
        for k in range(1, max_lag + 1):
            forward[k - 1] = _pooled_lagged_corr(ts, series, k, step_ns)
            backward[k - 1] = _pooled_lagged_corr(ts, [(y, x) for x, y in series], k, step_ns)
        return forward, backward

    pairs = [(buy, pulled_ask), (sell, pulled_bid)]
    forward, backward = profile(ts_ns, pairs)
    asymmetry = float(forward.mean() - backward.mean())

    rng = np.random.default_rng(seed)
    n = ts_ns.shape[0]
    block = max(4 * max_lag, 40)
    estimates = []
    if n > block:
        blocks_needed = int(np.ceil(n / block))
        for _ in range(bootstrap_samples):
            starts = rng.integers(0, n - block + 1, size=blocks_needed)
            rows = np.sort((starts[:, None] + np.arange(block)[None, :]).reshape(-1)[:n])
            resampled = [(buy[rows], pulled_ask[rows]), (sell[rows], pulled_bid[rows])]
            f, b = profile(ts_ns[rows], resampled)
            estimates.append(float(f.mean() - b.mean()))
    spread = np.asarray(estimates)

    return DetectionProfile(
        lags_s=tuple(float(k * sample_seconds) for k in range(1, max_lag + 1)),
        flow_leads_withdrawal=tuple(float(v) for v in forward),
        withdrawal_leads_flow=tuple(float(v) for v in backward),
        asymmetry=asymmetry,
        asymmetry_ci_low=float(np.quantile(spread, 0.05)) if spread.size else asymmetry,
        asymmetry_ci_high=float(np.quantile(spread, 0.95)) if spread.size else asymmetry,
        peak_lag_s=float((int(np.argmax(forward)) + 1) * sample_seconds),
    )


def _pooled_lagged_corr(
    ts_ns: np.ndarray,
    pairs: list[tuple[np.ndarray, np.ndarray]],
    lag: int,
    step_ns: int,
) -> float:
    """Correlation of ``x_t`` with ``y_{t+lag}`` pooled over pairs, skipping gapped pairs."""
    n = ts_ns.shape[0]
    index = np.arange(0, n - lag)
    contiguous = np.isclose(
        ts_ns[index + lag] - ts_ns[index], lag * step_ns, rtol=0.0, atol=step_ns * 0.01
    )
    rows = index[contiguous]
    if rows.shape[0] < 30:
        return 0.0
    total = 0.0
    weight = 0.0
    for x, y in pairs:
        a = x[rows]
        b = y[rows + lag]
        sa, sb = a.std(), b.std()
        if sa <= 0.0 or sb <= 0.0:
            continue
        total += float(np.mean((a - a.mean()) * (b - b.mean())) / (sa * sb)) * rows.shape[0]
        weight += rows.shape[0]
    return total / weight if weight > 0.0 else 0.0


def format_revelation(
    coincidence: TradeCoincidence,
    amplification: Amplification | None,
    detection: DetectionProfile | None,
) -> str:
    lines = [
        "trade coincidence",
        f"  samples: {coincidence.n_samples}",
        f"  zero-volume samples: {coincidence.zero_volume_sample_share:.1%}",
        f"  |mid move| in zero-volume samples: {coincidence.abs_move_share_zero_volume:.1%}",
        f"  variance in zero-volume samples: {coincidence.variance_share_zero_volume:.1%}",
        "",
        "withdrawal amplification",
    ]
    if amplification is None:
        lines.append("  insufficient data")
    else:
        lines += [
            f"  window: {amplification.window_s:g}s"
            f"  (n low={amplification.n_low}, high={amplification.n_high})",
            f"  response at median flow, low withdrawal:  {amplification.response_low_bps:.3f} bps",
            "  response at median flow, high withdrawal: "
            f"{amplification.response_high_bps:.3f} bps",
            f"  log ratio: {amplification.log_ratio:+.3f}"
            f"  [{amplification.log_ratio_ci_low:+.3f}, {amplification.log_ratio_ci_high:+.3f}]"
            f"  -> {'amplifies' if amplification.amplifies else 'not established'}",
        ]
    lines += ["", "detection (does withdrawal follow flow?)"]
    if detection is None:
        lines.append("  insufficient data or maker_flow columns missing")
    else:
        lines += [
            "  mean corr, flow -> later withdrawal: "
            f"{np.mean(detection.flow_leads_withdrawal):+.4f}",
            "  mean corr, withdrawal -> later flow: "
            f"{np.mean(detection.withdrawal_leads_flow):+.4f}",
            f"  asymmetry: {detection.asymmetry:+.4f}"
            f"  [{detection.asymmetry_ci_low:+.4f}, {detection.asymmetry_ci_high:+.4f}]"
            f"  -> {'makers detect flow' if detection.makers_detect else 'not established'}",
            f"  peak response lag: {detection.peak_lag_s:g}s",
        ]
    return "\n".join(lines)
