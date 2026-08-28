---
title: "Moving-source field consistency: what survives of the wake"
status: growing
families: [retarded-scarcity-wake]
almanac: 15-discussions/26-08/from-galactic-motion-to-the-moving-gravity-medium-problem.md
created: 2026-08-07
updated: 2026-08-21
---

# Moving-source field consistency

**The proposal (2026-08-07).** [The retarded-scarcity wake](../retarded-scarcity-wake/) sets up a
three-way fork — delayed-center memory (A), causal steady field (B), emergent metric (C) — and
routes the adjudication through a two-solver Orrery apparatus. This document argues that the
naïve delayed-center arm is **partly decidable on paper**: it is not the compact-source exterior
solution of the standard Poisson equation, and its alternative retarded-direction force is
non-conservative. Branch B supplies a known no-lag result only after a boost-invariant control
equation and complete coupling are specified. The live branch is therefore a genuinely
boost-violating substrate model with an explicit field equation, not retardation by itself.

The practical consequence is a reordered program: retain the delayed-center construction as a
negative control, define a precise boost-invariant calibration equation, derive the surviving
branch's amplitude law, and use observational work first to establish sensitivity and the
structure-formation baseline rather than to claim a universal wake bound.

**Current verdict:** the delayed-center construction fails as the source-free exterior solution
of the standard Poisson equation for a compact moving mass. That is narrower than proving that no
local substrate theory could produce the same shape: a different operator or a real distributed
substrate response could do so, but would have to be written explicitly and would no longer be the
retarded-position shortcut. The established-physics claims this document leans on — gravitational
aberration cancellation, gravitational Cherenkov bounds, and observed lopsidedness amplitudes —
remain `conjecture — to verify` pending the moving-source study note.

Principia's ledger has no `derived` status and admits evidence only through a cataloged sim or a
sourced study. The analytic rows below therefore remain `untested` until the proposed Orrery
fixture lands, even where the algebra is decisive on paper.

**Revised 2026-08-08.** The observational half is now deliberately conditional. Published
lopsidedness scales depend on sample and convention: values around 0.1 are typical in a larger
near-IR sample, while older smaller samples used 0.2 as a threshold, so the delayed-center toy's
\(2\times10^{-3}\) scale is roughly 50–100× smaller rather than uniquely 100× smaller. Even that
comparison does not bound the surviving boost-violating branch, whose amplitude law has not been
derived. A large-\(N\) alignment measurement is statistically conceivable under independent-noise
assumptions, but neither the noise model nor the proposed peculiar-velocity/tidal correlation is
yet established for the \(m=1\) observable.

## Contents

- [Evidence ledger](evidence-ledger.md)
- [Related](related.md)
- [Open questions](open-questions.md)


## The delayed-center potential is not a Poisson-vacuum field

Take the parent's postulate exactly as written: \(\boldsymbol{\Delta}(R)=-\mathbf{w}R/c_g\), with
\(+y\) along \(\mathbf{w}\) and \(\theta\) measured from the leading direction. Then

\[
\lvert\mathbf{r}-\boldsymbol{\Delta}\rvert
= R\sqrt{1+2\beta_g\cos\theta+\beta_g^{2}},
\qquad
\Phi_{\rm lag}=-\frac{GM}{R}\left(1+2\beta_g\cos\theta+\beta_g^{2}\right)^{-1/2}.
\]

For \(|\beta_g|<1\), that radical has the convergent Legendre expansion
\((1-2xt+t^{2})^{-1/2}=\sum_n P_n(x)t^{n}\) with \(x=\cos\theta\) and \(t=-\beta_g\). So the
postulate can be written as

\[
\boxed{\;\Phi_{\rm lag}(R,\theta)=-\frac{GM}{R}\sum_{n\ge0}(-\beta_g)^{n}P_n(\cos\theta)\;}
\]

The radical in the preceding equation remains the defining expression at \(\beta_g\ge1\), but
this series does not converge there. All first-order conclusions below concern the galactic
\(\beta_g\ll1\) regime.

