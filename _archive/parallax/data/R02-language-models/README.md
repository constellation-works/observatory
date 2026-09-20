---
title: "R02 Language Models Data"
summary: "Local storage boundary for corpora and derived language-model research data."
tags: [parallax, language-models, corpora, data-registry]
related: ["data/README.md", "docs/research/R02-language-models/README.md", "notebooks/R02-language-models/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R02
domain: language-models
---

# R02 language-model data

- `raw/` contains immutable, licensed source corpora and their provenance manifests.
- `processed/` contains reproducible tokenized corpora, splits, vocabularies, and derived datasets.
- `research.sqlite3` is the R02 experiment journal when created by the CLI.

Never place private messages, credentials, personal records, or restricted third-party corpora here.
Record license, source version, acquisition time, checksum, split construction, and transformation
revision before using a dataset in an experiment.
