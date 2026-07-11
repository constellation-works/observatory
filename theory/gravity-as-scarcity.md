---
title: "Gravity as the gradient of scarce space"
status: growing
families: [gravity-as-scarcity]
almanac: 15-discussions/26-07/gravity-as-scarcity-of-space.md
created: 2026-07-09
updated: 2026-07-10
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

## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| Accumulated per-shell dilution Σ 1/count(k) ∝ 1/r, so "gravity = gradient of scarcity" reproduces Newton's 1/r² | supported | by construction in [scarcity-grid-weight-black-hole](../../orrery/lab/sims/scarcity-grid-weight-black-hole/), [scarcity-capped-cumulative-field](../../orrery/lab/sims/scarcity-capped-cumulative-field/); note: storing 1/r² and differentiating gives 1/r³ — the stored field must be potential-like (correction #1 in the thread) |
| Dividing a fixed budget across shells yields inverse-square from pure geometry (Gauss's law analog) | supported | [scarcity-shell-depletion-field](../../orrery/lab/sims/scarcity-shell-depletion-field/) |
| Subtractive budget gives a hard cutoff radius r ≈ (3T/4π)^⅓ beyond which gravity dies (Yukawa-cartoon) | supported | [scarcity-capped-cumulative-field](../../orrery/lab/sims/scarcity-capped-cumulative-field/), [scarcity-star-well-headroom](../../orrery/lab/sims/scarcity-star-well-headroom/) — as a property of the *model*; no claim it matches nature |
| An extended (distributed) mass under the model bends rotation curves toward flat (dark-matter/MOND-adjacent) — the *shape* | supported | Qualitative: [rotation-curve-distributed-mass](../../orrery/lab/sims/rotation-curve-distributed-mass/). Quantitative: fit to real Gaia DR3 data ([scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/), ORB-10077) — with one free β the scarcity shape beats the nested no-halo baryons control decisively (RMSE 2.70 vs 18.40 km/s; ΔAIC ≈ −10⁵, stable across 27 profile variants). Measured curve & data lineage: [studies/milky-way-rotation-curve](../studies/milky-way-rotation-curve.md) |
| Fit to real MW data, the scarcity model **matches or beats a standard dark-matter halo once AIC penalizes parameter count** | mixed | **ORB-10082 ran** ([scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/), orrery `a9f93bd`) — reframed by Daniel before execution: NFW+baryons keeps a free baryonic scale plus M200 and concentration (3 physical params vs scarcity's 2; no longer equal-dof, AIC penalizes the extra). Point estimate favors scarcity — RMSE 2.70 vs 3.66 km/s, ΔAIC(scarcity−NFW) = −1663, same sign on all 27 profile variants (−2293 to −847) — **but the 200-resample bootstrap 95% CI spans −4129 to +1102 → statistically inconclusive, not a scarcity win**. Cutting the other way: NFW slightly wins the held-out band (4.99 vs 5.26 km/s RMSE) and flips the coherent residual sign; NFW is itself weakly identified here (drift pinned at its 10 km/s *upper* bound, c ≈ 37 — far above a typical MW-mass halo), so the 5–15 kpc band limits what the comparison establishes *in either direction*. Gate: **ORB-10083** (radially varying drift, applied identically to all three models) |
| The fitted scarcity model is an *absolute* description of the MW rotation curve | mixed | Reduced χ² ≈ 145 against the quoted statistical errors — a formal failure — but those errors omit dominant distance/selection/asymmetric-drift systematics, so even the true law would fail them (not a refutation). Held-out 15–18.75 kpc band: coherent one-signed ~4.9 km/s underprediction — the data flattens near 13–16 kpc where the model keeps declining; the shape term is *sufficient relative to the control, not complete*. Drift nuisance pinned at its 3 km/s lower bound and weakly identified → a radially-varying asymmetric-drift model (Faraday **ORB-10083**) is prerequisite to any stronger claim. See [scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/) |
| The fitted scarcity form leaves solar-system ephemerides (AU scale) inside observational precision | mixed | Constraint from the measured Newtonian-omission floor ([studies/solar-system-ephemeris-precision-floor](../studies/solar-system-ephemeris-precision-floor.md); Uranus rms 4.1e-9 AU is the tightest). **ORB-10097 ran** (Faraday; [solar-system-nbody](../../orrery/lab/sims/solar-system-nbody/) `scarcity/`, orrery `23fe253`, § below): the **multiplicative reading**, integrated on the exact ORB-10093 protocol with β and F(u) imported unchanged, puts **Uranus above its floor in the primary galactocentric orientation — 1.89× rms, 2.84× max** (7.7e-9 vs 4.1e-9 AU rms); the other seven planets stay below (Saturn next at 0.74×). Qualification: the six-axis orientation envelope **crosses** the Uranus floor (rms 0.66×–3.0×), so this is tension under the physically-motivated orientation, *not* an orientation-independent refutation. The **screened reading is identically Newtonian** — the explicit zero control — and is **unconstrained by this test**. The superposition rule itself is still unfixed in the model; the multiplicative branch is now the one carrying measured tension. Result: [summary.json](../../orrery/lab/sims/solar-system-nbody/scarcity/summary.json) |
| Adding swirl to the scarcity field reproduces frame dragging | mixed | [frame-drag-swirl](../../orrery/lab/sims/frame-drag-swirl/) — right shape; real frame dragging (Lense–Thirring) has specific magnitude/falloff this toy hasn't been checked against (`conjecture — to verify`: study note needed) |
| The scarcity picture is equivalent to weak-field GR's "gradient of time-flow rate" heuristic | untested | asserted by analogy in the thread; needs a worked comparison |

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
correctly, but the measured ratios in the ledger row are the numbers of record. And the
multiplicative rule the apparatus tested is a deliberately chosen *interpretation* of the
fitted form, not a field equation derived from the lattice model — deriving the actual local
superposition behavior (or a screening mechanism) is what would move this row out of `mixed`.

## Open questions

- **Does scarcity match a standard dark halo?** ORB-10082 ran: point estimate favors scarcity on
  every variant, the bootstrap cannot decide, and NFW wins the held-out band — **statistically
  undecided**. The live gate is **ORB-10083** (radially varying drift): until the nuisance stops
  absorbing model-dependent error, the comparison cannot settle.
- **What is the model's superposition rule?** Does a mass's scarcity factor multiply gravity
  sourced by *other* masses, or is the local field dominated by the local well? **ORB-10097
  adjudicated the multiplicative branch numerically**: in tension at Uranus under the primary
  galactocentric orientation (1.89× rms, 2.84× max floor), orientation envelope crossing the
  floor — so the branch is wounded but not orientation-independently dead. The screened branch
  is identically Newtonian and untestable by this instrument. What settles the question now is
  *theory*, not another integration: derive the local field behavior from the lattice model
  itself — which reading (or what screening mechanism) the model actually implies.
- Can the lattice model be normalized once (one constant) and then match *two* independent
  observables? That would upgrade "right shape" materially. (The rotation-curve fit uses one free
  β — a second, independent observable matched at the *same* β would be the real upgrade.)
- Where does the model *diverge* from Newton/GR at accessible scales? A falsifying sim is
  worth more than another confirming one.

## Related

Reference n-body baseline: [solar-system-nbody](../../orrery/lab/sims/solar-system-nbody/) (conventional
Newtonian leapfrog — the control the field models are compared against).
