"""LightGBM baseline for Playground Series S6E6 — stellar class prediction.

Stratified 5-fold multiclass LightGBM with photometric color features.
Saves out-of-fold predictions, per-fold scores, and a submission file.

Run from the competition root:
    python src/train_lgbm.py
"""

from __future__ import annotations

import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

SEED = 42
N_FOLDS = 5
# research/<R>/code/src -> the research item is parents[2]
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SUBS = ROOT / "output" / "submissions"
ARTIFACTS = ROOT / "output" / "artifacts"

TARGET = "class"
ID = "id"
BANDS = ["u", "g", "r", "i", "z"]
CATS = ["spectral_type", "galaxy_population"]
# alpha/delta (sky coords) KEPT: strong class signal. Galactic-plane sightlines
# are star-rich, which breaks the low-z STAR/GALAXY degeneracy that color misses.
# Empirically worth ~+1.4pt OOF accuracy and +4.4pt STAR recall. See EDA.
DROP: list[str] = []


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer physically-motivated features. Identical on train and test."""
    df = df.copy()
    # Photometric color indices: adjacent-band magnitude differences.
    df["u_g"] = df["u"] - df["g"]
    df["g_r"] = df["g"] - df["r"]
    df["r_i"] = df["r"] - df["i"]
    df["i_z"] = df["i"] - df["z"]
    # Soft Lyman-break / u-dropout feature: ramps up once the break enters
    # the u band (~z=1.5). Captures the redshift-dependent QSO color shift.
    df["dropout"] = np.clip(df["redshift"] - 1.5, 0.0, None)
    # Interaction that encodes the non-monotonic redshift x u-g relationship.
    df["redshift_x_ug"] = df["redshift"] * df["u_g"]
    # Cast categoricals for LightGBM native handling.
    for c in CATS:
        df[c] = df[c].astype("category")
    return df


def main() -> None:
    t0 = time.time()
    SUBS.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv(DATA / "train.csv")
    test = pd.read_csv(DATA / "test.csv")

    le = LabelEncoder()
    y = le.fit_transform(train[TARGET])
    n_class = len(le.classes_)
    print(f"classes: {list(le.classes_)}  | train={len(train):,}  test={len(test):,}")

    train = add_features(train)
    test = add_features(test)
    features = [c for c in train.columns if c not in [ID, TARGET, *DROP]]
    print(f"features ({len(features)}): {features}")

    params = {
        "objective": "multiclass",
        "num_class": n_class,
        "metric": "multi_logloss",
        "learning_rate": 0.12,
        "num_leaves": 127,
        "max_depth": -1,
        "min_child_samples": 50,
        "feature_fraction": 0.8,
        "bagging_fraction": 0.8,
        "bagging_freq": 1,
        "lambda_l2": 1.0,
        "class_weight": "balanced",
        "n_jobs": -1,
        "seed": SEED,
        "verbose": -1,
    }

    oof = np.zeros((len(train), n_class))
    test_pred = np.zeros((len(test), n_class))
    importances = np.zeros(len(features))
    scores: list[float] = []

    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    for fold, (tr, va) in enumerate(skf.split(train[features], y)):
        dtr = lgb.Dataset(train.iloc[tr][features], label=y[tr], categorical_feature=CATS)
        dva = lgb.Dataset(train.iloc[va][features], label=y[va], categorical_feature=CATS)
        model = lgb.train(
            params,
            dtr,
            num_boost_round=250,
            valid_sets=[dva],
            callbacks=[lgb.early_stopping(30, verbose=False), lgb.log_evaluation(0)],
        )
        oof[va] = model.predict(train.iloc[va][features])
        test_pred += model.predict(test[features]) / N_FOLDS
        importances += model.feature_importance(importance_type="gain") / N_FOLDS

        acc = accuracy_score(y[va], oof[va].argmax(1))
        scores.append(acc)
        print(f"fold {fold}: acc={acc:.5f}  best_iter={model.best_iteration}")

    oof_acc = accuracy_score(y, oof.argmax(1))
    oof_ll = log_loss(y, oof)
    print(f"\nOOF accuracy: {oof_acc:.5f}  (folds {np.mean(scores):.5f} +/- {np.std(scores):.5f})")
    print(f"OOF logloss : {oof_ll:.5f}")

    print("\nfeature importance (gain):")
    for f, imp in sorted(zip(features, importances), key=lambda x: -x[1]):
        print(f"  {f:16s} {imp:12.0f}")

    # Save OOF + artifacts for later blending.
    np.save(ARTIFACTS / "oof_lgbm.npy", oof)
    np.save(ARTIFACTS / "test_lgbm.npy", test_pred)

    # Submission in exact sample format: id + predicted label.
    sub = pd.DataFrame({ID: test[ID], TARGET: le.inverse_transform(test_pred.argmax(1))})
    out = SUBS / "submission_lgbm.csv"
    sub.to_csv(out, index=False)
    print(f"\nwrote {out}  ({len(sub):,} rows)")
    print(sub[TARGET].value_counts().to_string())
    print(f"\ndone in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
