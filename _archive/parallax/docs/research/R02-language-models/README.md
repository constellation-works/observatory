---
title: "R02 Language Models"
summary: "Charter and evidence boundary for tokenization, neural networks, and small transformer research."
tags: [parallax, language-models, tokenizers, transformers]
related: ["notebooks/R02-language-models/README.md", "docs/research/R02-language-models/hypothesis/README.md", "docs/research/R02-language-models/experiments/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R02
domain: language-models
---

# R02 language models

## Purpose

Understand tokenization, representation learning, optimization, attention, and transformer behavior
by implementing small systems and testing narrow empirical questions.

## Boundary

- Begin with public, synthetic, or personally owned corpora whose license and provenance are known.
- Do not train on private messages, credentials, personal records, or third-party restricted data.
- Educational models are not represented as production-capable systems.
- Capability, safety, and social-impact claims require their own registered evidence; benchmark
  improvement alone does not establish them.

## Evidence contract

- Freeze corpus version and train/validation/test partitions before comparison.
- Start with byte- or character-level and trivial statistical baselines.
- Report parameter count, vocabulary size, context length, compute, random seed, training tokens,
  and wall-clock cost.
- Separate optimization metrics from downstream task metrics.
- Use repeated seeds or uncertainty intervals when stochastic variation can change the conclusion.

## Initial learning path

The teaching implementations live in
[`notebooks/R02-language-models/from-scratch/`](../../../notebooks/R02-language-models/from-scratch/).
The first suggested comparison is byte or character tokenization versus a hand-built BPE tokenizer
at a fixed corpus split and vocabulary budget.

Register the claim in [`hypothesis/`](hypothesis/README.md), preregister each test in
[`experiments/`](experiments/README.md), and keep evolving literature or design notes under
[`docs/`](docs/README.md).
