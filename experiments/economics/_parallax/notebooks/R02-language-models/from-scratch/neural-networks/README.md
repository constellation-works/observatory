---
title: "R02 Neural-Network Primitives"
summary: "Build sequence for autodiff, layers, losses, optimizers, and numerical checks."
tags: [parallax, language-models, neural-networks, from-scratch]
related: ["notebooks/R02-language-models/from-scratch/README.md", "notebooks/R02-language-models/from-scratch/transformers/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R02
domain: language-models
---

# Neural-network primitives

## Planned sequence

- [ ] scalar reverse-mode automatic differentiation
- [ ] tensor shape and broadcasting exercises
- [ ] affine layers and parameter initialization
- [ ] activation functions and numerical gradient checks
- [ ] cross-entropy and stable softmax
- [ ] SGD, momentum, and Adam
- [ ] normalization, dropout, and train/evaluation modes

Every gradient-bearing component needs a finite-difference check on a tiny deterministic example.
