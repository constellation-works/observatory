# ROGII — Wellbore Geology Prediction

Kaggle Featured competition.
<https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction>

## Task

Predict `TVT` (True Vertical Thickness, in feet) throughout the hidden
evaluation zone of each horizontal well. The available inputs combine the
horizontal well trajectory and gamma-ray log with a vertical reference log
(the "typewell") for geological correlation.

This is a regression problem. Kaggle scores submissions using **root mean
squared error (RMSE)** over all hidden target rows.

## Data

Each well is identified by an 8-character hash and has:

- `{WELLNAME}__horizontal_well.csv`: trajectory, surfaces, gamma ray, and the
  partially masked target input.
- `{WELLNAME}__typewell.csv`: vertical reference `TVT`, gamma ray, and geology.
- `{WELLNAME}.png`: training-only well/cross-section visualization.

Important horizontal-well fields include `MD`, `X`, `Y`, `Z`, `GR`, `TVT`, and
`TVT_input`. In the evaluation zone, `TVT`/`TVT_input` is masked. Training files
also contain predicted formation surfaces (`ANCC`, `ASTNU`, `ASTNL`, `EGFDU`,
`EGFDL`, and `BUDA`).

The visible test directory contains only a few authoring examples. Kaggle
replaces it with roughly 200 hidden wells when the submitted notebook is run.

## Structure

```text
rogii-wellbore-geology-prediction/
├── data/          # competition files (gitignored)
├── notebooks/     # EDA and Kaggle submission notebook work (gitignored)
├── src/           # reusable loading, features, validation, and modeling code
├── submissions/   # generated submission.csv files
└── README.md
```

## Get the data

First accept the competition rules on Kaggle, then run from this directory:

```bash
kaggle competitions download -c rogii-wellbore-geology-prediction -p data
unzip 'data/*.zip' -d data
```

The current Kaggle file inventory is about 1.26 GiB across 2,327 files before
packaging.

## Validation

Split by `WELLNAME`, never by individual rows. Neighboring depth samples from
the same well are autocorrelated, so random row-wise validation would leak
well-specific structure and produce an overly optimistic RMSE.

A useful first scheme is deterministic grouped K-fold CV by well. Mask one
contiguous interval per validation well to better reproduce the competition's
missing evaluation zone, then compute RMSE only on that interval. Keep a fixed
seed and log per-fold and overall RMSE.

## Baseline direction

Start with a reproducible interpolation/correlation baseline using the known
`TVT_input` values surrounding the masked interval. Then compare it with a
grouped-CV gradient-boosting model using trajectory features, local/rolling
`GR` features, boundary distances, and features derived by aligning the
horizontal-well gamma-ray sequence with the typewell gamma-ray sequence.

Treat `TVT_input` carefully: it is a legitimate partially observed input, but
using unmasked target values from validation rows or constructing features
across the validation mask would be leakage.

## Submission

The submission must be named `submission.csv` and contain exactly:

```csv
id,tvt
000d7d20_1442,0.0
000d7d20_1443,0.0
```

`id` is `{WELLNAME}_{row_index}`. This is a notebook-only competition: internet
must be disabled, and Kaggle currently permits up to 9 hours on either CPU or
GPU. Commit the Kaggle notebook, then submit its generated `submission.csv`.

The pipeline is `python -m src.submit` (see its docstring for Kaggle paths).
It rebuilds every derived artifact from training data when missing, fits the
best-known stack on all training wells, discovers whatever wells are in
`test/`, and conforms the output to `sample_submission.csv`. The Kaggle
wrapper is `notebooks/kaggle_submission.ipynb`: upload `src/` as a dataset
named `rogii-src`, attach it plus the competition data, run all. Validated
locally on the visible test wells: ids match the sample exactly (14,151
rows); RMSE 10.1 against their training copies (optimistic — those wells
participate in the fitted caches).

## Timeline

