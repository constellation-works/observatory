---
title: "Wide-binary selection methodology: does geometry/truncation manufacture an acceleration-dependent artifact?"
status: exploratory
families: [wide-binary-selection-methodology]
almanac: "orbit:ORB-11221 (task-originated; no almanac discussion thread)"
created: 2026-09-05
updated: 2026-09-05
---

# Wide-binary selection methodology

**The idea.** [gaia-wide-binaries-low-acceleration](../../studies/gaia-wide-binaries-low-acceleration.md)
put Astrolabe's predeclared wide-binary pipeline against real Gaia DR3 data and found no
low-acceleration excess on a 25° cone (n = 156 pairs). That pipeline applies sky geometry,
brightness truncation, an escape-speed proper-motion gate, and a shifted-field chance-alignment
estimator before binning the scaled velocity statistic ṽ against internal Newtonian
acceleration g_N. This doc is **not** a claim that the pipeline is wrong, and not a new
gravity theory — it is a dedicated **methodological control family** asking a narrower
question: can geometry/truncation cuts interacting with a nonuniform sky population, or a
miscalibrated chance-alignment estimator, manufacture a spurious acceleration-dependent offset
in an otherwise purely Newtonian synthetic catalog run through the *real* pipeline? Candidate
pair-completeness defects in that pipeline are a separate, already-closed question (Astrolabe
ORB-11217, landed at astrolabe commit `90f5b58`) — this family is about the surviving
*intentional* selection design (the cuts as specified), chance contamination, and forward-model
assumptions, not about a completeness bug.

The full preregistered protocol — hypothesis, null, decision rule, controls, run matrix, and
the cross-repo contract for the Orrery follow-on experiment — is
[studies/wide-binary-selection-bias-preregistration](../../studies/wide-binary-selection-bias-preregistration.md).
This hub carries only the claim registry; the study note is the protocol itself and is where
the falsifiable content lives.

**Status.** The protocol remains frozen. ORB-11222 ran its cataloged synthetic fixture at
merged Orrery commit `28dd5c72bb670517b93b556f1d2483402c8e8655`
([wide-binary-selection-bias](../../../orrery/lab/sims/wide-binary-selection-bias/)). Its
candidate oracle passes all 44 enumerated realizations, but R0 sanity, cap isolation, shifted
field calibration, and positive-control power fail under the predeclared rule; the overall
verdict is therefore **unresolved**, not a result about gravity or the astronomical anomaly.
[gates/wide-binary-selection-bias-control](../../gates/wide-binary-selection-bias-control.json)
remains the live front, with repair task ORB-11241 diagnosing the frozen-control failures.

## Contents

- [evidence-ledger.md](evidence-ledger.md) — claim-by-claim outcomes, including unresolved
  controls and the independently supported candidate-oracle regression.
- [related.md](related.md) — links to the parent Gaia footprint, ORB-11217, and the literature
  precedent for estimator-forensics in this exact test.
- [open-questions.md](open-questions.md) — what the pilot needs to settle before promotion.
