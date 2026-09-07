"""Low-learning-rate LightGBM with per-fold checkpointing.

Low LR needs many boosting rounds, which can exceed a single run window, and
this environment doesn't persist background processes. So each invocation
trains the next un-checkpointed fold and saves its OOF + test predictions to
artifacts/cv_lowlr/. Once all folds exist, it combines them: reports OOF
accuracy and writes the submission.

Just run repeatedly until it prints "ALL FOLDS DONE", then once more to combine:
    python src/train_lgbm_lowlr.py    # trains fold 0, then 1, ... then combines
"""

from __future__ import annotations

import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, log_loss, recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

SEED = 42
N_FOLDS = 5
# experiments/kaggle/stellar/src -> observatory root is parents[4]
ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / "_data" / "kaggle" / "stellar"
SUBS = ROOT / "_outputs" / "kaggle" / "stellar" / "submissions"
ARTIFACTS = ROOT / "_outputs" / "kaggle" / "stellar" / "artifacts"
CKPT = ARTIFACTS / "cv_lowlr"

CATS = ["spectral_type", "galaxy_population"]
FEATURES = [
    "alpha", "delta", "u", "g", "r", "i", "z", "redshift",
    "spectral_type", "galaxy_population",
    "u_g", "g_r", "r_i", "i_z", "dropout", "redshift_x_ug",
]

PARAMS = {
    "objective": "multiclass",
    "num_class": 3,
    "metric": "multi_logloss",
    "learning_rate": 0.03,  # low LR — slow & careful
    "num_leaves": 127,
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


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["u_g"] = df["u"] - df["g"]
    df["g_r"] = df["g"] - df["r"]
    df["r_i"] = df["r"] - df["i"]
    df["i_z"] = df["i"] - df["z"]
    df["dropout"] = np.clip(df["redshift"] - 1.5, 0.0, None)
    df["redshift_x_ug"] = df["redshift"] * df["u_g"]
    for c in CATS:
        df[c] = df[c].astype("category")
    return df


def folds(y: np.ndarray):
    skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    return list(skf.split(np.zeros(len(y)), y))


def main() -> None:
    t0 = time.time()
    CKPT.mkdir(parents=True, exist_ok=True)
    train = add_features(pd.read_csv(DATA / "train.csv"))
    le = LabelEncoder()
    y = le.fit_transform(train["class"])
    splits = folds(y)

    # Find next fold to train.
    next_fold = next((k for k in range(N_FOLDS) if not (CKPT / f"fold{k}.npz").exists()), None)

    if next_fold is not None:
        test = add_features(pd.read_csv(DATA / "test.csv"))
        tr, va = splits[next_fold]
        dtr = lgb.Dataset(train.iloc[tr][FEATURES], label=y[tr], categorical_feature=CATS)
        dva = lgb.Dataset(train.iloc[va][FEATURES], label=y[va], categorical_feature=CATS)
        model = lgb.train(
            PARAMS, dtr, num_boost_round=3000, valid_sets=[dva],
            callbacks=[lgb.early_stopping(100, verbose=False), lgb.log_evaluation(0)],
        )
        val_pred = model.predict(train.iloc[va][FEATURES])
        test_pred = model.predict(test[FEATURES])
        acc = accuracy_score(y[va], val_pred.argmax(1))
        np.savez(
            CKPT / f"fold{next_fold}.npz",
            val_idx=va, val_pred=val_pred, test_pred=test_pred,
            best_iter=model.best_iteration,
        )
        print(f"fold {next_fold}: acc={acc:.5f}  best_iter={model.best_iteration}  ({time.time()-t0:.1f}s)")
        remaining = [k for k in range(N_FOLDS) if not (CKPT / f"fold{k}.npz").exists()]
        print("ALL FOLDS DONE" if not remaining else f"remaining folds: {remaining} — run again")
        return

    # All folds present -> combine.
    print("combining 5 folds...")
    oof = np.zeros((len(train), 3))
    test_pred = None
    iters = []
    for k in range(N_FOLDS):
        d = np.load(CKPT / f"fold{k}.npz")
        oof[d["val_idx"]] = d["val_pred"]
        tp = d["test_pred"]
        test_pred = tp / N_FOLDS if test_pred is None else test_pred + tp / N_FOLDS
        iters.append(int(d["best_iter"]))

    acc = accuracy_score(y, oof.argmax(1))
    ll = log_loss(y, oof)
    star = recall_score(y, oof.argmax(1), labels=[list(le.classes_).index("STAR")], average="macro")
    print(f"OOF accuracy: {acc:.5f}   logloss: {ll:.5f}   STAR recall: {star:.4f}")
    print(f"best_iters per fold: {iters}  (lr={PARAMS['learning_rate']})")
    print("compare: lr=0.12 baseline OOF acc=0.96782")

    np.save(ROOT / "artifacts" / "oof_lgbm_lowlr.npy", oof)
    np.save(ROOT / "artifacts" / "test_lgbm_lowlr.npy", test_pred)
    test = pd.read_csv(DATA / "test.csv")
    sub = pd.DataFrame({"id": test["id"], "class": le.inverse_transform(test_pred.argmax(1))})
    sub.to_csv(SUBS / "submission_lgbm_lowlr.csv", index=False)
    print(f"wrote {SUBS / 'submission_lgbm_lowlr.csv'}")
    print(sub["class"].value_counts().to_string())


if __name__ == "__main__":
    main()
