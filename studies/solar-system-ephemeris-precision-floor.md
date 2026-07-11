---
title: "Solar-system ephemeris precision floor — the Newtonian-omission residuals"
status: active
created: 2026-07-10
updated: 2026-07-10
---

# Solar-system ephemeris precision floor

The AU-scale bound any modified-gravity claim in this corpus must respect: how far a
pure-Newtonian solar system drifts from the real one over a decade, planet by planet. This is
the second observable of the gravity-as-scarcity upgrade-or-kill pair (the first is the
rotation curve, [milky-way-rotation-curve](milky-way-rotation-curve.md)).

## What the floor is

Faraday integrated an *untuned* Newtonian 9-body system — Sun + 8 planetary-**system**
barycenters carrying planetary-system GMs, initial conditions taken directly from the
first-epoch JPL Horizons states, inertial integration, heliocentric ICRF output — across
2016-01-01 → 2025-12-29 TDB (366 epochs, 10 d cadence), and tycho differenced it against the
matched Horizons ephemerides. The residual `dr_au` per epoch is therefore the accumulated
effect of **everything real that pure Newtonian point-mass gravity omits** (plus integrator/IC
noise): relativistic corrections, asteroids, solar oblateness.

| Planet | rms |Δr| (AU) | max |Δr| (AU) |
|---|---:|---:|
| Mercury | 1.56e-5 | 3.53e-5 |
| Venus | 3.55e-6 | 6.12e-6 |
| Earth | 2.49e-6 | 4.28e-6 |
| Mars | 8.40e-7 | 1.65e-6 |
| Jupiter | 1.84e-7 | 3.14e-7 |
| Saturn | 4.25e-8 | 9.39e-8 |
| Uranus | 4.08e-9 | 6.48e-9 |
| Neptune | 1.75e-8 | 3.64e-8 |

Values recomputed 2026-07-10 from the local parquets (below); they reproduce faraday's
`summary.json` — tycho's ingest verified the two independent comparison implementations agree
at rtol 1e-9.

## Interpreting Mercury's excess

Mercury's floor is dominated by the omitted general-relativistic perihelion advance,
**42.98 ″/century** (Will 2014, *Living Reviews in Relativity* 17:4, "The Confrontation
between General Relativity and Experiment", §3.5). Order-of-magnitude consistency: the GR
fractional acceleration correction for Mercury is ~3(v/c)² ≈ 7×10⁻⁸; over the ~1.5×10¹⁰ km
Mercury travels in the 10-year window this accumulates to ~10³ km ≈ 10⁻⁵ AU along-track —
matching the measured 1.56×10⁻⁵ AU rms. The floor declines outward roughly as GR does
((v/c)² falls with r); by Uranus/Neptune the residual is at the level of integrator/IC noise
plus Neptune's slight excess, so the outer floors are **upper bounds on allowed unmodeled
dynamics**, not clean GR measurements.

## What "observationally allowed" means here

Horizons ephemerides are fit to real observations. Any real dynamics missing from the
Newtonian baseline is therefore *contained in* these residuals. A proposed modification that,
under the same protocol (fixed first-epoch ICs, same grid, same frame), predicts a deviation
from the Newtonian baseline **larger than a planet's floor** would have shown up here — it is
excluded at that amplitude. The gravity-as-scarcity constraint row in
[theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md) applies this bound. Its
numerical adjudication (ORB-10097, orrery `23fe253`) split the model's two local-field
readings against exactly this floor: the **multiplicative** reading exceeds Uranus's floor in
the primary galactocentric orientation (1.89× rms, 2.84× max; the six-axis orientation
envelope crosses the floor, so the tension is orientation-dependent), while the **screened**
reading is identically Newtonian — the explicit zero control — and is not constrained by this
bound at all. Verdict and qualifications live in the theory doc's ledger.

## Lineage

- **Datasets:** astrolabe `data/processed/derived/<planet>_newtonian_residuals.parquet`
  (+ `.json` sidecars), 366 epochs each — ingested by tycho, ORB-10094 (`ws_astrolabe`).
- **Baseline producer:** faraday, ORB-10093 (`ws_orrery`) — orrery commit `f5e02e3`,
  `lab/sims/solar-system-nbody/baseline/newtonian_2016_2026.parquet` + `summary.json`.
- **Ephemeris side:** JPL Horizons state vectors, planetary-system barycenters (ids 1–8),
  Sun body center `500@10`, ICRF — astrolabe `ephemeris/<planet>_2016_2026` (ORB-10076).
- **Exchange contract:** astrolabe `docs/baseline-interface.md`.
- **First consumer:** the ORB-10097 scarcity falsifier — faraday, orrery commit `23fe253`,
  `lab/sims/solar-system-nbody/scarcity/summary.json` (multiplicative signature vs these
  floors; screened zero control). Reconciled into the theory ledger by kepler, ORB-10098.
- Run records: faraday `runs/26-07/run-20260711T011635.md` (baseline export), tycho
  `runs/26-07/run-20260710-orb-10094-baseline-ingest.md` (ingest).
