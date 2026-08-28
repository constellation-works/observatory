---
title: "Moving-source gravity bounds: aberration cancellation, preferred-frame PPN, moving-lens deflection, frame dragging, gravitational Cherenkov"
status: active
created: 2026-08-28
updated: 2026-08-28
---

# Moving-source gravity bounds: aberration cancellation, preferred-frame PPN, moving-lens deflection, frame dragging, gravitational Cherenkov

The measured walls around any theory whose *moving-source* sector differs from general
relativity's: what GR itself predicts and cancels for a moving source (and at what order),
the PPN preferred-frame parameters and their current bounds, what the one moving-lens
deflection experiment actually measured, frame dragging as measured, and the gravitational
Cherenkov constraint on a subluminal gravity mode. This is the wall the wind-tunnel
fixtures' measured wake gets confronted with
([theory/moving-sources-in-the-closed-system](../theory/moving-sources-in-the-closed-system.md));
the note was demanded by
[theory/moving-source-field-consistency](../theory/moving-source-field-consistency.md) and
[theory/retarded-scarcity-wake](../theory/retarded-scarcity-wake.md) § open debts. Every
citation below was checked against the actual source (arXiv/journal listing or the paper
text) before being recorded.

## Gravitational aberration in GR and its cancellation

The classical objection (Laplace, 1805, as quoted in Carlip 2000): if gravity pointed at
the *retarded* position of a moving source with speed-of-light propagation, the resulting
aberration torque would secularly destroy orbits; Laplace concluded gravity must propagate
at ≥ 7×10⁶ c. The resolution is that the premise is wrong for both electromagnetism and GR
(Carlip 2000, "Aberration and the speed of gravity", *Phys. Lett. A* 267, 81,
[gr-qc/9909087](https://arxiv.org/abs/gr-qc/9909087) — the abstract: "By evaluating the
gravitational effect of an accelerating mass, I show that aberration in general relativity
is almost exactly canceled by velocity-dependent interactions, permitting c_g = c"):

- **Electromagnetic control case (Heaviside/Liénard–Wiechert).** The velocity-dependent
  term of the Liénard–Wiechert field *linearly extrapolates* the retarded direction, so
  the electric field of a uniformly moving charge points at the charge's **instantaneous**
  position — for uniform motion "the effects of aberration are exactly canceled" (Carlip
  2000 §2). What survives is tied to acceleration: change the motion and the field keeps
  pointing at the extrapolated position until the light cone catches up; uncanceled
  radiation damping enters at order (v/c)³.
- **General relativity.** The cancellation is *stronger*: the gravitational acceleration
  extrapolates the retarded position **quadratically** — velocity and acceleration terms
  both appear (Carlip 2000 eq. 2.5) — so uniform motion produces no O(v/c) aberration
  dipole and the uncanceled residue is pushed to radiation-reaction order, (v/c)⁵
  (quadrupole radiation), consistent with binary-pulsar orbital decay agreeing with GR.
- **The reading that matters for us.** The cancellation is a derived property of the
  specific field equations (it follows from their conservation structure), not a generic
  feature of "finite-c_g" talk: a substrate equation either *derives* its own
  velocity-dependent cancellation or eats a Laplace-scale aberration effect that the
  solar system excludes. What is settled is the absence of the naive O(v/c) lag in EM and
  GR specifically — not the behavior of every preferred-medium equation.

## Preferred-frame PPN parameters α₁, α₂, α₃

In the PPN formalism, theories that violate the strong equivalence principle can make the
outcomes of local gravitational experiments depend on the laboratory's velocity relative
to "the mean rest frame of the universe" — preferred-frame effects, governed by the PPN
parameters α₁, α₂, α₃; all three vanish identically in GR, and fully conservative
theories predict none (Will 2014, "The Confrontation between General Relativity and
Experiment", *Living Rev. Relativ.* 17, 4, [arXiv:1403.7377](https://arxiv.org/abs/1403.7377),
§3.2, §4.3.2). α₃ doubles as a conservation-law parameter: a nonzero α₃ also violates
momentum conservation. In practice the preferred frame is taken to be the CMB rest frame,
through which the solar system moves at ≈ 370 km/s — the sourced velocity scales live in
[lorentz-violation-bounds](lorentz-violation-bounds.md) § velocity scales (cross-link, not
duplicated here).

Current limits (Will 2014, Table 4, with the primary measurements alongside):

| Parameter | Limit (Will 2014 Table 4) | Effect / experiment | Primary source |
|---|---|---|---|
| α₁ | 10⁻⁴ | orbital polarization, lunar laser ranging | Will 2014 §4.3.2 |
| α₁ | 7×10⁻⁵ | orbital polarization of the pulsar–white-dwarf binary PSR J1738+0333; the direct fit is α̂₁ = −0.4⁺³·⁷₋₃.₁×10⁻⁵ (95% CL) | Shao & Wex 2012, *Class. Quantum Grav.* 29, 215018, [arXiv:1209.4503](https://arxiv.org/abs/1209.4503) |
| α₂ | ≲ 10⁻⁷ | alignment of the Sun's spin axis with the planetary angular momentum over the age of the solar system (an anomalous α₂ torque would have precessed it away) | Nordtvedt 1987, "Probing gravity to the second post-Newtonian order and to one part in 10⁷ using the spin axis of the Sun", *Astrophys. J.* 320, 871 |
| α₂ | 2×10⁻⁹ | absence of spin precession in solitary millisecond pulsars PSR B1937+21 and PSR J1744−1134; the direct bound is \|α̂₂\| < 1.6×10⁻⁹ (95% CL) | Shao et al. 2013, *Class. Quantum Grav.* 30, 165019, [arXiv:1307.2552](https://arxiv.org/abs/1307.2552) |
| α₃ | 4×10⁻²⁰ | pulsar acceleration: period-derivative statistics of 21 millisecond pulsars | Will 2014 §4.3.2 and Table 4 |

Caveat recorded by Will himself (2014 §4.3.2): the pulsar bounds involve neutron stars
with strong internal gravity, so they are strictly bounds on *strong-field analogues*
(α̂₁, α̂₂) of the PPN parameters; Will's table treats them as bounds on the standard
parameters. The frame assumed in the pulsar analyses is the CMB frame. These are the
numbers any "PPN reduction of the effective metric" must land under — a raw wind U/c is
not comparable to them until that reduction exists.

## Moving-lens deflection: the 2002 Jupiter–quasar VLBI experiment

The one direct measurement of a velocity-dependent term in light deflection by a moving
body, and a controversy over what it measured:

- **The proposal.** Kopeikin 2001 ("Testing the relativistic effect of the propagation of
  gravity by very long baseline interferometry", *Astrophys. J.* 556, L1,
  [gr-qc/0105060](https://arxiv.org/abs/gr-qc/0105060)) argued that during Jupiter's close
  passage of quasar J0842+1835 on 2002 September 8, VLBI could detect an excess time delay
  beyond the static Shapiro delay, sensitive — on his reading — to the speed of gravity.
- **The measurement.** Fomalont & Kopeikin 2003 ("The measurement of the light deflection
  from Jupiter: experimental results", *Astrophys. J.* 598, 704,
  [astro-ph/0302294](https://arxiv.org/abs/astro-ph/0302294)): with the VLBA plus
  Effelsberg at 8.4 GHz, rms position error < 10 μas, against a GR prediction at closest
  approach of 1190 μas radial (static) deflection and 51 μas tangential (retarded)
  deflection in the direction of Jupiter's motion, they measured the retarded term at
  **0.98 ± 0.19 of the GR value**. Kopeikin and Fomalont announced this as a measurement
  of the speed of gravity, c_g = c to ~20% (Will 2014 §4.1.3 records the claim as
  "measured the correction term to about 20 percent"; the widely reported figure
  c_g/c = 1.06 ± 0.21 does not appear in the ApJ abstract and is left here unverified
  against a primary source).
- **The other reading.** Several authors argued the measured v/c term does not depend on
  the propagation speed of gravity at all: at first order in v/c only Jupiter's uniform
  motion matters, and in Jupiter's rest frame the field is static, so c_g is irrelevant —
  the term depends on the speed of *light* (Will 2003, "Propagation speed of gravity and
  the relativistic time delay", *Astrophys. J.* 590, 683,
  [astro-ph/0301145](https://arxiv.org/abs/astro-ph/0301145); Samuel 2003, "On the speed
  of gravity and the v/c corrections to the Shapiro time delay", *Phys. Rev. Lett.* 90,
  231101, [astro-ph/0304006](https://arxiv.org/abs/astro-ph/0304006), who further found
  the v/c effects "too small to have been measured" in that experiment). Will's PPN-class
  calculation makes the useful positive statement: the velocity-dependent delay term
  *does* carry a dependence on **α₁**, but the existing α₁ bounds (table above) "already
  far exceed the capability of the Jupiter VLBI experiment" (Will 2014 §4.1.3, which also
  records Kopeikin's continued opposition to this interpretation).
- **Static-limit anchor.** The best measured γ — Cassini's (2.1 ± 2.3)×10⁻⁵ on γ − 1 —
  and the light-deflection ladder are already sourced in
  [scalar-gravity-ppn-constraints](scalar-gravity-ppn-constraints.md) § measured values
  of γ (cross-link, not duplicated here).

The net for a wake theory: the only moving-lens datum is a 19% measurement of a 51 μas
velocity term consistent with GR, and the sharpest interpretation of it is as a
(non-competitive) bound on α₁ — the preferred-frame table above remains the binding wall.

## Frame dragging as measured

The physical O(GM·v/c²r) gravitomagnetic sector, measured two independent ways. In PPN
form the Lense–Thirring precession of a gyroscope is
Ω_LT = −½(1 + γ + ¼α₁)·(J − 3n(n·J))/r³ (Will 2014 eq. 69) — note the 1/r³ falloff and
that the coefficient itself carries the preferred-frame parameter α₁; the geodetic
precession is Ω_G = (γ + ½)·v × ∇U (Will 2014 eq. 70).

| Experiment | Result | Source |
|---|---|---|
| **Gravity Probe B** (four cryogenic gyroscopes, 642 km polar orbit, guide star IM Pegasi) | geodetic drift −6601.8 ± 18.3 mas/yr (GR: −6606.1) — 0.28%; **frame-dragging drift −37.2 ± 7.2 mas/yr (GR: −39.2)** — a 19% measurement | Everitt et al. 2011, *Phys. Rev. Lett.* 106, 221101, [arXiv:1105.3456](https://arxiv.org/abs/1105.3456) |
| **LAGEOS/LAGEOS II nodes** (laser ranging + CHAMP/GRACE Earth-gravity models; combined nodal precession ~31 mas/yr) | 99% of the GR Lense–Thirring prediction, claimed total error 5–10% ("a 10 percent confirmation of GR" — Will 2014 §4.4.1) | Ciufolini & Pavlis 2004, *Nature* 431, 958 |
| — published criticism | realistic 1σ total error ≈ **19%** with EIGEN-GRACE02S (geopotential systematics 4–9% by model, plus ~13% from secular zonal-harmonic variation over the 11-year span) — the 5% claim judged too optimistic | Iorio 2006, *J. Geod.* 80, 128, [gr-qc/0412057](https://arxiv.org/abs/gr-qc/0412057); Will 2014 §4.4.1 notes "some authors stressed the importance of adequately assessing systematic errors in the LAGEOS data" |
| **LARES + LAGEOS + LAGEOS II** (LARES launched 2012 near the supplementary inclination; GRACE model GGM05S) | μ = 0.994 ± 0.002 (1σ formal) ± 0.05 (systematic), μ = 1 being GR | Ciufolini et al. 2016, *Eur. Phys. J. C* 76, 120, [arXiv:1603.09674](https://arxiv.org/abs/1603.09674) |

Honest state of the ladder: GP-B's 19% and the satellite-ranging results (claimed 5%,
disputed to ~19% for 2004; claimed 5% systematics for 2016, with the same critic lineage
contesting the error budgets) agree with GR; nothing measures the gravitomagnetic sector
better than the few-percent-to-20% level. A theory with **no** gravitomagnetic sector at
all is nonetheless dead against any of these rows; a theory with a wake-generated
substitute must reproduce Ω_LT's magnitude, its 1/r³ falloff, and its spin-source
character where these experiments measure it.

## Gravitational Cherenkov radiation: the subluminal-gravity wall

Moore & Nelson 2001 ("Lower bound on the propagation speed of gravity from gravitational
Cherenkov radiation", *JHEP* 0109:023, [hep-ph/0106220](https://arxiv.org/abs/hep-ph/0106220)):
if gravity propagates *slower* than light, ultra-high-energy cosmic rays would radiate
gravitational Cherenkov radiation and lose their energy in transit; the observed arrival
of cosmic rays then bounds the deficit:

- **Galactic origin** (conservative): c − c_g < **2×10⁻¹⁵** c.
- **Extragalactic origin**: c − c_g < **~2×10⁻¹⁹** c.

Scope, from the paper's own assumptions: the bound applies to a **conventionally coupled**
gravitational mode (graviton coupled to matter with ordinary gravitational strength) that
is subluminal; it says nothing about c_g > c, and applying it to an *extra* substrate mode
requires knowing that mode's matter coupling and dispersion — the scoping already recorded
in [theory/moving-source-field-consistency](../theory/moving-source-field-consistency.md).
The complementary superluminal/equal-speed anchor — GW170817/GRB 170817A's
\|c_gw/c − 1\| ≲ 10⁻¹⁵ — is sourced in
[scalar-gravity-ppn-constraints](scalar-gravity-ppn-constraints.md) (cross-link).

## The velocity scales

Sourced in [lorentz-violation-bounds](lorentz-violation-bounds.md) § velocity scales
(CMB dipole 369.82 ± 0.11 km/s, Earth's ±30 km/s orbital motion, the ~42 km/s solar river
at 1 AU) — cross-link, not duplicated here.

## What this binds in our corpus

- [theory/moving-sources-in-the-closed-system](../theory/moving-sources-in-the-closed-system.md)
  — the closed system provably sources no vector potential, and its measured wake
  (ORB-10935/ORB-10937/ORB-10938) is the moving-source prediction. This note is the
  external wall its Theorem 2 confrontation was waiting for: the preferred-frame table
  (α₁, α₂ — what the owed PPN reduction must land under), the moving-lens datum and its
  α₁ reading, and the frame-dragging rows the wake's δv field must face where GEM is
  measured. The doc's `conjecture — to verify` rows citing "the studies note" now have
  their sourced targets; upgrading them is kepler's reconciliation job in the change-set
  that ingests this note.
- [theory/moving-source-field-consistency](../theory/moving-source-field-consistency.md)
  — its Carlip-cancellation row and Cherenkov row (both `conjecture — to verify`, "No
  studies/ note yet") are now sourced here: the cancellation is real, order-counted
  (uniform motion exactly canceled in EM, through (v/c)⁵-suppressed residuals in GR), and
  a property of the specific field equations — exactly the control case its Branch C
  analysis assumes.
- [theory/retarded-scarcity-wake](../theory/retarded-scarcity-wake.md) — § open debts
  explicitly demands this note before any observational fit; its Cherenkov-cone row and
  preferred-frame rows point at the Moore & Nelson and PPN sections above.

Not carried here: disk-lopsidedness statistics (demanded by the same open-debts list) —
that is a separate observational fact-cluster and still owed.
