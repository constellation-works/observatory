---
title: "The retarded-scarcity wake: moving gravity through a substrate"
status: exploratory
families: [retarded-scarcity-wake]
almanac: 15-discussions/26-08/from-galactic-motion-to-the-moving-gravity-medium-problem.md
created: 2026-08-07
updated: 2026-08-08
---

# The retarded-scarcity wake

**The idea (Daniel, 2026-08-07).** If gravity is a field carried by a physical substrate
with its own state of motion, a galaxy moving relative to that substrate should not be
assumed to carry an exactly spherical, instantaneously recentered potential. The galaxy's
dense center is the dominant coherent source; field information reaching its sparse
outskirts originated when that center was behind its current position. On the simplest
retarded-position rule, the dynamical center therefore lags the matter-density center,
making the scarcity potential greater on the leading edge and the gravitational attraction
stronger on the trailing edge. A sufficiently fast source may form a wake or cone if it
outruns disturbances supported by the substrate.

**Current analytic verdict (revised 2026-08-08): the Branch A shortcut fails under its stated
Poisson-vacuum interpretation; the fork survives only as an explicit substrate equation.** The
leading/trailing effect follows from the delayed-center rule below; it does **not** follow from
finite propagation speed or the word "medium" alone. [Moving-source field
consistency](../moving-source-field-consistency/) shows that \(\Phi_{\rm lag}\) is not the
source-free exterior solution of the standard Poisson equation for a compact galaxy and that its
alternative retarded-direction force is non-conservative. This does not exclude every local
substrate theory: a different operator or physical distributed response could reproduce similar
phenomenology, but must be specified as new Branch C dynamics. In a specified boost-invariant
control, the first-order lag cancels for uniform motion. Under Principia's evidence contract,
these analytic claims remain `untested` until the negative-control calculations are cataloged in
Orrery.

The doc-level status stays `exploratory` rather than `refuted`: Branch C is unadjudicated. What
died is the claim that the delayed-center mechanic is the ordinary compact-source field with a
propagation delay added. See the successor for the reordered program: a specified calibration
control, a derived Branch C amplitude law, and observational baseline work that does not yet claim
to bound every wake model.

## Contents

- [Evidence ledger](evidence-ledger.md)
- [Related](related.md)
- [Open questions](open-questions.md)


## Relationship to gravity as scarcity

This is a successor question, not an extension of the parent's empirical verdict.
[Gravity as scarcity](../gravity-as-scarcity/) supplies two pieces of mathematical language:

1. a stored scalar whose gradient acts as acceleration; and
2. the possibility that local field generation depends on available headroom.

It does **not** supply the moving-medium dynamics proposed here. In particular, this branch
does not reopen the fixed-β universality law refuted across SPARC galaxies, the static
photon sector refuted by light propagation, or the free-fall source law absent from the
counting mechanic. The new independent quantity is the source velocity relative to a
candidate substrate, and the new signature is angular: a dipole aligned with that velocity.
An axisymmetric rotation-curve boost and a directional wake are different observables.

## Minimal wake model

### 1. Variables and rest state

Let the substrate have a local velocity **U**, gravitational disturbance speed \(c_g\), and
stored scarcity scalar \(S(\mathbf{x},t)\). Let the galaxy's baryonic center move at velocity
**V**, so its substrate-relative velocity is

\[
\mathbf{w}=\mathbf{V}-\mathbf{U}, \qquad \beta_g=|\mathbf{w}|/c_g.
\]

The CMB frame is not assumed to equal **U**. It is only one measured reference frame that a
later observational analysis may test as a control.

Use conventional gravitational potential \(\Phi<0\) for sign calculations, with
\(\mathbf{a}=-\nabla\Phi\). A scarcity coordinate can be defined by adding a constant so it
starts at zero in the deepest region and rises outward. That shift changes no force. Thus
"greater potential" means numerically less negative \(\Phi\), not stronger gravity.

### 2. The delayed-center postulate

The narrow hypothesis to test first is:

> At radius \(R\), the outer field is centered on the source position one propagation time
> earlier, rather than on a velocity-corrected steady solution.

For a centrally dominated source moving uniformly, the retarded displacement is

