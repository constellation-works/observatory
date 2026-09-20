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
