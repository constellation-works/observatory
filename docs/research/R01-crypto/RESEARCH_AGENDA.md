---
title: "R01 Crypto Research Agenda"
summary: "Program-wide motivation, comparison ladder, and sequence for the registered R01 hypotheses."
tags: [parallax, crypto, research-agenda, hypotheses]
related: ["docs/research/R01-crypto/README.md", "docs/research/R01-crypto/hypothesis/README.md", "docs/research/R01-crypto/PROTOCOL.md"]
created_on: 2026-08-01
updated_on: 2026-08-19
status: active
research_id: R01
domain: crypto
---

# Crypto research agenda

This is the program-wide motivation and sequence for Parallax's first numbered research program,
crypto markets. The [`hypothesis/` registry](hypothesis/README.md) holds the frozen claims and
decision histories. Other domains receive their own numbered directories and share the common
research protocol without inheriting Bitcoin-specific baselines, metrics, or promotion rules.

The agenda records hypotheses before they become experiments and keeps the behavioral story
separate from what the data can actually establish. Nothing here is a claim of edge. Each idea
survives only by beating its stated baseline out of sample after measured costs.

The governing contracts remain:

- [`PROTOCOL.md`](PROTOCOL.md) — evidence, benchmark, cost, and promotion rules;
- [`DATA.md`](DATA.md) — immutable candle data;
- [`MICROSTRUCTURE.md`](MICROSTRUCTURE.md) — level-2 capture and the first horizon sweep;
- [`PHYSICS_MODEL.md`](PHYSICS_MODEL.md) — the active-fluid interpretation of the order book.

## Objective and posture

The objective is to beat Bitcoin buy-and-hold on positive net return and return-to-drawdown over
the same untouched interval. The immediate objective is more modest: build an instrument that can
reliably tell us when we do **not** have an edge.

The main adversary is hindsight. Every experiment must preserve its hypothesis, variables, lags,
horizons, cost assumptions, and rejection criterion before its test interval is examined.

## One system at two timescales

Parallax treats the market as a coupled system with two primary layers:

```text
daily macro weather
    risk appetite · liquidity · equities · rates · dollar · volatility · participant mix
        ↓ conditions
minute/second microstructure mechanics
    aggressive flow · depth · cancellation · persistence · refill · execution cost
        ↓ produces
conditional distribution of future mid-price movement
```

The daily layer is not repeated 1,440 times to manufacture a larger sample. It produces one frozen,
time-stamped regime estimate using only information available at its cutoff. The high-frequency
layer estimates how book mechanics behave inside that regime.

The combined target is:

```text
E[future BTC mid return]
    = g(book state, clock phase | daily macro state, speculative-risk state)
```

## Hypothesis register

| ID | Hypothesis | Baseline | What would reject it |
|---|---|---|---|
| [H01](hypothesis/H01-standard-order-flow-and-queue-imbalance.md) | Standard order-flow and queue imbalance predict short-horizon mid-price movement. | Constant/own-return model | No stable out-of-sample lift, or effect dies before executable cost. |
| [H02](hypothesis/H02-active-fluid-microstructure-features.md) | Pressure, effective resistance, wall persistence, and refill add information beyond standard imbalance. | H01 | No incremental forecast or economic value after cost and multiple-testing control. |
| [H03](hypothesis/H03-clock-phase-conditioning.md) | Clock phase changes the physical response of the book because participant populations rotate. | H02 without clock state | Session-conditioned coefficients do not improve calibration or stability. |
| [H04](hypothesis/H04-daily-macro-state.md) | Daily traditional-market shocks contain lagged information about BTC regime, return, volatility, or liquidity. | BTC-only daily autoregression | No walk-forward lift; apparent direction vanishes after common-shock and timing controls. |
| [H05](hypothesis/H05-equity-high-bitcoin-catch-up.md) | When equities are near highs and BTC is abnormally quiet or weak, continuing risk appetite sometimes produces BTC catch-up. | Momentum and unconditional BTC returns | Underperformance persists, or effect disappears when confirmation and risk-off states are separated. |
| [H06](hypothesis/H06-speculative-influx-weekend-flow.md) | A latent influx of speculative investors changes weekend BTC flow when institutional liquidity recedes. | Weekend/time-of-week seasonality alone | Only relative retail share rises, absolute speculative activity does not, or the state predicts neither direction nor volatility. |
| [H07](hypothesis/H07-multiscale-conditioning.md) | Daily macro and speculative states improve the microstructure model by changing its pressure-response coefficients. | Best H02/H03 model | Mixed-frequency conditioning adds no stable out-of-sample value. |
| [H08](hypothesis/H08-day-trader-night-flattening.md) | US night hours (21:00–00:00 Pacific, with an Eastern copy) have more negative Bitcoin hourly drift because day traders flatten to lock in P&L. | Complementary-hour mean; buy-and-hold | Pacific night mean is not below complementary hours; or an apparent leak is weekend-equal, crash-hour-only, or unexplained by later flow/inventory evidence. |

