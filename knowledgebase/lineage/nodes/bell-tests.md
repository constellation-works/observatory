---
id: bell-tests
title: Bell tests
domain: physics
status: refuted
created: 2026-09-07
updated: 2026-09-07
kill: CHSH |S| stays at or below the local bound 2 in the Monte Carlo
tags:
- orrery
evidence:
- id: ev1
  verdict: undermines
  strength: suggestive
  source: ../../../experiments/physics/bell-tests/pingpong-bell/
  date: 2026-09-07
  note: 'Analysis pipeline for the tabletop ping-pong Bell experiment: reads tally CSVs, computes correlations and the CHSH statistic. Polarity: a supported classical ceiling undermines this node''s claim that a local model reproduces quantum correlations (principia claim vortex-pingpong-classical-ceiling, supported)'
- id: ev2
  verdict: undermines
  strength: suggestive
  source: ../../../experiments/physics/bell-tests/vortex-bell/
  date: 2026-09-07
  note: 'CHSH test of the ''friction vortex'' local hidden-variable model: |S| saturates at exactly 2, the local bound, vs QM''s 2.83. Polarity: |S| pinned at the local bound is the kill condition firing (principia claim vortex-two-particle-bell, refuted; vortex-single-particle-spin stays supported and is not this node''s claim)'
---

## Where

- Sims: `experiments/physics/bell-tests/` (2): `pingpong-bell`, `vortex-bell`
- Family name in orrery's frozen catalog: `bell-tests`
