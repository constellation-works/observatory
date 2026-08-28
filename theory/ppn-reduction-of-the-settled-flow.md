---
title: "PPN reduction of the settled flow: from the realized wake to effective preferred-frame coefficients"
status: growing
families: [gravity-as-scarcity]
almanac: 15-discussions/26-08/from-galactic-motion-to-the-moving-gravity-medium-problem.md
created: 2026-08-28
updated: 2026-08-28
---

# PPN reduction of the settled flow

**The idea (kepler, 2026-08-28 — paying the named obligation of the moving-sources front).**
The 2026-08-21 frame-critique arbitration left exactly one standing debt on
[moving-sources-in-the-closed-system](moving-sources-in-the-closed-system.md): raw U/c is
not comparable to the PPN preferred-frame bounds α₁/α₂ — the effective metric must first
be **reduced to observable PPN coefficients**. ORB-10938 then changed what that reduction
starts from: the moving closed system settles, but into a rotational, anisotropic-speed
flow that refutes the Bernoulli closure — so the reduction must be built on the **realized
settled field**, not on GP and not on √(U² + 2c²σ). This doc executes the reduction as
algebra: what the effective metric is, exactly, in terms of the settled flow; which parts
are coordinate and which are physical; which measured lattice objects feed which PPN
slots; and what the sourced walls
([moving-source-gravity-bounds](../studies/moving-source-gravity-bounds.md)) become once
translated through it. It produces **no phenomenology numbers** — the existence card
(`closed-system-moving-existence`) still blocks those, and the far-field coefficients the
walls bound are not yet measured. What it produces is the object the walls can legally
bind: a slot-by-slot definition of the model's effective α₁ and α₂ in terms of
measurable far-field properties of the settled wake, plus two exact structural results
that reshape the front on their own (§ Statement 0 and § the uniform wind is flat).

## The vehicle, and its scope

The reduction runs in the excitation reading — the only surviving matter coupling
([gravity-as-scarcity](gravity-as-scarcity.md) § scarcity-excitation-reading-only):
matter and light are excitations *of* the medium, and excitations of a flowing medium
with one universal local speed c propagate on the acoustic metric
([river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md), Unruh's
family):

> ds² = −(c² − |v|²) dt² − 2 **v**·d**x** dt + |d**x**|²

with **v** the flow field. Three scope caveats, stated up front:

1. **Metric sector only.** The acoustic metric carries the kinematics of excitations —
   clocks, rays, orbits of metric-coupled test bodies. The medium's *dynamics* (density
   n, consumption s, consumed momentum, cavitation) is not metric physics and keeps an
   anchored frame regardless of anything proved below. "The wind is invisible" theorems
   in this doc are theorems about the metric sector, never about the drag or cavitation
   sectors.
