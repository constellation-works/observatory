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
