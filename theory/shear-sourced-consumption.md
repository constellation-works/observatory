---
title: "Shear-sourced consumption: a local candidate for the source law"
status: growing
families: [gravity-as-scarcity]
almanac: 15-discussions/26-08/from-big-bang-questions-to-the-shear-consumption-law.md
created: 2026-08-11
updated: 2026-08-20
---

# Shear-sourced consumption

**The idea (kepler, 2026-08-11 — provoked by Daniel: "give it a crack").** The source-law
debt — the one consolidated gravitational debt of the family
([gravity-as-scarcity](gravity-as-scarcity.md) § open questions; three strikes: ORB-10162,
ORB-10164, [two-substance-vortex-vacuum](two-substance-vortex-vacuum.md) §B2) — asks for a
law of non-conservation: *where does substance go*, such that the free-fall
(Gullstrand–Painlevé) inflow the clock sector demands is sustained. This doc proposes and
analytically characterizes one candidate: **space is consumed at a rate equal to its density
times the local anisotropic (tidal) strain rate of its own flow.** The law is local,
universal, scale-free, source-blind, has coefficient exactly one, uniquely selects the GP
profile among steady radial flows with the mass-scaling freedom every previous local attempt
lacked, consumes nothing in a homogeneous expanding universe, and closes its global budget
against Hubble generation at exactly the turnaround radius. It is a **named postulate with
measured-shape obligations**, not a derivation from the counting mechanic — the ORB-10162
verdict on the mechanic's natural rules stands untouched.

**Current verdict (rewritten 2026-08-12, after ORB-10751; amplitude paragraph added
2026-08-20):** *all three predeclared kill gates passed on-lattice.* Faraday's cataloged
dynamical lattice
([shear-consumption-lattice](../../orrery/lab/sims/shear-consumption-lattice/), orrery
`a8da4ec`) — frozen coefficient-one von Mises destruction, no imposed profile — converges
from rest and from perturbed states to a measured steady exponent **−0.5000150 ± 1.6×10⁻⁵**
(combined seed/resolution/timestep error; −1/2 inside one error), selects the exterior
amplitude strictly monotonically from the core flux, and consumes nothing (3.7×10⁻¹⁶ of
n|H|) on a uniformly expanding lattice. The law survived its falsifiers. Two things kept it
from being more than a strong candidate: the amplitude–mass coupling A = √(2GM) remained
underived (the gate showed A is *controllable* from the core, not that masses set it), and
the exploratory two-core probe measured a **different superposition family than the
counting mechanic's** (§ falsifier postscript) — the two lattice models disagreeing on a
measurable, with at most one of them the mechanic behind the MW boost.

**The amplitude development (2026-08-20, § the level-matching closure below):** both
residues now have an analytic answer awaiting its lattice gate. The doc's recorded natural
guess for the coupling — the matter region sets the surface inflow via its own internal
consumption, a *flux-type* coupling — is **excluded in closed form**: a universal
per-energy consumption rate matched at the body surface forces G_eff = κ²ρ_body/(24πn²) —
exterior gravity tracking the source's *bulk density*, independent of its mass — breaking
mass additivity and contradicting the counting mechanic's own verified σ ∝ M
normalization. What closes the amplitude instead is **level matching**: the counting
mechanic's draw-sourced standing level σ = GM/c²r, the parent's rolling rule applied to
space (ORB-10159 branch 3), and this doc's shear law form a closed, consistent,
parameter-free steady system whose unique solution is GP with **A = √(2GM)** — and whose
consistency *forces* the shear coefficient to be exactly one. On the closure, the two-core
superposition divergence is predicted to be a **flux-boundary artifact** (levels superpose
by the counting family, not the flux family). Every claim is gated: **ORB-10932** (level,
density, and composition gates), the level-core note on **ORB-10755**, and the sourcing
task **ORB-10933**. If ORB-10932's gates pass, the source-law debt's amplitude core
dissolves into postulates the family had already named — no new debt is created.

## The law

