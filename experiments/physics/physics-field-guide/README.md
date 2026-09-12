# Physics field guide

Domain: `physics` · Node: `neb show physics-field-guide` · Started: 2026-09-12

## Question

Can a small set of interactive chapters make established dynamical systems
experimentable while matching an independent Python reference at predefined
validation points?

## Kill condition

Any chapter's in-browser numerics differ from the independent Python reference
by more than the chapter's declared tolerance at its predefined validation
points.

## Chapter choices

### 1. Orbits and numerical error

The Kepler problem will compare explicit Euler, semi-implicit Euler, leapfrog,
and RK4 (the shared `_lib/web/integrators.js` already provides three of these
integrators; the remaining method can be added in the chapter apparatus).
Controls are initial speed, step size, and integrator. The analytic validation
references are the Kepler ellipse, the conserved specific energy
`E = v²/2 - μ/r`, and conserved angular momentum `L = r × v`. Validation
points will check position and these invariants against `reference.py`.

### 2. Waves, interference and boundaries

This chapter uses the linear N-mass chain, α=0 in the same FPUT model as the
reproduction, so the later reproduction integrator can be reused with
consistent units. Controls are wavelength/mode number, the phase between two
counter-propagating pulses, and fixed versus free boundary. Analytic
validation references are the dispersion relation
`ω_k = 2 sin(πk/2N)`, standing-wave superposition, and the sign reversal of a
reflection at a fixed end.

### 3. Resonance and damping

This chapter extends the established-physics `pendulum-driven` starter with a
driven damped oscillator. Controls are drive frequency, damping, and drive
amplitude. Analytic validation references are the steady-state amplitude and
phase response, the quality factor `Q`, and the transient envelope. The
reference implementation will make both the resonant peak and the approach
to steady state explicit.

## Apparatus boundary

No existing orrery simulation is adopted as a chapter: those sims test
speculative personal theories and are not the neutral teaching apparatus
needed here. `pendulum-driven` is the only established-physics starter and is
being extended for the resonance chapter. The remaining chapters use the
Kepler and linear-chain models specified above, with independent analytic and
Python validation.

The browser-facing schema, accessibility requirements, validation contract,
and export boundary are defined in
[`docs/design/paper-reproduction-workbench.md`](../../../docs/design/paper-reproduction-workbench.md).

## Run

```sh
uv run python experiments/physics/physics-field-guide/run.py
```

## Result

The chapter implementations and `reference.py` validation harness are
scheduled for later milestones; this milestone records the choices only.
