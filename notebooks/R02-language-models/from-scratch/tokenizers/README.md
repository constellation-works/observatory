---
title: "R02 Tokenizers"
summary: "Build sequence and first empirical comparison for byte, character, word, and BPE tokenizers."
tags: [parallax, language-models, tokenizers, from-scratch]
related: ["notebooks/R02-language-models/from-scratch/README.md", "notebooks/R02-language-models/from-scratch/experiments/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R02
domain: language-models
---

# Tokenizers

## Planned sequence

- [ ] UTF-8 byte tokenizer with exact round-trip tests
- [ ] Character tokenizer with explicit unknown-character behavior
- [ ] Word tokenizer as a deliberately brittle baseline
- [ ] Byte-pair encoding trainer and deterministic merge table
- [ ] BPE encoder/decoder with serialization and round-trip tests
- [ ] Comparison of vocabulary size, sequence length, compression, and unknown handling

## First research question

At a fixed corpus split and vocabulary budget, does hand-built BPE reduce held-out bytes per token
relative to the byte and character baselines without breaking exact decoding?
