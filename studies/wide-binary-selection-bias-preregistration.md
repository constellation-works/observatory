---
title: "Wide-binary selection-bias preregistration: geometry, truncation, and chance-alignment calibration"
status: active
created: 2026-09-05
updated: 2026-09-05
---

# Wide-binary selection-bias preregistration

A methodological question, not a discovery claim: can Astrolabe's own wide-binary selection
pipeline — the same one behind
[gaia-wide-binaries-low-acceleration](gaia-wide-binaries-low-acceleration.md)'s stellar-scale
null — manufacture a spurious acceleration-dependent offset, or a miscalibrated
chance-alignment rate, out of a synthetic catalog that is Newtonian by construction? This note
freezes the hypothesis, decision rule, controls, and run matrix **before** any synthetic
experiment is run, per [policy.md](../policy.md)'s gate-card discipline. The gate is
[gates/wide-binary-selection-bias-control](../gates/wide-binary-selection-bias-control.json);
the claim registry is
[theory/wide-binary-selection-methodology](../theory/wide-binary-selection-methodology/).

## Scope — what this is and is not

- **Is:** a preregistered calibration check of an apparatus (Astrolabe's selection + estimator
  code), run offline on synthetic data, evaluating whether *known* selection-design choices
  (not the ORB-11217 completeness bug, already fixed) can bias the statistic the real analysis
  reports.
- **Is not:** an observational discovery claim, a new Gaia download, a gravity fit, or an
  assertion that the ORB-10753 footprint's Newtonian-consistent verdict is wrong. It does not
  touch `theory/gravity-as-scarcity` or `theory/two-substance-vortex-vacuum` — no claim in
  either family is created, blocked, or reopened by this protocol.
- **Boundary:** this document specifies the recipe; a later Orrery task builds and runs the
  fixture (§ Cross-repo contract). It consumes versioned Astrolabe functions as a dependency
  and does not edit Astrolabe. Offline and CPU-bounded: synthetic catalogs only, no network
  call, no live Gaia TAP query.

## Why this hypothesis, and why now

Astrolabe's `select_wide_pairs` applies, in order: per-star quality cuts (RUWE, parallax S/N,
G-mag limit, local-volume parallax floor), a fixed angular window (θ ∈ [1.5″, 1°]), a projected
physical-separation window (s ∈ [0.5, 50] kAU, computed from θ × distance), an escape-speed
proper-motion gate (mass- and distance-dependent), and — for the chance-alignment control — a
shifted secondary catalog compared at the same cuts
(`src/astrolabe/analysis/wide_binaries.py`, astrolabe commit `90f5b58`, read directly for this
protocol rather than re-derived from memory). None of these cuts is uniform across the sky in a
real survey: photometric completeness, crowding, and astrometric quality vary with Galactic
latitude and field density, while θ and s couple through the *distance-dependent* conversion
s = θ · d. A cut that is angularly uniform (θ window) is not physically uniform (s window) once
the population's distance distribution varies with sky position — exactly the kind of coupling
that can turn an angularly neutral truncation into an acceleration-dependent one, since g_N is
set by s and M_tot together.

This is not a new concern in this literature. Boufourou 2026 (arXiv:2608.24556, "Estimator
forensics for the wide-binary gravity test") shows, for a *different* mechanism (eccentricity
correction interacting with undetected hierarchical triples), that a purely Newtonian universe
run through a realistic estimator recovers an effective γ = 1.08–1.13 — roughly half the
claimed anomaly — from estimator artifacts alone, and preregisters its own protocol for Gaia
DR4 for exactly this reason. That paper's mechanism (eccentricity × triple contamination) is
explicitly **not** the mechanism this protocol tests (geometry × truncation × chance-alignment
calibration); it is cited here as the precedent that establishes the *class* of concern is
real and has already cost a claimed detection its footing once, not as evidence for our
specific hypothesis. If this protocol's pilot instead finds that the geometry/truncation
channel reproduces an effect at a similar scale to Boufourou's contamination channel, that
would be a second, independent estimator-artifact finding; if it finds nothing, this is a
calibration/replication result for Astrolabe's apparatus, not a new claim about nature.

