## The clock sector — the ORB-10159 derivation

ORB-10156 left the clock sector as the model's silent failure: σ = clock-rate deficit was
flagged as a postulate the counting mechanic does not supply. This section makes that failure
explicit, then derives what the dynamical completion is forced to be. The instruments here
are the measured time-dilation ladder
([studies/gravitational-time-dilation](../../studies/gravitational-time-dilation.md)), the
river/analog-gravity machinery
([studies/river-model-and-analog-gravity](../../studies/river-model-and-analog-gravity.md)),
and the Lorentz-violation bounds
([studies/lorentz-violation-bounds](../../studies/lorentz-violation-bounds.md)).

### (a) The static model has no clock sector — refuted, and the fork is forced

Gravitational time dilation is a measured pure-g₀₀ effect: Pound–Rebka at 1% (with Snider),
Gravity Probe A tracking the GM/r *profile* to 7×10⁻⁵ over 10⁴ km, GPS running a permanent
+38.6 μs/day (4.46×10⁻¹⁰) correction, optical clocks resolving one millimeter of height. The
model as stated — a *static* stored field on a lattice with universal tick rate — predicts
exactly zero: nothing in the counting rules makes a depleted region's physics run slow.
**Refuted** (new ledger row above). Making depletion *dynamical* is the only completion path
inside the ontology, and it forks three ways at the first step:

- **Frozen:** depletion happened once (or accumulates too slowly to matter) — this is the
  static branch again. Dead as above.
- **Accumulating:** the mass keeps consuming and nothing replenishes, so σ grows. Since
  a = c²∇σ, the effective coupling grows at σ̇/σ ~ 1/t_age ≈ 2×10⁻¹⁰ yr⁻¹ for a
  4.6-Gyr-old Sun under any roughly constant consumption rate — an effective Ġ/G more than
  three orders of magnitude above the LLR bound (7.1 ± 7.6)×10⁻¹⁴ yr⁻¹ (studies note).
  Dead.
- **Steady state:** consumption balanced by inward flow of space, standing field static.
  The only live branch — and it is exactly the river reading. The question stops being
  whether space flows and becomes *what flow law the mechanic implies*.

### (b) The flow law, derived — and the kill condition applied

In steady state, continuity ties the flow to the consumption's radial distribution: the
volume flux through the shell at r equals the total consumption rate interior to it,
F(r) = 4πr²n₀v(r) = C(<r). The river dictionary (studies note) then converts flow into
physics: a static clock swims upstream at v(r) and dilates by √(1 − v²/c²) ≈ 1 − ½v²/c², and
slow bodies accelerate at a = −∇(½v²). So each candidate consumption rule *is* a
time-dilation profile and a force law — this is what makes the fork derivable:

1. **Sink at the mass only** (the naive "mass eats space where it sits"): all consumption at
   r = 0, so F is r-independent — the flux-conserving flow, v ∝ 1/r². Dilation ∝ v² ∝ 1/r⁴,
   gravity ∝ ∇v² ∝ 1/r⁵. Wrong profile for clocks (GP-A/Galileo test GM/r), wrong law for
   orbits. **The task's kill condition, confirmed: dead against GPS/optical-clock data** —
   and against Newton, independently.
