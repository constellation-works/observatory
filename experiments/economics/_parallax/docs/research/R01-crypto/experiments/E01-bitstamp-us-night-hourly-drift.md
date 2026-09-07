---
title: "E01 Bitstamp US Night Hourly Drift"
summary: "Exploratory test of H08: whether Bitstamp BTCUSD hourly returns are more negative in US night windows than in complementary hours."
tags: [parallax, crypto, bitcoin, hourly-returns, night-session]
related: ["docs/research/R01-crypto/hypothesis/H08-day-trader-night-flattening.md", "docs/research/R01-crypto/PROTOCOL.md", "docs/RESEARCH_PROTOCOL.md", "docs/research/R01-crypto/DATA.md", "notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.py"]
created_on: 2026-08-19
updated_on: 2026-08-19
status: completed
research_id: R01
domain: crypto
experiment_id: E01
hypothesis_id: H08
preregistered: false
outcome: revised
---

# E01: Bitstamp US night hourly drift

## Study status

Exploratory. Hourly Bitcoin returns on the local Kaggle Bitstamp tape were inspected on 2026-08-19
before this record was written. Windows, weekday splits, and the worst three-hour blocks were
chosen after seeing hour-of-day tables. This record cannot `advance` H08. A confirmatory test
requires a new preregistered experiment on data this study has not seen (after 2026-08-08 00:44 UTC
on this snapshot, or an independent venue).

## Question

On Bitstamp BTCUSD hourly close-to-close returns from 2026-04-01 through 2026-08-08, is the mean
return in 21:00–00:00 `America/Los_Angeles` more negative than in complementary hours? Does the
same three-hour window in `America/New_York` show the same signed gap? The decision is whether
H08's directional night claim is worth restating on a different clock, not whether to trade it.

## Methodology

### Design

- **Experimental or observational unit:** one UTC hourly bar aggregated from 1-minute OHLC
  (first open, max high, min low, last close, summed volume).
- **Population and sampling frame:** Bitstamp BTCUSD 1-minute bars in local Kaggle dataset
  `mczielinski/bitcoin-historical-data` version 685. Recent few months: 2026-04-01 00:00 UTC
  through 2026-08-08 00:44 UTC.
- **Treatment, signal, or intervention:** clock membership. Primary night = bar-open hour in
  {21, 22, 23} `America/Los_Angeles`. Secondary night = the same hours in `America/New_York`.
  Complementary hours are all other hours in the sample.
- **Response and horizon:** simple return \(R_t = C_t / C_{t-1} - 1\) at a one-hour horizon.
- **Known confounders and controls:** 24/7 buy-and-hold drift over the same timestamps; weekday
  versus weekend; US cash close (16:00 Eastern); one-hour crash outliers; missing minutes.

### Data contract

- **Sources and provenance:** Kaggle handle `mczielinski/bitcoin-historical-data`, local version
  **685**, retrieved 2026-08-08T04:23:40.014185+00:00. Uploader source note:
  `https://www.bitstamp.net/api/`. License **CC-BY-SA-4.0**. Schema status succeeded: columns
  `Timestamp` (unix seconds, BIGINT), `Open/High/Low/Close/Volume` (DOUBLE). Construct: Bitstamp
  BTC/USD 1-minute trade bars, not a global volume-weighted index.
- **Immutable dataset or snapshot identifier:**
  - resolved path:
    `/Users/daniel/data/kaggle/datasets/mczielinski/bitcoin-historical-data/versions/685`
  - file: `btcusd_1-min_data.csv` (388981746 bytes)
  - SHA-256: `7cc5764ca4307d0ed90400f0c1331fa1154c04f8a40187796e8ef6625a6dfece`
  - The file was read in place from that versioned path. It was not copied into
    `data/R01-crypto/raw/`.
- **Observation window:** 2026-04-01 00:00 UTC through 2026-08-08 00:44 UTC. The first hourly
  return uses the 2026-03-31 23:00 UTC close ($68,215).
