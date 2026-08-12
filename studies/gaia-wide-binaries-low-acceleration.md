---
title: "Gaia DR3 wide binaries across the low-acceleration boundary — first footprint"
status: active
created: 2026-08-12
updated: 2026-08-12
---

# Gaia wide binaries across the low-acceleration boundary

The first stellar-scale datum against the **acceleration-organization problem** (standing
debt #2, [ledger](../ledger.md); ORB-10169's residue). Wide binaries with internal Newtonian
acceleration g_N = G(M₁+M₂)/s² below a₀ ≈ 1.2×10⁻¹⁰ m/s² sample the same regime where the
SPARC data organize by acceleration — but with no dark-matter degeneracy: if the organization
is a property of *gravity*, it should appear here; if binaries are cleanly Newtonian through
the boundary, that constrains any universal low-acceleration carrier.

**Source (tycho, ORB-10753, ws_astrolabe, 2026-08-12).** Gaia DR3 (`gaiadr3.gaia_source`,
DOI 10.5270/esa-1ugzkg7), local-volume cone: ra 180°, dec +40°, radius 25°, d < 200 pc
(ϖ > 5 mas, ϖ/σ_ϖ > 10, RUWE < 1.4, G < 18); 51,549 stars → **156 pairs** after El-Badry &
Rix-style selection (θ ∈ [1.5″, 1°], s ∈ [0.5, 50] kAU projected, 3σ parallax consistency,
escape-velocity PM gate). Analysis policy — thermal eccentricity prior f(e) = 2e, RUWE +
ΔRV triple veto (residual triple fraction recorded as 0.10), shifted-field chance-alignment
control (global R = 0.013; only the two lowest-g bins flagged at R ≈ 0.13–0.17) — was
**predeclared in the task plan before binning**, with the contested alternatives (flat
eccentricity prior, RUWE < 1.2) exercised only in the sensitivity table afterward.
Comparison is against forward-modeled Keplerian Monte Carlo mocks with the same projected
selection, not circular-orbit analytics. Apparatus: astrolabe `9c08636` (adapter, analysis,
end-to-end script, offline tests — 70 passed); datasets in the astrolabe Store
(`catalog/widebin_pairs_baseline`, `derived/widebin_vtilde_gn`, `derived/widebin_sensitivity`,
box-side); full binned tables in the ORB-10753 task record.

**Result.** The scaled relative-velocity statistic ṽ = Δv_sky / v_circ(s, M_tot), binned in
g_N over 5.5×10⁻¹² → 4.6×10⁻⁸ m/s²:

- Low-g regime (g_N < 1.2×10⁻¹⁰, n = 16): median ṽ = 0.702 vs Newtonian mock 0.677 —
  **no low-acceleration excess**.
- High-g regime (n = 140): median ṽ = 0.625 vs mock 0.687 — consistent.
- The verdict is unchanged under every contested-choice combination (thermal/flat prior ×
  RUWE 1.4/1.2): the low-g median never moves off 0.702, the mock never leaves 0.65–0.69.
- One mid bin (g_N ≈ 1.8×10⁻¹⁰) sits ~2σ high — isolated, not a coherent excess across the
  boundary.

**Verdict: Newtonian-consistent on this footprint — an honest null.** The predeclared
pipeline found no acceleration organization at stellar scale where the SPARC apparatus
measures it at galactic scale.

**What this does and does not constrain.** With n = 6–16 pairs per low-g bin on a single
25° cone, this footprint cannot adjudicate the contested literature (Chae 2023/2024 excess
vs Banik et al. 2024 null — both from vastly larger samples); it is a pipeline-validated
first datum, not a decisive measurement. What it *does* do: put the corpus's own predeclared
apparatus on the Newtonian side at current power, and make "the boost is a universal
property of gravity below a₀" carry a burden it has not met at stellar scale. The follow-up
with teeth is a multi-cone / full-sky campaign reaching n ≫ 10³ pairs below a₀ (tycho's
recommended v2; not yet filed).

## Consumers

- [gravity-as-scarcity](../theory/gravity-as-scarcity.md) § what remains live — the
  acceleration-organized-successor question now has a stellar-scale null to respect.
- [ledger](../ledger.md) — supported row + standing debt #2.
