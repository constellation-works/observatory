---
title: "H01 Standard Order Flow and Queue Imbalance"
summary: "Tests whether standard imbalance signals predict executable short-horizon Bitcoin mid-price movement."
tags: [parallax, crypto, order-flow-imbalance, queue-imbalance]
related: ["docs/research/R01-crypto/hypothesis/README.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md", "docs/research/R01-crypto/MICROSTRUCTURE.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
hypothesis_id: H01
outcome: untested
---

# H01: Standard order flow and queue imbalance

## Claim

Standard order-flow imbalance and queue imbalance predict the direction or magnitude of future
Bitcoin mid-price movement at short horizons observable after the signal is formed.

## Motivation and mechanism

Aggressive flow and asymmetric resting depth may reveal near-term pressure on the best quotes. This
is established prior art and serves as the required control for later microstructure hypotheses, not
as Parallax's claimed edge.

## Predicted observables

- Increasing signed imbalance changes the conditional distribution of future mid-price returns.
- Any useful effect persists to at least one executable horizon after latency and measured cost.
- Estimates remain directionally stable across time-aware out-of-sample windows.

## Plausible alternatives

Bid-ask bounce, timestamp errors, book-reconstruction gaps, or contemporaneous price movement may
create apparent predictability. Mid-price labels, lagged execution, and reconstruction audits are
required controls.

## Baseline

A constant forecast and a model using only the asset's own lagged returns.

## Rejection criteria

Reject if there is no stable out-of-sample lift over the baseline, or if the effect decays before an
executable horizon after measured costs.

## Experiment queue

No standalone experiment is registered yet.

## Decision history

- 2026-08-03 — registered as an untested baseline hypothesis.
