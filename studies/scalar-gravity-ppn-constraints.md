---
title: "Scalar gravity, the PPN photon sector, and the Cassini bound"
status: active
created: 2026-07-12
updated: 2026-07-12
---

# Scalar gravity, the PPN photon sector, and the Cassini bound

The established-physics wall any scalar theory of gravity runs into: the photon sector. This
note carries the parametrized post-Newtonian (PPN) machinery, the measured values of γ, and
the lineage of scalar gravity from Nordström to the screened scalar-tensor theories — the
constraints the gravity-as-scarcity model is confronted with in
[theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md) (ORB-10156).

## The two weak-field potentials and γ

The static weak-field metric of *any* metric theory can be written (isotropic coordinates)

> ds² = −(1 + 2Φ/c²) c²dt² + (1 − 2γΦ/c²) δᵢⱼ dxⁱdxʲ,  Φ = −GM/r

Two distinct potentials: Φ in g₀₀ (the "time-time" potential — clock rates, and the *entire*
driver of slow-motion massive-particle dynamics, ẍ = −∇Φ independent of γ) and the spatial
potential γΦ in gᵢⱼ (the "space-space" potential — how much proper space a mass adds around
itself). The PPN parameter **γ measures how much space curvature a unit rest mass produces**;
GR predicts γ = 1 exactly. (Will 2014, *Living Reviews in Relativity* 17:4, "The
Confrontation between General Relativity and Experiment", §3.2 — the standard PPN reference
throughout this note.)

Slow massive particles never probe γ (their dynamics is Φ-only, suppressed by v²/c²).
**Photons probe Φ and γΦ equally** — every light-sector observable carries the factor
(1 + γ)/2:

- **Light deflection** by a mass M at impact parameter b:
  α = (1 + γ)/2 · 4GM/(c²b) — at the solar limb, (1 + γ)/2 × 1.75″.
  The γ = 0 value, 2GM/(c²b) = 0.875″, is the historical "Newtonian"/Soldner half-deflection
  (a corpuscle falling in the potential alone).
