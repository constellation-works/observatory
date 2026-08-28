## The lattice adjudication — the ORB-10162 measurement

The first of the clock sector's two gates has run (faraday,
[dynamical-consumption-lattice](../../../orrery/lab/sims/dynamical-consumption-lattice/),
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
([two-substance-vortex-vacuum](../two-substance-vortex-vacuum/), §B2: the incompressible fork
owes precisely this sink law, and harder — outside a star there are no cores to do the
consuming). That derivation is not attempted here. The statement of record: **impose the
rule as a named postulate (and say so), derive it from S2 dynamics (ORB-10161's obligation),
or concede the clock sector.** The excitation gate (**ORB-10158**) is independent and
remains open.