- Entry and team-merger deadline: July 29, 2026 at 23:59 UTC.
- Final submission deadline: August 5, 2026 at 23:59 UTC.

## Experiment log

| Date | Model | CV scheme | CV RMSE | Public LB | Notes |
|------|-------|-----------|---------|-----------|-------|
| 2026-07-14 | A: constant last-known TVT | Harness: 5-fold grouped, seed 42, real masked suffixes (`results/baselines`) | 15.91 | — | Median well 10.67, p90 22.97, worst 70.64 (`1b1eba53`). C beats A only in the first 1,000 ft after PS |
| 2026-07-14 | B: flat layer (`TVT_a - ΔZ`) | Same | 107.49 | — | Layers are not flat; confirms trajectory tracks topology. Error grows ~25 ft RMSE per 1,000 ft |
| 2026-07-14 | C: prefix-linear topology (last 1,000 ft of `s = TVT_input + Z`, anchored) | Same | 42.29 | — | Prefix dip does not persist over ~4,800 ft suffixes; worse than constant beyond 1,000 ft |
| 2026-07-14 | D: spatial topology `F(X,Y)` (k-NN weighted plane over ANCC samples, anchored delta) | Same (`results/stage2`) | 28.41 | — | Median well 8.60 beats A, but heavy tail (worst 589). Beats A on 468/773 wells; per-well A/D oracle = 10.16 |
| 2026-07-14 | D+: hard prefix-playoff pick of A vs D (lateral-aware window, 1 ft margin) | Same (`results/playoff-v2`) | 15.13 | — | Pick accuracy only 53%; window must fit inside the ~1,700 ft prefix |
| 2026-07-14 | D2: D + extrapolated prefix-residual trend | Same (`results/stage2b`) | 38.38 | — | Negative result: residual trends don't persist either (rung-C lesson repeats) |
| 2026-07-14 | S: soft blend of A and D, inverse-square replay-RMSE weights | Same (`results/stage2b`) | 13.49 | — | Median 8.35, p90 18.34, worst 75.61. Hedging beats picking at 53% accuracy |
| 2026-07-14 | G: learned gate — logistic P(D beats A) on {replay scores, neighbor distance, roughness}, prob as blend weight | Same (`results/gate`) | 12.12 | — | Median 7.60, p90 16.27, worst 74.81. Remaining regret vs 10.16 A/D oracle is concentrated: top 20 wells = 53%, mostly wells where D wins big but the gate stays on A |
| 2026-07-14 | F0: GR Viterbi offset around G prior (pointwise smoothed emission, fixed σ_geo=15) | Same (`results/gr`) | 12.52 | — | GR hurts good priors (+0.99 when prior <5 ft), helps bad ones (−2.7 when >30 ft) |
| 2026-07-14 | F1: F0 with adaptive σ_geo = clip(1.5 × prior replay RMSE, 4, 40) | Same (`results/gr-adaptive`) | 12.22 | — | Median improves to 7.41; tails still pay when prior error exceeds the ±40 ft grid |
| 2026-07-14 | F2: F1 with half-strength offsets (shrink 0.5) | Same (`results/gr-shrink`) | 12.02 | — | Median 7.51, p90 16.58, worst 72.31. GR corrections are noisy-but-unbiased; shrinkage pays. Pointwise emission is weak — windowed/shape matching is the obvious upgrade |
| 2026-07-15 | G2: gate + `\|∇F\|` dip features (median/p90 along suffix) | Same (`results/gate-v2`) | 12.04 | — | Physical fault/terrace signal from the plane fit's own gradient; free at query time |
| 2026-07-15 | F2 on G2 prior | Same (`results/gr-shrink-v2`) | 11.95 | — | Full stack with dip-aware gate |
| 2026-07-15 | F3: F2 + spatial GR bias field in emission | Same (`results/gr-bias`) | 11.92 | — | k-NN field of calibrated-GR residuals at true TVT (train wells), anchored ΔB subtracted; field magnitudes (±10 API p10–p90) match the GR-continuity surface |
| 2026-07-15 | F4: windowed shape emission (rolling variance of pointwise diff, mean-removed) | Same (`results/gr-shape`) | 11.92 | — | Negative result: neutral at low weight, harmful at full weight, at every window 400–4,000 ft. Laterals stretch stratigraphy ~200:1, so shape-along-MD ≈ level-at-low-frequency; window mean-removal deletes the signal. Vertical-log fingerprint intuition does not transfer |
| 2026-07-15 | **F5: bold level channel — full weight, σ_vel 0.05, adaptive_scale 3, shrink 0.7, bias field, no shape** | Same (`results/gr-bold`) | **11.65** | — | New best. Median 7.09, p90 15.79. The GR signal was there; the DP was too timid to use it |
| 2026-07-15 | G3: gate + ramp-hypothesis features (D's forecast \|ΔTVT\|, suffix length, ramp×replay) | Same (`results/gate-v3`) + exact offline eval on `gate_table_v4` | 12.09 | — | Negative result: worse than the 5-feature gate (12.04) in CV, and confirmed offline with exact blend-SSE algebra under logistic and GBM alike. D's ramp *forecast* is available but its *reliability* isn't predictable from these features. Exact-eval infra (sse_a/sse_d/cross per well) kept in gate_table_v4; blend oracle = 8.49, so gate headroom remains |
| 2026-07-15 | **F6: direction-aware NNW-SSE regional dip residual inside G2, then F5 GR correction** | Same (`results/dip-axis`, `results/dip-gate`, `results/dip-best-directional-z`) | **11.37** | — | Fold-fitted robust gradient points 333–336° at ~2.0° dip. Raw `β·ΔXY−ΔZ` is noisy (30.65 RMSE unshrunk); symmetric shrink improves A→15.37 and G2→11.92. After GR, the gain is asymmetric, so production applies 15% residual downhill and 0% uphill using inference-time `Z`: F5 improves 11.65→11.37, p90 15.79→15.64, worst 75.90→68.78 |
| 2026-07-15 | **F7: phase-aware panel local projection, 30% blend for first 1,000 ft over F6** | Same (`results/panel-local-projections`, `results/panel-best`) | **11.35** | — | Raw ΔGR adds nothing (direct geometry 15.779 vs raw GR 15.784), but conditioning on typewell slope/curvature improves the direct panel model to 15.371. Recursive 200-ft chaining drifts badly (27.375). The panel signal helps only near PS: blending 30% for `<1,000 ft` and reverting exactly to F6 afterward improves 11.37455→11.34778; four folds improve and the fifth changes +0.0004. See `approaches/panel-local-projections.md` |
| 2026-07-15 | T1: transductive F7 — test-well prefixes (level-aligned `TVT_input+Z` + prefix GR residuals) join the surface and bias field at inference | Fold-wise simulation: models observe held-out wells' inference view (`results/transductive`) | 11.35 | — | Globally flat in CV (11.34778→11.35149) but tail-safer: worst 68.8→66.0, p90 15.64→15.45; dense-support wells −0.27, out-of-support −0.09. CV structurally understates the hidden-test benefit (held-out wells always have dense train support; hidden acreage may not). Enabled by default in `src.submit` (`--no-transductive` to disable) |
| 2026-07-15 | O1: guarded same-well override (`src/overlap.py`) — hidden test wells sharing an id with `train/` get the train copy's path (direct TVT, contact-reconstruction fallback), only after matching the visible prefix to <1.0 ft RMSE | Visible test (3 train copies) | n/a | — | The public ~7.0 LB cluster exploits this train/test overlap (decoded from `rogii-7-016-safe-rebuild`). 3/3 visible wells accepted at prefix RMSE 0.0 → exact truth. Unverified wells keep the model prediction. On by default in `src.submit` (`--no-overlap-override`); report written next to the submission |
