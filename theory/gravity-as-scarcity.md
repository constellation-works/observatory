---
title: "Gravity as the gradient of scarce space"
status: growing
families: [gravity-as-scarcity]
almanac: 15-discussions/26-07/gravity-as-scarcity-of-space.md
created: 2026-07-09
updated: 2026-07-12
---

# Gravity as the gradient of scarce space

**The idea.** Gravity is not a force law but the gradient of a stored scalar — "scarcity of
space" — computed on a lattice by counting points in spherical shells around masses. A mass
depletes a finite budget of space; particles roll down the scarcity gradient. Built up over a
discussion thread (see `almanac` link) that repeatedly found the toy model rediscovering real
physics: Gauss's law from budget-division bookkeeping, Yukawa-like cutoffs from budget
exhaustion, MOND-flavored behavior, and frame dragging from adding swirl.

**Current verdict:** *right shape; magnitude no longer clearly wrong once **fit** rather than
predicted — but physically unvalidated.* The discussion's verdict was "right shape, wrong
magnitude": the *predicted* headroom boost ran ~10–25% where galaxies need ~2×. The first
confrontation with real data (Faraday's ORB-10077 fit, see below) sharpens this: with one free
shape parameter β, the scarcity curve fits Tycho's Gaia DR3 rotation curve decisively better than
the nested no-halo baryons control. But beating baryons-alone is *table stakes* — every
dark-matter and modified-gravity idea does; that is the dark-matter problem, not evidence for
scarcity. The comparison that matters — a standard NFW halo, penalized for its extra parameter —
has now run (ORB-10082, see below): the point estimate favors scarcity on every profile variant,
but the bootstrap says the sample cannot decide (95% CI spans zero), and NFW slightly wins the
held-out band. Held verdict, consistent with the almanac postscript (2026-07-10): **decisively
better than the no-halo control; statistically undecided against a standard halo; shape
promising; physically unvalidated.**

The ORB-10156 derivation (2026-07-12, § below) sharpened both ends of that verdict. Derived
rather than assumed: the model's photon sector comes out at PPN γ ≤ 0 in every reading the
lattice supports, against Cassini's γ − 1 = (2.1 ± 2.3)×10⁻⁵ — **as a complete theory of
gravitation, the model as stated is refuted by the light sector**; and the multiplicative
superposition rule was announced as the *derived* local behavior (depletion on a shared
budget is anonymous), attaching the ORB-10097 Uranus tension to the model proper with no
derived screened fallback — a derivation since refuted by measurement (ORB-10157, below).
What survives is exactly the distinctive part: the massive-sector galactic
phenomenology (the β-headroom boost), plus a named completion path — a screened scalar-tensor
structure the counting mechanic does not yet supply — recorded in
[studies/scalar-gravity-ppn-constraints](../studies/scalar-gravity-ppn-constraints.md).

The ORB-10159 derivation (2026-07-12, § clock sector below) then closed the other measured
gap: the static model predicts **zero gravitational time dilation** and is refuted by the
clock ladder outright; the accumulating variant is refuted by the LLR Ġ/G bound. What
survives is derived, not chosen: a steady-state completion in which space itself obeys the
model's one rolling rule — free-falling into consuming masses at exactly the
Gullstrand–Painlevé profile (½v² = c²σ, Schwarzschild clocks exact, the static Σ 1/count
field returning as the flow's comoving time-integral) — with matter and light as
excitations *of* the lattice (Unruh analog-gravity family; the aether/substance reading is
excluded by 9–12 orders against resonator bounds). On that branch the photon sector
*conditionally reopens with the right sign* (flow drag supplies γ = 1 exactly), the lattice
rest frame stays hidden (emergent Lorentz invariance, spacing bounded to ≲ 10⁸ ℓ_Pl by GRB
dispersion), and the multiplicative β factor is provably invisible to every current clock
instrument. The completion's price is two owed ingredients, each gated on a proposed
faraday sim: the volumetric consumption law the free-fall flow demands (**ORB-10162**) and
excitation dynamics on a flowing lattice (**ORB-10158**, scope extended).

The first of those gates has since closed **against the mechanic** (ORB-10162, 2026-07-12,
§ lattice adjudication below): run to steady state, both of the model's natural consumption
rules lock in exactly the two refuted flow laws — central-only is flux-conserving,
v ∝ r^(−2.00062 ± 0.00002); equal-per-shell is the budget flow, v ∝ r^(−0.99454 ± 0.00036) —
with per-shell sink scaling measured flat, r^(0.00029 ± 0.00026), where free-fall demands
r^(1/2). Per the predeclared gate **the river completion is refuted at the mechanic level:
the GP flow does not emerge from the existing counting rules.** It survives only as the
analytic conditional ORB-10159 derived — space obeying the rolling rule yields GP exactly —
whose r^(−3/2) volumetric destruction law is now a *measured* debt: impose it as a named
postulate, derive it from S2 substrate dynamics (**ORB-10161 Branch B's standing
obligation**), or concede the clock sector. The measurement also returns the verified static
1/r field *without* a comoving flow history (central-only's comoving dilution is zero before
the sink), so the static sims no longer lend the river reading ambient support.

The second gate closed the same day, against the other derived rule (ORB-10157, 2026-07-12,
§ superposition adjudication below): on a shared-budget counting lattice, an embedded compact
source's field follows **A(D) = (1−D)^1.071** — headroom screening, the turn-7 rule at unit
gain — not the β-amplified q-ratio ORB-10156 derived and ORB-10097 integrated, not
inverse-headroom enhancement (log-RMSE 2.077), and not independence (1.074). Anonymity forces
only survivor-fraction screening; the multiplicative rule is refuted *as a derivation* and
survives only as an identification hypothesis — the fitted galactic boost read as the
measured modulation, at the price of O(1) ambient occupancy depletion across the disk. The
ORB-10097 Uranus tension is accordingly **conditioned, not detached**: on the identification
it stands with the same integrated numbers (the boost's fitted local log-gradient transfers
to the Sun's field unchanged); without it, ORB-10097 tested a rule the mechanic doesn't
supply. The exactly-Newtonian escape stays closed either way — independence is measured
dead.

## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| Accumulated per-shell dilution Σ 1/count(k) ∝ 1/r, so "gravity = gradient of scarcity" reproduces Newton's 1/r² | supported | by construction in [scarcity-grid-weight-black-hole](../../orrery/lab/sims/scarcity-grid-weight-black-hole/), [scarcity-capped-cumulative-field](../../orrery/lab/sims/scarcity-capped-cumulative-field/); note: storing 1/r² and differentiating gives 1/r³ — the stored field must be potential-like (correction #1 in the thread) |
| Dividing a fixed budget across shells yields inverse-square from pure geometry (Gauss's law analog) | supported | [scarcity-shell-depletion-field](../../orrery/lab/sims/scarcity-shell-depletion-field/) |
| Subtractive budget gives a hard cutoff radius r ≈ (3T/4π)^⅓ beyond which gravity dies (Yukawa-cartoon) | supported | [scarcity-capped-cumulative-field](../../orrery/lab/sims/scarcity-capped-cumulative-field/), [scarcity-star-well-headroom](../../orrery/lab/sims/scarcity-star-well-headroom/) — as a property of the *model*; no claim it matches nature |
| An extended (distributed) mass under the model bends rotation curves toward flat (dark-matter/MOND-adjacent) — the *shape* | supported | Qualitative: [rotation-curve-distributed-mass](../../orrery/lab/sims/rotation-curve-distributed-mass/). Quantitative: fit to real Gaia DR3 data ([scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/), ORB-10077) — with one free β the scarcity shape beats the nested no-halo baryons control decisively (RMSE 2.70 vs 18.40 km/s; ΔAIC ≈ −10⁵, stable across 27 profile variants). Measured curve & data lineage: [studies/milky-way-rotation-curve](../studies/milky-way-rotation-curve.md) |
| Fit to real MW data, the scarcity model **matches or beats a standard dark-matter halo once AIC penalizes parameter count** | mixed | **ORB-10082 ran** ([scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/), orrery `a9f93bd`) — reframed by Daniel before execution: NFW+baryons keeps a free baryonic scale plus M200 and concentration (3 physical params vs scarcity's 2; no longer equal-dof, AIC penalizes the extra). Point estimate favors scarcity — RMSE 2.70 vs 3.66 km/s, ΔAIC(scarcity−NFW) = −1663, same sign on all 27 profile variants (−2293 to −847) — **but the 200-resample bootstrap 95% CI spans −4129 to +1102 → statistically inconclusive, not a scarcity win**. Cutting the other way: NFW slightly wins the held-out band (4.99 vs 5.26 km/s RMSE) and flips the coherent residual sign; NFW is itself weakly identified here (drift pinned at its 10 km/s *upper* bound, c ≈ 37 — far above a typical MW-mass halo), so the 5–15 kpc band limits what the comparison establishes *in either direction*. Gate: **ORB-10083** (radially varying drift, applied identically to all three models) |
| The fitted scarcity model is an *absolute* description of the MW rotation curve | mixed | Reduced χ² ≈ 145 against the quoted statistical errors — a formal failure — but those errors omit dominant distance/selection/asymmetric-drift systematics, so even the true law would fail them (not a refutation). Held-out 15–18.75 kpc band: coherent one-signed ~4.9 km/s underprediction — the data flattens near 13–16 kpc where the model keeps declining; the shape term is *sufficient relative to the control, not complete*. Drift nuisance pinned at its 3 km/s lower bound and weakly identified → a radially-varying asymmetric-drift model (Faraday **ORB-10083**) is prerequisite to any stronger claim. See [scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/) |
| The fitted scarcity form leaves solar-system ephemerides (AU scale) inside observational precision | mixed | Constraint from the measured Newtonian-omission floor ([studies/solar-system-ephemeris-precision-floor](../studies/solar-system-ephemeris-precision-floor.md); Uranus rms 4.1e-9 AU is the tightest). **ORB-10097 ran** (Faraday; [solar-system-nbody](../../orrery/lab/sims/solar-system-nbody/) `scarcity/`, orrery `23fe253`, § below): the **multiplicative reading**, integrated on the exact ORB-10093 protocol with β and F(u) imported unchanged, puts **Uranus above its floor in the primary galactocentric orientation — 1.89× rms, 2.84× max** (7.7e-9 vs 4.1e-9 AU rms); the other seven planets stay below (Saturn next at 0.74×). Qualification: the six-axis orientation envelope **crosses** the Uranus floor (rms 0.66×–3.0×), so this is tension under the physically-motivated orientation, *not* an orientation-independent refutation. The **screened reading is identically Newtonian** — the explicit zero control — and is **unconstrained by this test**. **ORB-10156 update, reversed by measurement (ORB-10157):** the multiplicative reading was briefly the *derived* local behavior; the lattice measurement (superposition rows below, § superposition adjudication) has since refuted the derivation — the mechanic's own modulation is survivor-fraction headroom screening A(D) = (1−D)^1.07079, unit gain, keyed to *local occupancy*, not the β-amplified q-ratio this run integrated. The tension is now **conditioned, not derived**: it stands iff the fitted galactic boost is identified with the measured screening law (which demands O(1) ambient occupancy depletion across the disk — a normalization nothing has fixed); on that identification the boost's fitted local log-gradient (3.2×10⁻¹⁰/AU) transfers to the Sun's field unchanged and every integrated number here stands; without it, this run tested a transplanted rule the mechanic doesn't supply. The anticipated "honest out" (a lattice computation moving the log-gradient at O(1)) was used, and overshot: the lattice moved not the gradient but the rule's derivational status — though, as anticipated, neither the sign nor the *existence* of the modulation moved (the exemption reading — the Sun generating as if alone, ephemerides exactly Newtonian — is measured dead at log-RMSE 1.074, so the tension cannot be dissolved by exemption, only relocated by normalization). Result: [summary.json](../../orrery/lab/sims/solar-system-nbody/scarcity/summary.json) |
| Adding swirl to the scarcity field reproduces frame dragging | mixed | [frame-drag-swirl](../../orrery/lab/sims/frame-drag-swirl/) — right shape; real frame dragging (Lense–Thirring) has specific magnitude/falloff this toy hasn't been checked against (`conjecture — to verify`: study note needed) |
| The scarcity picture is equivalent to weak-field GR's "gradient of time-flow rate" heuristic | mixed | **Worked computation (ORB-10156, § derivation below):** exact where the heuristic applies — both dynamics are a = c²∇σ with σ = GM/c²r, so scarcity coincides with the clock-rate deficit 1 − √(−g₀₀) point-by-point, and no static weak-field slow-motion massive-particle experiment can distinguish them. *Not* equivalent as a full weak-field account: the model has no mechanism making depleted regions tick slow (σ = clock deficit is a postulate, not counting — though if added, gravitational redshift comes out right for free), and the heuristic is only the g₀₀ half of a metric whose other half (Ψ) the model lacks — a measured difference (photon row). [studies/scalar-gravity-ppn-constraints](../studies/scalar-gravity-ppn-constraints.md). **ORB-10159 update:** on the river completion the missing clock mechanism is supplied — σ = ½v²/c² is *SR* dilation of a clock at rest in the free-fall inflow, and the identity σ = 1 − √(−g₀₀) becomes the exact GP lapse (§ clock sector (b)). **ORB-10162 update:** that mechanism now rests on an *imposed* flow — the mechanic's natural rules measurably do not produce it (river row below) |
| Light couples to scarcity so as to reproduce measured deflection and Shapiro delay (the photon sector; PPN γ) | refuted | **Derived, not assumed (ORB-10156, § below):** every photon coupling the lattice supports fails — photons blind to the field give zero deflection/delay (Nordström's fate); photons coupled to the stored time-potential give γ = 0 (half-GR: 0.875″ limb deflection, half Shapiro); the literal hop-on-depleted-lattice reading gives the wrong *sign* (light speeds up where points are sparse → bends away, Shapiro advance) with a non-PPN 1/r² profile. Best case \|γ − 1\| = 1 vs Cassini's (2.1 ± 2.3)×10⁻⁵ and VLBI's ~10⁻⁴ ([studies/scalar-gravity-ppn-constraints](../studies/scalar-gravity-ppn-constraints.md)). The hoped-for outcome — the lattice yielding time- and space-facing effects at the γ = 1 ratio — is **negative**: it would need a tick-rate deficit *and* a proper-space *excess* of GM/c²r each, and the mechanic supplies neither (depletion has the wrong sign for Ψ). Kills the model **as a complete theory of gravity as stated**; the galactic massive-sector result is untouched. Lattice-level check of the sign claim: proposed faraday task **ORB-10158**. **ORB-10159 update:** stands as stated (static lattice); the dynamical excitation completion conditionally reopens the sector with the *right* sign — flow drag supplies the γΦ half exactly (γ = 1) — see the excitation-completion row below and § clock sector (e); ORB-10158's scope extended with a flowing-lattice arm |
| The local superposition rule is multiplicative — accumulated background depletion modulates an embedded source's field generation with the fitted q-ratio coupling; screening does not arise | refuted | **Derived (ORB-10156, §(d) below), then measured against (ORB-10157, [lattice-two-source-superposition](../../orrery/lab/sims/lattice-two-source-superposition/), § superposition adjudication below):** the derivation ran — the fitted boost is literally a position-dependent coupling G_eff(r) = G·q(r)/q(R₀); depletion on a shared budget is anonymous; *therefore* an embedded source generates with the background's coupling. Set `supported` 2026-07-12; superseded the same day. The lattice measured the mechanic's actual modulation as **A(D) = (1−D)^1.07079** (log-RMSE 0.0031 vs 2.077 for the inverse-headroom enhancement operationalization and 1.074 for independence) — survivor-fraction screening at unit gain in *local occupancy*, carrying no imprint of a β-amplified response to *accumulated* dilution. The failing step is the transplant: anonymity licenses only "embedded sources are not exempt" — it does not make the fitted macroscopic factor the mechanic's transfer function; a coupling that responds to ambient occupancy with the fitted gain is a rule the counting mechanic does not contain (faraday's declared caveat: an occupancy-dependent attempt rate is a *different microscopic model*). What survives of the derivation: the anonymity argument itself (independence refuted — the exemption ORB-10097 called "screened" does not arise, so the old σ_sun < σ_gal level-vs-gradient point stands with its variable transposed), and the sign (the integrated factor was suppression-signed, like the measured law; the gap is gain and variable, not direction). Superposition question reopened with sharper alternatives (open questions below) |
| The mechanic's measured superposition rule is headroom screening: an embedded source's field scales as the local survivor fraction, A(D) = (1−D)^1.071, with no exhaustion upturn | supported | **Measured (ORB-10157, [lattice-two-source-superposition](../../orrery/lab/sims/lattice-two-source-superposition/), § superposition adjudication below):** 129² shared-budget lattice, 50,000 anonymous slots/cell, compact source (peak exposure 0.1) embedded in an extended disk well; sweeping ambient depletion D = 0.01–0.90 (12 levels, 32 replicates, seed 42, byte-identical reruns; all finite-count means within 2.31 SE of the exact binomial expectation), A(D) = (1−D)^1.07079, log-RMSE 0.0031; resolution checks 1.0725 (97²) / 1.0700 (161²), amplitude shifts ≤ 4.4×10⁻⁴; exponent excess over 1 attributed to spatially varying headroom across the 4–18-cell measurement annulus. Continuous suppression through exhaustion — amplitude 0.1790 at D = 0.80, 0.0029 at 0.995, no upturn. This is the turn-7 headroom rule (wells dug from remaining capacity) returned by the mechanic at unit gain — same family as the fitted q(r) boost (suppression; boost rising where depletion falls); it reproduces the *fitted* galactic form only under the O(1)-occupancy identification (§ below). Caveats (2D static pinned geometry, anonymous fixed-coupling attempts, declared-not-emergent profiles) scope extrapolation, not this verdict |
| The model as stated (static or accumulating depletion, no clock mechanism) is consistent with measured gravitational time dilation | refuted | **Derived (ORB-10159, § clock sector below):** a static scarcity field with universal tick rate predicts exactly zero dilation against the measured ladder — Pound–Rebka/Snider at 1%, Gravity Probe A tracking the GM/r *profile* to 7×10⁻⁵, GPS +38.6 μs/day as engineering fact, optical clocks resolving 1 mm ([studies/gravitational-time-dilation](../studies/gravitational-time-dilation.md)). The accumulating variant (consumption, no replenishment) is separately dead: σ̇/σ ~ 1/t_age ≈ 2×10⁻¹⁰ yr⁻¹ is an effective Ġ/G more than three orders above the LLR bound (7.1 ± 7.6)×10⁻¹⁴ yr⁻¹. Only the steady-state flow (river) branch survives as a dynamical completion — next row (where ORB-10162 has since measured the mechanic's natural rules failing to produce it) |
| The dynamical-consumption flow law is the free-fall (Gullstrand–Painlevé) river ½v² = c²σ = GM/r — i.e. the mechanic's own dynamics produce it; flux-conserving and budget-per-shell flows are refuted | refuted | **Derived (ORB-10159, §(b)), then measured (ORB-10162, [dynamical-consumption-lattice](../../orrery/lab/sims/dynamical-consumption-lattice/), orrery `98396a8`, § lattice adjudication below):** faraday's dynamical-consumption lattice, at steady state (1e-9 stationarity; byte-identical reruns), locks in exactly the two refuted flows over 1.7 decades of radius — central-only v ∝ r^(−2.00062 ± 0.00002) (flux-conserving, the predeclared kill condition), equal-per-shell v ∝ r^(−0.99454 ± 0.00036) (budget flow) — with per-shell sink scaling r^(0.00029 ± 0.00026), cleanly discriminating the implemented r⁰ draw from the r^(1/2) the free-fall branch demands. Neither natural rule self-organizes toward GP; σ = v²/2c² fails on both branches (7–8 dex, apparatus hop-speed c — expected, since neither branch *is* GP). **Per the predeclared gate the river completion is refuted at the mechanic level: the existing counting rules do not produce the free-fall flow.** What survives, exactly: the analytic branch-3 result — space obeying the rolling rule yields GP, Schwarzschild clocks exact, σ = ½v²/c² = 1 − √(−g₀₀) — as a *postulate* whose sustaining r^(−3/2) volumetric destruction law is now a measured debt, not just an analytic one. Cutting both ways: central-only's standing deficit reproduces the finite-reservoir 1/r field (R² 0.99999992) while its comoving dilution is zero pre-sink — the verified static shape returns as a diffusion profile, *not* a flow record (snapshot reconciliation in § below). Remaining routes: impose the rule by hand, derive it from S2 substrate dynamics (**ORB-10161 Branch B's obligation**, [two-substance-vortex-vacuum](two-substance-vortex-vacuum.md) §B2), or concede the clock sector. Apparatus caveats (radial shell reduction; apparatus-specific c normalization) recorded in § below — neither gates this verdict ([studies/river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md)) |
| Matter coupling: only the excitation (analog-gravity) reading lets the river buy time dilation while the lattice ontology does work | supported | **Derived by elimination (ORB-10159, §(c)):** the rules as stated make matter an external tracer reading ∇σ — a tracer inherits no SR-in-the-flowing-frame, so the river buys it no dilation (the drag objection is fatal: no coupling constant exists to carry it). The deflationary reading is exactly GR in GP coordinates — consistent, ontology idle (Hamilton & Lisle's own caution: nothing measurable flows). The excitation reading — matter as waves *of* the lattice, **Unruh 1981 acoustic-metric family, riding the GP river** — makes carriage constitutive with no coupling constant, and is the only reading delivering the clock sector with the ontology live. Price: excitation dynamics with one universal local speed is new structure the rules don't yet contain ([studies/river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md)) |
| On the excitation branch the lattice rest frame is undetectable at current bounds (emergent Lorentz invariance); the substance/aether branch is excluded | supported | **Computed (ORB-10159, §(d)):** substance coupling at O(1) predicts resonator anisotropy ~β²: 1.5×10⁻⁶ (370 km/s CMB-frame motion) down to 2×10⁻⁸ (fully entrained, 42 km/s local solar inflow) vs measured 10⁻¹⁷–10⁻¹⁸ — **excluded by 9–12 orders**. Excitation branch: one medium, one limiting speed → MM null by construction; residual lattice-scale dispersion is bounded, not excluded — parity-symmetric hop rules give a quadratic subluminal term, and GRB 090510 (E_QG,2 > 1.3×10¹¹ GeV) bounds the spacing to a ≲ 1.5×10⁻²⁷ m ≈ 10⁸ ℓ_Pl; parity-asymmetric rules (linear term) are already excluded past the Planck scale (E_QG,1 > 7.6 E_Pl). **Placement: emergent-metric, analog-gravity family** — not an aether, not relabeled GR ([studies/lorentz-violation-bounds](../studies/lorentz-violation-bounds.md)) |
| Under the excitation completion (free-fall flow, depletion as flow not standing deficit, universal local hop speed) the photon sector is exactly Schwarzschild's: γ = 1, deflection toward, Shapiro delay | mixed | **Computed (ORB-10159, §(e)):** a wave with constant local speed on GP inflow sees the acoustic metric with uniform c — exactly the Schwarzschild geometry (Unruh), so the γΦ half that the static mechanic provably cannot supply (photon row above) is delivered entirely by flow drag. The mathematics is exact and established; the row is `mixed` because all three premises are currently *owed postulates*, and any residual standing density deficit re-introduces the wrong-signed 1/r² index term as a contaminant whose absence Cassini/VLBI bound. The ORB-10156 refutation stands for the model as stated. **ORB-10162 update:** the free-fall-flow premise took its measured hit — neither natural counting rule produces it (river row above) — so all three premises now stand as imposed postulates (the flow's destruction law owed to S2 dynamics, ORB-10161 §B2); the acoustic-metric mathematics is untouched. Gate: **ORB-10158**, scope extended 2026-07-12 with a flowing-lattice arm (sign of deflection under inflow) alongside the static arm (contaminant magnitude) |
| The multiplicative β factor leaves all current clock comparisons unaffected — clocks are not a second instrument on the ORB-10097 branch | supported | **Computed (ORB-10159, §(f)):** the multiplicative rule (derived by ORB-10156; since measured to be the mechanic's behavior only under the fitted-boost identification — ORB-10157, superposition rows above) rescales locally generated σ by X(r_gal), \|X − 1\| ≤ 3.2×10⁻¹⁰ per AU of galactocentric offset — a branch property, holding for *any* multiplicative carrier of the fitted boost shape, the measured screening law included. Fractional correction to any measured redshift ≤ 3×10⁻¹⁰ vs 2.5×10⁻⁵ best accuracy (five orders below); annual species-universal rate modulation ~3×10⁻¹⁸ vs 10⁻¹⁶-class comparisons (and blind to LPI/null-redshift tests *because* universal; ~16 ps/yr vs ~100 ns pulsar timing); terrestrial differentials ≲ 10⁻²¹ vs 10⁻¹⁸ optical-clock systematics. Orbits integrate accelerations twice over decades, clocks read rates instantaneously — the binding instrument on the multiplicative branch remains ORB-10097's Uranus channel ([studies/gravitational-time-dilation](../studies/gravitational-time-dilation.md)) |

## Confronting real data — the ORB-10077 rotation-curve fit

The first time the model met measured data. Faraday (Sol, ORB-10077) took turn 9's headroom idea
in continuum form — v_S² = v_N² · q(r)/q(R₀) with q(r) = exp[−β ∫ F(u)/u² du], β the one free
shape parameter — and fit it in real units to Tycho's Gaia DR3 median-`v_φ` curve (ORB-10075
lineage), under a **predeclared** protocol: fit 5–15 kpc, hold out 15–18.75 kpc, same bounded
asymmetric-drift nuisance for model and control, decisive only if |ΔAIC| ≥ 10 with consistent
sign across all 27 mass-profile variants. Apparatus: [scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/)
(commit `9008d5b`); Faraday run record `agentbase/faraday/memory/runs/26-07/run-20260710T001006.md`.
**I did not modify the apparatus; questions about it became Faraday tasks (below).**

| Metric (5–15 kpc fit) | Scarcity | Newtonian baryons (nested control) |
|---|---:|---:|
| Baryonic mass | 1.204 × 10¹¹ M☉ | 1.224 × 10¹¹ M☉ |
| Scarcity β | 5.25 kpc | 0 (control) |
| Drift nuisance | 3.0 km/s (pinned at lower bound) | 3.0 km/s |
| RMSE | 2.70 km/s | 18.40 km/s |
| χ²/dof | 2458.8 / 17 | 102877 / 18 |

ΔAIC = AIC_scarcity − AIC_Newtonian = **−100416** (bootstrap [−134303, −59098]; profile-variant
range −158602 to −51749). Held-out 15–18.75 kpc: scarcity RMSE 5.26 km/s (mean underprediction
4.86 km/s) vs 31.16 km/s for the control. Lattice-convergence and outer-boundary changes move
predictions by ≤ 0.00014 km/s.

**How the evidence moves the theory (per the standing rules):**

1. **Gate on an equal-dof competitor, not the nested control.** The ΔAIC ≈ −10⁵ is against
   baryons-alone — table stakes; the whole point of the dark-matter problem is that *everything*
   beats baryons-alone. The claim "scarcity matches/beats a standard dark halo" is the one that
   would matter. Falsifier filed as **ORB-10082** — since run, reframed to a 3-parameter NFW;
   verdict **inconclusive** (next section).
2. **The held-out misfit is coherent, not noise.** A one-signed ~4.9 km/s underprediction where
   the real curve flattens (13–16 kpc) and the model keeps declining. The shape term is
   *sufficient relative to the control, not complete*. (The measured MW curve is itself gently
   declining, −1.7 km/s/kpc — see [studies/milky-way-rotation-curve](../studies/milky-way-rotation-curve.md)
   — so "flat" is shorthand, and the residual is a real shape mismatch, not a flat-vs-declining
   artifact.)
3. **The drift nuisance is an apparatus limitation.** A single constant drift term, pinned at its
   3 km/s lower bound and weakly identified by bootstrap, cannot represent the *radially varying*
   asymmetric-drift bias in an uncorrected median-`v_φ` curve. A radially-varying drift model is
   prerequisite to stronger claims: filed as **ORB-10083**.
4. **Calibrate the absolute-fit language.** Reduced χ² ≈ 145 is a formal failure against the
   quoted statistical errors — but those errors omit dominant distance/selection/drift
   systematics, so even the true law would fail them. This is *not* a refutation; equally, the
   2.70 km/s RMSE does not hide it. Both facts stand in the ledger.

**The 20–25 kpc follow-up decision.** Faraday's declared rule was to request Tycho's proposed
20–25 kpc/APOGEE extension only if the existing band failed to discriminate the apparatus from its
control. It did discriminate (comfortably), so **no APOGEE request was sent** — the more immediate
falsifiers were the standard-halo comparison (ORB-10082, since run — next section) and the drift
model (ORB-10083), not a longer baseline. Reconciled: the follow-up baseline is deferred, not
pending.

## Confronting a standard halo — the ORB-10082 NFW comparison

The falsifier ran (Faraday, orrery `a9f93bd`; run record
`agentbase/faraday/memory/runs/26-07/run-20260711T010553.md`), with one reframe by Daniel before
execution: NFW+baryons keeps its own free baryonic scale alongside M200 and concentration —
**3 physical parameters to scarcity's 2** — so the test is no longer equal-dof and AIC penalizes
the extra parameter. The protocol is otherwise inherited unchanged from ORB-10077 (same
predeclared bands, same bounded drift nuisance, seed 42, 27 profile variants, 200 bootstrap
resamples).

| Metric | Scarcity | NFW + baryons |
|---|---:|---:|
| RMSE (5–15 kpc fit) | 2.70 km/s | 3.66 km/s |
| AIC | 2464.8 | 4128.2 |
| Held-out 15–18.75 kpc RMSE | 5.26 km/s | 4.99 km/s |
| Held-out mean residual | +4.86 km/s (under) | −4.26 km/s (over) |
| Drift nuisance | 3.0 km/s (pinned, *lower* bound) | 10.0 km/s (pinned, *upper* bound) |

ΔAIC(scarcity − NFW) = **−1663** at the point estimate, same sign across all 27 profile variants
(−2293 to −847) — but the 200-resample bootstrap 95% interval spans **−4129 to +1102**. Per the
predeclared decision rule the verdict is **inconclusive**: the sample cannot decide between
scarcity and a standard halo. Three facts keep this honest in both directions:

1. **The point estimate is not evidence.** The bootstrap interval spans zero; recording this as
   a scarcity win would be exactly the laundering the standing rules forbid.
2. **NFW wins the held-out band, barely, and flips the residual sign** — scarcity coherently
   underpredicts where NFW overpredicts. Whichever model is right about 15–18.75 kpc, neither is
   complete there.
3. **NFW is itself weakly identified on this band** — its drift term pins the 10 km/s *upper*
   bound throughout the bootstrap (scarcity's pins the lower) and concentration fits at ~37
   (bootstrap median 37.2), far above the c ≈ 10–15 typical of an MW-mass halo. The 5–15 kpc
   band does not cleanly identify a conventional halo, which limits what this comparison can
   establish *in either direction*.

What decides next is **ORB-10083**. The two drift terms pinning *opposite* bounds says the
constant-drift nuisance is doing model-dependent work — the held-out misfit may belong to the
drift model, not to either gravity model. Radially varying asymmetric drift, applied identically
to scarcity, NFW, and the control, re-gates this row.

## Confronting the solar system — the AU-scale precision floor

The second observable of the upgrade-or-kill pair arrived 2026-07-10: tycho and faraday's
Newtonian-omission floor — how far a pure-Newtonian 9-body solar system drifts from JPL
Horizons over 2016–2026, per planet ([studies/solar-system-ephemeris-precision-floor](../studies/solar-system-ephemeris-precision-floor.md);
lineage ORB-10076 → ORB-10093 → ORB-10094). Any real dynamics the Newtonian baseline omits is
*contained in* those residuals, so a modification predicting more deviation than a planet's
floor is excluded at that amplitude.

**First pass (analytic, 2026-07-10).** The fitted continuum form multiplies Newtonian gravity
by q(r)/q(R₀); its local logarithmic gradient at the Sun's galactocentric radius is

> d ln q/dr = β·F(R₀)/R₀² ≈ 5.25 kpc × 0.86 / (8.25 kpc)² ≈ 0.066 /kpc ≈ **3.2×10⁻¹⁰ /AU**

In the heliocentric frame only the *differential* across the system matters. Two regimes:

- **Inner planets** complete many orbits in the window; a quasi-constant vector perturbation
  orbit-averages, leaving a bounded epicyclic response a_p/n² — predicted offsets sit **4–6
  orders below** their floors. Safe regardless of reading.
- **Outer planets** barely move in 10 years; nothing averages. The quasi-static bound
  ½·a_p·T² gives Jupiter 1.2e-7 (0.7× floor), Saturn 6.7e-8 (**1.6×**), Uranus 3.3e-8
  (**8×**), Neptune 2.1e-8 (**1.2×**) AU.

Whether the outer-planet numbers are a real prediction hinges on a model assumption the
lattice toy has never fixed: does the galactic scarcity factor **multiply the Sun's own
field** (then the tension above is real, and the floor already bites), or does the Sun's own
depletion **dominate and screen** the galactic gradient locally (then the prediction collapses
to ~0 and the bound is trivially satisfied)? That superposition rule is now a load-bearing
open question — `conjecture — to verify` either way. The ½aT² bound is also crude (no
orientation projection, no orbital geometry, no IC/GM absorption), which is why the
adjudication is an experiment, not more algebra: **ORB-10097** (Faraday) integrates the
multiplicative reading on the exact ORB-10093 protocol and compares per-planet deviations to
the measured floors. If the multiplicative reading survives unmodified it is remarkable; if
it fails, the *screened* variant becomes the only viable branch and the theory owes a
mechanism for the screening.

**Numerical adjudication (ORB-10097, run 2026-07-11).** Faraday integrated the multiplicative
reading on the exact ORB-10093 protocol — same first-epoch Horizons initial conditions,
366-epoch TDB grid, heliocentric ICRF frame — scaling every heliocentric acceleration by the
fitted local gradient exp[(βF(R₀)/R₀²)(r_gal − R₀)], with β = 5.25 kpc and the ORB-10077/10082
mass-profile surrogate imported unchanged (apparatus F(R₀) = 0.830; no retuning). Differenced
against a concurrently integrated pure-Newtonian twin (which matches the frozen ORB-10093
baseline to 4.5e-10 AU per coordinate; step-halving moves the signature ≤ 1.6e-12 AU). Result
([solar-system-nbody](../../orrery/lab/sims/solar-system-nbody/) `scarcity/`
[summary.json](../../orrery/lab/sims/solar-system-nbody/scarcity/summary.json), orrery `23fe253`):

- **Primary orientation** (galactocentric outward axis from the ICRF Galactic-center
  direction): **Uranus exceeds its floor — rms 7.7e-9 vs 4.1e-9 AU (1.89×), max 1.8e-8 vs
  6.5e-9 AU (2.84×)**. Every other planet is below its rms floor: Saturn 0.74×, Jupiter 0.17×,
  Neptune 0.11×, Mars 0.032×, and the inner three at ~2–4×10⁻³ — confirming the
  orbit-averaging regime split from the first pass.
- **Orientation qualification:** across the six cardinal-axis sweep the Uranus rms signature
  spans 2.7e-9 – 1.2e-8 AU (0.66×–3.0× floor) — the envelope **crosses** the floor, so the
  verdict is orientation-sensitive at O(1). Tension under the physically-motivated
  orientation, **not an orientation-independent refutation**. R₀ (8.25 → 8.122 kpc) shifts
  signatures only ~2.5%.
- **Screened control:** identically zero by construction — screened local dominance leaves
  the equations exactly Newtonian, so this test **cannot constrain the screened branch**.

Two honest postscripts. The first-pass ½aT² bound above overestimated the apparatus result by
~4× (Uranus 8× → 1.89× rms) — it picked the binding planet and the qualitative verdict
correctly, but the measured ratios in the ledger row are the numbers of record. And at the
time of the run, the multiplicative rule the apparatus tested was a deliberately chosen
*interpretation* of the fitted form, not a field equation derived from the lattice model.
**That gap briefly closed (ORB-10156, § next) and has reopened under measurement (ORB-10157,
§ superposition adjudication):** the multiplicative reading was derived from the mechanic on
the anonymity argument; the lattice then measured the mechanic's actual modulation as
survivor-fraction headroom screening — unit gain, keyed to local occupancy — so ORB-10097's
instrument tested the fitted-form transplant after all, not a rule the mechanic supplies.
The tension it found is conditioned on identifying the fitted boost with the measured
modulation (ledger row above); the exactly-Newtonian escape stays closed regardless
(independence refuted on the lattice at log-RMSE 1.074). The row stays `mixed` on the
orientation qualification *and* on that conditioning.

## The metric character of scarcity and the photon sector — the ORB-10156 derivation

Daniel's challenge (2026-07-12): *"call it scarcity or call it curvature, same thing, isn't
it?"* This section stops that being a matter of taste. The weak-field metric of any metric
theory carries **two** potentials — Φ in g₀₀ (clock rates; the entire driver of slow massive
particles) and γΦ in gᵢⱼ (how much proper space a mass adds; γ = 1 in GR) — and photons read
both while planets read only the first. All PPN machinery and measured values here lean on
[studies/scalar-gravity-ppn-constraints](../studies/scalar-gravity-ppn-constraints.md).

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
[studies note](../studies/scalar-gravity-ppn-constraints.md): solar limb deflection
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

## The clock sector — the ORB-10159 derivation

ORB-10156 left the clock sector as the model's silent failure: σ = clock-rate deficit was
flagged as a postulate the counting mechanic does not supply. This section makes that failure
explicit, then derives what the dynamical completion is forced to be. The instruments here
are the measured time-dilation ladder
([studies/gravitational-time-dilation](../studies/gravitational-time-dilation.md)), the
river/analog-gravity machinery
([studies/river-model-and-analog-gravity](../studies/river-model-and-analog-gravity.md)),
and the Lorentz-violation bounds
([studies/lorentz-violation-bounds](../studies/lorentz-violation-bounds.md)).

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

## The lattice adjudication — the ORB-10162 measurement

The first of the clock sector's two gates has run (faraday,
[dynamical-consumption-lattice](../../orrery/lab/sims/dynamical-consumption-lattice/),
orrery `98396a8`, seed 42): a 1000-shell radial counting lattice with deficit-driven
nearest-neighbour hopping, a fixed-density outer reservoir, and the mechanic's two natural
local destruction rules, evolved from a full state to demonstrated steady state (final step
change < 10⁻⁹ of the maximum standing deficit; shell-balance residuals 9.4×10⁻⁹ and
7.9×10⁻¹¹ of total sink; byte-identical reruns). Fits span radii 10–500 — 1.699 decades,
491 face samples:

| Local consumption rule | Measured v(r) exponent (± SE, 95% CI) | Nearest candidate law | Sink scaling per shell |
|---|---|---|---|
| central-only (sink at the mass — the naive rule) | −2.00062 ± 0.00002, [−2.00065, −2.00059] | r⁻² — the flux-conserving branch, §(b) rule 1 | localized to the innermost shell |
| equal-per-shell (the Gauss bookkeeping read as a rate) | −0.99454 ± 0.00036, [−0.99524, −0.99383] | r⁻¹ — the budget-flow branch, §(b) rule 2 | r^(0.00029 ± 0.00026), CI [−0.00022, 0.00079] — flat |

**The gate, applied.** Each rule locked in exactly the flow that continuity dictates for its
sink distribution — the two branches §(b) refuted against the clock ladder — and neither
self-organized toward free-fall: the naive rule *is* the predeclared kill-condition
flux-conserving flow, and the mechanic's own bookkeeping draws a flat r⁰ per-shell budget
where the GP river requires r^(1/2) (the measured CI excludes 1/2 by three orders of
magnitude). ORB-10162's predeclared gate — *"a lattice whose natural consumption rules
cannot produce the free-fall flow refutes the river completion at the mechanic level"* —
fires: **the GP flow does not emerge from the existing counting mechanic** (river-fork
ledger row moved `mixed` → `refuted`). What survives is exactly what was derived and no
more: extending the rolling rule to space yields GP analytically (§(b) branch 3 stands as
mathematics), but the r^(−3/2) volumetric destruction law that sustains it is now a
**measured** debt — the existing rules produce r⁰, and the lattice does not bend toward
r^(1/2) on its own.

**The time-integrated snapshot, reconciled.** ORB-10159's consistency identity — the static
Σ 1/count ∝ 1/r field is the comoving time-integral of the flow — was claimed *for branch 3*
(GP flow over a distributed volumetric sink). The measured branches do not exhibit it:
central-only's *standing* deficit reproduces the finite-reservoir static shape A(1/r − 1/R)
at R² = 0.99999992 (relative RMSE 3.6×10⁻⁵) — the verified static field returns — but a
comoving parcel on that branch accumulates *zero* destruction before the innermost sink, so
the standing 1/r is a diffusion-against-reservoir profile, not the comoving record of
anything; equal-per-shell matches neither shape (standing R² = −0.838, comoving R² = −17.30).
Scope, stated precisely: this does **not** refute the branch-3 identity — no GP branch
emerged for the measurement to test it on, so the identity stands as derived, exactly as
conditional as the branch it lives on. What the measurement *removes* is ambient support:
the lattice manifestly produces the verified 1/r standing field with no comoving history
behind it, so the static sims' 1/r result can no longer be read as suggestive evidence *for*
the flow interpretation. Likewise σ = v²/2c² fails on both measured branches (median
flow/standing-σ ratios 2.0×10⁻⁹ and 4.1×10⁻⁸; RMS log-discrepancies 8.4 and 7.2 dex) —
expected, since neither branch is GP; the failure confirms what the branches are, and does
not test branch 3.

**Apparatus caveats, and what they gate.** Two, both declared by faraday. (i) *Radial shell
reduction:* the lattice is a finite-volume spherical-shell reduction (deterministic mean-field
flow, Poisson counting over 50 time units for the sink measurement), not a full 3D stochastic
lattice. The flow-law fork is a statement of radial continuity and the reduction implements
exactly the spherical symmetry the analytic fork assumes, so the exponent verdict is not
softened; a conjecture that full-3D stochasticity self-organizes differently would need a
mechanism no current rule supplies. (ii) *Hop-speed normalization:* the identity check's
c ≡ D/dr is apparatus-specific, so the σ = v²/2c² residuals are apparatus-conditioned in
absolute normalization — but 7–8 dex is far beyond any O(1) renormalization (c enters
squared), and on the measured branches the identity is not expected regardless. **Neither
caveat gates the gate verdict.** One scope limit for the record: the third candidate family
ORB-10162 named — consumption keyed to local scarcity gradient or inflow speed — was not
run; such a rule is a *new coupling*, not part of the existing mechanic, so its absence does
not soften what the measurement says about the mechanic as it stands — it belongs to the
derive-it-from-deeper-dynamics route below.

**Where the debt now lives.** With the mechanic's own rules measured out, exactly one route
inside the family remains short of concession: derive the r^(−3/2) destruction rule from
substrate dynamics — **ORB-10161 Branch B's standing obligation**
([two-substance-vortex-vacuum](two-substance-vortex-vacuum.md), §B2: the incompressible fork
owes precisely this sink law, and harder — outside a star there are no cores to do the
consuming). That derivation is not attempted here. The statement of record: **impose the
rule as a named postulate (and say so), derive it from S2 dynamics (ORB-10161's obligation),
or concede the clock sector.** The excitation gate (**ORB-10158**) is independent and
remains open.

## The superposition adjudication — the ORB-10157 measurement

The second derivation gate has run (faraday,
[lattice-two-source-superposition](../../orrery/lab/sims/lattice-two-source-superposition/),
seed 42): a 129² shared-budget counting lattice — 50,000 anonymous slots per cell, full
outer reservoir — embeds a compact one-cell source (peak exposure 0.1) at the center of an
extended uniform-disk depletion well (radius 0.31 lattice widths) and measures the source's
paired field (the radial gradient of its increment to stored scarcity, projected onto its
isolated-source gradient over radii 4–18 cells) as ambient depletion D sweeps 0.01–0.90 in
12 levels, with the full profile recorded to D = 0.995. Depletion is literally anonymous:
every attempt picks a slot blind to source and state (survivors sampled exactly as
Binomial(C, e^(−H))), and compact hits can clear only slots the background left alive. All
12 seeded finite-count means (32 replicates each) lie within 2.31 standard errors of the
exact expectation; reruns are byte-identical.

| Candidate superposition law | Reading it operationalizes | log-RMSE (D ≤ 0.90) | Verdict |
|---|---|---|---|
| A = 1 (independence) | the exemption ORB-10097 called "screened": the Sun generates as if alone, ephemerides exactly Newtonian | 1.074 | refuted |
| A = 1/(1−D) (inverse-headroom enhancement) | the shared budget amplifies an embedded source's field | 2.077 | refuted — and no exhaustion upturn appears even at D = 0.995 (amplitude 0.0029 of isolated) |
| A = 1−D (plain local headroom) | turn 7: wells dug from remaining capacity | 0.0711 | right family |
| **A = (1−D)^1.07079 (measured)** | survivor-fraction screening; the exponent's excess over 1 is annulus geometry (headroom varies across the 4–18-cell band) | **0.0031** | **the mechanic's answer** — resolution checks 1.0725 (97²) / 1.0700 (161²), amplitude shifts ≤ 4.4×10⁻⁴ |

**The adjudication: which premise of the ORB-10156 derivation fails.** The derivation ran:
the fitted boost is a position-dependent coupling G_eff(r) = G·q(r)/q(R₀) keyed to
accumulated background depletion; depletion on a shared budget is anonymous; *therefore* an
embedded source generates with the background's coupling — the fitted factor, with its
fitted gain. The apparatus is faithful to the mechanic as stated — anonymity is implemented
literally, and the stored field is the model's additive draw bookkeeping (removals per
cell), not some second convention — so the inapplicability defense is not available. What
the measurement shows is that the anonymity premise proves less than the derivation drew
from it. Anonymity establishes only that an embedded source is *not exempt* from the shared
budget (independence: refuted). The modulation the budget itself supplies is the trivial
counting factor — a source's attempts can clear only surviving slots, so its field carries
exactly one factor of local survivor fraction, (1−D)^1.07, unit gain, keyed to *local
occupancy*. The derived rule needed something anonymity does not provide: a coupling that
responds to the *accumulated* dilution level with the fitted gain β. No counting rule in
the mechanic does that, and faraday's declared scope caveat names the gap exactly — a rule
whose depletion-attempt rate varies with occupancy is a *different microscopic model*.
**The failing step is the transplant:** "generates with the background's coupling" silently
substituted the fitted macroscopic factor for the mechanic's actual transfer function,
which had never been computed. The `supported` verdict is superseded and stays on the
ledger as the record of that mistake.

Two sign facts keep the bookkeeping honest, because the branch names have become
treacherous. First, the measured "screening" is *not* ORB-10097's "screened branch": that
branch meant exemption — the Sun's own depletion pins the local level, the galactic factor
never reaches its generation, ephemerides come out exactly Newtonian — which on the lattice
is the *independence* candidate, and it is refuted; what ORB-10156's point 3 argued against
the exemption survives with its variable transposed. Second, the refuted "multiplicative
enhancement" is not the sign ORB-10097 integrated: the integrated factor
exp[(βF(R₀)/R₀²)(r_gal − R₀)] makes the Sun's field *weaker* where galactic depletion is
higher — suppression-signed, like the measured law. What ORB-10097 imported that the
mechanic does not supply is the gain and the variable, not the direction.

**Relation to the fitted form — which reading the rotation-curve fit actually tested.** The
measured law is the original turn-7 headroom idea, returned by the mechanic itself at unit
gain: turn 9's ODE was ds/dr = G₀(1−s)·M(r)/r² — effective G proportional to remaining
headroom — and "wells dug from remaining capacity" is literally what the apparatus measured.
The fitted q(r) form is that rule in continuum dress with the gain promoted to the fitted β
on *accumulated* dilution. So the measured law sits squarely in the fitted form's own family
— headroom suppression, boost rising where depletion falls — where the enhancement
operationalization was its sign-mirror. What the ORB-10077/ORB-10082 fit tested was
therefore the *shape as phenomenology*: q(r) with one free gain, decisively better than the
no-halo control regardless of microscopic carrier. What it never tested is the carrier —
and the measured carrier reproduces the fitted boost only under a demanding identification:
for (1−D_gal(r))^1.071 to equal the fitted 0.70 → 1.36 boost across 5–18.75 kpc, ambient
*occupancy* depletion must vary O(1) across the disk (headroom ratio ≈ 1.94^(1/1.07) ≈ 1.86,
i.e. D ≳ 0.46 at 5 kpc even with the outer band fully undepleted) — a normalization
statement about how much lattice occupancy the Galaxy's mass consumes that the
accumulated-dilution picture never made and nothing has fixed. The alternatives now on the
table are sharper than multiplicative-vs-screened ever was: (i) the fitted boost *is* the
measured screening law, at O(1) galactic occupancy depletion; (ii) the boost requires a new
occupancy-coupled generation rule carrying the fitted gain — faraday's "different
microscopic model", owing its own lattice test; (iii) the boost is phenomenology the
counting mechanic does not carry.

**The ORB-10097 consequence, stated precisely.** The Uranus tension attached to the model
through the claim that the mechanic itself hands the Sun the fitted factor. Measured, it
does not — so the tension is **conditioned: neither detached nor retained outright**. On
reading (i), everything ORB-10097 integrated stands unchanged, because the boost's local
log-gradient at R₀ is a property of the fitted shape, not of its carrier: any multiplicative
modulation reproducing the fitted boost hands the Sun's field the same 3.2×10⁻¹⁰/AU
differential, and the 1.89×-rms primary-orientation excess (six-axis envelope 0.66–3.0×) is
again the model's own. On readings (ii)/(iii), ORB-10097's integration tested a rule the
mechanic doesn't have, and no solar-system prediction exists until the occupancy
normalization or the new coupling is fixed. What no reading recovers is the free escape:
the exemption branch that would have left ephemerides exactly Newtonian is the lattice's
independence candidate, measured dead at log-RMSE 1.074. The ORB-10097 ledger row carries
the condition; its integrated numbers are unretired.

**Apparatus caveats, and what they gate.** Three, all declared by faraday. (i) *2D static
pinned geometry:* both sources are fixed exposure maps on a 129² lattice (97² and 161²
checks move the exponent by ≤ 0.002), not emergent, moving, or self-consistently digging
depleters. (ii) *Anonymous fixed-coupling attempts:* the depletion-attempt rate never
responds to occupancy — one microscopic reading of "shared budget", and exactly the
mechanic as stated in every prior sim. (iii) *Declared, not emergent, profiles:* the
Poisson-solved exposure maps say where attempts land; superposition enters only through the
shared slots. None gates the verdict on the mechanic *as stated* — fidelity on (ii) is the
point of the experiment, and (i)/(iii) are the same declared-geometry idealization every
static-sector sim in this ledger uses. All three gate *extrapolation*: an occupancy-coupled
rule (reading (ii) of the fitted-form question above) is untested by construction, and a
moving or emergent source could in principle superpose differently — no current rule
supplies a mechanism for either, and conjuring one is new model-building, not this
measurement's problem. Cross-reference: the parent's boost citations in
[two-substance-vortex-vacuum](two-substance-vortex-vacuum.md) (§A3 and its Branch A ledger
rows) are updated to carry the same conditioning.

## Open questions

- **Does scarcity match a standard dark halo?** ORB-10082 ran: point estimate favors scarcity on
  every variant, the bootstrap cannot decide, and NFW wins the held-out band — **statistically
  undecided**. The live gate is **ORB-10083** (radially varying drift): until the nuisance stops
  absorbing model-dependent error, the comparison cannot settle.
- **What carries the galactic boost?** *The superposition question, reopened by measurement
  with sharper alternatives (ORB-10157, § superposition adjudication above).* It was briefly
  ~~resolved by derivation (ORB-10156)~~: multiplicative — anonymity was read as forcing the
  fitted q-ratio coupling onto embedded sources, making the ORB-10097 Uranus tension the
  model's own. The lattice then measured the mechanic's actual modulation: **headroom
  screening**, A(D) = (1−D)^1.071 — survivor-fraction suppression at unit gain in local
  occupancy; independence refuted (log-RMSE 1.074), inverse-headroom enhancement refuted
  (2.077). The open question is no longer multiplicative-vs-screened but which of three
  readings carries the fitted boost: (i) the measured screening law itself, requiring O(1)
  ambient occupancy depletion across the disk (D ≳ 0.46 at 5 kpc — a mass→occupancy
  normalization nothing has fixed); on this reading the ORB-10097 tension survives with the
  same integrated numbers; (ii) a new occupancy-dependent coupling with the fitted gain
  (faraday's "different microscopic model"), owing its own lattice adjudication; (iii)
  phenomenology the mechanic does not carry. The exemption reading (embedded sources
  unmodulated → exactly Newtonian) is measured dead either way.
- **Can the counting mechanic earn a Ψ sector?** *Reshaped by ORB-10159 (§ clock sector):*
  the answer has a derived form — on the excitation completion, the γΦ half is supplied
  entirely by **flow drag** (a wave on the GP inflow sees exact Schwarzschild; γ = 1 with
  the right sign, no proper-space excess needed), and the matching clock mechanism comes
  free (σ = ½v²/c² is SR dilation against the flow). The question therefore sharpens into
  the two owed ingredients: (i) can any counting rule produce the free-fall flow's
  volumetric sink law ∝ r^(−3/2) — **measured by ORB-10162: the natural rules cannot**
  (flat r^(0.0003 ± 0.0003) per-shell draw, CI excluding r^(1/2); § lattice adjudication);
  (ii) do excitations of a flowing lattice really propagate with the flow-drag sign —
  measured by **ORB-10158** (extended scope). (i) has now failed at the mechanic level —
  so, per this question's own terms, the model *as stated* stays what ORB-10156 proved it
  is: a massive-sector phenomenology, not a theory of gravity. The completion lives only if
  the sink rule is derived from deeper dynamics (**ORB-10161 Branch B's obligation**,
  [two-substance-vortex-vacuum](two-substance-vortex-vacuum.md) §B2) or honestly carried as
  an imposed postulate; (ii) still gates the photon arm. (The chameleon route of the
  studies note remains the fallback completion if the analog-gravity route dies.)
- ~~**Does a dynamical-consumption lattice actually flow at free-fall?**~~ **Answered by
  measurement (ORB-10162, § lattice adjudication above): no.** Both natural rules lock in
  exactly the refuted flows — central-only v ∝ r^(−2.0006 ± 0.0000) (the flux-conserving
  kill condition, which did emerge, from the naive rule), equal-per-shell
  v ∝ r^(−0.9945 ± 0.0004) — and the sink stays flat (r^(0.0003 ± 0.0003)) where free-fall
  needs r^(1/2). The river completion is refuted at the mechanic level. The surviving
  question is no longer whether the mechanic flows at free-fall but whether the r^(−3/2)
  destruction rule can be *derived* — ORB-10161 Branch B's standing obligation
  ([two-substance-vortex-vacuum](two-substance-vortex-vacuum.md) §B2) — or must be carried
  as an imposed postulate; failing both, the clock sector is conceded.
- Can the lattice model be normalized once (one constant) and then match *two* independent
  observables? That would upgrade "right shape" materially. (The rotation-curve fit uses one free
  β — a second, independent observable matched at the *same* β would be the real upgrade.)
  The sharpest version is now filed (ORB-10161's universality analysis): one *global*
  β = 5.25 kpc across an external-galaxy sample vs per-galaxy β — tycho ORB-10168 (SPARC
  catalog) + faraday ORB-10169, kill condition predeclared; the measured
  radial-acceleration relation is the standing risk
  ([studies/fifth-force-searches](../studies/fifth-force-searches.md)).
- Where does the model *diverge* from Newton/GR at accessible scales? Partially answered by
  ORB-10156/ORB-10097: it diverges in the photon sector (fatally, as stated) and at Uranus
  under the multiplicative rule (orientation-dependent tension, now conditioned on the
  fitted-boost identification — ORB-10157). A falsifying sim is still worth more than
  another confirming one — ORB-10157 was exactly that kind (it killed the derived
  superposition rule); ORB-10158 remains open.

## Related

Reference n-body baseline: [solar-system-nbody](../../orrery/lab/sims/solar-system-nbody/) (conventional
Newtonian leapfrog — the control the field models are compared against).

**Candidate microphysics:** [two-substance-vortex-vacuum](two-substance-vortex-vacuum.md)
(ORB-10160) — a substrate ontology (particles as vortex defects, charge as winding, void
cores) founded to *derive* this model's scarcity field as its effective far-field
description. Its equivalence-principle fork has a computed verdict that lands on exactly
this doc's surviving branch: void-volume-sourced gravity is refuted (MICROSCOPE), leaving
substrate *energy* as the source — the same energy-flow river completion ORB-10159 derived
here. It inherits this doc's ORB-10156 photon-sector refutation as a floor and the
ORB-10159 rest-frame constraints doubled. Its founding gates have since run: ORB-10163
measured the EM sign structure supported in 2-D, and **ORB-10164 measured the derivation
target refuted at the mechanic level — a substance-conserving lattice produces no
far-field scarcity from voids** (that doc's § lattice adjudications). The candidate's
bridge to this doc therefore hangs on the same object as this doc's own river debt: the
r^(−3/2)/non-conservation **source law**, one consolidated debt across ORB-10162,
ORB-10164, and that doc's §B2 obligation. Nothing in that doc moves this ledger.
