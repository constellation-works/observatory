---
title: "Research Index"
summary: "Canonical registry of numbered Parallax research programs and their mirrored layers."
tags: [parallax, research-index, research-conventions]
related: ["docs/ARCHITECTURE.md", "docs/RESEARCH_PROTOCOL.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
---

# Research index

| Research | Domain record | Exploration | Local data | Tested code | Status |
|---|---|---|---|---|---|
| `R01-crypto` | [`R01-crypto/`](R01-crypto/README.md) | [`notebooks/R01-crypto/`](../../notebooks/R01-crypto/README.md) | [`data/R01-crypto/`](../../data/R01-crypto/README.md) | [`parallax.crypto`](../../src/parallax/crypto/) | active |
| `R02-language-models` | [`R02-language-models/`](R02-language-models/README.md) | [`notebooks/R02-language-models/`](../../notebooks/R02-language-models/README.md) | [`data/R02-language-models/`](../../data/R02-language-models/README.md) | [`parallax.language_models`](../../src/parallax/language_models/) | active |
| `R03-consumer-goods` | [`R03-consumer-goods/`](R03-consumer-goods/README.md) | [`notebooks/R03-consumer-goods/`](../../notebooks/R03-consumer-goods/README.md) | [`data/R03-consumer-goods/`](../../data/R03-consumer-goods/README.md) | [`parallax.consumer_goods`](../../src/parallax/consumer_goods/) | active |
| `R04-ai-assistants` | [`R04-ai-assistants/`](R04-ai-assistants/README.md) | [`notebooks/R04-ai-assistants/`](../../notebooks/R04-ai-assistants/README.md) | [`data/R04-ai-assistants/`](../../data/R04-ai-assistants/README.md) | [`parallax.ai_assistants`](../../src/parallax/ai_assistants/) | paused |

Research directory names are durable identities. Add the next unused number; never renumber an
existing program when priorities change.

The identical slug also exists under `data/`. See the [`data registry`](../../data/README.md) for
ownership, raw/processed boundaries, and cross-program provenance rules.

Every numbered research directory contains three registries:

- `hypothesis/H<NN>-<title>.md` freezes a claim, baseline, alternatives, and rejection criteria;
- `experiments/E<NN>-<title>.md` freezes one test's methodology, then appends its results and
  outcome; and
- `docs/` holds evolving supporting domain knowledge.

The `HNN` and `ENN` counters are independent and local to a research program. Use lowercase
kebab-case titles and the generic templates in [`docs/_templates/`](../_templates/RESEARCH.md).