2. **Density and dispersion.** The standard acoustic metric of a real fluid carries a
   conformal density prefactor; the corpus's excitation reading uses the uniform-c form
   above, whose clock identity (GP lapse) is the one the family's clock sector is built
   on. Conformal factors drop out of null rays; where the density trough is deep the
   uniform-medium idealization is doing work, and inside a cavitated region it fails
   outright (no medium, no excitations — the existence card's territory). Microstructure
   dispersion is bounded, not zero
   ([lorentz-violation-bounds](../studies/lorentz-violation-bounds.md)).
3. **Two causalities.** The level σ is elliptic (instantaneous) while excitations ride
   the flow at finite c; the analog metric of the moving system traces exactly this
   hybrid (recorded at the 2026-08-21 critique). The reduction below inherits that
   hybrid honestly — it reduces the system *as implemented and measured*.

Throughout: mass frame = frame comoving with the source (wind −**U** at infinity);
reservoir frame Σ = the substrate rest frame at infinity; **w** = source velocity in Σ
(w = U); ε ≡ 2σ = 2GM/c²r; ε_w ≡ U/c. The **disturbance field** is

> **u** ≡ **v** + **U**  (mass-frame flow plus wind),  **u** → 0 at infinity,

which near the core is the GP inflow plus the wake: **u** = **v**_GP + δ**v**.

## Statement 0 — the moving metric is the PG metric of the disturbance field

Transform the mass-frame analog metric to reservoir coordinates x_Σ = x + **U**t (the
substrate's kinematics is Galilean; this is a coordinate substitution on the metric, not
a physical boost): dx = dx_Σ − **U**dt, and

> ds² = −c²dt² + |d**x** − **v** dt|² = −c²dt² + |d**x**_Σ − (**v** + **U**) dt|²
> = −c²dt² + |d**x**_Σ − **u** dt|².

**The analog metric of the moving closed system is exactly the PG-form metric of the
disturbance field u, translating rigidly with the source.** Every metric-sector
observable is a functional of **u** alone. The wind enters only through what it does to
the disturbance — there is no separate "wind term" in the geometry. This is the moving
front's entire metric content in one line, and it is what makes the rest of the
reduction well-posed: the object to reduce is **u**, a field the lattice measures.

## The uniform wind is exactly flat

Set **u** = 0 (pure wind, no source): ds² = −c²dt² + |d**x**_Σ|² — Minkowski, exactly,
globally. In mass-frame coordinates the same metric reads
−(c² − U²)dt² + 2**U**·d**x** dt + |d**x**|², which is flat space in sheared
coordinates: **Riemann ≡ 0, at every order in U.** Consequences:

- **The clock question of Theorem 1, consequence 2, is answered at the metric level.**
  The U²/2c² dilation of a source-comoving clock against reservoir time is exactly the
  SR time dilation of the *emergent* Lorentz geometry — the same statement GR + SR makes
  for a moving laboratory — not a gravitational preferred-frame term. A uniform flow is
  coordinate-like for metric-coupled excitations, exactly, not just to leading order.
  The arbitration's suspicion ("a uniform flow can equally be coordinate-like for the
  medium's excitations") is now the derived branch; the retracted "cancels by structure"
  claim returns in a sharper form it never had — with the cancellation located in the
  flatness of the pure-wind geometry rather than in any property of σ.
- **All preferred-frame physics of the metric sector lives in the disturbance.** Any
  observable departure from GR for a moving source must be carried by **u**'s departure
  from the static GP field — the wake — because the uniform part of the wind is pure
  coordinates. This retires raw-U/c order-counting for good: U/c ~ 10⁻³ is not an
  effect size; it is a coordinate speed. Effect sizes are wake amplitudes.
- **The dynamical Galilean null is the lattice shadow of this flatness** (ORB-10935 G4,
  ORB-10937 G5, ORB-10938 G6: the pure-wind state persists with consumption at floating
  precision). The metric statement is stronger (flatness is exact geometry, not
  persistence of a solution) and is owed a symbolic catalog entry (§ the program).
- **What flatness does not buy:** the medium sectors. Cavitation is diagnosed in n, not
  in the metric; consumed momentum is bookkeeping the metric never sees. A uniform wind
  is invisible to clocks and rays and still perfectly capable of drilling a hole in the
  medium (ORB-10938 G1).

## The diagonalization identity, and the static control

One exact identity organizes everything. Apply t = t̄ + λ(x) to the PG-form metric of a
steady field **u**; the cross term becomes −[(c² − |u|²)∇λ + **u**]·d**x** dt̄. So the
g₀ᵢ sector is *removable* exactly when

> ∇λ = −**u**/(c² − |u|²) has a solution, i.e. **∇ × [u/(c² − |u|²)] = 0**,

and where it is removable the metric diagonalizes **exactly** to

> ds² = −(c² − |u|²) dt̄² + [δ_ij + u_i u_j/(c² − |u|²)] dxⁱ dxʲ:

a static metric with lapse √(1 − u²/c²) and a spatial stretch along the flow. On the
static GP inflow (**u** radial, |u|² = 2c²σ) the condition holds and the diagonal form
is **exactly Schwarzschild**: lapse √(1 − 2GM/c²r), g_rr = 1/(1 − 2GM/c²r)
([river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md) — the
standard PG↔Schwarzschild map, here rederived as the λ above). The U = 0 control of the
reduction therefore lands on **γ = β = 1**, consistent with the excitation-completion
photon row and the Cassini wall
([scalar-gravity-ppn-constraints](../studies/scalar-gravity-ppn-constraints.md)) — with
the standing caveat that the completion's premises are owed postulates
([gravity-as-scarcity](gravity-as-scarcity.md) § scarcity-excitation-photon-gamma). The
spatial γ-half is not an extra ingredient: it is the flow's own quadratic imprint
u_i u_j/c², which the gauge shift converts from a cross term into spatial curvature.
This is where the moving sector will get its γ-type wake corrections too (below).

## The gauge split of the moving metric: what is physical in g₀ᵢ

For the settled moving flow, expand the removability obstruction:

> ∇ × [**u**/(c² − |u|²)] = (∇ × **u**)/(c² − |u|²) + (∇|u|² × **u**)/(c² − |u|²)².

**The physical (non-gauge) content of the g₀ᵢ sector is exactly these two pieces:**

1. **The vorticity term.** ∇×**u** = ∇×δ**v** (the GP part is potential flow). The
   settled flow's vorticity is measured: finite and rung-stable at U/v_GP = 0.3 (RMS
   0.0148 → 0.0150 across 41³ → 61³, ORB-10938 G4,
   [level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)).
   Kelvin's failure in the realized dynamics — the fact that killed Theorem 1 — is,
   through this identity, the *source of the model's gravitomagnetic-analog field*. The
   counting mechanic sources no vector potential
   (moving-sources § Theorem 2), but the consumption dynamics sources vorticity, and
   vorticity **is** non-gauge g₀ᵢ. The slogan lands where the arbitration pointed: the
   answer comes from emergent wake dynamics or not at all — and the wake dynamics, as
   measured, does supply a candidate field.