Two things fall out immediately, and neither needs a solver.

**The angular shape never decays.** Every term carries the same \(1/R\). Therefore \(R\,\Phi_{\rm lag}\)
is a function of \(\theta\) alone, and the dipole-to-monopole ratio is \(\beta_g\) *at every radius*,
out to infinity. A physical offset center — mass displaced by a fixed distance \(d\) — gives a
dipole ratio \(d/R\rightarrow0\). The delayed-center rule instead makes the asymmetry a fixed
fraction of the monopole arbitrarily far from the galaxy, because the postulated displacement
grows linearly with the distance at which you evaluate it. That is the first sign that
\(\boldsymbol{\Delta}(R)\) is a bookkeeping device rather than a configuration.

**The radial powers are forbidden by the standard exterior Laplace equation.** A solution of
\(\nabla^2\Phi=0\) outside a compact source and decaying at infinity must be built from
\(P_n(\cos\theta)/R^{n+1}\). Here every \(n\ge1\) term is \(P_n(\cos\theta)/R\).
Using \(\nabla^{2}\!\left[R^{a}P_n\right]=\left[a(a+1)-n(n+1)\right]R^{a-2}P_n\) with \(a=-1\):

\[
\nabla^{2}\Phi_{\rm lag}
= GM\sum_{n\ge1}(-\beta_g)^{n}\,n(n+1)\,\frac{P_n(\cos\theta)}{R^{3}},
\qquad
\rho_{\rm eff}=\frac{\nabla^{2}\Phi_{\rm lag}}{4\pi G}
\simeq-\frac{\beta_g M}{2\pi}\frac{\cos\theta}{R^{3}} .
\]

Read through the standard Poisson equation, the postulate therefore corresponds to an effective
source filling all of space: **negative** density ahead of the galaxy and positive behind it at
first order, falling as \(1/R^{3}\). Because every \(P_{n\ge1}\) integrates to zero over the sphere,
no effective *mass* is enclosed — the monopole is clean, which is why the pathology hides from any
spherically averaged diagnostic. The effective dipole moment is not clean:

\[
D_y=\int\rho_{\rm eff}\,R\cos\theta\;d^{3}r
=-\frac{2}{3}\beta_g M\int dR ,
\]

linearly divergent in the box radius. This is enough to reject \(\Phi_{\rm lag}\) as the
source-free exterior Poisson field of the compact galaxy. It is **not** an impossibility theorem
for every local conservative substrate theory: a different differential operator or a genuine
distributed substrate degree of freedom could support a nonharmonic exterior profile. Such a
model would have to state that mechanism and its conservation law explicitly; it would no longer
be the delayed-position shortcut pretending to follow from propagation time alone.

This resolves the shortcut side of the parent's rejection gate 1 without a solver: the proposed
\(O(\beta_g)\) profile is not an exterior Poisson-vacuum field. It does not determine whether a
different, explicitly boost-violating Branch C equation produces its own \(m=1\) response.

## Two rules, and only one of them is even a force law

The parent declares \(\mathbf{a}=-\nabla\Phi\) but then computes accelerations as though the
displaced center were a point mass at fixed offset. These are different objects and they disagree
at first order — see § The corrected first-order contrast. The second rule deserves its own
treatment, because it is the more natural reading of "the field points where the source was":

\[
\mathbf{a}_{\rm ret}(\mathbf{r})=-\,GM\,
\frac{\mathbf{r}-\boldsymbol{\Delta}(R)}{\lvert\mathbf{r}-\boldsymbol{\Delta}(R)\rvert^{3}} .
\]

Because \(\boldsymbol{\Delta}\) depends on \(R\), this field has nonzero curl —
\(\lvert\nabla\times\mathbf{a}_{\rm ret}\rvert\approx\beta_g\,\lvert\mathbf{a}\rvert/R\) at generic
points — and is therefore **non-conservative**. Numerically, generic closed loops spanning both
radius and polar angle can return work of order \(\beta_g GM/R\) per circuit. Nonzero curl
guarantees that such loops exist, not that every eccentric trajectory gains energy with the same
sign on every lap.

