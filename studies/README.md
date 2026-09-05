# studies/

Sourced notes on **established physics** — the facts our theories and sims lean on. Maintained
by **kepler** (`agentbase/kepler/memory`).

## The contract

One note per fact-cluster (a bound, a measured value, an experiment lineage). Each carries
frontmatter (`title`, `status`, `created`, `updated`) and, for every load-bearing fact, a
**verifiable citation** — paper, textbook chapter, or measured value with source. House rule:
citations are checked against the actual source before being recorded; a fact that can't be
sourced right now is written `conjecture — to verify`, never stated as settled.

`theory/` docs and sim docstrings point here instead of restating physics from memory —
one place to be wrong, one place to fix.

## Notes

- [milky-way-rotation-curve](milky-way-rotation-curve.md) — measured MW circular-velocity curve
  (Eilers et al. 2019), the MOND acceleration scale, and the ORB-10075 Gaia DR3 dataset lineage.
- [chsh-bounds](chsh-bounds.md) — the classical, quantum, and measured CHSH bounds.
- [solar-system-ephemeris-precision-floor](solar-system-ephemeris-precision-floor.md) — per-planet
  Newtonian-omission residuals vs JPL Horizons 2016–2026 (the AU-scale bound), Mercury's GR
  excess, and the ORB-10093/ORB-10094 lineage.
- [scalar-gravity-ppn-constraints](scalar-gravity-ppn-constraints.md) — the PPN photon sector
  (γ, deflection, Shapiro), the Cassini bound, and the scalar-gravity lineage Nordström →
  Brans–Dicke → screened scalar-tensor (chameleon/Vainshtein).
- [gravitational-time-dilation](gravitational-time-dilation.md) — the measured clock ladder
  Pound–Rebka → Gravity Probe A → GPS → Galileo → optical clocks (10⁻¹⁸), the GM/r profile
  tests, LPI/universality bounds, and the LLR Ġ/G constancy bound.
- [river-model-and-analog-gravity](river-model-and-analog-gravity.md) — Gullstrand–Painlevé
  coordinates, the Hamilton–Lisle river model (free-fall flow, exact Schwarzschild clocks),
  and Unruh acoustic metrics / analogue gravity (excitations of a flowing medium).
- [lorentz-violation-bounds](lorentz-violation-bounds.md) — Michelson–Morley to rotating
  resonators (10⁻¹⁷–10⁻¹⁸ anisotropy), the SME frame, the CMB dipole velocity, GRB
  dispersion bounds on lattice-scale (emergent-Lorentz) violations, and GRB-polarimetry
  vacuum-birefringence bounds.
- [vortex-atoms-and-quantized-circulation](vortex-atoms-and-quantized-circulation.md) —
  the vortex-matter lineage: Kelvin's vortex atoms and the knot-theory origin, Maxwell's
  vortex cells and the 1865 removability lesson, the Bjerknes sign reversal, measured
  quantized circulation/flux (Onsager/Feynman/Vinen), fractional-vortex confinement, and
  the nuclear-electron (N-14 statistics) lesson.
- [superfluid-vacuum-and-emergent-gauge-fields](superfluid-vacuum-and-emergent-gauge-fields.md)
  — Volovik's ³He program (emergent Weyl fermions, gauge fields, metric; Fermi-point
  topological protection), what it does and doesn't deliver, and the two-fluid two-sound
  fact (Landau/Peshkov).
- [maxwell-mode-content-and-two-fluid-acoustics](maxwell-mode-content-and-two-fluid-acoustics.md)
  — Maxwell vacuum plane-wave content (two transverse polarizations, two Gauss
  constraints; Jackson §7.1–7.2, Maxwell 1865) versus two-fluid longitudinal sounds
  (Landau/Peshkov) and Helmholtz frozen vorticity; equal characteristic speeds are not
  polarizations. Comparator for the packet-Hamiltonian linearization (ORB-11219).
- [equivalence-principle-tests](equivalence-principle-tests.md) — the measured η ladder
  (Eötvös → Eöt-Wash → MICROSCOPE at 10⁻¹⁵, plus ALPHA-g antimatter free fall) and the
  composition of mass (QCD mass budget, nuclear binding energies) that makes
  inventory-coupled gravity fail it.
