## Falsifier → faraday

Filed as **ORB-10751** (ws_orrery, crew sol, high, 2026-08-11): a dynamical lattice
implementing local strain-coupled destruction — s computed from neighbor flow differences,
no imposed profile — with predeclared gates:

1. **Attractor gate:** seeded from rest and from perturbed states around a consuming core,
   does the flow converge to v ∝ r^(−1/2) (measured exponent −0.5 within apparatus error)?
   Failure to converge, or convergence to another exponent, kills the law.
2. **Amplitude gate:** does an imposed core boundary condition (surface inflow or core
   consumption rate) select the amplitude A monotonically and stably? If A is not
   controllable by the core, debt 2 is unpayable in this form.
3. **Silence gate:** a uniformly expanding lattice must show consumption consistent with
   zero (the cosmological-silence check, on-lattice).
4. **Superposition probe:** two cores; measure the modulation law and compare against the
   ORB-10157 headroom-screening family. Exploratory, not a kill gate.

### Adjudication (ORB-10751, faraday, 2026-08-12) — all three kill gates passed

Cataloged as [shear-consumption-lattice](../../../orrery/lab/sims/shear-consumption-lattice/)
(orrery `a8da4ec`; deterministic, byte-identical rerun verified, run-record SHA
`294f74c8…`). Apparatus: radial finite-volume lattice, nearest-neighbour Fick transport,
frozen coefficient-one von Mises destruction computed from neighbour flow differences,
fixed-flux core, unit-density outer reservoir — **the velocity profile is measured, never
imposed.** Verified at source against `summary.json`:

1. **Attractor — passed.** p = −0.5000149713, regression SE 2.9×10⁻⁷, combined
   seed/resolution/timestep error 1.6×10⁻⁵; the two initial conditions agree to 1.2×10⁻⁶;
   128/256/512-shell and dt-halving sequences both approach −1/2 monotonically.
2. **Amplitude — passed.** Exterior amplitude strictly monotonic in core flux across two
   orders of magnitude (0.003 → 0.3), initial-condition spread < 10⁻⁶. The coupling *route*
   is open; the √(2GM) identification remains underived (debt 2 stands, narrowed).
3. **Silence — passed.** Uniform expansion consumes ≤ 3.7×10⁻¹⁶ of n|H| — zero at apparatus
   precision.
4. **Superposition probe — divergence measured** (exploratory; coarse 25³ grid, stated as
   the run's strongest limitation). The two-core modulation is best fit by
   A(D) = 1/(1 + 6.82 D^0.668) (log-RMSE 0.031); the ORB-10157 screening family fits poorly
   (log-RMSE 0.421) and screens far less. Consequence if it survives resolution: the shear
   law and the counting mechanic make **incompatible superposition predictions**, and the
   shear law's stronger screening pushes the solar-system channel toward the *screened*
   reading — the one ORB-10097/ORB-10098 found unconstrained (predicts ~0 AU-scale
   deviation), not the multiplicative reading that carries the Uranus tension. The
   resolution-converged adjudication is filed as **ORB-10755** (faraday, ws_orrery, high):
   ≥3-rung resolution ladder, deeper-depletion range, separation control — converged
   family or artifact-verdict, predeclared.

### Adjudication (ORB-10755, faraday, 2026-08-21) — the divergence survives resolution, under flux cores

Faraday promoted the probe to a deterministic 25³/41³/65³ ladder with fixed physical
source width and the frozen coefficient-one rule (orrery `acc9fab`; run record
`2026-08-21-seed-42.json`, SHA `78d428a4…`). Fitted on one matched depletion grid per
rung, with second-order spacing extrapolation: **c = 4.6251 ± 0.1841,
β = 0.60556 ± 0.02687** in A(D) = 1/(1 + c·D^β); 65³ log-RMSE 0.051 against 0.241
(constrained headroom) and 0.480 (fixed ORB-10157 family). Depletion extended to
D = 0.243; three fixed-mass separation controls fit A(D) at log-RMSE 0.035; 65³
step-halving shifts the result by 1.8×10⁻⁷. **The divergent family is converged physics
of flux-type cores — not a grid artifact.** The run kept the level-core closure explicitly
out of scope as a distinct boundary model, so this settles the flux arm only; the
discriminating level-core arm is **ORB-10934** (§ closure (d)).
