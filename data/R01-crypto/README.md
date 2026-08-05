---
title: "R01 Crypto Data"
summary: "Local storage boundary for immutable and derived crypto research data."
tags: [parallax, crypto, market-data, data-registry]
related: ["data/README.md", "docs/research/R01-crypto/DATA.md", "docs/research/R01-crypto/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
---

# R01 crypto data

- `raw/` contains immutable candles, order-book captures, trades, quotes, and source observations.
- `processed/` contains reconstructible features and analysis-ready tables with provenance.
- `journal.sqlite3` is the crypto trade-thesis journal when created by the CLI.
- `research.sqlite3` is the R01 research-experiment journal when created by the CLI.

Actual datasets and databases are local ignored artifacts. Their contracts, source timestamps,
checksums or snapshot IDs, code revisions, and transformation versions belong in the linked R01
documents and experiment records.
