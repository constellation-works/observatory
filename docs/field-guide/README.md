# Physics field guide

Reference material, not a research record: the chapters teach established
physics and are held to an independent Python reference. Started 2026-09-12.
Origin node: [`_archive/lineage/nodes/physics-field-guide.md`](../../_archive/lineage/nodes/physics-field-guide.md).
The validation record is [`VALIDATION.md`](VALIDATION.md).

## Question

Can a small set of interactive chapters make established dynamical systems
experimentable while matching an independent Python reference at predefined
validation points?

## The bar

A chapter fails if its in-browser numerics differ from the independent Python reference
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
[`docs/design/paper-reproduction-workbench.md`](../design/paper-reproduction-workbench.md).

## Run

```sh
make serve   # then open /docs/field-guide/<chapter>/index.html
./_scripts/export-field-guide.sh   # shareable tree at output/field-guide-export/
```

## Chapters

| # | chapter | state |
|---|---|---|
| 1 | [`orbits-numerical-error/`](orbits-numerical-error/) | built — the exemplar for the shared chapter apparatus |
| 2 | [`waves-boundaries/`](waves-boundaries/) | built |
| 3 | [`resonance-damping/`](resonance-damping/) | built |

The shared apparatus the chapters reuse (`_lib/web/plot.js`, `chapter.js`,
`chapter.css`, and the `chapter.json` / `reference.py` / `validation.json`
contract) is documented in
[`_lib/README.md`](../../_lib/README.md).

## Result

Chapter 1 is built and validated: its browser numerics agree with the
independent Python reference at all sixteen predefined validation points
(worst relative difference 0, declared tolerance 1e-9 relative), and the
convergence table recovers the order of every integrator.

Chapter 2 is built and validated: its browser numerics agree with the
independent Python reference at all twelve predefined validation points
(worst relative difference on the order of 1e-15, declared tolerance 1e-9
relative), the measured standing-wave periods agree with the analytic
dispersion relation to well under the declared 1%, the two-pulse
superposition maximum matches the linear sum of the two pulses run
separately, the reflection sign matches the fixed/free prediction, and the
convergence entry recovers Stormer-Verlet's second order. Chapter 3 is built and validated on the same terms: its six predefined
(omega, zeta) cases agree between `resonance.js` and `reference.py`, and it
reuses the apparatus unchanged.
