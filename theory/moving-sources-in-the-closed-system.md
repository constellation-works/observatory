---
title: "Moving sources in the closed system: the substrate wind, exactly"
status: growing
families: [gravity-as-scarcity]
almanac: 15-discussions/26-08/from-galactic-motion-to-the-moving-gravity-medium-problem.md
created: 2026-08-21
updated: 2026-08-21
---

# Moving sources in the closed system

**The idea (kepler, 2026-08-21 — the front that opens once the closure is fully measured).**
With ORB-10751, ORB-10932, ORB-10755, and ORB-10934 all adjudicated, the closed system
{draw-sourced counting level σ = GM/c²r, rolling rule for space a = c²∇σ, coefficient-one
shear-consumption law} is a measured structure — but every measurement so far is **static
and radial**. The oldest killer of substrate theories waits exactly one step further: a
source *moving through* the substrate. The
[retarded-scarcity-wake](retarded-scarcity-wake.md) family already mapped this territory
for a *postulated* retarded potential and found that nothing survives except an explicit
substrate equation with derived dynamics
([moving-source-field-consistency](moving-source-field-consistency.md): retardation talk is
not a model; Branch C — matter as excitations of the medium — is the only live reading).
The closed system **is** such an explicit substrate equation, and its uniform-motion
problem turns out to be partly solvable in closed form. Two exact results fall out, one
reassuring and one sharp: the wind is invisible in the *speed* field (and therefore, in
the excitation reading, in the clock sector at first order), and the flow *pattern* around
a moving mass provably differs from general relativity's moving-source river at first
order in the wind — a measurable wake, with a new named debt (consumed momentum) attached.

**Current verdict:** the wind-tunnel fixture ran (ORB-10935, faraday, 2026-08-21 — §
adjudication below) and split the front cleanly. The Galilean null and the Bernoulli
branch's lattice realization are verified at machine precision, the measured wake differs
grossly from GR's boosted river (0.46–0.73 rad RMS), and the Bernoulli speed law's
no-stagnation-point corollary gives a sharp qualitative discriminator. But the apparatus's
predeclared steady-existence measurable returned a real wrinkle: **no globally smooth
steady single-valued flow branch exists at any swept wind strength** (ladder-stable
caustics). Because the apparatus *imposes* Bernoulli (a Hamilton–Jacobi march of the speed
law) rather than letting the dynamics discover it, the theorem rows sit at `mixed`, not
`supported`: the conditional algebra is machine-verified, and its premise — that the
moving system reaches a steady irrotational state — is now the front's live question.

The dynamical-relaxation fixture then ran (ORB-10937, faraday, 2026-08-21 — second §
adjudication below) and returned **the third outcome** — the one the binary framing
missed: neither a steady state nor sustained unsteadiness, but *slow relaxation still in
progress at the feasible horizon*. The velocity sector settles (its residual meets the
predeclared criterion at every wind on the finest rung); the density sector does not —
the consumption trough around the core is still deepening at T = 60, decaying at a
U-independent rate whose e-folding time (~65) is comparable to the whole run. No steady
sample was admitted, so the Theorem 1 kill remains undelivered. One constructed-branch
result did *not* survive contact with the dynamics: the realized consumed-momentum drag
is **linear in the wind** (|∫s·v_x dV| ≈ 56·U^0.98, drag sign at every U), not the
branch's near-U-independent 20.3·U^0.098. The extended-horizon fixture (filed at this
adjudication) inherits the kill next.

## Setup

Substrate of uniform density n, at rest at infinity (frame Σ — the reservoir frame the
lattice apparatus has always had). A mass M translates uniformly at velocity **U** through
Σ. Work in the mass frame (inertial for uniform **U**; the closed system's ingredients are
all Galilean-covariant): the wind blows past at −**U** at infinity, and the level is
**exactly comoving** — draws move with the mass and the level solve is elliptic
(instantaneous), as in every cataloged apparatus (ORB-10932/ORB-10934's discrete Gauss /
Poisson accumulation). So σ = GM/c²r rides rigidly with the source. A finite
level-propagation speed would add retardation distortions on top; that is the
[retarded-scarcity-wake](retarded-scarcity-wake.md) family's question and is out of scope
here — this doc analyzes the closed system *as implemented and measured*.

