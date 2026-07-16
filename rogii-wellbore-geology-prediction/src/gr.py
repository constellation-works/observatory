"""Stages 3+4: gamma-ray observation model and constrained state-space update.

The geometric prior (gated A/D blend) fixes *where the trajectory should be*
relative to the shared topology; GR corrects it row by row. The hidden state
is the offset ``o_t = TVT_t - prior_t``, tracked on a bounded grid by a
Viterbi pass along the suffix:

    cost_t(o) = emission_t(prior_t + o)          (GR mismatch, when GR exists)
              + lambda_geo * o^2                  (stay near the prior)
              + lambda_vel * (o_t - o_{t-1})^2    (offsets drift slowly)

Working in offset space keeps the prior's shape — including the exact
``dZ`` geometry — and lets the DP spend its freedom only on what the prior
got wrong.

Stage 3 (emission calibration) is fitted per well on the known prefix: the
typewell GR is resampled to a uniform TVT grid and lightly smoothed, the
horizontal GR is median-filtered, and a robust affine map between them is
estimated from ``(TVT_input, GR)`` pairs. The residual scale from that fit
sets the emission weight, so noisy pairings automatically trust the prior
more. Missing GR rows contribute no emission and coast on the prior.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from .baselines import Model, WellLoader
from .data import WellPair, list_wells, load_well

REF_STEP_FT = 0.25
REF_SMOOTH_SAMPLES = 9       # ~2.25 ft median window on the reference log
HORIZ_SMOOTH_SAMPLES = 11    # ~11 ft median window on the horizontal log
MIN_CALIB_PAIRS = 50


def _resample_reference(typewell: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Typewell GR on a uniform TVT grid, lightly median-smoothed."""
    tw = typewell.sort_values("TVT")
    tvt = tw["TVT"].to_numpy()
    grid = np.arange(tvt[0], tvt[-1] + REF_STEP_FT, REF_STEP_FT)
    gr = np.interp(grid, tvt, tw["GR"].to_numpy())
    gr = (pd.Series(gr)
          .rolling(REF_SMOOTH_SAMPLES, center=True, min_periods=1)
          .median().to_numpy())
    return grid, gr


def _smooth_horizontal(gr: np.ndarray) -> np.ndarray:
    return (pd.Series(gr)
            .rolling(HORIZ_SMOOTH_SAMPLES, center=True, min_periods=3)
            .median().to_numpy())


def _calibrate(pair: WellPair, grid: np.ndarray, ref: np.ndarray,
               gr_smooth: np.ndarray) -> tuple[float, float, float] | None:
    """Robust affine map ``gr_horizontal ~ a * gr_reference + b``.

    Returns ``(a, b, sigma)`` with ``sigma`` in reference-GR units, or None
    when the prefix offers too few usable pairs.
    """
    ps = pair.prediction_start
    tvt_in = pair.horizontal["TVT_input"].to_numpy()[:ps]
    gh = gr_smooth[:ps]
    ok = np.isfinite(tvt_in) & np.isfinite(gh)
    if ok.sum() < MIN_CALIB_PAIRS:
        return None
    gr_ref = np.interp(tvt_in[ok], grid, ref)
    gh = gh[ok]
    keep = np.ones(len(gh), dtype=bool)
    a, b = 1.0, 0.0
    for _ in range(3):  # iteratively reweighted least squares, 2.5-MAD clip
        if keep.sum() < MIN_CALIB_PAIRS or np.ptp(gr_ref[keep]) < 1e-6:
            return None
        a, b = np.polyfit(gr_ref[keep], gh[keep], 1)
        resid = gh - (a * gr_ref + b)
        mad = np.median(np.abs(resid[keep] - np.median(resid[keep])))
        keep = np.abs(resid) < 2.5 * max(1.4826 * mad, 1e-3)
    if a <= 1e-3:  # degenerate/inverted mapping: don't trust GR at all
        return None
    sigma = max(1.4826 * mad / a, 1.0)
    return float(a), float(b), float(sigma)


