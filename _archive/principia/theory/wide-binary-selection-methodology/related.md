## Related

- [studies/gaia-wide-binaries-low-acceleration](../../studies/gaia-wide-binaries-low-acceleration.md)
  — the parent footprint (ORB-10753) this protocol audits. That note's own "what this does and
  does not constrain" section already flags the sample as pipeline-validated but not decisive;
  this family is the calibration check that section calls for.
- **Astrolabe ORB-11217** (landed at astrolabe commit `90f5b58`) — made candidate-pair
  generation complete on the sphere and fixed the shifted-field secondary-catalog semantics.
  That was a completeness *bug fix*; this family's hypothesis is about the surviving
  *intentional* selection design (the cuts as specified) plus forward-model assumptions, not a
  reopening of the bug. The independent-oracle claim here (`wbsel-candidate-oracle-regression`)
  re-verifies that fix as a control, deliberately kept separate from the bias-statistic verdict.
- [wide-binary-selection-bias](../../../orrery/lab/sims/wide-binary-selection-bias/) — ORB-11222's
  frozen synthetic run at Orrery `28dd5c72bb670517b93b556f1d2483402c8e8655`: candidate oracle
  passes, but sanity/calibration/power controls fail, so the methodological verdict remains
  unresolved and ORB-11241 owns repair.
- Boufourou 2026 (arXiv:2608.24556) — the literature precedent that estimator/selection
  artifacts, not new physics, can manufacture a pseudo-signal in exactly this class of test (the
  eccentricity-triple coupling mechanism there is different from the geometry/truncation
  mechanism tested here; see the study note's references section for the distinction).
- No `theory/gravity-as-scarcity` or `theory/two-substance-vortex-vacuum` claim depends on this
  family. This is deliberate: the family exists so a methodology question about an external
  apparatus (Astrolabe) does not need to borrow or perturb either theory's live front.
