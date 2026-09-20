"""Coarse-to-fine cascade for Playground Series S6E6.

Stage 1: general 3-class LightGBM (reuses OOF from train_lgbm.py).
Stage 2: binary STAR-vs-GALAXY specialist, trained on the low-redshift zone
         where the two classes are confusable, with color x magnitude features.

Routing (test-time-available info only): if stage 1 predicts STAR or GALAXY
*and* redshift < ZONE, defer the STAR/GALAXY decision to the specialist.

Evaluation is leakage-free: stage-2 OOF is built on the *same* folds as the
saved stage-1 OOF, and routing uses out-of-fold predictions only.

    python src/train_cascade.py
"""

from __future__ import annotations

import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

SEED = 42
N_FOLDS = 5
ZONE = 0.5  # redshift below which STAR/GALAXY confusion lives; routing + specialist scope
# research/<R>/code/src -> the research item is parents[2]
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
ARTIFACTS = ROOT / "output" / "artifacts"
SUBS = ROOT / "output" / "submissions"

CATS = ["spectral_type", "galaxy_population"]


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["u_g"] = df["u"] - df["g"]
    df["g_r"] = df["g"] - df["r"]
    df["r_i"] = df["r"] - df["i"]
    df["i_z"] = df["i"] - df["z"]
    df["dropout"] = np.clip(df["redshift"] - 1.5, 0.0, None)
    df["redshift_x_ug"] = df["redshift"] * df["u_g"]
    # Color x magnitude: breaks the red-M-star vs red-galaxy degeneracy.
    # A red, *bright* object is a nearby star; a red, *faint* one is a galaxy.
    df["gr_x_r"] = df["g_r"] * df["r"]
    df["ug_x_r"] = df["u_g"] * df["r"]
    for c in CATS:
        df[c] = df[c].astype("category")
    return df


# Specialist uses base features + the targeted interactions.
SPEC_FEATS = [
    "u", "g", "r", "i", "z", "redshift", "spectral_type", "galaxy_population",
    "u_g", "g_r", "r_i", "i_z", "gr_x_r", "ug_x_r",
]


