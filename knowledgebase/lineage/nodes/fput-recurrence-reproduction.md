---
id: fput-recurrence-reproduction
title: FPUT recurrence reproduction
domain: physics
status: testing
created: 2026-09-12
updated: 2026-09-12
kill: An independent Störmer–Verlet reconstruction of LA-1940 Fig. 1 (N=32, α=1/4, δt²=1/8) does not show the first mode-1 recurrence within ±1000 cycles of the digitized figure, or returns less than 94% of the initial mode-1 energy at that recurrence.
tags:
- paper-reproduction
evidence:
- id: ev1
  verdict: inconclusive
  strength: strong
  source: knowledgebase/studies/physics/fput-recurrence-reproduction.md
  date: 2026-09-12
  note: M1=28400 cycles and M2=0.977753 passed, but C3 dt/2 recurrence movement=0.0510563 exceeded 0.01; M3 and M4 also failed. Protocol v1 was not changed.
  origin:
    task: ORB-12360
- id: ev2
  verdict: inconclusive
  strength: strong
  source: studies/physics/fput-recurrence-reproduction.md
  date: 2026-09-12
  note: 'Canonical study locator for the protocol-v1 result: M1/M2 passed, while C3 movement 0.0510563 exceeded 0.01 and M3/M4 failed. ev1 retains the repository-root spelling in this append-only corpus.'
  origin:
    task: ORB-12360
- id: ev3
  verdict: inconclusive
  strength: strong
  source: ../../studies/physics/fput-recurrence-reproduction.md
  date: 2026-09-12
  note: Canonical relative source for the protocol-v1 study. Earlier ev1/ev2 preserve two non-resolving locator spellings created from contradictory repository examples; this append-only corpus does not expose evidence deletion.
  origin:
    task: ORB-12360
tasks:
- id: ORB-12360
  state: done
  why: run frozen protocol v1 baseline, numerical controls, and figure comparison
origin:
  task: ORB-12359
  run: jrun-20260912-2042-c3
---


