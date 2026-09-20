---
id: T009
title: The vortex electron vs Bell
status: refuted
tags: [physics, quantum, bell, vortex]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
claims: [H001]
supersedes: []
---

# T009 — The vortex electron vs Bell

The lock this record points at is
[`_archive/principia/theory/vortex-electron/`](../_archive/principia/theory/vortex-electron/): its `README.md`,
`claims.json` (4 claims: 2 supported, 2 refuted) and `evidence-ledger.md` are the authority for every
claim below and are not restated here. principia's own document status is
`refuted`; this record carries the layout-v2 status `refuted`.

## What it said

Local hidden variables in the vortex-electron picture reproduce quantum
correlations, up to and including a CHSH violation.

## Why it is refuted

|S| saturates at exactly the local bound of 2
([`H001`](../hypotheses/H001-local-vortex-hidden-variables-reach-the-quantum-chsh-bound.md),
[`R001`](../research/R001-bell-tests/)). The single-particle spin claim stays
supported inside the lock; the two-particle claim is refuted, which is the claim
the family was for.

## Migration note

One theory record per principia family, created when the corpus moved to research
layout v2. The lock moved byte-for-byte to `_archive/principia/` and is read-only:
nothing here changes a claim it owns. If a claim needs restating, it is restated
as a hypothesis in the live corpus and the lock is left as history
(`_archive/principia/policy.md`). Its checker still runs, as `make check-archive`.