Steady state in the mass frame. The flow **v** (substrate velocity in the mass frame)
obeys:

- **Rolling rule** (steady): (**v**·∇)**v** = c²∇σ.
- **Continuity with consumption**: ∇·(n**v**) = −s.
- **Shear law**: s = n·√((3/2) e^dev : e^dev).

The inflow at infinity is uniform (−**U**), hence irrotational; the force is a pure
gradient, so Kelvin's theorem keeps the flow irrotational everywhere. (For ∇×**v** = 0 the
convective term is (**v**·∇)**v** = ∇(|**v**|²/2) — the identity is symbolically checked.)

## Theorem 1 — the wind is invisible in the speed field

For steady irrotational flow the momentum equation integrates globally:

> ∇(|**v**|²/2) = c²∇σ  ⟹  **|v|² = U² + 2c²σ(x)  everywhere.**

The constant is fixed at infinity. Consequences, each exact at this order:

1. **Speed isotropy.** At fixed distance from the source, the river's *speed* is exactly
   isotropic — √(U² + 2GM/r) — for every wind strength. The wake lives entirely in the
   **direction field**; the speed field carries no dipole, no fore-aft asymmetry, nothing
   at any order in U. Note the consumption law never entered: this holds for *any*
   consumption rule, being a property of {comoving elliptic level + rolling rule +
   irrotational inflow} alone. The shear law's role is downstream: with continuity it
   selects the direction field (and decides whether a steady wake exists at all — an
   existence question only the lattice can answer; first answer 2026-08-21, § adjudication:
   no globally smooth single-valued branch at any swept wind; second answer the same day,
   dynamical: the velocity sector settles but the density trough is still relaxing at the
   feasible horizon — existence remains the live question, now looking like slow
   convergence rather than intrinsic unsteadiness).
2. **The clock sector inherits no first-order wind anomaly.** In the excitation reading
   (the only surviving one — [lorentz-violation-bounds](../studies/lorentz-violation-bounds.md)),
   a clock at rest in the mass frame dilates by its speed relative to the local river:
   1 − |**v**|²/2c² = **1 − U²/2c² − GM/c²r** — precisely the special-relativistic
   dilation for absolute motion U compounded with the gravitational term, the combination
   that agrees with general relativity's boosted-Schwarzschild static clock at first
   order (the GP-dilation identity is the river model's own,
   [river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md)).
   The classic ether-drift clock anomaly — the thing that kills naive medium theories —
   *cancels by structure*: Bernoulli against a comoving level converts wind speed into
   exactly the SR dilation the wind should produce. Second-order cross terms
   (O(U²·GM/c⁴r)) are not examined here and belong to PPN territory.
3. **Multi-source form.** Levels superpose by the counting family (measured through
   superposition order: ORB-10157, ORB-10934), so in the dilute regime
   |**v**|² = U² + 2c²Σᵢσᵢ. The theorem survives source multiplicity.
4. **The pure-wind state is exactly steady and exactly silent.** Uniform **v** = −**U**
   with no source has zero strain (checked), zero consumption, and satisfies all three
   equations — the Galilean null the apparatus must reproduce identically.

## Theorem 2 — the wake is not the boost: a first-order discriminator against GR

