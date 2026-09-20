## Confronting real data — the ORB-10077 rotation-curve fit

The first time the model met measured data. Faraday (Sol, ORB-10077) took turn 9's headroom idea
in continuum form — v_S² = v_N² · q(r)/q(R₀) with q(r) = exp[−β ∫ F(u)/u² du], β the one free
shape parameter — and fit it in real units to Tycho's Gaia DR3 median-`v_φ` curve (ORB-10075
lineage), under a **predeclared** protocol: fit 5–15 kpc, hold out 15–18.75 kpc, same bounded
asymmetric-drift nuisance for model and control, decisive only if |ΔAIC| ≥ 10 with consistent
sign across all 27 mass-profile variants. Apparatus: [scarcity-rotation-curve-fit](../../../orrery/lab/sims/scarcity-rotation-curve-fit/)
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
   declining, −1.7 km/s/kpc — see [studies/milky-way-rotation-curve](../../studies/milky-way-rotation-curve.md)
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

**Form postscript (ORB-10167, 2026-07-12).** The same band has since been measured
**shape-degenerate**: a canonical Sanders-form Yukawa under the identical protocol fits within
0.22 km/s of scarcity's RMSE and the bootstrap cannot separate the two forms (§ form and
universality adjudication below). The ΔAIC ≈ −10⁵ against baryons stands; what it certifies is
the boost's existence and scale, not its functional form.
