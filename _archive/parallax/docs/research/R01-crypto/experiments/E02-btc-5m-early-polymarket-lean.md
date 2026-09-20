---
title: "E02 BTC 5-Minute Early Polymarket Lean"
summary: "Preregistered test of H09: whether Polymarket BTC 5-minute Up/Down books already lean toward the eventual winner at 5s, 15s, and 30s."
tags: [parallax, crypto, polymarket, 5-minute, informed-flow]
related: ["docs/research/R01-crypto/hypothesis/H09-whale-weak-window-early-polymarket-lean.md", "docs/research/R01-crypto/PROTOCOL.md", "docs/RESEARCH_PROTOCOL.md", "docs/research/R01-crypto/DATA.md", "notebooks/R01-crypto/E02-btc-5m-early-polymarket-lean.py"]
created_on: 2026-08-20
updated_on: 2026-08-20
status: completed
research_id: R01
domain: crypto
experiment_id: E02
hypothesis_id: H09
preregistered: true
outcome: revised
---

# E02: BTC 5-minute early Polymarket lean

## Study status

Preregistered against H09. Schema, file list, and coverage of local Kaggle v1 were inspected when
H09 was frozen; outcome-conditional leans were not computed until this notebook ran. Cuts (τ, signed
mid, 0.5 baseline, extreme-open threshold, PT night hours, depth terciles) were not changed after
seeing results. This record can never `advance` the whale mechanism: the tape has no Bitcoin path,
so a mechanical copy of an already-moved coin is untested. The directional observable is still
reportable.

## Question

In resolved Polymarket BTC 5-minute Up/Down markets, is the Up-token mid at 5s, 15s, and 30s after
`market_start` already on the eventual winner's side, beating an uninformed 0.5? The decision is
whether H09's early-lean prediction is real enough to justify a Bitcoin-joined follow-up, not
whether a whale moved spot.

## Methodology

### Design

- **Experimental or observational unit:** one resolved BTC 5-minute Up/Down market.
- **Population and sampling frame:** local Kaggle
  `kachoio/polymarket-5-minute-crypto-updown-markets` version 1, BTC files only
  (`btc_markets.parquet`, `btc_ticks.parquet`).
- **Treatment, signal, or intervention:** Up-token implied probability
  `mid_up = (bu + au) / 2` at frozen elapsed times τ ∈ {5, 15, 30} seconds. The quote used at τ is
  the last tick with `ts_utc ≤ market_start + τ`.
- **Response and horizon:** inferred market `outcome` (`Up` / `Down`). Primary response is the
  outcome-signed mid `s · (mid_up − 0.5)` with `s = +1` if Up else `−1`. Directional agreement is
  `sign(mid_up − 0.5)` versus that outcome; mids at exactly 0.5 are ties and leave the agreement
  denominator.
- **Known confounders and controls:** already-extreme opening mids (`|mid_up − 0.5| > 0.15` at
  τ = 0); PT 21:00–00:00 versus other hours; ET weekend versus weekday; lowest versus highest
  tercile of contemporaneous Polymarket bid depth `du + dd`; markets with `n_ticks < 300`. No
  Bitcoin return control is possible on this tape.

### Data contract

- **Sources and provenance:** Kaggle handle `kachoio/polymarket-5-minute-crypto-updown-markets`,
  local version **1**, retrieved 2026-08-20T06:36:02.571307+00:00. License **CC0-1.0**. Uploader
  source note: public Polymarket CLOB WebSocket plus Gamma API; independent recording, not
  affiliated with Polymarket. Construct: per-second top of book for 5-minute crypto Up/Down
  markets. `outcome` is inferred from the final tick (winning bid near 0.99), not from chain.
  No Bitcoin price column.
- **Immutable dataset or snapshot identifier:**
  - resolved path:
    `/Users/daniel/data/kaggle/datasets/kachoio/polymarket-5-minute-crypto-updown-markets/versions/1`
  - `btc_markets.parquet` (3,921,352 bytes), SHA-256
    `8e0ed78021bd98d3dba18829266103ebd9b46a77f6ba872a1c7f98be77b506bd`
  - `btc_ticks.parquet` (182,475,803 bytes), SHA-256
    `173760b951ac0a2c795e1c3873a506e2fd4372db356dd3515f06582820ff975e`
  - Files were read in place from that versioned path. They were not copied into
    `data/R01-crypto/raw/`.
- **Observation window:** market starts 2026-03-24 22:10 UTC through 2026-05-18 10:30 UTC
  (last tick 2026-05-18 10:34:59 UTC). Offsets in this window: PT UTC−7, ET UTC−4.
- **Information cutoff:** quotes at or before `market_start + τ` for the signal; the market-level
  `outcome` is the label only. End-of-window ticks are used solely as a label-quality check
  (`QC_LAST_TICK`), not as a feature.
- **Exclusions and missing-data policy:** drop markets with null `outcome` (1,456 of 15,682) or
  with no formable Up mid (`bu`/`au` missing) at that τ. 15,682 tick-covered markets; 14,226 with
  a non-null inferred outcome. Three markets have `n_ticks < 300`. No tick elapsed outside
  `[0, 300]`.

Rejected for this question: `hugobde/polymarket-bitcoin-15min-up-or-down` (15-minute, 1-minute
fidelity, no depth); other coins in the same Kaggle set (not BTC); local Bitstamp 1-minute
(too coarse to control intra-window BTC path). `angelhanna/polymarket-btc-snapshots-2026` was
unregistered and deleted as too heavy.

Validity risks: inferred labels; collector outages on 15–18 Apr 2026; volume/liquidity are
discovery-time Gamma snapshots; bid-side depth only; two independent Up/Down books so
`bu + bd ≠ 1`; 1 Hz cache sampling.

