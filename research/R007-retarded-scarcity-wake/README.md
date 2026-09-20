---
id: R007
title: Retarded scarcity wake
status: done
tags: [physics, gravity, scarcity]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: [H005]
---

# R007 — Retarded scarcity wake

Origin:
[`_archive/lineage/nodes/retarded-scarcity-wake.md`](../../_archive/lineage/nodes/retarded-scarcity-wake.md).
Tests [`H005`](../../hypotheses/H005-the-retarded-scarcity-wake-is-a-viable-source-law.md).
Theories: [`T005`](../../theories/T005-the-retarded-scarcity-wake.md),
[`T006`](../../theories/T006-moving-source-field-consistency.md).

## Question

Can the delayed-center shortcut serve as the source law for a moving mass's
scarcity wake? The kill condition: it fails as a Poisson-vacuum field, or the
explicit boost-violating equation dissipates.

## Method

- `code/delayed-center-analytic-checks/` — deterministic quadrature,
  finite-difference, loop-work and contrast ladders over the shortcut, with the
  run recorded in `RUN-2026-09-04.md` and `assets/results.json`.
- `code/retarded-scarcity-wake/` — an interactive negative control that shows the
  refuted shortcut and the supercritical regime it would need.

No external input.

## Result

Both halves of the kill condition fire. The ladders catalogue why the shortcut is
non-Laplacian, and the regime where it could work is observationally inaccessible.
`H005` is `refuted`; principia records the family as refuted and keeps the
surviving constraints as `moving-source-field-consistency`.

## Limitations

The checks are analytic ladders over one proposed shortcut, not a proof that no
retarded construction can work — which is exactly what `T006` exists to bound.
The interactive sim is a visualisation of a known-negative result.

## Next

None here. Branch C in `T006` is where anything further would start.