def main() -> None:
    t0 = time.time()
    SUBS.mkdir(parents=True, exist_ok=True)

    train = add_features(pd.read_csv(DATA / "train.csv"))
    test = add_features(pd.read_csv(DATA / "test.csv"))

    le = LabelEncoder()
    y = le.fit_transform(train["class"])  # GALAXY=0, QSO=1, STAR=2
    classes = list(le.classes_)
    g_idx, s_idx = classes.index("GALAXY"), classes.index("STAR")

    # Stage-1 OOF from the baseline (same folds as below).
    stage1_oof = np.load(ARTIFACTS / "oof_lgbm.npy")
    stage1_pred = stage1_oof.argmax(1)

    spec_params = {
        "objective": "binary",
        "metric": "binary_logloss",
        "learning_rate": 0.05,
        "num_leaves": 63,
        "min_child_samples": 40,
        "feature_fraction": 0.8,
        "bagging_fraction": 0.8,
        "bagging_freq": 1,
        "lambda_l2": 1.0,
        "is_unbalance": True,
        "n_jobs": -1,
        "seed": SEED,
        "verbose": -1,
    }

    # Binary target within the STAR/GALAXY specialist: 1 = STAR, 0 = GALAXY.
    is_star = (y == s_idx).astype(int)
    sg_mask = np.isin(y, [g_idx, s_idx])  # STAR or GALAXY rows
    in_zone = train["redshift"].values < ZONE

    # Stage-2 OOF: specialist P(STAR) for every training row, out-of-fold.
    spec_oof = np.full(len(train), np.nan)
    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    for tr, va in skf.split(train, y):
        # Train only on low-z STAR/GALAXY rows in this fold (both correct & wrong).
        tr_spec = tr[sg_mask[tr] & in_zone[tr]]
        dtr = lgb.Dataset(
            train.iloc[tr_spec][SPEC_FEATS], label=is_star[tr_spec], categorical_feature=CATS
        )
        model = lgb.train(spec_params, dtr, num_boost_round=400)
        spec_oof[va] = model.predict(train.iloc[va][SPEC_FEATS])

    # ---- Cascade combination (out-of-fold, honest) ----
    # Route only rows that are (a) predicted STAR/GALAXY, (b) in the low-z zone,
    # and (c) *uncertain* per stage-1 confidence. Confident calls keep stage-1.
    def cascade(stage1_p, stage1_conf, p_star, z, thr=0.5, conf_gate=1.0):
        final = stage1_p.copy()
        routed = np.isin(stage1_p, [g_idx, s_idx]) & (z < ZONE) & (stage1_conf < conf_gate)
        final[routed] = np.where(p_star[routed] >= thr, s_idx, g_idx)
        return final, routed

    z = train["redshift"].values
    stage1_conf = stage1_oof.max(1)
    base_acc = accuracy_score(y, stage1_pred)
    base_star = recall_score(y, stage1_pred, labels=[s_idx], average="macro")

    print(f"baseline (stage-1 only):  acc={base_acc:.5f}  STAR recall={base_star:.4f}")
    print(f"\nrouting zone: z < {ZONE}  | scan over confidence gate x decision threshold:\n")

    best = (base_acc, 0.5, 1.0, stage1_pred)
    for conf_gate in [0.70, 0.85, 0.95, 1.00]:
        for thr in [0.45, 0.50, 0.55, 0.60]:
            final, routed = cascade(stage1_pred, stage1_conf, spec_oof, z, thr, conf_gate)
            acc = accuracy_score(y, final)
            star = recall_score(y, final, labels=[s_idx], average="macro")
            print(
                f"  gate={conf_gate:.2f} thr={thr:.2f}: acc={acc:.5f} "
                f"(delta {acc - base_acc:+.5f})  STAR recall={star:.4f}  routed={routed.sum():,}"
            )
            if acc > best[0]:
                best = (acc, thr, conf_gate, final)
        print()

    best_acc, best_thr, best_gate, best_pred = best
    improved = best_acc > base_acc
    print(f"best: acc={best_acc:.5f} at thr={best_thr:.2f} gate={best_gate:.2f}  (delta {best_acc - base_acc:+.5f})")
    if not improved:
        print("=> cascade does NOT beat baseline; STAR/GALAXY overlap is irreducible with these features.")
    print("\nconfusion matrix (rows=true, cols=pred)", classes)
    print(confusion_matrix(y, best_pred))

    # ---- Refit on full data and write submission with the best threshold ----
    dtr_full = lgb.Dataset(
        train[sg_mask & in_zone][SPEC_FEATS],
        label=is_star[sg_mask & in_zone],
        categorical_feature=CATS,
    )
    spec_full = lgb.train(spec_params, dtr_full, num_boost_round=400)

    if not improved:
        print("\nskipping cascade submission — baseline submission_lgbm.csv remains best.")
        print(f"done in {time.time() - t0:.1f}s")
        return

    test_stage1_oof = np.load(ARTIFACTS / "test_lgbm.npy")
    test_stage1 = test_stage1_oof.argmax(1)
    test_conf = test_stage1_oof.max(1)
    test_pstar = spec_full.predict(test[SPEC_FEATS])
    test_final, test_routed = cascade(
        test_stage1, test_conf, test_pstar, test["redshift"].values, best_thr, best_gate
    )

    sub = pd.DataFrame({"id": test["id"], "class": le.inverse_transform(test_final)})
    out = SUBS / "submission_cascade.csv"
    sub.to_csv(out, index=False)
    print(f"\nwrote {out}  (routed {test_routed.sum():,} of {len(test):,} test rows)")
    print(sub["class"].value_counts().to_string())
    print(f"\ndone in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
