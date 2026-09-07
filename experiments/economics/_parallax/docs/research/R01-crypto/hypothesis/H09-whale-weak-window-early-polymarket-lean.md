---
title: "H09 Whale Weak-Window Early Polymarket Lean"
summary: "Tests whether Polymarket BTC 5-minute Up/Down books lean toward the eventual winner in the first seconds, as would be expected if a well-capitalized actor hits weak windows."
tags: [parallax, crypto, polymarket, informed-flow, 5-minute]
related: ["docs/research/R01-crypto/hypothesis/H01-standard-order-flow-and-queue-imbalance.md", "docs/research/R01-crypto/hypothesis/H03-clock-phase-conditioning.md", "docs/research/R01-crypto/experiments/E02-btc-5m-early-polymarket-lean.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md"]
created_on: 2026-08-20
updated_on: 2026-08-20
status: active
research_id: R01
domain: crypto
hypothesis_id: H09
outcome: revised
---

# H09: Whale weak-window early Polymarket lean

## Claim

A well-capitalized actor who can move Bitcoin prefers "weak" moments: windows where a given
amount of pressure produces a larger signed move. If that actor (or flow that already knows the
intended direction) is present, the Polymarket BTC 5-minute Up/Down book already leans toward the
eventually winning side in the first seconds of the window, before the remaining time has resolved
the underlying.

The population is resolved Polymarket BTC 5-minute Up/Down markets. The signal is the Up-token
implied probability at a frozen elapsed time τ after `market_start`. The response is the market's
resolved direction. Primary τ values are 5s, 15s, and 30s of the 300-second window.

## Motivation and mechanism

Spot depth, participation, and attention are not constant. A whale minimizing the capital needed
to dictate a short-horizon print would wait for thin books, quiet seconds, or off-peak clocks, then
push in one direction. The same actor, or anyone who can see that pressure forming, can buy the
matching Polymarket token while it is still cheap.

The 5-minute Up/Down contract is a binary on the same coin over a short, repeating window, so it
is a natural place for that lean to show up as an early implied-probability gap in the direction
of the later winner.

This tape does not observe whale identity, BTC depth, or BTC prints. The mechanism is a story
about *who* moves *what*; the claim's testable content is the early Polymarket lean.

## Predicted observables

- **Primary prediction:** at each frozen τ ∈ {5, 15, 30} seconds after `market_start`, the
  Up-token mid `(bu + au) / 2` already points toward the resolved outcome. Concretely, the
  outcome-signed mid `s · (mid_up − 0.5)` with `s = +1` if the market resolves Up and `−1` if Down
  has a positive mean, and `sign(mid_up − 0.5)` agrees with the outcome more often than 50%.
- **Secondary predictions:** the early lean is larger in clocks that H03 would call thin (US night,
  weekend); larger when contemporaneous Polymarket bid depth `du + dd` is in the lowest tercile;
  and still present after dropping markets whose first-second mid already sits at an extreme
  (`|mid_up − 0.5| > 0.15`), so the result is not only windows that opened already decided.
