---
id: R002
title: Pendulum driven
status: done
tags: [physics, established-physics, apparatus]
derived_from: [Q001]
created: 2026-09-07
updated: 2026-09-20
tests: []
---

# R002 — Pendulum driven

Origin: [`_archive/lineage/nodes/pendulum-driven.md`](../../_archive/lineage/nodes/pendulum-driven.md),
a seed with no kill condition. Explores
[`Q001`](../../questions/Q001-where-does-the-driven-pendulum-go-chaotic.md).

## Question

What does the damped driven pendulum do across drive amplitude, drive frequency
and damping — and does the shared browser harness make that explorable?

## Method

`code/pendulum-driven/` is an interactive sim: RK4 over the pendulum equation
with live parameter sliders, built on `_lib/web/` (`loop.js`, `panel.js`,
`canvas2d.js`). Serve the repository root with `make serve`, then open
`/research/R002-pendulum-driven/code/pendulum-driven/index.html`.

## Result

The sim runs and is the harness's reference consumer — the
`resonance-damping` field-guide chapter extends it
([`docs/field-guide/resonance-damping/`](../../docs/field-guide/resonance-damping/)).
It settles nothing about the parameter space: no assessment is recorded from it,
because sweeping by hand is not a measurement.

## Limitations

Interactive exploration with no recorded sweep, no located bifurcations and no
declared tolerance. Nothing here is evidence for or against anything.

## Next

If `Q001` is to be answered, it needs a scripted sweep with stated precision on
the transitions — a new R item, not an edit to this one.