def build_bias_samples(train_dir: Path, cache_path: Path,
                       budget_s: float | None = None) -> pd.DataFrame:
    """Decimated ``(well, X, Y, r)`` table of calibrated-GR residuals.

    ``r = gh_calibrated - ref(TVT_true)`` in reference-GR units, measured at
    the *true* TVT of each training row (training-only information, used at
    fit time only). Spatially smooth lateral GR variation — the bias Daniel's
    continuity surface shows (|ΔGR| ~4 API at 644 ft, ~10 API beyond 5 mi) —
    lives in this field; a test well's emission can subtract its local value.
    Resumable like the other caches.
    """
    done: set[str] = set()
    if cache_path.exists():
        done = set(pd.read_csv(cache_path)["well"])
    wells = list_wells(train_dir)
    t0 = time.time()
    for well in wells:
        if well in done:
            continue
        if budget_s is not None and time.time() - t0 > budget_s:
            print(f"budget hit at {len(done)}/{len(wells)}; rerun to resume")
            break
        pair = load_well(train_dir, well)
        grid, ref = _resample_reference(pair.typewell)
        gh = _smooth_horizontal(pair.horizontal["GR"].to_numpy())
        calib = _calibrate(pair, grid, ref, gh)
        rows = []
        if calib is not None:
            a, b, _ = calib
            h = pair.horizontal
            tvt = h["TVT"].to_numpy()
            resid = (gh - b) / a - np.interp(tvt, grid, ref)
            md = h["MD"].to_numpy()
            edges = np.arange(md[0], md[-1] + 200.0, 200.0)
            which = np.digitize(md, edges)
            df = pd.DataFrame({"which": which, "X": h["X"], "Y": h["Y"],
                               "r": resid})
            g = df.groupby("which").agg(X=("X", "median"), Y=("Y", "median"),
                                        r=("r", "median")).dropna()
            for row in g.itertuples():
                rows.append({"well": well, "X": row.X, "Y": row.Y, "r": row.r})
        out = pd.DataFrame(rows if rows else [],
                           columns=["well", "X", "Y", "r"])
        if len(out):
            out.to_csv(cache_path, mode="a",
                       header=not cache_path.exists(), index=False)
        else:  # keep resumability even for wells yielding no samples
            pd.DataFrame([{"well": well, "X": np.nan, "Y": np.nan,
                           "r": np.nan}]).to_csv(
                cache_path, mode="a",
                header=not cache_path.exists(), index=False)
        done.add(well)
    return pd.read_csv(cache_path).dropna(subset=["r"])


class BiasField:
    """k-NN median of the calibrated-GR residual field, with distance decay."""

    def __init__(self, table: pd.DataFrame, k: int = 24,
                 halflife_ft: float = 5000.0):
        self._xy = table[["X", "Y"]].to_numpy()
        self._r = table["r"].to_numpy()
        self._tree = cKDTree(self._xy)
        self.k = k
        self.halflife_ft = halflife_ft

    def __call__(self, xy: np.ndarray) -> np.ndarray:
        dist, idx = self._tree.query(xy, k=min(self.k, len(self._r)),
                                     workers=-1)
        b = np.median(self._r[idx], axis=1)
        # Far from support the field says nothing; decay to zero correction.
        w = 0.5 ** (dist.mean(axis=1) / self.halflife_ft)
        return b * w

    def augment(self, xy: np.ndarray, r: np.ndarray) -> None:
        self._xy = np.vstack([self._xy, xy])
        self._r = np.concatenate([self._r, r])
        self._tree = cKDTree(self._xy)


