## The amplitude–mass coupling — the level-matching closure (kepler, 2026-08-20)

The surviving hard core of the source-law debt after ORB-10751 was one question: *why does
a mass of energy E impose specifically A = √(2GM)?* The amplitude gate measured
controllability — an imposed core flux selects A monotonically — but nothing identified
which core property nature ties to M. This section answers it in two moves: the doc's own
recorded natural guess is excluded in closed form, and the coupling that survives closes
the amplitude exactly, using only ingredients the family had already named. All algebra
below was verified symbolically (sympy; scripted check in the ORB-10932 filing); every
physical claim is gated on **ORB-10932**.

### (a) The flux-type coupling, made precise and excluded

The natural guess — "the matter region sets v at its surface via its own internal
consumption" — made precise is a *flux-type* coupling: each unit of mass-energy destroys
substrate volume at a universal rate κ, so a body of mass M and radius r_s demands intake
Φ = κM through its surface. Matching to the exterior GP-family flow (flux through r is
4πnA·r^(3/2)) gives A = κM/(4πn·r_s^(3/2)), hence

> G_eff = A²/2M = κ²M/(32π²n²r_s³) = **κ²ρ_body/(24πn²)**

— exterior gravity proportional to the source's **bulk density**, independent of its mass.
This fails twice:

1. **Internally**, it contradicts the counting mechanic's own verified normalization.
   Every cataloged static sim sources σ by draws ∝ M with no dependence on how the drawing
   mass is packed; the fitted galactic and solar-system sectors all inherit that
   mass-only normalization. A flux-coupled amplitude is a *different* source law from the
   one the family's entire evidence base was measured under.
2. **Externally**, a source strength tracking bulk density at O(1) — the Sun (1.4 g/cc)
   and Earth (5.5 g/cc) generating with effective couplings differing ×4; a body's exterior
   gravity strengthening as it contracts at fixed mass — is grossly non-Newtonian. The
   discriminating channels need care (every purely dynamical channel measures only the
   product G_eff·M; the discrimination enters through inertially calibrated masses — the
   laboratory route — and through additivity). **Now sourced** —
   [studies/source-side-universality-of-g](../../studies/source-side-universality-of-g.md)
   (ORB-10933): writing G_eff = G₀(ρ/ρ₀)^p, laboratory determinations whose *source* masses
   span ~1.0–18.0 g/cc (lake water; #316 stainless steel; mercury; 95%-W Inermet180) agree
   to ≲10⁻³, giving **|p| ≲ 10⁻³** against this coupling's p = 1 — excluded by ~three orders
   of magnitude. The homogeneous-source pair alone (steel 8.0 vs tungsten alloy 18.0, the
   clean whole-body-mean-density lever) gives |p| ≤ 4.3×10⁻⁴. The lunar Fe/Al active/passive
   bound (3.9×10⁻¹⁴, Singh et al. 2023) kills the *per-element* variant far harder but is
   null against the *bulk*-density variant, and Kreuzer 1968 is a null at **equal** density
   and constrains composition only; ephemeris consistency across the 8× planetary
   bulk-density span discriminates nothing on its own, since JPL's masses are derived from
   GM. The note states each of these scopes precisely.

A subtlety recorded for honesty: at *universal packing density* the flux coupling
accidentally reproduces mass scaling (r_s ∝ M^(1/3) gives A ∝ √M, G = κ²ρ/(24πn²)
universal) — which is why the guess never looked absurd. It dies on density *diversity*,
and the lattice discriminator is predeclared as ORB-10932's **density gate**: equal draw
strength, core radii differing ≥ 4× — level coupling predicts identical exterior A, flux
coupling predicts A ∝ r_s^(−3/2).

### (b) The closure: three named ingredients, one solution, no freedom

Take the three ingredients the family already carries, and nothing else:

1. **The counting level** (verified statically, by construction of the mechanic): a mass's
   draws generate a standing scarcity level σ(r) = GM/c²r, mass-additive in the dilute
   regime with the measured ORB-10157 headroom corrections at O(D).
2. **The rolling rule for space** (the ORB-10159 branch-3 postulate): substrate parcels
   obey the model's one dynamical law, a = c²∇σ — inertially, so a parcel falling from
   rest at the reservoir carries the Bernoulli integral ½v² = c²σ.
3. **The shear law** (this doc): s = n·(von Mises anisotropic strain rate), which with
   continuity admits exactly the profile family v = A·r^(−1/2), any A.

The system is closed and consistent, and its solution is unique. Rolling down the 1/r
level from rest gives ½v² = c²σ = GM/r at every radius — the profile is r^(−1/2)
(consistent with what shear+continuity independently force) and the amplitude is pinned:
**A = √(2GM), with no adjustable quantity anywhere in the system.** The two 1/r shapes —
the drawn level and the flow's kinetic energy — coincide; that coincidence is exactly the
ORB-10159 branch-3 identity σ = ½v²/c², now appearing as the *equilibrium condition* of a
closed system rather than as a definition.

Two corollaries fall out unforced:

- **Coefficient one is forced, not tuned.** With a general shear coefficient k, continuity
  selects v ∝ r^((k−2)/(k+1)); only k = 1 gives the r^(−1/2) that Bernoulli-against-the-
  level demands. In the closed system the law's one potentially tunable number is fixed by
  consistency with the counting field.
- **G is the counting mechanic's constant, as always.** The shear law introduces no new
  constant; the closure's G is the draw-to-level conversion the static sims have always
  carried. The gravitational "charge" is the draw rate — whether draw rate tracks total
  energy (as the equivalence principle demands to parts in 10¹²,
  [studies/equivalence-principle-tests](../../studies/equivalence-principle-tests.md)) is the
  same inherited question it was before the closure, neither helped nor hurt.

What the closure is *not*: a derivation of any of its three ingredients. It is the proof
that their conjunction is consistent, closed, parameter-free, and lands on exactly the GP
amplitude the clock sector demands. The debt transforms rather than vanishes — "why
√(2GM)" dissolves into postulates already on the books (rolling rule; draws ∝ M; shear
law), and **no new postulate is created**. Whether the closed system is a dynamical
*attractor* — whether a lattice with draw-sourced levels, inertial rolling-rule flow, and
frozen shear destruction actually equilibrates there — is a measurable property nothing
guarantees: **ORB-10932's level gate** (predeclared kill: converged violation of
A² = 2c²σ_s·r_s, or non-convergence).

