---
title: "H02 Active-Fluid Microstructure Features"
summary: "Tests whether persistence, refill, void, and resistance features add value beyond standard imbalance."
tags: [parallax, crypto, microstructure, active-fluid]
related: ["docs/research/R01-crypto/hypothesis/H01-standard-order-flow-and-queue-imbalance.md", "docs/research/R01-crypto/PHYSICS_MODEL.md", "docs/research/R01-crypto/MICROSTRUCTURE.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
hypothesis_id: H02
outcome: untested
---

# H02: Active-fluid microstructure features

## Claim

Wall persistence, refill, liquidity voids, effective resistance, and cancel-versus-fill features
add stable short-horizon Bitcoin mid-price information beyond standard order-flow and queue
imbalance.

## Motivation and mechanism

Visible depth is resistance only while it survives a challenge. Refill and cancellation describe
the adaptive evolution of the book and may distinguish durable absorption from transient displayed
liquidity.

## Predicted observables

- The added feature families improve out-of-sample forecast calibration or discrimination.
- Incremental information survives a lagged, executable horizon and measured costs.
- The pressure-response relationship is reasonably stable across walk-forward windows.

## Plausible alternatives

The extra features may be noisy transforms of ordinary imbalance, encode reconstruction errors, or
win only through a large multiple-testing search.

## Baseline

The best validated H01 model using standard order-flow and queue imbalance.

## Rejection criteria

Reject if the added features provide no incremental out-of-sample forecast or economic value after
costs and multiple-testing control.

## Experiment queue

No standalone experiment is registered yet.

## Decision history

- 2026-08-03 — registered as the primary R01 microstructure hypothesis; untested.
