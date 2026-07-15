"""Hidden-test discovery and submission generation.

Runs the full best-known stack (F6: GR state-space correction over the
dip-axis-augmented A/D gate — see the README experiment log) against whatever
wells are present in ``test/``, and writes ``submission.csv``.

Designed for the Kaggle notebook rerun: internet-free, self-sufficient, and
path-parameterized (competition input is read-only on Kaggle, so every
derived artifact goes to ``--results-dir``). All caches and the gate's
training labels are rebuilt from the training data alone when missing;
with a warm cache the whole run is minutes, cold it is well under the
9-hour budget.

Local dry run (visible test wells):

    python -m src.submit

Kaggle:

    python -m src.submit \
        --data-dir /kaggle/input/rogii-wellbore-geology-prediction \
        --results-dir /kaggle/working/results \
        --out /kaggle/working/submission.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from .baselines import default_baselines
from .data import default_data_dir, list_wells, load_well
from .gate import TABLE_NAME, DipAxisGate, build_gate_table
from .gr import GRStateSpace, build_bias_samples
from .topology import SpatialTopology, build_surface_samples
from .validate import run_cv


def ensure_artifacts(data_dir: Path, results_dir: Path) -> None:
    """Build every derived artifact the stack needs, training data only."""
    train_dir = data_dir / "train"
    cache = results_dir / "cache"
    cache.mkdir(parents=True, exist_ok=True)

    build_surface_samples(train_dir, cache / "surface_samples.parquet")
    build_bias_samples(train_dir, cache / "bias_samples.csv")
    build_gate_table(data_dir, cache / TABLE_NAME, results_dir=results_dir)

    # Leakage-safe per-well labels for the gate come from grouped CV runs.
    if not (results_dir / "baselines" / "per_well.csv").exists():
        run_cv(default_baselines(), data_dir, results_dir / "baselines")
    if not (results_dir / "stage2" / "per_well.csv").exists():
        run_cv([SpatialTopology(train_dir, cache / "surface_samples.parquet")],
               data_dir, results_dir / "stage2")


def build_model(data_dir: Path, results_dir: Path) -> GRStateSpace:
    """The best-known configuration (F6), fitted on all training wells."""
    train_dir = data_dir / "train"
    model = GRStateSpace(
        DipAxisGate(train_dir, results_dir, residual_shrink=0.1),
        level_weight=1.0, shape_weight=0.0,
        sigma_vel=0.05, adaptive_scale=3.0, shrink=0.7,
        bias_cache=(train_dir, results_dir / "cache" / "bias_samples.csv"),
    )
    model.fit(list_wells(train_dir), None)
    return model


def predict_test(model: GRStateSpace, data_dir: Path) -> pd.DataFrame:
    test_dir = data_dir / "test"
    rows = []
    for well in list_wells(test_dir):
        pair = load_well(test_dir, well)
        pred = np.asarray(model.predict(pair), dtype=float)
        for id_, tvt in zip(pair.submission_ids(), pred):
            rows.append((id_, float(tvt)))
        print(f"{well}: {len(pred)} rows, "
              f"range {pred.min():.1f}..{pred.max():.1f}")
    return pd.DataFrame(rows, columns=["id", "tvt"])


def reconcile(preds: pd.DataFrame, data_dir: Path) -> pd.DataFrame:
    """Conform to sample_submission's ids and order when it exists."""
    sample_path = data_dir / "sample_submission.csv"
    if not sample_path.exists():
        return preds
    sample = pd.read_csv(sample_path)
    lookup = dict(zip(preds["id"], preds["tvt"]))
    missing = [i for i in sample["id"] if i not in lookup]
    if missing:
        # Should not happen; keep the submission valid rather than crash.
        fallback = float(np.median(preds["tvt"])) if len(preds) else 0.0
        print(f"WARNING: {len(missing)} sample ids missing from predictions "
              f"(e.g. {missing[:3]}); filling with {fallback:.1f}")
    extra = len(preds) - (len(sample) - len(missing))
    if extra:
        print(f"note: {extra} predicted ids not in sample_submission; dropped")
    out = sample.copy()
    out["tvt"] = [lookup.get(i, float(np.median(preds["tvt"])))
                  for i in sample["id"]]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=default_data_dir())
    ap.add_argument("--results-dir", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    data_dir = args.data_dir
    results_dir = args.results_dir or data_dir.parent / "results"
    out = args.out or data_dir.parent / "submissions" / "submission.csv"

    ensure_artifacts(data_dir, results_dir)
    model = build_model(data_dir, results_dir)
    preds = predict_test(model, data_dir)
    submission = reconcile(preds, data_dir)

    out.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(out, index=False)
    print(f"wrote {len(submission)} rows -> {out}")


if __name__ == "__main__":
    main()