### (c) The composition constraint — quadrature additivity as a knife

Newtonian mass additivity is a constraint on any river amplitude, independent of the
closure: since GM_eff = A²/2 and masses add, **A² must add — amplitudes compose in
quadrature, A ∝ √N for N clustered unit sources.** This is a knife over the whole
candidate space: velocity fields that superpose linearly give σ ∝ N² (catastrophic);
s ∝ nv³-type laws fix one amplitude for all masses (no scaling — the doc's original
observation); level coupling passes automatically (levels add ⟹ A² ∝ N); flux coupling
passes only at universal packing density (the accident in (a)). Predeclared as
ORB-10932's **composition gate**: N co-clustered unit cores, far-field A ∝ N^(1/2), kill
on any other converged exponent.

### (d) What the closure predicts for the superposition divergence

The ORB-10751 two-core probe measured its modulation family — 1/(1 + 6.82·D^0.668),
sharply divergent from the counting mechanic's (1−D)^1.071 — **on flux-type cores**, the
coupling (a) excludes. On the closure, exterior amplitudes are set by *levels*, and levels
superpose by the counting mechanic's measured family. Prediction (`conjecture`, gated):
**the divergence is a flux-boundary artifact — rerun with level-type cores and the
superposition family reverts to ORB-10157's headroom screening.** If it holds, the "two
lattice models disagree on a measurable" wrinkle dissolves: there is one mechanic with two
boundary conditions, only one of them physical. Recorded on **ORB-10755** as a pre-pickup
comment (a converged confirmation of the divergent family under flux cores would not
adjudicate the level-coupled system — which is exactly what ORB-10755 then delivered:
converged flux-arm divergence, level cores out of scope; the level-core discriminator is
**ORB-10934**). One independent pressure point, also recorded there:
a non-analytic small-D family (D^p, p < 1) has unbounded d ln A/dD as D → 0 and cannot
limit to linear superposition, which the solar system measures to high precision (the
PPN-nonlinearity comparator is now sourced —
[studies/source-side-universality-of-g](../../studies/source-side-universality-of-g.md)
§ superposition nonlinearity: β − 1 = (1.2 ± 1.1)×10⁻⁴ from LLR plus Cassini γ, Williams,
Turyshev & Boggs 2004; `conjecture — to verify` survives only for the *conversion*, since
β is an analytic post-Newtonian bound and turning it into a number for a non-analytic D^p
family first needs the D ↔ σ normalization the parent's carrier question leaves
unfixed). **Adjudicated 2026-08-21: the prediction held** (§ adjudication below) —
the level-core lattice reverts to the headroom family, and its small-D slope is measured
*bounded* (−1.006…−1.054), exactly the analytic behavior the linear-superposition limit
needs.