2. **The mechanic's own bookkeeping, read as a rate** — equal absolute budget drawn per
   shell (the Gauss's-law-analog rule, ledger row 2): consumption per unit radius constant,
   F ∝ r, v ∝ 1/r. Dilation ∝ 1/r², gravity ∝ 1/r³. Dead against the clock ladder — and
   *internally inconsistent*: the same bookkeeping read statically gives the verified 1/r²
   force, read dynamically through the river dictionary it gives 1/r³. The static and
   dynamical readings of one rule disagree, so the rule cannot be the whole story.
3. **Space obeys the model's own rolling law.** The model has exactly one dynamical rule —
   things accelerate down the scarcity gradient. If lattice points are not exempt from the
   dynamics they create, an inflowing parcel obeys v·dv/dr = c²·dσ/dr, and falling from
   rest at the outer reservoir: **½v² = c²σ = GM/r — the free-fall law, exactly the
   Gullstrand–Painlevé river**, v = √(2GM/r). Dilation √(1 − 2GM/c²r): Schwarzschild
   *exactly*, every row of the measured ladder passed by construction, and
   a = −∇(½v²) = −GM/r² r̂ hands back the verified Newtonian sector unchanged.

**The consistency identity, computed.** The task requires the static Σ 1/count ∝ 1/r result
to be the time-integrated snapshot of the derived flow. On branch 3 it is, exactly and twice
over. First, the accumulated dilution is a comoving integral: a parcel falling from the
reservoir to r traverses every shell k > r and accumulates their per-shell dilutions —
Σ_{k>r} 1/count(k) ∝ 1/r *is* the running record of the flow's history, which is why the
static sims verified it. Second, the ORB-10156 Φ-sector identity extends without
modification: the free-fall law gives σ = ½v²/c², and the GP lapse for a static observer is

> √(−g₀₀) = √(1 − v²/c²) = √(1 − 2GM/c²r),  so 1 − √(−g₀₀) ≈ ½v²/c² = σ

— the same σ = 1 − √(−g₀₀) computed statically in ORB-10156(c), now with a *mechanism*:
scarcity is the flow's kinetic energy, and the clock deficit is SR dilation against the
flow. The static verdict survives as the snapshot of the dynamical one. (*Measured caveat,
ORB-10162:* the identity is a branch-3 property, not a general one — the lattice's
central-only branch reproduces the finite-reservoir 1/r standing field at R² 0.99999992
with *zero* comoving dilution before the sink, so a verified static 1/r field is not by
itself evidence of a comoving flow record; § lattice adjudication below.)

**The debt.** Branch 3's flow is not free: continuity dictates where consumption must
happen. F ∝ r²·r^(−1/2) = r^(3/2) grows outward, so space is destroyed *throughout the
volume* — sink density ∝ r^(−3/2), consumption per shell growing as r^(1/2) out to the
budget's cutoff radius (the model's own finite-budget edge, ledger row 3, is what keeps the
integral finite — the river's reservoir has a boundary). No current counting rule produces
an r^(1/2)-per-shell draw; the equal-per-shell rule produces r⁰ and is refuted above. So the
honest statement of record: **the flow law is earned** (one new postulate — space itself
obeys the rolling rule — turns the mechanic's own dynamics into exact GP), **but the
consumption law that sustains it is owed.** Whether a dynamical-consumption lattice actually
self-organizes to the free-fall flow is a measurable property of the mechanic: faraday task
**ORB-10162** (emergent flow law, sink distribution, and the time-integrated snapshot
check) — **since run; the answer is no for both natural rules** (§ lattice adjudication
below).

### (c) Matter coupling: in the lattice, of the lattice, or neither

The drag objection: a real river carries a swimmer by molecular collisions; matter has no
coupling constant to space. What do the hop rules actually support?

- **As stated: neither reading.** Matter in every sim is an *external tracer* — it has a
  position, reads ∇σ, and is made of nothing the lattice knows about. An external tracer
  inherits no SR-in-the-flowing-frame, so for it the river buys **no dilation at all**: the
  clock sector's rescue in (b) silently assumed matter is built on the flowing medium. The
  drag objection is fatal to the tracer reading.
- **Deflationary (GR's answer):** the flow field is a map of which motions are force-free;
  its local value is unobservable, only gradients are physical. Consistent — but it is
  *exactly* GR in GP coordinates (Hamilton & Lisle's own caution: nothing measurable
  flows), so the lattice ontology does no work. On this reading the model is relabeled GR
  plus the galactic β-boost as a bolt-on phenomenology.
- **Excitation (analog gravity, Unruh 1981):** matter is a wave *of* the lattice —
  phonon-like — so being carried is constitutive, not an interaction; no coupling constant
  is needed because there is no second substance. This is the only reading under which the
  river mechanism in (b) actually delivers time dilation *and* "space" remains a physical
  ingredient. Its price is new structure: the lattice must support excitation dynamics with
  one universal local propagation speed (the current rules have no matter-wave sector; the
  one-hop-per-tick signal rule of ORB-10156(iii) is the germ, but as a *static-lattice*
  rule it produced the wrong-signed photon sector).

**Verdict (ledger row): by elimination, the excitation reading is the only one that buys the
clock sector while keeping the ontology live** — the canonical family is the GP river
carrying Unruh-style excitations. It is a completion target, not a property of the current
rules.

### (d) The rest-frame question: aether, emergent metric, or relabeled GR

The three placements, computed against measurement:

- **Substance (aether):** if matter couples to the lattice as a foreign body, motion
  relative to the lattice frame is detectable. The scales are fixed: 370 km/s through the
  CMB frame (β² ≈ 1.5×10⁻⁶), or — granting full entrainment down to the local flow — the
  solar GP inflow at Earth, 42 km/s (β² ≈ 2×10⁻⁸). Rotating-resonator bounds sit at
  10⁻¹⁷–10⁻¹⁸ (Eisele 2009; Nagel 2015; SME tables). An O(1) substance coupling is
  **excluded by 9–12 orders of magnitude**. Dead.
- **Excitation (emergent metric):** all excitations of one medium share one limiting speed,
  so no experiment made of excitations detects uniform motion through the medium —
  Michelson–Morley is null *by construction*, and the SME anisotropy coefficients vanish at
  leading order provided every species rides the same lattice (universality is the
  emergent-LI condition). The invariance must still break at the lattice scale, as
  energy-dependent dispersion — and this is *bounded, not excluded*: a parity-symmetric hop
  rule has an even dispersion relation (ω = (2c/a)sin(ka/2)-type), so the leading correction
  is quadratic and subluminal, δv/c ~ −(Ea/ħc)²; GRB 090510 gives E_QG,2 > 1.3×10¹¹ GeV,
  which translates to a **maximum lattice spacing a ≲ 1.5×10⁻²⁷ m ≈ 10⁸ Planck lengths**. A
  parity-*asymmetric* rule would generate a linear term, and the linear bounds
  (E_QG,1 > 7.6 E_Planck) already exceed the Planck scale — so the hop rule is constrained
  to be parity-symmetric. Both constraints are survivable; neither is currently testable
  from inside the model.
- **Relabeled GR:** the deflationary reading of (c) — no rest frame because the flow is
  gauge. Consistent by construction and empirically empty.

**Placement (ledger row): on its only viable branch the model is an emergent-metric theory
of the analog-gravity family** — not an aether (killed at 9–12 orders), not merely relabeled
GR (it retains in-principle discriminators: the quadratic lattice dispersion, the sink law
of (b), and the galactic β-boost).

### (e) What the excitation reading does to the refuted photon sector

The ORB-10156 photon refutation computed light propagation on the *static* depleted lattice:
sparser points → longer hops → n < 1 near mass → bending *away*, Shapiro *advance*. That
verdict stands for the model as stated. But the excitation completion changes the
computation's premises: on a *flowing* lattice with the depletion expressed as inflow rather
than as a standing density deficit, a wave with constant local hop speed sees the acoustic
metric with uniform c and GP flow — which is **exactly the Schwarzschild geometry** (Unruh;
studies note). Deflection comes out *toward* the mass at the full γ = 1 magnitude and the
Shapiro effect is a *delay*: the γΦ half of the metric that ORB-10156 proved the static
mechanic cannot supply is delivered entirely by flow drag. The wrong-signed static effect
survives only as a *contaminant*: any residual standing deficit adds a 1/r²-profile n < 1
term on top of the flow term, and its measured absence (Cassini, VLBI) bounds how much of
the depletion may live in density rather than flow.

Recorded as a new `mixed` ledger row — the mathematics is exact but conditional on the three
postulates the completion owes (free-fall flow, excitation matter, flow-not-deficit
depletion). **ORB-10158's scope was extended accordingly** (2026-07-12 comment): a
flowing-lattice propagation arm (does the sign flip to *toward*?) alongside the original
static arm, which now measures the contaminant.

### (f) Clock-rate screening: is the multiplicative β factor a second instrument?

ORB-10156 derived the multiplicative rule: local field generation scales as
X(r_gal) = q(r_gal)/q(R₀), with local log-gradient βF(R₀)/R₀² ≈ 3.2×10⁻¹⁰ /AU. (The
derivation has since been refuted at the mechanic level — ORB-10157, § superposition
adjudication — but the computation below is a *branch* property: it holds for any
multiplicative carrier of the fitted boost shape, the measured screening law under the
fitted identification included.) If the same
factor rescales local σ — and on the river reading it must, since σ and acceleration are one
object — every locally generated clock deficit is multiplied by X. Computed against the
clock instruments:

- **Redshift-profile tests:** for any local comparison, both clocks carry nearly the same X
  (Earth sits within 1 AU of the normalization point), so the *fractional* correction to a
  measured redshift is |X − 1| ≤ 3.2×10⁻¹⁰ — five orders below the best profile-test
  accuracy (Galileo 2.5×10⁻⁵, GP-A 7×10⁻⁵).
- **Annual modulation:** Earth's galactocentric radius swings by ±1 AU, modulating X by
  ±3.2×10⁻¹⁰; acting on the Sun's potential at Earth (σ_⊙ ≈ 9.9×10⁻⁹) this is a
  species-universal rate modulation of amplitude ~3×10⁻¹⁸ — beneath 10⁻¹⁶-class clock
  comparisons, invisible to null-redshift (LPI) tests *because* it is universal, and worth
  only ~16 ps of annual timing residual against pulsar references (precision ~100 ns).
- **Terrestrial differentials:** across an Earth-diameter baseline ΔX ~ 2.7×10⁻¹⁴, giving
  rate differences ≲ 10⁻²¹ — three orders below even 10⁻¹⁸ optical-clock systematics.

**Verdict (ledger row): the multiplicative branch is safe from — equivalently, unconstrained
by — every current clock instrument.** Clocks do *not* become a second instrument on the
ORB-10097 branch at 10⁻¹⁶, or even 10⁻¹⁸: orbits integrate accelerations twice over decades
while clocks read rates instantaneously, so the Uranus channel keeps a lead of many orders.
The binding constraint on the multiplicative branch remains ORB-10097's orientation-dependent
Uranus tension (itself now conditioned on the fitted-boost identification — ORB-10157,
§ superposition adjudication).

### (g) What the model now is

Assembled, the clock sector forces a specific shape. To live, the model must become: a
lattice whose points **free-fall down their own scarcity gradient** into consuming masses
(steady state, GP flow — earned from the rolling rule; sink law owed, and since *measured
absent* from the natural rules, ORB-10162 — imposed, derived from S2 dynamics (ORB-10161
§B2), or conceded), carrying
**matter and light as excitations with one universal local speed** (Unruh family — owed
entirely; reopens the photon sector with the right sign, ORB-10158), with **emergent Lorentz
invariance** breaking only below ~10⁸ Planck lengths (allowed), the β-boost intact at
galactic scale (clock-safe, (f); its superposition carrier now measured as headroom
screening rather than a derived q-ratio coupling — ORB-10157), and the solar-system sector reducing *exactly*
to GR wherever the completion's postulates hold. Every step is computed above; every owed
ingredient is named and gated on a sim — and the first gate (ORB-10162) has closed against
the mechanic (§ next). What is *not* available: the static model (dead
against clocks), the accumulating model (dead against Ġ/G), flux-conserving or
budget-per-shell rivers (dead against the profile), the mechanic's own natural consumption
rules as the source of the river (measured, ORB-10162), and any substance reading of the
lattice (dead against the resonators).
