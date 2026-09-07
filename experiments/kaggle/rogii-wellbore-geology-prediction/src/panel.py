"""Panel local-projection experiment for TVT movement.

Each well is a panel and measured depth is its ordered index.  For every
horizon ``h=1..max_lag`` the experiment learns a separate regression for

    TVT[t+h] - TVT[t]

from signed X/Y/Z movement and gamma-ray change.  Training windows come only
from the observed pre-Prediction-Start lateral, so every feature has the same
availability it will have for a hidden suffix.  At inference, the fitted
local projections are chained in ``max_lag``-foot blocks.

Three ablations are evaluated with deterministic grouped-by-well CV:

``geom``
    X/Y/Z movement only.
``raw``
    Geometry plus calibrated horizontal ``delta GR``.
``phase``
    Raw features plus typewell-slope/curvature interactions and regularized
    inversions of ``delta GR``.  These are inference-time proxies for layer
    type: unlike the supplied ``Geology`` label, they exist for test wells.

Run from the competition directory::

    python -m src.panel --run panel-local-projections

Outputs are written under ``results/<run>/``. The production pipeline imports
only :class:`DirectPanelPhase` and :class:`EarlyPanelBlend`; diagnostics and
plotting remain isolated behind this module's CLI.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

from .baselines import Model, WellLoader
from .data import INFERENCE_COLS, WellPair, default_data_dir, list_wells, load_well
from .ensemble import lateral_start
from .gr import _calibrate, _resample_reference, _smooth_horizontal
from .topology import RegionalDipPrior
from .validate import DISTANCE_BUCKET_FT, make_folds, summarize


FEATURE_NAMES = [
    "dX",
    "dY",
    "dZ",
    "dGR",
    "dGR_inv_l1",
    "dGR_inv_l4",
    "dGR_inv_l16",
    "dGR_x_ref_slope",
    "dGR_x_ref_curvature",
    "dX_x_ref_slope",
    "dY_x_ref_slope",
    "dZ_x_ref_slope",
    "dX_x_ref_curvature",
    "dY_x_ref_curvature",
    "dX_x_ref_roughness",
    "dY_x_ref_roughness",
    "dZ_x_ref_roughness",
]

VARIANTS: dict[str, tuple[np.ndarray, float]] = {
    "panel_geom_a100": (np.arange(3), 100.0),
    "panel_raw_gr_a100": (np.arange(4), 100.0),
    "panel_phase_a10": (np.arange(len(FEATURE_NAMES)), 10.0),
    "panel_phase_a100": (np.arange(len(FEATURE_NAMES)), 100.0),
    "panel_phase_a1000": (np.arange(len(FEATURE_NAMES)), 1000.0),
}

DIRECT_VARIANTS: dict[str, tuple[np.ndarray, float]] = {
    "panel_direct_geom_a1000": (np.arange(3), 1000.0),
    "panel_direct_raw_gr_a1000": (np.arange(4), 1000.0),
    "panel_direct_phase_a100": (np.arange(len(FEATURE_NAMES)), 100.0),
    "panel_direct_phase_a1000": (np.arange(len(FEATURE_NAMES)), 1000.0),
    "panel_direct_phase_a10000": (np.arange(len(FEATURE_NAMES)), 10000.0),
}


@dataclass
class WellSignals:
    """Inference-available arrays used by all local-projection horizons."""

    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    md: np.ndarray
    gr_calibrated: np.ndarray
    ref_grid: np.ndarray
    ref_slope: np.ndarray
    ref_curvature: np.ndarray
    ref_roughness: np.ndarray


@dataclass
class NormalEquations:
    """Per-horizon sufficient statistics for deterministic ridge fits."""

    xtx: np.ndarray
    xty: np.ndarray
    n: np.ndarray
    wells: np.ndarray


def _signals(pair: WellPair) -> WellSignals:
    """Prepare calibrated GR and typewell phase descriptors for one well."""
    h = pair.horizontal
    grid, ref = _resample_reference(pair.typewell)
    slope = np.clip(np.gradient(ref, grid), -20.0, 20.0)
    curvature = np.clip(np.gradient(slope, grid), -10.0, 10.0)
    roughness = (
        pd.Series(ref)
        .rolling(41, center=True, min_periods=5)
        .std()
        .bfill()
        .ffill()
        .clip(0.0, 50.0)
        .to_numpy()
    )

    gr_smooth = _smooth_horizontal(h["GR"].to_numpy(dtype=float))
    calibration = _calibrate(pair, grid, ref, gr_smooth)
    if calibration is None:
        gr_calibrated = np.full(len(h), np.nan)
    else:
        a, b, _ = calibration
        gr_calibrated = (gr_smooth - b) / a
        # Interpolate only short internal gaps. Long missing runs remain a
        # no-GR update, matching the production state-space behavior.
        gr_calibrated = (
            pd.Series(gr_calibrated)
            .interpolate(limit=100, limit_direction="both", limit_area="inside")
            .to_numpy()
        )

    return WellSignals(
        x=h["X"].to_numpy(dtype=float),
        y=h["Y"].to_numpy(dtype=float),
        z=h["Z"].to_numpy(dtype=float),
        md=h["MD"].to_numpy(dtype=float),
        gr_calibrated=gr_calibrated,
        ref_grid=grid,
        ref_slope=slope,
        ref_curvature=curvature,
        ref_roughness=roughness,
    )


def _feature_matrix(
    signals: WellSignals,
    origins: np.ndarray,
    ends: np.ndarray,
    anchor_tvt: np.ndarray | float,
) -> np.ndarray:
    """Return signed geometry, raw-GR, and typewell-phase interactions."""
    dx = signals.x[ends] - signals.x[origins]
    dy = signals.y[ends] - signals.y[origins]
    dz = signals.z[ends] - signals.z[origins]

    dgr = signals.gr_calibrated[ends] - signals.gr_calibrated[origins]
    dgr = np.where(np.isfinite(dgr), dgr, 0.0)

    anchor_tvt = np.asarray(anchor_tvt, dtype=float)
    slope = np.interp(anchor_tvt, signals.ref_grid, signals.ref_slope)
    curvature = np.interp(anchor_tvt, signals.ref_grid, signals.ref_curvature)
    roughness = np.interp(anchor_tvt, signals.ref_grid, signals.ref_roughness)

    slope2 = slope * slope
    columns = [
        dx,
        dy,
        dz,
        dgr,
        dgr * slope / (slope2 + 1.0),
        dgr * slope / (slope2 + 4.0),
        dgr * slope / (slope2 + 16.0),
        dgr * slope,
        dgr * curvature,
        dx * slope,
        dy * slope,
        dz * slope,
        dx * curvature,
        dy * curvature,
        dx * roughness,
        dy * roughness,
        dz * roughness,
    ]
    return np.column_stack(columns).astype(np.float64, copy=False)


def _empty_normal_equations(max_lag: int) -> NormalEquations:
    p = len(FEATURE_NAMES)
    return NormalEquations(
        xtx=np.zeros((max_lag, p, p), dtype=np.float64),
        xty=np.zeros((max_lag, p), dtype=np.float64),
        n=np.zeros(max_lag, dtype=np.int64),
        wells=np.zeros(max_lag, dtype=np.int64),
    )


def accumulate_training_windows(
    train_wells: list[str],
    loader,
    max_lag: int,
    origin_step: int,
) -> NormalEquations:
    """Accumulate pre-PS lateral windows without retaining row-level data."""
    equations = _empty_normal_equations(max_lag)
    for well in train_wells:
        pair = loader(well)
        ps = pair.prediction_start
        landing = lateral_start(pair)
        if landing is None:
            continue
        tvt = pair.horizontal["TVT_input"].to_numpy(dtype=float)
        signals = _signals(pair)
        # A common origin set makes every lag directly comparable and lets the
        # expensive typewell-phase interpolation run once per well.
        origins = np.arange(landing, ps - max_lag, origin_step, dtype=np.int64)
        if not len(origins):
            continue
        horizons = np.arange(1, max_lag + 1, dtype=np.int64)
        origins_all = np.tile(origins, max_lag)
        horizons_all = np.repeat(horizons, len(origins))
        ends_all = origins_all + horizons_all
        y_all = tvt[ends_all] - tvt[origins_all]
        x_all = _feature_matrix(
            signals, origins_all, ends_all, tvt[origins_all]
        )
        for horizon in range(1, max_lag + 1):
            rows = slice((horizon - 1) * len(origins), horizon * len(origins))
            y = y_all[rows]
            ok = np.isfinite(y)
            if not ok.any():
                continue
            x, y = x_all[rows][ok], y[ok]
            equations.xtx[horizon - 1] += x.T @ x
            equations.xty[horizon - 1] += x.T @ y
            equations.n[horizon - 1] += len(y)
            equations.wells[horizon - 1] += 1
    return equations


def _smooth_coefficients(coef: np.ndarray, window: int) -> np.ndarray:
    if window <= 1 or len(coef) < 5:
        return coef
    window = min(window, len(coef) if len(coef) % 2 else len(coef) - 1)
    if window < 5:
        return coef
    if window % 2 == 0:
        window -= 1
    return savgol_filter(coef, window_length=window, polyorder=2, axis=0)


def fit_coefficient_curves(
    equations: NormalEquations,
    smoothing_window: int,
    variants: dict[str, tuple[np.ndarray, float]] = VARIANTS,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    """Fit per-horizon ridge models and return raw and smoothed coefficients."""
    max_lag, p, _ = equations.xtx.shape
    raw: dict[str, np.ndarray] = {}
    smooth: dict[str, np.ndarray] = {}
    for name, (features, alpha) in variants.items():
        coef = np.zeros((max_lag, p), dtype=np.float64)
        for h in range(max_lag):
            xtx = equations.xtx[h][np.ix_(features, features)]
            xty = equations.xty[h][features]
            n = max(int(equations.n[h]), 1)
            scale = np.sqrt(np.maximum(np.diag(xtx) / n, 1e-12))
            gram = xtx / np.outer(scale, scale)
            rhs = xty / scale
            ridge = gram + alpha * np.eye(len(features))
            beta_scaled = np.linalg.solve(ridge, rhs)
            coef[h, features] = beta_scaled / scale
        raw[name] = coef
        smooth[name] = _smooth_coefficients(coef, smoothing_window)
    return raw, smooth


def predict_chained(
    pair: WellPair,
    coefficient_curves: dict[str, np.ndarray],
    max_lag: int,
) -> dict[str, np.ndarray]:
    """Chain local projections in blocks, updating typewell phase recursively."""
    ps = pair.prediction_start
    n = len(pair.horizontal)
    tvt_in = pair.horizontal["TVT_input"].to_numpy(dtype=float)
    signals = _signals(pair)
    predictions = {
        name: np.empty(n - ps, dtype=np.float64) for name in coefficient_curves
    }

    anchor_row = ps - 1
    anchor_tvt = {name: float(tvt_in[anchor_row]) for name in coefficient_curves}
    while anchor_row < n - 1:
        block_end = min(anchor_row + max_lag, n - 1)
        ends = np.arange(anchor_row + 1, block_end + 1, dtype=np.int64)
        origins = np.full(len(ends), anchor_row, dtype=np.int64)
        horizons = ends - anchor_row
        for name, coef in coefficient_curves.items():
            x = _feature_matrix(signals, origins, ends, anchor_tvt[name])
            delta = np.einsum("ij,ij->i", x, coef[horizons - 1])
            block_pred = anchor_tvt[name] + delta
            predictions[name][ends - ps] = block_pred
            anchor_tvt[name] = float(block_pred[-1])
        anchor_row = block_end
    return predictions


def _score_predictions(
    pair: WellPair,
    predictions: dict[str, np.ndarray],
    fold: int,
) -> tuple[list[dict], list[pd.DataFrame]]:
    ps = pair.prediction_start
    truth = pair.suffix_target()
    md = pair.horizontal["MD"].to_numpy(dtype=float)
    bucket = ((md[ps:] - md[ps - 1]) // DISTANCE_BUCKET_FT).astype(int)
    rows: list[dict] = []
    distance_rows: list[pd.DataFrame] = []
    for name, pred in predictions.items():
        if pred.shape != truth.shape or not np.isfinite(pred).all():
            raise ValueError(f"{name}/{pair.name}: invalid prediction array")
        se = (pred - truth) ** 2
        rows.append({
            "model": name,
            "well": pair.name,
            "n": len(se),
            "sse": float(se.sum()),
            "rmse": float(np.sqrt(se.mean())),
            "fold": fold,
        })
        by_distance = (
            pd.DataFrame({"bucket_kft": bucket, "se": se})
            .groupby("bucket_kft")["se"]
            .agg(sse="sum", n="count")
            .reset_index()
        )
        by_distance.insert(0, "well", pair.name)
        by_distance.insert(0, "model", name)
        by_distance.insert(0, "fold", fold)
        distance_rows.append(by_distance)
    return rows, distance_rows


def _coefficient_frame(
    fold: int,
    raw: dict[str, np.ndarray],
    smooth: dict[str, np.ndarray],
    equations: NormalEquations,
    horizons: np.ndarray | None = None,
) -> pd.DataFrame:
    if horizons is None:
        horizons = np.arange(1, len(equations.n) + 1)
    rows = []
    for model in raw:
        for h in range(len(raw[model])):
            for j, feature in enumerate(FEATURE_NAMES):
                rows.append({
                    "fold": fold,
                    "model": model,
                    "lag_ft": int(horizons[h]),
                    "feature": feature,
                    "coefficient_raw": raw[model][h, j],
                    "coefficient": smooth[model][h, j],
                    "n_windows": equations.n[h],
                    "n_wells": equations.wells[h],
                })
    return pd.DataFrame(rows)


def direct_horizons(max_lag: int = 200) -> np.ndarray:
    """Dense short horizons plus sparse knots over a full hidden suffix."""
    long = [
        250,
        300,
        400,
        500,
        600,
        750,
        1000,
        1250,
        1500,
        2000,
        2500,
        3000,
        4000,
        5000,
        6000,
        8000,
    ]
    return np.unique(np.r_[np.arange(1, max_lag + 1), long]).astype(np.int64)


def accumulate_direct_windows(
    train_wells: list[str],
    loader,
    horizons: np.ndarray,
) -> NormalEquations:
    """Use each training well's real PS as one direct forecast origin.

    Unlike recursive 200-ft chaining, this learns how much each signal remains
    trustworthy after 1, 2, ... 8 kft.  Targets are available only because the
    well is in the training fold; held-out well targets never enter fitting.
    """
    equations = _empty_normal_equations(len(horizons))
    for well in train_wells:
        pair = loader(well)
        ps = pair.prediction_start
        origin = ps - 1
        max_horizon = len(pair.horizontal) - ps
        keep = horizons <= max_horizon
        if not keep.any():
            continue
        kept_horizons = horizons[keep]
        ends = origin + kept_horizons
        origins = np.full(len(ends), origin, dtype=np.int64)
        tvt_in = pair.horizontal["TVT_input"].to_numpy(dtype=float)
        truth = pair.horizontal["TVT"].to_numpy(dtype=float)
        y = truth[ends] - tvt_in[origin]
        x = _feature_matrix(_signals(pair), origins, ends, tvt_in[origin])
        for row, h_index in enumerate(np.nonzero(keep)[0]):
            if not np.isfinite(y[row]):
                continue
            xr = x[row]
            equations.xtx[h_index] += np.outer(xr, xr)
            equations.xty[h_index] += xr * y[row]
            equations.n[h_index] += 1
            equations.wells[h_index] += 1
    return equations


def predict_direct(
    pair: WellPair,
    coefficient_curves: dict[str, np.ndarray],
    horizons: np.ndarray,
) -> dict[str, np.ndarray]:
    """Predict every suffix row directly from the last observed TVT anchor."""
    ps = pair.prediction_start
    n_suffix = len(pair.horizontal) - ps
    origin = ps - 1
    ends = np.arange(ps, len(pair.horizontal), dtype=np.int64)
    origins = np.full(n_suffix, origin, dtype=np.int64)
    anchor = float(pair.horizontal["TVT_input"].to_numpy()[origin])
    x = _feature_matrix(_signals(pair), origins, ends, anchor)
    row_horizons = np.arange(1, n_suffix + 1)
    predictions = {}
    for name, coef in coefficient_curves.items():
        interpolated = np.column_stack(
            [np.interp(row_horizons, horizons, coef[:, j])
             for j in range(coef.shape[1])]
        )
        predictions[name] = anchor + np.einsum("ij,ij->i", x, interpolated)
    return predictions


class DirectPanelPhase:
    """Production form of the best non-recursive phase-aware panel model."""

    name = "Q_panel_direct_phase_a100"

    def __init__(self, max_lag: int = 200):
        self.max_lag = max_lag
        self.horizons = direct_horizons(max_lag)
        self.coef_: np.ndarray | None = None

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        equations = accumulate_direct_windows(train_wells, loader, self.horizons)
        variants = {self.name: (np.arange(len(FEATURE_NAMES)), 100.0)}
        _, coefficients = fit_coefficient_curves(
            equations, smoothing_window=1, variants=variants
        )
        self.coef_ = coefficients[self.name]

    def predict(self, pair: WellPair) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("DirectPanelPhase must be fitted before predict")
        return predict_direct(
            pair, {self.name: self.coef_}, self.horizons
        )[self.name]


class EarlyPanelBlend:
    """Use a small panel update only where its CV gain is stable.

    The direct panel signal is stable in the first 1,000 ft but accumulates
    geological misspecification farther out. Beyond that boundary the wrapper
    is exactly the existing F6 prediction.
    """

    def __init__(
        self,
        prior: Model,
        panel: DirectPanelPhase | None = None,
        weight: float = 0.30,
        max_distance_ft: float = 1000.0,
    ):
        if not 0.0 <= weight <= 1.0:
            raise ValueError("panel weight must be between zero and one")
        self.prior = prior
        self.panel = panel if panel is not None else DirectPanelPhase()
        self.weight = weight
        self.max_distance_ft = max_distance_ft
        self.name = f"J_panel_w{weight:g}_{int(max_distance_ft)}ft_{prior.name}"

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        self.prior.fit(train_wells, loader)
        self.panel.fit(train_wells, loader)

    def observe_test(self, pairs) -> None:
        """Delegate the transductive step; the panel itself needs targets
        that test wells cannot supply, so only the prior benefits."""
        if hasattr(self.prior, "observe_test"):
            self.prior.observe_test(pairs)

    def predict(self, pair: WellPair) -> np.ndarray:
        base = np.asarray(self.prior.predict(pair), dtype=float)
        panel = np.asarray(self.panel.predict(pair), dtype=float)
        ps = pair.prediction_start
        md = pair.horizontal["MD"].to_numpy(dtype=float)
        distance = md[ps:] - md[ps - 1]
        use_panel = distance < self.max_distance_ft
        out = base.copy()
        out[use_panel] = (
            (1.0 - self.weight) * base[use_panel]
            + self.weight * panel[use_panel]
        )
        return out


def run_direct_grouped_cv(
    data_dir: Path,
    out_dir: Path,
    max_lag: int = 200,
    n_folds: int = 5,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Grouped CV for non-recursive, distance-dependent panel projections."""
    train_dir = data_dir / "train"
    wells = list_wells(train_dir)
    folds = make_folds(wells, n_folds=n_folds, seed=seed)
    horizons = direct_horizons(max_lag)

    def loader(name: str) -> WellPair:
        return load_well(train_dir, name, columns=INFERENCE_COLS + ["TVT"])

    for fold, held_out in enumerate(folds):
        fold_scores = out_dir / f"direct_fold_{fold}_per_well.csv"
        fold_distance = out_dir / f"direct_fold_{fold}_by_distance.csv"
        fold_coef = out_dir / f"direct_fold_{fold}_coefficients.csv"
        if fold_scores.exists() and fold_distance.exists() and fold_coef.exists():
            print(f"direct fold {fold}: cached")
            continue
        held_set = set(held_out)
        train_wells = [well for well in wells if well not in held_set]
        print(f"direct fold {fold}: fitting {len(train_wells)} wells")
        equations = accumulate_direct_windows(train_wells, loader, horizons)
        raw, coefficients = fit_coefficient_curves(
            equations, smoothing_window=1, variants=DIRECT_VARIANTS
        )
        _coefficient_frame(
            fold, raw, coefficients, equations, horizons=horizons
        ).to_csv(fold_coef, index=False)

        score_rows: list[dict] = []
        distance_rows: list[pd.DataFrame] = []
        for i, well in enumerate(held_out, start=1):
            pair = loader(well)
            predictions = predict_direct(pair, coefficients, horizons)
            rows, by_distance = _score_predictions(pair, predictions, fold)
            score_rows.extend(rows)
            distance_rows.extend(by_distance)
            if i % 50 == 0:
                print(f"direct fold {fold}: predicted {i}/{len(held_out)} wells")
        pd.DataFrame(score_rows).to_csv(fold_scores, index=False)
        pd.concat(distance_rows, ignore_index=True).to_csv(fold_distance, index=False)

    per_well = pd.concat(
        [pd.read_csv(out_dir / f"direct_fold_{f}_per_well.csv")
         for f in range(n_folds)],
        ignore_index=True,
    )
    coefficients = pd.concat(
        [pd.read_csv(out_dir / f"direct_fold_{f}_coefficients.csv")
         for f in range(n_folds)],
        ignore_index=True,
    )
    pd.concat(
        [pd.read_csv(out_dir / f"direct_fold_{f}_by_distance.csv")
         for f in range(n_folds)],
        ignore_index=True,
    ).to_csv(out_dir / "direct_by_distance.csv", index=False)
    return per_well, coefficients


