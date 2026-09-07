"""Does the governing equation hold? Fit the exponents of price response to flow and depth.

The fluid model proposes ``velocity = pressure / resistance``. Written as a scaling law with the
exponents left free:

```text
directional mid response  ~  k * |net flow| ** delta  *  resting depth ** -gamma
```

The naive fluid form and Kyle (1985) both predict ``delta = 1``. The empirical impact literature
finds ``delta`` close to ``0.5`` (the square-root law), which the locally linear order book model of
Donier, Bonart, Mastromatteo & Bouchaud (2015) derives from a hydrodynamic treatment of *latent*
liquidity rather than visible depth. So this module tests the governing equation directly, before
any latent-state estimation exists to obscure the answer:

* ``delta`` near 1.0 with ``gamma`` near 1.0 supports the naive ratio form;
* ``delta`` near 0.5 reproduces the canonical result and says the equation needs latent liquidity;
* ``gamma`` whose interval contains zero says resting depth does no work at all, and "resistance"
  is not a separately identified force.

This measurement is **contemporaneous and descriptive**. It characterises how price responds to
flow within the same window. It is not a forecast and carries no implication of tradeable edge.

Two design choices keep the statistics defensible. Windows are non-overlapping, which removes the
overlapping-label problem at the source rather than correcting for it afterwards. Exponents are fit
to *bin means* of the directional response rather than to logs of individual observations, because
per-window responses are frequently zero or against the flow, and dropping those would bias the
curve upward exactly where the effect is smallest.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

DEFAULT_WINDOWS_S = (1.0, 5.0, 10.0, 30.0, 60.0, 300.0)
DEFAULT_FLOW_BINS = 12
DEFAULT_DEPTH_BINS = 4
BOOTSTRAP_SAMPLES = 300
NANOS_PER_SECOND = 1_000_000_000
EXPONENT_TOLERANCE = 0.15
"""How far from a candidate exponent still counts as that exponent. See ``_compatible_with``."""


@dataclass(frozen=True)
class WindowSample:
    """Non-overlapping windows of aggregated flow, starting depth, and realised response."""

    flow: np.ndarray
    """Absolute net aggressive flow over the window, in quote notional."""

    resistance: np.ndarray
    """Resting notional on the side opposing the flow, measured at the window start."""

    response: np.ndarray
    """Mid-price move over the window in bps, signed in the direction of the flow."""

    withdrawal: np.ndarray
    """Opposing-side maker withdrawal over the window, in quote notional, non-negative.

    Depth pulled beyond what executions consumed, on the side resisting the net flow. Zero when
    the feature table predates the ``maker_flow_*`` columns.
    """

    window_s: float
    dropped_windows: int

    def __len__(self) -> int:
        return int(self.flow.shape[0])


@dataclass(frozen=True)
class ExponentFit:
    """Fitted scaling exponents with block-bootstrap intervals."""

    window_s: float
    n_windows: int
    n_bins: int
    delta: float
    delta_ci_low: float
    delta_ci_high: float
    gamma: float
    gamma_ci_low: float
    gamma_ci_high: float
    r_squared: float
    delta_small_flow: float
    delta_large_flow: float
    mean_response_bps: float

    @property
    def supports_linear(self) -> bool:
        """Whether the naive ``flow / depth`` form is compatible with the estimate."""
        return self._compatible_with(1.0)

    @property
    def supports_square_root(self) -> bool:
        return self._compatible_with(0.5)

    def _compatible_with(self, target: float) -> bool:
        """Interval containment, widened by a practical tolerance.

        The bootstrap interval captures sampling variability only, not the estimator's own small
        bias or any misspecification. Across a day of capture the interval shrinks below +/- 0.01,
        at which point pure containment becomes a hair trigger: a correctly recovered 0.513 would
        be reported as neither square-root nor linear. Since the two candidate exponents are 0.5
        apart, a tolerance of ``EXPONENT_TOLERANCE`` cannot confuse them.
        """
        if self.delta_ci_low <= target <= self.delta_ci_high:
            return True
        return abs(self.delta - target) <= EXPONENT_TOLERANCE

    @property
    def depth_matters(self) -> bool:
        """False when resting depth does no work, which unidentifies 'resistance'."""
        return not (self.gamma_ci_low <= 0.0 <= self.gamma_ci_high)

    @property
    def single_power_law(self) -> bool:
        """A power law has one exponent. Materially different halves mean it is not one."""
        return abs(self.delta_small_flow - self.delta_large_flow) < 0.25

    def verdict(self) -> str:
        if not self.single_power_law:
            return "not-a-power-law"
        if self.supports_square_root and not self.supports_linear:
            return "square-root"
        if self.supports_linear and not self.supports_square_root:
            return "linear"
        if self.supports_linear and self.supports_square_root:
            return "indeterminate"
        return "other"

    def as_dict(self) -> dict[str, float | bool | str]:
        return {
            "window_s": self.window_s,
            "n_windows": self.n_windows,
            "n_bins": self.n_bins,
            "delta": self.delta,
            "delta_ci_low": self.delta_ci_low,
            "delta_ci_high": self.delta_ci_high,
            "gamma": self.gamma,
            "gamma_ci_low": self.gamma_ci_low,
            "gamma_ci_high": self.gamma_ci_high,
            "r_squared": self.r_squared,
            "delta_small_flow": self.delta_small_flow,
            "delta_large_flow": self.delta_large_flow,
            "mean_response_bps": self.mean_response_bps,
            "depth_matters": self.depth_matters,
            "single_power_law": self.single_power_law,
            "verdict": self.verdict(),
        }


def aggregate_windows(
    columns: dict[str, np.ndarray],
    window_s: float,
    sample_seconds: float = 1.0,
    depth_band: str = "25",
) -> WindowSample:
    """Cut the feature table into non-overlapping windows.

    Resistance is read at the window *start* and taken from the side opposing the net flow, so it
    is predetermined rather than contaminated by the move it is supposed to have resisted. Windows
    whose span does not match the requested duration are dropped: they straddle a capture gap, and
    a gap would otherwise register as an enormous response to very little flow.
    """
    for required in ("ts_ns", "mid", "trade_qty", "trade_imbalance"):
        if required not in columns:
            raise ValueError(f"feature table is missing the {required!r} column")
    bid_column, ask_column = f"depth_bid_{depth_band}", f"depth_ask_{depth_band}"
    if bid_column not in columns or ask_column not in columns:
        raise ValueError(f"feature table has no depth band {depth_band!r}")

    width = int(round(window_s / sample_seconds))
    if width < 1:
        raise ValueError("window must be at least one sample wide")

    ts_ns = columns["ts_ns"]
    mid = columns["mid"]
    # trade_imbalance * trade_qty recovers signed base volume exactly; mid converts it to notional.
    signed_flow = columns["trade_imbalance"] * columns["trade_qty"] * mid

    usable = (ts_ns.shape[0] - 1) // width
    if usable < 1:
        return WindowSample(_empty(), _empty(), _empty(), _empty(), window_s, dropped_windows=0)

    start = np.arange(usable) * width
    end = start + width

    net_flow = signed_flow[: usable * width].reshape(usable, width).sum(axis=1)
    span_ns = ts_ns[end] - ts_ns[start]
    expected_ns = width * sample_seconds * NANOS_PER_SECOND

    response = np.log(mid[end] / mid[start]) * 10_000.0 * np.sign(net_flow)
    resistance = np.where(net_flow > 0.0, columns[ask_column][start], columns[bid_column][start])

    if "maker_flow_bid" in columns and "maker_flow_ask" in columns:
        pulled_ask = _window_sum(columns["maker_flow_ask"], usable, width)
        pulled_bid = _window_sum(columns["maker_flow_bid"], usable, width)
        # maker_flow is base-asset net posting; negative means pulled. Notional via start mid.
        opposing = np.where(net_flow > 0.0, pulled_ask, pulled_bid)
        withdrawal = np.maximum(0.0, -opposing) * mid[start]
    else:
        withdrawal = np.zeros(usable)

    keep = (
        np.isclose(span_ns, expected_ns, rtol=1e-6)
        & (net_flow != 0.0)
        & (resistance > 0.0)
        & np.isfinite(response)
    )
    return WindowSample(
        flow=np.abs(net_flow[keep]),
        resistance=resistance[keep],
        response=response[keep],
        withdrawal=withdrawal[keep],
        window_s=window_s,
        dropped_windows=int(usable - int(keep.sum())),
    )


def _window_sum(values: np.ndarray, usable: int, width: int) -> np.ndarray:
    return values[: usable * width].reshape(usable, width).sum(axis=1)


def fit_exponents(
    flow: np.ndarray,
    resistance: np.ndarray,
    response: np.ndarray,
    window_s: float = 1.0,
    flow_bins: int = DEFAULT_FLOW_BINS,
    depth_bins: int = DEFAULT_DEPTH_BINS,
    seed: int = 0,
    bootstrap_samples: int = BOOTSTRAP_SAMPLES,
) -> ExponentFit | None:
    """Fit ``response ~ k * flow**delta * resistance**-gamma`` on bin means.

    Returns ``None`` when there is not enough data, rather than a fit nobody should trust.
    """
    if not (flow.shape == resistance.shape == response.shape):
        raise ValueError("flow, resistance, and response must share a shape")
    if flow_bins < 3 or depth_bins < 1:
        raise ValueError("need at least three flow bins and one depth bin")

    valid = (flow > 0.0) & (resistance > 0.0) & np.isfinite(response)
    flow, resistance, response = flow[valid], resistance[valid], response[valid]
    if flow.shape[0] < flow_bins * depth_bins * 10:
        return None

    estimate = _fit_once(flow, resistance, response, flow_bins, depth_bins)
    if estimate is None:
        return None
    _, delta, gamma, r_squared, n_bins = estimate

    rng = np.random.default_rng(seed)
    block = max(int(round(10.0 / max(window_s, 1e-9))), 5)
    deltas, gammas = _bootstrap(
        flow, resistance, response, flow_bins, depth_bins, block, rng, bootstrap_samples
    )

    median = np.median(flow)
    small = _fit_once(
        flow[flow <= median], resistance[flow <= median], response[flow <= median], 6, 1
    )
    large = _fit_once(flow[flow > median], resistance[flow > median], response[flow > median], 6, 1)

    return ExponentFit(
        window_s=window_s,
        n_windows=int(flow.shape[0]),
        n_bins=n_bins,
        delta=delta,
        delta_ci_low=float(np.quantile(deltas, 0.05)) if deltas.size else delta,
        delta_ci_high=float(np.quantile(deltas, 0.95)) if deltas.size else delta,
        gamma=gamma,
        gamma_ci_low=float(np.quantile(gammas, 0.05)) if gammas.size else gamma,
        gamma_ci_high=float(np.quantile(gammas, 0.95)) if gammas.size else gamma,
        r_squared=r_squared,
        delta_small_flow=small[1] if small else float("nan"),
        delta_large_flow=large[1] if large else float("nan"),
        mean_response_bps=float(response.mean()),
    )


def _fit_once(
    flow: np.ndarray,
    resistance: np.ndarray,
    response: np.ndarray,
    flow_bins: int,
    depth_bins: int,
) -> tuple[float, float, float, float, int] | None:
    """Bin, average, then regress in log space. Averaging first is what handles zeros.

    Returns ``(intercept, delta, gamma, r_squared, n_bins)``.
    """
    if flow.shape[0] < flow_bins * depth_bins * 5:
        return None
    flow_index = _quantile_bin(flow, flow_bins)
    depth_index = (
        _quantile_bin(resistance, depth_bins) if depth_bins > 1 else np.zeros_like(flow_index)
    )
    cell = flow_index * depth_bins + depth_index
    cell_count = flow_bins * depth_bins

    counts = np.bincount(cell, minlength=cell_count).astype(float)
    mean_response = np.bincount(cell, weights=response, minlength=cell_count)
    mean_flow = np.bincount(cell, weights=flow, minlength=cell_count)
    mean_resistance = np.bincount(cell, weights=resistance, minlength=cell_count)

    populated = counts > 0
    with np.errstate(invalid="ignore", divide="ignore"):
        mean_response = mean_response[populated] / counts[populated]
        mean_flow = mean_flow[populated] / counts[populated]
        mean_resistance = mean_resistance[populated] / counts[populated]
    weights = counts[populated]

    # Only cells whose average response ran with the flow can enter a log fit.
    usable = mean_response > 0.0
    if int(usable.sum()) < 4:
        return None
    target = np.log(mean_response[usable])
    design = np.column_stack(
        [
            np.ones(int(usable.sum())),
            np.log(mean_flow[usable]),
            -np.log(mean_resistance[usable]) if depth_bins > 1 else np.zeros(int(usable.sum())),
        ]
    )
    weight = np.sqrt(weights[usable])
    coefficients, *_ = np.linalg.lstsq(design * weight[:, None], target * weight, rcond=None)

    fitted = design @ coefficients
    residual = float(np.sum(weights[usable] * (target - fitted) ** 2))
    centred = target - np.average(target, weights=weights[usable])
    total = float(np.sum(weights[usable] * centred**2))
    r_squared = 1.0 - residual / total if total > 0.0 else 0.0
    return (
        float(coefficients[0]),
        float(coefficients[1]),
        float(coefficients[2]),
        r_squared,
        int(usable.sum()),
    )


def _bootstrap(
    flow: np.ndarray,
    resistance: np.ndarray,
    response: np.ndarray,
    flow_bins: int,
    depth_bins: int,
    block: int,
    rng: np.random.Generator,
    samples: int,
) -> tuple[np.ndarray, np.ndarray]:
    size = flow.shape[0]
    if size <= block:
        return (np.empty(0), np.empty(0))
    blocks_needed = int(np.ceil(size / block))
    starts_high = size - block + 1

    deltas: list[float] = []
    gammas: list[float] = []
    for _ in range(samples):
        starts = rng.integers(0, starts_high, size=blocks_needed)
        rows = (starts[:, None] + np.arange(block)[None, :]).reshape(-1)[:size]
        estimate = _fit_once(flow[rows], resistance[rows], response[rows], flow_bins, depth_bins)
        if estimate is not None:
            deltas.append(estimate[1])
            gammas.append(estimate[2])
    return (np.asarray(deltas), np.asarray(gammas))


def _quantile_bin(values: np.ndarray, bins: int) -> np.ndarray:
    edges = np.quantile(values, np.linspace(0.0, 1.0, bins + 1)[1:-1])
    return np.searchsorted(edges, values, side="right")


def _empty() -> np.ndarray:
    return np.empty(0, dtype=float)


def sweep_windows(
    columns: dict[str, np.ndarray],
    windows_s: Sequence[float] = DEFAULT_WINDOWS_S,
    sample_seconds: float = 1.0,
    depth_band: str = "25",
    seed: int = 0,
) -> list[ExponentFit]:
    """Fit the scaling law at each aggregation window. The exponent is window dependent."""
    fits: list[ExponentFit] = []
    for window_s in windows_s:
        sample = aggregate_windows(columns, window_s, sample_seconds, depth_band)
        if len(sample) == 0:
            continue
        fit = fit_exponents(
            sample.flow,
            sample.resistance,
            sample.response,
            window_s=window_s,
            seed=seed,
        )
        if fit is not None:
            fits.append(fit)
    return fits


def format_fits(fits: Sequence[ExponentFit]) -> str:
    header = (
        f"{'window_s':>9} {'n':>8} {'delta':>7} {'d_ci':>15} {'gamma':>7} {'g_ci':>15} "
        f"{'r2':>6} {'verdict':>16}"
    )
    lines = [header, "-" * len(header)]
    for fit in fits:
        delta_ci = f"[{fit.delta_ci_low:.2f},{fit.delta_ci_high:.2f}]"
        gamma_ci = f"[{fit.gamma_ci_low:.2f},{fit.gamma_ci_high:.2f}]"
        lines.append(
            f"{fit.window_s:>9.1f} {fit.n_windows:>8d} {fit.delta:>7.3f} {delta_ci:>15} "
            f"{fit.gamma:>7.3f} {gamma_ci:>15} {fit.r_squared:>6.3f} {fit.verdict():>16}"
        )
    return "\n".join(lines)