\[
\boldsymbol{\Delta}(R)\simeq-\mathbf{w}\,\frac{R}{c_g}.
\]

The toy potential outside the dominant source is therefore

\[
\Phi_{\rm lag}(\mathbf{r})=-\frac{GM}{|\mathbf{r}-\boldsymbol{\Delta}|}.
\]

This is a postulate, not yet a derived Green-function solution. Its virtue is that it states
Daniel's moving-field intuition without laundering it into standard relativity.

### 3. Leading/trailing sign

Choose \(+y\) along **w** and let \(\theta\) be measured from the leading direction. For
\(\beta_g\ll1\), \(|\boldsymbol{\Delta}|\simeq\beta_gR\), giving

\[
\Phi_{\rm lag}(R,\theta)
\simeq-\frac{GM}{R}
+\frac{GM}{R}\,\beta_g\cos\theta+O(\beta_g^2).
\]

At the leading edge, \(\theta=0\):

\[
\Phi_{\rm lead}\simeq-\frac{GM}{R}(1-\beta_g),
\qquad
g_{\rm lead}\simeq g_0(1-\beta_g).
\]

At the trailing edge, \(\theta=\pi\):

\[
\Phi_{\rm trail}\simeq-\frac{GM}{R}(1+\beta_g),
\qquad
g_{\rm trail}\simeq g_0(1+\beta_g).
\]

So the leading potential is greater (less negative), while the trailing gravitational field
is stronger. To first order, the edge-to-edge contrasts are

\[
\Phi_{\rm lead}-\Phi_{\rm trail}\simeq2\frac{GM}{R}\beta_g,
\qquad
\frac{g_{\rm trail}-g_{\rm lead}}{g_0}\simeq2\beta_g.
\]

**Corrected 2026-08-07.** This section previously gave \(4\beta_g\) for the acceleration
contrast. That coefficient does not come from \(\mathbf{a}=-\nabla\Phi\) applied to the
\(\Phi_{\rm lag}\) above; it comes from a *different* rule — a point mass at fixed separation
\(R(1+\beta_g)\), giving \(g_0/(1+\beta_g)^2\simeq g_0(1-2\beta_g)\). The two rules are not the
same object and are not both derivable from the postulate as stated. The gradient rule gives
\(2\beta_g\) and is the one this section's declared \(\mathbf{a}=-\nabla\Phi\) requires; the
alternative rule is separately non-conservative. See
[moving-source-field-consistency](../moving-source-field-consistency/) § Two rules.

These coefficients belong to the delayed point-center approximation. They are recorded here for
provenance only: the successor rejects the postulate as the compact-source exterior solution of
the standard Poisson equation. Specified boost-invariant controls such as electromagnetism and
general relativity cancel the naïve first-order lag; an alternative substrate equation must state
its own dynamics and coupling.

## Density dependence

For an extended galaxy with density \(\rho(\mathbf{x})\), every mass element contributes on
its own delay and distance. The qualitative hypothesis is that central concentration makes
the wake coherent: much of the outer potential refers to nearly the same dense region and
therefore nearly the same retarded displacement. A diffuse outer disk contributes more local
field with shorter delays and partially recenters the potential.

That suggests a dimensionless concentration response \(C\), to be measured rather than
chosen:

\[
A_1(R)=C[\rho;R]\,\beta_g+O(\beta_g^2),
\]

where \(A_1\) is the normalized \(m=1\) coefficient of the potential around a ring. The
point-center limit predicts \(C\to1\) for the potential coefficient above. The theory does
not yet predict \(C\) for a bulge+disk mass profile. If concentration fails to control
\(A_1\) in the apparatus, this density-based part of the idea is wrong even if some wake
survives.

## Competing substrate branches

The first apparatus must compare mechanisms, not merely render the favored picture.
**Narrowed analytically on 2026-08-08** — the Poisson-vacuum reading of A is dead; B is a known
calibration only after its boost-invariant equation is specified; C remains open; D is excluded
for conventionally coupled gravity modes but not automatically for every hypothetical substrate
mode. Retained below as the original statement of the fork, with each disposition noted.

### Branch A — delayed-center memory — **analytically rejected; fixture pending**

