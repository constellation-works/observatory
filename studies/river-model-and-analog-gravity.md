---
title: "The river model (Gullstrand–Painlevé) and analog gravity (acoustic metrics)"
status: active
created: 2026-07-12
updated: 2026-07-12
---

# The river model (Gullstrand–Painlevé) and analog gravity (acoustic metrics)

Two pieces of established physics that make "space flows into masses" a precise statement
rather than a picture: the Gullstrand–Painlevé (GP) form of the Schwarzschild geometry and
its physical elaboration as the *river model*; and Unruh's acoustic metrics, the canonical
demonstration that excitations of a flowing medium propagate on an effective Lorentzian
geometry. These are the canonical families the dynamical reading of gravity-as-scarcity is
placed against in [theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md) (ORB-10159).

## Gullstrand–Painlevé coordinates and the river model

The Schwarzschild geometry in GP coordinates (Painlevé 1921, *C. R. Acad. Sci. (Paris)* 173,
677; Gullstrand 1922, *Ark. Mat. Astron. Fys.* 16(8), 1):

> ds² = −c²dt² + (dr + v(r) dt)² + r²dΩ²,  with v(r) = √(2GM/r)

Same geometry as Schwarzschild — a coordinate transformation, not a different theory. Its
reading (Hamilton & Lisle 2008, "The river model of black holes", *Am. J. Phys.* 76, 519;
arXiv:gr-qc/0411060): flat space "flows" radially inward with the Newtonian escape velocity
v = √(2GM/r); local physics is special relativity in the frame comoving with the flow;
objects move through the flowing space per SR while the space itself falls in. Load-bearing
facts, each verifiable from the line element:

- **The flow free-falls.** v(r) = √(2GM/r) is exactly the speed of an observer falling from
  rest at infinity: ½v² = GM/r. The river obeys Newtonian energy conservation in the flat
  background — it accelerates down the potential it represents.
- **A static clock dilates by the flow speed.** Setting dr = dΩ = 0: dτ² = (1 − v²/c²)dt²,
  so √(−g₀₀) = √(1 − v²/c²) = √(1 − 2GM/c²r) — *exactly* the Schwarzschild time dilation. In
  the river reading, gravitational time dilation *is* SR time dilation of a clock swimming
  upstream at v(r).
- **The horizon is where the river reaches c**: v(r_s) = c at r_s = 2GM/c², and inside it
  the flow is superluminal relative to infinity (nothing local exceeds c relative to the
  river). Regular at the horizon; the constant-t spatial slices are flat.
- **Flux arithmetic** (ours, from the line element — flagged as derived, not sourced): the
  volume flux through a shell is 4πr²v(r) ∝ r^(3/2), *growing* outward. A GP river with
  incompressible density is therefore not a flux-conserving flow with a point sink: in a
  steady state, volume must be destroyed *throughout* the region (sink density
  ∝ r^(−3/2)), predominantly at large radius per shell (∝ r^(1/2) per unit radius). A
  flux-conserving point-sink flow would instead force v ∝ 1/r², which is *not* the GP
  profile and yields the wrong time dilation (∝ 1/r⁴ rather than the measured GM/c²r — see
  [gravitational-time-dilation](gravitational-time-dilation.md)).
- **The caution the source itself carries:** Hamilton & Lisle stress the river is a
  coordinate dressing of Schwarzschild — nothing observable "moves"; in pure GR the flow
  field is gauge and only the geometry it encodes is physical. Treating the river as a
  physical medium is an *addition* to GR, not a reading of it.

## Acoustic metrics and analog gravity

Unruh 1981 ("Experimental black-hole evaporation?", *Phys. Rev. Lett.* 46, 1351): sound
waves in an irrotational barotropic fluid with flow velocity **v** and sound speed c_s
propagate exactly as a massless scalar field on the effective ("acoustic") metric

> ds² ∝ −(c_s² − v²)dt² − 2**v**·d**x** dt + d**x**²

The standard modern reference is Barceló, Liberati & Visser 2011, "Analogue Gravity",
*Living Rev. Relativity* 14:3. Load-bearing facts:

- **Excitations of a moving medium see a Lorentzian geometry.** For phonons, "being carried
  by the flow" is not an interaction with a coupling constant — a phonon *is* a disturbance
  of the medium, so advection is constitutive. This is the canonical answer to "why would
  matter be dragged by flowing space": it is dragged if and only if it is an excitation *of*
  the space, not a foreign body *in* it.
- **Constant c_s + GP flow = Schwarzschild.** If the medium's propagation speed is uniform
  and the flow has the free-fall profile v = √(2GM/r), the acoustic line element is exactly
  the GP form above, i.e. exactly the Schwarzschild geometry: a sonic horizon where v = c_s
  (Unruh's sonic black hole). All effects usually attributed to the spatial potential
  (γΦ — deflection toward the mass, Shapiro *delay*) are then supplied by flow drag, with
  no refractive-index gradient at all.
- **Lorentz invariance is emergent and low-energy only.** All excitations of one medium
  share one limiting speed c_s, so no experiment *made of the excitations* detects uniform
  motion relative to the medium at leading order — a Michelson–Morley null by construction.
  The invariance breaks at the medium's microstructure scale, appearing as high-frequency
  dispersion (see [lorentz-violation-bounds](lorentz-violation-bounds.md)).
- **The dynamics is not GR's.** Analog metrics reproduce kinematics (wave propagation on a
  fixed background); the medium's flow obeys fluid equations, not Einstein's equations. An
  analog model owes its own account of *why* the flow has the GR-matching profile.

## What this binds in our corpus

The dynamical ("river") reading of gravity-as-scarcity is a member of exactly this family:
its clock sector works only if the lattice inflow has the free-fall profile (GP), and its
matter coupling works only in the excitation (analog-gravity) reading. The derivation and
verdicts live in [theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md)
(ORB-10159 section and ledger).
