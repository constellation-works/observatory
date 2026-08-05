---
title: "R02 From-Scratch Model Lab"
summary: "Learning sequence for transparent tokenizer, neural-network, and transformer implementations."
tags: [parallax, language-models, from-scratch, learning-lab]
related: ["notebooks/R02-language-models/README.md", "docs/research/R02-language-models/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R02
domain: language-models
---

# From-scratch model lab

This lab exists to understand mechanisms by building them. Code here favors transparent equations,
small data, assertions, and inspectable intermediate values over speed or framework conventions.

## Rules

- Implement the idea before using a high-level equivalent as an oracle.
- Start with Python and NumPy; add a dependency only when the lesson specifically concerns it.
- Pair each primitive with a tiny hand-computable example and a numerical comparison test.
- Record shapes, invariants, parameter counts, seeds, and expected failure modes.
- Keep datasets tiny and licensed; generated fixtures are preferred for unit tests.
- Do not use lab code as evidence for a durable research claim. Graduate the needed implementation
  according to [`docs/ARCHITECTURE.md`](../../../docs/ARCHITECTURE.md).

## Build order

1. [`tokenizers/`](tokenizers/README.md) — bytes, characters, BPE, encoding contracts
2. [`neural-networks/`](neural-networks/README.md) — tensors, gradients, layers, losses, optimizers
3. [`transformers/`](transformers/README.md) — embeddings, attention, blocks, autoregressive models
4. [`experiments/`](experiments/README.md) — controlled comparisons and learning reports

Each stage should remain runnable on a laptop with deliberately small models and corpora.
