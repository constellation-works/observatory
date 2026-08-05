---
title: "R01 Crypto Research Protocol"
summary: "Benchmark, cost, preregistration, evaluation, and promotion rules for crypto research."
tags: [parallax, crypto, research-protocol]
related: ["docs/RESEARCH_PROTOCOL.md", "docs/research/R01-crypto/README.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md"]
created_on: 2026-07-31
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
---

# R01 crypto research protocol

The crypto domain tests whether a systematic strategy can outperform Bitcoin buy-and-hold out of
sample after all material trading frictions, without taking unacceptable risk.

## Definition of "beat the market"

The benchmark is a passive long Bitcoin position over the exact same out-of-sample timestamps.
Both strategy and benchmark are evaluated net of the measured one-way cost required to establish
their positions. Parallax records a win only when all three are true:

1. strategy net total return is positive;
2. strategy net total return exceeds benchmark net total return; and
3. strategy net return divided by maximum drawdown exceeds the benchmark's value.

The second term is deliberately simple and auditable. Because both series use the same interval,
it avoids choosing an annualization convention just to improve the score. Cash-like inactivity
cannot win because positive strategy return is also required.

## Cost contract

Cost is measured from our fills and contemporaneous best bid/ask, separated into fee, half-spread,
and execution slippage beyond the touch. The initial screen rejects any proposed trade with less
than 15 bps gross expected edge, and also rejects any proposal whose expected edge does not exceed
the measured round-trip cost. Assumed costs may be used for stress testing but cannot support a
promotion claim.

## Preregistration contract

Before a discretionary or paper trade, record the hypothesis, entry rule, exit rule, invalidation,
size, and expected edge in bps. The journal enforces append-only preregistrations with SQLite
triggers. Fill, fees, slippage, and result are appended afterward; they never replace the original
thesis.

## Crypto evaluation order

1. Start with a trivial Bitcoin buy-and-hold benchmark.
2. Test mechanics on synthetic data where the expected answer is known.
3. Develop only on training data and make bounded choices on validation data.
4. Evaluate once on the untouched test interval.
5. Repeat with rolling walk-forward splits across distinct market regimes.
6. Stress costs, latency, missing data, exchange outages, and parameter sensitivity.
7. Compare against simpler strategies before attributing value to complexity.

Random row-level train/test splits are not valid for time-series claims. A profitable backtest is
evidence for further testing, not evidence that live profit will follow.

## Promotion ladder

`research → historical replay → paper → shadow → live`

Advancement requires a recorded review of the prior stage. Live capital is outside the initial
scope and requires Daniel's explicit approval, documented risk limits, a kill switch, and a
separate execution design review.
