## The metric character of scarcity and the photon sector — the ORB-10156 derivation

Daniel's challenge (2026-07-12): *"call it scarcity or call it curvature, same thing, isn't
it?"* This section stops that being a matter of taste. The weak-field metric of any metric
theory carries **two** potentials — Φ in g₀₀ (clock rates; the entire driver of slow massive
particles) and γΦ in gᵢⱼ (how much proper space a mass adds; γ = 1 in GR) — and photons read
both while planets read only the first. All PPN machinery and measured values here lean on
[studies/scalar-gravity-ppn-constraints](../../studies/scalar-gravity-ppn-constraints.md).

### (a) What kind of metric object is scarcity? γ, computed

The lattice stores two distinct objects, and they must not be conflated:

- the **accumulated dilution** Σ 1/count(k) ∝ 1/r — the potential-like scalar particles roll
  down (ledger row 1; thread correction #1);
- the **local per-shell dilution** 1/count(k) ∝ 1/r² — the literal point-density deficit at
  radius r.

Slow massive particles in any weak-field metric obey ẍ = −∇Φ *independent of γ*; the model's
rolling law is ẍ = −∇s. So the dynamical identification is forced and exact: **the stored
scarcity is Φ — a time-potential**, fixed by the very trajectories the sims integrate. The
"particles roll down a stored potential" mechanic is the Φ-like statement.

The space-facing potential Ψ ≡ γΦ could only come from the literal depletion of point
density, and that fails twice:

1. **Wrong radial law.** The density deficit is the per-shell dilution, ∝ 1/r², not ∝ 1/r. It
   contributes nothing to the 1/r coefficient that defines γ. Read that way, the model has
   **γ = 0**.
2. **Wrong sign.** Weak-field GR puts *more* proper space near a mass (radial rulers measure
   an excess ∫(GM/c²r)dr — the embedding funnel); depletion puts *less* space near a mass. A
   volumetric reading of point count (proper volume ∝ points) therefore gives Ψ with the
   **opposite sign** to GR — γ < 0, pushing the light sector away from GR, through and past
   Nordström.

**Computed: γ_derived = 0 at best** (time potential on flat space), negative under the
literal volumetric reading. The Φ-vs-Ψ question in the task is answered: scarcity as counted
is Φ-like; its Ψ-like content has the wrong profile and the wrong sign.

### (b) The photon sector, branch by branch

Three photon couplings exhaust what the mechanic supports; measured against the limb
deflection α = (1+γ)/2 × 1.75″ and Cassini's γ − 1 = (2.1 ± 2.3)×10⁻⁵:

| Branch | Mechanism | Deflection | Shapiro | Verdict |
|---|---|---|---|---|
| (i) blind photons | nothing in the counting model couples a null signal to the stored scalar (the model as simulated has no photon dynamics) | 0 | 0 | refuted — Nordström's fate; deflection is measured at the GR value to ~10⁻⁴ |
| (ii) universal Φ-coupling | photons feel the stored scalar like matter: effective index n = 1 + GM/c²r (γ = 0) | 0.875″ — the half-GR Soldner value | half GR | refuted — \|γ − 1\| = 1 vs 2.3×10⁻⁵: four orders outside the band |
| (iii) literal lattice propagation | signal hops point-to-point on the depleted lattice: sparser points → longer hops per tick → light runs **faster** where space is scarce, n < 1 near mass | bends **away** from the Sun | an **advance**, not a delay | refuted — wrong sign of both observables; profile also 1/r² (non-PPN). Sim adjudication of the sign: proposed faraday task **ORB-10158** |

Branch (iii) spelled out, since it is the reading most faithful to the ontology: if points
are sparser near the mass and a signal advances one hop per tick, each hop covers more ground
where depletion is high — an effective index below 1 — so wavefronts refract *away* from the
well and radar echoes return *early*. Light avoiding the Sun and a Shapiro advance are each
categorically excluded by measurement (deflection toward, since 1919; Cassini's delay is a
delay).

Could the lattice have derived γ = 1? It would need the counting mechanic to produce, from
depletion alone, *both* a clock-rate deficit of GM/c²r (it has no clock mechanism at all)
*and* a proper-space **excess** of GM/c²r (depletion gives a deficit — the wrong sign). The
task's hoped-for outcome — "if the lattice yields both time- and space-facing effects at the
right ratio, the model derives γ = 1" — is hereby recorded as **negative**. A γ = 1 photon
sector must be *added*, and adding a tensor/space sector by hand is precisely the
scalar-tensor move (see the family placement in (e)).

### (c) The weak-field time-flow correspondence, computed

The GR heuristic: local clock rate R(x) ≡ √(−g₀₀) ≈ 1 + Φ/c²; slow bodies obey
a = −c²∇R. The model: a = −∇s. Setting σ ≡ GM/c²r (the dimensionless scarcity, s = c²σ):

> model: a = −∇s = c²∇σ  ·  heuristic: a = −c²∇R = c²∇σ, since R = 1 − σ

The two dynamics are **identical**, term for term, with the identification **σ = 1 − R**: the
fractional scarcity *is* the fractional clock-rate deficit, point by point, at the same
normalization GM/c²r. This is a computation, not an analogy — the formerly `untested` ledger
row is re-gated on it. But the equivalence is exactly as big as the heuristic's domain and no
bigger: in GR the scalar is a *measured clock rate* (gravitational redshift z = Δσ,
Pound–Rebka — studies note), while the lattice has no mechanism making depleted regions tick
slow; σ = clock deficit is an added postulate (if added, redshift comes out right for free —
the cheapest honest extension, but an axiom, not counting). And the heuristic is only the
g₀₀ *half* of the metric; the Ψ half is where the pictures measurably part (b). Row verdict:
**mixed** — exact in the massive slow-motion sector, false as a claim of full weak-field
equivalence.

### (d) The superposition rule, derived

*(Kept as the record of the derivation. Its conclusion has since been measured against and
superseded — ORB-10157, § superposition adjudication below; the postscript closing this
subsection states which step failed.)*

The load-bearing question ORB-10097 left open. On the lattice it splits by regime:

1. **Dilute (linear) regime: depletions add.** To first order, budget bookkeeping superposes
   — whether each mass draws on original or remaining density differs only at second order.
   Additive potentials mean the Galaxy contributes a nearly uniform acceleration across the
   solar system, absorbed by the freely-falling heliocentric frame up to its *tide*: of order
   ½·(a_gal·r/R₀)·T² ≈ 8×10⁻¹³ AU at Uranus over the 10-year window — more than three orders
   below the tightest floor. A strictly linear scarcity model predicts no observable
   solar-system signature. **But strict linearity also forfeits the β-boost** — the boost
   *is* a nonlinearity — so this branch is not available as a defense: the theory that fit
   the rotation curve cannot claim it.
2. **The boost mechanic, read as a field statement: multiplicative.** The fitted form
   v_S² = v_N² · q(r)/q(R₀) is literally a position-dependent effective coupling
   G_eff(r) = G · q(r)/q(R₀), keyed to the accumulated background depletion at r. On a shared
   finite budget, **depletion is anonymous** — a lattice point diluted by the Galaxy is
   simply diluted; no counting rule lets a source's field generation respond only to *its
   own* depletion. An embedded source therefore generates with the background's coupling: the
   Sun's field at galactocentric r_gal is multiplied by exactly the factor ORB-10097
   integrated. **The multiplicative reading is the derived local behavior, not an optional
   interpretation** — and the Uranus tension (1.89× rms floor in the physical galactocentric
   orientation; six-axis envelope 0.66–3.0×) is the model's own.
3. **No screening arises.** The screened branch's premise — the Sun's own depletion dominates
   and pins the local scarcity — is quantitatively false in the model's own potential-like
   units: the galactic level at the solar circle is σ_gal ≈ (v_c/c)² ≈ 6×10⁻⁷ (up to an O(1)
   logarithm), while the Sun's own σ_sun = GM☉/c²r falls below that beyond r ≈ 0.017 AU
   (≈ 3.7 R☉) — ~1×10⁻⁸ at Earth, ~5×10⁻¹⁰ at Uranus. The Sun dominates local *gradients*
   out to interstellar distances, but the mechanic couples to *levels*, and the level is set
   by the Galaxy everywhere planets orbit. The model's only two nonlinearities — headroom
   modulation (which *produces* the multiplicative behavior) and budget exhaustion (which
   produces the far cutoff, not local shielding) — supply neither a chameleon mechanism
   (density-dependent scalar mass, thin shells) nor a Vainshtein mechanism (derivative
   self-interaction). If a screening extension is ever attempted, the **chameleon family is
   the natural analog** (screening keyed to ambient level, matching the lattice ontology),
   and Cassini fixes its design target: \|γ − 1\| < 2.3×10⁻⁵ locally while leaving the
   galactic boost intact. As of now it would be a *new model*, not a reading of this one.

Sim adjudication of point 2 at the mechanic level (does an embedded source's field really
scale with background depletion on an actual shared-budget lattice, and by what functional
form?): **since run (ORB-10157), and the derivation did not survive it** (§ superposition
adjudication below). The lattice confirms point 2's anonymity premise and its qualitative
core — embedded sources are not exempt (independence refuted, log-RMSE 1.074) — but refutes
the transplant step: the modulation the shared budget actually supplies is survivor-fraction
screening, A(D) = (1−D)^1.071 at unit gain in local occupancy, not the fitted q-ratio with
its β gain. Point 3's headline ("no screening arises") is measured false in the
survivor-fraction sense; what does *not* arise is the exemption ORB-10097 called "screened"
— the level-vs-gradient argument stands for exactly that. Points 1–3 stay as the record of
the derivation; the measured verdict supersedes their conclusions (superposition rows in the
ledger).

### (e) Where the model sits, and where "scarcity = curvature" holds

**Family placement.** As stated, the model is static, preferred-frame scalar gravity on flat
space — the family whose canonical Lorentz-invariant ancestor is **Nordström 1913**,
geometrized by Einstein–Fokker as conformally flat curvature and killed by the 1919
deflection measurement. The lattice model is *pre*-Nordström (no Lorentz invariance, no field
dynamics), and its derived photon sector is Nordström-grade or worse (γ ≤ 0 across branches).
The surviving descendants are **scalar-tensor** theories (Brans–Dicke: Cassini forces
ω ≳ 4×10⁴) and their **screened** completions (chameleon / Vainshtein) with γ ≈ 1 locally by
construction. Binding constraints, all sourced in the
[studies note](../../studies/scalar-gravity-ppn-constraints.md): solar limb deflection
(\|γ − 1\| ≲ 10⁻⁴, VLBI), Cassini Shapiro (2.3×10⁻⁵), Mercury's perihelion, and at family
level the GW polarization content (a pure scalar has no transverse tensor modes).

**The answer to "same thing, isn't it?" — no, three ways, each now computed:**

- **Where they coincide exactly:** the static weak-field slow-motion *massive* sector. There
  s = Φ = the g₀₀ half of curvature ((c) above), and no experiment confined to that sector —
  stellar rotation-curve kinematics, Newtonian-order planetary dynamics — can distinguish
  them. This degeneracy is why the identification ever felt like taste.
- **Where they measurably differ and curvature wins:** the photon sector. Curvature comes
  with Ψ = Φ (γ = 1, Cassini-confirmed); scarcity as derived has γ ≤ 0 ((a), (b)). As a
  complete account of gravitation the model is refuted here, by ≥ 4 orders of magnitude.
- **Where the model must differ to exist at all:** galactic accelerations. If scarcity were
  *identically* curvature, the β-headroom boost would be relabeled away — GR+baryons reduces
  to the Newtonian control at rotation-curve accelerations, and that control lost by
  ΔAIC ≈ −10⁵ (ORB-10077). The model's one decisive empirical result lives precisely in its
  *deviation* from GR/Newton at low acceleration.

**The precise statement of record:** scarcity ≡ curvature *only* on the static weak-field
slow-motion massive-particle sector; it is measurably *not* curvature in the photon sector,
where being different currently kills it; and it must remain *not* curvature at galactic
scale, where being different is its entire content. The survival path is a screened
scalar-tensor completion — γ → 1 in the solar system, boost intact at galactic scale — and
the Ψ sector has to be *earned* from the counting mechanic rather than bolted on (the literal
mechanic currently yields the wrong sign of Ψ). Precedent that such completions are possible
but costly: TeVeS, itself now severely constrained (studies note). Until that sector exists,
the honest position: **scarcity is a phenomenological modification of the massive sector at
galactic scales — refuted as a complete theory of gravity, alive as exactly that
modification.**