This matters for the apparatus in a specific and unobvious way. Constant-\(R\) circles return
**exactly zero** work, by the \(\sin\theta\) parity of the tangential component. A Stage-2 tracer
study seeded only on circular orbits would therefore see no non-conservation at all, while a study
that varies eccentricity and apsidal orientation can expose loop-dependent work — which the
parent's § Observable signatures lists as a *physical* signature ("secular torque, heating, or
drag if the substrate absorbs momentum").
Under this rule that heating is an artifact of a non-conservative postulate, not evidence of
momentum transfer to a substrate. The parent's rejection gate 3 (conservation) would fire, but the
apparatus could easily be configured never to trigger it.

## The corrected first-order contrast

From the parent's own \(\Phi_{\rm lag}=-\frac{GM}{R}\left(1-\beta_g\cos\theta\right)+O(\beta_g^{2})\),
the inward acceleration is

\[
g(R,\theta)=-\frac{\partial\Phi}{\partial R}\Big|_{\rm inward}
=\frac{GM}{R^{2}}\left(1-\beta_g\cos\theta\right),
\qquad
g_{\rm lead}=g_0(1-\beta_g),\quad g_{\rm trail}=g_0(1+\beta_g),
\]

\[
\frac{g_{\rm trail}-g_{\rm lead}}{g_0}\simeq 2\beta_g \quad\text{(not }4\beta_g\text{)}.
\]

The parent's \(4\beta_g\) is what \(\mathbf{a}_{\rm ret}\) gives: a point mass at separation
\(R(1+\beta_g)\) yields \(g_0/(1+\beta_g)^{2}\simeq g_0(1-2\beta_g)\). Both coefficients are
internally derivable; neither is derivable from *both* stated rules. Since Stage 1 predeclares
"the leading/trailing signs derived above" as its prediction, the ambiguity has to be resolved
before predeclaration means anything — a factor of two is the difference between a passed and a
failed convergence comparison.

The potential contrast, \(\Phi_{\rm lead}-\Phi_{\rm trail}\simeq2\beta_g GM/R\), is unaffected.

## Why uniform motion does not make a wake in the boost-invariant control

For a boost-invariant field theory, a galaxy in **uniform** translation has a frame in which the
entire matter configuration — dense center and sparse outskirts alike — is static. The retarded
solution can therefore be stationary without being centered on a sequence of independently stale
positions. The intuition that "field information reaching the outskirts originated when the
center was behind its current position" omits the velocity-dependent part of the steady solution
and the fact that the outskirts share the same translation.

This argument is conditional. A medium with a physically observable rest frame, dissipation, or
other explicit boost violation can distinguish uniform motion and can support a steady wake in the
source frame. That is not a consequence of finite propagation alone; it is extra dynamics that
must be specified as Branch C.

Relative to the boost-invariant control, an \(O(\beta_g)\) dipole can therefore arise from:

1. **Acceleration.** A genuinely accelerated source can leave a retarded signature. Its scale is
   controlled by the velocity change over the relevant propagation time and by the field equation,
   not simply by the uniform speed \(\lvert\mathbf{w}\rvert\).
2. **Explicit boost-violation.** A substrate equation that is not invariant under boosts genuinely
   distinguishes \(\mathbf{U}\), and can produce a first-order dipole. This is Branch C with the
   symmetry actually broken rather than hidden, and its coupling is bounded — not predicted — by
   [lorentz-violation-bounds](../../studies/lorentz-violation-bounds.md).

