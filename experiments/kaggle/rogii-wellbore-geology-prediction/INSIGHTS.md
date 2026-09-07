# Modeling insights

See [the data dictionary](data/README.md) for column definitions and coordinate
conventions.

## The well trajectory encodes geological information

After a directional well lands in its lateral section, its upward or downward
pitch appears to be chosen to follow the expected dip of the target layers. The
trajectory is therefore more than a geometric input: it may contain geological
knowledge introduced by the well plan and subsequent steering decisions.

An upward-moving lateral does not necessarily move toward a shallower
geological position. If the rock layers rise at approximately the same rate,
the well can rise in physical `Z` while staying at nearly constant `TVT`.

### Case study: well `0a57a29c`

From the point where the well becomes horizontal to its final row:

| Measurement | Landing (`MD=11,384`) | End (`MD=17,905`) | Change |
| --- | ---: | ---: | ---: |
| `Z` | -9,155.98 ft | -8,964.38 ft | +191.60 ft |
| `TVT` | 11,185.75 ft | 11,210.09 ft | +24.34 ft |
| `ANCC` surface `Z` | -8,732.73 ft | -8,516.79 ft | +215.94 ft |

All six supplied formation surfaces (`ANCC`, `ASTNU`, `ASTNL`, `EGFDU`,
`EGFDL`, and `BUDA`) rise by the same 215.94 ft over this interval. These are
not six independent topology signals: within a well they are vertically
shifted copies of one shared surface shape. Meanwhile, the borehole rises by
191.60 ft. The borehole therefore moves only 24.34 ft deeper relative to that
shared geological topology:

```text
change in TVT ≈ change in formation-surface Z - change in well Z
              ≈ 215.94 - 191.60
              ≈ 24.34 ft
```

The sign matters because `Z` uses a negative-depth convention: increasing `Z`
means moving upward.

Over roughly 6,521 ft of lateral:

- The borehole pitches upward by approximately 1.7 degrees.
- The geological surfaces rise by approximately 1.9 degrees.
- The correlation between well `Z` and the shared formation-surface topology is
  about 0.9989.
- `TVT` remains within a range of only 24.34 ft after landing.

If the borehole had risen by exactly the same 215.94 ft as the surfaces, its
TVT would have remained constant. Because it rose slightly less, it gradually
moved deeper in geological coordinates.

### Modeling implications

1. **Use the trajectory as a geological prior.** Derive per-row and rolling
   features such as `dX/dMD`, `dY/dMD`, `dZ/dMD`, horizontal displacement,
   inclination, azimuth, curvature, and distance from the landing or Prediction
   Start point.
2. **Benchmark a constant-TVT lateral.** Predicting the last observed
   `TVT_input` throughout the masked suffix is a physically meaningful baseline
   when the well is being steered to remain in one narrow stratigraphic zone.
3. **Benchmark local trend extrapolation.** Estimate the recent pre-PS
   `dTVT/dMD` and test whether a constrained continuation improves on the
   constant baseline.
4. **Learn a trajectory correction.** A model can start from the geometric
   contribution of `dZ` and use trajectory, spatial, and GR-alignment features
   to estimate the unknown lateral layer movement.
5. **Represent the six surfaces as topology plus offsets.** For lateral dip and
   shape, any available surface supplies effectively the same signal. Their
   vertical separations may still encode well-level stratigraphic spacing, so a
   compact representation is one topology curve plus five relative offsets
   rather than six collinear curves.
6. **Use formation surfaces only for training analysis or auxiliary
   supervision.** They make this relationship visible, but they are absent from
   test and cannot be required by the inference pipeline.

### Caveats and validation

Across all 773 training wells, the separation between any of the other five
surfaces and `ANCC` changes by no more than 0.01 ft within a well. Their
row-to-row slopes also agree within 0.01 ft, confirming that the differences
are rounding rather than independent topology. The vertical offsets vary
between wells, however, so they can still describe well-level formation
spacing.

