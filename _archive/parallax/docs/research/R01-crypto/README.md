---
title: "R01 Crypto"
summary: "Charter and evidence boundary for Parallax research into crypto markets and microstructure."
tags: [parallax, crypto, market-research]
related: ["docs/research/R01-crypto/PROTOCOL.md", "docs/research/R01-crypto/hypothesis/README.md", "docs/research/R01-crypto/experiments/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
---

# R01 crypto

## Purpose

Test whether observable market structure or cross-market state supports systematic strategies that
outperform a passive Bitcoin benchmark after realistic costs and risk.

## Boundary

- Public and explicitly authorized market data only.
- Research, replay, paper, and shadow operation are allowed stages.
- Live order placement and capital allocation remain disabled without Daniel's explicit approval
  and a separate execution and risk review.

## Evidence contract

- UTC point-in-time observations with immutable raw storage.
- Signals execute no earlier than the first observation after their inputs were available.
- Bitcoin buy-and-hold over identical timestamps is the default passive benchmark.
- Fees, spread, slippage, funding, turnover, latency, and outages are material.
- Time-aware out-of-sample and walk-forward evaluation is required.

The domain-neutral contract lives in [`../../RESEARCH_PROTOCOL.md`](../../RESEARCH_PROTOCOL.md).
Crypto-specific rules live in [`PROTOCOL.md`](PROTOCOL.md), and the canonical hypothesis ledger is
the [`hypothesis/` registry](hypothesis/README.md). [`RESEARCH_AGENDA.md`](RESEARCH_AGENDA.md)
preserves the program-wide motivation and sequence; standalone hypothesis records freeze each
claim. Experiments and their outcomes live in the [`experiments/` registry](experiments/README.md),
and evolving domain knowledge may be added under [`docs/`](docs/README.md).