## The four confound classes (kept separate; no assumed sign)

The task naming this protocol is explicit that these must not be conflated, and that the
protocol must not presuppose which direction any bias points:

1. **Candidate completeness defects — out of scope, already closed.** ORB-11217 found and
   fixed a genuine completeness bug (a raw-RA prefilter that was not a valid spherical bound,
   plus underspecified shifted-catalog semantics), landed at astrolabe commit `90f5b58` with an
   independent SkyCoord oracle and 87 passing tests. This protocol does **not** reopen that
   question as a hypothesis; it only re-runs an independent oracle as a **regression control**
   (`wbsel-candidate-oracle-regression`) on the specific footprints used here (nonuniform,
   RA-wrap, polar), since those are geometries ORB-11217's own fixtures may not have exercised
   identically.
2. **Intentional selection-design bias — the hypothesis under test.** The θ/s window,
   brightness cap, and PM-escape gate are all *specified as intended* (not bugs); the question
   is whether their interaction with a nonuniform sky population biases ṽ(g_N). Arms R1
   (§ Run matrix).
3. **Chance contamination / shifted-field miscalibration.** The shifted-field estimator's own
   accuracy at recovering a *known* contamination rate, independent of whether the primary
   bias statistic fires. Arms R3.
4. **Forward-model assumptions.** The photometric mass–luminosity relation (Pecaut & Mamajek
   2013 piecewise fit), the eccentricity prior, and isotropic-orientation projection in
   `newtonian_mock_pairs` are assumptions of the *comparator*, not the pipeline under test. This
   protocol's synthetic "truth" catalog uses the same assumptions the comparator uses (so it
   cannot by itself indict the comparator's physics) but adds realistic per-star measurement
   scatter (parallax and PM errors, RUWE) that the comparator does not carry — isolating
   whether *measurement-driven* mass/velocity scatter, not the comparator's dynamical
   assumptions, is what couples to geometry. A comparator-physics audit (thermal vs. flat
   eccentricity, isotropic vs. anisotropic orientation) is out of scope here; Astrolabe's
   existing `sensitivity_table` already exercises the contested-choice axis operationally.

No arm of this protocol assumes the sign of any bias; the decision rule (§ below) is symmetric
in `|B_i|`.

## Primary hypothesis and null

Let ṽ_recovered(g_N) be the pipeline's output on a synthetic catalog run through the full
selection chain (quality cuts, θ/s window, PM-escape gate, on a nonuniform footprint), and let
ṽ_comparator(g_N) be Astrolabe's own operational comparator (`newtonian_mock_pairs` +
`binned_vtilde`, the same one ORB-10753's real analysis reports against). Define the per-bin
primary bias statistic

    B_i = median(ṽ_recovered)_i − median(ṽ_comparator)_i

and the secondary diagnostic

    S_i = median(ṽ_recovered)_i − median(ṽ_truth)_i

where ṽ_truth is the same synthetic population's pairs with *no* observational selection
applied (physical binary membership only) — S isolates selection-induced distortion from
comparator mismatch; B is what an operational analysis would actually see and report.

- **H1 (primary hypothesis).** Under the nonuniform-footprint, zero-injected-effect arm (R1),
  at least one populated g_N bin (n ≥ 5 pairs) shows |B_i| ≥ 0.04 in median ṽ, reproducibly
  across the predeclared seed ladder (§ Uncertainty), and/or the shifted-field estimator
  R_chance falls outside its predeclared tolerance on a known injected contamination fraction.
- **H0 (null).** Every populated bin under R1 (and its cap/footprint variants) satisfies
  |B_i| < 0.04 within the seed-to-seed bootstrap uncertainty, and R_chance recovers every
  injected contamination fraction within its predeclared tolerance band.

Both are falsifiable in either direction: H1 does not predict low-g excess or deficit
specifically, only that *some* bin's deviation clears the predeclared bar.

