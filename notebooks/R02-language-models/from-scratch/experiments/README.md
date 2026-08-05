---
title: "R02 From-Scratch Experiments"
summary: "Recording contract for controlled comparisons of hand-built language-model components."
tags: [parallax, language-models, experiments, from-scratch]
related: ["notebooks/R02-language-models/from-scratch/README.md", "docs/RESEARCH_PROTOCOL.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R02
domain: language-models
---

# From-scratch experiments

Experiment outputs belong under ignored `artifacts/`; compact configurations and reports may live
here. Every comparison records:

- registered experiment id;
- corpus and split version;
- implementation revision;
- baseline and primary metric;
- parameter count and compute budget;
- seeds and number of repeats;
- result with uncertainty; and
- reject, revise, or advance decision.

Start with tokenizer compression and round-trip correctness, then a bigram language-model baseline,
then the smallest transformer that can overfit a tiny fixture before using a real corpus.
