## Confronting the solar system — the AU-scale precision floor

The second observable of the upgrade-or-kill pair arrived 2026-07-10: tycho and faraday's
Newtonian-omission floor — how far a pure-Newtonian 9-body solar system drifts from JPL
Horizons over 2016–2026, per planet ([studies/solar-system-ephemeris-precision-floor](../../studies/solar-system-ephemeris-precision-floor.md);
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
([solar-system-nbody](../../../orrery/lab/sims/solar-system-nbody/) `scarcity/`
[summary.json](../../../orrery/lab/sims/solar-system-nbody/scarcity/summary.json), orrery `23fe253`):

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
