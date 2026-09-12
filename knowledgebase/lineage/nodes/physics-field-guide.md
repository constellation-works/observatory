---
id: physics-field-guide
title: Physics field guide
domain: physics
status: testing
created: 2026-09-12
updated: 2026-09-12
kill: Any chapter's in-browser numerics differ from the independent Python reference by more than the chapter's declared tolerance at its predefined validation points.
tags:
- field-guide
evidence:
- id: ev1
  verdict: supports
  strength: strong
  source: experiments/physics/physics-field-guide/waves-boundaries
  date: 2026-09-12
  note: 'Chapter 2 (waves-boundaries) built and validated: all 12 predefined validation cases agree between waves.js and reference.py (worst relative difference ~1e-15, tolerance 1e-9); standing-wave periods for k=1..8 agree with the analytic dispersion omega_k=2 sin(pi k/2N) to <=0.024% (tol 1%); the two-pulse crossing maximum matches the linear superposition of the two pulses run separately (phase 0 doubles, phase pi cancels to 0); reflection sign is -1 at a fixed end and +1 at a free end as predicted; the dt^2 convergence entry recovers Stormer-Verlet order 2.001. Kill condition not triggered.'
  origin:
    task: ORB-12363
- id: ev2
  verdict: supports
  strength: strong
  source: ../../../experiments/physics/physics-field-guide/waves-boundaries
  date: 2026-09-12
  note: 'Canonical relative source for ev1, using the corpus-relative locator convention (see fput-recurrence-reproduction ev3): the waves-boundaries chapter directory, from knowledgebase/lineage/nodes/. Same validation summary as ev1.'
  origin:
    task: ORB-12363
- id: ev3
  verdict: supports
  strength: strong
  source: experiments/physics/physics-field-guide/resonance-damping
  date: 2026-09-12
  note: 'Chapter 3 (resonance-damping) built and validated: all 6 predefined (omega, zeta) validation cases agree between resonance.js and reference.py (worst relative difference 0, declared tolerance 1e-9); RK4 steady-state amplitude/phase agree with the analytic response to <=1.5e-7 relative / <=6.1e-8 rad absolute (declared tolerance 0.5%% / 0.005 rad); the RK4 trajectory agrees with the closed-form underdamped transient to <=8.3e-9 absolute (declared tolerance 1e-6); the dt^4 convergence entry recovers RK4 order 4.035 (expected 4); omega_r = omega_0 sqrt(1-2 zeta^2) and Q = 1/(2 zeta) both match their analytic formulas exactly; phase crosses pi/2 exactly at omega = omega_0 for every zeta in the grid. make check passes (342 tests) and the Playwright browser_check.py passes all 28 checks (desktop + 375px layout, full keyboard operation including the pendulum toggle, no console errors, reduced-motion static path, SVG download). Kill condition not triggered.'
  origin:
    task: ORB-12364
origin:
  task: ORB-12359
  run: jrun-20260912-2042-c3
---


