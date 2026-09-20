# Panel local projections over the well trajectory

## Question

Can the wells be treated as panels, with signed spatial movement replacing
time, so lag-dependent regressions recover the formation's up/down motion?
Can the horizontal/typewell GR relationship improve those regressions once the
current layer state is represented?

The experiment is implemented in `src/panel.py` and run with:

```bash
python -m src.panel --run panel-local-projections
```

All reported prediction scores use the existing deterministic five-fold split
grouped by well (seed 42) and the real masked suffixes.

## Formulation

The panel identifier is the well and the ordered index is measured depth
(`MD`), not `X` or `Y`. Coordinates are continuous signed covariates:

```text
ΔhTVT(i,t)
  = βX(h) ΔhX(i,t)
  + βY(h) ΔhY(i,t)
  + βZ(h) ΔhZ(i,t)
  + θ(h) GR_context(i,t,h)
  + error(i,t,h)
```

There is one ridge regression for each horizon `h=1..200 ft`. Coefficients are
smoothed across adjacent horizons with a deterministic Savitzky-Golay filter.
Training windows for these short-horizon models come only from the observed
pre-Prediction-Start lateral.

The physical identity remains:

```text
surface elevation S = TVT + Z
ΔTVT = ΔS - ΔZ
```

Consequently, a vertical coefficient close to `-1` is physically sensible;
the unknown part is whether the surface followed the well's horizontal move.

## GR and latent layer state

Raw `ΔGR` cannot be added directly to `ΔTVT`: their units differ and the sign
of the relationship reverses across typewell GR peaks and troughs. Each well's
horizontal GR is first robustly calibrated to its typewell using only its
known prefix. The phase-aware model adds:

- local typewell GR slope, curvature, and roughness at the anchor TVT;
- interactions of those descriptors with `ΔX`, `ΔY`, and `ΔZ`;
- regularized inverse-slope terms
  `ΔGR × g′ / (g′² + λ)` for `λ = 1, 4, 16`;
- short internal GR-gap interpolation, while long gaps produce no GR update.

These are test-available latent layer descriptors. The training-only
`Geology` strings are deliberately not used.

## Two forecast modes

### Recursive 200-ft projections

The first version chains the 1–200 ft models across the complete suffix. It is
faithful to a short-lag panel interpretation, but every block makes the next
block's predicted TVT its new typewell-phase anchor.

### Direct distance-dependent projections

The second version avoids recursion. For every training well, the actual last
known TVT is the single anchor, and models are fitted directly at horizons
1–200, then 250, 300, 400, 500, 600, 750, 1,000, 1,250, 1,500, 2,000, 2,500,
3,000, 4,000, 5,000, 6,000, and 8,000 ft. Coefficients are interpolated between
these horizons. Training targets come only from wells in the training fold.

## Results

| Model | Grouped-CV RMSE | Median well | p90 well | Worst well |
| --- | ---: | ---: | ---: | ---: |
| Recursive geometry | 29.2777 | 15.8806 | 44.3858 | 133.0517 |
| Recursive raw GR | 29.2798 | 15.8868 | 44.3727 | 133.0066 |
| Recursive phase-aware GR, strongest shrink | 27.3753 | 14.9059 | 41.0100 | 125.5485 |
| Direct geometry | 15.7794 | 10.4748 | 22.3474 | 70.1353 |
| Direct raw GR | 15.7840 | 10.4272 | 22.2665 | 70.0490 |
| **Direct phase-aware GR** | **15.3707** | **10.0180** | **22.1789** | **71.1600** |
| Constant TVT | 15.9099 | 10.6651 | 22.9725 | 70.6394 |
| Previous production F6 | 11.3746 | 7.0847 | 15.6431 | 68.7818 |

Raw `ΔGR` is neutral to slightly harmful. Conditioning it on typewell phase is
real signal: the direct phase model beats direct geometry on 467 of 773 wells
and improves global RMSE by 0.4087 ft. It also beats constant TVT by 0.5391 ft.
The gain is concentrated in the first 3,000 ft; beyond roughly 4,000 ft the
phase update becomes harmful.

The recursive version fails because small local movement errors accumulate.
Its RMSE by distance is 6.90, 15.56, 24.10, 31.48, and 38.20 ft in the first
five 1,000-ft buckets. The direct formulation removes most of that drift.

## What the coefficient curves show

Across `h=1..200`, the geometry coefficients are stable rather than
oscillatory:

```text
βX: -0.0141 -> -0.0137 ft/ft
βY: +0.0303 -> +0.0289 ft/ft
βZ: -0.9833 -> -0.9493 ft/ft
```

This recovers the previously identified NNW-SSE dip axis. There is no pooled
periodic up/down pattern in `βX(h)` or `βY(h)`. The local departures cancel in
the mean but grow strongly in magnitude. After removing the fitted regional
plane, RMS residual surface change is:

| Spatial lag | RMS residual surface change |
| ---: | ---: |
| 50 ft | 0.94 ft |
| 200 ft | 3.23 ft |
| 1,000 ft | 12.86 ft |
| 2,000 ft | 22.74 ft |
| 5,000 ft | 46.61 ft |

The mean signed residual stays near zero. In other words, the formation has
large balanced local rises and falls, but a single global lag coefficient
cannot say which one a new well will encounter.

## Pipeline decision

A fixed blend of the direct panel model throughout the suffix worsens F6. The
phase signal is nevertheless consistently useful in the first 1,000 ft. A
30% panel / 70% F6 blend there, followed by unchanged F6 afterward, scores:

```text
F6:                 11.3745517 RMSE
F6 + early panel:   11.3477769 RMSE
```

Four folds improve and the fifth changes by only +0.0004 RMSE. The production
wrapper `EarlyPanelBlend` therefore confines the new signal to that validated
short-range regime. This is F7; it does not replace the topology/GR state-space
model at long range.

## Artifacts

- `results/panel-local-projections/coefficients.csv`
- `results/panel-local-projections/residual_scale.csv`
- `results/panel-local-projections/per_well.csv`
- `results/panel-local-projections/coefficient-curves.png`
- `results/panel-local-projections/residual-scale-and-cv.png`
- `results/panel-best/per_well.csv`

