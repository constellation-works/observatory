---
id: physics-field-guide
title: Physics field guide
status: hypothesis
created: 2026-09-12
updated: 2026-09-13
kill: Any chapter's in-browser numerics differ from the independent Python reference by more than the chapter's declared tolerance at its predefined validation points.
tags:
- field-guide
- physics
references:
- id: r1
  kind: other
  uri: ../../../experiments/physics/physics-field-guide/waves-boundaries
  title: 'Chapter 2 (waves-boundaries) built and validated: all 12 predefined validation cases agree between waves.js and reference.py (worst relative difference ~1e-15, tolerance 1e-9); standing-wave periods for k=1..8 agree with the analytic dispersion omega_k=2 sin(pi k/2N) to <=0.024% (tol 1%); the two-pulse crossing maximum matches the linear superposition of the two pulses run separately (phase 0 doubles, phase pi cancels to 0); reflection sign is -1 at a fixed end and +1 at a free end as predicted; the dt^2 convergence entry recovers Stormer-Verlet order 2.001. Kill condition not triggered.'
  note: '[supports/strong] Chapter 2 (waves-boundaries) built and validated: all 12 predefined validation cases agree between waves.js and reference.py (worst relative difference ~1e-15, tolerance 1e-9); standing-wave periods for k=1..8 agree with the analytic dispersion omega_k=2 sin(pi k/2N) to <=0.024% (tol 1%); the two-pulse crossing maximum matches the linear superposition of the two pulses run separately (phase 0 doubles, phase pi cancels to 0); reflection sign is -1 at a fixed end and +1 at a free end as predicted; the dt^2 convergence entry recovers Stormer-Verlet order 2.001. Kill condition not triggered.'
  added: 2026-09-12
  origin:
    task: ORB-12363
- id: r2
  kind: other
  uri: ../../../experiments/physics/physics-field-guide/waves-boundaries
  title: 'Canonical relative source for ev1, using the corpus-relative locator convention (see fput-recurrence-reproduction ev3): the waves-boundaries chapter directory, from knowledgebase/lineage/nodes/. Same validation summary as ev1.'
  note: '[supports/strong] Canonical relative source for ev1, using the corpus-relative locator convention (see fput-recurrence-reproduction ev3): the waves-boundaries chapter directory, from knowledgebase/lineage/nodes/. Same validation summary as ev1.'
  added: 2026-09-12
  origin:
    task: ORB-12363
- id: r3
  kind: other
  uri: ../../../experiments/physics/physics-field-guide/resonance-damping
  title: 'Chapter 3 (resonance-damping) built and validated: all 6 predefined (omega, zeta) validation cases agree between resonance.js and reference.py (worst relative difference 0, declared tolerance 1e-9); RK4 steady-state amplitude/phase agree with the analytic response to <=1.5e-7 relative / <=6.1e-8 rad absolute (declared tolerance 0.5%% / 0.005 rad); the RK4 trajectory agrees with the closed-form underdamped transient to <=8.3e-9 absolute (declared tolerance 1e-6); the dt^4 convergence entry recovers RK4 order 4.035 (expected 4); omega_r = omega_0 sqrt(1-2 zeta^2) and Q = 1/(2 zeta) both match their analytic formulas exactly; phase crosses pi/2 exactly at omega = omega_0 for every zeta in the grid. make check passes (342 tests) and the Playwright browser_check.py passes all 28 checks (desktop + 375px layout, full keyboard operation including the pendulum toggle, no console errors, reduced-motion static path, SVG download). Kill condition not triggered.'
  note: '[supports/strong] Chapter 3 (resonance-damping) built and validated: all 6 predefined (omega, zeta) validation cases agree between resonance.js and reference.py (worst relative difference 0, declared tolerance 1e-9); RK4 steady-state amplitude/phase agree with the analytic response to <=1.5e-7 relative / <=6.1e-8 rad absolute (declared tolerance 0.5%% / 0.005 rad); the RK4 trajectory agrees with the closed-form underdamped transient to <=8.3e-9 absolute (declared tolerance 1e-6); the dt^4 convergence entry recovers RK4 order 4.035 (expected 4); omega_r = omega_0 sqrt(1-2 zeta^2) and Q = 1/(2 zeta) both match their analytic formulas exactly; phase crosses pi/2 exactly at omega = omega_0 for every zeta in the grid. make check passes (342 tests) and the Playwright browser_check.py passes all 28 checks (desktop + 375px layout, full keyboard operation including the pendulum toggle, no console errors, reduced-motion static path, SVG download). Kill condition not triggered.'
  added: 2026-09-12
  origin:
    task: ORB-12364
