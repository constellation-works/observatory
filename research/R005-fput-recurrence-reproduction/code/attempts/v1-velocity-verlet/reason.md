# Protocol-v1 failed baseline

The frozen velocity-Verlet reconstruction completed, and M1, M2, C1 and C2
passed. Control C3 failed without a tolerance change: halving `delta t` while
holding physical duration fixed moved the recurrence by 0.0510563, above the
protocol limit of 0.01. M3 and M4 also missed their reference tolerances. The
matching `metrics.json` is retained here as the small, tracked summary; the
full regenerable run remains under the record's `output/` and is intentionally ignored.

**Superseded by protocol v2, reason: reference mislabel.** The M3/M4 misses
recorded here are largely artifacts of two things `protocol/v2.*` corrects,
not evidence against the reconstruction: (1) `reference/fig1-digitized.csv`
had three peaks assigned to the wrong mode numbers (see
`reference/README.md`'s changelog), so this run's M3 reference column points
at the wrong target for modes 2 and 4; and (2) v1's M3/M4 *definitions*
themselves were mis-specified (M3's "first local maximum" caught a sub-1%
early bump instead of the labelled peak; M4 summed modes 6-31 instead of
taking their individual maximum) — see `protocol/v2.json`'s `changelog` for
the dated, `post_hoc`-flagged amendments. C3's 5.1% dt/2 sensitivity is a
real finding, unaffected by the reference or metric-definition amendments;
v2 keeps its definition and 1% threshold but reports it rather than gating
execution status on it. This `v1-velocity-verlet` result is preserved
byte-for-byte as the historical record of the pre-repair, pre-amendment
comparison; it is not re-run or edited.
