---
title: "Lorentz-violation bounds: Michelson–Morley to SME resonators and GRB dispersion"
status: active
created: 2026-07-12
updated: 2026-07-12
---

# Lorentz-violation bounds: Michelson–Morley to SME resonators and GRB dispersion

The measured walls around any theory with a preferred frame or a spatial microstructure:
laboratory bounds on anisotropy of c (aether-style violations) and astrophysical bounds on
energy-dependent photon dispersion (lattice-scale violations). These bound the rest-frame
question for gravity-as-scarcity in
[theory/gravity-as-scarcity](../theory/gravity-as-scarcity/) (ORB-10159).

## The velocity scales

A theory in which matter couples to a spatial substance must confront the measured motion
relative to the natural candidate frames: the solar system moves at **369.82 ± 0.11 km/s**
relative to the CMB rest frame (Planck 2018: Aghanim et al. 2020, *Astron. & Astrophys.*
641, A1), i.e. β = v/c ≈ 1.23×10⁻³, β² ≈ 1.5×10⁻⁶; Earth's orbital motion adds ±30 km/s
annually (β² ≈ 10⁻⁸); and in a Gullstrand–Painlevé inflow picture the solar river at 1 AU
runs at the local escape speed √(2GM☉/r) ≈ 42 km/s (β² ≈ 2×10⁻⁸ — derived arithmetic, not
sourced).

## Laboratory anisotropy bounds (Michelson–Morley class)

| Experiment | Bound | Source |
|---|---|---|
| Michelson–Morley 1887 (interferometer) | null at the sensitivity of Earth's 30 km/s orbital aether wind — fringes < ¼ of expected | Michelson & Morley 1887, *Am. J. Sci.* 34, 333 |
| Rotating optical resonators 2009 | Δc/c anisotropy < ~1×10⁻¹⁷ ((0.6 ± 1.2)×10⁻¹⁷) | Eisele, Nevsky & Schiller 2009, *Phys. Rev. Lett.* 103, 090401 |
| Rotating sapphire microwave resonators 2015 | anisotropy coefficient (9.2 ± 10.7)×10⁻¹⁹ | Nagel et al. 2015, *Nature Communications* 6, 8174 |

The modern framework is the Standard-Model Extension (SME; Colladay & Kostelecký 1998,
*Phys. Rev. D* 58, 116002), with measured coefficients compiled in Kostelecký & Russell
2011, *Rev. Mod. Phys.* 83, 11 (living data tables). The resonator bounds above constrain
the photon-sector anisotropy coefficients at 10⁻¹⁷–10⁻¹⁸.

**The kill arithmetic for substance couplings** (ours, flagged as derived): a medium theory
in which matter couples to the medium's rest frame at O(1) predicts anisotropies of order
β² — that is 1.5×10⁻⁶ for the CMB-frame motion, or 2×10⁻⁸ even granting full entrainment
down to the local solar inflow. Against 10⁻¹⁷–10⁻¹⁸ measured bounds, an O(1)
substance-coupled preferred frame is excluded by **9 to 12 orders of magnitude**. Only two
escapes are known: no coupling (the frame is gauge — deflationary), or matter as excitations
*of* the medium (one shared limiting speed → Michelson–Morley null by construction; see
[river-model-and-analog-gravity](river-model-and-analog-gravity.md)).

## Astrophysical dispersion bounds (lattice-scale violations)

An emergent-Lorentz-invariance theory generically breaks the invariance at its
microstructure scale as energy-dependent photon group velocity, parametrized
v/c ≈ 1 ± (E/E_QG,1) ± (E/E_QG,2)². Gamma-ray-burst timing bounds (short GRB 090510,
Fermi-LAT):