- id: r4
  kind: other
  uri: ../../studies/physics/physics-field-guide.md
  title: 'Milestone 6 integrated acceptance across all three chapters, rerun rather than inherited. Kill condition (browser numerics differing from the independent Python reference beyond the declared tolerance) not triggered: orbits-numerical-error 16 cases, waves-boundaries 12, resonance-damping 6, worst relative difference 0 at the declared 1e-9 tolerance in each, recomputed independently through each chapter''s own runCase and compared in Python as well as by the page. Each chapter''s tests/browser_check.py passes at 1280 and 375 px (28/28, 28/28, 29/29) and a separate acceptance pass written for this milestone passes 150/150: no console or page errors, every labelled control reachable by Tab with arrow keys changing the value and the plotted numbers, every preset applying its declared values, pause/single-step/reset, prefers-reduced-motion completing the static path with Play and Single step disabled and the same observable reported, and the on-page validation table equal to validation.json. Two defects found and fixed here: window.__chapter.runCase accepted out-of-range parameters and returned NaNs (now refused by checkParameters with a message naming the control, value and declared range), and two log-range presets landed on the nearest slider notch (zeta 0.0199526 and 1.20226 instead of the declared 0.02 and 1.2; applyPreset now applies the declared value exactly). make check green: 344 passed, 5 skipped, neb check 0 errors. Shaky: the 1e-9 agreement bounds transcription error between two implementations of the same algorithm, not modelling error; the physics tolerances (dispersion, steady-state, transient, convergence order) are the looser separate checks, and the pendulum toggle has no analytic reference.'
  note: '[supports/strong] Milestone 6 integrated acceptance across all three chapters, rerun rather than inherited. Kill condition (browser numerics differing from the independent Python reference beyond the declared tolerance) not triggered: orbits-numerical-error 16 cases, waves-boundaries 12, resonance-damping 6, worst relative difference 0 at the declared 1e-9 tolerance in each, recomputed independently through each chapter''s own runCase and compared in Python as well as by the page. Each chapter''s tests/browser_check.py passes at 1280 and 375 px (28/28, 28/28, 29/29) and a separate acceptance pass written for this milestone passes 150/150: no console or page errors, every labelled control reachable by Tab with arrow keys changing the value and the plotted numbers, every preset applying its declared values, pause/single-step/reset, prefers-reduced-motion completing the static path with Play and Single step disabled and the same observable reported, and the on-page validation table equal to validation.json. Two defects found and fixed here: window.__chapter.runCase accepted out-of-range parameters and returned NaNs (now refused by checkParameters with a message naming the control, value and declared range), and two log-range presets landed on the nearest slider notch (zeta 0.0199526 and 1.20226 instead of the declared 0.02 and 1.2; applyPreset now applies the declared value exactly). make check green: 344 passed, 5 skipped, neb check 0 errors. Shaky: the 1e-9 agreement bounds transcription error between two implementations of the same algorithm, not modelling error; the physics tolerances (dispersion, steady-state, transient, convergence order) are the looser separate checks, and the pendulum toggle has no analytic reference.'
  added: 2026-09-13
  origin:
    task: ORB-12365
origin:
  task: ORB-12359
  run: jrun-20260912-2042-c3
---