- **Information cutoff:** 2026-08-08 00:44 UTC on this snapshot. The last hourly bar
  (2026-08-08 00:00 UTC) is incomplete (45 of 60 minutes) and was retained.
- **Exclusions and missing-data policy:** no rows dropped for zero volume. In this window there
  were 0 missing minutes, 0 missing hours, 0 nulls, 0 high < low, and 0 non-positive closes
  (185,805 1-minute rows; 1,241 zero-volume minutes). 3,097 hourly bars; 3,096 returns.

Rejected for this question: `jacksoncrow/stock-market-dataset` and other local equity tapes (not
Bitcoin). No second crypto venue was in the local Kaggle catalog.

Validity risks: uploader mirror of Bitstamp; venue basis versus Binance/Coinbase R01 candles;
snapshot is stale relative to wall time after 2026-08-08; inferred CSV types are sampling hints.

Owning research program: `R01-crypto`. Work is exploratory, not a durable import.

### Evaluation contract

- **Train, validation, and untouched test split:** none. The entire recent-month window was used
  after inspection. No holdout remains on this snapshot.
- **Baseline:** mean hourly simple return in complementary hours, and buy-and-hold close-to-close
  over the same first and last hourly closes.
- **Primary metric:** difference in mean hourly simple return, Pacific night minus complementary
  hours, in basis points. One-sided question: night mean < complementary mean.
- **Secondary metrics:** Eastern night versus complementary hours; night-only compound return;
  buy-and-hold compound; share of negative hours; weekday versus weekend night means; US cash-close
  hour mean; bootstrap 95% CI on the night mean.
- **Uncertainty method:** Welch two-sample t (normal p, one-sided less) and 8,000-draw bootstrap
  percentile CI on the in-window mean (seed 7). Fat tails make the t approximation optimistic.
- **Robustness checks:** DST via `America/Los_Angeles` and `America/New_York` (offsets in this
  window were UTC−7 and UTC−4, so PDT/EDT); weekday/weekend split; location of hours with
  \(R_t < -2\%\); ranking of all 24 three-hour local blocks (exploratory, post-selection).
- **Parameter search and trial count:** not pre-specified. Hour-of-day tables and three-hour
  blocks were examined after the primary window. Treat those rankings as discovery.
- **Costs or resource budget:** none. This is a descriptive drift test, not an executable
  strategy. No fees, spread, or slippage are applied; a later trading test would need them.
- **Rejection criterion:** reject H08's directional claim if the Pacific night mean is not below
  the complementary-hour mean. The mechanism is not tested without trader-identity or inventory
  data; weekday concentration can only weaken or fail to weaken it.

### Protocol deviations

The method was written after the data were viewed. Night windows were the motivating cut, but
worst-block discovery, weekday splits, and cash-close comparisons were added after seeing
hour-of-day tables. Those checks stay exploratory.

## Reproducibility

- **Code revision:** `notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.py` (source of
  truth) and `notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.ipynb` (executes the script).
- **Environment or lockfile:** `uv.lock` plus `--group notebook` (`pandas 3.0.5`, `numpy 2.5.1`).
- **Random seeds:** bootstrap seed 7.
- **Command or notebook:**
  `uv run --group notebook python notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.py`
  Results below are labeled `PRIMARY` / `SECONDARY` prints from that script.
- **Artifacts:** none under `data/R01-crypto/processed/`. The notebook plot is stored in the
  `.ipynb` outputs.

## Results

Buy-and-hold over the window: $68,252.00 (2026-04-01 00:00 UTC) to $64,872.52 (2026-08-08 00:00
UTC) = **−4.95%**. Month-end closes: Apr $76,310 (+11.87% from 31 Mar 23:00), May $73,568
(−3.59%), Jun $58,526 (−20.45%), Jul $62,818 (+7.33%), Aug 8 $64,873 (+3.27% partial). Unconditional
hourly mean **−0.08 bps**, std 41.7 bps (~39% annualized 24/7), excess kurtosis 10.8.

**Primary (Pacific 21:00–00:00), n = 387 vs 2,709 complementary**

