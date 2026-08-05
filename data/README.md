---
title: "Parallax Data Registry"
summary: "Ownership and partitioning rules for local data across numbered research programs."
tags: [parallax, data, research-conventions]
related: ["docs/ARCHITECTURE.md", "docs/research/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
---

# Parallax data registry

Every local dataset and domain-specific state file belongs to exactly one numbered research program
and lives under its complete research slug:

```text
data/R<NN>-<title>/
  raw/                 immutable source observations
  processed/           reproducible derived datasets
  research.sqlite3     append-only experiment journal, created on demand
  ...                  other domain-specific state with documented provenance
```

The directory names mirror `docs/research/RNN-title/` and `notebooks/RNN-title/`. Never place
domain data directly under `data/raw/` or `data/processed/`, and never mix observations from two
research programs merely because they use the same file format.

A dataset used by another program retains one owning research slug. The consuming experiment links
the owning data contract, immutable snapshot, and transformation rather than silently copying or
reclassifying it. Raw and processed payloads remain local and ignored; only registry documents and
empty boundary markers are tracked.