General relativity's river around a uniformly moving mass is, at leading order in U/c, the
kinematic boost of the static GP river: **v**_GR = **U** + **v**_GP. Its speed field is
**anisotropic**: |**v**_GR|² = U² + 2GM/r + 2**U**·**v**_GP — a speed dipole of magnitude
2U·v_GP·cosθ. The closed system **forbids that dipole** (Theorem 1). Equivalently, checked
symbolically: the boosted-GP field fails the closed system's momentum equation with
residual exactly (**U**·∇)**v**_GP ≠ 0 — it would require the comoving level to carry a
velocity-coupled dipole term **U**·**v**_GP/c², which the counting mechanic does not
generate. Draws source a scalar level; nothing sources a vector potential.

Stated structurally: **the closed system as it stands has no gravitomagnetic sector.** Its
g₀ᵢ-analog is whatever direction field the wake dynamics produce, not GR's
velocity-coupled term. The two theories therefore differ at **O(U·v_GP)** — first order in
the wind — in every observable that rides the flow's *direction* rather than its speed:
photon propagation (fore-aft deflection and Shapiro asymmetry around a moving lens), and
orbiting-clock cross terms (for an orbital velocity **w**, dilation reads
|**v** − **w**|²; the −2**v**·**w** term samples the direction field, so the wake pattern
sets an O(Uw/c²) orbital-phase modulation that GR fixes differently). Whether the
measured wake conspires toward or away from GR's structure is exactly what the wind-tunnel
apparatus measures; the external bounds it must then face (moving-lens deflection,
preferred-frame PPN α₁/α₂, frame-dragging measurements) are the studies note's cargo —
`conjecture — to verify` until sourced.

## The new debt the wake exposes: consumed momentum

The shear law destroys substrate volume; the destroyed parcels carry momentum n**v**. For
every static configuration this bookkeeping was invisible — spherical symmetry integrates
the consumed momentum to zero. The wake breaks the symmetry: consumption is fore-aft
asymmetric at O(U), so the consumed-momentum integral ∫s**v** dV has a net component along
**U**. The theory has never said where it goes. Three postures, now distinguishable:

1. **It vanishes with the volume** (the law already breaks volume conservation by design):
   no force on anything, but momentum non-conservation acquires a *directional*,
   in-principle-observable signature.
2. **The substrate absorbs it**: the wake carries a momentum flux; the reservoir
   recoils — cosmology's books again.
3. **The source absorbs it**: a moving mass feels secular drag (or thrust — the sign is
   not obvious and must be measured), decelerating it toward the substrate frame over
   secular timescales — ephemeris- and pulsar-constrainable, once normalized.

The lattice can measure the wake's momentum budget in lattice units (gate G3). Converting
any of it to a physical drag requires the substrate-inertia normalization nothing in the
family has fixed — the same class of gap as the D ↔ σ normalization on the carrier
question. Recorded as a **named debt**, not resolved here.

## What sets U — the inherited question, sharpened

[retarded-scarcity-wake](retarded-scarcity-wake.md) § open debts already asks what defines
the substrate velocity at a real body. The closed system sharpens it uncomfortably:
substrate parcels obey the rolling rule — they free-fall — while matter virializes into
orbits. A parcel and a star that once comoved do not stay comoving; around any orbiting
body the model *generically* predicts a wind of order the local orbital/infall speeds. If
the galactic Newtonian field is river-carried, the arithmetic (from the sourced velocity
scales in [lorentz-violation-bounds](../studies/lorentz-violation-bounds.md) § velocity
scales: solar galactic orbit ~220 km/s; CMB motion 369.82 km/s; solar river at 1 AU
~42 km/s) puts U_⊙ at O(300 km/s) — U/c ~ 10⁻³ — and Theorem 2's O(U·v_GP) photon-sector
wake effects land in the neighborhood of measured light-deflection precision. That is a
**live kill test**, not yet executable: it needs the measured wake structure (the
apparatus below) and the sourced bounds (the studies note). The escape routes are
themselves informative: either the local substrate comoves with local structure (needs a
mechanism the rolling rule does not provide), or the galactic field is not river-carried
(feeding the open carrier question on
[gravity-as-scarcity](gravity-as-scarcity.md) § what remains live), or the model eats a
preferred-frame contradiction at O(10⁻³).

## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| Steady irrotational flow of the closed system around a uniformly moving mass has exactly isotropic speed \|v\|² = U² + 2c²σ; the wake is confined to the direction field (Theorem 1) | mixed | The algebra is exact (sympy) and its lattice realization is verified at machine precision — ORB-10935 G1: normalized speed dipoles 0.8–2.7×10⁻¹⁶, pointwise Bernoulli residual ≤3.9×10⁻¹⁶, all 8 U×r cases converged ([level-core-wind-tunnel](../../orrery/lab/sims/level-core-wind-tunnel/)). But the apparatus *imposes* the speed law (Hamilton–Jacobi march) and found **no globally smooth steady single-valued branch at any swept U** (§ adjudication). The dynamical fixture (ORB-10937, [level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)) then evolved the real equations with Bernoulli imposed nowhere: no case met the joint steadiness criterion by T = 60, so **no steady sample was admitted and the kill remains undelivered** — a finite-horizon result (velocity sector settles; density trough still relaxing, e-fold ~65 ≈ horizon), not a refutation of steadiness. The extended-horizon fixture inherits the kill |
| A clock comoving with the moving mass reads 1 − U²/2c² − GM/c²r — no first-order ether-drift clock anomaly; wind dilation is exactly SR's | untested | Corollary of Theorem 1 in the excitation reading (readings and dilation identity: [river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md), [lorentz-violation-bounds](../studies/lorentz-violation-bounds.md)). Rides on Theorem 1's realization — unresolved until the steady-existence question settles (see the mixed row above). Second-order cross terms unexamined (PPN territory) |
| The pure-wind state (no source) is an exact steady solution with exactly zero consumption | supported | ORB-10935 G4 (kill gate): no-core wind states at all four speeds keep maximum pointwise consumption ≤2.2×10⁻¹⁷ and speed error exactly 0.0 on every rung — the real frozen stencil evaluated, not a construction ([level-core-wind-tunnel](../../orrery/lab/sims/level-core-wind-tunnel/)). ORB-10937 G5 (kill gate) adds the dynamical twin: pure wind advanced to T = 60 by the full SSP-RK2 time integrator preserves velocity and density exactly with consumption at floating precision, on every rung and wind ([level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)) |
| The boosted-GP field is not a solution of the closed system — residual (U·∇)v_GP; the steady wake differs from GR's moving-source river at O(U·v_GP), and the GR speed dipole 2U·v_GP is forbidden (Theorem 2) | mixed | Boost-failure is exact (symbolic residual) and the measured departure is gross, not perturbative — ORB-10935 G2: 0.456–0.732 rad weighted RMS direction departure from U + v_GP across all U, fore-aft n_x asymmetry −0.86…−0.92, and **no stagnation point can exist on any Bernoulli branch** (q ≥ U > 0) while boosted GP has axis speed zeros — a sharp qualitative discriminator. Mixed because the realized wake is provisional on the same steady-existence question as Theorem 1 — ORB-10937 admitted no steady case, so the realized direction field has still not been measured on a settled flow |
| The closed system has no gravitomagnetic sector; reproducing tested g₀ᵢ phenomenology (moving-lens deflection, frame dragging, preferred-frame PPN α₁/α₂) from emergent wake dynamics is an open obligation with existing external bounds | conjecture — to verify | Structural (no vector source in the counting mechanic); the external bounds await the moving-source studies note this doc's program files (the note [moving-source-field-consistency](moving-source-field-consistency.md) § open debts already demanded) |
| Consumed momentum has no bookkeeping; the wake makes the gap observable (possible secular drag on moving sources) | mixed | ORB-10935 G3 measured the constructed branch: drag sign at every wind, fit \|∫s·v_x dV\| = 20.3·U^0.098 — nearly U-independent. ORB-10937 G4 then measured the *realized* (time-averaged, still-relaxing) flow and the constructed scaling **did not survive**: consumed +x momentum is **linear in the wind** — consumed/U = 61.8, 61.8, 61.1, 57.2 across the 33× sweep, fit \|∫s·v_x dV\| = 55.9·U^0.979, drag sign at every U, finest adjacent-rung shifts within the 25% target ([level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)). Linear-in-U drag is what momentum-flux capture predicts (rate ∝ nU × capture volume) and is the physically sensible secular-drag form. The surface ledger stays advective-only; the debt itself (where the momentum goes, physical normalization) remains open |
| No globally smooth steady single-valued flow branch exists around a moving core at any swept wind strength — the moving system's steady state, if any, is not a positive-x Bernoulli graph | supported | ORB-10935's predeclared steady-existence measurable: caustic clip fractions at finest 0.740, 0.713, 0.573, 0.028 for U/v_GP ∈ {0.03, 0.1, 0.3, 1}, ladder-stable across 41³/61³/81³. At low U partly structural (the near-radial GP inflow limit is not a positive-x graph), but the trans-critical wind also clips. ORB-10937's dynamics neither confirm nor deny a steady end-state within T = 60: the flow is classified `decaying_slowly_not_yet_saturated` at every (U, rung) — what the true dynamics settle to is now the extended-horizon fixture's question |
| The approach to steadiness is rate-limited by the density sector, not the velocity sector: the velocity field settles while the consumption trough relaxes at a U-independent rate | supported | ORB-10937 G1 finest rung, all four winds: the velocity residual meets its half of the predeclared criterion over the window (max dv_rms 5.2–5.3×10⁻⁴ < 2×10⁻³) while the density residual fails it everywhere (dn_rms 4.5–6.1×10⁻³), with minimum density still declining monotonically (0.27–0.32 at T = 60) and late log-residual slope −0.0148…−0.0173 per time unit across the whole sweep — an e-folding time ~65, U-independent, comparable to the horizon ([level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)). Consistent with relaxation toward a consumption–resupply balance rather than turbulence: no growing modes, no saturated shedding frequency dominates |
| The local wind U at real bodies is O(local orbital/infall speeds) if the relevant fields are river-carried, putting photon-sector wake effects at O(10⁻³) relative scale for the Sun | conjecture | Arithmetic over sourced velocity scales ([lorentz-violation-bounds](../studies/lorentz-violation-bounds.md) § velocity scales); contingent on the open galactic-carrier question; kill test executable only after the realized wake structure + the studies note |

