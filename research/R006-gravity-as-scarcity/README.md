---
id: R006
title: Gravity as scarcity
status: abandoned
tags: [physics, gravity, scarcity, legacy]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: []
---

# R006 — Gravity as scarcity

Origin: [`_archive/lineage/nodes/gravity-as-scarcity.md`](../../_archive/lineage/nodes/gravity-as-scarcity.md).
Theory: [`T001`](../../theories/T001-gravity-as-the-gradient-of-scarce-space.md)
(superseded), with
[`T002`](../../theories/T002-moving-sources-in-the-closed-system.md),
[`T003`](../../theories/T003-ppn-reduction-of-the-settled-flow.md) and
[`T004`](../../theories/T004-shear-sourced-consumption.md).

**Legacy multi-sim record.** 24 sims spanning a retired research programme,
migrated together under `code/<sim>/` because splitting them into 24 R items
would manufacture 24 write-ups nobody wrote. New R items are one question, one
run; this one is history. `tests` is empty: the programme's claims live in the
principia lock, not as hypotheses in the live corpus.

## Question

Is gravity the gradient of a finite, locally consumed space budget? The node's
kill condition: a settled-flow reduction that cannot reproduce the PPN bounds, or
a source law that needs the retarded wake it forbids.

## Method

Twenty-four sims under `code/`, in four groups:

- **Counting and depletion lattices** — `dynamical-consumption-lattice`,
  `shear-consumption-lattice`, `lattice-two-source-superposition`,
  `lattice-photon-propagation`, `flowing-lattice-photon-propagation`,
  `level-coupled-shear-lattice`.
- **The level core** — `level-core-wind-tunnel`,
  `level-core-dynamical-relaxation`, `level-core-cavitation-threshold-map`,
  `level-core-far-field-slot-coefficients`, `level-core-two-core-superposition`,
  `moving-core-acoustic-rays`.
- **Algebraic and PPN checks** — `ppn-reduction-symbolic-checks` (exact SymPy
  gates), `frame-drag-swirl`, `frame-drag-swirl-lense-thirring-check`.
- **Confronting data and visualisation** — `sparc-scarcity-universality`,
  `scarcity-rotation-curve-fit`, `rotation-curve-distributed-mass`,
  `solar-system-nbody`, `scarcity-capped-cumulative-field`,
  `scarcity-field-slice-toggle`, `scarcity-grid-weight-black-hole`,
  `scarcity-shell-depletion-field`, `scarcity-star-well-headroom`.

The data-confronting sims read astrolabe's processed catalogues; see
`data/manifest.json`. Their built-in default paths still look for the retired
sibling `orrery`/`astrolabe` checkout layout and need `--data`.

## Result

The static sector produced supported results — the PG reduction, pure-wind
flatness, Schwarzschild diagonalization and the two-piece shift obstruction are
exact, and the far-field slot coefficients extend through r = 24. The programme
still failed where it had to succeed: across 149 SPARC galaxies `beta_i` tracks
disk scale (rho = 0.343, p = 1.86e-5), the per-galaxy model wins by 51,723 AIC
and the predeclared universality claim fails; the Sanders-form Yukawa fit's
scarcity-minus-Yukawa delta-AIC bootstrap interval crosses zero, so the Gaia band
is shape-degenerate; and the moving level core cavitates and violates the proposed
Bernoulli closure. The family was retired by decision on 2026-09-04.

## Limitations

The per-claim verdicts are principia's, in
[`_archive/principia/theory/gravity-as-scarcity/claims.json`](../../_archive/principia/theory/gravity-as-scarcity/claims.json)
and its evidence ledger; this README does not restate them and cannot overrule
them. Several sims are visualisations that settle nothing on their own
(`scarcity-field-slice-toggle` is cited by no claim). Retirement is a
research-allocation decision, not an impossibility proof: supported claims stay
supported and unresolved claims are not relabelled as disproven.

## Next

None. The programme is closed; the sims are kept because they are what stops the
ground being re-trodden.