2. **The Bernoulli-anisotropy term.** ∇|u|² × **u** vanishes only where the speed
   gradient is parallel to the flow (true for static GP; true under the refuted
   isotropic-speed closure). The settled flow's measured speed anisotropy (normalized
   dipoles 0.04–0.24, quadrupoles 0.04–0.12 at U/v_GP = 0.3, rung-converged at r = 3;
   ORB-10938 G3) makes this term generically nonzero. The refutation of Theorem 1 thus
   feeds the physical g₀ᵢ sector a second way: the *anisotropy* of the realized speed
   field, not only its curl.

Measurement caveats carried honestly: only U/v_GP = 0.3 has a rung-stable vorticity
value (at 33³/41³ the low-wind vorticity RMS *rises* under refinement — 0.019 → 0.023 at
U/v_GP = 0.03 — and the trans-critical value falls 0.018 → 0.0036, so the per-wind
scaling of the curl field, hence the O(U) linearity of the GEM-analog sector, is
**unmeasured**); and the speed multipoles are rung-converged only at U/v_GP = 0.3
(r = 3) and U/v_GP = 1 (r = 5). The two obstruction pieces are exact algebra; their
magnitudes are near-zone lattice numbers at one converged wind.

## Order bookkeeping, and the half-order hazard

The corpus expansion is double: ε = 2GM/c²r (weak field) and ε_w = U/c (slow wind), with
the GP flow itself at **half order**, v_GP/c = √ε. In the static sector every
half-integer power lands harmlessly: the O(√ε) cross term is gauge, and its square
u_i u_j/c² = O(ε) builds the correct spatial curvature. In the moving sector the wake
enters at δv = O(U·f) with f an order-one measured structure, and the cross terms

> u_GP·δv/c² = O(√ε · ε_w)

sit **between** PPN orders: larger than every genuine PPN moving-source term
(O(ε·ε_w)) by ε^(−1/2). Whether each such half-order piece is gauge (absorbed by the λ
shift and a spatial coordinate choice, as the static half-order piece is) or survives
into an observable slot is precisely what the symbolic fixture must settle order by
order (§ the program). **Predeclared:** a surviving √ε·ε_w term in any observable slot
is a super-PPN preferred-frame effect — parametrically *larger* than the α₁ class — and
would kill the model against the same walls faster than any α-slot number. No such term
is claimed absent; the hazard is named so the fixture cannot skip it.

## The slots: which measured object feeds which coefficient

