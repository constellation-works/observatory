## The program — gates predeclared

**Wind-tunnel lattice (faraday, ws_orrery — filed with this doc).** The ORB-10934
apparatus (full 3-D draw-sourced level coupling, frozen coefficient-one stencil) with a
uniform wind boundary condition: substrate streaming past a single comoving level core at
speeds U spanning sub- to trans-critical ratios against the local river scale. Gates:

1. **G1 — speed-isotropy gate (kill gate for Theorem 1).** On the converged ladder, the
   measured speed field at fixed r must be isotropic and equal to √(U² + 2c²σ(r)) within
   apparatus error, across all wind strengths. A converged anisotropy — in particular any
   dipole — refutes the Bernoulli closure of the moving system (and with it the clock
   corollary's cancellation).
2. **G2 — wake-structure measurement.** The direction field's angular structure versus
   the boosted-GP comparator: multipoles of v̂, stagnation geometry, fore-aft asymmetry
   versus U. Measurement, not a kill — this is the model's moving-source *prediction
   being generated*, the input the photon-sector confrontation needs.
3. **G3 — momentum-budget gate.** Net momentum flux balance over the wake (lattice
   units): which of the three consumed-momentum postures the dynamics realize, and the
   drag/thrust scaling with U. Kill only on non-convergence.
4. **G4 — Galilean null control.** Wind with no core: the uniform state must persist with
   consumption exactly zero at apparatus precision (the moving-frame twin of ORB-10751's
   Hubble-silence gate).

Also predeclared as *out of scope here*: rotating sources (the frame-dragging
confrontation needs its own apparatus), finite level-propagation speed (the
retarded-wake family's territory), and any observational fit before G2's wake structure
and the studies note both exist.

### Adjudication (ORB-10935, faraday, 2026-08-21) — the branch is exact, the wake is not the boost, and steady existence is now the question

**Apparatus.** [level-core-wind-tunnel](../../../orrery/lab/sims/level-core-wind-tunnel/)
(orrery `3f08098`): the ORB-10934 3-D draw-sourced elliptic level extended with a uniform
wind, in the comoving-core frame (wind enters only at the upstream face; the level is
solved once per rung and rides with the core). Fixed physical domain (half-width 12) and
core width (σ = 0.75) across a 41³/61³/81³ ladder; wind sweep U/v_GP(r=5) ∈ {0.03, 0.1,
0.3, 1}; consumption stencil byte-identical to ORB-10751 (SHA-256
`aa1155e0…` exact match); deterministic, no RNG, byte-identical rerun verified.
**Method caveat, load-bearing:** the direction field is *constructed* as the positive-x
Hamilton–Jacobi branch of |∇Φ|² = U² + 2σ — the apparatus imposes Bernoulli and asks
whether a globally consistent branch exists and what it looks like. It does not evolve
the rolling rule to a steady state. The gates read accordingly.

1. **G1 — pass, at machine precision.** On the constructed branch, normalized speed
   dipoles are 0.8–2.7×10⁻¹⁶ with low multipoles inside combined apparatus errors of
   1.7–5.8×10⁻⁴, and the pointwise speed matches √(U² + 2c²σ) to ≤3.9×10⁻¹⁶ — for every
   wind strength and both measurement radii, converged. The Bernoulli branch's lattice
   realization is exact; what G1 does *not* test, given the construction, is whether the
   dynamics select this branch.
2. **G2 — measured, converged.** The realized direction field departs from the boosted-GP
   comparator U + v_GP by 0.456–0.732 rad weighted RMS across the sweep — gross, not
   perturbative — with fore-aft mean-n_x asymmetry −0.86…−0.92. And one exact corollary
   surfaced with teeth: **the Bernoulli speed law forbids stagnation points** (q =
   √(U² + 2c²σ) ≥ U > 0 everywhere), while the boosted-GP field has axis speed zeros. A
   moving-mass flow with a stagnation point would refute the speed law outright — a
   qualitative, parameter-free discriminator between the closed system and GR's river.
3. **The predeclared steady-existence measurable returned its wrinkle.** At every swept
   wind the march hits caustics: clip fractions at the finest rung 0.740, 0.713, 0.573,
   0.028 (U ascending), stable across the ladder. No globally smooth steady single-valued
   branch exists in this ansatz. At low U this is partly structural — the U → 0 limit is
   the radial GP inflow, which no positive-x potential graph can represent — but even the
   trans-critical wind clips. Honest reading: the theorems' shared premise (a steady
   irrotational state) has not been shown to be dynamically realized. Steady-wake
   existence — steady non-graph flow, a genuinely unsteady wake, or no attractor at all —
   is now the front's live question.
4. **G3 — pass, converged.** On the constructed branch the consumed +x momentum integral
   has **drag sign at every wind** (posture 3's sign, in lattice units): 14.2, 12.2, 10.7,
   21.5 across the sweep, four-wind fit |∫s·v_x dV| = 20.3·U^0.0976 — nearly
   U-independent, which itself wants explaining if it survives the dynamical apparatus.
   The advective flux-minus-consumed residual is reported, not zeroed: the level-stress
   surface term is deliberately unmodeled.
5. **G4 — pass, exactly.** The pure-wind null: no-core wind states at all four speeds
   keep maximum pointwise consumption ≤2.2×10⁻¹⁷ and speed error exactly zero on every
   rung — the real frozen stencil evaluated on the real lattice, the moving-frame twin of
   ORB-10751's Hubble-silence gate. This one is a true dynamical statement, not a
   construction.

**Declared limits:** one-way draw coupling; finite zero-level Dirichlet box (fixed
physical geometry across the ladder, no infinite-reservoir extrapolation); single-valued
positive-x graph ansatz (the caustic diagnostic is the honest boundary of its
representational reach); advective-only momentum surface term.

**Consequence and successor.** The front's structure after ORB-10935: the *conditional*
content (Bernoulli branch, boost-failure, no-stagnation corollary, drag-sign asymmetry,
Galilean null) is measured and healthy; the *premise* (steady realization) is not. The
successor fixture is the **dynamical-relaxation wind tunnel** (ORB-10937, filed at this
adjudication, faraday, ws_orrery): evolve the actual equations — rolling rule +
continuity + shear — as an initial-value problem from a blended wind/GP start, and let
the dynamics decide. If a steady state emerges, its speed field is a *discovered* test of
Theorem 1 (the kill G1 could not deliver by construction) and its direction field
supersedes G2's branch. If none emerges, the moving closed system is intrinsically
unsteady, and the wake confrontation changes character entirely (time-dependent lensing
residuals, not static wake multipoles).

### Adjudication (ORB-10937, faraday, 2026-08-21) — the dynamics relax slowly, the velocity settles first, and the drag is linear in the wind

**Apparatus.** [level-core-dynamical-relaxation](../../../orrery/lab/sims/level-core-dynamical-relaxation/)
(orrery `eceac3e`): the literal time-dependent system — ∂**v**/∂t + (**v**·∇)**v** = c²∇σ,
∂n/∂t + ∇·(n**v**) = −s, frozen ORB-10751 stencil (SHA-256 `aa1155e0…` exact match),
comoving draw-sourced elliptic level — evolved as an initial-value problem with a
donor-cell finite-volume SSP-RK2 integrator, adaptive CFL, upstream Dirichlet wind,
open outflow faces, and **Bernoulli imposed nowhere**. Fixed physical geometry as
ORB-10935 (half-width 12, core σ = 0.75), same four winds, to T = 60; ladder 25³/33³/41³
(coarser than ORB-10935's — a declared computational bound); deterministic, byte-identical
rerun verified. Two initial conditions (ramped pure wind; wind/GP blend) at (33³, U = 0.3).

1. **G1 — no case steady within the horizon, and the verdict is explicitly
   finite-horizon.** No (U, rung) met the joint predeclared criterion (volume-RMS
   residuals < 2×10⁻³ over the final window) by T = 60; the two finest rungs agree
   categorically at every wind. But the structure of the failure is the finding: the
   **velocity residual meets its half of the criterion at every finest-rung wind**
   (5.2–5.3×10⁻⁴) — only the **density** residual fails (4.5–6.1×10⁻³). The consumption
   trough around the core is still deepening (minimum density 0.27–0.32 and falling),
   decaying at late log-slope −0.0148…−0.0173 per time unit at every wind — a
   U-independent e-folding time of ~65, comparable to the entire horizon. Every case is
   classified `decaying_slowly_not_yet_saturated`: no growing modes, no saturated
   shedding. This reads as *slow relaxation toward a steady balance*, not intrinsic
   unsteadiness — but T = 60 (≲ one e-fold, and shorter than the two lowest winds'
   box-crossing times) cannot adjudicate that.
2. **G2/G3 — executed, empty.** With no admitted steady case, the discovered speed law
   (the Theorem 1 kill this apparatus exists to deliver) and the realized wake
   comparison got no sample. The kill remains undelivered — not dodged: the gates ran
   and predeclared admission simply never triggered.
3. **G4 — the constructed branch's drag scaling did not survive the dynamics.** On the
   realized (time-averaged) flow the consumed +x momentum has drag sign at every wind
   with finest values 0.263, 0.876, 2.60, 8.11 — consumed/U = 61.8, 61.8, 61.1, 57.2,
   i.e. **linear in the wind within ~8% across a 33× sweep** (fit |∫s·v_x dV| =
   55.9·U^0.979, vs the constructed branch's 20.3·U^0.098). All finest adjacent-rung
   shifts pass the 25% convergence target. Linear-in-U is the signature of a
   **fixed-strength sink** — wind-independent volume consumption Q, captured momentum
   n·Q·U; flux capture (area × wind) would be quadratic. The slogan first written here
   said "flux capture" and was corrected at the 2026-08-21 critique; the constructed
   branch's near-U-independence was an artifact of the imposed-Bernoulli ansatz. Ledger stays
   advective-only (no level-stress surface term supplied by the model).
4. **G5 — pass, exactly.** Pure wind, no core, advanced to T = 60 by the identical full
   time integrator: velocity and density preserved exactly, consumption at floating
   precision on every rung and wind. The dynamical Galilean null holds.
5. **Attractor uniqueness — unresolved.** The two initial conditions remain distinct at
   T = 60 (relative L² differences 0.40 velocity, 0.39 density); since neither is
   steady, this measures transient memory, not attractor multiplicity.

**Declared limits:** T = 60 shorter than the two lowest winds' box-crossing times
(finite-horizon wording throughout); bounded 25³/33³/41³ ladder with donor-cell
truncation diffusion quantified only by adjacent-rung shifts; one-sided zero-gradient
open faces may reflect nonlinear structure; density positivity floor recorded per case;
advective-only momentum surface ledger.

**Consequence and successor.** The binary the previous adjudication posed — steady state
or intrinsic unsteadiness — was the wrong shape: the dynamics returned *slow relaxation,
unresolved at horizon*. The velocity-first settling and the U-independent density decay
rate point at a specific mechanism: the trough deepens until consumption (s ∝ n) falls
to what the wind resupplies, so the balance depth and the settling time are set by the
local consumption rate, not the wind — and if the ~65 e-fold holds, a horizon of several
hundred time units should either settle every case or show the decay stalling. That is
the successor: the **extended-horizon relaxation** (filed at this adjudication, faraday,
ws_orrery) — same apparatus, T ≥ 600 (~9 observed e-folds), sectoral residuals and a
trough-saturation diagnostic predeclared, global mass budget (boundary influx vs ∫s dV →
balance) as the steady-approach signature, and the same inherited kill: any admitted
steady case's speed field is the discovered test of Theorem 1.

By amendment at the 2026-08-21 critique triage, the successor (ORB-10938, adjudicated in
the third § below) also
predeclares: **cavitation as a named outcome and kill** (track n_min(t) toward a finite
floor vs toward the positivity cutoff — n → 0 voids the excitation reading around every
moving mass); the **early velocity-sector Bernoulli residual** (Theorem 1 is a statement
about **v** alone, and the velocity sector already meets its criterion — measure
|v|² − U² − 2c²σ on any settled velocity sector without waiting for the density to
finish); adjacent-rung agreement on the decay *slope* (the ~65 e-fold is the most
artifact-prone number in ORB-10937 — donor-cell diffusion acts as an effective
relaxation rate); and ‖∇×v‖ on every case (a velocity sector that settles with growing
curl fails Theorem 1's irrotational premise numerically). A photon-sector modulation
scale estimate is filed alongside (ORB-10939 — acoustic ray tracing across candidate
direction fields vs boosted Schwarzschild; a bracket, not a falsifier, the direction
field being exactly the unsettled quantity).

### Frame critique and arbitration (grok, Daniel — 2026-08-21): the comparator moves to the right frame

A requested outside critique of this doc (orchestrator inbox,
msg-2026-08-20-moving-sources-closed-system-critique) was arbitrated by Daniel and
reconciled in this change-set. Accepted and folded in place: the boosted-GP comparator
is GR's lab-frame coordinate picture, not a GR observable (Theorem 2 restated —
mass-frame GR is Schwarzschild; the speed-dipole and axis-stagnation contrasts demoted
to Galilean-picture comparisons); the clock corollary's "cancels by structure"
retracted; the linear drag re-read as a fixed-strength sink with a posture-3 timescale
bound; cavitation vs finite floor named as the trough's undistinguished end-states;
Theorem 1's velocity-only character exploited (early Bernoulli residual on a settled
velocity sector); the matching-region and local-orbital-wind sharpenings under § what
sets U; the two-causalities note under § setup; the multi-source caveat under Theorem 1.

Where the arbitration trimmed the critique — recorded so the ledger does not overclaim
in the other direction:

1. The U² term in g₀₀ is *second* order in U; genuinely first-order effects arise
   through the wake/g₀ᵢ sector — which is where Theorem 2's observables already pointed.
2. U/c ~ 10⁻³ is not directly comparable to PPN α₁/α₂ — the effective metric must first
   be reduced to observable PPN coefficients. That reduction is now a named obligation
   of this front.
3. Neither the cancellation nor the observability of the common U² clock term is
   established: a uniform flow can be coordinate-like for excitations. Only relational
   clock/orbital predictions settle it.
4. Ray tracing cartoon direction fields is a *scale estimate*, not a falsifier — the
   direction field is exactly the unsettled quantity. ORB-10939 is scoped accordingly:
   its primary deliverable is the cross-field spread of the modulation, which quantifies
   how much the photon sector is hostage to the relaxation outcome.

Actions in this change-set: the theorem and ledger restatements above; ORB-10938 amended
(cavitation outcome, early velocity-sector residual, slope convergence, curl reporting);
ORB-10939 filed (photon-sector modulation scale, medium, ws_orrery).

### Adjudication (ORB-10938, faraday, 2026-08-21) — the system settles, the settled flow is not Bernoulli, and the trough cavitates at intermediate wind

**Apparatus.** [level-core-dynamical-relaxation](../../../orrery/lab/sims/level-core-dynamical-relaxation/)
(orrery `3246ace` — the same catalog entry evolved in place, per the same-model rule): the
identical donor-cell SSP-RK2 physical apparatus as ORB-10937 (frozen ORB-10751 stencil,
SHA-256 `aa1155e0…` exact match; Bernoulli imposed nowhere), run from fresh initial
conditions to **T = 600** (~9 observed e-folds) at 33³ and 41³ for all four winds, plus a
full-horizon **61³ anchor at U/v_GP = 0.3** — the full requested horizon was feasible, no
tradeoff taken. The 2026-08-21 amendment is fully incorporated (cavitation as a separate
ladder-confirmed verdict; velocity-sector admission for the Bernoulli residual;
adjacent-rung slope/n_min convergence; all-case curl). Deterministic; byte-identical
rerun verified; both ORB-10937 initial conditions continued together at (33³, U = 0.3).

1. **G1 — every case settles; and the cavitation kill fires.** All nine (U, rung) cases
   meet the joint volume-RMS criterion by T = 600, both sectors, matching verdicts on
   adjacent rungs — the slow-relaxation reading was right and the front's premise
   question is answered: the moving closed system reaches a settled state. But the
   predeclared cavitation diagnostic separates locally: at **U/v_GP = 0.3** the
   trough-minimum trajectory is a cutoff-ward candidate on every rung (n_min
   3.4×10⁻³ → 2.2×10⁻³ → 1.3×10⁻³ across 33³/41³/61³, still draining, extrapolated
   cutoff contact accelerating with refinement), with candidate agreement on both
   adjacent-rung pairs — **the predeclared branch-kill criterion for the excitation
   reading, met**. U/v_GP = 1 saturates at a real floor (n_min ≈ 0.2, the only
   trough-saturated case); the two low winds are 41³-candidates without 33³ agreement —
   unconfirmed, trending cutoff-ward. Caveat as recorded: ladder-agreed extrapolation,
   not cutoff contact.
2. **G2 — flux balance tracks the wind.** Late influx/consumption ratios: 0.40–0.43
   (U/v_GP = 0.03), 0.66–0.67 (0.1), 0.93–0.95 (0.3, all three rungs), 0.998–0.999
   (1.0), all with late trends ~10⁻⁵/time — the settled states balance at trans-critical
   wind and sit in a slowly-fed deficit at sub-critical wind, consistent with the
   still-draining trough minima.
3. **G3 — the Theorem 1 kill, delivered.** On velocity-settled, rung-converged samples
   the squared Bernoulli residual |v|² − U² − 2c²σ has relative RMS **0.121 (r = 3) and
   0.447 (r = 5)** at 41³, U/v_GP = 0.3 — beyond combined temporal/resolution error,
   with the 61³ anchor (0.145 at r = 3) independently beyond error — and normalized
   speed dipoles 0.04–0.24 where the imposed branch had 10⁻¹⁶. The dynamics settle to a
   flow that is **not** the Bernoulli closure. Fixture verdict:
   `bernoulli_closure_refuted_on_converged_velocity_sector`.
4. **G4 — the realized wake is the marched branch's geometry, without its speed law.**
   Direction-field multipoles at U/v_GP = 0.3 (41³ and 61³, r = 3 and 5) differ from
   ORB-10935's marched branch by 0.016–0.18 and from boosted GP by 0.30–0.37. No
   stagnation point anywhere (minimum interior speed ~0.043 ≈ U at the domain corner —
   far from the threshold). Vorticity is finite at settlement and rung-stable at
   U/v_GP = 0.3 (RMS 0.0148 → 0.0150 across 41³→61³): the settled flow is rotational —
   Kelvin's premise fails in the realized dynamics, which is *where* the Bernoulli
   closure loses its footing.
5. **G5 — the drag law moves again at settlement.** Late-time 41³ fit
   |∫s·v_x dV| = **81.24·U^1.332** — superlinear, against the transient linear
   55.9·U^0.979 (measured/transient-fit 0.23, 0.26, 0.43, 0.76 ascending in U) and the
   constructed branch's 20.3·U^0.098. Drag sign at every wind persists. Reading: the
   transient linear law was the deepening-trough era; the settled trough depth is
   U-dependent (deep at low U, floor at high U), so the settled consumption–momentum
   product picks up extra wind dependence. The posture-3 BHL bound (§ consumed momentum)
   was premised on linear and needs recomputing on the settled law.
6. **G6 — the dynamical Galilean null holds to T = 600** on every executed rung and wind.
7. **Attractor probe — same attractor.** Both ORB-10937 initial conditions settle to the
   same state: final relative L² differences 0.75% (velocity), 0.25% (density).

**Declared limits:** the cavitation kill is extrapolation-based (see G1 caveat); only
U/v_GP = 0.3 has a 61³ anchor (the four-wind ladder ends at 41³); open-face treatment,
donor-cell diffusion, density floor, and the advective-only momentum surface ledger
remain the documented apparatus limits.

**Consequence.** The front's premise question is closed and both theorems come down with
it as *realized* descriptions: the moving closed system settles, but into a rotational,
anisotropic-speed flow the exact algebra does not describe, with the direction geometry
the marched branch already sketched. The live objects are now (i) the **realized wake
field itself** as the model's moving-source prediction — ORB-10939's ray tracing should
bracket the photon sector against *this* field, which exists in the catalog; (ii) the
**cavitation kill** at sub-critical wind — either the excitation reading is dead around
slowly moving masses or the closed system is missing physics that floors the trough
(a pressure/EOS term, level backreaction — nothing currently in the rules provides it);
(iii) the **PPN reduction**, which must now start from the realized settled flow, not
from √(U² + 2c²σ) — executed 2026-08-28 as
[ppn-reduction-of-the-settled-flow](../ppn-reduction-of-the-settled-flow/) (ORB-11039).
No successor lattice fixture is filed at this adjudication: the next
moves are theory-side (kepler) and the already-filed ORB-10939.

**Moving-source bounds studies note (kepler, ws_principia — filed with this doc).** The
sourced walls Theorem 2's confrontation needs: gravitational aberration in GR (the Carlip
cancellation), preferred-frame PPN parameters α₁/α₂ and their current bounds, moving-lens
deflection measurements, frame-dragging measurements, and gravitational Cherenkov
constraints — the note [moving-source-field-consistency](../moving-source-field-consistency/)
and [retarded-scarcity-wake](../retarded-scarcity-wake/) already demanded, now needed by
three docs.
