"""Hidden-test discovery and submission generation.

Runs the full best-known stack (F7: F6 plus a short-range phase-aware panel
update — see the README experiment log) against whatever wells are present in
``test/``, and writes ``submission.csv``.

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

from .baselines import Model, default_baselines
from .data import default_data_dir, list_wells, load_well, resolve_data_dir
from .gate import TABLE_NAME, DipAxisGate, build_gate_table
from .gr import GRStateSpace, build_bias_samples
from .panel import DirectPanelPhase, EarlyPanelBlend
from .topology import SpatialTopology, build_surface_samples
from .validate import run_cv


def ensure_artifacts(data_dir: Path, results_dir: Path) -> None:
    """Build every derived artifact the stack needs, training data only."""
    train_dir = data_dir / "train"
    cache = results_dir / "cache"
    cache.mkdir(parents=True, exist_ok=True)

    build_surface_samples(train_dir, cache / "surface_samples.parquet")
    build_bias_samples(train_dir, cache / "bias_samples.csv")

    # Leakage-safe per-well labels for the gate come from grouped CV runs.
    if not (results_dir / "baselines" / "per_well.csv").exists():
        run_cv(default_baselines(), data_dir, results_dir / "baselines")
    if not (results_dir / "stage2" / "per_well.csv").exists():
        run_cv([SpatialTopology(train_dir, cache / "surface_samples.parquet")],
               data_dir, results_dir / "stage2")

    build_gate_table(data_dir, cache / TABLE_NAME, results_dir=results_dir)


def build_model(data_dir: Path, results_dir: Path) -> Model:
    """The best-known configuration (F7), fitted on all training wells."""
    train_dir = data_dir / "train"
    f6 = GRStateSpace(
        DipAxisGate(
            train_dir, results_dir, uphill_shrink=0.0, downhill_shrink=0.15
        ),
        level_weight=1.0,
        shape_weight=0.0,
        sigma_vel=0.05,
        adaptive_scale=3.0,
        shrink=0.7,
        bias_cache=(train_dir, results_dir / "cache" / "bias_samples.csv"),
    )
    model = EarlyPanelBlend(
        f6,
        panel=DirectPanelPhase(),
        weight=0.30,
        max_distance_ft=1000.0,
    )
    model.fit(list_wells(train_dir), lambda name: load_well(train_dir, name))
    return model


def predict_test(model: Model, data_dir: Path,
                 transductive: bool = True) -> pd.DataFrame:
    test_dir = data_dir / "test"
    test_wells = list_wells(test_dir)
    pairs = [load_well(test_dir, w) for w in test_wells]
    if transductive and hasattr(model, "observe_test"):
        # Test wells' observed prefixes (s = TVT_input + Z, prefix GR
        # residuals) densify the spatial surface and GR bias field exactly
        # where predictions happen — including hidden wells supporting each
        # other. No labels involved; CV-neutral globally, improves the tail
        # and out-of-support wells (README log, run `transductive`).
        model.observe_test(pairs)
        print(f"transductive: observed {len(pairs)} test-well prefixes")
    rows = []
    for pair in pairs:
        pred = np.asarray(model.predict(pair), dtype=float)
        for id_, tvt in zip(pair.submission_ids(), pred):
            rows.append((id_, float(tvt)))
        print(f"{pair.name}: {len(pred)} rows, "
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
    ap.add_argument("--no-transductive", action="store_true",
                    help="skip observing test-well prefixes before predicting")
    args = ap.parse_args()

    data_dir = resolve_data_dir(args.data_dir)
    print(f"competition data: {data_dir}")
    results_dir = args.results_dir or data_dir.parent / "results"
    out = args.out or data_dir.parent / "submissions" / "submission.csv"

    ensure_artifacts(data_dir, results_dir)
    model = build_model(data_dir, results_dir)
    preds = predict_test(model, data_dir,
                         transductive=not args.no_transductive)
    submission = reconcile(preds, data_dir)

    out.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(out, index=False)
    print(f"wrote {len(submission)} rows -> {out}")


if __name__ == "__main__":
    main()
