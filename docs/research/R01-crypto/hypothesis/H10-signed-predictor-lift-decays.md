---
title: "H10 Signed Predictor Lift Decays"
summary: "Tests whether public signed Bitcoin predictors lose walk-forward lift after cost, so the research product is the lifetime of that lift, not a standing rule."
tags: [parallax, crypto, nonstationarity, decay, adaptive-markets]
related: ["docs/research/R01-crypto/hypothesis/H01-standard-order-flow-and-queue-imbalance.md", "docs/research/R01-crypto/PROTOCOL.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md"]
created_on: 2026-08-20
updated_on: 2026-08-20
status: active
research_id: R01
domain: crypto
hypothesis_id: H10
outcome: untested
---

# H10: Signed predictor lift decays

## Claim

In Bitcoin, a public signed predictor does not persist as a trading rule. If a frozen, point-in-time
feature — lagged returns, clock membership, order-flow or queue imbalance, or a lagged daily macro
shock — shows signed lift over its baseline in a discovery window, that lift decays to indistinguishable
from the baseline, or below the measured (or 15 bps gross screen) round-trip cost, in later
walk-forward blocks after execution lag.

The research product is the measured lifetime or half-life of that lift, not an entry rule to keep
running.

Population: Bitcoin/USD (spot or linear perp) at the horizon named by the predictor class.
Discovery and test blocks are contiguous in time, non-overlapping, and purged so no discovery label
uses test-period prices.

## Motivation and mechanism

A pattern that is public, signed, and larger than cost is what other participants are paid to
remove. Once it is in the book, the book changes. What remains may be compensation for risk or
inventory, a few seconds of mechanically decaying impact, or nothing.

H08 and H09 are compatible with this prior: the named night dump was not on the frozen clock, and
the 5-minute Polymarket lean is the coin already having moved. They do not test H10; they are why
the claim was written.

This is not a claim that nothing is measurable. Decay time, cost, and “this state has no edge” can
persist as facts after the free lunch is gone.

## Predicted observables

- **Primary prediction:** for a preregistered predictor in the class above, out-of-sample lift in
  the first walk-forward block after discovery is already smaller than discovery-window lift, and
  net of execution lag and round-trip cost is not above the baseline. A second later block does not
  restore a stable signed rule.
- **Secondary predictions:** any remaining gross predictability is concentrated at horizons shorter
  than the cost screen; clock or volume slices where participation is higher show faster decay;
  restating the same rule after seeing the decay is not a persistence result.
- **Information cutoff:** only features observable at the signal time. Labels are measured from the
  lagged executable price. Discovery-block fitting does not use later prices.

## Plausible alternatives

- A risk premium or inventory compensation that *should* persist because someone is being paid.
- Slow structural demand (ETF flow, options hedges) that looks like a rule but is not an arbitrage.
- Apparent decay from a badly timed split, a single crash block, or overfitting in discovery.
- The predictor was never public or never large enough to attract offsetting flow.

## Baseline

Treat a discovery-window signed edge as if it were still the rule in later blocks (frozen
coefficients, same lag and cost). H10 requires that this continuation loses to the no-edge forecast
(constant or own-return baseline already named by the predictor's parent hypothesis).

## Rejection criteria

Reject for a given predictor class if walk-forward net lift stays above the cost screen across at
least two later non-overlapping regimes after discovery is closed. That is a persistent rule for
that class, not a lifetime. Weaken the claim if decay is only a one-block crash or only appears
when the discovery window was itself selected after seeing the path.

H01–H07 remain testable. This claim constrains how their results are reported: lifetime and
walk-forward death, not a mascot clock or a standing long/short.

## Experiment queue

No standalone experiment is registered yet. A first test should pick one frozen predictor class
(H01 imbalance or a lagged-return / clock dummy on candles), split discovery vs later blocks before
fitting, and print lift by block after lag and cost.

## Decision history

- 2026-08-20 — registered from the prior that public signed patterns are eaten; not a restatement
  of H08 or H09. No evaluation data were opened for this claim.
