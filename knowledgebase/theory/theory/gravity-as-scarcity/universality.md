## The form and universality adjudication — the ORB-10167 and ORB-10169 measurements

The two final shape measurements on the boost have run (faraday; the apparatus records are
the numbers of record:
[scarcity-rotation-curve-fit](../../../orrery/lab/sims/scarcity-rotation-curve-fit/)
`assets/results.json`, orrery `8990fd3`;
[sparc-scarcity-universality](../../../orrery/lab/sims/sparc-scarcity-universality/)
`assets/results.json`, orrery `1ab8085`). The first asks whether the MW band ever identified
the boost's functional form; the second asks whether the fitted β is one number across
galaxies. The answers: no, and no — and the second *no* is the family's predeclared kill
condition firing.

### ORB-10167 — form degeneracy on the MW band

The Sanders-form Yukawa (ORB-10161 §A2's shape control,
[two-substance-vortex-vacuum](../two-substance-vortex-vacuum/)) joined the exact
ORB-10077/10082 protocol as a fourth model: same predeclared 5–15 kpc fit and 15–18.75 kpc
held-out bands, same bounded drift nuisance, 27 profile variants, 200 bootstrap resamples,
seed 42 — with the parameter count kept honest at k = 4 (mass normalization, α, ξ, drift;
faraday's own correction, its L-0006). Measured:

- **The best fit lands on the analytic matching point.** α = −0.679, ξ = 4.642 kpc — the
  free fit found ORB-10161 §A2's matched parameters (α ≈ −0.68) on its own. RMSE 2.91 km/s
  vs scarcity's 2.70.
- **The point estimate prefers scarcity; the bootstrap cannot.** ΔAIC(scarcity − Yukawa) =
  −369.6, same sign across all 27 profile variants (−479.7 to −138.9) — but the
  200-resample bootstrap 95% interval spans **[−503.9, +1051.9]**. Per the predeclared
  decision rule (decisive only if the interval excludes zero) the verdict is
  **shape-degenerate**: the band does not distinguish exponential saturation from the
  scarcity form's 1/r tail.
- **Held-out: both models underpredict coherently.** Scarcity 5.26 km/s (+4.86 under),
  Yukawa 5.52 km/s (+5.11 under) — the 13–16 kpc flattening eludes both forms alike.

Caveats, both faraday's: the Yukawa multiplier is the point-source kernel over the spherical
enclosed-mass surrogate (the disk convolution flagged in ORB-10161 §A2 remains undone), and
the shared drift nuisance pins its lower bound as in every run on this band. Neither rescues
form identification: they grade how far the degeneracy verdict extrapolates, not the measured
inability to separate the shapes here.

**What this does to ORB-10077.** The fit's ΔAIC ≈ −10⁵ over baryons stands untouched, and
the point-estimate preference for scarcity over the Yukawa (all 27 variants) enters the
ledger as a recorded fact. But the band never tested the *functional form*: a canonical
Yukawa — the shape belonging to an independently refuted fifth-force family (ORB-10161
Branch A) — sits inside the sample's resolving power. The evidential content of the family's
one decisive empirical result is hereby restated at its measured size: **a ~5 kpc
rise-and-saturate boost beats baryons on the MW band — carrier unidentified
(ORB-10157/ORB-10170), functional form unidentified (ORB-10167).**

### ORB-10169 — the universality measurement: the kill condition fired

The "one constant, two observables" question — open since founding, sharpened by ORB-10161
§A5 into a predeclared kill condition — has its answer. Faraday fit three models to 149
galaxies / 3,150 points from the SPARC-derived catalog (tycho ORB-10168 lineage; standard
Q ≤ 2 and inclination ≥ 30° cuts), under one uniform nuisance policy (one positive baryonic
normalization per galaxy, no drift term) and honest parameter counting (global-β scarcity
k = 150; per-galaxy-β scarcity k = 298; global-a₀ MOND control k = 150). Measured:

- **Global β = 5.526 kpc** — 5% from the MW's fitted 5.25. The proximity is real and is
  recorded; it does not save what follows.
- **Per-galaxy β wins by 51,723 AIC** (106,619 global → 54,896 per-galaxy) — the sample
  overwhelmingly rejects one shared length.
- **β_i tracks galaxy size:** Spearman ρ = 0.343, p = 1.86×10⁻⁵ against disk scale length
  (and ρ = 0.401, p = 4.1×10⁻⁷ against characteristic acceleration; per-galaxy β_i spans
  ~0–21.3 kpc, median 3.07). Constant-β heterogeneity: χ² = 48,362 on 121 dof, p
  underflowing to zero.
- **The same-policy MOND control organizes the data better by five figures:** global-a₀
  AIC 29,198 vs global scarcity's 106,619 (gap 77,421; fitted a₀ = 1.41×10⁻¹⁰ m/s²). The
  discrepancy organizes by *acceleration*, not by any fixed length — the measured
  radial-acceleration-relation verdict (McGaugh, Lelli & Schombert 2016;
  [studies/fifth-force-searches](../../studies/fifth-force-searches.md)).

The predeclared kill condition — a positive β_i–size correlation at p < 0.01 plus rejection
of constant β_i at p < 0.01; in the task's words, *"if β_i systematically tracks galaxy
size … the fixed-β scarcity form is refuted as a universal law — the same verdict Sanders'
r₀ received"* — **is met on both prongs, by orders of magnitude. The fixed-β scarcity form
is refuted as a universal law at this apparatus.** The proposer's knife cuts deepest when it
is their own predeclared condition that fired; it fired.

**Caveat grading — what limits decisiveness vs what cannot be explained away.** All declared
by faraday, who limits the verdict explicitly to this apparatus and likelihood:

- *Spherical enclosed-mass surrogate over thin-disk component curves* — a shape systematic
  applied uniformly to every galaxy and every model. It inflates absolute misfit and can
  bias any individual β_i; it grades the exact AIC magnitudes.
- *Statistical-only errors* — absolute χ² is unacceptable for **all** fits, the MOND control
  included, so no model earns an absolute-goodness claim here; the designed instrument is
  relative comparison under a shared likelihood.
- *Uniform no-drift nuisance policy* — differs from the MW apparatus (which carries a
  bounded drift term), so the 5.53-vs-5.25 β comparison is same-family, not same-protocol.
- *Input provenance* — ORB-10168's delivery landed producer code but not the processed
  parquets; the validation parquets were reconstructed from the published HTTPS tables for
  this run (SHA-256 hashes recorded in the apparatus results; repair task per faraday
  L-0001/F2026-07-008).

Graded: these gate **decisiveness** — the exact AIC numbers, any absolute-fit statement, the
cross-apparatus identity of β. None of them gates the verdict, because none can manufacture
what was measured: a p ~ 10⁻⁵ correlation between β_i and galaxy size across 149 galaxies,
and a five-figure AIC gap between acceleration organization and fixed-length organization
computed under an *identical* likelihood and nuisance policy. A uniform systematic does not
know each galaxy's disk scale length.

**What refuses laundering.** Three facts stand in the ledger beside the refutation, per the
standing rules: scarcity's point-estimate preference over the Yukawa on the MW band (all 27
variants); the global-β proximity to the MW fit (5.53 vs 5.25 kpc); and the per-galaxy
scarcity form remaining a serviceable per-galaxy fitter (AIC 54,896). They are recorded
facts about a form now refuted as a universal law — they do not soften the verdict, and the
verdict does not erase them.