- **Information cutoff:** only CLOB quotes with `ts_utc ≤ market_start + τ`. No later ticks, no
  end-of-window volume, no on-chain resolution after the fact. The `outcome` label is the
  market-level target, not a feature. In the local Kaggle tape that label is inferred from the
  final tick (winning side's bid near 0.99), not from chain.

Intended source for a first test: local Kaggle
`kachoio/polymarket-5-minute-crypto-updown-markets` v1,
`btc_markets.parquet` and `btc_ticks.parquet`, CC0-1.0, collector window 2026-03-24 22:10 UTC
through 2026-05-18 10:35 UTC. Per-second top of book; no Bitcoin price column.

## Plausible alternatives

- **Mechanical copy of an already-moved coin.** If Bitcoin has already printed most of the 5-minute
  return in the first seconds, an efficient Polymarket book *must* lean toward the winner. That is
  path dependence, not a whale. Distinguishing it requires an aligned BTC tape at or inside
  1-second resolution; Bitstamp 1-minute bars are too coarse (five bars per window).
- Uninformed noise around 0.5 that only collapses in the last seconds.
- Last-tick label leakage: `outcome` is inferred from the final bid, so any test that uses ticks
  near `market_end` as both signal and label is invalid.
- Collector outages clustered at the same UTC minutes (documented 15 Apr, 16 Apr, 18 Apr 2026
  gaps) or short markets with `n_ticks < 300`.
- Spread artifact: Up and Down are separate books, so `bu + bd ≠ 1`; a one-sided empty book can
  look like a lean.
- Other coins' 5-minute markets (ETH, SOL, …) behaving differently from BTC.

Whale identity, BTC order-book weakness, and PM-leads-spot versus spot-leads-PM cannot be
established from this Polymarket tape alone.

## Baseline

An uninformed 0.5 mid at the same τ: agreement rate 50%, mean outcome-signed mid 0. The early
lean must beat this, not merely look directional in a sample where one side happened to win more
often.

A later experiment that joins Bitcoin prints should add a second baseline: the lean predicted by
the contemporaneous coin return over `[market_start, market_start + τ]`. Residual PM lead after
that control is what would start to separate informed/PM-first flow from a mechanical copy.

## Rejection criteria

Reject the directional claim if, at every primary τ, the outcome-signed mid is not above 0 and
directional agreement is not above 50% on BTC 5-minute markets that have a non-null inferred
outcome and a quote at that τ. Weaken the whale/weak-window mechanism if an apparent early lean
vanishes after dropping already-extreme opens, is no stronger in thin-depth or night/weekend
windows, or is fully explained by contemporaneous Bitcoin returns once a second-level (or better)
BTC tape is joined.

## Experiment queue

- [E02 BTC 5-minute early Polymarket lean](../experiments/E02-btc-5m-early-polymarket-lean.md) —
  preregistered; cannot promote the whale mechanism (no BTC path). Methodology:
  [E02 script](../../../../notebooks/R01-crypto/E02-btc-5m-early-polymarket-lean.py),
  [E02 notebook](../../../../notebooks/R01-crypto/E02-btc-5m-early-polymarket-lean.ipynb).
- **Candidate, not preregistered** — BTC-residual test of the early lean at a 15-minute horizon.
  Source: local Kaggle `hugobde/polymarket-bitcoin-15min-up-or-down` v1 (`data.parquet`; columns
  `index`, `t`, `p`, `outcome`, `event`; 1-minute fidelity, no depth), joined to Bitstamp 1-minute
  `mczielinski/bitcoin-historical-data` v685. Question: does the outcome-signed lean at
  τ ∈ {1, 2, 3} minutes still predict the outcome after controlling for the contemporaneous BTC
  return over `[market_start, market_start + τ]`? This is the residual control E02 could not run.
  **Precondition before any use:** confirm whether `outcome` in that tape is also inferred from the
  final tick; if it is, the label-leakage rule under "Plausible alternatives" applies unchanged.
  Freeze τ, the control specification, and the rejection criterion before computing anything.

## Decision history

- 2026-08-20 — registered from the weak-window whale story before a notebook was run. Schema and
  coverage of the local 5-minute Kaggle tape were inspected; outcome-conditional leans were not
  computed.
- 2026-08-20 — [E02](../experiments/E02-btc-5m-early-polymarket-lean.md) preregistered evaluation:
  `revised`. Early Up mids at 5s/15s/30s already lean toward the inferred winner and beat 0.5.
  Night clocks show a larger lean; Polymarket depth does not; a mechanical copy of Bitcoin is
  untested. A restated informativeness claim and a BTC-residual experiment belong in a new `HNN`.
- 2026-08-20 — archived. No BTC-residual or restated-informativeness follow-up will be opened from
  this line; later work starts elsewhere.
- 2026-08-20 — re-opened at Daniel's request while reviewing the E02 record. The archive note above
  assumed no BTC-residual follow-up was runnable from this line. That was true at a 5-minute
  horizon, which needs a sub-minute BTC path unavailable locally, but the 15-minute Polymarket tape
  gives 15 one-minute bars per window, making τ ∈ {1, 2, 3} minutes resolvable against local
  Bitstamp 1-minute bars. Queued as a candidate above; deliberately left unpreregistered.
  The whale claim in this file is unchanged and still unsupported — E02's `revised` outcome stands,
  and the open question remains PM-leads-spot versus spot-leads-PM, not whale identity.
  Also recorded from that review: the last-tick leakage listed under "Plausible alternatives" is
  easy to walk into. Any test asking whether *late-window* odds moves predict the outcome is
  circular on a tape whose `outcome` is inferred from the closing book — E02's `QC_LAST_TICK`
  agreement of 1.000 is that rule measuring itself. Early-τ signals with a hard information cutoff
  are the only safe form on these tapes.
  Paused here; work resumes at a later session.
