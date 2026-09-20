---
id: R008
title: Swirl photon
status: done
tags: [physics, electromagnetism, vortex, legacy]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: [H006]
---

# R008 — Swirl photon

Origin: [`_archive/lineage/nodes/swirl-photon.md`](../../_archive/lineage/nodes/swirl-photon.md).
Tests [`H006`](../../hypotheses/H006-swirl-modes-of-the-vortex-electron-are-photons.md).
Theory:
[`T007`](../../theories/T007-the-swirl-ball-electron-and-the-photon-correspondence.md).
Legacy record: three sims migrated together.

## Question

Is the swirl mode of the vortex electron the photon? The kill condition: a swirl
mode whose quanta are not photons, or a far field that does not match the
classical dipole.

## Method

- `code/oscillating-electron-retarded-fields/` — the computed field: a tight,
  smooth electron turn and its outward delayed response, drawn as dense
  stationary samples of the full retarded field, with a headless browser check
  and numerical reports under `assets/`.
- `code/swirl-ball/` — the swirl-ball picture of the electron, v6, with v3 and v5
  kept under `variants/`.
- `code/swirl-ball-far-field/` — the original illustrative animation: dense
  expanding rings and a tight turnaround.

Serve the repository root (`make serve`) to open any of them.

## Result

The far field matches the classical dipole and the retarded construction behaves
as the picture requires: three `supports` assessments on `H006`, the strongest
`strong`. principia's `swirl-photon` family is `resolved` with three of four
claims supported.

## Limitations

Visualisation and far-field agreement, not a quantisation argument: nothing here
derives photon statistics, which is the half of the kill condition that stays
untested. One claim in the family is refuted.

## Next

A quantisation argument, or an observable that separates this mode from the
classical dipole. Either is a new R item.
