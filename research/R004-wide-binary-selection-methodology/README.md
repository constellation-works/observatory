---
id: R004
title: Wide binary selection methodology
status: done
tags: [physics, gaia, wide-binaries, methodology]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: [H003]
---

# R004 — Wide binary selection methodology

Origin:
[`_archive/lineage/nodes/wide-binary-selection-methodology.md`](../../_archive/lineage/nodes/wide-binary-selection-methodology.md).
Tests [`H003`](../../hypotheses/H003-wide-binary-selection-manufactures-an-acceleration-artifact.md).
Legacy record: the preregistered run and its diagnosis, migrated together.

## Question

Do geometry and truncation in wide-binary selection manufacture an
acceleration-dependent artifact? The protocol's kill condition is that the
preregistered control shows no injected-effect power difference between selected
and unselected samples.

## Method

- `code/wide-binary-selection-bias/` — the frozen ORB-11221 protocol executed as
  a preregistered 12-arm Newtonian injection/recovery matrix against astrolabe's
  repaired spherical selector, with its binned scaled-velocity, shifted-field,
  comparator and sensitivity functions, and an independent Astropy candidate
  oracle as a regression control. The population is Newtonian by construction.
  The script refuses checkouts whose apparatus, protocol or gate hashes differ
  from the frozen inputs. 44 enumerated realizations (the protocol prose says 47;
  the discrepancy is recorded, not invented away).
- `code/wide-binary-control-diagnosis/` — diagnoses the four controls that failed,
  reanalysing that run without retuning the frozen protocol.

## Result

The primary comparison is not available: four controls failed. The diagnosis
locates the failures in the control apparatus and reports them rather than tuning
them away. Both sims are recorded as `inconclusive` on `H003`.

## Limitations

The nonuniform quality and density gradients are preregistered stress shapes, not
measured Gaia completeness laws. Exploratory sensitivity rows are excluded from
the frozen primary decision. Nothing here is an observational or nature-level
claim. The sims are the frozen record of their runs and are not edited in the
light of later work.

## Next

Repair the four controls in a new R item against the same frozen protocol. The
existing rows stay as they are.