- **Shapiro time delay** (radar echoes passing near the Sun run late; proposed as the "fourth
  test" by Shapiro 1964, *Phys. Rev. Lett.* 13, 789): Δt = (1 + γ)/2 × the GR value,
  logarithmically peaked at superior conjunction.

A note on sign conventions used here and in the theory doc: with Φ = −GM/r < 0, weak-field GR
(γ = 1) makes clocks near a mass tick *slow* by GM/c²r and puts *more* proper space near a
mass — the radial proper distance between r₁ and r₂ exceeds r₂ − r₁ by ∫(GM/c²r)dr (the
embedding-funnel excess). Both effects have the same magnitude and the photon sector needs
both, at that ratio, to give γ = 1.

## Measured values of γ

| Observable | Result | Source |
|---|---|---|
| 1919 eclipse deflection | 1.98″ (Sobral) and 1.61″ (Príncipe) — consistent with 1.75″, excluding 0 and the 0.875″ half-value | Dyson, Eddington & Davidson 1920, *Phil. Trans. R. Soc. A* 220, 291 |
| VLBI deflection (radio, ~10⁵ quasar observations) | γ − 1 = (−0.8 ± 1.2) × 10⁻⁴ | Lambert & Le Poncin-Lafitte 2011, *Astron. & Astrophys.* 529, A70; summarized in Will 2014 §3.4.1 |
| **Cassini Shapiro delay** (Doppler tracking through 2002 solar conjunction) | **γ − 1 = (2.1 ± 2.3) × 10⁻⁵** | Bertotti, Iess & Tortora 2003, *Nature* 425, 374 |

The Cassini bound is the binding one: any theory whose photon sector departs from γ = 1 at
more than a few × 10⁻⁵ is refuted. A theory predicting γ = 0 (half deflection, half delay) or
no coupling at all (zero deflection, zero delay) is off by |γ − 1| ≥ 1 — four to five orders
of magnitude outside the allowed band.

## Scalar gravity: the canonical lineage and how it died

- **Nordström 1913** (*Ann. Phys.* 42, 533) — the canonical Lorentz-invariant scalar theory
  of gravity, the best pre-GR competitor. Einstein & Fokker 1914 (*Ann. Phys.* 44, 321)
  showed it is equivalent to a **conformally flat** metric theory, g = φ²η. Conformal
  rescalings preserve null geodesics, so light in Nordström's theory travels the straight
  lines of flat space: **zero light deflection** (effectively γ = −1 in the deflection
  factor). It also predicts a perihelion *retreat* at −1/6 the GR rate (about −7″/century
  for Mercury; Deruelle 2011, *Gen. Rel. Grav.* 43, 3337). The 1919 eclipse measurement
  killed it. The general lesson (Will 2014 §2): a pure scalar cannot feed the spatial metric
  with the right sign and ratio; only a tensor field does.
- **Scalar-tensor (Brans & Dicke 1961**, *Phys. Rev.* 124, 925**)** — gravity = tensor +
  scalar with coupling ω; the scalar's share dilutes the spatial potential:
  γ = (1 + ω)/(2 + ω). The Cassini bound forces **ω ≳ 40,000** (Will 2014 §3.4.2) — the
  scalar's fraction of gravity is < ~2.5 × 10⁻⁵ in the solar system. Unscreened
  scalar-tensor theories are cornered to be observationally indistinguishable from GR.
- **Screened scalar-tensor** — the modern escape: keep an O(1) scalar at large
  scales/low densities while hiding it locally, so γ → 1 where Cassini looks.
  Two mechanism families:
  - **Chameleon** (Khoury & Weltman 2004, *Phys. Rev. Lett.* 93, 171104; symmetron variant:
    Hinterbichler & Khoury 2010, *Phys. Rev. Lett.* 104, 231301) — the scalar's effective
    mass (or coupling) depends on the ambient matter density/potential; dense environments
    give it a short range ("thin shell"), suppressing the scalar force locally.
  - **Vainshtein** (Vainshtein 1972, *Phys. Lett. B* 39, 393) — derivative self-interactions
    of the scalar dominate near sources, suppressing the scalar's gradient inside a large
    "Vainshtein radius".
- **Family-level constraints beyond PPN.** A pure scalar carries only a "breathing"
  polarization, no transverse tensor modes — the GW170814 three-detector polarization
  analysis strongly favors pure tensor over pure scalar or pure vector (Abbott et al. 2017,
  *Phys. Rev. Lett.* 119, 141101). And the relativistic-MOND precedent TeVeS (Bekenstein
  2004, *Phys. Rev. D* 70, 083509) — the existence proof that a scalar-driven galactic
  modification *can* be dressed with a tensor sector to get light bending right — is itself
  severely constrained by the GW170817/GRB 170817A speed bound |c_gw/c − 1| ≲ 10⁻¹⁵
  (Abbott et al. 2017, *Astrophys. J. Lett.* 848, L13).

One more measured anchor used by the theory doc's time-flow correspondence: gravitational
redshift between heights, z = gΔh/c² — clocks genuinely run slow deeper in a potential
(Pound & Rebka 1960, *Phys. Rev. Lett.* 4, 337).

## What this binds in our corpus

Any theory in `theory/` whose weak-field content is a single scalar potential on flat space —
gravity-as-scarcity as currently stated is one — inherits this wall: its photon sector is
either absent (Nordström's fate, zero deflection), half-strength (γ = 0), or wrong-signed,
and all of those sit ≥ 4 orders of magnitude outside the Cassini band. The only known viable
completions are screened scalar-tensor structures with γ ≈ 1 locally. The confrontation and
the derived verdicts live in
[theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md) (ORB-10156 section and ledger).
