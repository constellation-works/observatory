# Topology-first TVT reconstruction with GR measurement updates

**Status:** Proposed, not yet implemented or scored.

This approach derives the prediction from the geometry of a shared geological
surface. Gamma ray is used as a noisy observation that corrects the geometric
trajectory rather than as the sole source of alignment.

See also:

- [Data dictionary](../data/README.md)
- [Trajectory/topology insight](../INSIGHTS.md)

## Motivation from the downloaded data

The approach is based on the following empirical observations:

- Within every training well, `ANCC`, `ASTNU`, `ASTNL`, `EGFDU`, `EGFDL`, and
  `BUDA` are vertically shifted copies of one shared topology. Their pairwise
  separation varies by no more than 0.01 ft within a well.
- The masked suffix of a typical well spans thousands of horizontal feet but a
  narrow range of TVT. Median suffix values are approximately 4,832 ft of
  horizontal displacement and 26.37 ft of TVT range.
- A single typewell geology label dominates an average of 97.36% of each
  masked suffix. `EGFDL` is dominant for 653 of 773 training wells.
- Horizontal GR strongly resembles typewell GR when evaluated at the true TVT:
  global correlation is about 0.856 raw and 0.897 after modest smoothing.
- Raw per-foot `dGR` does not directly measure surface movement. Its
  correlation with formation-surface change is about 0.002, so local GR
  differences should not be treated as a topology derivative.
- Horizontal trajectories are almost straight in map view. Steering primarily
  changes inclination/`Z`, not horizontal azimuth.

These observations suggest a control-like process: the planned trajectory
contains a geological prior, and GR provides feedback about departures from
the desired stratigraphic position.

## Physical formulation

For horizontal-well row `t`, define:

- `u_t = TVT_t`: hidden geological position after Prediction Start.
- `z_t = Z_t`: observed physical vertical coordinate.
- `s_t`: the shared layer-topology coordinate at `(X_t, Y_t)`.

The observed relationship is:

```text
delta TVT = delta layer topology - delta Z
```

or:

```text
u_t - u_0 = (s_t - s_0) - (z_t - z_0)
```

Therefore:

```text
s_t = u_t + z_t + constant
```

The unknown constant is unimportant because predictions can be anchored at the
last known `TVT_input` row. Before Prediction Start, the relative topology is
directly observable as:

```text
s_known_t = TVT_input_t + Z_t
```

This turns the task into forecasting the continuation of a smooth spatial
surface, followed by a GR-based correction.

## Stage 1: validation harness and geometric baselines

Use the actual `TVT_input` mask supplied in every training well. For each fold,
hold out complete wells, fit all global components using only the remaining
wells, and score the held-out masked suffix against its training-only `TVT`.

Implement the following baselines in order.

### 1. Last-known TVT

Assume the planned trajectory perfectly follows one geological position:

```text
TVT_hat_t = TVT_input_at_PS_minus_1
```

This is the simplest expression of the narrow-target-zone hypothesis.

### 2. Flat layer

Assume layer topology is constant while the borehole changes `Z`:

```text
s_hat_t = s_anchor
TVT_hat_t = s_anchor - Z_t
```

where:

```text
s_anchor = last_TVT_input + Z_anchor
```

### 3. Local linear topology

After detecting the landed/lateral portion, fit a robust line to the last
500–1,000 known feet:

```text
s_known = alpha + beta * along_lateral_distance
```

Extrapolate the line after Prediction Start and recover TVT with:

```text
TVT_hat_t = s_hat_t - Z_t
```

Because a single well follows nearly one azimuth, this estimates only the
directional dip along that path. It does not identify independent `X` and `Y`
gradients.

### 4. Low-curvature topology

Permit slow changes in dip with a regularized quadratic or smoothing spline,
but constrain curvature tightly. Long-range unconstrained polynomial
extrapolation should be avoided.

The baseline comparison separates three hypotheses:

- Constant TVT: the borehole follows the layer.
- Constant topology: the layer is flat.
- Continued topology slope: the pre-PS geological dip persists.

## Stage 2: spatial topology from other wells

Learn a shared map `F(X, Y)` from the training wells. Only one formation
surface is required for topology; the remaining five are collinear copies with
different vertical offsets.

Candidate training targets are:

1. `ANCC`, with another surface used as fallback where `ANCC` is missing.
2. `TVT + Z`, which directly describes topology in the target coordinate but
   may contain a well-specific vertical offset.

Decimate each trajectory spatially before fitting. Millions of one-foot rows
provide little additional information for a smooth surface and would
overweight long wells.

Start with interpretable spatial estimators:

- Distance-weighted local plane fitted to nearby wells.
- Local polynomial regression.
- RBF or thin-plate spline.
- Local kriging if variogram behavior supports it.

For a held-out or test well, use only the predicted topology change and anchor
it to the known prefix:

```text
delta_F_t = F_hat(X_t, Y_t) - F_hat(X_anchor, Y_anchor)

TVT_geo_t = TVT_anchor + delta_F_t - (Z_t - Z_anchor)
```

Anchoring cancels much of the error in absolute surface depth. The quantity
that matters is the change in topology along the future trajectory.