Let the substrate have density n and flow field **v**, with strain-rate tensor
e_ij = ½(∂_i v_j + ∂_j v_i). Decompose e into its isotropic part (tr e)/3 and deviatoric
part e^dev. The proposed consumption law:

**s = n · √( (3/2) e^dev : e^dev )**  — volumetric destruction rate = density × von Mises
equivalent (anisotropic) strain rate, coefficient 1.

For an axisymmetric radial flow (eigenvalues e_rr, e_θθ, e_θθ) this scalar reduces exactly
to |e_rr − e_θθ|, so the radial statement is s = n(e_rr − e_θθ): destruction wherever the
flow stretches along one axis and squeezes along the others — i.e., wherever it is *tidally
distorted*. Isotropic strain — uniform expansion or compression — consumes nothing.

Sign convention: converging accelerating inflow (GP-like) has e_rr > 0 > e_θθ and consumes;
the time-reversed (white-hole-like) outflow has the shear signature reversed and *generates*.
The law carries a sensible two-sided symmetry rather than a bolted-on arrow.

## The derivation — uniqueness with free amplitude

Steady state, uniform n (the incompressible fork of the debt), radial flow v_r(r):

- Continuity: s = −n ∇·**v** = −n (e_rr + 2e_θθ).
- The law: s = n (e_rr − e_θθ).

Equating: e_rr − e_θθ = −e_rr − 2e_θθ ⟹ **e_θθ = −2 e_rr**, i.e. dv_r/dr = −v_r/2r, whose
general solution is

**v_r = −A r^(−1/2)** for any A ≥ 0.

No power-law ansatz — this is the full solution of the ODE. Three properties, each of which
killed previous candidates and is delivered here:

1. **The profile is unique** — v ∝ r^(−1/2) is the *only* steady radial flow the law
   admits. This is the GP profile; with A = √(2GM) it gives σ = v²/2c² = GM/c²r, the 1/r
   scarcity field, and Schwarzschild clock rates exactly, per the ORB-10159 analytic branch.
2. **The amplitude is free.** A scale-free local law of the form s ∝ n v³ also reproduces
   the r^(−3/2) sink, but fixes *one* amplitude for all masses (its coupling would have to
   run as 1/GM) — no mass scaling. The shear law leaves A as an integration constant, so
   different masses can carry different field strengths under one universal rule. This was
   the structural obstruction to any local source law; the shear law dissolves it.
3. **The sink comes out right by identity.** For the GP flow, e_rr = +v/2r (inner shells
   fall faster — radial stretch) and e_θθ = −v/r (transverse squeeze), so
   n(e_rr − e_θθ) = (3/2)nv/r — exactly the volumetric consumption continuity demands,
   at coefficient one. Nothing is tuned.

## Three checks that came out unforced

- **Cosmological silence.** Pure Hubble flow **v** = H**r** has e_rr = e_θθ = H — zero
  anisotropic shear — so the law consumes nothing in a homogeneous expanding universe.
  Homogeneous-isotropic (FRW) spacetimes are exactly the Weyl-flat ones, so "shear consumes,
  isotropic strain is free" echoes GR's split between tidal (Weyl) and volume (Ricci)
  curvature (`conjecture` as a correspondence — resonance noted, nothing derived). The
  law does not eat the expansion; conversely it supplies no generation term — what sources
  the 3Hn of homogeneous expansion is cosmology's side of the books, not this law's.
- **The global budget closes at the turnaround radius.** The GP flow's intake through a
  sphere of radius R grows as 4πnA R^(3/2) — an isolated mass in static space would demand
  infinite supply, which is the old "where does it all come from" objection to every inflow
  picture. In an expanding universe, Hubble generation at 3H per unit volume supplies
  4πnHR³ inside R, and this balances the intake exactly where HR = √(2GM/R) — i.e. at
  R³ = 2GM/H², the **turnaround radius**, the physically correct boundary where infall
  detaches from expansion. Masses eat what expansion makes, with no tuned cutoff.
  **Measured (ORB-10754, 2026-08-12): order-unity yes, exact no** — against the
  Karachentsev-program zero-velocity radii with *independent* (orbital/virial) masses,
  R_meas/R_sc ≈ 0.55 median (0.43–0.83); the data track the ΛCDM zero-velocity formula
  (ratio ≈ 1.0), whose O(1) matter/Λ factors this law's pure-Hubble idealization drops.
  Details and the circularity discipline in
  [studies/cosmological-expansion-and-bound-systems](../studies/cosmological-expansion-and-bound-systems.md)
  § measured turnaround radii.