## Effect-size threshold — where 0.04 comes from

The threshold must be meaningful for the discrimination this protocol actually serves: is a
geometry/truncation artifact large enough to explain, or contribute to, the contested
low-acceleration literature? Two anchors, both already in the corpus or sourced above:

- Chae 2023 (arXiv:2305.04613; *ApJ* 952, 128) reports an effective gravitational boost
  interpretable as γ_eff ≈ 1.4 at the lowest accelerations; translated to a velocity-ratio
  statistic (ṽ ∝ v_circ,eff ∝ √γ), that is a ~18% offset in median ṽ.
  Banik et al. 2024 (*MNRAS* 527, 4573) report a Newtonian result at high significance on the
  same class of data, i.e. a real offset (if any) is bounded well below that 18% figure.
- Boufourou 2026 (arXiv:2608.24556) finds a *pure estimator artifact* (no injected physics)
  recovers γ ≈ 1.08–1.13 — a ~4–6% offset in the equivalent ṽ statistic — from the
  eccentricity/triple channel alone.

Setting the primary decision threshold at **0.04 in median ṽ** (≈4%) puts it at the low end of
Boufourou's demonstrated artifact-floor scale: a geometry/truncation effect at or above this
size would be scientifically actionable (comparable to a channel already shown to move a
literature verdict), while a clean result below threshold means this specific channel does not
by itself account for effects at the scale the literature disputes. This is one predeclared
primary threshold; § Positive control also reports the protocol's realized minimum-detectable
effect so the threshold's power is not assumed.

## Generative population (frozen recipe)

Extends Astrolabe's own `make_synthetic_star_field` / `newtonian_mock_pairs` (already used for
its offline tests) with the sky nonuniformity those functions do not model:

1. **Binary population.** Draw from `newtonian_mock_pairs`' existing model exactly
   (log-uniform true semi-major axis, thermal eccentricity prior — `BASELINE_ECC_PRIOR` —
   isotropic orientation, uniform mass in [0.2, 1.5] M_sun per component) so the dynamical
   truth is identical to the operational comparator's own assumptions (§ confound class 4).
2. **Sky placement (the nonuniformity under test).** Instead of a single field center, place
   pairs and field stars over a footprint with:
   - a **declination-dependent quality gradient**: RUWE and parallax fractional error scale
     with `1 + 0.5·|sin(dec − dec_0)|` (a stand-in for latitude-dependent crowding/systematics;
     labeled a **model assumption, not a sourced physical crowding law** — the qualitative
     shape, not the coefficient, is what this pilot needs);
   - an **anisotropic density gradient**: field-star surface density rising linearly by ×3 from
     one edge of the footprint to the other (stand-in for a real density gradient toward the
     Galactic plane);
   - a **fixed apparent-G truncation** (`g_mag_max = 18`, matching `BASELINE_CUTS`) applied
     after distance-dependent apparent magnitude, so the *effective* absolute-magnitude (hence
     mass) completeness limit varies with the local distance distribution across the footprint.
3. **Measurement scatter.** Parallax and PM errors drawn from the quality-gradient model above
   (not zero, unlike the existing `make_synthetic_star_field` fixture which uses fixed small
   errors); RUWE drawn from a distribution whose median tracks the same gradient.
4. **Contamination (for R3).** A predeclared fraction of field-star pairs planted at random
   sky positions with parallax/PM consistent with chance alignment (not physical pairs), at
   0%, 5%, 10%, and 20% of the true-pair count.
5. **Injected effect (for R4).** A deterministic additive offset to `dv_kms` for true pairs
   with g_N below the second bin edge, of predeclared amplitude 0.02, 0.05, or 0.10 in ṽ units
   — a known, exactly-quantified signal for the power calculation, not a physical model.

## Independent candidate-pair oracle