H01 is prior art and a required control, not the proposed edge. The primary research question begins
at H02.

## H01–H02: order-book physics

### State interpretation

Treat the limit order book as an active, adaptive fluid:

- aggressive market buys and sells are flow;
- signed order-flow imbalance is pressure differential;
- resting depth is absorption capacity;
- additions and cancellations alter the channel geometry;
- refill is replenishment or compressibility;
- autocorrelated recent flow is momentum or memory;
- mid-price movement is boundary displacement after local capacity is exhausted.

Standing orders are resistance, not opposing flow. A sell wall absorbs buying only while it remains
posted. Effective resistance therefore depends on survival and refill, not visible size alone:

```text
effective resistance
    ≈ visible depth × P(order survives until challenged)
      + expected refill before price arrives
```

The first approximation is:

```text
expected price velocity
    ≈ (net aggressive flow + directional book change)
      / effective surviving liquidity
```

Book depth itself evolves:

```text
d(depth)/dt = additions - cancellations - executions + repricing
```

This is not a passive conservation-law system. Traders observe the same state and adapt. The model
must return probabilities and uncertainty, not a deterministic path.

### Incremental claim

The physics model succeeds only if persistence, refill, void, and cancel-versus-fill features add
out-of-sample information beyond ordinary order-flow and queue imbalance at a horizon that survives
measured costs.

Required outputs include:

- expected mid-price displacement by horizon;
- probability and direction of the next boundary movement;
- probability a void refills before price reaches it;
- probability a challenged wall persists, is consumed, or is cancelled;
- coefficient and calibration stability across regimes;
- the full decay curve rather than the best-looking isolated horizon.

### Measurement limits

Information quality is the first bottleneck:

- dropped or out-of-sequence depth updates corrupt the reconstructed book;
- inaccurate clocks can reverse apparent cause and effect;
- level 2 shows net depth change, not gross additions and cancellations;
- hidden orders and reactive makers make visible depth an incomplete state;
- trade prices contain bid-ask bounce, so labels use mid price;
- public predictability is not automatically executable edge.

A useful summary is:

```text
usable edge
    ≈ predictive information
      - measurement and reconstruction error
      - latency decay
      - execution cost
```

## H03: humans, sessions, and clock phase

Crypto trades continuously, but humans and institutions do not. Geographic sessions, market opens,
scheduled announcements, settlement clocks, and periodic algorithms change the population acting on
the book.

Clock phase is a boundary condition rather than a directional force. For each minute of the week,
estimate normal:

- aggressive buy/sell pressure;
- depth, spread, and volatility;
- wall survival, cancellation, and refill;
- trade-size distribution and venue mix;
- cost and pressure-to-price response.

The potentially useful feature is a session-normalized deviation:

```text
normalized pressure
    = (observed pressure - expected pressure for this clock phase)
      / clock-phase variability
```

Use timezone-aware sessions such as `America/New_York`, not fixed “EST” buckets. Daylight saving
time changes New York relative to UTC. Weekdays, weekends, regional overlaps, exchange settlements,
and scheduled macro releases remain separate states until evidence supports combining them.

The likely value is improved calibration and regime recognition, not a rule such as “buy every
Tuesday at 15:00.”

H08 is a different clock claim: a signed night-session drift from day-trader flattening, not a
session-normalized pressure response. Exploratory [E01](experiments/E01-bitstamp-us-night-hourly-drift.md)
revised the frozen Pacific 21:00–00:00 window. A restated Eastern-evening clock, if pursued, is a
new hypothesis and needs a preregistered test on unseen data.

## H04: daily macro weather

### The model

Traditional markets may change Bitcoin's daily regime through global liquidity, risk appetite,
rates, the dollar, and common shocks. Start with a small preregistered distributed-lag or VAR model:

```text
BTC return[d + h]
    = regime intercept
      + Σ asset Σ lag response[asset, lag] × asset shock[d - lag]
      + Σ lag own_response[lag] × BTC return[d - lag]
      + error[d]
```

Candidate daily inputs, added only through preregistered experiments:

