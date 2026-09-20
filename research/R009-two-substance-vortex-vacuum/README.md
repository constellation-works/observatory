---
id: R009
title: Two-substance vortex vacuum
status: done
tags: [physics, gravity, electromagnetism, vortex, legacy]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: [H007]
---

# R009 — Two-substance vortex vacuum

Origin:
[`_archive/lineage/nodes/two-substance-vortex-vacuum.md`](../../_archive/lineage/nodes/two-substance-vortex-vacuum.md).
Tests [`H007`](../../hypotheses/H007-the-two-substance-vacuum-yields-gravity-and-electromagnetism.md).
Theory: [`T008`](../../theories/T008-the-two-substance-vortex-vacuum.md).
Legacy record: four sims migrated together.

## Question

Does a two-substance vortex vacuum yield both a gravitational sector from a
source law in the packet Hamiltonian and the electromagnetic sign in 3-D? Either
failure is the kill condition.

## Method

- `code/two-substance-defect-gravity/` — a conserved two-substance defect lattice:
  stationary scarcity monopole, forced moving wake, independent void-volume
  variant.
- `code/two-substance-dynamical-packet/` — coupling controls, time-resolved
  profile lags, primary-observable refinement, an emission gate and a Hamiltonian
  audit (`RUN-2026-08-21.md`).
- `code/two-substance-packet-linear-symbol/` — independent Fourier-operator and
  time-evolution controls over the linearized packet symbol
  (`RUN-2026-09-05.md`).
- `code/two-substance-vortex-lattice/` — a 2-D conserved-density lattice: sign,
  force law, short-range correction and the neutral balanced state.

Each run's numbers are in its `assets/results.json`. No external input.

## Result

The packet sector holds: both propagating branches classify as longitudinal sound
and transverse current, and the coupling controls distinguish the families the
claim needs. The gravitational sector does not come out of the source law as
proposed — the defect-gravity lattice is a `refutes` assessment at `strong`. The
log on `H007` therefore disagrees with itself and the hypothesis is
`inconclusive`.

## Limitations

The vortex lattice is 2-D, so the electromagnetic sign in 3-D — half the kill
condition — is untouched by it. principia's family is `exploratory` with 8
supported against 6 refuted claims, and the two declared kill conditions are
tracked there, not here.

## Next

The 3-D sign, or a source law that yields the gravitational sector without the
wake `T005` refuted. Either is a new R item.