## The program — gates predeclared

**Wind-tunnel lattice (faraday, ws_orrery — filed with this doc).** The ORB-10934
apparatus (full 3-D draw-sourced level coupling, frozen coefficient-one stencil) with a
uniform wind boundary condition: substrate streaming past a single comoving level core at
speeds U spanning sub- to trans-critical ratios against the local river scale. Gates:

1. **G1 — speed-isotropy gate (kill gate for Theorem 1).** On the converged ladder, the
   measured speed field at fixed r must be isotropic and equal to √(U² + 2c²σ(r)) within
   apparatus error, across all wind strengths. A converged anisotropy — in particular any
   dipole — refutes the Bernoulli closure of the moving system (and with it the clock
   corollary's cancellation).
2. **G2 — wake-structure measurement.** The direction field's angular structure versus
   the boosted-GP comparator: multipoles of v̂, stagnation geometry, fore-aft asymmetry
   versus U. Measurement, not a kill — this is the model's moving-source *prediction
   being generated*, the input the photon-sector confrontation needs.
3. **G3 — momentum-budget gate.** Net momentum flux balance over the wake (lattice
   units): which of the three consumed-momentum postures the dynamics realize, and the
   drag/thrust scaling with U. Kill only on non-convergence.
4. **G4 — Galilean null control.** Wind with no core: the uniform state must persist with
   consumption exactly zero at apparatus precision (the moving-frame twin of ORB-10751's
   Hubble-silence gate).

Also predeclared as *out of scope here*: rotating sources (the frame-dragging
confrontation needs its own apparatus), finite level-propagation speed (the
retarded-wake family's territory), and any observational fit before G2's wake structure
and the studies note both exist.

### Adjudication (ORB-10935, faraday, 2026-08-21) — the branch is exact, the wake is not the boost, and steady existence is now the question

**Apparatus.** [level-core-wind-tunnel](../../orrery/lab/sims/level-core-wind-tunnel/)
(orrery `3f08098`): the ORB-10934 3-D draw-sourced elliptic level extended with a uniform
wind, in the comoving-core frame (wind enters only at the upstream face; the level is
solved once per rung and rides with the core). Fixed physical domain (half-width 12) and
core width (σ = 0.75) across a 41³/61³/81³ ladder; wind sweep U/v_GP(r=5) ∈ {0.03, 0.1,
0.3, 1}; consumption stencil byte-identical to ORB-10751 (SHA-256
`aa1155e0…` exact match); deterministic, no RNG, byte-identical rerun verified.
**Method caveat, load-bearing:** the direction field is *constructed* as the positive-x
Hamilton–Jacobi branch of |∇Φ|² = U² + 2σ — the apparatus imposes Bernoulli and asks
whether a globally consistent branch exists and what it looks like. It does not evolve
the rolling rule to a steady state. The gates read accordingly.

1. **G1 — pass, at machine precision.** On the constructed branch, normalized speed
   dipoles are 0.8–2.7×10⁻¹⁶ with low multipoles inside combined apparatus errors of
   1.7–5.8×10⁻⁴, and the pointwise speed matches √(U² + 2c²σ) to ≤3.9×10⁻¹⁶ — for every
   wind strength and both measurement radii, converged. The Bernoulli branch's lattice
   realization is exact; what G1 does *not* test, given the construction, is whether the
   dynamics select this branch.
2. **G2 — measured, converged.** The realized direction field departs from the boosted-GP
   comparator U + v_GP by 0.456–0.732 rad weighted RMS across the sweep — gross, not
   perturbative — with fore-aft mean-n_x asymmetry −0.86…−0.92. And one exact corollary
   surfaced with teeth: **the Bernoulli speed law forbids stagnation points** (q =
   √(U² + 2c²σ) ≥ U > 0 everywhere), while the boosted-GP field has axis speed zeros. A
   moving-mass flow with a stagnation point would refute the speed law outright — a
   qualitative, parameter-free discriminator between the closed system and GR's river.
3. **The predeclared steady-existence measurable returned its wrinkle.** At every swept
   wind the march hits caustics: clip fractions at the finest rung 0.740, 0.713, 0.573,
   0.028 (U ascending), stable across the ladder. No globally smooth steady single-valued
   branch exists in this ansatz. At low U this is partly structural — the U → 0 limit is
   the radial GP inflow, which no positive-x potential graph can represent — but even the
   trans-critical wind clips. Honest reading: the theorems' shared premise (a steady
   irrotational state) has not been shown to be dynamically realized. Steady-wake
   existence — steady non-graph flow, a genuinely unsteady wake, or no attractor at all —
   is now the front's live question.
4. **G3 — pass, converged.** On the constructed branch the consumed +x momentum integral
   has **drag sign at every wind** (posture 3's sign, in lattice units): 14.2, 12.2, 10.7,
   21.5 across the sweep, four-wind fit |∫s·v_x dV| = 20.3·U^0.0976 — nearly
   U-independent, which itself wants explaining if it survives the dynamical apparatus.
   The advective flux-minus-consumed residual is reported, not zeroed: the level-stress
   surface term is deliberately unmodeled.
5. **G4 — pass, exactly.** The pure-wind null: no-core wind states at all four speeds
   keep maximum pointwise consumption ≤2.2×10⁻¹⁷ and speed error exactly zero on every
   rung — the real frozen stencil evaluated on the real lattice, the moving-frame twin of
   ORB-10751's Hubble-silence gate. This one is a true dynamical statement, not a
   construction.

**Declared limits:** one-way draw coupling; finite zero-level Dirichlet box (fixed
physical geometry across the ladder, no infinite-reservoir extrapolation); single-valued
positive-x graph ansatz (the caustic diagnostic is the honest boundary of its
representational reach); advective-only momentum surface term.

**Consequence and successor.** The front's structure after ORB-10935: the *conditional*
content (Bernoulli branch, boost-failure, no-stagnation corollary, drag-sign asymmetry,
Galilean null) is measured and healthy; the *premise* (steady realization) is not. The
successor fixture is the **dynamical-relaxation wind tunnel** (ORB-10937, filed at this
adjudication, faraday, ws_orrery): evolve the actual equations — rolling rule +
continuity + shear — as an initial-value problem from a blended wind/GP start, and let
the dynamics decide. If a steady state emerges, its speed field is a *discovered* test of
Theorem 1 (the kill G1 could not deliver by construction) and its direction field
supersedes G2's branch. If none emerges, the moving closed system is intrinsically
unsteady, and the wake confrontation changes character entirely (time-dependent lensing
residuals, not static wake multipoles).

### Adjudication (ORB-10937, faraday, 2026-08-21) — the dynamics relax slowly, the velocity settles first, and the drag is linear in the wind

**Apparatus.** [level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)
(orrery `eceac3e`): the literal time-dependent system — ∂**v**/∂t + (**v**·∇)**v** = c²∇σ,
∂n/∂t + ∇·(n**v**) = −s, frozen ORB-10751 stencil (SHA-256 `aa1155e0…` exact match),
comoving draw-sourced elliptic level — evolved as an initial-value problem with a
donor-cell finite-volume SSP-RK2 integrator, adaptive CFL, upstream Dirichlet wind,
open outflow faces, and **Bernoulli imposed nowhere**. Fixed physical geometry as
ORB-10935 (half-width 12, core σ = 0.75), same four winds, to T = 60; ladder 25³/33³/41³
(coarser than ORB-10935's — a declared computational bound); deterministic, byte-identical
rerun verified. Two initial conditions (ramped pure wind; wind/GP blend) at (33³, U = 0.3).

1. **G1 — no case steady within the horizon, and the verdict is explicitly
   finite-horizon.** No (U, rung) met the joint predeclared criterion (volume-RMS
   residuals < 2×10⁻³ over the final window) by T = 60; the two finest rungs agree
   categorically at every wind. But the structure of the failure is the finding: the
   **velocity residual meets its half of the criterion at every finest-rung wind**
   (5.2–5.3×10⁻⁴) — only the **density** residual fails (4.5–6.1×10⁻³). The consumption
   trough around the core is still deepening (minimum density 0.27–0.32 and falling),
   decaying at late log-slope −0.0148…−0.0173 per time unit at every wind — a
   U-independent e-folding time of ~65, comparable to the entire horizon. Every case is
   classified `decaying_slowly_not_yet_saturated`: no growing modes, no saturated
   shedding. This reads as *slow relaxation toward a steady balance*, not intrinsic
   unsteadiness — but T = 60 (≲ one e-fold, and shorter than the two lowest winds'
   box-crossing times) cannot adjudicate that.
2. **G2/G3 — executed, empty.** With no admitted steady case, the discovered speed law
   (the Theorem 1 kill this apparatus exists to deliver) and the realized wake
   comparison got no sample. The kill remains undelivered — not dodged: the gates ran
   and predeclared admission simply never triggered.
3. **G4 — the constructed branch's drag scaling did not survive the dynamics.** On the
   realized (time-averaged) flow the consumed +x momentum has drag sign at every wind
   with finest values 0.263, 0.876, 2.60, 8.11 — consumed/U = 61.8, 61.8, 61.1, 57.2,
   i.e. **linear in the wind within ~8% across a 33× sweep** (fit |∫s·v_x dV| =
   55.9·U^0.979, vs the constructed branch's 20.3·U^0.098). All finest adjacent-rung
   shifts pass the 25% convergence target. Linear-in-U drag is what momentum-flux
   capture predicts — the core eats the incoming flux at a rate ∝ nU × capture volume —
   and is the physically sensible form for a secular drag; the constructed branch's
   near-U-independence was an artifact of the imposed-Bernoulli ansatz. Ledger stays
   advective-only (no level-stress surface term supplied by the model).
4. **G5 — pass, exactly.** Pure wind, no core, advanced to T = 60 by the identical full
   time integrator: velocity and density preserved exactly, consumption at floating
   precision on every rung and wind. The dynamical Galilean null holds.
5. **Attractor uniqueness — unresolved.** The two initial conditions remain distinct at
   T = 60 (relative L² differences 0.40 velocity, 0.39 density); since neither is
   steady, this measures transient memory, not attractor multiplicity.

**Declared limits:** T = 60 shorter than the two lowest winds' box-crossing times
(finite-horizon wording throughout); bounded 25³/33³/41³ ladder with donor-cell
truncation diffusion quantified only by adjacent-rung shifts; one-sided zero-gradient
open faces may reflect nonlinear structure; density positivity floor recorded per case;
advective-only momentum surface ledger.

**Consequence and successor.** The binary the previous adjudication posed — steady state
or intrinsic unsteadiness — was the wrong shape: the dynamics returned *slow relaxation,
unresolved at horizon*. The velocity-first settling and the U-independent density decay
rate point at a specific mechanism: the trough deepens until consumption (s ∝ n) falls
to what the wind resupplies, so the balance depth and the settling time are set by the
local consumption rate, not the wind — and if the ~65 e-fold holds, a horizon of several
hundred time units should either settle every case or show the decay stalling. That is
the successor: the **extended-horizon relaxation** (filed at this adjudication, faraday,
ws_orrery) — same apparatus, T ≥ 600 (~9 observed e-folds), sectoral residuals and a
trough-saturation diagnostic predeclared, global mass budget (boundary influx vs ∫s dV →
balance) as the steady-approach signature, and the same inherited kill: any admitted
steady case's speed field is the discovered test of Theorem 1.

**Moving-source bounds studies note (kepler, ws_principia — filed with this doc).** The
sourced walls Theorem 2's confrontation needs: gravitational aberration in GR (the Carlip
cancellation), preferred-frame PPN parameters α₁/α₂ and their current bounds, moving-lens
deflection measurements, frame-dragging measurements, and gravitational Cherenkov
constraints — the note [moving-source-field-consistency](moving-source-field-consistency.md)
and [retarded-scarcity-wake](retarded-scarcity-wake.md) already demanded, now needed by
three docs.

## Related

- [shear-sourced-consumption](shear-sourced-consumption.md) — the closed system whose
  moving-source problem this doc opens; its debt 5 (non-radial flows) is exactly this
  territory, now with two exact results and a fixture program.
- [gravity-as-scarcity](gravity-as-scarcity.md) — the parent; the wind question couples to
  its open galactic-carrier question through § what sets U.
- [retarded-scarcity-wake](retarded-scarcity-wake.md) /
  [moving-source-field-consistency](moving-source-field-consistency.md) — the postulated
  moving-medium family; this doc supplies what its surviving branch demanded (an explicit
  substrate equation with derived moving-source behavior) for the elliptic-level closed
  system specifically.
- [studies/river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md) —
  GP dilation identity and the excitation reading.
- [studies/lorentz-violation-bounds](../studies/lorentz-violation-bounds.md) — the
  resonator wall and the sourced velocity scales the wind arithmetic uses.
