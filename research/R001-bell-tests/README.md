---
id: R001
title: Bell tests
status: done
tags: [physics, quantum, bell, legacy]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: [H001]
---

# R001 — Bell tests

Origin: [`_archive/lineage/nodes/bell-tests.md`](../../_archive/lineage/nodes/bell-tests.md).
Tests [`H001`](../../hypotheses/H001-local-vortex-hidden-variables-reach-the-quantum-chsh-bound.md).
Legacy record: two sims migrated together from orrery's `bell-tests` family.

## Question

Can a local hidden-variable model of the friction-vortex kind reach the quantum
CHSH value, or does it stop at the classical bound |S| = 2?

## Method

- `code/vortex-bell/` — Monte Carlo CHSH test of the friction-vortex model
  (`vortex_bell.py`), with a corkscrew variant and a tilt enumeration over the
  measurement-angle space.
- `code/pingpong-bell/` — the analysis pipeline for the tabletop ping-pong
  experiment: reads tally CSVs, computes correlations and the CHSH statistic.
  `sample-tally.csv` is a committed worked example.

No external input; every draw is seeded in code.

## Result

|S| saturates at exactly 2, the local bound, against quantum mechanics' 2√2 ≈
2.83. The tabletop pipeline finds correlations under the same classical ceiling.
Both are recorded as `refutes` assessments on `H001`, which is `refuted`.

## Limitations

The Monte Carlo explores the model's own parameterisation, not every conceivable
local model, and the tabletop tally is a worked example rather than a completed
experiment. The single-particle spin result in principia's `vortex-electron`
family stays supported and is a different claim
([`T009`](../../theories/T009-the-vortex-electron-vs-bell.md)).

## Next

None. The kill condition fired and principia's family is refuted.