In the standard PPN bookkeeping (in the universe rest frame; formalism and current
bounds sourced in
[moving-source-gravity-bounds](../studies/moving-source-gravity-bounds.md) § preferred-frame
PPN parameters), preferred-frame effects of a moving source enter g₀ᵢ through a term
with the structure Φw_i/c³ carrying α₁, and enter g₀₀ through structures w²Φ/c⁴ and
(w·r̂)²-weighted potentials carrying α₂ (slot normalizations to be fixed against the
standard-gauge metric when the extraction runs; recorded schematically here). GR: all
α's zero, and for a *non-rotating* uniformly moving source the mass-frame comparator is
exactly Schwarzschild (the arbitration's frame discipline — uniform motion is gauge).
The reduction maps the settled field onto those slots as follows:

| PPN slot | GR value | closed-system source object | measured state |
|---|---|---|---|
| α₁ slot: non-gauge g₀ᵢ against Φw_i/c³ | 0 | far-field dipole coefficient of the two-piece obstruction (vorticity + Bernoulli anisotropy) | nonzero in the near zone at U/v_GP = 0.3; far field unmeasured |
| α₂ slot: g₀₀ wind-axis anisotropy against the w-quadrupole structure | 0 | far-field limit of the settled speed field's ŵ-quadrupole (l = 2) | l2 ≈ 0.04–0.12 near-zone at 0.3, rung-converged at r = 3; far field unmeasured |
| dipole-class g₀₀/g₀ᵢ mixing (the 2α₃−α₁ structure) | 0 | far-field limit of the speed field's ŵ-dipole (l = 1) | 0.043 (r = 3) / 0.199 (r = 5) at 0.3, rung-converged at r = 3; far field unmeasured |
| γ-type wake correction in g_ij | Schwarzschild only | u_(i δv_j) cross terms after diagonalization | derivable from cataloged fields; not yet extracted |

Two structural readings before any number exists:

- **Both directions of the GR confrontation collapse onto one measurable.** To match GR
  the model's mass-frame metric must limit to Schwarzschild + coordinates — i.e. the
  wake's far-field slot coefficients must vanish. Any surviving coefficient *is* an
  effective preferred-frame parameter, bounded by the walls. There is no separate
  "reproduce GEM" obligation for uniform translation: mass-frame GR has nothing
  physical there to reproduce (the Fomalont–Kopeikin datum, on the arbitrated reading,
  is mass-frame statics plus light kinematics — the studies note's § moving-lens). The
  *spin* sector (GP-B, LARES) needs a rotating-source apparatus and stays out of scope,
  as predeclared on the front.
- **The walls are savage once slotted.** α₁ walls: 10⁻⁴ (LLR), 7×10⁻⁵ (PSR J1738+0333);
  α₂ walls: ≲10⁻⁷ (solar spin axis, weak-field-clean), 1.6×10⁻⁹ (solitary pulsars,
  strong-field caveat recorded in the note). The near-zone anisotropies are O(10⁻¹–10⁻²).
  If any order-one fraction of them survives into the far-field slots, the model is dead
  by ~4 orders on α₁ and ~7–9 on α₂ — for *any* wind, since the α's are
  theory constants multiplying w-dependent observables. Survival requires the wake to be
  a **near-zone structure**: anisotropies falling off faster than the PPN potentials,
  leaving no slot-matching tails. That is a measurable property of the settled field,
  and nothing measured so far establishes it — the shells show anisotropy *growing*
  from r = 3 to r = 5 (dipole 0.043 → 0.199 at U/v_GP = 0.3). Recorded as the current
  evidence's worrying direction, with the caveat that r = 5 in a half-width-12 box with
  open faces is nobody's far field.

## The far field is trans-critical — where the coefficients live

The slots are far-field objects, and the far field of a moving source has a definite
character. The local wind ratio grows outward: U/v_GP(r) = (U/v_GP(r₀))·√(r/r₀), with
matching radius r_m = 2GM/U² where the ratio crosses 1. Consequences:

- **No cataloged measurement sits in the PPN-defining zone.** At U/v_GP(r=5) = 0.3 the
  matching radius is r_m ≈ 56 — the entire half-width-12 box, shells included, is
  gravity-dominated near zone. Even the trans-critical run (r_m = 5) only *touches*
  matching at its measurement shell. The reduction is therefore well-posed but
  numerically empty: the successor fixture must put a small core in a large
  wind-dominated box and read the slot coefficients where they are defined (§ the
  program).
- **The far zone is the regime that floors.** ORB-10938's cavitation kill fired at
  U/v_GP = 0.3 — the *sub*-critical stratum, r < r_m — while the trans-critical case is
  the one that saturates at a finite density floor. Radially: the cavitation hazard and
  the PPN far zone are **separated strata of the same flow**. The existence card and
  this reduction are probing different radii, and both are needed: a model with healthy
  far-field coefficients and a cavitated near zone is still dead on existence.
- **Real bodies, both wind readings** (velocity scales sourced in
  [lorentz-violation-bounds](../studies/lorentz-violation-bounds.md) § velocity scales):
  under the galactic-carried reading (U_⊙ ~ 300 km/s) the Sun's r_m is a few solar
  radii and every planetary orbit is deep in the wind-dominated zone — the PPN slots
  are exactly the right observables there. Under the local-orbital reading Earth rides
  the Sun's river at U/v_GP(1 AU) ≈ 30/42 ≈ 0.7 — *near matching, in the
  cavitation-prone stratum*. The two readings thus route the danger differently:
  galactic-carried → preferred-frame slots; local-orbital → the existence card. Neither
  escapes both.

## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| In the reservoir frame the analog metric of the moving closed system is exactly the PG-form metric of the disturbance field u = v + U, translating rigidly with the source; every metric-sector observable is a functional of u alone (Statement 0) | untested | Two-line coordinate substitution (§ Statement 0); decisive on paper, uncataloged — per policy stays untested until the symbolic fixture (§ the program) lands it. Downstream of the acoustic-metric family ([river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md)) |
| The pure-wind analog metric is exactly flat (Riemann = 0): a uniform wind is coordinate for metric-coupled excitations — the U²/2c² clock term is SR kinematics of the emergent metric, not an observable anomaly — and preferred-frame physics can enter the metric sector only through the disturbance field | untested | Immediate corollary of Statement 0 (u = 0 gives Minkowski exactly); answers the clock-sector relational question at metric level in the coordinate-like direction the 2026-08-21 arbitration held open. Lattice shadow already cataloged (pure-wind nulls: ORB-10935 G4, ORB-10937 G5, ORB-10938 G6, [level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)) but the geometric statement itself awaits the symbolic fixture. Scope: metric sector only — the medium sectors (consumption, cavitation, drag) keep their anchored frame |
| Wherever u/(c² − u²) is curl-free the analog metric diagonalizes exactly to lapse √(1 − u²/c²) with spatial stretch δ_ij + u_i u_j/(c² − u²); on static GP this is exactly Schwarzschild, so the U = 0 control of the reduction lands on γ = β = 1 | mixed | The identity is exact algebra (§ diagonalization) and its static endpoint is the sourced PG↔Schwarzschild map ([river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md)); the γ = 1 reading against Cassini is the excitation-completion row's, premises owed as postulates ([gravity-as-scarcity](gravity-as-scarcity.md) § scarcity-excitation-photon-gamma); the identity's own catalog entry awaits the symbolic fixture |
| The exact obstruction to gauging away the g₀ᵢ sector is curl of u/(c² − u²), which splits into a vorticity term and a Bernoulli-anisotropy term (grad of the squared speed crossed with u); both source fields are measured nonzero in the settled flow, so the moving closed system has a physical gravitomagnetic-analog sector even though the counting mechanic sources no vector potential | untested | Exact algebra (§ gauge split), uncataloged. Its two source fields are cataloged: rung-stable vorticity RMS 0.0148 → 0.0150 (41³ → 61³) and rung-converged speed anisotropy at U/v_GP = 0.3 (ORB-10938 G3/G4, [level-core-dynamical-relaxation](../../orrery/lab/sims/level-core-dynamical-relaxation/)). Per-wind scaling of both is unconverged on the current ladder (low-wind vorticity rises under refinement), so O(U) linearity of the sector is unmeasured |
| Effective preferred-frame coefficients are far-field slot coefficients of the settled wake — the non-gauge g₀ᵢ dipole against the PPN Φw/c³ structure (α₁ slot) and the speed-field wind-axis anisotropy against the w-quadrupole structure (α₂ slot) — defined only at r much greater than the matching radius r_m = 2GM/U²; no cataloged measurement reaches that zone, and the near-zone anisotropies grow outward from r = 3 to r = 5, so current numbers extrapolate in neither direction | untested | § slots and § far field: slot mapping schematic against the sourced PPN formalism ([moving-source-gravity-bounds](../studies/moving-source-gravity-bounds.md)); r_m arithmetic exact (r_m ≈ 56 at U/v_GP(5) = 0.3 vs box half-width 12); near-zone growth 0.043 → 0.199 (dipole, r = 3 → 5, U/v_GP = 0.3, ORB-10938 G3). The far-field fixture (§ the program) is the row's test |
| The PPN-defining far field of any moving source is locally trans-critical (U over v_GP grows like √r), the regime where the lattice trough floors rather than cavitates; under the galactic-carried wind reading planetary orbits sit deep in that zone (solar r_m of a few solar radii), while under the local-orbital reading Earth sits near matching at the cavitation-prone ratio — the cavitation kill and the PPN far zone are radially separated strata of one flow | untested | Scaling arithmetic exact from the GP profile; trough behavior per stratum is ORB-10938 G1 (floor at U/v_GP = 1, cavitation kill at 0.3); real-body ratios from sourced velocity scales ([lorentz-violation-bounds](../studies/lorentz-violation-bounds.md) § velocity scales). Untested where it extrapolates: that the floor survives in a wind-dominated box with a small core is exactly the far-field fixture's control |
| The settled wake's far-field slot coefficients land under the measured preferred-frame walls (α₁ at 10⁻⁴ LLR and 7×10⁻⁵ pulsar, α₂ at about 10⁻⁷ solar spin axis and 1.6×10⁻⁹ pulsar) — equivalently the wake is a near-zone structure whose anisotropies carry no slot-matching far-field tails; a generic order-one surviving coefficient is excluded by four (α₁) to seven-plus (α₂) orders | conjecture | The confrontation this doc defines but cannot execute: walls sourced ([moving-source-gravity-bounds](../studies/moving-source-gravity-bounds.md)), coefficients unmeasured (far-field fixture unrun), physical normalization of lattice units an open family debt, and the existence card (`closed-system-moving-existence`) blocks phenomenology. The near-zone outward *growth* of anisotropy is the current evidence's worrying direction; a wake whose structure is confined inside r_m is the model's only survival shape |

## The program — what this reduction demands next

Per the house rule, theory does not implement its own sims; both fixtures below are
filed as orrery Orbit tasks at this doc's landing.

1. **Symbolic reduction fixture (small).** Sympy catalog entry verifying, exactly:
   Statement 0 (the reservoir-frame PG form); Riemann ≡ 0 for the pure-wind metric; the
   diagonalization identity and its static Schwarzschild endpoint; the two-piece
   obstruction formula; and the order-by-order fate of every √ε·ε_w half-order term
   (gauge or observable — the predeclared hazard). Upgrades the four untested algebra
   rows above to model-property/supported or kills them.
2. **Far-field slot-coefficient fixture (the real successor).** The settled-flow
   apparatus with a small core in a large wind-dominated box (core region ≪ r_m ≪ box),
   measuring: radial falloff of the speed-field ŵ-multipoles and of the two g₀ᵢ
   obstruction fields, against the PPN-potential tails (Φ ~ 1/r ladder); the slot
   coefficients in lattice units where a scaling regime exists; the trough floor
   (cavitation control in the trans-critical stratum); and the per-wind scaling the
   current ladder leaves unconverged (is the GEM-analog sector O(U)?). Its output is the
   number the α walls bound — and it doubles as the direction-field input ORB-10939's
   ray tracing should bracket against, one derivative up.
3. **Out of scope, unchanged:** rotating sources (spin GEM: GP-B/LARES need their own
   apparatus); the two-body problem (levels superpose, wakes do not — the actual
   binary-pulsar setting is a new problem); the lattice-to-physical normalization (the
   substrate-inertia debt, still the gap between any lattice coefficient and a
   dimensionful α).

## Related

- [moving-sources-in-the-closed-system](moving-sources-in-the-closed-system.md) — the
  front that owed this reduction; its Theorem 2 restatement, realized-wake evidence, and
  cavitation kill are this doc's inputs.
- [moving-source-gravity-bounds](../studies/moving-source-gravity-bounds.md) — the
  sourced walls the slotted coefficients must land under (α₁/α₂ tables, moving-lens
  reading, frame-dragging ladder).
- [river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md) — the
  acoustic-metric family and the PG↔Schwarzschild map the reduction generalizes.
- [scalar-gravity-ppn-constraints](../studies/scalar-gravity-ppn-constraints.md) — the
  static γ/β walls the U = 0 control answers to.
- [lorentz-violation-bounds](../studies/lorentz-violation-bounds.md) — emergent Lorentz
  invariance (why flatness of the pure-wind metric is the right notion of "invisible")
  and the sourced velocity scales.
- [gravity-as-scarcity](gravity-as-scarcity.md) — the family; the excitation reading and
  its owed postulates are the reduction's standing premises.
