---
title: "H07 Multiscale Conditioning"
summary: "Tests whether validated daily states improve validated microstructure pressure-response models."
tags: [parallax, crypto, multiscale-model, regime-conditioning]
related: ["docs/research/R01-crypto/hypothesis/H02-active-fluid-microstructure-features.md", "docs/research/R01-crypto/hypothesis/H03-clock-phase-conditioning.md", "docs/research/R01-crypto/hypothesis/H04-daily-macro-state.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
hypothesis_id: H07
outcome: untested
---

# H07: Multiscale conditioning

## Claim

Daily macro or speculative states that survive independent tests improve the stability, calibration,
or economic value of a validated microstructure model by conditioning its pressure-response
coefficients.

## Motivation and mechanism

Local book pressure may produce different price responses under different daily liquidity, risk, or
participant states. Integration is justified only after each component earns its place separately.

## Predicted observables

- Mixed-frequency conditioning improves untouched performance over the best simpler model.
- Gains survive measured cost and remain calibrated across walk-forward regimes.
- The combined model does not rely on a failed component or a selected best-looking horizon.

## Plausible alternatives

Daily states may add complexity without information, duplicate clock or volatility features, or
overfit a small number of effective daily observations.

## Baseline

The best independently validated H02 or H03 microstructure model without daily-state conditioning.

## Rejection criteria

Reject if mixed-frequency conditioning adds no stable out-of-sample forecast or economic value.

## Experiment queue

No standalone experiment is registered yet.

## Decision history

- 2026-08-03 — registered as untested.