def _load_direct_curve(path: Path, model: str) -> tuple[np.ndarray, np.ndarray]:
    frame = pd.read_csv(path)
    frame = frame[frame["model"] == model]
    horizons = np.sort(frame["lag_ft"].unique()).astype(np.int64)
    pivot = frame.pivot(index="lag_ft", columns="feature", values="coefficient")
    pivot = pivot.reindex(index=horizons, columns=FEATURE_NAMES)
    if pivot.isna().any().any():
        raise ValueError(f"incomplete coefficient curve in {path}")
    return horizons, pivot.to_numpy(dtype=float)


def run_f6_blend_cv(
    data_dir: Path,
    out_dir: Path,
    n_folds: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    """Test whether the new panel signal improves the current F6 pipeline.

    Blend weights are fixed before scoring.  This is intentionally simpler
    than learning a meta-gate from the same OOF rows and keeps the comparison
    leakage-safe.
    """
    from .validate import build_models

    train_dir = data_dir / "train"
    wells = list_wells(train_dir)
    folds = make_folds(wells, n_folds=n_folds, seed=seed)
    panel_model = "panel_direct_phase_a100"
    weights = (0.05, 0.10, 0.20, 0.30)

    def loader(name: str) -> WellPair:
        return load_well(train_dir, name, columns=INFERENCE_COLS + ["TVT"])

    for fold, held_out in enumerate(folds):
        fold_scores = out_dir / f"blend_fold_{fold}_per_well.csv"
        fold_distance = out_dir / f"blend_fold_{fold}_by_distance.csv"
        if fold_scores.exists() and fold_distance.exists():
            print(f"F6 blend fold {fold}: cached")
            continue
        held_set = set(held_out)
        train_wells = [well for well in wells if well not in held_set]
        f6 = build_models("dip-best", data_dir)[0]
        print(f"F6 blend fold {fold}: fitting {len(train_wells)} wells")
        f6.fit(train_wells, loader)
        horizons, panel_coef = _load_direct_curve(
            out_dir / f"direct_fold_{fold}_coefficients.csv", panel_model
        )

        score_rows: list[dict] = []
        distance_rows: list[pd.DataFrame] = []
        for i, well in enumerate(held_out, start=1):
            pair = loader(well)
            pred_f6 = np.asarray(f6.predict(pair), dtype=float)
            pred_panel = predict_direct(
                pair, {panel_model: panel_coef}, horizons
            )[panel_model]
            predictions = {"current_F6_rerun": pred_f6}
            predictions.update({
                f"F6_plus_panel_w{weight:g}": (
                    (1.0 - weight) * pred_f6 + weight * pred_panel
                )
                for weight in weights
            })
            rows, by_distance = _score_predictions(pair, predictions, fold)
            score_rows.extend(rows)
            distance_rows.extend(by_distance)
            if i % 25 == 0:
                print(f"F6 blend fold {fold}: predicted {i}/{len(held_out)} wells")
        pd.DataFrame(score_rows).to_csv(fold_scores, index=False)
        pd.concat(distance_rows, ignore_index=True).to_csv(fold_distance, index=False)

    per_well = pd.concat(
        [pd.read_csv(out_dir / f"blend_fold_{f}_per_well.csv")
         for f in range(n_folds)],
        ignore_index=True,
    )
    pd.concat(
        [pd.read_csv(out_dir / f"blend_fold_{f}_by_distance.csv")
         for f in range(n_folds)],
        ignore_index=True,
    ).to_csv(out_dir / "blend_by_distance.csv", index=False)
    return per_well


def run_grouped_cv(
    data_dir: Path,
    out_dir: Path,
    max_lag: int = 200,
    origin_step: int = 50,
    smoothing_window: int = 21,
    n_folds: int = 5,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run deterministic grouped CV and persist fold-level outputs."""
    train_dir = data_dir / "train"
    wells = list_wells(train_dir)
    folds = make_folds(wells, n_folds=n_folds, seed=seed)
    out_dir.mkdir(parents=True, exist_ok=True)

    def loader(name: str) -> WellPair:
        return load_well(train_dir, name, columns=INFERENCE_COLS + ["TVT"])

    for fold, held_out in enumerate(folds):
        fold_scores = out_dir / f"fold_{fold}_per_well.csv"
        fold_distance = out_dir / f"fold_{fold}_by_distance.csv"
        fold_coef = out_dir / f"fold_{fold}_coefficients.csv"
        if fold_scores.exists() and fold_distance.exists() and fold_coef.exists():
            print(f"fold {fold}: cached")
            continue
        held_set = set(held_out)
        train_wells = [well for well in wells if well not in held_set]
        print(f"fold {fold}: fitting {len(train_wells)} wells")
        equations = accumulate_training_windows(
            train_wells, loader, max_lag=max_lag, origin_step=origin_step
        )
        raw, smooth = fit_coefficient_curves(equations, smoothing_window)
        _coefficient_frame(fold, raw, smooth, equations).to_csv(fold_coef, index=False)

        score_rows: list[dict] = []
        distance_rows: list[pd.DataFrame] = []
        for i, well in enumerate(held_out, start=1):
            pair = loader(well)
            predictions = predict_chained(pair, smooth, max_lag=max_lag)
            rows, by_distance = _score_predictions(pair, predictions, fold)
            score_rows.extend(rows)
            distance_rows.extend(by_distance)
            if i % 50 == 0:
                print(f"fold {fold}: predicted {i}/{len(held_out)} wells")
        pd.DataFrame(score_rows).to_csv(fold_scores, index=False)
        pd.concat(distance_rows, ignore_index=True).to_csv(fold_distance, index=False)

    per_well = pd.concat(
        [pd.read_csv(out_dir / f"fold_{f}_per_well.csv") for f in range(n_folds)],
        ignore_index=True,
    )
    coefficients = pd.concat(
        [pd.read_csv(out_dir / f"fold_{f}_coefficients.csv") for f in range(n_folds)],
        ignore_index=True,
    )
    per_well.to_csv(out_dir / "per_well.csv", index=False)
    coefficients.to_csv(out_dir / "coefficients.csv", index=False)
    pd.concat(
        [pd.read_csv(out_dir / f"fold_{f}_by_distance.csv") for f in range(n_folds)],
        ignore_index=True,
    ).to_csv(out_dir / "by_distance.csv", index=False)
    summary = summarize(per_well)
    summary.to_csv(out_dir / "summary.csv")
    print(summary.round(4).to_string())
    return per_well, coefficients


def residual_scale_diagnostic(
    data_dir: Path,
    out_path: Path,
    max_lag: int,
) -> pd.DataFrame:
    """RMS local topology departure after removing the regional dip plane."""
    train_dir = data_dir / "train"
    wells = list_wells(train_dir)
    prior = RegionalDipPrior(
        train_dir, data_dir.parent / "results" / "cache" / "surface_samples.parquet"
    )
    prior.fit(wells, loader=None)
    beta = prior.beta_
    extra = [250, 300, 400, 500, 750, 1000, 1500, 2000, 3000, 4000, 5000]
    lags = np.unique(np.r_[np.arange(1, max_lag + 1), extra]).astype(int)
    sum_sq = np.zeros(len(lags), dtype=np.float64)
    sum_signed = np.zeros(len(lags), dtype=np.float64)
    count = np.zeros(len(lags), dtype=np.int64)

    for well in wells:
        pair = load_well(
            train_dir, well, columns=["MD", "X", "Y", "Z", "TVT", "TVT_input"]
        )
        landing = lateral_start(pair)
        if landing is None:
            continue
        h = pair.horizontal
        q = (
            h["TVT"].to_numpy(dtype=float)
            + h["Z"].to_numpy(dtype=float)
            - beta[0] * h["X"].to_numpy(dtype=float)
            - beta[1] * h["Y"].to_numpy(dtype=float)
        )
        for j, lag in enumerate(lags):
            if landing + lag >= len(q):
                continue
            origins = np.arange(landing, len(q) - lag, 20, dtype=np.int64)
            delta = q[origins + lag] - q[origins]
            delta = delta[np.isfinite(delta)]
            sum_sq[j] += float(delta @ delta)
            sum_signed[j] += float(delta.sum())
            count[j] += len(delta)

    result = pd.DataFrame({
        "lag_ft": lags,
        "n_windows": count,
        "rms_residual_surface_change_ft": np.sqrt(sum_sq / np.maximum(count, 1)),
        "mean_residual_surface_change_ft": sum_signed / np.maximum(count, 1),
        "beta_x": beta[0],
        "beta_y": beta[1],
    })
    result.to_csv(out_path, index=False)
    return result


def plot_results(
    data_dir: Path,
    out_dir: Path,
    per_well: pd.DataFrame,
    coefficients: pd.DataFrame,
    residual_scale: pd.DataFrame,
) -> None:
    """Create static, reproducible diagnostics from the persisted CSVs."""
    import matplotlib.pyplot as plt

    phase = coefficients[coefficients["model"] == "panel_phase_a100"]
    stats = (
        phase.groupby(["lag_ft", "feature"])["coefficient"]
        .agg(["mean", "min", "max"])
        .reset_index()
    )
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    panels = [
        (axes[0, 0], ["dX", "dY"], "Horizontal coefficients", "ft TVT / ft"),
        (axes[0, 1], ["dZ"], "Vertical coefficient", "ft TVT / ft"),
        (axes[1, 0], ["dGR"], "Raw GR coefficient", "ft TVT / API"),
        (
            axes[1, 1],
            ["dGR_inv_l1", "dGR_inv_l4", "dGR_inv_l16"],
            "Typewell-phase GR coefficients",
            "coefficient",
        ),
    ]
    for ax, features, title, ylabel in panels:
        for feature in features:
            part = stats[stats["feature"] == feature]
            ax.plot(part["lag_ft"], part["mean"], label=feature)
            ax.fill_between(part["lag_ft"], part["min"], part["max"], alpha=0.15)
        ax.axhline(0.0, color="0.5", linewidth=0.8)
        ax.set(title=title, xlabel="Lag along MD (ft)", ylabel=ylabel)
        ax.grid(alpha=0.2)
        ax.legend()
    fig.savefig(out_dir / "coefficient-curves.png", dpi=160)
    plt.close(fig)

    summary = summarize(per_well).reset_index()
    f6_path = data_dir.parent / "results" / "dip-best-directional-z" / "per_well.csv"
    has_f6_rerun = summary["model"].str.startswith("current_F6").any()
    if f6_path.exists() and not has_f6_rerun:
        f6 = pd.read_csv(f6_path)
        summary = pd.concat(
            [
                summary,
                pd.DataFrame({
                    "model": ["current_F6"],
                    "global_rmse": [float(np.sqrt(f6["sse"].sum() / f6["n"].sum()))],
                }),
            ],
            ignore_index=True,
        )

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    axes[0].plot(
        residual_scale["lag_ft"],
        residual_scale["rms_residual_surface_change_ft"],
    )
    axes[0].set(
        xlabel="Spatial lag along the lateral (ft)",
        ylabel="RMS residual surface change (ft)",
        title="Topology departure after regional dip",
    )
    axes[0].grid(alpha=0.2)
    order = summary.sort_values("global_rmse")
    axes[1].barh(order["model"], order["global_rmse"])
    axes[1].set(xlabel="Grouped-CV RMSE (ft)", title="Suffix prediction")
    axes[1].grid(axis="x", alpha=0.2)
    fig.savefig(out_dir / "residual-scale-and-cv.png", dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--run", default="panel-local-projections")
    parser.add_argument("--max-lag", type=int, default=200)
    parser.add_argument("--origin-step", type=int, default=50)
    parser.add_argument("--smoothing-window", type=int, default=21)
    parser.add_argument("--n-folds", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.max_lag < 2:
        parser.error("--max-lag must be at least 2")

    out_dir = args.data_dir.parent / "results" / args.run
    chained_per_well, chained_coefficients = run_grouped_cv(
        args.data_dir,
        out_dir,
        max_lag=args.max_lag,
        origin_step=args.origin_step,
        smoothing_window=args.smoothing_window,
        n_folds=args.n_folds,
        seed=args.seed,
    )
    direct_per_well, direct_coefficients = run_direct_grouped_cv(
        args.data_dir,
        out_dir,
        max_lag=args.max_lag,
        n_folds=args.n_folds,
        seed=args.seed,
    )
    blend_per_well = run_f6_blend_cv(
        args.data_dir, out_dir, n_folds=args.n_folds, seed=args.seed
    )
    per_well = pd.concat(
        [chained_per_well, direct_per_well, blend_per_well], ignore_index=True
    )
    coefficients = pd.concat(
        [chained_coefficients, direct_coefficients], ignore_index=True
    )
    per_well.to_csv(out_dir / "per_well.csv", index=False)
    coefficients.to_csv(out_dir / "coefficients.csv", index=False)
    summarize(per_well).to_csv(out_dir / "summary.csv")
    residual_path = out_dir / "residual_scale.csv"
    residual_scale = residual_scale_diagnostic(
        args.data_dir, residual_path, max_lag=args.max_lag
    )
    plot_results(args.data_dir, out_dir, per_well, coefficients, residual_scale)


if __name__ == "__main__":
    main()
