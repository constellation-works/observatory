---
title: "R02 Transformers"
summary: "Build sequence for attention, decoder blocks, autoregressive training, and ablations."
tags: [parallax, language-models, transformers, from-scratch]
related: ["notebooks/R02-language-models/from-scratch/README.md", "notebooks/R02-language-models/from-scratch/neural-networks/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R02
domain: language-models
---

# Transformers

## Planned sequence

- [ ] token and positional embeddings
- [ ] scaled dot-product attention with an explicit causal mask
- [ ] multi-head attention and head concatenation
- [ ] residual paths and layer normalization
- [ ] feed-forward block
- [ ] complete decoder block
- [ ] tiny autoregressive language model
- [ ] training loop, checkpoint, sampling, and evaluation
- [ ] ablations for heads, context length, depth, and tokenizer choice

Each implementation should expose intermediate tensors and assert expected shapes. Compare the final
small model against a bigram baseline before increasing complexity.
