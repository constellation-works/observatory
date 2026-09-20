---
title: "Source-side universality of G: laboratory determinations across source densities, active/passive mass, and the GM degeneracy"
status: active
created: 2026-08-28
updated: 2026-08-28
---

# Source-side universality of G

The measured wall around any theory whose **source strength depends on a property of the
source body other than its mass** — specifically, on the source's *density*. This note
exists because [theory/shear-sourced-consumption](../theory/shear-sourced-consumption/)
§ closure (a) derives, in closed form, that a flux-type amplitude coupling forces
\(G_\text{eff} = \kappa^2\rho_\text{body}/(24\pi n^2)\) — exterior gravity proportional to
the source's bulk density, independent of its mass — and rests one leg of its exclusion on
"measurement says no". That leg needed sourcing. Every citation below was checked against
the actual source (journal abstract, arXiv/ar5iv full text, or the agency data page) before
being recorded.

The headline: the discrimination is **almost entirely a laboratory result**, and the
astronomical channels that look like they should settle it mostly cannot. Stating which is
which is most of the value of this note.

## The two hypotheses, kept apart

Two readings of "source strength tracks density" behave very differently against the data,
and the literature's bounds land on them unevenly:

- **H_local** — every mass element sources with a strength set by *its own* material
  density: \(g \propto \int \rho(\mathbf{x})^{1+p}\,d^3x\) for \(p \neq 0\). A body's
  interior composition then matters, and its center of *active* mass separates from its
  center of *passive* mass.
- **H_bulk** — the coefficient is set by the whole body's *mean* density
  \(\bar\rho = M/V\), as the surface-flux matching in shear-sourced-consumption § closure (a)
  actually derives: \(G_\text{eff} = G_0(\bar\rho/\rho_0)^p\), with \(p=1\) the flux
  coupling's prediction. Internal structure is invisible; only whole-body mean density
  counts.

H_local is killed several orders of magnitude harder than H_bulk, and by a different
experiment. Both are killed.

## Which observable channels discriminate, and which cannot

