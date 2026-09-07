"""Learned support-aware gate between the constant and spatial models.

The inverse-square replay blend ignores *why* the spatial model fails: wells
at the edge of spatial support or over rough (faulted) topology. This module
learns that relationship. Per well, the features are:

- ``s_a``, ``s_d``: prefix-replay RMSE of A (constant) and D (spatial).
- ``nbr_dist``: median distance from the well's suffix path to the nearest
  surface sample of any *other* well (edge-of-support signal).
- ``roughness``: median std of the 16 nearest other-well surface samples
  (fault/terrace signal).

All four are computable for a hidden test well. Training labels — whether D
beats A on the true suffix — come from the harness CV runs, which held each
well out when scoring it, so they are leakage-safe. Feature rows for the
table are computed against an all-wells surface with the well's own samples
excluded from every query, which matches the fold-fitted geometry a held-out
well sees.

Build the table (resumable):

    python -m src.gate --budget-s 30
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

from .baselines import ConstantTVT, Model, WellLoader
from .data import WellPair, default_data_dir, list_wells, load_well, outputs_root
from .ensemble import PrefixPlayoff, _masked_at
from .topology import RegionalDipPrior, SpatialTopology

#: Gate features. Ramp-hypothesis features (D's forecast |ΔTVT|, suffix
#: length, interactions) were tried and *rejected*: with exact blend-SSE
#: evaluation on gate_table_v4 they rank worse than these five, under both
#: logistic and GBM models (see README experiment log, 2026-07-15). The gap
#: to the blend oracle (~8.5) needs a feature that predicts D's
#: *reliability*, not its boldness.
FEATURES = ["log_score_ratio", "log_nbr_dist", "log_roughness",
            "log_dip_med", "log_dip_p90"]
TABLE_NAME = "gate_table_v4.csv"


def replay_scores(pair: WellPair, a: Model, d: Model,
                  playoff: PrefixPlayoff) -> tuple[float, float] | None:
    """Prefix-replay RMSE of both candidates, or None if no window fits."""
    cut = playoff._playoff_ps(pair)
    if cut is None:
        return None
    ps = pair.prediction_start
    truth = pair.horizontal["TVT_input"].to_numpy()[cut:ps]
    replay = _masked_at(pair, cut)
    ok = np.isfinite(truth)
    out = []
    for m in (a, d):
        pred = np.asarray(m.predict(replay), dtype=float)[: ps - cut]
        out.append(float(np.sqrt(np.mean((pred[ok] - truth[ok]) ** 2))))
    return out[0], out[1]


def support_features(pair: WellPair,
                     surface: SpatialTopology) -> tuple[float, float, float, float]:
    """(nbr_dist, roughness, dip_med, dip_p90) along the suffix path.

    ``dip_*`` come from the surface's own plane fits (|gradient| = tan dip),
    respecting ``surface.exclude_well`` — the physical fault/terrace signal.
    """
    ps = pair.prediction_start
    xy = pair.horizontal[["X", "Y"]].to_numpy()[ps::100]
    other = surface._wells != pair.name
    tree = cKDTree(surface._xy[other])
    s_other = surface._s[other]
    dist, idx = tree.query(xy, k=16, workers=-1)
    _, grad = surface._fit_planes(xy)
    return (float(np.median(dist[:, 0])),
            float(np.median(s_other[idx].std(axis=1))),
            float(np.median(grad)),
            float(np.percentile(grad, 90)))


def ramp_features(pred_d: np.ndarray, anchor: float) -> tuple[float, float]:
    """(end, max) |ΔTVT| that the spatial model forecasts for the suffix.

    A's forecast is identically zero, so this is the *ramp hypothesis*: the
    error analysis (INSIGHTS.md) shows failures concentrate in wells whose
    suffix TVT ramps smoothly away from the anchor, and that D usually sees
    the ramp while the gate hedges to constant-TVT.
    """
    dev = np.abs(pred_d - anchor)
    return float(dev[-1]), float(dev.max())


def featurize(s_a: float, s_d: float, nbr_dist: float, roughness: float,
              dip_med: float, dip_p90: float) -> list[float]:
    eps = 1e-6
    return [np.log(s_a + eps) - np.log(s_d + eps),
            np.log1p(nbr_dist),
            np.log1p(roughness),
            np.log(dip_med + 1e-4),
            np.log(dip_p90 + 1e-4)]


def build_gate_table(data_dir: Path, out_path: Path,
                     budget_s: float | None = None,
                     results_dir: Path | None = None) -> pd.DataFrame:
    """Per-well features + leakage-safe labels; resumable, cached."""
    train_dir = data_dir / "train"
    results = results_dir if results_dir is not None else outputs_root(data_dir) / "results"
    wells = list_wells(train_dir)

    done: set[str] = set()
    if out_path.exists():
        done = set(pd.read_csv(out_path)["well"])

    a = ConstantTVT()
    d = SpatialTopology(train_dir, results / "cache" / "surface_samples.parquet")
    d.fit(wells, loader=None)  # all wells; exclusion happens per query
    playoff = PrefixPlayoff([a, d])

    t0 = time.time()
    for well in wells:
        if well in done:
            continue
        if budget_s is not None and time.time() - t0 > budget_s:
            print(f"budget hit at {len(done)}/{len(wells)}; rerun to resume")
            break
        pair = load_well(train_dir, well,
                         columns=["MD", "X", "Y", "Z", "GR", "TVT_input", "TVT"])
        d.exclude_well = well
        scores = replay_scores(pair, a, d, playoff)
        nbr_dist, roughness, dip_med, dip_p90 = support_features(pair, d)
        pred_d = np.asarray(d.predict(pair), dtype=float)
        d.exclude_well = None
        ps = pair.prediction_start
        anchor = pair.horizontal["TVT_input"].to_numpy()[ps - 1]
        ramp_end, ramp_max = ramp_features(pred_d, anchor)
        # Exact blend algebra: for any weight w, the blended suffix SSE is
        # w^2*sse_d + (1-w)^2*sse_a + 2w(1-w)*cross. Stored so gate models
        # can be evaluated offline exactly and trained on the optimal w*.
        true = pair.suffix_target()
        err_a = anchor - true
        err_d = pred_d - true
        row = {"well": well, "nbr_dist": nbr_dist, "roughness": roughness,
               "dip_med": dip_med, "dip_p90": dip_p90,
               "ramp_end": ramp_end, "ramp_max": ramp_max,
               "sfx_len": len(pair.horizontal) - ps,
               "sse_a": float(err_a @ err_a), "sse_d": float(err_d @ err_d),
               "cross": float(err_a @ err_d),
               "s_a": scores[0] if scores else np.nan,
               "s_d": scores[1] if scores else np.nan}
        pd.DataFrame([row]).to_csv(out_path, mode="a",
                                   header=not out_path.exists(), index=False)
        done.add(well)

    table = pd.read_csv(out_path)
    if len(table) == len(wells):
        rmse_d = pd.read_csv(results / "stage2" / "per_well.csv")
        rmse_a = pd.read_csv(results / "baselines" / "per_well.csv")
        rmse_a = rmse_a[rmse_a.model == "A_const"]
        table = (table
                 .merge(rmse_d[["well", "rmse"]].rename(columns={"rmse": "rmse_d"}), on="well")
                 .merge(rmse_a[["well", "rmse"]].rename(columns={"rmse": "rmse_a"}), on="well"))
        print(f"gate table complete: {len(table)} wells, "
              f"{table['s_a'].isna().sum()} without replay window")
    return table


class LearnedGate:
    """Blend A and D with a logistic P(D beats A) on support-aware features.

    The gate is trained inside ``fit`` on training wells only, weighted by
    |rmse_a - rmse_d| so wells where the pick matters dominate the loss.
    Wells without a replay window fall back to A.
    """

    def __init__(self, train_dir: Path, results_dir: Path):
        self.name = "G_learnedgate"
        self.a = ConstantTVT()
        self.d = SpatialTopology(train_dir,
                                 results_dir / "cache" / "surface_samples.parquet")
        self.playoff = PrefixPlayoff([self.a, self.d])
        self.results_dir = results_dir
        self._clf = None

    def _training_table(self) -> pd.DataFrame:
        t = pd.read_csv(self.results_dir / "cache" / TABLE_NAME)
        rmse_d = pd.read_csv(self.results_dir / "stage2" / "per_well.csv")
        rmse_a = pd.read_csv(self.results_dir / "baselines" / "per_well.csv")
        rmse_a = rmse_a[rmse_a.model == "A_const"]
        return (t
                .merge(rmse_d[["well", "rmse"]].rename(columns={"rmse": "rmse_d"}), on="well")
                .merge(rmse_a[["well", "rmse"]].rename(columns={"rmse": "rmse_a"}), on="well"))

    def observe_test(self, pairs) -> None:
        """Transductive step: test-well prefixes densify the D surface."""
        self.d.observe_test(pairs)

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler

        self.a.fit(train_wells, loader)
        self.d.fit(train_wells, loader)

        t = self._training_table()
        t = t[t["well"].isin(set(train_wells))].dropna(subset=["s_a", "s_d"])
        x = np.array([featurize(r.s_a, r.s_d, r.nbr_dist, r.roughness,
                                r.dip_med, r.dip_p90)
                      for r in t.itertuples()])
        y = (t["rmse_d"] < t["rmse_a"]).to_numpy()
        w = np.abs(t["rmse_a"] - t["rmse_d"]).to_numpy()
        self._clf = make_pipeline(StandardScaler(), LogisticRegression(C=1.0))
        self._clf.fit(x, y, logisticregression__sample_weight=w)

    def _blend_weight(self, pair: WellPair) -> float | None:
        """Gate weight for D, or None when prefix replay is unavailable."""
        scores = replay_scores(pair, self.a, self.d, self.playoff)
        if scores is None:
            return None
        nbr_dist, roughness, dip_med, dip_p90 = support_features(pair, self.d)
        x = np.array([featurize(scores[0], scores[1], nbr_dist, roughness,
                                dip_med, dip_p90)])
        return float(self._clf.predict_proba(x)[0, 1])

    def predict(self, pair: WellPair) -> np.ndarray:
        pred_a = self.a.predict(pair)
        w = self._blend_weight(pair)
        if w is None:
            return pred_a
        return w * self.d.predict(pair) + (1.0 - w) * pred_a


class DipAxisGate(LearnedGate):
    """A/D gate whose safe component carries the regional dip residual.

    The existing gate still estimates how much to trust the high-variance
    local spatial surface D.  Where it falls back toward the safe constant
    prior, that component is replaced by :class:`RegionalDipPrior`, adding
    only the shrunken NNW-SSE formation-motion mismatch.  This preserves the
    gate's leakage-safe A/D training labels while applying the regional prior
    precisely where the stack previously assumed zero TVT movement.
    """

    def __init__(self, train_dir: Path, results_dir: Path,
                 residual_shrink: float = 0.15,
                 uphill_shrink: float | None = None,
                 downhill_shrink: float | None = None):
        super().__init__(train_dir, results_dir)
        self.regional = RegionalDipPrior(
            train_dir,
            results_dir / "cache" / "surface_samples.parquet",
            residual_shrink=residual_shrink,
            uphill_shrink=uphill_shrink,
            downhill_shrink=downhill_shrink,
        )
        # Distinct leading tag keeps downstream GRStateSpace experiment names
        # separate from the original G gate (which derives its tag from the
        # text before the first underscore).
        if self.regional.uphill_shrink == self.regional.downhill_shrink:
            tag = f"{self.regional.uphill_shrink:g}"
        else:
            tag = (f"u{self.regional.uphill_shrink:g}"
                   f"d{self.regional.downhill_shrink:g}")
        self.name = f"H{tag}_dipaxis"

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        super().fit(train_wells, loader)
        self.regional.fit(train_wells, loader)

    def observe_test(self, pairs) -> None:
        super().observe_test(pairs)

    def predict(self, pair: WellPair) -> np.ndarray:
        pred_safe = self.regional.predict(pair)
        w = self._blend_weight(pair)
        if w is None:
            return pred_safe
        return w * self.d.predict(pair) + (1.0 - w) * pred_safe


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=default_data_dir())
    ap.add_argument("--budget-s", type=float, default=None)
    args = ap.parse_args()
    out = outputs_root(args.data_dir) / "results" / "cache" / TABLE_NAME
    out.parent.mkdir(parents=True, exist_ok=True)
    build_gate_table(args.data_dir, out, budget_s=args.budget_s)


if __name__ == "__main__":
    main()
