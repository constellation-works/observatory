---
title: "R01 Crypto Order-Book Microstructure"
summary: "Hypotheses, data contracts, baselines, and evaluation rules for crypto order-book research."
tags: [parallax, crypto, microstructure, order-book]
related: ["docs/research/R01-crypto/README.md", "docs/research/R01-crypto/PHYSICS_MODEL.md", "docs/research/R01-crypto/PROTOCOL.md"]
created_on: 2026-07-31
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
---

# Order-book microstructure

## The hypothesis

A price move that outruns its resting liquidity leaves a void behind it. When momentum stalls
against the next wall that can absorb it, price reverts toward the side that still has depth. If
walls can be watched dissolving faster than the flow pushing into them, the next resting level
becomes a target rather than a guess.

Stated that way it is testable, and it is also not new. The prior art worth standing on:

| Component | Canonical treatment |
|---|---|
| Signed flow predicts short-horizon returns | Cont, Kukanov & Stoikov (2014), *The Price Impact of Order Book Events* |
| Touch imbalance predicts the next tick | Gould & Bonart (2016), *Queue Imbalance as a One-Tick-Ahead Price Predictor* |
| Impact is transient and decays | Bouchaud, Gefen, Potters & Wyart (2004) — the propagator model |
| Impact scales sublinearly in size | The square-root law of market impact |
| Trade prices manufacture fake mean reversion | Roll (1984) — bid-ask bounce |

Two of those are load-bearing here. The propagator is the shape the "recent drop leaves upward
ammo, decaying with volume" idea already has, so `flow_*` and `drift_*` implement it with the decay
constant as a *measured* parameter rather than a chosen one. Roll is why every label in this
package is a mid-price return: a series of executed prices carries bounce that looks exactly like
the reversion being hunted and cannot be traded.

Note the sign conflict. This hypothesis says a thin bid side below predicts reversion down into it.
The queue-imbalance literature finds price moves *toward* the thin side. Both features are computed
and neither sign is assumed; which dominates at which horizon is the empirical question.

## Three ways this fails, all measurable

**The visible book is not the liquidity.** Most resting orders in crypto are cancelled before they
are touched, and real depth is substantially latent: makers post reactively as price approaches,
and icebergs hide size. A void may simply refill on approach. Measurable directly: for each void,
check whether depth reappeared before price arrived.

**Cancel and fill are different events with the same footprint.** A wall that was eaten signals
informed flow and continuation. A wall that was pulled is a maker stepping away, often ahead of a
fake move. Raw depth cannot tell them apart. `maker_flow_*` separates them by subtracting executed
volume from the observed depth change. Caveat that cannot be engineered away: a level-2 feed yields
the *net* of additions and cancellations, never the gross of either. Gross needs level 3.

**Horizon versus cost.** These signals typically decay over seconds to tens of seconds. Retail
taker cost is roughly 10 to 20 bps round trip. If the half-life is 30 seconds this is not a manual
strategy at any size, whatever the R² says. `parallax book sweep` reports the decay curve and
prices every horizon against measured cost, so this is settled by data rather than by preference.

## Why a conditional-expectation study and not a backtest

Fitting `E[forward mid return | book state]` at every sampled instant uses millions of observations
where discretionary trading yields dozens. Distinguishing a 55% win rate from a coin flip needs
roughly 400 trades; the same question asked of the conditional mean is answerable from a day of
capture. If the conditional mean is flat, no execution scheme rescues it and the idea can be
dropped cheaply. A backtest is what comes after this says yes, not instead of it.

## Data contract

The recorder writes gzipped JSON lines, one record per message, verbatim and unparsed, tagged with
a local receive timestamp. It never reconstructs a book. Reconstruction is offline and replayable;
capture is not, so it carries as little logic as it can.

| Record | Meaning |
|---|---|
| `manifest` | capture version, symbol, streams, endpoints. Repeated at the head of every rotated file |
| `ws` | one websocket message: `depthUpdate`, `aggTrade`, or `bookTicker` |
| `snapshot` | REST depth snapshot, the anchor for offline reconstruction |
| `event` | connect, disconnect, failed snapshot, stop |

`event` records exist so that holes are labelled. A gap nobody can see is worse than a gap that is
marked, because the analysis will happily label across it.

Files rotate hourly to
`data/R01-crypto/raw/book/<SYMBOL>/<YYYY-MM-DD>/<HH>.jsonl.gz`. Roughly 1 to 3 GB per day per symbol
at 100 ms depth, so check disk before a long capture.

Reconstruction implements Binance's documented synchronisation procedure, including its failure
branch: when the update-id chain breaks, the assembler declares itself unsynced and refuses to
serve book states until a snapshot re-anchors it. Endpoints and the sync procedure were checked
against exchange documentation on 2026-07-31; reverify before diagnosing a remote error.

## Sampling and leakage

Sampling runs on a fixed wall-clock grid, not per event, so that busy periods do not dominate the
sample by producing more rows. Every sample instant is drained *before* the event stamped at that
instant is applied, so an update at T cannot leak into the sample at T. That ordering is enforced
by `test_a_sample_never_sees_an_update_stamped_at_its_own_instant`; the naive ordering inflated one
depth feature 56-fold.

Samples are dropped, and counted, when the book is unsynced or when the last update is older than
the staleness tolerance. Forward returns are `NaN` when the forward observation lands past a gap,
which stops a five-minute outage from becoming a one-second label.

Two further guards sit at the evaluation boundary, because a time-ordered split is not by itself
enough:

- **Execution lag.** A signal executes `--execution-lag-s` after the last observation it used, and
  its label is measured from that later price. The default is one sample, never zero: a predictor
  that trades at the mid it just measured is not one anybody can run, and at short horizons that
  single assumption is the difference between an edge and an artefact. Zero lag remains available
  as a sensitivity check, and the lag is printed in every result row so it cannot be lost.