The case study demonstrates a strong association, not proof of the drilling
intent or data-generation process. The trajectory and shared topology may have
been planned from common geological information or produced by related
processing. Its usefulness should be evaluated with grouped-by-well
validation.

When simulating a validation Prediction Start, mask `TVT_input` before deriving
features. Compare the constant-TVT, local-trend, trajectory-only, GR-alignment,
and combined approaches using RMSE on the complete masked suffix.

## Where the model still fails: ramp wells (2026-07-15)

Error analysis of the best stack (`results/gr-bold`, 11.65 global RMSE)
shows the residual error is not diffuse — it is concentrated in one well
type:

- **90 of 773 wells have |net suffix ΔTVT| > 30 ft ("ramp wells") and carry
  44% of the total squared error.** The top 5% of wells carry 45%.
- Suffix TVT range is the strongest per-well error predictor
  (Spearman +0.42); its top quartile scores 17.8 RMSE vs 7.3–9.4 for the
  rest.
- These are **smooth, sustained ramps, not faults**: max TVT move within any
  50 ft of lateral is typically 3–9 ft on the worst wells; only 2 of the
  top 20 exceed 10 ft.
- The trajectory does not announce the ramp: corr(|net ΔZ|, |net ΔTVT|) is
  0.07 across wells. The layer moves under a comparatively straight well —
  the well *leaves its zone* stratigraphically.
- On 38 of the 90 ramp wells, the raw spatial model D already beats the
  full gated stack; substituting D on just those wells would take the
  global RMSE from 11.65 to ~10.2. The gate hedges toward constant-TVT
  because none of its features (short replay, support distance, dip)
  distinguish a flat suffix from a ramp suffix.
- GR often cannot rescue these wells: several worst ramp wells are missing
  60–80% of suffix GR.

Implication: the cheapest large gain is gate features that see the *ramp
hypothesis* itself — D's own predicted |net ΔTVT| over the suffix (A's is
zero by construction), suffix length, and their interaction with replay
quality. If D predicts a large ramp and validates on the prefix, believe D.

## Regional dip-axis residual (2026-07-15)

The physical uphill/downhill split is predominantly one regional dip axis:
uphill laterals head north/northwest and downhill laterals head south/southeast.
A robust within-well fit on training-fold `ANCC` changes learns approximately

```text
expected Δsurface = -0.015 × ΔX + 0.032 × ΔY
expected ΔTVT     = expected Δsurface - ΔZ
```

Across the five grouped folds the up-dip bearing is 333–336 degrees and the
dip is approximately 2.0 degrees. This is stable, but the unshrunk regional
plane is not locally accurate enough: using the full expected mismatch scores
30.65 RMSE. Shrinking the residual to 10–15% improves constant-TVT from 15.91
to about 15.4 without assuming the global plane is the local surface.

The production implementation (`RegionalDipPrior` and `DipAxisGate`) fits the
axis on training wells only, anchors at the last known `TVT_input`, and applies
the shrunken residual only to the safe component of the A/D gate. The existing
GR state-space model then estimates its remaining offset. Symmetric 10%
residual shrink improves the geometric gate from 12.04 to 11.92 RMSE.

After the GR update, however, the benefit is directional: downhill wells
improve while uphill wells are already best served by the original safe prior.
The final configuration therefore uses the observed suffix `ΔZ` (available at
inference) only to select strength: 15% of `β·ΔXY−ΔZ` downhill, 0% uphill. The
formation-motion estimate itself always comes from the fold-fitted regional
axis. This direction-aware stack improves F5 from 11.65 to 11.37 RMSE, with
downhill RMSE falling from 12.43 to 11.80 and uphill essentially unchanged at
11.04.

## Panel local projections and typewell phase (2026-07-15)

Treating wells as panels is useful when `MD` remains the ordered index and
signed `ΔX`, `ΔY`, and `ΔZ` are the regressors. Across lags 1–200 ft, the
grouped-fold coefficient curves are stable: `βX` stays near -0.014, `βY` near
+0.029, and `βZ` weakens only slightly from about -0.98 to -0.95. There is no
pooled oscillatory X/Y pattern; the curves recover the same regional dip axis.