Per realization, an independent brute-force implementation using
`astropy.coordinates.SkyCoord.search_around_sky` (the same class of oracle ORB-11217's own
execution summary reports building) re-derives the candidate set at each footprint (equatorial
baseline, RA-wrap, polar) and is diffed against Astrolabe's `_radius_candidates` output. This
is a **regression control on ORB-11217's fix**, evaluated separately from the bias statistic
(`wbsel-candidate-oracle-regression`; § confound class 1) — a disagreement here indicts
Astrolabe's completeness, not this protocol's geometry/truncation hypothesis.

## Sample cuts

Baseline cuts are Astrolabe's own `BASELINE_CUTS` (RUWE < 1.4, ϖ/σ_ϖ ≥ 10, G < 18, ϖ ≥ 5 mas,
θ ∈ [1.5″, 3600″], s ∈ [0.5, 50] kAU, 3σ parallax consistency, 3× escape-speed PM gate, RV diff
≤ 20 km/s), used unmodified so results are directly comparable to the operational pipeline.
Contested-choice variants (RUWE < 1.2, flat eccentricity prior) are exercised only via
Astrolabe's existing `sensitivity_table`, not repeated here.

## Sky rotations / RA-wrap / polar controls

Three field placements, each carrying the full generative recipe above:

- **Equatorial baseline** — RA 180°, Dec +40°, r = 25° (matches ORB-10753's real footprint for
  direct comparability).
- **RA-wrap** — RA 0° ± 15°, Dec +40°, r = 15° (straddles the 360°/0° boundary).
- **Polar** — Dec +85°, r = 10° (near-pole convergent meridians).

## Shifted-field estimator — cap ladder and isotropic/no-cap controls

- **Cap ladder** (max_stars): 2000 (heavy), 8000 (operational default), None (uncapped) —
  applied to the equatorial-baseline footprint only (R1 family); other footprints use the
  operational default.
- **Shift ladder** for `chance_alignment_rate`: the operational default (`ra_shift_deg=0.5`)
  plus 2.0° and 5.0°, to check the estimator is not shift-magnitude-sensitive on a nonuniform
  footprint (a shift-dependent R_chance at fixed true contamination would itself be a
  miscalibration finding).
- **Isotropic/no-cap negative control (R0):** uniform sky density, uniform quality (no
  gradient), max_stars=None, zero contamination, zero injected effect — the fully-null arm this
  protocol's own machinery must pass cleanly, or the synthetic framework itself (not Astrolabe)
  is suspect.

## Finite run matrix

| Run | Purpose | Population | Footprint | max_stars | Contamination | Injected effect | Seeds |
|---|---|---|---|---|---|---|---|
| R0 | Negative control | isotropic, uniform quality | equatorial | None | 0% | none | 5 |
| R1-baseline | Primary test | nonuniform gradient | equatorial | 8000 | 0% | none | 5 |
| R1-uncapped | Cap isolation | nonuniform gradient | equatorial | None | 0% | none | 5 |
| R1-heavycap | Cap stress | nonuniform gradient | equatorial | 2000 | 0% | none | 5 |
| R2-wrap | RA-wrap control | nonuniform gradient | RA-wrap | 8000 | 0% | none | 3 |
| R2-polar | Polar control | nonuniform gradient | polar | 8000 | 0% | none | 3 |
| R3-5 | Chance-alignment calibration | nonuniform gradient | equatorial | 8000 | 5% | none | 3 |
| R3-10 | Chance-alignment calibration | nonuniform gradient | equatorial | 8000 | 10% | none | 3 |
| R3-20 | Chance-alignment calibration | nonuniform gradient | equatorial | 8000 | 20% | none | 3 |
| R4-0.02 | Power floor (diagnostic) | nonuniform gradient | equatorial | 8000 | 0% | 0.02 | 3 |
| R4-0.05 | Power (primary) | nonuniform gradient | equatorial | 8000 | 0% | 0.05 | 3 |
| R4-0.10 | Power (primary) | nonuniform gradient | equatorial | 8000 | 0% | 0.10 | 3 |