- S&P 500 and Nasdaq returns, preferably futures when timing spans cash-market closure;
- changes in Treasury yields or Treasury-futures returns;
- VIX and MOVE changes;
- dollar-index returns;
- gold and broad commodity returns;
- spot Bitcoin ETF creations, redemptions, or net flows when available at the cutoff;
- crypto-native funding, basis, open interest, stablecoin supply/flow, and venue volume.

Model returns and yield changes, never unrelated raw price levels. Include BTC's own lags so its
existing momentum is not attributed to another asset.

### What a regression establishes

Keep four levels of inference distinct:

1. contemporaneous correlation — assets move together;
2. lagged predictiveness or VAR connectedness — one series improves forecasts of another;
3. structural causality — an independently identified shock caused a response;
4. actual capital flow — money moved between asset classes.

Ordinary lagged regression and reduced-form VAR reach level 2. They do not prove levels 3 or 4.
Common news, omitted variables, asynchronous closes, and correlated innovations can create apparent
direction. Actual flow requires transaction, position, subscription/redemption, or account-level
evidence.

The IMF spillover paper is a connectedness baseline, not a flow study. It uses a reduced-form VAR
and generalized forecast-error variance decomposition on daily returns and volatilities. Its
“directional spillover” measures attributed forecast variance, not identified causal transmission.

### Timing and sample integrity

- Every feature carries the timestamp at which it became observable.
- A US close can predict only subsequent BTC observations.
- Closed cash markets are not forward-filled into fake flat observations; use futures or mark stale.
- Daily observations remain the unit of macro inference even when their state conditions minute data.
- Coefficients are estimated walk-forward and allowed to change across structural regimes.
- Lag counts stay small or regularized; searching many assets × lags × horizons is multiple testing.

The daily layer should predict volatility, liquidity, and coupling regime as well as direction. It
may be more useful as “macro weather” than as a directional trading rule.

## H05: equity abundance and BTC catch-up

### Behavioral story

After equities rise, some investors realize profits or rebalance toward an asset they perceive as
having more upside. When SPY is near an all-time high and Bitcoin has been quiet, Bitcoin may become
a catch-up candidate.

That story is plausible but not required for the predictor to work, and it must not be confused with
proof of capital transfer. “Quiet” or “lagging” does not mean undervalued. Relative weakness may
continue through momentum rather than reverse.

### Competing predictions

- **Catch-up:** continuing risk appetite plus abnormal BTC weakness leads to positive BTC residual
  returns.
- **Relative momentum:** capital continues preferring equities and BTC remains weak.
- **Risk-off failure:** equities roll over, broad deleveraging begins, and BTC behaves as a higher-beta
  risk asset rather than a refuge.

### Candidate state

- SPY within a preregistered distance of its trailing high and still advancing;
- BTC realized volatility and range compressed relative to its own history;
- BTC return below the value predicted by its rolling macro relationship;
- confirmation from BTC volume, ETF flow, relative momentum, or aggressive order flow;
- explicit failure gate when equities roll over, volatility rises, or liquidity deteriorates.

Test 1-, 5-, 10-, and 20-day BTC returns separately in three states: equities advancing near highs,
near highs but rolling over, and already in drawdown. Compare against both unconditional BTC returns
and a continuation/momentum model.

The current prior is asymmetric: any catch-up is more plausible during continuing risk-on conditions
and may disappear or reverse when equities falter.

## H06: influx of speculative investors and the weekend

### Latent variable

The desired variable is not generic “fear or greed.” It is the absolute influx of investors willing
to take short-horizon, convex, high-variance risk.

Small-lot, short-dated option activity may help estimate it. Candidate components include:

- absolute premium in small-lot buy-to-open calls and puts;
- call-versus-put and out-of-the-money concentration;
- 0DTE and very-short-dated concentration;
- retail-broker flow estimates where their construction is auditable;
- absolute count and notional of small crypto trades;
- retail-oriented venue and pair activity;
- speculative altcoin volume as a secondary, explicitly noisy proxy.

Aggregate low option volume is not influx. Trade size, initiation, opening/closing status, premium,
and direction matter. A small contract count can still represent meaningful premium, while high
contract count can be mechanically cheap lottery exposure.

### Share is not influx

```text
retail share = retail activity / total activity
```

Retail share can rise on weekends because institutional activity falls even when absolute retail
activity also falls. Thin liquidity can amplify price response without any new money entering.
Measure both the numerator and denominator.

### Weekend experiment

US equity options are closed on weekends. Freeze a Friday speculative-risk score at a precise
information cutoff, then test whether it changes the distribution of weekend BTC:

- net return and aggressive order-flow direction;
- realized volatility and jumps;
- spread, depth, refill, and wall survival;
- absolute small-trade activity and its share of all activity.