- **Purge at the split.** Training rows whose label window closes at or after the first test
  observation were scored on test-period prices, so they are dropped and counted as `purged`. At a
  900 s horizon on a one-second grid that is roughly 900 rows of the training set fitted on the
  very window they are about to be judged against. The purge is subtracted from the training side
  only; the holdout keeps every labelled row past the split.

## Running it

```sh
# 1. Capture. Start this first: level-2 history cannot be backfilled.
uv sync --group capture
uv run parallax book record --symbol BTCUSDT

# 2. Reconstruct into a sampled feature table.
uv run parallax book build --symbol BTCUSDT --sample-seconds 1.0

# 3. Ask whether anything predicts forward mid returns, and at what horizon.
uv run parallax book sweep --round-trip-cost-bps 14.0
```

`--round-trip-cost-bps` takes a cost *measured* from real fills via
`parallax.crypto.costs.MeasuredCostModel`, per the cost contract in `PROTOCOL.md`. An assumed
cost can stress-test a result; it cannot support one.

## Testing the governing equation directly

`PHYSICS_MODEL.md` proposes `velocity = pressure / resistance`. Written as a scaling law with the
exponents free:

```text
directional mid response  ~  k * |net flow| ** delta  *  resting depth ** -gamma
```

`parallax book impact` fits `delta` and `gamma` from capture. This settles the shape of the
equation before any latent-state estimation exists to obscure it, and it is cheap: the answer
arrives from one day of data.

| Result | Reading |
|---|---|
| `delta ≈ 1`, `gamma ≈ 1` | The naive ratio form survives. Also Kyle's (1985) linear lambda. |
| `delta ≈ 0.5` | The canonical square-root law. The equation needs *latent* liquidity and diffusion, not visible depth and division (Donier, Bonart, Mastromatteo & Bouchaud, 2015). |
| `gamma` interval spans 0 | Resting depth does no work. "Resistance" is not a separately identified force, and pressure over resistance is a reparameterisation rather than a measurement. |
| halves disagree by > 0.25 | Not a single power law. Reported as `not-a-power-law`; do not quote an exponent. |

The prior from the literature is that `delta` comes out near 0.5, so expect the naive form to be
rejected. That is the informative outcome, not a failure: it tells you which version of the fluid
model to build.

Three properties make the estimate defensible. Windows are non-overlapping, which removes the
overlapping-observation problem at the source. Exponents are fit to *bin means* of the directional
response rather than to logs of individual windows, because per-window responses are often zero or
run against the flow, and dropping those biases the curve upward exactly where the effect is
smallest. Resistance is read at the window start, from the side opposing the flow, so it is
predetermined rather than contaminated by the move it is meant to have resisted.

The estimator is validated by planting known exponents in synthetic data and recovering them
(`test_microstructure_impact.py`): it returns 0.50 and 1.00 to two decimals, separates 0.5 from
1.0, widens its interval rather than drifting as noise rises, and reports `delta ≈ 0` on pure noise.

**This measurement is contemporaneous and descriptive.** It characterises how price responds to
flow within the same window. It is not a forecast, it implies no edge, and it must never be quoted
as one. The predictive question is `parallax book sweep`.

## Pressure or revelation: the withdrawal tests

The strongest critique of any mechanical impact law is that price moves because liquidity
providers *update beliefs and withdraw*, not because volume pushes (Glosten & Milgrom, 1985). A
single eager buyer can move price drastically if sellers detect the eagerness and pull their
offers; small net flow with large response is the signature. `parallax book revelation` runs three
measurements of that story:

1. **Trade coincidence** — what share of mid movement happens in samples with no trades at all?
   A large share caps what any `flow^delta` law can ever explain. Caveat: at one-second sampling a
   quote-driven move sharing a second with unrelated trades is counted as trade-coincident, so
   this figure is a *lower bound* on quote-driven movement.
2. **Withdrawal amplification** — at the same flow, do windows where the opposing side was pulling
   depth move further than windows where it held? Both terciles are priced at the pooled median
   flow, so withdrawal is not confounded with volume. The mechanical view predicts no gap.
3. **Detection** — does withdrawal *follow* aggressive flow with a consistent lag, and more than
   the reverse ordering? This is h(), the maker-detection function, and it is the closest of the
   three to a forecast: withdrawal that begins before the move completes is observable in time.

All three are validated on synthetic data with planted and absent effects, and all three are
descriptive measurements of coupling, not signals. Sync procedure note: reconstruction buffers
diffs received while the REST snapshot was in flight and replays them across it, per Binance's
documented procedure — the diffs covering `lastUpdateId + 1` onward routinely precede the snapshot
record in receive order.

## Reading the sweep

```
 horizon_s    n_test    oos_r2  rank_ic  gross_bps   ci_low  ci_high   net_bps  verdict
```

`gross_bps` is the realised forward return in the direction of the signal, over the most confident
decile of out-of-sample predictions. `ci_low` and `ci_high` come from a moving-block bootstrap,
because overlapping forward-return labels are heavily autocorrelated and ordinary standard errors
would be far too narrow.

`verdict` is `survives` only when `ci_low` clears cost. The point estimate clearing cost is not
enough, and a positive `oos_r2` on its own means nothing tradeable.

Expect `dead` at most horizons. That is the normal outcome and it is the cheap one. Read the shape
of the decay curve rather than hunting for the single horizon that looks best: a genuine
microstructure effect decays smoothly from short horizons, while an isolated significant cell
surrounded by noise is what multiple testing produces. Count every hypothesis tested, including the
losers, because that count is what makes the survivors interpretable.