47 total realizations. Each is a single synthetic-catalog generation plus one pass of the
existing Astrolabe pipeline over a few thousand to a few tens of thousands of synthetic stars —
vectorized numpy/cKDTree work, no network, no fitting loop; the whole matrix is expected to run
in minutes, not hours, on a single core (an Orrery task should record the actual wall time as
part of its own evidence, not assume this estimate).

Seeds (shared across runs that specify 5 or 3): `[7, 11, 23, 42, 101]`, taking the first *k*
for a *k*-seed run. Seed 42 matches Astrolabe's own `newtonian_mock_pairs` default for
continuity with the existing test suite.

## Uncertainty method

Primary uncertainty on each B_i (and R_chance) is the **realization bootstrap**: the spread
(median ± 1.4826×MAD) of the statistic across the run's seed list, which captures
population-realization and measurement-scatter variance the way repeated independent synthetic
universes would. Astrolabe's own within-sample per-bin error (1.4826×MAD/√n, already computed
by `binned_vtilde`) is retained and reported as a secondary/diagnostic uncertainty, since it
does not capture footprint-to-footprint systematic scatter and is not the basis for the
decision rule.

## Decision rule (predeclared)

- **R0 sanity gate.** Must show |B_i| below 1.5× its own seed-to-seed uncertainty in every
  populated bin, and R_chance consistent with zero injected contamination, before R1's result
  is trusted — a failure here indicts the synthetic framework, not Astrolabe.
- **R1 family (primary).** PASS (no geometry/truncation artifact at the predeclared scale) iff
  |B_i| < 0.04 in every populated bin for R1-baseline, R1-uncapped, R1-heavycap, R2-wrap, and
  R2-polar, using the realization-bootstrap uncertainty to judge reproducibility (a single-seed
  excursion above 0.04 that does not survive the bootstrap spread does not fire H1). FAIL
  (protocol's H1 supported) if any of those arms clears 0.04 reproducibly (median |B_i| across
  seeds ≥ 0.04 with the bootstrap band excluding zero).
- **Cap isolation.** If R1-baseline fails but R1-uncapped does not (or vice versa), the cap is
  implicated as a contributing factor and reported separately from the geometry/truncation
  verdict.
- **R3 (chance-alignment calibration).** PASS iff R_chance is within ±0.05 absolute of the true
  5% contamination fraction, and within ±25% relative of the true 10%/20% fractions, at every
  shift-ladder value and every footprint tested.
- **R4 (power).** The protocol is judged adequately sensitive iff the primary bias statistic
  flags (|B_i| ≥ 2× its seed-to-seed uncertainty in the affected bins) the 0.05 and 0.10
  injected arms in ≥ 80% of seeds. The 0.02 arm is diagnostic only, expected to under-power at
  this sample size, and is not a pass/fail gate.
- Any registry status change (untested → supported/mixed/refuted) happens in the same
  commit as whichever Orrery task lands this fixture's results, per house rule; this
  preregistration commit leaves every claim `untested`.

## Cross-repo contract (principia → Orrery)

**Astrolabe pin.** Commit `90f5b58` (ORB-11217 landed), package version `0.1.0`
(`astrolabe/pyproject.toml`). Any Orrery fixture consuming this protocol should record the
actual commit/version it ran against as evidence metadata (it may drift from this pin; that
drift itself is worth recording, not silently absorbed).

**Functions to evaluate** (`src/astrolabe/analysis/wide_binaries.py`, read directly for this
protocol, not reimplemented from memory):

- `select_star_quality`, `select_wide_pairs` — the pipeline under test (§ confound class 2).
- `chance_alignment_rate` — the shifted-field estimator (§ confound class 3).
- `newtonian_mock_pairs`, `binned_vtilde` — the operational comparator (§ confound class 4).
- `make_synthetic_star_field` — the existing offline-fixture generator this protocol's
  generative recipe extends with sky nonuniformity (§ Generative population).
- `sensitivity_table` — reused unmodified for the contested-choice axis, not re-derived.

