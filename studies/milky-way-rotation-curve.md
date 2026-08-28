---
title: "Measured Milky Way rotation curve and the MOND acceleration scale"
status: active
created: 2026-07-10
updated: 2026-07-10
---

# Measured Milky Way rotation curve

The established-physics facts the `gravity-as-scarcity` rotation-curve claim is tested against:
what the Milky Way's circular-velocity curve actually looks like, and the acceleration scale at
which the mass discrepancy sets in.

## The measured curve

| Fact | Value | Source |
|---|---|---|
| Circular velocity at the Sun's radius R₀ | v_c(R₀) = 229.0 ± 0.2 km/s (statistical); ~2–5% systematic | Eilers, Hogg, Rix & Ness 2019 |
| Slope of the curve beyond the inner disk | dv_c/dR = **−1.7 ± 0.1 km/s/kpc** — gently *declining*, not perfectly flat | Eilers et al. 2019 |
| Range measured | 5 ≤ R ≤ 25 kpc (inner 5 kpc excluded — the bar breaks axisymmetry) | Eilers et al. 2019 |
| Method | Jeans equation in an axisymmetric potential, ≳23,000 luminous red-giant stars (APOGEE spectra + WISE/2MASS/Gaia photometry, spectrophotometric parallaxes) | Eilers et al. 2019 |
| Implied dark-halo mass within the virial radius | (7.25 ± 0.26) × 10¹¹ M☉ | Eilers et al. 2019 |

**Citation.** A.-C. Eilers, D. W. Hogg, H.-W. Rix, M. K. Ness, "The Circular Velocity Curve of the
Milky Way from 5 to 25 kpc," *Astrophysical Journal* **871**, 120 (2019).
DOI [10.3847/1538-4357/aaf648](https://doi.org/10.3847/1538-4357/aaf648); arXiv:1810.09466;
ADS bibcode 2019ApJ...871..120E. *(Verified against the ADS record and the arXiv abstract on
2026-07-10.)*

The load-bearing subtlety for our ledger: the real curve is **not flat** — it declines gently
(−1.7 km/s/kpc). "Flat rotation curve" is the textbook shorthand for "far above the Keplerian
v ∝ R^(−1/2) a pure baryonic disk would give," not literal constancy. A model that produces a
still-declining curve in the outer disk is not automatically wrong; it must be compared to the
*measured* slope, not to a flat line.

## The MOND acceleration scale

| Fact | Value | Source |
|---|---|---|
| Milgrom's acceleration constant a₀ | a₀ ≈ 1.2 × 10⁻¹⁰ m/s² (= 1.2 × 10⁻⁸ cm/s²), fitted from spiral rotation curves | M. Milgrom 1983 |

**Citation.** M. Milgrom, "A modification of the Newtonian dynamics as a possible alternative to
the hidden mass hypothesis," *Astrophysical Journal* **270**, 365 (1983) — the first of three
consecutive 1983 papers (ApJ **270**, 365 / 371 / 384) introducing MOND. The a₀ ≈ 1.2 × 10⁻¹⁰
m/s² value is the canonical fit from spiral-galaxy rotation curves. *(a₀ value verified 2026-07-10;
recorded as the standard fitted constant.)*

Below a₀ the observed accelerations exceed the Newtonian-baryonic prediction — the mass
discrepancy. Any modified-gravity account of rotation curves must reproduce this scale, not just
the shape. This is the quantitative bar behind the discussion's recurring "right shape, wrong
magnitude" verdict: the scarcity headroom effect produced a ~10–25% boost where galaxies need
~2×.

## The dataset our sim actually fit (ORB-10075 lineage)

The Orrery experiment [scarcity-rotation-curve-fit](../../orrery/lab/sims/scarcity-rotation-curve-fit/)
does **not** fit the Eilers curve directly; it fits a Gaia DR3 median-`v_φ` curve that **tycho**
derived and delivered in ORB-10075. Lineage, from the delivered sidecar
(`astrolabe/data/processed/derived/mw_rotation_curve.json`):

- **Product:** `derived/mw_rotation_curve.parquet` — 30 rows, columns `R_kpc, v_c_kms, v_c_err_kms,
  n_stars`; 4.0–25.0 kpc in 0.5 kpc bins, `|z| < 0.5 kpc`, min 30 stars per bin.
- **Three-catalog Gaia lineage:** `mw_disk_gaia`, `mw_disk_outer_gaia`, `mw_disk_anticenter_gaia`
  (deduplicated on `source_id`); Bailer-Jones photogeometric distances (`r_med_photogeo`) carry
  the far bins; fetched 2026-07-10.
- **Galactocentric frame:** R₀ = 8.122 kpc, z_sun = 20.8 pc, v_sun = (12.9, 245.6, 7.78) km/s.
- **Known bias — the reason the fit carries a drift nuisance:** the curve is **median `v_φ`, NOT
  asymmetric-drift corrected**, so it is biased *low* by ~5–15 km/s for a mixed-population sample
  (stated in the sidecar `method` field). Both the scarcity and Newtonian fits absorb this with the
  same bounded constant asymmetric-drift term; the sim's pinned-lower-bound drift and its coherent
  held-out underprediction (see the theory ledger) are downstream of this uncorrected bias — a
  constant offset cannot capture a drift that varies with radius.

## What hangs on this

- [theory/gravity-as-scarcity](../theory/gravity-as-scarcity/) — the rotation-curve ledger row
  cites this note for (a) the measured slope the model is judged against, (b) the a₀ magnitude bar,
  and (c) the dataset provenance and its asymmetric-drift bias.