- **All consumption is distributed; the mass itself eats nothing.** The inward flux
  4πr²nv ∝ r^(3/2) → 0 at the center: the law needs no point sink at the matter, so it
  evades ORB-10162's specific failure (central-only consumption gives the refuted
  flux-conserving 1/r² flow). The mass *anchors* the flow; the vacuum's own strained state
  does the consuming.

## What this does not deliver — the debts of the payment

Stated before anyone gets excited:

1. **It is a postulate.** The law is not derived from the counting mechanic — it is a third
   rule, exactly the "impose it as a named postulate" route the parent's statement of record
   anticipated, now with unexpectedly good structure. ORB-10162's verdict (neither *natural*
   counting rule yields GP) stands in full.
2. **The amplitude–mass coupling is underived.** With the central flux zero, nothing in the
   fluid mechanics ties A to M. The boundary condition at the matter — how a mass of given
   energy imposes √(2GM) on the exterior flow — is the surviving hard core of the source-law
   debt, relocated but not paid. (Natural guess: the matter region sets v at its surface via
   its own internal consumption; underived.) **Update 2026-08-20 (§ the level-matching
   closure below):** the natural guess is now excluded in closed form, and the coupling has
   an analytic closure — level matching against the counting field — that dissolves this
   debt into already-named postulates iff its lattice gates pass (**ORB-10932**).
3. **Stability is unproven.** Uniqueness of the steady state is not convergence to it. If GP
   is a repeller rather than an attractor under time-dependent dynamics, the law is dead on
   arrival. Lattice question.
4. **Superposition is unknown.** Two-source behavior under the shear law has no analytic
   result here — and after ORB-10157 (the multiplicative rule's derivation dying by
   measurement), no superposition claim gets stated without a lattice run.
5. **Non-radial flows are unexplored.** Rotating, translating, and wave-carrying
   configurations all shear; the law consumes in all of them. Whether that produces
   phenomenology (secular drag on orbiting bodies? consumption in gravitational-wave
   fields?) or pathology is unknown and must be bounded before the law is more than a
   steady-state statement.
6. **It does not touch the galactic question.** The acceleration-organization problem
   (ORB-10169) is untouched: this law addresses the clock/photon-sector debt, not the
   boost's carrier or form.

## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| The shear-consumption law + continuity uniquely select v ∝ r^(−1/2) (GP) among steady radial flows, with free amplitude | supported | Closed-form ODE derivation (§ above), now cataloged with its dynamical confirmation: **ORB-10751** measures steady exponent −0.5000149713 ± 2.9×10⁻⁷ (regression SE), ± 1.6×10⁻⁵ combined across seeds/resolution/timestep — −1/2 within one combined error |
| The GP sink s = (3/2)nv/r equals n(e_rr − e_θθ) at coefficient exactly 1, and equals the von Mises form for radial flows | supported | Algebraic identity (§ the law), exercised on-lattice: ORB-10751's frozen rule *is* the coefficient-one von Mises law and the GP profile emerges under it |
| The law consumes nothing in homogeneous Hubble flow (cosmological silence) | supported | ORB-10751 silence gate: uniformly expanding lattice shows max consumption density 7.4×10⁻¹⁸ = 3.7×10⁻¹⁶ of n\|H\| — consistent with zero |
| GP is a dynamical *attractor* under the law (arbitrary initial flows converge) | supported | ORB-10751 attractor gate: convergence from rest and from perturbed initial states; initial-condition exponent difference 1.2×10⁻⁶; resolution (128/256/512 shells) and timestep (dt 0.2/0.1/0.05) sequences both converge on −1/2 |
| A core boundary condition selects the exterior amplitude A monotonically and stably | supported | ORB-10751 amplitude gate: exterior half-power amplitude rises strictly (2.4×10⁻⁴ → 2.6×10⁻²) across core flux 0.003–0.3; max initial-condition relative spread 9.6×10⁻⁷ |
| A mass of energy E imposes specifically A = √(2GM) via its boundary condition | mixed | The *controllability* half is measured (row above); the *identification* half now has a closed-form candidate — the level-matching closure (§ 2026-08-20): counting level + rolling rule + shear law force A = √(2GM) uniquely, with no new postulate. `mixed` until the closed system is measured to be a lattice attractor: **ORB-10932** level gate |
| The amplitude coupling is flux-type — a universal per-energy consumption rate matched at the matter surface (the doc's recorded natural guess) | refuted | Closed-form (§ closure (a), symbolically checked): flux matching forces G_eff = κ²ρ_body/(24πn²) — source strength ∝ bulk density, independent of M — contradicting the counting mechanic's verified mass-only σ ∝ M normalization and breaking mass additivity except at universal packing density. External universality bounds `conjecture — to verify` → **ORB-10933**; lattice discriminator predeclared as **ORB-10932**'s density gate |
| The closed system {draw-sourced 1/r level, inertial rolling rule, coefficient-one shear law} is consistent, parameter-free, and uniquely selects GP with A = √(2GM); consistency forces the shear coefficient k = 1 | supported | Closed-form derivation (§ closure (b)): Bernoulli against the 1/r level gives ½v² = c²σ = GM/r at every radius; shear+continuity independently give v ∝ r^((k−2)/(k+1)), matching only at k = 1. Verified symbolically. The *attractor* question is separate and `untested` → **ORB-10932** |
| Newtonian mass additivity forces quadrature composition of river amplitudes (A² additive; A ∝ √N for clustered sources) | supported | Algebra (§ closure (c)): GM_eff = A²/2 and mass additivity. Kills linear velocity superposition (σ ∝ N²) and one-amplitude laws (s ∝ nv³) structurally; level coupling passes by construction. Lattice gate: **ORB-10932** composition gate (kill on converged exponent ≠ 1/2) |
| The ORB-10751 two-core superposition divergence is a flux-boundary artifact; level-type cores restore the counting mechanic's ORB-10157 headroom family | conjecture | Predicted by the closure (§ closure (d)); recorded as a pre-pickup comment on **ORB-10755**. A converged confirmation of the divergent family under flux cores would not adjudicate the level-coupled system; the level-core arm does |
| Two-source superposition under the shear law reproduces the measured headroom-screening family (ORB-10157) | mixed — measured divergence | ORB-10751 two-core probe (exploratory, coarse 25³ grid): best fit A(D) = 1/(1 + 6.82 D^0.668) at log-RMSE 0.031; the ORB-10157 family (1−D)^1.071 fits at log-RMSE 0.421 with substantially weaker screening. **The shear law and the counting mechanic disagree on superposition** — at most one matches whatever nature does. Resolution-converged adjudication filed as **ORB-10755** |
| Global budget: Hubble generation inside R balances GP intake exactly at the turnaround radius R³ = 2GM/H² | mixed | **ORB-10754** (tycho, 11 systems, Karachentsev program + Virgo/Fornax): with independent masses, measured turnaround radii sit at 0.43–0.83× (median ≈ 0.55) the budget radius — right scale, wrong coefficient. Data track the ΛCDM zero-velocity formula (≈ 1.0), whose matter/Λ factors the pure-Hubble idealization here drops. Circular R₀-derived masses excluded per the compilation's own flags ([study note](../studies/cosmological-expansion-and-bound-systems.md)) |
| "Shear consumes, isotropic strain doesn't" corresponds to GR's Weyl/Ricci split | conjecture | Resonance only; no derivation, no citation yet |

## Falsifier → faraday

Filed as **ORB-10751** (ws_orrery, crew sol, high, 2026-08-11): a dynamical lattice
implementing local strain-coupled destruction — s computed from neighbor flow differences,
no imposed profile — with predeclared gates:

1. **Attractor gate:** seeded from rest and from perturbed states around a consuming core,
   does the flow converge to v ∝ r^(−1/2) (measured exponent −0.5 within apparatus error)?
   Failure to converge, or convergence to another exponent, kills the law.
2. **Amplitude gate:** does an imposed core boundary condition (surface inflow or core
   consumption rate) select the amplitude A monotonically and stably? If A is not
   controllable by the core, debt 2 is unpayable in this form.
3. **Silence gate:** a uniformly expanding lattice must show consumption consistent with
   zero (the cosmological-silence check, on-lattice).
4. **Superposition probe:** two cores; measure the modulation law and compare against the
   ORB-10157 headroom-screening family. Exploratory, not a kill gate.

### Adjudication (ORB-10751, faraday, 2026-08-12) — all three kill gates passed

Cataloged as [shear-consumption-lattice](../../orrery/lab/sims/shear-consumption-lattice/)
(orrery `a8da4ec`; deterministic, byte-identical rerun verified, run-record SHA
`294f74c8…`). Apparatus: radial finite-volume lattice, nearest-neighbour Fick transport,
frozen coefficient-one von Mises destruction computed from neighbour flow differences,
fixed-flux core, unit-density outer reservoir — **the velocity profile is measured, never
imposed.** Verified at source against `summary.json`:

1. **Attractor — passed.** p = −0.5000149713, regression SE 2.9×10⁻⁷, combined
   seed/resolution/timestep error 1.6×10⁻⁵; the two initial conditions agree to 1.2×10⁻⁶;
   128/256/512-shell and dt-halving sequences both approach −1/2 monotonically.
2. **Amplitude — passed.** Exterior amplitude strictly monotonic in core flux across two
   orders of magnitude (0.003 → 0.3), initial-condition spread < 10⁻⁶. The coupling *route*
   is open; the √(2GM) identification remains underived (debt 2 stands, narrowed).
3. **Silence — passed.** Uniform expansion consumes ≤ 3.7×10⁻¹⁶ of n|H| — zero at apparatus
   precision.
4. **Superposition probe — divergence measured** (exploratory; coarse 25³ grid, stated as
   the run's strongest limitation). The two-core modulation is best fit by
   A(D) = 1/(1 + 6.82 D^0.668) (log-RMSE 0.031); the ORB-10157 screening family fits poorly
   (log-RMSE 0.421) and screens far less. Consequence if it survives resolution: the shear
   law and the counting mechanic make **incompatible superposition predictions**, and the
   shear law's stronger screening pushes the solar-system channel toward the *screened*
   reading — the one ORB-10097/ORB-10098 found unconstrained (predicts ~0 AU-scale
   deviation), not the multiplicative reading that carries the Uranus tension. The
   resolution-converged adjudication is filed as **ORB-10755** (faraday, ws_orrery, high):
   ≥3-rung resolution ladder, deeper-depletion range, separation control — converged
   family or artifact-verdict, predeclared.

## The amplitude–mass coupling — the level-matching closure (kepler, 2026-08-20)

The surviving hard core of the source-law debt after ORB-10751 was one question: *why does
a mass of energy E impose specifically A = √(2GM)?* The amplitude gate measured
controllability — an imposed core flux selects A monotonically — but nothing identified
which core property nature ties to M. This section answers it in two moves: the doc's own
recorded natural guess is excluded in closed form, and the coupling that survives closes
the amplitude exactly, using only ingredients the family had already named. All algebra
below was verified symbolically (sympy; scripted check in the ORB-10932 filing); every
physical claim is gated on **ORB-10932**.

### (a) The flux-type coupling, made precise and excluded

The natural guess — "the matter region sets v at its surface via its own internal
consumption" — made precise is a *flux-type* coupling: each unit of mass-energy destroys
substrate volume at a universal rate κ, so a body of mass M and radius r_s demands intake
Φ = κM through its surface. Matching to the exterior GP-family flow (flux through r is
4πnA·r^(3/2)) gives A = κM/(4πn·r_s^(3/2)), hence

> G_eff = A²/2M = κ²M/(32π²n²r_s³) = **κ²ρ_body/(24πn²)**

— exterior gravity proportional to the source's **bulk density**, independent of its mass.
This fails twice:

1. **Internally**, it contradicts the counting mechanic's own verified normalization.
   Every cataloged static sim sources σ by draws ∝ M with no dependence on how the drawing
   mass is packed; the fitted galactic and solar-system sectors all inherit that
   mass-only normalization. A flux-coupled amplitude is a *different* source law from the
   one the family's entire evidence base was measured under.
2. **Externally**, a source strength tracking bulk density at O(1) — the Sun (1.4 g/cc)
   and Earth (5.5 g/cc) generating with effective couplings differing ×4; a body's exterior
   gravity strengthening as it contracts at fixed mass — is grossly non-Newtonian. The
   discriminating channels need care (every purely dynamical channel measures only the
   product G_eff·M; the discrimination enters through inertially calibrated masses —
   laboratory G determinations with source materials spanning ~2–19 g/cc agree at ~10⁻⁴ —
   and through additivity). `conjecture — to verify`: the precise sourced bounds are
   **ORB-10933**'s studies note.

A subtlety recorded for honesty: at *universal packing density* the flux coupling
accidentally reproduces mass scaling (r_s ∝ M^(1/3) gives A ∝ √M, G = κ²ρ/(24πn²)
universal) — which is why the guess never looked absurd. It dies on density *diversity*,
and the lattice discriminator is predeclared as ORB-10932's **density gate**: equal draw
strength, core radii differing ≥ 4× — level coupling predicts identical exterior A, flux
coupling predicts A ∝ r_s^(−3/2).

### (b) The closure: three named ingredients, one solution, no freedom

Take the three ingredients the family already carries, and nothing else:

1. **The counting level** (verified statically, by construction of the mechanic): a mass's
   draws generate a standing scarcity level σ(r) = GM/c²r, mass-additive in the dilute
   regime with the measured ORB-10157 headroom corrections at O(D).
2. **The rolling rule for space** (the ORB-10159 branch-3 postulate): substrate parcels
   obey the model's one dynamical law, a = c²∇σ — inertially, so a parcel falling from
   rest at the reservoir carries the Bernoulli integral ½v² = c²σ.
3. **The shear law** (this doc): s = n·(von Mises anisotropic strain rate), which with
   continuity admits exactly the profile family v = A·r^(−1/2), any A.

The system is closed and consistent, and its solution is unique. Rolling down the 1/r
level from rest gives ½v² = c²σ = GM/r at every radius — the profile is r^(−1/2)
(consistent with what shear+continuity independently force) and the amplitude is pinned:
**A = √(2GM), with no adjustable quantity anywhere in the system.** The two 1/r shapes —
the drawn level and the flow's kinetic energy — coincide; that coincidence is exactly the
ORB-10159 branch-3 identity σ = ½v²/c², now appearing as the *equilibrium condition* of a
closed system rather than as a definition.

Two corollaries fall out unforced:

- **Coefficient one is forced, not tuned.** With a general shear coefficient k, continuity
  selects v ∝ r^((k−2)/(k+1)); only k = 1 gives the r^(−1/2) that Bernoulli-against-the-
  level demands. In the closed system the law's one potentially tunable number is fixed by
  consistency with the counting field.
- **G is the counting mechanic's constant, as always.** The shear law introduces no new
  constant; the closure's G is the draw-to-level conversion the static sims have always
  carried. The gravitational "charge" is the draw rate — whether draw rate tracks total
  energy (as the equivalence principle demands to parts in 10¹²,
  [studies/equivalence-principle-tests](../studies/equivalence-principle-tests.md)) is the
  same inherited question it was before the closure, neither helped nor hurt.

What the closure is *not*: a derivation of any of its three ingredients. It is the proof
that their conjunction is consistent, closed, parameter-free, and lands on exactly the GP
amplitude the clock sector demands. The debt transforms rather than vanishes — "why
√(2GM)" dissolves into postulates already on the books (rolling rule; draws ∝ M; shear
law), and **no new postulate is created**. Whether the closed system is a dynamical
*attractor* — whether a lattice with draw-sourced levels, inertial rolling-rule flow, and
frozen shear destruction actually equilibrates there — is a measurable property nothing
guarantees: **ORB-10932's level gate** (predeclared kill: converged violation of
A² = 2c²σ_s·r_s, or non-convergence).

