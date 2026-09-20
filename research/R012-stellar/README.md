---
id: R012
title: Stellar
status: done
tags: [kaggle, astronomy, machine-learning]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: []
---

# R012 — Stellar class prediction (Playground S6E6)

Origin: the `stellar` competition workspace, migrated with the kaggle domain.
`tests` is empty: nothing here bears on a hypothesis in this corpus.

## Question

Predict the stellar class (star, galaxy, quasar) from photometry and sky
position — and how much of the remaining error is irreducible without sky
information?

## Method

LightGBM over colour indices with dropout and interaction features, 5-fold CV,
in `code/src/train_lgbm.py`, plus a low-learning-rate variant
(`train_lgbm_lowlr.py`) and a two-stage cascade (`train_cascade.py`). Data is
fetched per `data/manifest.json`; submissions are written to the ignored
`output/`.

## Result

0.95401 accuracy from colour indices alone; **0.96782** once alpha/delta are kept,
a +1.4-point gain that comes from galactic-plane sightlines being star-rich and so
breaking the low-redshift star/galaxy degeneracy (STAR recall 0.88 → 0.93,
logloss 0.090). Dropping the learning rate to 0.03 adds 0.0003 accuracy — inside
fold noise — so the model was already converged at 0.12.

## Limitations

Public-leaderboard scores were never recorded against these CV numbers, so the
CV-to-LB relationship is unmeasured. Categorising the coordinates hurts (−0.4
points) and the star-versus-galaxy cascade gave no gain: the remaining overlap
looks irreducible without more sky information, which is an observation about
this dataset, not a result about stellar classification.

## Next

None: a playground competition, kept for the sky-coordinate lesson.

---

# Competition notes

Kept as written, from `experiments/kaggle/stellar/README.md`.
Paths in it are the old layout's: the code is now `code/`, the data
`data/` and the run products `output/`, both ignored by git.

Kaggle Playground Series, Season 6 Episode 6.
<https://www.kaggle.com/competitions/playground-series-s6e6/overview>

## Task

Multi-class classification: predict the **stellar class** of an astronomical
object from its tabular features. Classes follow the SDSS stellar classification
(e.g. `GALAXY`, `STAR`, `QSO`). Confirm exact classes, features, and the
evaluation metric on the competition's Overview/Data tabs before modeling.

## Structure

```
stellar/
├── data/          # train.csv, test.csv, sample_submission.csv (gitignored)
├── notebooks/     # EDA & experiments
├── src/           # features, models, training, inference
├── submissions/   # generated submission files
└── README.md
```

## Get the data

```bash
kaggle competitions download -c playground-series-s6e6 -p data
unzip 'data/*.zip' -d data
```

## Submit

```bash
kaggle competitions submit -c playground-series-s6e6 \
  -f submissions/submission.csv -m "description"
```

## Notes / log

Track experiments here — CV scheme, local CV score vs. public LB, key features.

| Date | Model | CV | Public LB | Notes |
|------|-------|----|-----------|-------|
| 2026-06-07 | LightGBM 5-fold | 0.95401 acc | — | Baseline. Color indices + dropout/interaction feats; alpha/delta dropped. logloss 0.1223. STAR weakest (recall 0.88); errors concentrate at z<0.1 (acc 0.88 vs 0.97). `src/train_lgbm.py` |
| 2026-06-07 | LightGBM 5-fold + sky coords | 0.96782 acc | — | **+1.4pt** from keeping alpha/delta (galactic-plane sightlines are star-rich → breaks low-z STAR/GALAXY tie). STAR recall 0.88→0.93. logloss 0.090. Categorizing coords hurts (-0.4pt); galactic latitude marginal. STAR-vs-GALAXY cascade gave no gain (overlap irreducible w/o sky info). `src/train_lgbm.py` |
| 2026-06-07 | LightGBM lr=0.03 (~600 trees) | 0.96813 acc | — | Low LR: +0.0003 acc (within fold noise), logloss 0.090→0.089. No real accuracy gain; model already converged at lr=0.12. Per-fold checkpointed `src/train_lgbm_lowlr.py`. |