Blend the global spatial slope with the locally observed pre-PS slope. The
blend weight should depend on distance to neighboring training wells and the
length/stability of the known lateral prefix.

### Leakage-safe spatial validation

When holding out a well, exclude all of its following information from the
spatial fit:

- Formation surfaces.
- Full `TVT`.
- Post-PS `TVT_input` reconstruction.
- Any spatial samples derived from those values.

Report both ordinary grouped-by-well CV and spatially blocked CV. A global
surface can interpolate nearby held-out wells well while failing on genuinely
new areas.

## Stage 3: calibrate the GR observation model

The typewell provides a reference curve:

```text
g_ref(u) = typewell GR at TVT u
```

The horizontal tool does not necessarily have identical amplitude, noise, or
resolution. Use the known prefix pairs `(TVT_input, horizontal_GR)` to calibrate
each well before matching:

1. Interpolate the typewell GR at every known `TVT_input`.
2. Fit a robust affine or quantile mapping between typewell and horizontal GR.
3. Estimate an appropriate smoothing/resolution kernel from the known prefix.
4. Retain an explicit horizontal-GR missingness mask.

Compare multi-scale windows rather than individual values. Candidate emission
features include:

- Robustly normalized GR levels.
- First and second differences.
- Rolling means, medians, and variances.
- Peak/trough locations and edge strength.
- Coarse and fine window representations.

The known prefix determines which transformations actually transfer between
the paired logs.

## Stage 4: constrained state-space inference

Treat TVT as a hidden state evolving along measured depth. The spatial model
produces a prior `TVT_geo_t`; GR produces a likelihood around that prior.

For each row, search only a bounded grid around the geometric prediction, for
example ±30–60 ft at the typewell sampling resolution. Use a dynamic program,
beam search, or particle filter with a cost of the form:

```text
cost_t(u_t) =
    lambda_gr   * GR_window_mismatch(u_t)
  + lambda_geo  * (u_t - TVT_geo_t)^2
  + lambda_vel  * (delta_u_t - delta_u_previous)^2
  + lambda_acc  * (delta2_u_t)^2
```

Important transition properties:

- TVT must be allowed to increase, decrease, or remain flat.
- Large instantaneous changes should be expensive unless the evidence supports
  a discontinuity.
- When horizontal GR is missing or uninformative, inference should revert
  toward the geometric prior.
- Repeated typewell GR patterns should produce low confidence rather than an
  arbitrary large alignment jump.

This differs from unconstrained correlation or ordinary monotonic DTW. The
geometry identifies a plausible neighborhood; GR chooses among nearby states.

### Confidence

Record the gap between the best and second-best path/window costs or the
entropy of the state distribution. Use low confidence to:

- Increase reliance on topology/trajectory.
- Reduce the size of GR-driven corrections.
- Flag wells and depth intervals for error analysis.

## Stage 5: physically structured combination

The final prediction should be expressed as a correction to the topology
model:

```text
TVT_final_t = TVT_geo_t + GR_state_correction_t
```

Avoid blending unrelated models without understanding their contributions.
The desired ablation ladder is:

| Run | Topology prior | GR correction | Purpose |
| --- | --- | --- | --- |
| A | Last-known TVT | None | Target-following baseline |
| B | Flat layer | None | Pure `Z` geometry |
| C | Prefix linear/curved | None | Local topology continuation |
| D | Cross-well spatial surface | None | Regional topology |
| E | Best geometric prior | Independent window correction | Tests the GR emission without path consistency |
| F | Best geometric prior | State-space update | Full proposed method |

Each addition must improve grouped CV and worst-well behavior, not merely the
public leaderboard.

## Evaluation diagnostics

The primary metric is global row-weighted RMSE over held-out masked suffixes.
Also report:

- Per-well RMSE distribution and worst wells.
- RMSE by distance after Prediction Start.
- RMSE by horizontal-GR missing fraction.
- RMSE by spatial distance to the nearest training well.
- RMSE by suffix TVT range and amount of trajectory rise/fall.
- Error in predicted `delta TVT`, not only absolute TVT.
- GR correction magnitude and confidence.

Use the three visible test wells only to verify the inference and submission
pipeline. Kaggle identifies them as training examples, so they are not a valid
holdout.

## Expected failure modes

- Repeated or nearly flat typewell GR patterns create ambiguous alignments.
- Long missing horizontal-GR intervals remove the observation update.
- Faults or abrupt topology changes violate smooth-surface assumptions.
- A held-out/test well may lie outside the spatial support of training wells.
- Prefix-only topology extrapolation may drift over a long suffix.
- The target interval differs across wells; no universal GR range should be
  assumed.
- Surface columns are training-only and must never be required at inference.

## Suggested implementation layout

```text
src/
├── data.py             # Paired well/typewell loading and masks
├── geometry.py         # MD, inclination, azimuth, landing, path distance
├── topology.py         # Prefix and cross-well surface estimators
├── gr_reference.py     # Resampling, calibration, window features
├── state_space.py      # Constrained TVT inference
├── validate.py         # Leakage-safe grouped/spatial CV and diagnostics
└── submit.py           # Hidden-test discovery and submission generation
```

Keep random seeds and fold definitions fixed, save fold-level predictions, and
log every ablation in the competition README.