### (c) The composition constraint — quadrature additivity as a knife

Newtonian mass additivity is a constraint on any river amplitude, independent of the
closure: since GM_eff = A²/2 and masses add, **A² must add — amplitudes compose in
quadrature, A ∝ √N for N clustered unit sources.** This is a knife over the whole
candidate space: velocity fields that superpose linearly give σ ∝ N² (catastrophic);
s ∝ nv³-type laws fix one amplitude for all masses (no scaling — the doc's original
observation); level coupling passes automatically (levels add ⟹ A² ∝ N); flux coupling
passes only at universal packing density (the accident in (a)). Predeclared as
ORB-10932's **composition gate**: N co-clustered unit cores, far-field A ∝ N^(1/2), kill
on any other converged exponent.

### (d) What the closure predicts for the superposition divergence

The ORB-10751 two-core probe measured its modulation family — 1/(1 + 6.82·D^0.668),
sharply divergent from the counting mechanic's (1−D)^1.071 — **on flux-type cores**, the
coupling (a) excludes. On the closure, exterior amplitudes are set by *levels*, and levels
superpose by the counting mechanic's measured family. Prediction (`conjecture`, gated):
**the divergence is a flux-boundary artifact — rerun with level-type cores and the
superposition family reverts to ORB-10157's headroom screening.** If it holds, the "two
lattice models disagree on a measurable" wrinkle dissolves: there is one mechanic with two
boundary conditions, only one of them physical. Recorded on **ORB-10755** as a pre-pickup
comment (a converged confirmation of the divergent family under flux cores would not
adjudicate the level-coupled system). One independent pressure point, also recorded there:
a non-analytic small-D family (D^p, p < 1) has unbounded d ln A/dD as D → 0 and cannot
limit to linear superposition, which the solar system measures to high precision
(`conjecture — to verify`: the precise PPN-nonlinearity bound belongs to ORB-10933's
studies note, and the D ↔ σ normalization is the same one the parent's carrier question
leaves unfixed).

