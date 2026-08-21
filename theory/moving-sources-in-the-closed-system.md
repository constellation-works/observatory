---
title: "Moving sources in the closed system: the substrate wind, exactly"
status: exploratory
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

**Current verdict:** analytic, awaiting its lattice fixture. All algebra below is verified
symbolically (sympy script attached to the wind-tunnel task filing); under the house rule
the theorem rows stay `untested` until the cataloged apparatus measures them
(precedent: [moving-source-field-consistency](moving-source-field-consistency.md), which
holds decisive-on-paper algebra to the same standard). The wind-tunnel lattice task is
predeclared both ways below.

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
   existence question only the lattice can answer).
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
| Steady irrotational flow of the closed system around a uniformly moving mass has exactly isotropic speed \|v\|² = U² + 2c²σ; the wake is confined to the direction field (Theorem 1) | untested | Closed-form global Bernoulli (§ Theorem 1), consumption-law-independent; symbolically verified (sympy, attached to the wind-tunnel filing). Awaiting the cataloged fixture: speed-isotropy gate G1, predeclared kill on converged anisotropy |
| A clock comoving with the moving mass reads 1 − U²/2c² − GM/c²r — no first-order ether-drift clock anomaly; wind dilation is exactly SR's | untested | Corollary of Theorem 1 in the excitation reading (readings and dilation identity: [river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md), [lorentz-violation-bounds](../studies/lorentz-violation-bounds.md)). Second-order cross terms unexamined (PPN territory) |
| The pure-wind state (no source) is an exact steady solution with exactly zero consumption | untested | Uniform flow has zero strain (§ Theorem 1.4, symbolically checked); null-control gate G4 |
| The boosted-GP field is not a solution of the closed system — residual (U·∇)v_GP; the steady wake differs from GR's moving-source river at O(U·v_GP), and the GR speed dipole 2U·v_GP is forbidden (Theorem 2) | untested | Symbolic residual and dipole checks (§ Theorem 2). Wake-structure gate G2 measures the realized direction field against the boost comparator |
| The closed system has no gravitomagnetic sector; reproducing tested g₀ᵢ phenomenology (moving-lens deflection, frame dragging, preferred-frame PPN α₁/α₂) from emergent wake dynamics is an open obligation with existing external bounds | conjecture — to verify | Structural (no vector source in the counting mechanic); the external bounds await the moving-source studies note this doc's program files (the note [moving-source-field-consistency](moving-source-field-consistency.md) § open debts already demanded) |
| Consumed momentum has no bookkeeping; the wake makes the gap observable (possible secular drag on moving sources) | conjecture | New named debt (§ consumed momentum). Momentum-budget gate G3 measures the wake's asymmetry in lattice units; physical normalization requires the unfixed substrate-inertia scale |
| The local wind U at real bodies is O(local orbital/infall speeds) if the relevant fields are river-carried, putting photon-sector wake effects at O(10⁻³) relative scale for the Sun | conjecture | Arithmetic over sourced velocity scales ([lorentz-violation-bounds](../studies/lorentz-violation-bounds.md) § velocity scales); contingent on the open galactic-carrier question; kill test executable only after G2 + the studies note |

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
