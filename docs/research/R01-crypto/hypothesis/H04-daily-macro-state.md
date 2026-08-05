---
title: "H04 Daily Macro State"
summary: "Tests whether lagged traditional-market shocks improve forecasts of Bitcoin daily state."
tags: [parallax, crypto, macro-state, distributed-lag]
related: ["docs/research/R01-crypto/hypothesis/README.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md", "docs/research/R01-crypto/PROTOCOL.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
hypothesis_id: H04
outcome: untested
---

# H04: Daily macro state

## Claim

Point-in-time traditional-market shocks contain lagged information that improves forecasts of
Bitcoin's daily return, volatility, liquidity, or coupling regime beyond Bitcoin's own history.

## Motivation and mechanism

Global risk appetite, liquidity, rates, the dollar, and volatility may condition Bitcoin's daily
state. Predictive connection does not by itself establish structural causality or capital flow.

## Predicted observables

- A small preregistered distributed-lag or VAR model improves walk-forward forecasts.
- Improvements remain after common-shock and asynchronous-market timing controls.
- Daily state may predict volatility or liquidity more reliably than return direction.

## Plausible alternatives

Common news, omitted variables, stale cash-market prices, or BTC autocorrelation may create apparent
cross-market direction.

## Baseline

A Bitcoin-only daily autoregression with the same walk-forward evaluation.

## Rejection criteria

Reject if there is no stable walk-forward lift or if apparent direction disappears after
common-shock and information-timing controls.

## Experiment queue

No standalone experiment is registered yet.

## Decision history

- 2026-08-03 — registered as untested.