`conjecture — to verify`: for electromagnetism, the Heaviside field of a uniformly moving charge
points at the instantaneous position exactly because the Liénard–Wiechert velocity term cancels
the retarded-position aberration. [Carlip 2000](https://arxiv.org/abs/gr-qc/9909087) shows the
analogous velocity-dependent cancellation in general relativity through the nonradiative orders
relevant to orbital stability; radiation reaction is the controlled residual. This resolves
Laplace's aberration objection without requiring instantaneous gravity. What is settled is the
absence of the naïve \(O(\beta_g)\) lag in those specified theories—not the behavior of every
possible preferred-medium equation.

## The gravitomagnetic gap

The parent's Stage 2 adds "non-interacting tracer particles" to the measured field. But the
tracers share the galaxy's velocity \(\mathbf{w}\) relative to the substrate, and in any theory
with a velocity-coupling (gravitomagnetic-analogue) force, that force acts on them. The
electromagnetic precedent demonstrates that a field component viewed in one frame is not by
itself the force law for a moving tracer: electric and magnetic terms transform together so that
the physical co-moving description agrees with the rest-frame one.

If the substrate model carries only a scalar \(S\) with \(\mathbf{a}=-\nabla S\), then that absence
of velocity coupling is itself a physical postulate rather than a neutral default. The complete
tracer coupling has to be specified in the apparatus contract, or Stage 2 cannot distinguish a
substrate prediction from an artifact of an incomplete force law.

## The delayed-center toy supplies a scale, not a ceiling

`conjecture — to verify`. If \(c_g=c\), as the GW170817/GRB 170817A bound requires for the
observed tensor mode ([scalar-gravity-ppn-constraints](../../studies/scalar-gravity-ppn-constraints.md)),
then a generous peculiar velocity of 600 km/s gives \(\beta_g\approx2\times10^{-3}\). The
delayed-center toy consequently gives \(A_1\sim2\times10^{-3}\) when its concentration coefficient
is taken to be order unity.

Published comparison scales are sample-dependent. The Jog & Combes review reports older samples
with roughly 30% of disks above \(A_1=0.2\), but also a larger 149-galaxy sample with roughly 30%
above 0.1 and a characteristic amplitude near 0.1
([review](https://ned.ipac.caltech.edu/level5/Sept09/Jog/Jog2.html),
[arXiv:0811.1101](https://arxiv.org/abs/0811.1101)). The toy amplitude is therefore roughly
50–100× below representative observed lopsidedness scales. A study note must fix the population,
radial statistic, and threshold before quoting one factor as canonical.

This comparison scopes **the refuted delayed-center toy only**. Branch C has no derived relation
between a boost-breaking parameter and \(A_1\), so \(2\times10^{-3}\) is not a ceiling on every
surviving substrate wake. The missing calculation is

\[
A_1=F(\epsilon_{\rm boost},\beta_g,\rho,\text{tracer coupling}),
\]

followed by bounds on \(\epsilon_{\rm boost}\). Until that exists, the document cannot conclude
that a surviving wake either explains or fails to explain the observed population.

A conventionally coupled subluminal gravitational mode faces a separate and powerful wall.
[Moore & Nelson 2001](https://arxiv.org/abs/hep-ph/0106220) infer
\((c-c_g)/c<2\times10^{-15}\) under the conservative assumption that the observed ultra-high-energy
cosmic rays traveled only Galactic distances, and a bound of order \(2\times10^{-19}\) if their
origin is extragalactic. Either excludes \(c_g\sim10^{-3}c\) for the mode they analyze. Applying the
same limit to an additional substrate mode requires specifying that mode's coupling to matter and
its dispersion; "any subluminal mode" is too broad.

## Idealized detectability of the toy amplitude

The following arithmetic asks a narrow question: if an aligned component really has
\(A_1=2\times10^{-3}\), and if every other contribution is independent zero-mean scatter, how many
galaxies would be required? Under those assumptions the error falls as \(1/\sqrt N\):

| per-galaxy \(\sigma(A_1)\) | \(N\) for \(3\sigma\) on \(A_1=2\times10^{-3}\) | for \(5\sigma\) |
|---|---|---|
| 0.05 | 5,600 | 15,600 |
| 0.10 | 22,500 | 62,500 |
| 0.20 | 90,000 | 250,000 |

Imperfect velocity directions multiply these totals by \(1/f^2\), where \(f\) is the attenuation
of the aligned statistic. Values such as 4× for \(f=0.5\) or 11× for \(f=0.3\) are illustrations,
not catalog forecasts. Correlated structure, selection effects, and coherent reconstruction errors
do not necessarily average down this way. The table establishes conditional detectability, not
that the proposed test can identify a substrate contribution.

## A degeneracy to measure, not assume

The common-cause intuition is plausible: an overdensity contributes both to a galaxy's peculiar
velocity and to its external tidal environment. But the leading Taylor expansion of the external
potential about the galaxy's freely falling center is

\[
\Phi_{\rm ext}=\Phi_0+g_i x_i+\frac12T_{ij}x_i x_j+\frac16O_{ijk}x_i x_j x_k+\cdots.
\]

The uniform \(g_i\) term is locally unobservable, while the tidal tensor \(T_{ij}\) is quadrupolar
and naturally drives \(m=0\) and \(m=2\) structure in a disk—not an \(m=1\) phase. An \(m=1\)
alignment can arise from tidal gradients \(O_{ijk}\), halo offsets, accretion, or nonlinear disk
response, but it is not implied by the shared overdensity alone.

Therefore the peculiar-velocity/asymmetry-axis correlation is a **conjectured confounder**, not a
supported zeroth-order prediction. Isolation cuts do not guarantee its removal, but they may
change it and cannot be dismissed without measurement. A positive alignment result must still be
compared with a cosmological simulation baseline; the reason is that the null correlation is
unknown, not that it has already been shown to equal the proposed signal.

## A candidate geometric discriminator

`untested`, and the underlying response is **asserted rather than derived**.

There is no reason for \(\mathbf{w}\) to lie in the disk plane. Decomposing it against the disk
normal:

- the **in-plane** component sources the \(m=1\) lopsidedness discussed throughout; and
- the **perpendicular** component gives a vertical potential gradient whose magnitude varies with
  radius — a warp-like distortion rather than an in-plane one.

If that holds, the model may predict a **split** between which distortion a galaxy shows and its
orientation relative to \(\mathbf{w}\): disks with \(\mathbf{w}\) near their plane should be
preferentially lopsided, while disks with \(\mathbf{w}\) near their normal should be displaced
vertically. Whether the resulting mode and available samples make this measurable remains part of
the derivation debt.

The forcing components are fixed geometrically once \(\mathbf{w}\) is known, but the observable
response is not parameter-free: disk self-gravity, vertical restoring frequency, halo shape, gas
fraction, and forcing history all enter. The perpendicular dipole produces a radially varying
vertical acceleration at the midplane, which may resemble a bowl-like displacement rather than
the usual integral-sign warp. Standard tides may also possess orientation dependence.

Before it can be used it must be derived: compute the vertical response of a disk to the
perpendicular component of the dipole term, classify the resulting vertical mode, and compare it
with the orientation dependence in a structure-formation baseline. A *uniform* vertical pull is
unobservable by the equivalence principle; the signal lives entirely in differential forcing.

## Proposed program

Replacing the parent's § Future Orrery apparatus. No apparatus is authorized here either; this is
the recommended shape of the faraday task when one is.

### Stage 0 — analytic pass (no apparatus)

This document. Outcome: the delayed-center construction is rejected as a compact-source exterior
solution of the standard Poisson equation, and its alternative force rule is identified as
non-conservative. This does not adjudicate every local substrate equation. Cost: no solver.

### Stage 1′ — solver calibration, not science

Specify a boost-invariant control equation and its complete source and tracer couplings, then use
its uniformly moving solution for **instrument validation**. That control must return no
\(O(\beta_g)\) dipole; depending on the field component and frame, the first deformation may be
\(O(\beta_g^2)\) and fore-aft symmetric or the co-moving observable may remain identical to rest.
A first-order dipole is a solver defect only if the declared control equation forbids it. A generic
"causal hyperbolic solver" is not enough specification to make that judgment.

Do **not** build the delayed-center solver as a physics arm. If it is built at all, it is built as
a demonstration that the shortcut reproduces \(\rho_{\rm eff}\propto\cos\theta/R^{3}\) under the
standard Poisson diagnostic and non-conservative loop work — a negative-control fixture,
catalogued as such.

### Stage 2′ — the only live mechanic question

Specify a substrate equation that breaks boost invariance *explicitly*, and compute what wake
amplitude a given breaking parameter yields. Note the change in epistemic status: the wake is then
a **free parameter bounded by Lorentz tests**, not a prediction of the theory. Stage 2′ is
worthwhile only if it produces a relation between the breaking parameter and \(A_1\) that the
existing bounds do not already crush. Test that relation against
[lorentz-violation-bounds](../../studies/lorentz-violation-bounds.md) *before* writing the solver.

Any tracer study in this stage must include the velocity-coupling sector (§ The gravitomagnetic
gap) and must seed eccentric as well as circular orbits (§ Two rules).

### Stage 3′ — baseline and feasibility work

Catalog work can begin before a substrate solver, but it does not yet bound every wake model. Its
immediate purpose is to measure the null correlation, catalog error model, and attainable
sensitivity. Interpreting any result as a substrate bound must wait for Stage 2′ to supply a common
velocity definition, an amplitude law, and the relevant observable.

Three requirements the first draft of this section missed:

1. **Size the sample against a declared signal.** The table in § Idealized detectability applies
   only to the delayed-center toy amplitude and independent scatter. A null at \(A_1\sim10^{-2}\)
   sensitivity says nothing about a \(2\times10^{-3}\) toy signal, but neither number bounds Branch
   C until its amplitude relation exists.
2. **Measure the null correlation.** Use a cosmological simulation to determine whether peculiar
   velocity actually correlates with the \(m=1\) phase, through which physical channel, and how
   isolation changes it. Do not promote the common-cause intuition to a baseline result in advance.
3. **Derive the shape observable first.** The proposed vertical response is not parameter-free and
   may be a bowl-like mode rather than an integral-sign warp. It becomes a preferred test only if
   its response and its distinction from standard tides are both demonstrated.

Same controls as the parent requires beyond that: companions, ram pressure, bars, spiral
structure, inclination, measurement asymmetry. Per-galaxy free wake directions remain forbidden.

## Rejection criteria for this document

What would overturn or materially narrow the argument above:

1. **Change the exterior operator or source inventory.** The non-harmonicity argument applies to
   the standard Poisson-vacuum exterior problem. A local conservative substrate equation with a
   different operator or a physical distributed response would evade that narrow result, while
   acquiring new source, boundary, and conservation obligations of its own.
2. **Boost-violating recovery.** If the substrate equation is explicitly non-boost-invariant,
   Branch-A-like phenomenology can be recovered legitimately. That does not rescue Branch A — it
   relabels the result as Branch C and inherits the Lorentz bounds. If those bounds turn out to
   permit an \(O(\beta_g)\) galactic dipole, this document's scoping conclusion is too strong.
3. **Amplitude relation.** If a concrete Branch C equation yields a bounded amplitude large enough
   to account for observed lopsidedness, the toy-model scale in this document is irrelevant. The
   current 50–100× comparison is not a rejection criterion for that branch.
4. **First-order aberration cancellation.** Stage 1′ relies on the absence of an \(O(\beta_g)\)
   dipole in its specified boost-invariant control. Exact cancellation at every order is not
   required for that calibration; the study note must state which orders Carlip and the
   electromagnetic result actually establish.
5. **The proposed degeneracy.** A cosmological baseline may predict no useful correlation between
   peculiar-velocity direction and \(m=1\) phase, because the leading tide is quadrupolar. That
   would simplify the alignment test rather than contradict the Poisson-vacuum result.
6. **The warp split.** If the perpendicular component of the dipole produces a rigid vertical
   displacement rather than a radially varying one, the lopsidedness/warp trade-off does not exist
   and the shape test dies with it.