- **Linear (n = 1):** E_QG,1 > 1.2 E_Planck from the initial analysis (Abdo et al. 2009,
  *Nature* 462, 331); the dedicated follow-up strengthens the subluminal case to
  **E_QG,1 > 7.6 E_Planck** (Vasileiou et al. 2013, *Phys. Rev. D* 87, 122001).
  E_Planck = 1.22×10¹⁹ GeV.
- **Quadratic (n = 2):** E_QG,2 > 1.3×10¹¹ GeV (same Vasileiou et al. 2013 analysis) —
  eight orders of magnitude *below* the Planck energy.

**Generic lattice dispersion** (ours, flagged as derived; textbook lattice-wave algebra): a
wave hopping on a lattice of spacing a with a parity-symmetric rule has an even dispersion
relation — e.g. the 1-D chain ω = (2c/a)·sin(ka/2) = ck·[1 − (ka)²/24 + …] — so the leading
correction is **quadratic and subluminal**, δv_g/c ≈ −(ka)²/8; odd (linear) terms are
forbidden by parity. Consequences:

1. A parity-symmetric lattice evades the (Planck-exceeding) linear bounds automatically.
2. The quadratic bound translates to a **maximum lattice spacing**:
   a ≲ ħc/E_QG,2 ≈ 1.5×10⁻²⁷ m ≈ 10⁸ Planck lengths. A Planck-spaced lattice sits eight
   orders below current GRB sensitivity; any lattice coarser than ~10⁻²⁷ m is refuted.
3. A lattice with a parity-*asymmetric* hop rule acquires a linear term and is dead at any
   spacing coarser than ~E_Planck⁻¹ — the linear bounds already exceed the Planck scale.
4. Discreteness also makes the quadratic term direction-dependent (cubic anisotropy) — at
   Planck-squared suppression this sits far below all current sensitivity; but any
   *energy-independent* residual anisotropy falls under the resonator bounds above, which
   is why emergent-metric models need all species to share one medium (universality) rather
   than approximate frame-independence.

## Vacuum birefringence bounds (GRB polarimetry)

A photon sector in which the two polarization states propagate at (even slightly)
different speeds is *birefringent*: linear polarization rotates with propagation distance,
and for the energy-dependent (dimension-5, CPT-odd) case the rotation grows as E², so any
high linear polarization observed from a cosmological source washes out unless the
helicity-speed split is essentially zero. Measured wall:

- **GRB 140206A** (INTEGRAL/IBIS Compton polarimetry; redshift z = 2.739 from the optical
  afterglow): linear polarization > 28% at 90% confidence in the prompt emission, giving
  **ξ < 1 × 10⁻¹⁶** on the dimension-5 birefringence parameter — the deepest such limit
  from a cosmological source (Götz et al. 2014, *Mon. Not. R. Astron. Soc.* 444, 2776).

Interpretation for medium models (ours, flagged as derived): ξ ~ 10⁻¹⁶ means the two
transverse polarizations must see *one* medium to that fractional precision at gamma-ray
energies. A vacuum built from two components that couple differently to the two
polarization states — or whose two components carry the EM mode at two speeds — is bound
directly by this, independent of the isotropy (resonator) and dispersion (GRB timing)
walls above.

## What this binds in our corpus

For gravity-as-scarcity's rest-frame question: the lattice-as-substance (aether) branch is
excluded by the resonator bounds at 9–12 orders; the lattice-as-medium-of-excitations
branch survives with two computed conditions — a parity-symmetric hop rule (no linear
dispersion) and lattice spacing ≲ 10⁸ Planck lengths. The placement lives in
[theory/gravity-as-scarcity](../theory/gravity-as-scarcity/) (ORB-10159 section and
ledger). For the two-substance vortex vacuum
([theory/two-substance-vortex-vacuum](../theory/two-substance-vortex-vacuum/),
ORB-10160) every wall in this note binds *doubled*: two substrates supply two candidate
rest frames (each facing the resonator exclusion) and a two-component photon sector facing
the birefringence bound — kill condition B in that doc's ledger.