The postulate above: the field points toward a retarded matter configuration without a
velocity term that recenters the steady solution. Prediction: an \(O(\beta_g)\) dipole,
dynamical-center lag, leading/trailing asymmetry, and possible momentum transfer to the
substrate.

*Analytic disposition:* rejected as the source-free exterior solution of the standard Poisson
equation for a compact galaxy. Under that diagnostic it requires an effective dipolar density
\(\propto\cos\theta/R^3\) filling space, with a linearly divergent dipole moment. A different
operator or a physical substrate response is not excluded, but would constitute a new model with
new conservation and source obligations. See
[moving-source-field-consistency](../moving-source-field-consistency/).

### Branch B — causal steady field — **specified control required**

A hyperbolic substrate equation evolves a field sourced by the moving density and is allowed
to reach steady state in the galaxy's comoving coordinates. Prediction to adjudicate: the
first-order dipole may cancel, leaving a fore-aft-symmetric deformation beginning at
\(O(\beta_g^2)\). If so, finite propagation is real but the delayed-center postulate is
refuted.

*Disposition:* electromagnetism and general relativity provide known boost-invariant controls in
which velocity-dependent terms remove the naïve first-order lag. Branch B becomes a calibration
target only after the control equation, source coupling, frame, and tracer observable are fixed. A
generic causal hyperbolic substrate is not settled by naming those precedents.

### Branch C — emergent metric — **the surviving branch**

Matter and measuring devices are excitations of the same substrate, so uniform motion is
hidden at leading order. The candidate rest frame is then observable only through
microstructure-scale dispersion or other Lorentz-breaking corrections. Existing bounds are
carried by [lorentz-violation-bounds](../../studies/lorentz-violation-bounds.md). This branch may
erase the proposed galactic wake altogether.

*Disposition:* untouched by the analytic pass, and now the whole of the live question. Note the
change in epistemic status it forces: with A dead, a wake requires *explicit* boost-violation, so
its amplitude is a free parameter **bounded** by Lorentz tests rather than **predicted** by
retardation. The branch is worth pursuing only if some breaking parameter yields an \(A_1\) the
existing bounds do not already crush.

### Branch D — supercritical wake — **ordinary gravity excluded**

If \(|\mathbf{w}|>c_g\), disturbances cannot propagate ahead of the source and a Mach-like
cone may form. This is the closest branch to the electron-cone intuition in the Almanac
discussion, but it is conditional and presently only a conjecture. If \(c_g\) is identified
with the observed tensor gravitational-wave speed, massive planets and galaxies cannot
enter this branch; any additional slower substrate mode must be specified and confronted
with [scalar-gravity-ppn-constraints](../../studies/scalar-gravity-ppn-constraints.md).

*Disposition:* for a conventionally coupled gravitational mode, the escape hatch is closed.
Moore & Nelson 2001 give a conservative Cherenkov speed-deficit bound of \(2\times10^{-15}\) for
Galactic cosmic-ray origins and ~\(2\times10^{-19}\) for extragalactic origins (`conjecture — to
verify` pending the moving-source study note). Either keeps a galaxy moving at \(10^{-3}c\) far
below the mode speed. Extending that conclusion to an extra substrate mode requires its coupling
to matter and its dispersion to be specified.

## Observable signatures

The model's clean signatures are directional. In the galaxy frame, the substrate wind fixes
an axis even while stars orbit:

- an \(m=1\) component of \(\Phi(R,\theta)\) proportional to \(\cos\theta\);
- a dynamical center displaced behind the baryonic density peak;
- stronger inward acceleration and altered orbital speed on the trailing side;
- weaker attraction on the leading side;
- secular torque, heating, or drag if the substrate absorbs momentum;
- a correlation of the asymmetry axis with the galaxy's velocity relative to one common
  inferred frame, rather than with its disk scale alone. **Degenerate — see below.**

> **Amended 2026-08-08.** The last bullet requires a cosmological-simulation baseline. Peculiar
> velocity and environment share causes, but the leading tidal tensor is quadrupolar and does not
> by itself predict an \(m=1\) phase alignment; the null correlation must be measured rather than
> assumed. The fifth bullet is also compromised under one reading of the mechanic: loop-dependent
> work can arise as an artifact of the non-conservative force rule, independent of any substrate
> momentum exchange. A candidate geometric signature keyed to the angle between **w** and the disk
> normal is proposed, but its vertical response is parameter-dependent and not yet derived, in
> [moving-source-field-consistency](../moving-source-field-consistency/).

