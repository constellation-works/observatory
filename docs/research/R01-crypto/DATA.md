---
title: "R01 Crypto Candle Data Contract"
summary: "Point-in-time ingestion, normalization, partitioning, and immutability rules for crypto candles."
tags: [parallax, crypto, market-data, data-contract]
related: ["docs/research/R01-crypto/README.md", "docs/research/R01-crypto/PROTOCOL.md"]
created_on: 2026-07-31
updated_on: 2026-08-19
status: active
research_id: R01
domain: crypto
---

# Candle data contract

Parallax backfills unauthenticated one-minute spot candles from two independent venues:

- Binance Spot `GET /api/v3/klines` through the market-data-only host, with 1,000 candles per
  request.
- Coinbase Exchange `GET /products/{product_id}/candles`, with 300 candles per request.

Both adapters paginate explicit UTC ranges, normalize into the same candle schema, and write
Zstandard-compressed Parquet partitions by venue, product, interval, and UTC day. Raw partitions
are immutable: an identical rerun is accepted, while conflicting bytes for an existing day stop
the backfill for investigation. The command reports missing minute buckets rather than silently
forward-filling them.

R01 owns these datasets under `data/R01-crypto/`: source observations live in `raw/`, while every
derived table lives in `processed/` with its inputs and transformation revision recorded.

Coinbase documents that historical rates can be incomplete and omits intervals with no ticks.
Missing buckets therefore remain missing in raw data. Any later fill policy belongs in a versioned
processed dataset, never the raw layer.

External versioned tapes (including local Kaggle snapshots) used by an experiment are cited in that
experiment's data contract: handle, numeric version, file path, SHA-256, retrieval time, license,
and information cutoff. They are not imported into `data/R01-crypto/raw/` unless an immutable R01
snapshot is created. Do not treat a Kaggle mirror as a substitute for the Binance and Coinbase
contracts above.

## Backfill

Dates are UTC, with an inclusive start and exclusive end. Use complete historical days so a raw
daily partition never represents a still-forming day.

```sh
uv run parallax data fetch \
  --venue binance --symbol BTCUSDT \
  --start 2023-01-01 --end 2026-07-31

uv run parallax data fetch \
  --venue coinbase --symbol BTC-USD \
  --start 2023-01-01 --end 2026-07-31
```

The endpoints, limits, and schemas were checked against official exchange documentation on
2026-07-31. Reverify them before changing an adapter or diagnosing a remote error.
