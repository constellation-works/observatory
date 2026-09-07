# CLAUDE.md — Predicting Stellar Class (Playground Series S6E6)

Competition-specific guidance. See `../CLAUDE.md` for workspace-wide conventions.

## Problem

Multi-class classification of stellar class from tabular astronomical features
(SDSS-style: typically `GALAXY`, `STAR`, `QSO`). The training data is
synthetically generated from a real dataset, so distributions are close to the
original but not identical.

## Before modeling

- Read the Data tab: confirm the **target column**, class labels, feature
  meanings, and the exact **evaluation metric** (Playground multiclass is
  commonly accuracy — verify). Optimize that metric directly.
- Check class balance; stellar datasets are usually imbalanced (GALAXY/STAR
  dominate, QSO rarer). Use stratified CV.
- Inspect for physically implausible values (e.g. magnitude placeholders like
  -9999) and decide on cleaning consistently across train and test.

## Approach

- Baseline: gradient boosting (LightGBM/XGBoost/CatBoost) on raw features with
  stratified K-fold — strong default for this kind of tabular problem.
- Feature ideas: photometric color indices (differences between band
  magnitudes), redshift-derived features. Keep transforms identical on test.
- Consider blending GBDT models; a tuned single GBDT is a solid first target.
- Watch for leakage from id-like columns; drop or treat carefully.

## Reproducibility

- Fixed seed across `numpy`, framework RNGs, and CV splits.
- Save out-of-fold predictions and per-fold scores so runs are comparable.
- Trust local stratified CV over public LB movement.

## Output

Submission must match `sample_submission.csv` format exactly (id column +
predicted class label). Write to `submissions/`.
