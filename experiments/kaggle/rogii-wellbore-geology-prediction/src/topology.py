"""Stage 2: cross-well spatial topology surface (ablation rung D).

Within a well the six formation surfaces are one shared topology with fixed
vertical offsets, so a single surface (``ANCC``) carries all the lateral-shape
signal. This module learns a map ``F(X, Y)`` of that topology from *other*
wells and predicts a held-out well's TVT as::

    TVT_t = TVT_anchor + (F(X_t, Y_t) - F(X_a, Y_a)) - (Z_t - Z_a)

Anchoring at the last known ``TVT_input`` row cancels absolute-level error in
``F``; only the topology *change* along the future trajectory matters.

Leakage safety: ``fit`` filters the precomputed sample table to training
wells only, so a held-out well's surfaces never influence its own prediction.
Surface columns are used exclusively inside ``fit`` — ``predict`` needs only
inference-time columns — so the model remains valid for hidden test wells.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.spatial import cKDTree

from .baselines import WellLoader
from .data import WellPair, list_wells, load_well

#: Along-path spacing of surface samples taken from each training well.
SAMPLE_SPACING_FT = 200.0
#: Along-path spacing of F(X, Y) queries on the held-out trajectory
#: (interpolated back to 1-ft rows afterwards).
QUERY_SPACING_FT = 100.0


def build_surface_samples(train_dir: Path, cache_path: Path) -> pd.DataFrame:
    """Decimated ``(well, X, Y, s)`` table of ANCC surface samples.

    Rows with missing ``ANCC`` are dropped (0.9% of training rows). The table
    is cached because it never changes between runs; leakage filtering happens
    later, per fold.
    """
    if cache_path.exists():
        return pd.read_parquet(cache_path)

    frames = []
    for well in list_wells(train_dir):
        h = load_well(train_dir, well, columns=["MD", "X", "Y", "ANCC"]).horizontal
        h = h.dropna(subset=["ANCC"])
        if h.empty:
            continue
        md = h["MD"].to_numpy()
        keep = np.searchsorted(md, np.arange(md[0], md[-1] + 1, SAMPLE_SPACING_FT))
        keep = np.unique(np.clip(keep, 0, len(h) - 1))
        sample = h.iloc[keep][["X", "Y", "ANCC"]].rename(columns={"ANCC": "s"})
        sample.insert(0, "well", well)
        frames.append(sample)

    if not frames:
        raise FileNotFoundError(
            f"No paired horizontal wells found in {train_dir}. "
            "Check the competition data mount/path before building caches."
        )
    table = pd.concat(frames, ignore_index=True)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_parquet(cache_path, index=False)
    return table


class RegionalDipPrior:
    """Regional dip-axis prior, expressed directly as a TVT residual.

    A robust regional formation gradient ``beta = (dS/dX, dS/dY)`` is fitted
    from within-well ANCC changes in the training fold.  Centering the fit on
    changes, rather than absolute surface elevations, prevents regional
    elevation offsets from masquerading as dip.

    At inference the expected formation movement is ``beta @ (dX, dY)``.
    Only its mismatch with the borehole's vertical movement changes TVT::

        dTVT_raw = beta_x * dX + beta_y * dY - dZ

    The prediction is anchored at the last observed ``TVT_input``.  Small
    shrink factors are deliberate: the NNW-SSE axis gets the *direction* right
    almost everywhere, but local departures from the regional plane make the
    unshrunk magnitude noisy.  The scalar prior's grouped-CV optimum is 0.15;
    the final stack uses 0.15 downhill and 0.0 uphill because the correction's
    benefit becomes asymmetric after the GR state-space update.

    Formation surfaces are used only by ``fit``.  ``predict`` requires the
    same inference-time X/Y/Z/TVT_input columns available in hidden test.
    """

    def __init__(
        self,
        train_dir: Path,
        cache_path: Path,
        residual_shrink: float = 0.15,
        uphill_shrink: float | None = None,
        downhill_shrink: float | None = None,
    ):
        uphill_shrink = residual_shrink if uphill_shrink is None else uphill_shrink
        downhill_shrink = residual_shrink if downhill_shrink is None else downhill_shrink
        if not all(0.0 <= value <= 1.0
                   for value in (residual_shrink, uphill_shrink, downhill_shrink)):
            raise ValueError("residual shrink factors must be between 0 and 1")
        self.train_dir = train_dir
        self.cache_path = cache_path
        self.residual_shrink = residual_shrink
        self.uphill_shrink = uphill_shrink
        self.downhill_shrink = downhill_shrink
        if uphill_shrink == downhill_shrink:
            self.name = f"R_dipaxis_s{uphill_shrink:g}"
        else:
            self.name = f"R_dipaxis_u{uphill_shrink:g}_d{downhill_shrink:g}"
        self.beta_: np.ndarray | None = None

    @property
    def bearing_deg(self) -> float:
        """Up-dip bearing in degrees clockwise from north."""
        if self.beta_ is None:
            raise RuntimeError("RegionalDipPrior must be fitted first")
        return float((np.degrees(np.arctan2(self.beta_[0], self.beta_[1])) + 360) % 360)

    @property
    def dip_deg(self) -> float:
        """Magnitude of the fitted regional dip in degrees."""
        if self.beta_ is None:
            raise RuntimeError("RegionalDipPrior must be fitted first")
        return float(np.degrees(np.arctan(np.hypot(*self.beta_))))

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        table = build_surface_samples(self.train_dir, self.cache_path)
        table = table[table["well"].isin(set(train_wells))]

        # One endpoint delta per well gives every well equal weight and strips
        # out its unknown absolute surface elevation/intercept.
        grouped = table.groupby("well", sort=False)
        first = grouped[["X", "Y", "s"]].first()
        last = grouped[["X", "Y", "s"]].last()
        delta = last - first
        delta = delta.replace([np.inf, -np.inf], np.nan).dropna()
        delta = delta[np.hypot(delta["X"], delta["Y"]) >= 100.0]
        if len(delta) < 3:
            raise ValueError("at least three training wells are required to fit regional dip")

        xy = delta[["X", "Y"]].to_numpy(dtype=float)
        ds = delta["s"].to_numpy(dtype=float)
        beta0, *_ = np.linalg.lstsq(xy, ds, rcond=None)
        resid = ds - xy @ beta0
        scale = max(1.4826 * np.median(np.abs(resid - np.median(resid))), 1.0)

        # Soft-L1 keeps a handful of fault/terrace crossings from rotating the
        # regional axis.  With fixed inputs this solve is deterministic.
        fit = least_squares(
            lambda beta: (xy @ beta - ds) / scale,
            beta0,
            loss="soft_l1",
        )
        self.beta_ = fit.x.astype(float)

    def predict(self, pair: WellPair) -> np.ndarray:
        if self.beta_ is None:
            raise RuntimeError("RegionalDipPrior must be fitted before predict")
        ps = pair.prediction_start
        h = pair.horizontal
        x = h["X"].to_numpy()
        y = h["Y"].to_numpy()
        z = h["Z"].to_numpy()
        anchor = h["TVT_input"].to_numpy()[ps - 1]
        dx = x[ps:] - x[ps - 1]
        dy = y[ps:] - y[ps - 1]
        dz = z[ps:] - z[ps - 1]
        expected_surface = self.beta_[0] * dx + self.beta_[1] * dy
        mismatch = expected_surface - dz

        # Use the whole suffix's physical Z direction to choose one stable
        # regime. The regional plane supplies expected *formation movement*;
        # it should not override the observed local steering direction on the
        # handful of wells where those signs disagree. A row-by-row switch
        # would introduce an artificial kink. Full X/Y/Z is available for the
        # hidden suffix at inference.
        shrink = (self.downhill_shrink if dz[-1] < 0.0
                  else self.uphill_shrink)
        return anchor + shrink * mismatch


class SpatialTopology:
    """Rung D: k-NN distance-weighted local-plane estimate of F(X, Y)."""

    def __init__(
        self,
        train_dir: Path,
        cache_path: Path,
        k: int = 32,
        max_well_frac: float = 0.5,
    ):
        self.name = f"D_spatial_k{k}"
        self.train_dir = train_dir
        self.cache_path = cache_path
        self.k = k
        #: Cap on the fraction of neighbors from any single well, so one
        #: nearby lateral cannot dictate the whole plane.
        self.max_well_frac = max_well_frac
        #: When set, samples from this well are skipped in neighbor queries.
        #: Used to compute unbiased per-well features on a surface fitted to
        #: all wells; a no-op when the well was excluded from ``fit`` anyway.
        self.exclude_well: str | None = None
        self._tree: cKDTree | None = None
        self._xy: np.ndarray | None = None
        self._s: np.ndarray | None = None
        self._wells: np.ndarray | None = None

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        table = build_surface_samples(self.train_dir, self.cache_path)
        table = table[table["well"].isin(set(train_wells))]
        self._xy = table[["X", "Y"]].to_numpy()
        self._s = table["s"].to_numpy()
        self._wells = table["well"].to_numpy()
        self._tree = cKDTree(self._xy)

    def observe_test(self, pairs: list[WellPair]) -> None:
        """Densify the surface with *test wells' observed prefixes*.

        At inference time every test well exposes ~1,700 ft of known
        topology (``s = TVT_input + Z``) along its prefix — unlabeled-suffix
        information that is legitimately available when Kaggle reruns the
        notebook, and that supports exactly the wells being predicted
        (including each other). The prefix topology sits on a per-well/
        typewell datum, so each well's samples are level-aligned to the
        fitted train surface (median offset over its own prefix) before
        joining the pool. All offsets are computed against the original
        train-only surface first, so the result is order-independent.
        """
        new_xy, new_s, new_wells = [], [], []
        for pair in pairs:
            h = pair.horizontal
            ps = pair.prediction_start
            md = h["MD"].to_numpy()[:ps]
            keep = np.searchsorted(md, np.arange(md[0], md[-1] + 1, SAMPLE_SPACING_FT))
            keep = np.unique(np.clip(keep, 0, ps - 1))
            s_tvt = (h["TVT_input"].to_numpy() + h["Z"].to_numpy())[keep]
            xy = h[["X", "Y"]].to_numpy()[keep]
            ok = np.isfinite(s_tvt)
            if ok.sum() < 3:
                continue
            offset = float(np.median(self._f_hat(xy[ok]) - s_tvt[ok]))
            new_xy.append(xy[ok])
            new_s.append(s_tvt[ok] + offset)
            new_wells.append(np.full(ok.sum(), pair.name))
        if not new_xy:
            return
        self._xy = np.vstack([self._xy] + new_xy)
        self._s = np.concatenate([self._s] + new_s)
        self._wells = np.concatenate([self._wells] + new_wells)
        self._tree = cKDTree(self._xy)

    def _f_hat(self, queries: np.ndarray) -> np.ndarray:
        """Weighted-plane F estimate at each (x, y) query point."""
        return self._fit_planes(queries)[0]

    def _fit_planes(self, queries: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """(F, |gradient|) at each query; the plane solve yields both.

        ``|gradient|`` is ``tan(local dip)`` of the topology surface — near
        zero on flat-lying beds, spiking at faults/terraces.
        """
        k_search = min(self.k * 3, len(self._s))
        dist, idx = self._tree.query(queries, k=k_search, workers=-1)
        out = np.empty(len(queries))
        grad = np.empty(len(queries))
        max_per_well = max(1, int(self.k * self.max_well_frac))
        for i, (d_row, i_row) in enumerate(zip(dist, idx)):
            # Enforce per-well diversity among the k nearest kept neighbors.
            keep: list[int] = []
            counts: dict[str, int] = {}
            for d, j in zip(d_row, i_row):
                w = self._wells[j]
                if w == self.exclude_well:
                    continue
                if counts.get(w, 0) >= max_per_well:
                    continue
                counts[w] = counts.get(w, 0) + 1
                keep.append(j)
                if len(keep) == self.k:
                    break
            j = np.array(keep)
            dx = self._xy[j] - queries[i]
            d = np.hypot(dx[:, 0], dx[:, 1])
            bw = max(np.median(d), 1.0)
            w = np.exp(-0.5 * (d / bw) ** 2)
            a = np.column_stack([np.ones(len(j)), dx])  # plane about the query
            aw = a * w[:, None]
            coef, *_ = np.linalg.lstsq(aw.T @ a, aw.T @ self._s[j], rcond=None)
            out[i] = coef[0]
            grad[i] = np.hypot(coef[1], coef[2])
        return out, grad

    def predict(self, pair: WellPair) -> np.ndarray:
        ps = pair.prediction_start
        h = pair.horizontal
        md = h["MD"].to_numpy()
        z = h["Z"].to_numpy()
        anchor_tvt = h["TVT_input"].to_numpy()[ps - 1]

        # Query F sparsely (anchor + every QUERY_SPACING_FT), then interpolate.
        q_idx = np.unique(np.concatenate([
            [ps - 1],
            np.searchsorted(md, np.arange(md[ps - 1], md[-1] + 1, QUERY_SPACING_FT)),
            [len(md) - 1],
        ]).clip(0, len(md) - 1))
        f_q = self._f_hat(h[["X", "Y"]].to_numpy()[q_idx])
        f = np.interp(md[ps:], md[q_idx], f_q)
        f_anchor = f_q[q_idx == ps - 1][0]

        return anchor_tvt + (f - f_anchor) - (z[ps:] - z[ps - 1])


class TrendCorrectedSpatial(SpatialTopology):
    """Rung D2: D plus an affine correction fitted to prefix residuals.

    Where the learned surface has the wrong local tilt, the residual
    ``r = (TVT_input + Z) - F`` drifts linearly across the lateral prefix.
    Fitting that drift and extrapolating it (slope clipped to stay tame)
    corrects the suffix prediction; the offset term reproduces anchoring but
    uses the whole window, so it is robust to noise in the single anchor row.
    """

    def __init__(self, *args, window_ft: float = 1500.0,
                 max_slope: float = 0.01, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_ft = window_ft
        self.max_slope = max_slope
        self.name = f"D2_trendcorr_k{self.k}_{int(window_ft)}ft"

    def predict(self, pair: WellPair) -> np.ndarray:
        ps = pair.prediction_start
        h = pair.horizontal
        md = h["MD"].to_numpy()
        z = h["Z"].to_numpy()
        tvt_in = h["TVT_input"].to_numpy()

        base = super().predict(pair)  # anchored at ps - 1

        lo = int(np.searchsorted(md[:ps], md[ps - 1] - self.window_ft))
        q_idx = np.unique(np.searchsorted(
            md, np.arange(md[lo], md[ps - 1] + 1, 50.0)).clip(0, ps - 1))
        f_prefix = self._f_hat(h[["X", "Y"]].to_numpy()[q_idx])
        r = (tvt_in[q_idx] + z[q_idx]) - f_prefix
        ok = np.isfinite(r)
        if ok.sum() < 5:
            return base
        slope, _intercept = np.polyfit(md[q_idx][ok], r[ok], 1)
        slope = float(np.clip(slope, -self.max_slope, self.max_slope))
        # base already matches at the anchor; apply only the *change* in the
        # residual trend after the anchor.
        return base + slope * (md[ps:] - md[ps - 1])
