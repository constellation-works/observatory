---
title: "Parallax"
summary: "A local platform for falsifiable, reproducible research across numbered domains."
tags: [parallax, research, data-science]
related: ["CLAUDE.md", "docs/ARCHITECTURE.md", "docs/research/README.md"]
created_on: 2026-07-31
updated_on: 2026-08-03
status: active
---

# parallax

Parallax is a local platform for falsifiable, reproducible empirical research across numbered
domains. It supplies the common discipline: freeze the question, preserve point-in-time data,
compare against a credible baseline, evaluate honestly, record negative results, and separate
evidence from action.

Crypto is the first and currently most developed research domain. Its foundation includes public
Binance/Coinbase one-minute candles in immutable Parquet partitions, an append-only trade journal,
a fill-derived cost model, and an explicit risk-adjusted Bitcoin benchmark gate. These remain a
crypto specialization rather than assumptions every Parallax domain must inherit.

## Principles

- One numbered research program owns one explicit domain, evidence contract, agenda, and safety
  boundary.
- Every experiment declares its question, hypothesis, baseline, method, primary metric,
  information cutoff, and rejection criterion before final evaluation.
- Hypotheses live in `HNN-title.md` records; experiments live in `ENN-title.md` records that append
  methodology, results, and outcome without rewriting the frozen plan.
- Choose evaluation splits that match the observation process; time series and grouped data do not
  receive arbitrary row-level splits.
- Keep raw data immutable and every reported experiment reproducible.
- Preserve failed hypotheses and negative results rather than rewriting the original claim.
- Keep labs exploratory. Claimed results depend only on reviewed, tested code under `src/`.
- Live actions are disabled by default and require an explicit human decision and domain-specific
  safety review.

## Quickstart

```sh
uv sync --group dev
uv run pytest
uv run parallax doctor
```

For notebook work, install the optional local tooling once and launch from the numbered notebook
root:

```sh
uv sync --group notebook
make notebook
```

The target registers `Python (parallax)` inside `.venv` and launches Jupyter Notebook with
`notebooks/` as its root. It does not install a user-global kernel.

Dependencies stay minimal and are added only when a concrete research requirement justifies them:
`pyarrow` for Parquet, `numpy` for the regression sweep, and `websockets` in the optional
`capture` group, needed only by the live recorder.

## Consumer-attention pilot

Import one frozen five-year wearable-health history:

```sh
make consumer-goods-import
```

Before running it, export `smart ring`, `smartwatch`, and `fitness tracker` together from the
official Google Trends UI and save the CSV as
`data/R03-consumer-goods/inbox/google-trends/wearable-health.csv`. The importer validates the frozen
query basket and stores an immutable, checksummed dataset under
`data/R03-consumer-goods/raw/history/YYYY-MM-DD/`. Search interest is the phase-one attention proxy;
it is not labeled as purchases or causal demand. The other families remain gated until this pilot
shows a robust held-out signal. See the
[`R03 tracking universe`](docs/research/R03-consumer-goods/docs/TRACKING_UNIVERSE.md) and
[`data contract`](docs/research/R03-consumer-goods/docs/DATA.md).

## Domain-neutral workflow

Freeze a study before opening its final evaluation data:

```sh
uv run parallax research preregister \
  --domain R02-language-models \
  --question "Does BPE improve compression over a byte tokenizer?" \
  --hypothesis "BPE lowers validation bytes per token at fixed vocabulary size." \
  --baseline "byte tokenizer" \
  --method "same corpus split and vocabulary budget" \
  --metric "validation bytes per token" \
  --invalidation "the interval includes zero improvement" \
  --data-cutoff "corpus-v1 before opening the held-out split"
```

The outcome is appended later with `parallax research close`; the original record cannot be
updated or deleted through normal SQLite writes. Without `--db`, the journal is stored at
`data/<research-slug>/research.sqlite3`; pass the same `--domain` to `close` and `show` so they open
the owning partition.

## Crypto workflows

Backfill complete UTC days from either public endpoint; no API key is used:

```sh
uv run parallax data fetch \
  --venue binance --symbol BTCUSDT \
  --start 2023-01-01 --end 2026-07-31

uv run parallax data fetch \
  --venue coinbase --symbol BTC-USD \
  --start 2023-01-01 --end 2026-07-31
```

Freeze a thesis before acting:

```sh
uv run parallax journal preregister \
  --hypothesis "..." --entry-rule "..." --exit-rule "..." \
  --invalidation "..." --size "0.001 BTC" --expected-edge-bps 25
```

Capture the order book, reconstruct it, and measure how fast any predictability decays:

```sh
uv sync --group capture
uv run parallax book record --symbol BTCUSDT      # start first; L2 history cannot be backfilled
uv run parallax book record --symbol BTCUSDT --market futures   # + liquidations, funding, perp book
uv run parallax book build  --symbol BTCUSDT
uv run parallax book sweep  --round-trip-cost-bps 14.0
uv run parallax book impact                        # scaling exponents of the governing equation
uv run parallax book revelation                    # pressure vs maker-withdrawal tests
```

The scheduled mechanical-flow calendar (unlocks, expiries, delistings) lives in
`events/calendar.jsonl`; schema and filing discipline in
[`docs/research/R01-crypto/EVENTS.md`](docs/research/R01-crypto/EVENTS.md).

See [`docs/research/R01-crypto/DATA.md`](docs/research/R01-crypto/DATA.md) for the candle contract,
[`docs/research/R01-crypto/MICROSTRUCTURE.md`](docs/research/R01-crypto/MICROSTRUCTURE.md) for the
order-book hypothesis, and
[`docs/research/R01-crypto/PROTOCOL.md`](docs/research/R01-crypto/PROTOCOL.md) for the crypto
benchmark, cost, journal, and promotion rules. The
[`R01 hypothesis registry`](docs/research/R01-crypto/hypothesis/README.md) is the canonical crypto
claim ledger; the [`R01 agenda`](docs/research/R01-crypto/RESEARCH_AGENDA.md) preserves the broader
motivation and experiment sequence.

## Layout

```text
src/parallax/          common research infrastructure and domain packages
docs/research/         numbered durable research records: RNN-title
docs/ideas/            repository-wide raw ideas: INNN-title.md
docs/sessions/         requested continuation handoffs: YYYY-MM-DD-title.md
notebooks/             matching RNN-title exploration and learning implementations
tests/                 offline deterministic tests
docs/                  research contracts and operating decisions
data/RNN-title/raw/    immutable observations owned by one research program (ignored)
data/RNN-title/processed/ derived datasets with provenance (ignored)
artifacts/             generated reports, plots, and model outputs (ignored)
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the graduation boundary between a learning
notebook experiment and reusable production code.
