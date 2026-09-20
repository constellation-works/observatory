---
title: "Fifth-force searches: Yukawa constraints from the laboratory to the kiloparsec"
status: active
created: 2026-07-12
updated: 2026-07-12
---

# Fifth-force searches: Yukawa constraints from the laboratory to the kiloparsec

The established-physics wall around any proposed new finite-range interaction: a century of
searches parameterized as a Yukawa correction to the Newtonian potential,

> V(r) = −(G M m / r) [1 + α e^(−r/λ)]

with dimensionless strength α and range λ — the standard frame of the α–λ exclusion plot
(Fischbach & Talmadge, *The Search for Non-Newtonian Gravity*, Springer 1999; Adelberger,
Heckel & Nelson 2003, *Annu. Rev. Nucl. Part. Sci.* 53, 77). This note carries the measured
limits, two structural facts about mediated forces, and the two canonical episodes (Fischbach
1986; Sanders 1984) that the S2-disjunction derivation leans on in
[theory/two-substance-vortex-vacuum](../theory/two-substance-vortex-vacuum/) (ORB-10161).

## The measured α–λ ladder

| Range probed | Bound | Source |
|---|---|---|
| sub-mm (inverse-square-law torsion balances) | gravity-strength Yukawa (\|α\| = 1) excluded for λ > 56 μm (2007), pushed to λ > 38.6 μm (2020), 95% confidence | Kapner et al. 2007, *Phys. Rev. Lett.* 98, 021101; Lee et al. 2020, *Phys. Rev. Lett.* 124, 101101 (Eöt-Wash) |
| Earth–Moon (~10⁸ m) | α < 5.9 × 10⁻¹¹ near the peak-sensitivity range λ ≈ a_Moon/2 ≈ 1.9 × 10⁸ m | lunar laser ranging; Merkowitz 2010, *Living Rev. Relativity* 13, 7 |
| planetary (10¹⁰–10¹¹ m) | α ≲ 10⁻⁹–10⁻¹⁰ from the classic model-independent ephemeris analysis; modern ephemerides reach ~10⁻¹²–10⁻¹³ | Talmadge, Berthias, Hellings & Standish 1988, *Phys. Rev. Lett.* 61, 1159; Iorio 2007 (arXiv:gr-qc/0507041) |
| composition-dependent coupling, any λ ≳ Earth-orbit scale | η(Ti, Pt) ≲ 3 × 10⁻¹⁵ (MICROSCOPE), applied to the fifth force's charge-to-mass differences | [equivalence-principle-tests](equivalence-principle-tests.md) |
| λ ≫ 1 AU, any mediator that does not bend light | \|α\| ≲ 1.2 × 10⁻⁵ from Cassini's γ (see "the light/mass discriminator" below) | derived below from Bertotti, Iess & Tortora 2003 via [scalar-gravity-ppn-constraints](scalar-gravity-ppn-constraints.md) |

Direct inverse-square-law tests never reach kiloparsec ranges: for λ ≫ solar system, a Yukawa
is locally an exact rescaling of G for all massive-body dynamics, and ephemerides cannot see
it. The kpc column of the α–λ plot is instead closed by the two structural facts below.

## Two structural facts about mediated forces

**Exchange-force sign systematics.** Standard field theory of static exchange forces:
scalar exchange is attractive between like charges; vector exchange is repulsive between like
charges and attractive between opposites (the systematics are laid out in Fischbach &
Talmadge 1999, ch. 2 — this is textbook, not conjecture). Consequence for rotation curves: an
attractive (α > 0) Yukawa *adds* force at short range that dies at long range, so its boost
factor [1 + α e^(−r/λ)(1 + r/λ)] decreases monotonically with r — it can only produce a
*falling* boost. A rotation-curve boost that *rises* with radius requires α < 0: a repulsive
short-range component that nearly cancels gravity inside λ (so the laboratory G is the
screened value G_∞(1 + α)) and releases it beyond — which at the mediator level means a
**vector**, coupled to some conserved charge.