| Metric | Night | Complementary |
|---|---:|---:|
| Mean | −0.12 bps | −0.07 bps |
| Difference | −0.04 bps | — |
| Bootstrap 95% CI on night mean | [−3.38, +3.12] bps | — |
| Welch t (one-sided less) | −0.02, p ≈ 0.49 | — |
| Compound of night hours only | −0.66% | — |
| Share negative | 48.6% | 50.7% |
| Weekday night mean (n = 279) | +0.10 bps | — |
| Weekend night mean (n = 108) | −0.68 bps | — |

The primary window is not more negative than the rest of the day. Weekday Pacific nights are
slightly *positive*, which is the wrong sign for US day-trader flattening on that clock.

**Secondary (Eastern 21:00–00:00), n = 387**

| Metric | Night | Complementary |
|---|---:|---:|
| Mean | −2.28 bps | +0.24 bps |
| Difference | −2.52 bps | — |
| Bootstrap 95% CI on night mean | [−6.73, +2.07] bps | — |
| Welch t (one-sided less) | −1.06, p ≈ 0.14 | — |
| Compound of night hours only | −8.79% | — |
| Share negative | 53.8% | 50.0% |
| Weekday night mean (n = 279) | −2.78 bps | — |
| Weekend night mean (n = 108) | −1.00 bps | — |

Holding only Eastern 21:00–00:00 lost 8.79%. Skipping those hours turned the window from −4.95%
to **+4.21%**. The signed gap is economically visible and stronger on weekdays, but the CI includes
zero and the pre-specified Pacific primary fails.

Hourly Eastern means inside the window: 21:00 **−6.07 bps** (compound −7.67%), 22:00 **−3.70 bps**
(−4.75%), 23:00 **+2.92 bps** (+3.72%). The leak is 21:00–23:00 Eastern, not through midnight.

**Mechanism-adjacent checks (not identified tests)**

- US cash close, 16:00 Eastern: **+6.69 bps** overall, **+6.64 bps** on weekdays. Flattening at the
  equity close is the wrong sign on this tape.
- Hours with \(R_t < -2\%\) (6 bars): three at 06:00 PT / 09:00 ET (including 2026-06-25 13:00 UTC,
  −4.78%), none in Pacific 21:00–00:00, one at 22:00 PT / 01:00 ET. The June crash is a cash-open
  hour, not a night hour.
- Worst three-hour block after ranking all 24 (discovery, not confirmatory): **17:00–20:00 PT /
  20:00–23:00 ET**, mean **−3.25 bps**, compound **−12.11%**. Weekdays **−4.83 bps** versus
  weekends **+0.84 bps**. That block is one hour earlier than H08's Eastern copy.
- Worst single hour: **06:00 PT / 09:00 ET** (US cash open), **−11.11 bps**, compound **−13.65%**
  if that hour is held every day.

No trader-identity, closing-order, or inventory series were available. Day-trader flattening is
not established. The weekday concentration on the Eastern evening block is compatible with
US-hours participants and is also compatible with other weekday-only clocks (opens, news, options).

## Outcome

- **Decision:** `revise`
- **Rationale:** H08's primary Pacific 21:00–00:00 window does not have heavier downward drift than
  complementary hours. The Eastern copy is directionally consistent with a US-evening leak and is
  stronger on weekdays, but it was not the frozen primary, is not significant at conventional
  levels, and does not identify day traders. US cash-close flattening is contradicted. The claim
  should be restated on an Eastern evening clock, or dropped, in a new hypothesis.
- **Limitations:** one venue, one ~4-month snapshot ending 2026-08-08, no holdout, fat tails, last
  hour incomplete, method written after seeing the tape, three-hour block ranking is post-selected,
  no cost model, no second venue.
- **Next step:** if restated, freeze a new `HNN` on a DST-aware `America/New_York` evening window
  (candidate discovery block 20:00–23:00, or the original 21:00–00:00 Eastern copy) with weekday
  interaction and a crash-hour robustness gate. Preregister a new `ENN` on unseen data: later
  Bitstamp hours, or R01 Binance/Coinbase candles after this cutoff. Do not promote from E01.