Raw `ΔGR` has effectively no transferable coefficient. Interacting calibrated
`ΔGR` with the local typewell GR slope/curvature does add signal, however: a
direct phase-aware panel model scores 15.37 RMSE versus 15.78 for geometry and
15.78 for raw GR. This supports the conditional relationship
`ΔGR ≈ g′(TVT) × ΔTVT`, not an unconditional `ΔGR -> ΔTVT` mapping.

The local topology does not repeat at a clear short wavelength. After removing
the regional plane, RMS surface departure grows from 3.23 ft at 200 ft to
12.86 ft at 1,000 ft and 46.61 ft at 5,000 ft, while the mean signed departure
stays near zero. Chaining 200-ft projections therefore accumulates error and
scores 27.38 RMSE. Direct projections avoid much of the drift, but remain much
weaker than F6.

The transferable panel gain is short-range. A 30% direct-panel update over F6
for only the first 1,000 ft improves grouped CV from 11.37455 to 11.34778; after
1,000 ft the production wrapper returns exactly to F6. Full methodology and
ablations are in `approaches/panel-local-projections.md`.

## Undulation correlogram along the well path (2026-07-15)

Lag analysis of the detrended topology `r = (TVT + Z) − pooled dip plane`
across 120 sampled training wells (lags 25–5,000 ft along MD; pooled dip
refit independently at 1.99° toward 333°, matching F6). Chart data in
`outputs`-side `correlogram.json`; the analysis decomposes the undulation
budget into two parts:

- **Per-well tilt (local dip minus regional dip): ~17 ft std.** With only the
  pooled plane removed, the residual has σ = 19.6 ft and its correlogram
  crashes to ρ ≈ −1.6 at 5,000 ft — a diagnostic artifact of well-specific
  tilt, not oscillation. Adding a per-well linear detrend drops σ to 9.1 ft,
  so most of the "undulation" budget is actually *tilt* — consistent with the
  panel finding that RMS departure grows steadily with distance rather than
  repeating at a short wavelength.
- **True oscillation: σ ≈ 9.1 ft, half-wavelength ~2,500–3,000 ft.** The
  tilt-free correlogram decays through ρ = 0.56 at 500 ft, 0.25 at 1,000 ft,
  zero at ~1,500 ft, then goes *negative* and plateaus at ρ ≈ −0.44 from
  3,000 ft onward — a genuine hole effect. Hills become valleys at
  ~3,000 ft; ridge-to-ridge wavelength is roughly 6,000 ft.

Modeling consequences:

1. **Linear prefix extrapolation is exactly wrong past ~1,500 ft** (rung C's
   failure, restated spectrally): the correct continuation is mean-reverting —
   follow the local slope briefly, bend back to the (per-well tilt + regional
   dip) trend, mildly overshoot beyond ~3,000 ft.
2. **The prefix carries forecast value only ~1,000–1,500 ft into the suffix**
   (ρ < 0.5 beyond that after tilt removal). Everything farther must come from
   neighboring wells, where spatial ρ ≈ 0.9 at typical few-hundred-ft spacing.
3. **The intrinsic ceiling matches the oracle.** Kriging the oscillation with
   ρ ≈ 0.9 neighbors leaves conditional σ ≈ 19.6·√(1−0.81) ≈ 8.5 ft —
   numerically the same as the measured 8.49 A/D blend oracle. Two independent
   estimates of the field's predictability agree.
4. The natural successor prior is a GP/kriging model along the path:
   regional dip trend + per-well tilt term + oscillatory (hole-effect) kernel,
   conditioned jointly on the well's own prefix and neighboring wells' topology
   samples, feeding the same DP seat the gate output occupies today.

GR, given the same treatment (well-demeaned, smoothed), shows a variogram that
is still rising at 5,000 ft with no sill: lateral GR level is a long-range
regional field (consistent with the GR-continuity surface and the bias-field
finding), not local texture.
