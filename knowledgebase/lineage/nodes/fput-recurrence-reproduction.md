---
id: fput-recurrence-reproduction
title: FPUT recurrence reproduction
domain: physics
status: supported
created: 2026-09-12
updated: 2026-09-13
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
- id: ev4
  verdict: supports
  strength: suggestive
  source: knowledgebase/studies/physics/fput-recurrence-reproduction.md
  date: 2026-09-12
  note: 'Protocol v2 (corrected mode labels + amended M3/M4/C3 definitions, post_hoc-flagged): M1=28400 and M2=0.977753 pass as before. M3 now passes on all three gated modes using global maxima against the corrected reference (mode2 14100/0.882 vs 14000/0.883, mode3 9250/0.712 vs 9400/0.700, mode4 6550/0.454 vs 6500/0.450). M4 passes per-mode (0.063170 <= 0.066667); summed value 0.084518 still reported. C3 still fails its own 1% threshold (0.0510563 dt/2 shift) but is now a reported sensitivity check, not gating. Execution status flips from v1''s ''failed control'' to v2''s ''completed''; scientific assessment flips from inconclusive to supports. Shaky: C3''s sensitivity is real and unresolved; mode 3''s second maximum (~19k) rests on the softest digitized reading.'
  origin:
    task: ORB-12375
- id: ev5
  verdict: supports
  strength: suggestive
  source: knowledgebase/studies/physics/fput-recurrence-reproduction.md
  date: 2026-09-12
  note: 'Milestone 3 workbench: the protocol-v2 baseline reproduces byte-for-byte (metrics.json 1570191f…, energies.csv c145ec40…, figure.png 4614da6d…) from a fresh /tmp environment pinned to NumPy 2.5.3 / Matplotlib 3.11.1 following the exported REPRODUCE.md, and every digitized feature residual sits inside the stated +/-250 cycle / +/-5 unit digitization uncertainty (largest: -200 cycles for the mode-1 recurrence, +3.68 units for mode 3''s first maximum) when the reconstruction is drawn on the original figure''s own axes geometry. Bounded exploration: dt=0.125 (the naive caption reading) spans only 3750 model-time units in 30,000 cycles versus 10,606.6 at dt=1/sqrt(8), so the recurrence near model time 10,041 falls outside the figure''s abscissa entirely and C3 passes vacuously with movement 0.0 at the window edge; alpha=1.0 keeps a recurrence at 28,400 cycles but returns only 77.0% of E1(0) with the per-mode higher-mode ceiling rising from 0.063 to 0.611 of E1(0) (qualitative only, no Fig. 2 digitization exists). Shaky: the orbit-research record chain is partial (program, claim, two input artifacts) because the executor worktree mounts .git read-only, so the registered protocol, run receipts and assessment land with tools/record_chain.py after delivery; the C3 5.1% dt/2 sensitivity at the baseline is unchanged and unresolved.'
  origin:
    task: ORB-12361
- id: ev6
  verdict: supports
  strength: strong
  source: ../../studies/physics/fput-recurrence-reproduction.md
  date: 2026-09-13
  note: 'Milestone 6 integrated acceptance, rerun from scratch: a /tmp environment built only from the evidence package and the public OSTI source (PDF verified at 1,570,076 bytes / sha256 3155813b..., fresh uv venv pinned to numpy 2.5.3 + matplotlib 3.11.1, clean clone at the run''s own git_revision) reproduces the registered protocol-v2 baseline byte-for-byte: metrics.json 1570191f...e86721, energies.csv c145ec40...f270c4ee, figure.png 4614da6d...56f2d768, the same digests the baseline artifact records register. Measured: M1 28,400 cycles (ref 28,600, tol 1,000), M2 0.9777532985498025 (ref 0.9666666666666667, tol 0.03), M3 mode2 14,100/0.8817707004889854, mode3 9,250/0.7122695735332155, mode4 6,550/0.45443492092262405 (all within 5% time / 0.10 height), M4 0.06316980197954705 (tol 0.0666666667) -- all pass; C1 0.00030083236612377107 and C2 0.002015601922728094 pass; C3 0.05105633802816894 still fails its own 1% threshold as a reported, non-gating sensitivity check. The two exploratory runs (alpha=1.0, dt=0.125) leave the baseline directory''s recursive digest 43acc0c3... unchanged and an out-of-range alpha=5.0 is refused with exit 2. Study page clean at 1280 and 375 px with every metrics and residual row equal to metrics.json (40/40 checks); export --check verified 28/28 members with 0 absolute paths; the now-complete 11-record chain validates (orbit-research validate: valid, 0 errors) with 2 documented pending claim->program references. Shaky: C3''s 5.1% dt/2 sensitivity is unchanged and unresolved; the digitized reference and the inferred integrator ordering remain the limits of the comparison.'
  origin:
    task: ORB-12365
tasks:
- id: ORB-12360
  state: done
  why: run frozen protocol v1 baseline, numerical controls, and figure comparison
- id: ORB-12375
  state: done
  why: correct digitized mode labels and amend protocol to v2, re-run baseline
- id: ORB-12361
  state: open
  why: 'workbench slice: study page, bounded exploratory runs, scientific records and the verified evidence package'
origin:
  task: ORB-12359
  run: jrun-20260912-2042-c3
---


