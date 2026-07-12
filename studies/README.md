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

## Wanted (backlog)

- Lense–Thirring frame-dragging magnitude/falloff (needed by
  [theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md))
- Grangier–Roger–Aspect 1986 antibunching (needed by
  [theory/swirl-photon](../theory/swirl-photon.md))
- Neutrality of matter (electron–proton charge cancellation bound, ~10⁻²¹) and the Skyrme
  baryon-number-as-winding citation (needed by
  [theory/two-substance-vortex-vacuum](../theory/two-substance-vortex-vacuum.md))