The primary interaction is:

```text
weekend response
    = Friday speculative-risk state
      × weekend institutional-liquidity reduction
```

The prior is that speculative appetite may predict weekend volatility more reliably than direction.
“Weekend means retail buying” is not an acceptable hypothesis.

## H07: integrated multiscale model

The final model is conditional rather than universal:

```text
expected price response
    = f(
        local pressure,
        effective resistance,
        persistence,
        refill,
        clock phase,
        daily macro state,
        speculative-risk state
      )
```

Integration happens only after each layer earns its place independently. A complex model cannot be
used to hide a failed component. The comparison ladder is:

1. constant and BTC-own-history baselines;
2. standard order-flow and queue imbalance;
3. active-fluid microstructure features;
4. clock-phase conditioning;
5. daily macro conditioning;
6. speculative-risk/weekend interaction;
7. the combined model.

At each step, retain the simpler model unless the new layer improves untouched performance,
calibration, and economic value after cost.

## Data inventory and gaps

### Already represented in Parallax

- Binance and Coinbase one-minute spot candles;
- Binance level-2 diffs, aggregate trades, best quotes, and snapshots;
- immutable raw storage and explicit gap handling;
- measured execution-cost components and preregistration journal;
- order-flow, queue, void, refill, cancel/fill residual, and horizon-decay machinery.

### Needed for later hypotheses

- carefully timed daily equity, futures, rates, dollar, volatility, and commodity series;
- spot Bitcoin ETF flow with publication timestamps;
- options trades rich enough to infer size, direction, opening status, expiry, strike, and premium;
- direct or defensible retail-flow estimates rather than aggregate options volume;
- cross-venue crypto trade-size distributions and liquidity states;
- scheduled-event calendar with actual release timestamps;
- our own paper/shadow fills for measured costs.

Public availability is not enough. Every source needs a provenance record, availability timestamp,
revision policy, gap audit, and license or use constraint before it enters an experiment.

## Experiment sequence

1. **Instrument validation:** prove the book reconstructs exactly across normal operation, reconnects,
   gaps, duplicate messages, and clock boundaries.
2. **Baseline sweep:** estimate standard order-flow and queue-imbalance decay over mid-price horizons.
3. **Physics increment:** add persistence, refill, void, and cancel/fill residuals one family at a time.
4. **Clock conditioning:** estimate minute-of-week baselines and session-specific response functions.
5. **Daily macro baseline:** run a small preregistered daily distributed-lag/VAR experiment.
6. **Catch-up test:** compare reversal and momentum explanations for SPY-high/BTC-quiet states.
7. **Speculative influx:** construct the options/crypto risk-appetite score and test the weekend
   interaction.
8. **Multiscale integration:** condition the surviving microstructure model on surviving daily states.
9. **Replay and paper:** only after conditional forecasts clear measured cost with stable uncertainty.

Negative results remain permanent evidence. Do not silently redefine “quiet,” change a lag, move a
session boundary, or drop a failed regime after seeing the outcome; preregister a new version.

## Research anchors

- Cont, Kukanov, and Stoikov, *The Price Impact of Order Book Events* — standard order-flow
  imbalance baseline: <https://arxiv.org/abs/1011.6402>
- Gould and Bonart, *Queue Imbalance as a One-Tick-Ahead Price Predictor in a Limit Order Book*:
  <https://arxiv.org/abs/1512.03492>
- Iyer and Popescu, *New Evidence on Spillovers Between Crypto Assets and Financial Markets* — a
  reduced-form connectedness reference, not evidence of actual flow:
  <https://www.imf.org/-/media/Files/Publications/WP/2023/English/wpiea2023213-print-pdf.ashx>
- Eross et al., *Time-of-day periodicities of trading volume and volatility in Bitcoin exchange*:
  <https://www.sciencedirect.com/science/article/abs/pii/S1544612319301904>
- Moskowitz, Ooi, and Pedersen, *Time Series Momentum* — the continuation alternative to naive
  catch-up: <https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf>
- Bryzgalova, Pavlova, and Sikorskaya, *An Anatomy of Retail Option Trading*:
  <https://experts.illinois.edu/en/publications/an-anatomy-of-retail-option-trading/>
- Jain et al., *Insights from Bitcoin Trading* — weekday/weekend activity and retail participation:
  <https://digitalcommons.memphis.edu/facpubs/11597/>

These references motivate controls and measurements. They do not establish a current tradeable edge;
their data periods, market structure, and endpoint assumptions must be rechecked when an experiment
is designed.