This is not yet an explanation of flat rotation curves. An axisymmetric dark-matter-like
signal is \(m=0\); this proposal is primarily \(m=1\). Any claim that orbital averaging turns
the dipole into a radial boost must be derived and tested separately.

## Future Orrery apparatus

> **Superseded 2026-08-08.** The staged program below did not sufficiently distinguish the
> Poisson-vacuum shortcut, a specified boost-invariant control, and a genuinely boost-violating
> substrate equation. The replacement program — a negative-control fixture, an explicit
> calibration equation, a derived Branch C amplitude law, and observational baseline work — is in
> [moving-source-field-consistency](../moving-source-field-consistency/) § Proposed program.
> Two specification gaps found there apply to any successor apparatus: tracer studies need the
> velocity-coupling (gravitomagnetic-analogue) sector specified or they measure the chosen frame,
> and they must seed eccentric as well as circular orbits or they cannot see non-conservation.
> This section is retained for provenance.

No apparatus is authorized or implemented by this document. When the theory is promoted to
an experiment, the first Faraday task should build a cataloged Orrery sim with frozen rules
and the following stages.

### Stage 1 — point-source mechanic

Implement two solvers on the same grid:

1. the delayed-center rule, exactly as written; and
2. a causal hyperbolic field solver with the same static kernel and propagation speed.

Sweep \(\beta_g\in\{0,10^{-3},10^{-2},10^{-1}\}\), both velocity signs, multiple grid
resolutions, and a stationary control. Measure:

- ring multipoles \(A_0,A_1,A_2\);
- leading/trailing potential and acceleration;
- dynamical-center offset versus radius;
- field energy and momentum balance;
- convergence under grid and timestep refinement.

Predeclared delayed-center prediction: \(A_1\propto\beta_g\), sign reversal when **w**
reverses, and the leading/trailing signs derived above. The causal solver is the adversarial
control, not an implementation detail.

### Stage 2 — distributed galaxy

Use equal-total-mass profiles with varied concentration: point-like center, bulge+disk,
exponential disk, and diffuse sphere. Keep \(c_g\), **w**, outer radius, and numerical policy
fixed. Measure \(C[\rho;R]=A_1/\beta_g\) and whether the dynamical-center lag survives local
outer-disk contributions.

Only after the field is measured should non-interacting tracer particles be added. Compare
the two azimuthal halves of their rotation field and track secular torque or orbital heating.
Do not fit real data in this stage.

### Stage 3 — observational confrontation

If and only if a consistent substrate solver retains a wake, preregister a galaxy-sample
test. Fit one common substrate velocity **U** and coupling law across isolated galaxies;
compare predicted asymmetry axes and amplitudes against observed kinematic lopsidedness.
Controls must include companions, tides, ram pressure, bars, spiral structure, inclination,
and measurement asymmetry. Per-galaxy free wake directions would make the theory
non-predictive and are forbidden.

## Rejection criteria

The wake branch is refuted, not repaired, if any of these gates fires:

1. **Mechanic gate:** the causal substrate solver has \(A_1\) consistent with zero at first
   order while the delayed-center shortcut alone produces the effect. Then the wake was an
   artifact of the shortcut.
2. **Convergence gate:** \(A_1/\beta_g\), its sign, or the center offset fails to converge
   with resolution and timestep.
3. **Conservation gate:** a persistent wake exchanges energy or momentum but the theory has
   no substrate account balancing it.
4. **Density gate:** central concentration does not predict the amplitude under fixed mass,
   radius, and velocity. Then the specific dense-center argument is false.
5. **Universality gate:** explaining a sample requires an independent substrate direction,
   wave speed, or coupling for each galaxy, or those parameters merely track disk size.
6. **Orientation gate:** after environmental controls, observed asymmetry axes do not align
   with the single inferred substrate-relative velocity field.
7. **Existing-physics gate:** the coupling needed for a galactic signal exceeds the
   preferred-frame, photon-sector, gravitational-wave-speed, or local-dynamics bounds carried
   by the Principia studies.
