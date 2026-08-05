---
title: "H03 Clock-Phase Conditioning"
summary: "Tests whether participant timing changes the response of Bitcoin prices to book pressure."
tags: [parallax, crypto, clock-phase, market-sessions]
related: ["docs/research/R01-crypto/hypothesis/H02-active-fluid-microstructure-features.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md", "docs/research/R01-crypto/MICROSTRUCTURE.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
hypothesis_id: H03
outcome: untested
---

# H03: Clock-phase conditioning

## Claim

Minute-of-week, geographic session, and scheduled market clocks change the response of Bitcoin
mid-price to otherwise similar order-book pressure because the active participant population and
liquidity process vary through time.

## Motivation and mechanism

Crypto trades continuously, but humans, institutions, settlement processes, and periodic algorithms
do not. Clock phase may act as a boundary condition for depth, spread, refill, and pressure response.

## Predicted observables

- Session-normalized pressure improves calibration over an unconditional microstructure model.
- Conditioned coefficients remain stable across daylight-saving and walk-forward boundaries.
- Gains appear across preregistered sessions rather than one selected time bucket.

## Plausible alternatives

Apparent clock effects may be volatility seasonality, scheduled announcements, exchange-specific
outages, or post-selection over many time buckets.

## Baseline

The best validated H02 model without clock-state features.

## Rejection criteria

Reject if session-conditioned coefficients do not improve out-of-sample calibration or stability.

## Experiment queue

No standalone experiment is registered yet.

## Decision history

- 2026-08-03 — registered as untested.