- [fifth-force-searches](fifth-force-searches.md) — the α–λ Yukawa exclusion ladder
  (Eöt-Wash sub-mm → LLR → planetary), the exchange-force sign systematics, the light/mass
  discriminator at λ ≫ AU, and the Fischbach 1986 / Sanders 1984 canon with the
  universality problem (radial-acceleration relation).
- [gravitational-redshift-astronomical](gravitational-redshift-astronomical.md) — the
  redshift rungs beyond the solar neighborhood: solar Fe lines (HARPS-LFC), S2/S0-2 at
  Sgr A* (GRAVITY, Do), and stacked galaxy clusters (Wojtak) with the Kaiser kinematic
  caveat — redshift tracking the dynamics-inferred potential at every measured scale.
- [cosmological-expansion-and-bound-systems](cosmological-expansion-and-bound-systems.md) —
  where expansion reaches: locally \(\Lambda\) *is* a centrifugal term (\(\omega^2=\Lambda c^2/3\),
  period 106 Gyr), so the max turnaround radius is the cosmological Hill radius (~1 Mpc for
  10¹² M⊙); the term is 2×10⁻⁴ of self-gravity at a galaxy's disk edge; Price & Romano's
  all-or-nothing barrier as a saddle-node at \(r_c\) (the orbit's valley exists, it just never
  migrates); why no energy is dissipated (static potential, no \(\dot r\) term) while global energy
  genuinely is not conserved, set against the measured inspiral ladder — solar mass loss, lunar
  tides, Hulse–Taylor, WASP-12b — where a real sink always shows up; the solar-system
  non-expansion bound (≳70×);
  the \(\dot G/G\) wall on "gravity and expansion are one phenomenon"; and the two
  near-coincidence traps — lunar recession vs \(H_0r\), galaxy size growth vs the scale factor.
- [moving-source-gravity-bounds](moving-source-gravity-bounds.md) — the moving-source walls:
  Carlip's aberration cancellation (EM exact for uniform motion, GR through (v/c)⁵), the
  preferred-frame PPN parameters α₁/α₂/α₃ and their bounds (LLR, solar spin axis, binary and
  solitary pulsars), the 2002 Jupiter-VLBI moving-lens measurement and its interpretation
  dispute, frame dragging as measured (GP-B, LAGEOS/LARES with the error-budget criticisms),
  and the Moore–Nelson gravitational-Cherenkov bounds on subluminal gravity.
- [wide-binary-selection-bias-preregistration](wide-binary-selection-bias-preregistration.md) —
  preregistered protocol (hypothesis, null, decision rule, controls, run matrix) testing whether
  Astrolabe's wide-binary selection pipeline's geometry/truncation cuts or shifted-field
  chance-alignment estimator manufacture a spurious acceleration-dependent bias on a synthetic
  Newtonian-only catalog; cites Chae 2023, Banik et al. 2024, Boufourou 2026, El-Badry, Rix &
  Heintz 2021, and Pecaut & Mamajek 2013.
- [source-side-universality-of-g](source-side-universality-of-g.md) — the wall on a
  source-strength that tracks the source's *density*: which channels discriminate (only the
  laboratory route, because every dynamical channel measures \(G_\text{eff}M\)), the
  laboratory G ladder across source-mass densities ~1.0–18.0 g/cm³ (lake water, #316
  stainless steel, mercury, tungsten alloy) agreeing to ≲10⁻³, the active/passive-mass
  lineage (Kreuzer 1968 at equal density — composition only; Bartlett & van Buren 1986 and
  Singh et al. 2023 lunar Fe/Al at 4×10⁻¹² → 3.9×10⁻¹⁴, killing the *local* variant and
  null against the *bulk* variant), the GM/M degeneracy that makes ephemeris consistency
  non-discriminating, and the PPN-β superposition-nonlinearity comparator.

## Wanted (backlog)

- Grangier–Roger–Aspect 1986 antibunching (needed by
  [theory/swirl-photon](../theory/swirl-photon/))
- Neutrality of matter (electron–proton charge cancellation bound, ~10⁻²¹) and the Skyrme
  baryon-number-as-winding citation (needed by
  [theory/two-substance-vortex-vacuum](../theory/two-substance-vortex-vacuum/))