Owning research program: `R01-crypto`. Work is a durable experiment citation of an external
versioned tape, not an R01 raw import.

### Evaluation contract

- **Train, validation, and untouched test split:** none. The full BTC v1 window is the evaluation
  sample. A later confirmatory test needs a later collector window or another venue.
- **Baseline:** uninformed 0.5 at the same τ: mean outcome-signed mid 0, agreement 50% among
  non-ties.
- **Primary metric:** mean outcome-signed mid at each of τ = 5, 15, 30 seconds, one-sided greater
  than 0; and directional agreement, one-sided greater than 50%.
- **Secondary metrics:** the same after dropping extreme opens; night minus rest (PT 21–23);
  weekend minus weekday (ET); lowest minus highest Polymarket bid-depth tercile; `n_ticks ≥ 300`.
- **Uncertainty method:** one-sample (or two-sample Welch) t with a normal tail, plus 8,000-draw
  bootstrap percentile 95% CI on the in-slice mean (seed 7).
- **Robustness checks:** last-tick agreement as a label audit; short-market count; extreme-open
  drop.
- **Parameter search and trial count:** none. No extra τ values were scanned.
- **Costs or resource budget:** none. This is not an executable strategy.
- **Rejection criterion:** reject H09's directional claim if every primary τ has mean signed mid
  ≤ 0 and agreement ≤ 50%. Weaken the whale/weak-window mechanism if the lean vanishes after the
  extreme-open drop, is no stronger at night/weekend or thin PM depth, or (in a later study) is
  absorbed by contemporaneous Bitcoin returns.

### Protocol deviations

None. The last-tick quality check was named in H09 as a leakage risk to avoid as a feature; it is
reported only as `QC_LAST_TICK`.

## Reproducibility

- **Code revision:** `notebooks/R01-crypto/E02-btc-5m-early-polymarket-lean.py` (source of truth)
  and `notebooks/R01-crypto/E02-btc-5m-early-polymarket-lean.ipynb` (executes the script).
- **Environment or lockfile:** `uv.lock` plus `--group notebook`.
- **Random seeds:** bootstrap seed 7.
- **Command or notebook:**
  `uv run --group notebook python notebooks/R01-crypto/E02-btc-5m-early-polymarket-lean.py`
  Results below are labeled `PRIMARY` / `SECONDARY` / `QC_LAST_TICK` prints from that script.
- **Artifacts:** none under `data/R01-crypto/processed/`.

## Results

Coverage: 15,682 BTC markets, 4,704,518 ticks. Inferred outcomes 7,177 Up / 7,049 Down / 1,456
null. Last-tick label audit (`QC_LAST_TICK`, n = 14,226): agreement **1.000**, mean signed mid
**0.4928** — the inferred winner matches the final book on every labeled market.

**Primary, all labeled BTC 5-minute markets**

| τ | n | Mean signed mid | Bootstrap 95% CI | Agreement | Agree 95% CI | p(signed > 0) |
|---|---:|---:|---|---:|---|---:|
| 5s | 14,224 | 0.0126 | [0.0114, 0.0137] | 56.93% | [56.11%, 57.73%] | ~0 |
| 15s | 14,225 | 0.0265 | [0.0248, 0.0282] | 59.93% | [59.12%, 60.72%] | ~0 |
| 30s | 14,225 | 0.0431 | [0.0409, 0.0452] | 62.49% | [61.68%, 63.28%] | ~0 |

Unsigned mean `mid_up` stays near 0.50 (0.502–0.503). The book is not one-sided; it is already
tilted toward whichever side later wins. The lean grows with elapsed time, as a mechanical copy of
an unfolding Bitcoin path would also do.

**Secondary**

- Drop `|open mid − 0.5| > 0.15` (286 markets): τ = 5s mean signed mid **0.0115**, agreement
  **56.64%**. The primary is not only windows that opened already decided.
- PT 21:00–23:00 versus rest: night mean is larger at every τ (diff +0.0053 / +0.0096 / +0.0070;
  one-sided p ≈ 0.0019 / 0.00014 / 0.018). Compatible with a weaker night clock; also compatible
  with any night-correlated Bitcoin move.
- ET weekend versus weekday: larger at τ = 5s (diff +0.0028, p ≈ 0.019); not distinguishable at
  15s (p ≈ 0.077) or 30s (p ≈ 0.14).
- Lowest versus highest Polymarket bid-depth tercile: mixed. Stronger in the thin tercile at
  15s (diff +0.0067, p ≈ 0.00095); not at 5s (p ≈ 0.16); **wrong sign** at 30s (diff −0.0008,
  p ≈ 0.61). Thin *Polymarket* depth is not a stable "weak moment" proxy.
- `n_ticks ≥ 300`: identical to primary (1–2 short markets).

No Bitcoin prints were joined. The mechanical-copy alternative is therefore untested.

## Outcome

- **Decision:** `revise`
- **Rationale:** H09's directional prediction holds at every frozen τ: early Up mids already point
  toward the inferred winner and beat 0.5 by a wide margin. That is not enough to promote the whale
  story. Night clocks show a larger lean; Polymarket depth does not do so consistently; the tape
  cannot tell PM-leads-spot from spot-leads-PM. Restate the supported observable without whale
  identity, and test residual lead after a second-level (or better) BTC path.
- **Limitations:** one collector, ~7.5 weeks, inferred labels, 9.3% null outcomes, no holdout,
  no BTC control, PM depth is not BTC depth, 5-minute horizon only.
- **Next step:** freeze a new `HNN` on early 5-minute PM informativeness (no whale claim),
  preregister an `ENN` that joins an aligned BTC tape and asks whether `signed_mid` at τ still
  predicts the outcome after the contemporaneous coin return over `[0, τ]`. Do not promote H09
  from E02.
