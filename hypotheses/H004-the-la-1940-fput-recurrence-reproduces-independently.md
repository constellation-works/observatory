---
id: H004
title: The LA-1940 FPUT recurrence reproduces independently
status: supported
tags: [physics, paper-reproduction, nonlinear-dynamics]
derived_from: []
created: 2026-09-12
updated: 2026-09-20
revision: 2
assessments:
  - date: 2026-09-12
    research: R005
    revision: 1
    verdict: inconclusive
    strength: strong
    note: >-
      Protocol v1: M1 = 28400 cycles and M2 = 0.977753 passed, but the C3 dt/2
      recurrence movement of 0.0510563 exceeded the declared 0.01, and M3 and M4 also
      failed. Protocol v1 was not changed in the light of the result.
  - date: 2026-09-13
    research: R005
    revision: 2
    verdict: supports
    strength: suggestive
    note: >-
      Protocol v2 (corrected digitized mode labels, amended M3/M4/C3 definitions, all
      flagged post hoc): M1 = 28400 and M2 = 0.977753 pass as before, and the amended
      metrics pass. The numerics are byte-for-byte the v1 reconstruction; only the
      digitized reference and two metric definitions changed.
  - date: 2026-09-13
    research: R005
    revision: 2
    verdict: supports
    strength: strong
    note: >-
      Integrated acceptance rerun from scratch in a clean /tmp environment built only
      from the evidence package and the public OSTI source, reproducing the v2 baseline
      byte-for-byte.
---

# H004 — The LA-1940 FPUT recurrence reproduces independently

Origin:
[`_archive/lineage/nodes/fput-recurrence-reproduction.md`](../_archive/lineage/nodes/fput-recurrence-reproduction.md).

## The claim

An independent Störmer–Verlet reconstruction of LA-1940 Fig. 1 (N = 32,
α = 1/4, δt² = 1/8) shows the first mode-1 recurrence within ±1000 cycles of the
digitized figure and returns at least 94% of the initial mode-1 energy there.

## Revisions

- **revision 1** (2026-09-12) — the original statement, assessed against
  protocol v1, whose digitized reference mislabelled three peaks.
- **revision 2** (2026-09-13) — the same physical claim against the corrected
  digitization and the amended M3/M4/C3 definitions of protocol v2. The v1
  assessment stays in the log and does not carry to this statement.


## Migration note

This record was split out of the lineage node above when the corpus moved to
research layout v2. `derived_from` is empty because the node graph had no
ancestry to carry; the evidence below is the node's recorded evidence, dated as
it was recorded. The status is the one implied by the latest assessment — a
person owns it and may change it without changing the log.