**The light/mass discriminator (our arithmetic, on measured anchors).** For λ ≫ 1 AU the
Yukawa factor is fully active across the solar system, so every massive-body determination of
the Sun's GM (planetary ephemerides) measures G_∞(1 + α)M. But a scalar mediator does not
deflect light (conformal invariance of null geodesics — Nordström's lesson, see
[scalar-gravity-ppn-constraints](scalar-gravity-ppn-constraints.md)) and a vector mediator
does not couple to the uncharged photon: light propagates on G_∞M alone. Deflection and
Shapiro delay computed with the ephemeris-calibrated GM are then off by the factor
1/(1 + α), which reads as an effective PPN γ:

> γ_eff − 1 = −2α/(1 + α)  →  Cassini's \|γ − 1\| ≤ 2.3 × 10⁻⁵ forces \|α\| ≤ 1.2 × 10⁻⁵

for *any* non-metric-coupled Yukawa with λ ≫ AU, independent of what it couples to. The
massive spin-2 escape (a mediator that does bend light) runs into the vDVZ discontinuity:
massive-graviton exchange yields γ = 1/2 in its active range (van Dam & Veltman 1970,
*Nucl. Phys. B* 22, 397; Zakharov 1970, *JETP Lett.* 12, 312) — equally dead against Cassini
unless Vainshtein-screened, which is no longer a Yukawa (screened completions:
[scalar-gravity-ppn-constraints](scalar-gravity-ppn-constraints.md)).

## The Fischbach episode (canon: how composition-coupled fifth forces die)

Fischbach et al. 1986 (*Phys. Rev. Lett.* 56, 3, "Reanalysis of the Eötvös experiment")
proposed a ~100 m-range force coupled to hypercharge from apparent composition-dependent
residuals in the 1922 Eötvös data. The proposal launched the modern fifth-force program;
within a few years the dedicated torsion-balance and free-fall experiments (Eöt-Wash and
successors) found no effect, and by the early 1990s the original signal was dead — the
retrospective is Fischbach & Talmadge 1999. Two durable lessons: composition-coupled forces
are the *easiest* kind to kill (every material pair is an instrument), and the modern α–λ
limits above are that program's descendants.

## The kiloparsec rung: Sanders 1984 and the universality problem

Sanders 1984 (*Astron. Astrophys.* 136, L21, "Anti-gravity and galaxy rotation curves")
implemented exactly the α < 0 structure above: a low-mass **vector** boson carrying a
repulsive Yukawa that nearly balances gravity below galactic scales (characterized by a
coupling α and a fixed length r₀), producing nearly flat spiral rotation curves from 10 to
100 kpc from baryons alone. Its measured failure mode is the **universality problem**: one
fixed r₀ cannot fit galaxies whose disks span two orders of magnitude in size — the observed
mass discrepancy sets in at a fixed *acceleration*, not a fixed length (Sanders & McGaugh
2002, *Annu. Rev. Astron. Astrophys.* 40, 263). The modern sharpening is the radial
acceleration relation: across 153 SPARC galaxies and 2693 points, the observed acceleration
is a single tight function of the baryonic acceleration alone (McGaugh, Lelli & Schombert
2016, *Phys. Rev. Lett.* 117, 201101; the SPARC sample: Lelli, McGaugh & Schombert 2016,
*Astron. J.* 152, 157). Any fixed-length-scale account must either reproduce that
organization or be killed by it.

## What this binds in our corpus

The S2-as-fifth-force branch of the two-substance vortex vacuum
([theory/two-substance-vortex-vacuum](../theory/two-substance-vortex-vacuum/), ORB-10161):
its required (α ≈ −0.68, ξ₂ ≈ 5.25 kpc) sits in the open window of the direct ISL ladder but
is closed by the composition row (if charge-coupled), the sign systematics (if α > 0), and
the light/mass discriminator (any mediator) — the derivation and verdicts live in the theory
doc. The fixed-length-scale universality exposure applies equally to the parent scarcity
form's fixed β (adjudication: ORB-10168/ORB-10169). The gravitational-redshift face of the
same disjunction is in
[gravitational-redshift-astronomical](gravitational-redshift-astronomical.md).