class GRStateSpace:
    """Rung F: Viterbi offset correction of a geometric prior using GR."""

    def __init__(
        self,
        prior: Model,
        half_width_ft: float = 40.0,
        step_ft: float = 0.5,
        sigma_geo_ft: float = 15.0,
        sigma_vel: float = 0.02,   # ft of offset drift per ft of MD
        max_shift_steps: int = 2,
        adaptive: bool = True,
        adaptive_scale: float = 1.5,
        adaptive_range: tuple[float, float] = (4.0, 40.0),
        shrink: float = 1.0,
        bias_cache: tuple[Path, Path] | None = None,  # (train_dir, cache_path)
        shape_window_ft: float = 400.0,
        shape_weight: float = 1.0,
        level_weight: float = 0.25,
        min_valid_frac: float = 0.15,
    ):
        self.prior = prior
        self.half_width_ft = half_width_ft
        self.step_ft = step_ft
        self.sigma_geo_ft = sigma_geo_ft
        self.sigma_vel = sigma_vel
        self.max_shift_steps = max_shift_steps
        #: When on, sigma_geo per well = clip(scale * prior replay RMSE),
        #: so GR corrects boldly only where the prior is demonstrably weak.
        self.adaptive = adaptive
        self.adaptive_scale = adaptive_scale
        self.adaptive_range = adaptive_range
        #: Fraction of the Viterbi offset actually applied (variance shrink).
        self.shrink = shrink
        self.bias_cache = bias_cache
        self._bias_field: BiasField | None = None
        #: Shape channel: level-removed windowed mismatch. With the offset
        #: held constant across a window, sum((gh - mean) - (ref - mean))^2
        #: over the window equals the window *variance* of the pointwise
        #: difference — so the whole channel is rolling-variance cumsums.
        self.shape_window_ft = shape_window_ft
        self.shape_weight = shape_weight
        self.level_weight = level_weight
        self.min_valid_frac = min_valid_frac
        tag = "a" if adaptive else f"g{sigma_geo_ft:g}"
        bias_tag = "_bias" if bias_cache else ""
        shape_tag = f"_shp{int(shape_window_ft)}" if shape_weight > 0 else ""
        self.name = (f"F_grdp_{prior.name.split('_')[0]}_{tag}"
                     f"_v{sigma_vel:g}_s{shrink:g}{bias_tag}{shape_tag}")

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        self.prior.fit(train_wells, loader)
        if self.bias_cache is not None:
            train_dir, cache_path = self.bias_cache
            table = build_bias_samples(train_dir, cache_path)
            table = table[table["well"].isin(set(train_wells))]
            self._bias_field = BiasField(table)

    def observe_test(self, pairs: list[WellPair]) -> None:
        """Transductive step: test prefixes densify the surface + GR field.

        The GR residual samples use only prefix rows (``TVT_input``), the
        same calibration as prediction, and no suffix information.
        """
        if hasattr(self.prior, "observe_test"):
            self.prior.observe_test(pairs)
        if self._bias_field is None:
            return
        xs, rs = [], []
        for pair in pairs:
            grid, ref = _resample_reference(pair.typewell)
            gh = _smooth_horizontal(pair.horizontal["GR"].to_numpy())
            calib = _calibrate(pair, grid, ref, gh)
            if calib is None:
                continue
            a, b, _ = calib
            ps = pair.prediction_start
            h = pair.horizontal
            tvt_in = h["TVT_input"].to_numpy()[:ps]
            resid = (gh[:ps] - b) / a - np.interp(tvt_in, grid, ref)
            md = h["MD"].to_numpy()[:ps]
            which = np.digitize(md, np.arange(md[0], md[-1] + 200.0, 200.0))
            df = pd.DataFrame({"which": which, "X": h["X"].to_numpy()[:ps],
                               "Y": h["Y"].to_numpy()[:ps], "r": resid})
            g = df.groupby("which").agg(X=("X", "median"), Y=("Y", "median"),
                                        r=("r", "median")).dropna()
            if len(g):
                xs.append(g[["X", "Y"]].to_numpy())
                rs.append(g["r"].to_numpy())
        if xs:
            self._bias_field.augment(np.vstack(xs), np.concatenate(rs))

    def predict(self, pair: WellPair) -> np.ndarray:
        base = np.asarray(self.prior.predict(pair), dtype=float)
        grid, ref = _resample_reference(pair.typewell)
        gr_smooth = _smooth_horizontal(pair.horizontal["GR"].to_numpy())
        calib = _calibrate(pair, grid, ref, gr_smooth)
        if calib is None:
            return base
        a, b, sigma = calib

        sigma_geo = self.sigma_geo_ft
        if self.adaptive:
            from .ensemble import PrefixPlayoff, _masked_at
            playoff = PrefixPlayoff([self.prior])
            cut = playoff._playoff_ps(pair)
            if cut is not None:
                ps0 = pair.prediction_start
                truth = pair.horizontal["TVT_input"].to_numpy()[cut:ps0]
                replay_pred = np.asarray(
                    self.prior.predict(_masked_at(pair, cut)), dtype=float
                )[: ps0 - cut]
                ok = np.isfinite(truth)
                replay_rmse = float(np.sqrt(np.mean(
                    (replay_pred[ok] - truth[ok]) ** 2)))
                lo, hi = self.adaptive_range
                sigma_geo = float(np.clip(
                    self.adaptive_scale * replay_rmse, lo, hi))

        ps = pair.prediction_start
        gh = (gr_smooth[ps:] - b) / a          # horizontal GR in reference units
        if self._bias_field is not None:
            # Subtract the *change* in the spatial GR bias relative to the
            # prefix; the prefix's own bias is already inside (a, b).
            xy = pair.horizontal[["X", "Y"]].to_numpy()
            md_all = pair.horizontal["MD"].to_numpy()
            lo = int(np.searchsorted(md_all[:ps], md_all[ps - 1] - 1500.0))
            q = np.arange(ps, len(md_all), 100)
            b_sparse = self._bias_field(xy[q])
            b_prefix = float(np.median(self._bias_field(xy[lo:ps:100])))
            gh = gh - (np.interp(md_all[ps:], md_all[q], b_sparse) - b_prefix)
        has_gr = np.isfinite(gh)

        offsets = np.arange(-self.half_width_ft,
                            self.half_width_ft + self.step_ft, self.step_ft)
        n_t, n_s = len(base), len(offsets)

        # Level channel: squared calibrated mismatch at prior + offset.
        cand_tvt = base[:, None] + offsets[None, :]
        ref_at = np.interp(cand_tvt.ravel(), grid, ref).reshape(n_t, n_s)
        emission = np.zeros((n_t, n_s), dtype=np.float32)
        emission[has_gr] = (self.level_weight
                            * (gh[has_gr, None] - ref_at[has_gr]) ** 2
                            / (2.0 * sigma ** 2)).astype(np.float32)

        if self.shape_weight > 0:
            # Shape channel: rolling variance of d = gh - ref along MD.
            # Mean removal inside each window kills residual level bias;
            # what remains is pattern mismatch. Windows with too little GR
            # coverage contribute nothing (coast on the prior).
            w_rows = max(int(self.shape_window_ft), 3)
            half = w_rows // 2
            min_valid = max(int(self.min_valid_frac * w_rows), 5)

            # Window scale from the prefix at the *true* alignment.
            gh_pref = (gr_smooth[:ps] - b) / a
            tvt_pref = pair.horizontal["TVT_input"].to_numpy()[:ps]
            d_pref = gh_pref - np.interp(tvt_pref, grid, ref)
            var_pref = (pd.Series(d_pref)
                        .rolling(w_rows, center=True, min_periods=min_valid)
                        .var())
            sigma_w2 = float(np.nanmedian(var_pref))
            if not np.isfinite(sigma_w2) or sigma_w2 <= 0:
                sigma_w2 = sigma ** 2

            d = np.where(has_gr[:, None], gh[:, None] - ref_at, 0.0)
            lo = np.clip(np.arange(n_t) - half, 0, n_t)
            hi = np.clip(np.arange(n_t) + half + 1, 0, n_t)
            c1 = np.vstack([np.zeros((1, n_s)), np.cumsum(d, axis=0)])
            c2 = np.vstack([np.zeros((1, n_s)), np.cumsum(d * d, axis=0)])
            cn = np.concatenate([[0.0], np.cumsum(has_gr.astype(float))])
            n_w = (cn[hi] - cn[lo])[:, None]
            with np.errstate(invalid="ignore", divide="ignore"):
                s1 = c1[hi] - c1[lo]
                var = (c2[hi] - c2[lo]) / n_w - (s1 / n_w) ** 2
            shape = np.where(n_w >= min_valid,
                             self.shape_weight * var / (2.0 * sigma_w2),
                             0.0)
            emission += np.nan_to_num(shape).astype(np.float32)

        prior_cost = (offsets ** 2 / (2.0 * sigma_geo ** 2)).astype(np.float32)
        shift_cost = np.array(
            [(k * self.step_ft) ** 2 / (2.0 * self.sigma_vel ** 2)
             for k in range(self.max_shift_steps + 1)], dtype=np.float32)

        # Viterbi over offsets; transitions limited to +-max_shift_steps.
        # TVT is continuous through PS, so the path starts pinned near
        # offset zero (sigma 1 ft) and can only drift away over rows.
        anchor_cost = (offsets ** 2 / 2.0).astype(np.float32)
        cost = emission[0] + prior_cost + anchor_cost
        back = np.zeros((n_t, n_s), dtype=np.int8)
        for t in range(1, n_t):
            best = cost.copy()
            arg = np.zeros(n_s, dtype=np.int8)
            for k in range(1, self.max_shift_steps + 1):
                for sgn in (1, -1):
                    shifted = np.full(n_s, np.inf, dtype=np.float32)
                    if sgn > 0:
                        shifted[k:] = cost[:-k] + shift_cost[k]
                    else:
                        shifted[:-k] = cost[k:] + shift_cost[k]
                    better = shifted < best
                    best[better] = shifted[better]
                    arg[better] = sgn * k
            back[t] = arg
            cost = best + emission[t] + prior_cost

        path = np.empty(n_t, dtype=np.int64)
        path[-1] = int(np.argmin(cost))
        for t in range(n_t - 1, 0, -1):
            path[t - 1] = path[t] - back[t, path[t]]
        return base + self.shrink * offsets[path]