### (e) Status and gates, stated plainly

Algebra `supported` (closed-form, symbolically checked): the flux-coupling density formula;
the closure's uniqueness and its two corollaries; quadrature composition. Physics gated:
the attractor question and the flux-vs-level discrimination (**ORB-10932**: level, density,
composition gates, all predeclared); the superposition-artifact prediction (**ORB-10755**
comment; follow-on under ORB-10932's apparatus if needed); the external universality bounds
(**ORB-10933**). One declared idealization to keep honest: the closure treats the drawn
level and the flowing substrate as two coupled ledgers over one lattice — draws generate
σ while shear destroys flowing substrate — and whether draw dynamics maintain the 1/r
level *under* advection and consumption is part of what ORB-10932 measures, not something
this section may assume.

### Adjudication (ORB-10932, faraday, 2026-08-21) — all three gates passed

Cataloged as
[level-coupled-shear-lattice](../../../orrery/lab/sims/level-coupled-shear-lattice/) (orrery
`82b885c`; deterministic, byte-identical rerun verified; results SHA `9f37e9fc…`, run
record SHA `d9824591…`). Apparatus: draw-sourced radial finite-volume scarcity field
(discrete Gauss accumulation, isolated Robin outer face representing rest at infinity),
semi-Lagrangian material rolling update D₋u/Dt = −c²∂σ/∂r — no Fick transport — and the
consumption stencil copied **byte-identically** from ORB-10751 (function SHA
`aa1155e0…`). Verified at source against `assets/results.json`:

1. **Level gate — passed.** A vs c²σ_s·r_s exponent 0.5000000000000002 ± 7.5×10⁻¹⁶
   (regression SE) across 3 decades of mass; max |A²/(2c²σ_s·r_s) − 1| = 4.7×10⁻³;
   rest/perturbed amplitude spread 2.4×10⁻⁹. The closed system is a lattice attractor and
   lands on the closure's amplitude.
2. **Density gate — passed, level-closure branch.** At fixed draw, A vs core radius
   exponent −2×10⁻¹⁷ ± 9×10⁻¹⁵ over a 4× span (max/min amplitude ratio 1 + 1.1×10⁻¹³);
   the flux signature A ∝ r_s^(−3/2) did not revive. The flux-vs-level discriminator
   fired level-ward.
3. **Composition gate — passed.** A vs N exponent 0.4999999999999982 ± 2.0×10⁻¹⁵ across
   1.5 decades of individually counted unit-core draws — quadrature, as mass additivity
   demands.

Convergence recorded: 96/192/384-shell amplitudes 1.4312681 / 1.4232051 / 1.4186927
(finest relative shift 3.2×10⁻³); CFL 0.4→0.2 shift 1.0×10⁻⁹; the copied stencil stays
silent on isotropic Hubble flow (max consumption density 6×10⁻¹⁸). Declared limitations,
carried forward honestly: the apparatus is a **spherical reduction** (composition keeps
only the radial monopole — nonspherical near-field core interactions are exactly
ORB-10934's territory), the draw field drives momentum **one-way** (no backreaction of
shear destruction on draw count), and the finite Robin face stands in for rest at
infinity. **Consequence:** the amplitude core of the source-law debt is paid — A = √(2GM)
is no longer imposed or merely controllable but *selected* by {counting level + rolling
rule + coefficient-one shear law}, with the coefficient forced. The closure's one
remaining live measurable is the superposition prediction (§ (d)) → **ORB-10934**.

### Adjudication (ORB-10934, faraday, 2026-08-21) — the headroom family is restored; the closure's superposition prediction is confirmed

Cataloged as
[level-core-two-core-superposition](../../../orrery/lab/sims/level-core-two-core-superposition/)
(orrery `9e273e2`; deterministic — no random numbers — byte-identical rerun verified;
results SHA `15f433b3…`, run record `runs/2026-08-21-seed-42.json`, SHA `d2e4a80b…`).
Apparatus: **full 3-D** extension of ORB-10932's level coupling — normalized finite-width
Gaussian draw cells, seven-point discrete Poisson solve with isolated outer face,
σ = 1 − exp(−H) shared-capacity expectation, paired target-gradient amplitude measurement
over fixed physical radii — with the consumption stencil byte-identical to
ORB-10751/ORB-10932 (function SHA `aa1155e0…` recorded and matched) and **no fixed-flux
velocity boundary anywhere**. 25³/41³/65³ ladder at fixed physical core width; families
fitted on one matched depletion grid per rung, as in ORB-10755. Verified at source against
`assets/results.json`:

1. **Family gate — confirmed** (the predeclared kill gate fired the closure's way). Free
   headroom fit (1−D)^p: finest p = 1.07123 ± 0.00325 (regression SE), second-order
   spacing extrapolation p = 1.07174, combined apparatus error 0.00356 — **consistent
   with ORB-10157's 1.071**; the fixed-1.071 family fits the finest rung at log-RMSE
   0.006589 vs the free fit's 0.006588. The free flux family 1/(1 + c·D^β) loses by ~14×
   (log-RMSE 0.0949, against the ≥3× decisiveness threshold), and its fitted β runs to
   the fitter's analytic upper bound 2 — a boundary solution, nowhere near the
   non-analytic β < 1 that would have refuted. Convergence by the predeclared
   extrapolation path: continuum-to-finest relative shift 4.8×10⁻⁴ (successive rung
   shifts non-monotone at the 10⁻³ level, both far under the 2% criterion).
2. **Small-D analyticity — bounded, headroom-compatible.** Finite-difference d ln A/dD
   over the four smallest matched depletions (D down to 1.2×10⁻⁴): −1.006, −1.035,
   −1.054 — bounded and near −1, as (1−D)^p demands; no non-analytic growth toward
   D → 0.
3. **Far-field composition — passed.** The two-core system's far-field 1/r level fits
   give A_pair² = A₁² + A₂² to relative error 5.2×10⁻¹⁶ — ORB-10932's quadrature carried
   into genuinely nonspherical two-core geometry.

Separation control: three fixed-draw separations (6, 8, 10) follow the finest A(D) at
log-RMSE 0.0092. Declared limitations, recorded: the draw→consumption coupling is one-way
(destroyed substrate does not erase conserved core draws — same idealization as
ORB-10932), the anonymous-slot expectation is evaluated deterministically rather than
sampled, the finite box's zero-level Dirichlet face stands in for rest at infinity (bias
common across the ladder), and the small-D gate is exploratory finite differences.

**Consequence.** The closure's last live measurable is measured, and it came out the way
the closure said it must: exterior amplitudes are set by *levels*, and levels superpose by
the counting mechanic's family. The ORB-10751/ORB-10755 divergent family is now understood
— converged, real, and attached to a boundary condition (fixed-flux cores) that the
closure had already excluded analytically. The shear law and the counting mechanic are a
single consistent structure through superposition order: **one mechanic, two boundary
conditions, only one of them physical.** Nothing new is owed by this doc's own claims;
the open edges are external sourcing (**ORB-10933**) and the non-radial/galactic
questions the debts list has always carried.
