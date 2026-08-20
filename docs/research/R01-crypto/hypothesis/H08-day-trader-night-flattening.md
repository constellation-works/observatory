---
title: "H08 Day-Trader Night Flattening"
summary: "Tests whether US night hours have more negative Bitcoin hourly drift because day traders flatten to lock in P&L."
tags: [parallax, crypto, clock-phase, day-traders, night-session]
related: ["docs/research/R01-crypto/hypothesis/H03-clock-phase-conditioning.md", "docs/research/R01-crypto/hypothesis/H06-speculative-influx-weekend-flow.md", "docs/research/R01-crypto/experiments/E01-bitstamp-us-night-hourly-drift.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md"]
created_on: 2026-08-19
updated_on: 2026-08-19
status: active
research_id: R01
domain: crypto
hypothesis_id: H08
outcome: revised
---

# H08: Day-trader night flattening

## Claim

Bitcoin/USD hourly close-to-close simple returns are more negative during the US night window
21:00–00:00 `America/Los_Angeles` than during complementary hours in the same sample, because
US-hours day traders sell (flatten) inventory to lock in P&L as their session ends.

The primary clock is Pacific local time, DST-aware. A secondary copy of the same three-hour window
in `America/New_York` is part of the claim's stated PST/EST night session, not a substitute primary
window. Hour labels are the bar-open hour in that timezone: 21, 22, and 23.

## Motivation and mechanism

Crypto trades continuously, but many discretionary traders do not. After the US waking day, short-
horizon traders may flatten rather than hold inventory overnight, producing net selling and a
downward drift in the first hours of their night.

The mechanism is a story about *who* is selling and *why*. Hourly return seasonality can support
the directional prediction without identifying day traders, lock-in behavior, or inventory transfer.
H03 treats clock phase as a boundary condition on book response; this claim treats a specific night
window as a directional force.

## Predicted observables

- **Primary prediction:** mean hourly simple return in 21:00–00:00 `America/Los_Angeles` is below
  the mean in complementary hours, and below zero, on a 1-minute Bitcoin/USD tape aggregated to
  hourly bars.
- **Secondary predictions:** the same three-hour window in `America/New_York` is also more negative
  than complementary hours; the night gap is larger on weekdays than weekends, when US day traders
  are less active; US equity cash close (16:00 `America/New_York` on weekdays) is not required to
  carry the whole effect if flattening happens later, at sleep time rather than at the cash close.
- **Information cutoff:** only prices observable at or before each hourly close. No future bars,
  no revised prints after the local snapshot.

## Plausible alternatives

- Unconditional 24/7 drift, with the night window selected after seeing the path.
- Volatility or jump seasonality without a signed drift (fat left tails in one hour, not a mean
  leak).
- Asia-session flow, scheduled US data, or a single crash hour/month dominating the mean.
- Exchange-specific Bitstamp microstructure rather than a Bitcoin-wide night effect.
- Day-trader flattening at US cash close (16:00 Eastern) rather than at 21:00–00:00 Pacific.
- Lower overnight liquidity amplifying two-sided noise, not net selling.

Trader identity, closing-order flags, and inventory are required to distinguish flattening from
these alternatives. They are not in the candle tape.

## Baseline

Unconditional hourly Bitcoin simple returns over the same timestamps (passive hold; no clock
filter). The night window must be more negative than this complementary-hour mean, not merely
negative in a down market.

## Rejection criteria

Reject the directional claim if the primary Pacific 21:00–00:00 mean hourly return is not below
the complementary-hour mean. Weaken or reject the mechanism if an apparent night leak is as strong
on weekends as on weekdays, is confined to one crash hour or one month, or if later flow or
inventory evidence shows no net selling by short-horizon US-session traders.

## Experiment queue

- [E01 Bitstamp US night hourly drift](../experiments/E01-bitstamp-us-night-hourly-drift.md) —
  exploratory (`preregistered: false`); cannot promote this claim. Methodology:
  [E01 script](../../../../notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.py),
  [E01 notebook](../../../../notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.ipynb).

## Decision history

- 2026-08-19 — registered from an already-opened Bitstamp 1-minute tape. The claim is frozen as
  stated; it is not a restatement after seeing results.
- 2026-08-19 — [E01](../experiments/E01-bitstamp-us-night-hourly-drift.md) exploratory evaluation:
  `revised`. The primary Pacific 21:00–00:00 window is not more negative than complementary hours.
  The Eastern copy is directionally negative and stronger on weekdays, but not distinguishable at
  conventional significance, and it cannot identify day traders. A restated clock belongs in a new
  hypothesis and a preregistered experiment on unseen data.
