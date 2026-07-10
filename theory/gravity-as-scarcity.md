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
scarcity. The claim that would matter — matching a standard dark halo at equal parameter count —
is **untested** (falsifier: ORB-10082). Held verdict, consistent with the almanac postscript
(2026-07-10): **decisively better than the no-halo control; shape promising; physically
unvalidated.**

## Evidence ledger

| Claim | Status | Evidence |
|---|---|---|
| Accumulated per-shell dilution Σ 1/count(k) ∝ 1/r, so "gravity = gradient of scarcity" reproduces Newton's 1/r² | supported | by construction in [scarcity-grid-weight-black-hole](../../orrery/lab/sims/scarcity-grid-weight-black-hole/), [scarcity-capped-cumulative-field](../../orrery/lab/sims/scarcity-capped-cumulative-field/); note: storing 1/r² and differentiating gives 1/r³ — the stored field must be potential-like (correction #1 in the thread) |
| Dividing a fixed budget across shells yields inverse-square from pure geometry (Gauss's law analog) | supported | [scarcity-shell-depletion-field](../../orrery/lab/sims/scarcity-shell-depletion-field/) |
| Subtractive budget gives a hard cutoff radius r ≈ (3T/4π)^⅓ beyond which gravity dies (Yukawa-cartoon) | supported | [scarcity-capped-cumulative-field](../../orrery/lab/sims/scarcity-capped-cumulative-field/), [scarcity-star-well-headroom](../../orrery/lab/sims/scarcity-star-well-headroom/) — as a property of the *model*; no claim it matches nature |
| An extended (distributed) mass under the model bends rotation curves toward flat (dark-matter/MOND-adjacent) — the *shape* | supported | Qualitative: [rotation-curve-distributed-mass](../../orrery/lab/sims/rotation-curve-distributed-mass/). Quantitative: fit to real Gaia DR3 data ([scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/), ORB-10077) — with one free β the scarcity shape beats the nested no-halo baryons control decisively (RMSE 2.70 vs 18.40 km/s; ΔAIC ≈ −10⁵, stable across 27 profile variants). Measured curve & data lineage: [studies/milky-way-rotation-curve](../studies/milky-way-rotation-curve.md) |
| Fit to real MW data, the scarcity model **matches or beats a standard dark-matter halo at equal parameter count** | **untested** | Only the *nested no-halo* control has been beaten — table stakes, since everything beats baryons-alone (that *is* the dark-matter problem). The decisive test is an equal-dof NFW(+baryons, 2 free params, same drift nuisance, same predeclared bands) comparison — **unrun**, filed as Faraday task **ORB-10082**. Until it runs, ΔAIC vs the control is not evidence for the theory |
| The fitted scarcity model is an *absolute* description of the MW rotation curve | mixed | Reduced χ² ≈ 145 against the quoted statistical errors — a formal failure — but those errors omit dominant distance/selection/asymmetric-drift systematics, so even the true law would fail them (not a refutation). Held-out 15–18.75 kpc band: coherent one-signed ~4.9 km/s underprediction — the data flattens near 13–16 kpc where the model keeps declining; the shape term is *sufficient relative to the control, not complete*. Drift nuisance pinned at its 3 km/s lower bound and weakly identified → a radially-varying asymmetric-drift model (Faraday **ORB-10083**) is prerequisite to any stronger claim. See [scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/) |
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
   beats baryons-alone. The claim "scarcity matches/beats a standard dark halo at equal parameter
   count" is the one that would matter, and it is **untested**. Falsifier filed: **ORB-10082**
   (NFW + baryons, 2 free params, same nuisance and protocol).
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
falsifiers are the equal-dof halo (ORB-10082) and the drift model (ORB-10083), not a longer
baseline. Reconciled: the follow-up baseline is deferred, not pending.

## Open questions

- **Does scarcity match a standard dark halo at equal dof?** The live falsifier (ORB-10082). If
  NFW+baryons fits as well or better at the same parameter count, the ΔAIC-vs-control result
  carries no weight for the theory.
- Can the lattice model be normalized once (one constant) and then match *two* independent
  observables? That would upgrade "right shape" materially. (The rotation-curve fit uses one free
  β — a second, independent observable matched at the *same* β would be the real upgrade.)
- Where does the model *diverge* from Newton/GR at accessible scales? A falsifying sim is
  worth more than another confirming one.

## Related

Reference n-body baseline: [solar-system-nbody](../../orrery/lab/sims/solar-system-nbody/) (conventional
Newtonian leapfrog — the control the field models are compared against).
