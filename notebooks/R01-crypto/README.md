---
title: "R01 Crypto Notebooks"
summary: "Exploratory notebooks and disposable analyses for the R01 crypto research program."
tags: [parallax, crypto, notebooks, exploration]
related: ["docs/research/R01-crypto/README.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md", "docs/research/R01-crypto/experiments/E01-bitstamp-us-night-hourly-drift.md"]
created_on: 2026-08-03
updated_on: 2026-08-19
status: active
research_id: R01
domain: crypto
---

# R01 crypto notebooks

Exploratory crypto analysis belongs here. Sequence is hypothesis → notebook → experiment: freeze
`HNN`, implement `ENN-title.ipynb` or `.py` here, then write the experiment record from that run.

Each notebook records its registered experiment id, input data cutoff, environment, and output
artifact paths. Reusable logic and every implementation supporting a durable claim graduate to
`src/parallax/crypto/` with deterministic tests.

| Experiment | Methodology |
|---|---|
| [E01](../../docs/research/R01-crypto/experiments/E01-bitstamp-us-night-hourly-drift.md) | [E01-bitstamp-us-night-hourly-drift.py](E01-bitstamp-us-night-hourly-drift.py) / [E01-bitstamp-us-night-hourly-drift.ipynb](E01-bitstamp-us-night-hourly-drift.ipynb) |