**Purely dynamical channels cannot.** Every celestial determination of a body's
gravitational influence — Kepler's third law, spacecraft tracking, ephemeris fitting —
measures the product \(GM\) (the standard gravitational parameter \(\mu\)), never \(G\) and
\(M\) separately. JPL's own planetary physical-parameters table states the direction of
inference explicitly: "Mass values were updated from current estimates of GM," and "Bulk
density values (and uncertainties) were computed based on updated mass values and computed
volumes"
([JPL SSD, Planetary Physical Parameters](https://ssd.jpl.nasa.gov/planets/phys_par.html)).
So the planetary masses and the planetary bulk densities are *outputs* of assuming a
universal \(G\), not independent measurements that could contradict it. An
\(H_\text{bulk}\) universe with \(G_\text{eff}(\bar\rho)\) and correspondingly rescaled
masses reproduces every purely dynamical observable exactly. **Ephemeris consistency across
the solar system's bulk-density range is not, by itself, evidence against a
density-dependent source law.**

**Free-fall (equivalence-principle) tests cannot.** Eötvös through MICROSCOPE bound the
universality of *response* to an external field — the ratio of passive gravitational to
inertial mass of the *test* body, to \(10^{-15}\)
([equivalence-principle-tests](equivalence-principle-tests.md)). A density-dependent source
law is a statement about the *field-generating* side and leaves the test-body side
untouched; the η ladder is silent on it. This is the standard active/passive split and it
has to be respected when quoting "the equivalence principle excludes it".

**Laboratory \(G\) determinations do.** This is the one channel that breaks the \(GM\)
degeneracy, because the source body's mass is established *non-gravitationally* — weighed
against the kilogram, i.e. inertially/passively calibrated — and its geometry machined and
metrologically characterized. Comparing experiments whose source masses are made of
different materials is therefore a direct comparison of \(G_\text{eff}\) at different
source densities.

**Active/passive-mass tests do, for H_local.** A material-dependent active mass makes a
compositionally asymmetric body exert a net force on itself; the resulting self-acceleration
is observable in lunar laser ranging.

**Additivity/nonlinearity tests bound a different thing** (how gravity superposes rather
than what sets its strength) and are recorded below for the doc's separate superposition
question.

## Laboratory G across source-mass densities

Material densities below are nominal handbook values; they enter only as *ratios*, and no
conclusion here is sensitive to them at the 10% level. Each row's source-mass material and
\(G\) value was read from the paper itself.

| Determination | Source (field) mass | ρ_source (g/cm³) | G (10⁻¹¹ m³ kg⁻¹ s⁻²) | rel. unc. |
|---|---|---|---|---|
| Hubler, Cornaz & Kündig 1995 (lake) | lake water displacing air | ~1.0 | 6.669 ± 0.005 (112 m); 6.678 ± 0.007 (88 m) | ~8×10⁻⁴ |
| Gundlach & Merkowitz 2000 (UWash) | four #316 stainless-steel spheres, ≈8.140 kg each | ~8.0 | 6.674215 ± 0.000092 | 1.4×10⁻⁵ |
| Schlamminger et al. 2006 (UZur) | two 7.5 t tanks, ≈6760 kg mercury each in steel | ~13.5 (Hg), composite body | 6.674252(109)(54) | 1.8×10⁻⁵ |
| Rosi et al. 2014 (LENS) | 24 Inermet180 cylinders (95% W, 3.5% Ni, 1.5% Cu), ≈516 kg | ~18.0 | 6.67191 ± 0.00099 | 1.5×10⁻⁴ |
| CODATA 2022 recommended | — | — | 6.67430 ± 0.00015 | 2.2×10⁻⁵ |

Sources, checked:

- **Lake water, ρ ≈ 1.0.** B. Hubler, A. Cornaz & W. Kündig, "Determination of the
  gravitational constant with a lake experiment: New constraints for non-Newtonian gravity",
  *Phys. Rev. D* **51**, 4005 (1995),
  [doi:10.1103/PhysRevD.51.4005](https://doi.org/10.1103/PhysRevD.51.4005). From the
  abstract: "A high-precision balance was used to measure the weight difference of two 1-kg
  stainless steel masses as a function of the variable water level of a pumped-storage lake.
  Water-level changes up to 44 m produced a maximum weight difference of 1390 μg, which
  could be measured with a resolution of 0.5 μg. … the measurement directly yields the
  gravitational interaction between the test masses and the locally moved mass (water and
  air). … They yield values for G of (6.669±0.005)×10⁻¹¹ m³ kg⁻¹ s⁻² at 112 m and
  (6.678±0.007)×10⁻¹¹ m³ kg⁻¹ s⁻² at 88 m, both in agreement with laboratory
  determinations."
- **#316 stainless steel, ρ ≈ 8.0.** J. H. Gundlach & S. M. Merkowitz, "Measurement of
  Newton's constant using a torsion balance with angular acceleration feedback", *Phys. Rev.
  Lett.* **85**, 2869 (2000), [gr-qc/0006043](https://arxiv.org/abs/gr-qc/0006043). The
  attractor spheres were "machined from the same selected stock of ultrasonically tested
  #316 stainless steel", average diameter 124.89 mm, mass ≈8.140 kg;
  G = (6.674215 ± 0.000092)×10⁻¹¹, ≈13.7 ppm.
- **Mercury, ρ ≈ 13.5.** S. Schlamminger et al., "Measurement of Newton's gravitational
  constant", *Phys. Rev. D* **74**, 082001 (2006),
  [gr-qc/0609027](https://arxiv.org/abs/gr-qc/0609027). Beam balance with "two moveable
  field masses … each with a mass of 7.5 t", stainless-steel tanks each holding ≈6760 kg of
  mercury; G = 6.674252(109)(54)×10⁻¹¹ (16.3 ppm statistical, 8.1 ppm systematic).
- **Tungsten alloy, ρ ≈ 18.0.** G. Rosi et al., "Precision measurement of the Newtonian
  gravitational constant using cold atoms", *Nature* **510**, 518 (2014),
  [arXiv:1412.7954](https://arxiv.org/abs/1412.7954); apparatus described in the companion
  proceedings [PMC4173270](https://pmc.ncbi.nlm.nih.gov/articles/PMC4173270/): 24 cylinders
  of "Inermet180, a sintered alloy of 95% W, 3.5% Ni and 1.5% Cu", total ≈516 kg, in a
  hexagonal pattern around the Raman beams. G = 6.67191(99)×10⁻¹¹, 150 ppm.
- **CODATA.** *CODATA Recommended Values of the Fundamental Physical Constants: 2022*,
  [arXiv:2409.03787](https://arxiv.org/abs/2409.03787): G = 6.67430(15)×10⁻¹¹ m³ kg⁻¹ s⁻²,
  relative standard uncertainty 2.2×10⁻⁵, from 16 input values, with "the same 3.9 expansion
  factor applied to their uncertainties in 2018 to reduce their inconsistencies to an
  acceptable level".

### The bound, and the honesty about it

Write \(G_\text{eff} = G_0(\rho/\rho_0)^p\); the flux coupling predicts \(p = 1\).

- **Strict H_bulk reading** (compact, *homogeneous* source bodies only, so that "the body's
  mean density" is unambiguous): stainless steel (≈8.0) vs tungsten alloy (≈18.0), a 2.25×
  density ratio. The two determinations differ fractionally by
  (6.674215 − 6.67191)/6.673 = **3.5×10⁻⁴**, giving \(|p| \le 3.5\times10^{-4}/\ln 2.25 =
  \mathbf{4.3\times10^{-4}}\). The mercury-tank determination sits between them and agrees
  with the steel one to 6×10⁻⁶, but it is a *composite* body (steel shell plus mercury fill),
  so it is consistency, not a clean bulk-density lever.
- **H_local / continuum reading** (each mass element sourcing at its own material density —
  the reading under which a lake's water layer is admissible): lake water (≈1.0) vs
  stainless steel (≈8.0), an 8× ratio. The lake and laboratory values agree to
  ≲8×10⁻⁴, within the lake experiment's own ~7.5×10⁻⁴ uncertainty, giving
  \(|p| \lesssim 8\times10^{-4}\). Water vs tungsten alloy is an 18× ratio and formally
  tighter (\(\lesssim 3\times10^{-4}\)), uncertainty-limited by the lake.

Either way **\(|p| \lesssim 10^{-3}\), against a predicted \(p = 1\)** — the flux coupling
is excluded by roughly three orders of magnitude. Stated without the log fit: under
\(G_\text{eff} \propto \rho\), a water-sourced determination of \(G\) would come out ~18×
below a tungsten-sourced one — an 1800% discrepancy where ≤0.08% is observed.

The honest caveat, and why the bound is quoted conservatively: **the modern \(G\)
determinations are mutually inconsistent** at roughly the 5×10⁻⁴ level — that is exactly
why CODATA inflates their uncertainties by 3.9. The bound above therefore uses the *observed
scatter itself* as the allowed discrepancy rather than any experiment's quoted error bar. It
is a bound limited by unmodeled systematics in \(G\) metrology, not by statistics, and it is
conservative for precisely that reason: whatever is causing the ~5×10⁻⁴ spread, it is
manifestly not a factor-of-two effect tracking source density.

A second caveat, recorded because it bites a naive version of the argument: within any
*single* \(G\) experiment the source density is fixed, so no experiment tests this
internally. The lever is entirely cross-experiment, and it therefore inherits every
cross-experiment systematic. That is a real limitation of the channel, and it is still three
orders of magnitude more than enough.

## Active and passive gravitational mass

Newton's third law for gravitating bodies requires *active* gravitational mass (what
generates the field) to equal *passive* gravitational mass (what the field pulls on). A
source law that depends on anything but mass generically breaks it.

- **Kreuzer 1968.** L. B. Kreuzer, "Experimental measurement of the equivalence of active
  and passive gravitational mass", *Phys. Rev.* **169**, 1007 (1968),
  [doi:10.1103/PhysRev.169.1007](https://doi.org/10.1103/PhysRev.169.1007). From the
  abstract: "A homogeneous Teflon cylinder, which is completely immersed in a mixture of
  dibromomethane and trichloroethylene prepared to have about the same density as Teflon,
  was slowly moved back and forth in this liquid. The resultant time-varying gravitational
  field due to the density difference between the solid Teflon and the displaced liquid was
  detected by a Cavendish-type torsion balance … The time-varying gravitational field
  detected by the balance was extrapolated to the condition of neutral buoyancy. The
  fractional density difference between the Teflon and the liquid required to produce this
  field was found to be Δρ/ρ = (1.2±4.4)×10⁻⁵. This upper bound of approximately 5×10⁻⁵ is
  compared to 10⁻³, the best value that can be deduced from other experiments."

  **What it does not constrain — the point that matters here.** The null is taken *at the
  condition of neutral buoyancy*, i.e. with the Teflon and the liquid at **equal density by
  construction**. Kreuzer therefore compares two materials of the same density and different
  composition (fluorocarbon vs bromo-/chlorocarbon). It is a clean composition test at fixed
  density and gives **exactly zero leverage on a density-dependent source strength** —
  under either H_local or H_bulk its predicted signal is identically null. Quoting Kreuzer
  against a density-dependent \(G\) would be a mis-citation.
- **Bartlett & van Buren 1986.** D. F. Bartlett & D. Van Buren, "Equivalence of active and
  passive gravitational mass using the moon", *Phys. Rev. Lett.* **57**, 21 (1986),
  [doi:10.1103/PhysRevLett.57.21](https://doi.org/10.1103/PhysRevLett.57.21). Using lunar
  laser ranging and a model of the lunar interior, the ratios of active to passive mass for
  iron and aluminium agree to **4×10⁻¹²**.
- **Singh et al. 2023.** V. V. Singh, J. Müller, L. Biskupek, E. Hackmann & C. Lämmerzahl,
  "Equivalence of Active and Passive Gravitational Mass Tested with Lunar Laser Ranging",
  *Phys. Rev. Lett.* **131**, 021401 (2023),
  [arXiv:2212.09407](https://arxiv.org/abs/2212.09407). A new limit of **3.9×10⁻¹⁴** for
  Al vs Fe, "about 100 times better than that of Bartlett and Van Buren". The mechanism, as
  the paper states it: the Moon's center of mass is offset from its center of figure by
  ≈1.98 km, so its Al-rich crust and Fe-rich interior are compositionally asymmetric; an
  active/passive inequality then produces a *self-force* on the Moon whose tangential
  component changes the lunar orbital angular velocity, which LLR range residuals bound.

  **What these do and do not constrain.** They bound a *material-dependent* active mass —
  and because aluminium (ρ ≈ 2.70) and iron (ρ ≈ 7.87) differ by 2.9× in density, they bound
  **H_local** devastatingly: \(p = 1\) would make the Fe and Al active-to-passive ratios
  differ by O(1), i.e. ~10¹³ times the measured limit. They are, however, **null by
  construction against H_bulk**: the Moon has a single mean density, so a source law keyed to
  whole-body mean density predicts no internal asymmetry and no self-force. The lunar tests
  are the sharpest knife in this note and they cut only one of the two hypotheses. H_bulk is
  left to the laboratory route above.

## Ephemeris-level consistency: what it is and is not worth

Solar-system bodies span a wide range of bulk densities — from Saturn at 0.6871 ± 0.0002
g/cm³ to Earth at 5.5134 ± 0.0003 g/cm³, an 8.0× span (JPL SSD planetary physical
parameters; Mercury 5.4289, Venus 5.243, Mars 3.9340, Jupiter 1.3262, Uranus 1.270, Neptune
1.638). It is tempting to say that ephemerides fitted with one universal \(G\) across that
span already exclude a density-dependent source law.

**They do not, on their own** — for the reason given above: those densities are computed
*from* masses that were themselves computed from \(GM\) under the assumption of a universal
\(G\). The dynamics constrains \(\mu = G_\text{eff}M\) per body and nothing else; any
\(G_\text{eff}(\bar\rho)\) can be absorbed into a rescaled \(M\). The solar system's role in
this argument is as a *consistency* check downstream of the laboratory result, not as an
independent discriminator.

There is a residual channel worth naming rather than overclaiming: under H_bulk the system
\(\mu = G_0(\bar\rho/\rho_0)^pM\), \(\bar\rho = M/V\), with \(V\) measured independently
(radio occultations, limb fitting), is *closed* — it determines \(M\) per body without a
laboratory \(G\), and yields a different mass scale from the standard one. Those masses
would then have to be consistent with independent interior physics: mean-density-driven
composition models, moments of inertia, tidal Love numbers, and the giant planets'
hydrogen/helium budgets. Whether that closure is already excluded quantitatively is
**`conjecture — to verify`** here — it needs an interior-modeling source this note does not
carry, and the laboratory bound above makes it unnecessary for the exclusion that prompted
the note.

## Superposition nonlinearity (the separate question)

Recorded here because [theory/shear-sourced-consumption](../theory/shear-sourced-consumption/)
§ closure (d) asks for it: the measured wall on *nonlinearity in the superposition of
gravity* is the PPN parameter β. From lunar laser ranging combined with the Cassini γ
determination — J. G. Williams, S. G. Turyshev & D. H. Boggs, "Progress in Lunar Laser
Ranging Tests of Relativistic Gravity", *Phys. Rev. Lett.* **93**, 261101 (2004),
[gr-qc/0411113](https://arxiv.org/abs/gr-qc/0411113):

- Nordtvedt parameter η = 4β − γ − 3 = **(4.4 ± 4.5)×10⁻⁴**
- **β − 1 = (1.2 ± 1.1)×10⁻⁴**, using Cassini's γ − 1 = (2.1 ± 2.3)×10⁻⁵

**Scope, stated precisely.** β bounds the second-order metric nonlinearity at
post-Newtonian order in the solar system — the leading correction to linear superposition,
and it is *analytic* in the small parameter. A screening family that is non-analytic as its
small parameter → 0 (a \(D^q\) law with \(q<1\), unbounded \(d\ln A/dD\)) is qualitatively
outside the PPN expansion rather than merely bounded by it, so β is the right *comparator*
but converting it into a numerical bound on such a family requires first fixing the model's
\(D \leftrightarrow \sigma\) normalization — which the parent family's carrier question
leaves open. The bound is sourced; the conversion is not, and remains owed.

## What this binds in our corpus

- [theory/shear-sourced-consumption](../theory/shear-sourced-consumption/) § closure (a) —
  the flux-type amplitude coupling's *external* leg. The laboratory route is the
  discriminating one (source-mass densities ~1.0 to ~18.0 g/cm³, agreement ≲10⁻³ ⟹
  \(|p| \lesssim 10^{-3}\) vs the predicted \(p = 1\)); the lunar active/passive tests kill
  the local variant at 3.9×10⁻¹⁴ and are null against the bulk variant; ephemeris
  consistency alone discriminates nothing because every dynamical channel measures
  \(G_\text{eff}M\). The doc's `conjecture — to verify` on this passage is upgraded in the
  change-set that lands this note.
- [theory/shear-sourced-consumption](../theory/shear-sourced-consumption/) § closure (d) —
  the PPN-nonlinearity comparator for a non-analytic small-D superposition family: β − 1 =
  (1.2 ± 1.1)×10⁻⁴, with the normalization gap stated above.
- [equivalence-principle-tests](equivalence-principle-tests.md) — cross-link, and a boundary:
  the η ladder constrains the *test-body* side and does not reach a source-side law. The two
  notes are complementary, not redundant.
- [fifth-force-searches](fifth-force-searches.md) — cross-link. A density-dependent
  \(G_\text{eff}\) is not a Yukawa fifth force (no new range, no new composition charge in
  the H_bulk reading), so the α–λ exclusion ladder does not cover it; the lake experiment
  appears in both notes but for different reasons (there, the 1/r² test at 88–112 m).

## Open debts

- **BIPM torsion-balance source-mass material.** The BIPM determinations (Quinn et al. 2013,
  *Phys. Rev. Lett.* **111**, 101102) sit at the high end of the modern \(G\) spread and
  would widen the cross-experiment lever, but the source-mass material could not be read
  from an accessible copy of the paper; nothing here relies on it. `conjecture — to verify`.
- **The full CODATA input table.** Only four determinations are tabulated above — the ones
  whose source-mass material was verified directly. The remaining twelve CODATA inputs are
  not characterized here.
- **Interior-model closure under H_bulk** — flagged `conjecture — to verify` in the
  ephemeris section above.
