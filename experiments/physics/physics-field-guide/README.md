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
make serve   # then open /experiments/physics/physics-field-guide/<chapter>/index.html
```

## Chapters

| # | chapter | state |
|---|---|---|
| 1 | [`orbits-numerical-error/`](orbits-numerical-error/) | built — the exemplar for the shared chapter apparatus |
| 2 | waves, interference and boundaries | planned |
| 3 | resonance and damping | planned |

The shared apparatus the chapters reuse (`_lib/web/plot.js`, `chapter.js`,
`chapter.css`, and the `chapter.json` / `reference.py` / `validation.json`
contract) is documented in
[`experiments/physics/_lib/README.md`](../_lib/README.md).

## Result

Chapter 1 is built and validated: its browser numerics agree with the
independent Python reference at all sixteen predefined validation points
(worst relative difference 0, declared tolerance 1e-9 relative), and the
convergence table recovers the order of every integrator. Chapters 2 and 3
are scheduled for a later milestone and reuse the apparatus unchanged.