**New code the Orrery fixture must supply** (not present in Astrolabe today, and out of scope
to add there per this task's boundary): the nonuniform-footprint generator (§ Generative
population steps 2–5), the independent SkyCoord oracle, the realization-bootstrap aggregator,
and the run-matrix driver (§ Finite run matrix). None of this requires editing Astrolabe;
all of it consumes Astrolabe's public functions as a versioned dependency.

**I/O contract.** Input: none external (the generator is self-contained, seeded, offline).
Output: one row per (run, bin, seed) with columns `run_id, seed, g_N_lo_ms2, g_N_hi_ms2,
n_pairs, vtilde_med, B_i, S_i, r_chance` plus run-level metadata (footprint, max_stars,
contamination_frac, injected_amplitude, astrolabe_commit) — a superset of
`COLUMN_SEMANTICS_BINNED` sufficient to reconstruct every claim's verdict without rerunning.

**Verification.** Fixture-only: the whole matrix must run from the frozen recipe above with no
network access and no live Gaia query, exactly as `make_synthetic_star_field` already does for
Astrolabe's own offline tests.

## References

- K.-H. Chae, "Breakdown of the Newton–Einstein Standard Gravity at Low Acceleration in
  Internal Dynamics of Wide Binary Stars," *ApJ* 952, 128 (2023), arXiv:2305.04613 — the
  claimed low-acceleration anomaly this protocol's effect-size threshold is scaled against.
- I. Banik et al., "Strong constraints on the gravitational law from Gaia DR3 wide binaries,"
  *MNRAS* 527, 4573 (2024) — the high-significance Newtonian counter-result from the same
  class of data.
- H. Boufourou, "Estimator forensics for the wide-binary gravity test: the eccentricity-triple
  coupling manufactures a pseudo-signal, and a pre-registered protocol for Gaia DR4," arXiv:
  2608.24556 (2026) — the literature precedent that estimator artifacts (a different specific
  mechanism) can manufacture a pseudo-signal in this exact class of test, and the direct
  precedent for preregistering a protocol before results exist.
- K. El-Badry, H.-W. Rix & T. M. Heintz, "A million binaries from Gaia eDR3: sample selection
  and validation of Gaia parallax uncertainties," *MNRAS* 506, 2269 (2021), arXiv:2101.05282 —
  the quality-cut and pair-validation conventions ("El-Badry & Rix-style selection") Astrolabe's
  pipeline and this protocol both inherit. That paper's own chance-alignment method is an
  empirical per-pair rate computed from the catalog's own observables, not a shifted/rotated
  field; Astrolabe's shifted-field estimator (and this protocol's calibration test of it) is a
  distinct technique and is not attributed to El-Badry, Rix & Heintz.
- M. J. Pecaut & E. E. Mamajek, "Intrinsic Colors, Temperatures, and Bolometric Corrections of
  Pre-Main-Sequence Stars," *ApJS* 208, 9 (2013), arXiv:1307.2657 — source of the
  main-sequence M_G → mass relation Astrolabe's `mass_from_abs_g` implements and this
  protocol's forward model reuses unmodified.
- **Conjecture — to verify:** the declination-dependent quality-gradient coefficient
  (`1 + 0.5·|sin(dec − dec_0)|`) and the ×3 density-gradient ratio (§ Generative population) are
  stand-in shapes chosen to stress-test the geometry/truncation coupling, not measured values
  from a real survey completeness map; no claim in this protocol depends on their specific
  numeric values being realistic, only on the qualitative gradient existing.

## Relationship to the wall and existing families

This protocol reopens no `schema/wall.json` entry, touches no claim in `gravity-as-scarcity` or
`two-substance-vortex-vacuum`, and asserts nothing about whether the Chae/Banik dispute is
resolved. It is a single new family (`wide-binary-selection-methodology`) with one live gate
([wide-binary-selection-bias-control](../gates/wide-binary-selection-bias-control.json)), so the
one-live-front-per-family rule is trivially satisfied and no existing family's live front is
displaced.