### (e) Status and gates, stated plainly

Algebra `supported` (closed-form, symbolically checked): the flux-coupling density formula;
the closure's uniqueness and its two corollaries; quadrature composition. Physics gated:
the attractor question and the flux-vs-level discrimination (**ORB-10932**: level, density,
composition gates, all predeclared); the superposition-artifact prediction (**ORB-10755**
comment; follow-on under ORB-10932's apparatus if needed); the external universality bounds
(**ORB-10933**). One declared idealization to keep honest: the closure treats the drawn
level and the flowing substrate as two coupled ledgers over one lattice — draws generate
σ while shear destroys flowing substrate — and whether draw dynamics maintain the 1/r
level *under* advection and consumption is part of what ORB-10932 measures, not something
this section may assume.

## Related

- [gravity-as-scarcity](gravity-as-scarcity.md) — the parent; this doc addresses its
  source-law debt (§ open questions) and, if the gates pass, converts the GP-conditional
  clock (ORB-10159) and photon (ORB-10158-gated) sectors from conditional to postulated-law
  physics. Nothing here moves the parent's ledger.
- [two-substance-vortex-vacuum](two-substance-vortex-vacuum.md) — §B2's incompressible fork
  owes exactly this law; if the shear law survives its gates, that family's Branch B
  inherits it as the candidate S2 non-conservation dynamics (ORB-10164's L-0005 handoff).
- [studies/river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md) —
  the GP flow and its clock/photon consequences.
- [studies/cosmological-expansion-and-bound-systems](../studies/cosmological-expansion-and-bound-systems.md)
  — the expansion-side physics the turnaround-balance check leans on.
