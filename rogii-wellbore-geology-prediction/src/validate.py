"""Leakage-safe grouped cross-validation and diagnostics.

Folds are deterministic (seeded shuffle of well names, contiguous chunks).
For each fold, models are fitted on the training wells only and score the
held-out wells' actual masked suffixes against the training-only ``TVT``.
Fit-free baselines pass through the same machinery so every number in the
experiment log comes from one code path.

Per-well results are appended to ``results/<run>/per_well.csv`` as they are
produced, and finished (model, well) pairs are skipped on rerun, so an
interrupted run resumes where it stopped. Distance-after-PS diagnostics are
accumulated in ``results/<run>/by_distance.csv``.

Run:

    python -m src.validate --run baselines --budget-s 600
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

from .baselines import Model, default_baselines
from .data import INFERENCE_COLS, WellPair, default_data_dir, list_wells, load_well

TRAIN_COLS = INFERENCE_COLS + ["TVT"]
DISTANCE_BUCKET_FT = 1000.0


def make_folds(wells: list[str], n_folds: int = 5, seed: int = 42) -> list[list[str]]:
    """Deterministic grouped folds: seeded shuffle, contiguous chunks."""
    rng = np.random.default_rng(seed)
    shuffled = list(np.array(sorted(wells))[rng.permutation(len(wells))])
    return [list(chunk) for chunk in np.array_split(shuffled, n_folds)]


def _score_well(model: Model, pair: WellPair) -> tuple[dict, pd.DataFrame]:
    ps = pair.prediction_start
    pred = np.asarray(model.predict(pair), dtype=float)
    true = pair.suffix_target()
    if pred.shape != true.shape:
        raise ValueError(
            f"{model.name}/{pair.name}: predicted {pred.shape}, expected {true.shape}"
        )
    se = (pred - true) ** 2
    per_well = {
        "model": model.name,
        "well": pair.name,
        "n": len(se),
        "sse": float(se.sum()),
        "rmse": float(np.sqrt(se.mean())),
    }

    md = pair.horizontal["MD"].to_numpy()
    dist = md[ps:] - md[ps - 1]
    bucket = (dist // DISTANCE_BUCKET_FT).astype(int)
    by_dist = (
        pd.DataFrame({"bucket_kft": bucket, "se": se})
        .groupby("bucket_kft")["se"]
        .agg(sse="sum", n="count")
        .reset_index()
    )
    by_dist.insert(0, "well", pair.name)
    by_dist.insert(0, "model", model.name)
    return per_well, by_dist


def run_cv(
    models: list[Model],
    data_dir: Path,
    out_dir: Path,
    n_folds: int = 5,
    seed: int = 42,
    budget_s: float | None = None,
) -> pd.DataFrame:
    train_dir = data_dir / "train"
    wells = list_wells(train_dir)
    folds = make_folds(wells, n_folds=n_folds, seed=seed)

    out_dir.mkdir(parents=True, exist_ok=True)
    per_well_path = out_dir / "per_well.csv"
    by_dist_path = out_dir / "by_distance.csv"
    done: set[tuple[str, str]] = set()
    if per_well_path.exists():
        prev = pd.read_csv(per_well_path)
        done = set(zip(prev["model"], prev["well"]))

    def loader(name: str) -> WellPair:
        return load_well(train_dir, name, columns=TRAIN_COLS)

    t0 = time.time()
    stopped = False
    for fold_idx, held_out in enumerate(folds):
        held_set = set(held_out)
        train_wells = [w for w in wells if w not in held_set]
        todo = [m for m in models if any((m.name, w) not in done for w in held_out)]
        if not todo:
            continue
        for model in todo:
            model.fit(train_wells, loader)
        for well in held_out:
            if budget_s is not None and time.time() - t0 > budget_s:
                stopped = True
                break
            pending = [m for m in todo if (m.name, well) not in done]
            if not pending:
                continue
            pair = load_well(train_dir, well, columns=TRAIN_COLS)
            for model in pending:
                per_well, by_dist = _score_well(model, pair)
                per_well["fold"] = fold_idx
                pd.DataFrame([per_well]).to_csv(
                    per_well_path, mode="a", header=not per_well_path.exists(), index=False
                )
                by_dist.to_csv(
                    by_dist_path, mode="a", header=not by_dist_path.exists(), index=False
                )
                done.add((model.name, well))
        if stopped:
            break

    res = pd.read_csv(per_well_path)
    n_expected = len(wells) * len(models)
    print(f"Scored {len(res)}/{n_expected} (model, well) pairs"
          + (" — budget hit, rerun to resume" if stopped else ""))
    if len(res) == n_expected:
        print(summarize(res).round(2).to_string())
    return res


def summarize(per_well: pd.DataFrame) -> pd.DataFrame:
    g = per_well.groupby("model").agg(
        sse=("sse", "sum"),
        n=("n", "sum"),
        med_well_rmse=("rmse", "median"),
        p90_well_rmse=("rmse", lambda s: s.quantile(0.9)),
        worst_well_rmse=("rmse", "max"),
    )
    g.insert(0, "global_rmse", np.sqrt(g.pop("sse") / g.pop("n")))
    return g


def summarize_by_distance(by_dist: pd.DataFrame) -> pd.DataFrame:
    g = by_dist.groupby(["model", "bucket_kft"]).agg(sse=("sse", "sum"), n=("n", "sum"))
    g["rmse"] = np.sqrt(g.pop("sse") / g.pop("n"))
    return g["rmse"].unstack("model")


def build_models(names: str, data_dir: Path) -> list[Model]:
    from .topology import RegionalDipPrior, SpatialTopology

    train_dir = data_dir / "train"
    cache = data_dir.parent / "results" / "cache" / "surface_samples.parquet"
    from .baselines import ConstantTVT
    from .ensemble import PrefixPlayoff, SoftBlendPlayoff
    from .gate import DipAxisGate, LearnedGate
    from .gr import GRStateSpace
    from .panel import DirectPanelPhase, EarlyPanelBlend
    from .topology import TrendCorrectedSpatial

    registry: dict[str, Callable[[], list[Model]]] = {
        "baselines": default_baselines,
        "stage2": lambda: [SpatialTopology(train_dir, cache)],
        "dip-axis": lambda: [RegionalDipPrior(train_dir, cache)],
        "dip-axis-sweep": lambda: [
            RegionalDipPrior(train_dir, cache, residual_shrink=s)
            for s in (0.1, 0.15, 0.2)
        ],
        "playoff": lambda: [PrefixPlayoff(
            [ConstantTVT(), SpatialTopology(train_dir, cache)])],
        "playoff-sweep": lambda: [
            PrefixPlayoff([ConstantTVT(), SpatialTopology(train_dir, cache)],
                          eval_window_ft=w, margin_ft=m)
            for w in (700.0, 1000.0) for m in (0.0, 1.0)
        ],
        "gate": lambda: [LearnedGate(train_dir, data_dir.parent / "results")],
        "dip-gate": lambda: [
            DipAxisGate(train_dir, data_dir.parent / "results")
        ],
        "dip-gate-sweep": lambda: [
            DipAxisGate(train_dir, data_dir.parent / "results", residual_shrink=s)
            for s in (0.1, 0.15, 0.2)
        ],
        "gr": lambda: [GRStateSpace(LearnedGate(train_dir, data_dir.parent / "results"),
                                    shape_weight=0.0)],
        "gr-shrink": lambda: [GRStateSpace(
            LearnedGate(train_dir, data_dir.parent / "results"), shrink=0.5,
            shape_weight=0.0)],
        "best": lambda: [GRStateSpace(
            LearnedGate(train_dir, data_dir.parent / "results"),
            level_weight=1.0, shape_weight=0.0,
            sigma_vel=0.05, adaptive_scale=3.0, shrink=0.7,
            bias_cache=(train_dir,
                        data_dir.parent / "results" / "cache" / "bias_samples.csv"))],
        "dip-best": lambda: [GRStateSpace(
            DipAxisGate(train_dir, data_dir.parent / "results",
                        uphill_shrink=0.0, downhill_shrink=0.15),
            level_weight=1.0, shape_weight=0.0,
            sigma_vel=0.05, adaptive_scale=3.0, shrink=0.7,
            bias_cache=(train_dir,
                        data_dir.parent / "results" / "cache" / "bias_samples.csv"))],
        "panel": lambda: [DirectPanelPhase()],
        "panel-best": lambda: [EarlyPanelBlend(
            GRStateSpace(
                DipAxisGate(train_dir, data_dir.parent / "results",
                            uphill_shrink=0.0, downhill_shrink=0.15),
                level_weight=1.0, shape_weight=0.0,
                sigma_vel=0.05, adaptive_scale=3.0, shrink=0.7,
                bias_cache=(train_dir,
                            data_dir.parent / "results" / "cache" / "bias_samples.csv")),
            weight=0.30,
            max_distance_ft=1000.0,
        )],
        "dip-best-sweep": lambda: [GRStateSpace(
            DipAxisGate(train_dir, data_dir.parent / "results", residual_shrink=s),
            level_weight=1.0, shape_weight=0.0,
            sigma_vel=0.05, adaptive_scale=3.0, shrink=0.7,
            bias_cache=(train_dir,
                        data_dir.parent / "results" / "cache" / "bias_samples.csv"))
            for s in (0.05, 0.1, 0.15)
        ],
        "gr-bold": lambda: [
            GRStateSpace(LearnedGate(train_dir, data_dir.parent / "results"),
                         level_weight=1.0, shape_weight=0.0,
                         sigma_vel=0.05, adaptive_scale=sc, shrink=sh,
                         bias_cache=(train_dir,
                                     data_dir.parent / "results" / "cache" / "bias_samples.csv"))
            for sc, sh in ((3.0, 0.7), (5.0, 1.0))
        ],
        "gr-shape": lambda: [
            GRStateSpace(LearnedGate(train_dir, data_dir.parent / "results"),
                         shrink=s, bias_cache=(
                             train_dir,
                             data_dir.parent / "results" / "cache" / "bias_samples.csv"))
            for s in (0.5, 1.0)
        ],
        "gr-bias": lambda: [GRStateSpace(
            LearnedGate(train_dir, data_dir.parent / "results"), shrink=0.5,
            shape_weight=0.0,
            bias_cache=(train_dir,
                        data_dir.parent / "results" / "cache" / "bias_samples.csv"))],
        "gr-sweep": lambda: [
            GRStateSpace(LearnedGate(train_dir, data_dir.parent / "results"),
                         sigma_geo_ft=g, sigma_vel=v)
            for g, v in ((15.0, 0.01), (15.0, 0.05), (30.0, 0.02))
        ],
        "stage2b": lambda: [
            TrendCorrectedSpatial(train_dir, cache),
            SoftBlendPlayoff([ConstantTVT(), SpatialTopology(train_dir, cache)]),
            SoftBlendPlayoff([ConstantTVT(), SpatialTopology(train_dir, cache),
                              TrendCorrectedSpatial(train_dir, cache)]),
        ],
    }
    models: list[Model] = []
    for name in names.split(","):
        models.extend(registry[name.strip()]())
    return models


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", default="baselines", help="results subdirectory name")
    ap.add_argument("--models", default="baselines",
                    help="comma-separated model sets: baselines, stage2")
    ap.add_argument("--data-dir", type=Path, default=default_data_dir())
    ap.add_argument("--n-folds", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--budget-s", type=float, default=None,
                    help="stop after this many seconds; rerun to resume")
    args = ap.parse_args()

    out_dir = args.data_dir.parent / "results" / args.run
    run_cv(build_models(args.models, args.data_dir), args.data_dir, out_dir,
           n_folds=args.n_folds, seed=args.seed, budget_s=args.budget_s)


if __name__ == "__main__":
    main()
