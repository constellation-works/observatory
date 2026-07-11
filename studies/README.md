# studies/

Sourced notes on **established physics** — the facts our theories and sims lean on. Maintained
by **kepler** (`agentbase/kepler/memory`).

## The contract

One note per fact-cluster (a bound, a measured value, an experiment lineage). Each carries
frontmatter (`title`, `status`, `created`, `updated`) and, for every load-bearing fact, a
**verifiable citation** — paper, textbook chapter, or measured value with source. House rule:
citations are checked against the actual source before being recorded; a fact that can't be
sourced right now is written `conjecture — to verify`, never stated as settled.

`theory/` docs and sim docstrings point here instead of restating physics from memory —
one place to be wrong, one place to fix.

## Notes

- [milky-way-rotation-curve](milky-way-rotation-curve.md) — measured MW circular-velocity curve
  (Eilers et al. 2019), the MOND acceleration scale, and the ORB-10075 Gaia DR3 dataset lineage.
- [chsh-bounds](chsh-bounds.md) — the classical, quantum, and measured CHSH bounds.
- [solar-system-ephemeris-precision-floor](solar-system-ephemeris-precision-floor.md) — per-planet
  Newtonian-omission residuals vs JPL Horizons 2016–2026 (the AU-scale bound), Mercury's GR
  excess, and the ORB-10093/ORB-10094 lineage.

## Wanted (backlog)

- Lense–Thirring frame-dragging magnitude/falloff (needed by
  [theory/gravity-as-scarcity](../theory/gravity-as-scarcity.md))
- Grangier–Roger–Aspect 1986 antibunching (needed by
  [theory/swirl-photon](../theory/swirl-photon.md))
