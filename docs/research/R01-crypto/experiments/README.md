---
title: "R01 Crypto Experiment Registry"
summary: "Registry for preregistered crypto experiments and their preserved outcomes."
tags: [parallax, crypto, experiments, research-registry]
related: ["docs/research/R01-crypto/hypothesis/README.md", "docs/research/R01-crypto/PROTOCOL.md", "docs/_templates/EXPERIMENT.md"]
created_on: 2026-08-03
updated_on: 2026-08-19
status: active
research_id: R01
domain: crypto
---

# R01 crypto experiment registry

Create experiments as `E<NN>-<lowercase-kebab-title>.md`, using the next unused R01 experiment
number. Every experiment tests exactly one primary hypothesis, links that `HNN` record in both
frontmatter and `related`, and freezes its methodology before final evaluation.

| ID | Experiment | Hypothesis | Methodology | Preregistered | Outcome |
|---|---|---|---|---|---|
| E01 | [Bitstamp US night hourly drift](E01-bitstamp-us-night-hourly-drift.md) | [H08](../hypothesis/H08-day-trader-night-flattening.md) | [script](../../../../notebooks/R01-crypto/E01-bitstamp-us-night-hourly-drift.py) | false | revised |

Retain every experiment after rejection, invalidation, revision, or an inconclusive result. A
`preregistered: false` record cannot `advance` its hypothesis.
