---
title: "Shear-sourced consumption: a local candidate for the source law"
status: exploratory
families: [gravity-as-scarcity]
almanac: 15-discussions/26-08/from-big-bang-questions-to-the-shear-consumption-law.md
created: 2026-08-11
updated: 2026-08-11
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

**Current verdict:** *analytically characterized; nothing tested.* Every row below is
`untested` or `conjecture` per the house rule (evidence enters only through a cataloged
orrery sim or a sourced study note). The falsifier task is filed (§ below).

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
  detaches from expansion (standard structure-formation turnaround scales agree at order
  unity; `conjecture — to verify`, cosmology study note owed:
  [studies/cosmological-expansion-and-bound-systems](../studies/cosmological-expansion-and-bound-systems.md)
  is the natural carrier). Masses eat what expansion makes, with no tuned cutoff.
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
   its own internal consumption; underived.)
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
| The shear-consumption law + continuity uniquely select v ∝ r^(−1/2) (GP) among steady radial flows, with free amplitude | untested | Closed-form ODE derivation (§ above); decisive on paper but uncataloged — awaits an orrery fixture per the house rule |
| The GP sink s = (3/2)nv/r equals n(e_rr − e_θθ) at coefficient exactly 1, and equals the von Mises form for radial flows | untested | Algebraic identity (§ the law); same cataloging debt |
| The law consumes nothing in homogeneous Hubble flow (cosmological silence) | untested | e^dev = 0 for **v** = H**r** — one-line check, uncataloged |
| Global budget: Hubble generation inside R balances GP intake exactly at the turnaround radius R³ = 2GM/H² | conjecture — to verify | Arithmetic identity given the law; the comparison to measured turnaround scales needs the cosmology study note |
| "Shear consumes, isotropic strain doesn't" corresponds to GR's Weyl/Ricci split | conjecture | Resonance only; no derivation, no citation yet |
| GP is a dynamical *attractor* under the law (arbitrary initial flows converge) | untested | **ORB-10751**'s primary gate (§ below) |
| A mass of energy E imposes amplitude A = √(2GM) via its boundary condition | untested | Underived (debt 2); the falsifier probes whether an imposed core consumption rate selects A |
| Two-source superposition under the shear law reproduces the measured headroom-screening family (ORB-10157) or something else | untested | Lattice question; no analytic claim made |

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
