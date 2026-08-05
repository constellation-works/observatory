---
title: "Parallax Architecture"
summary: "The numbered research, notebook, domain-package, and common-infrastructure boundaries."
tags: [parallax, architecture, research-conventions]
related: ["CLAUDE.md", "docs/research/README.md", "docs/RESEARCH_PROTOCOL.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
---

# Parallax architecture

Parallax separates common research discipline from domain assumptions while giving every research
program one durable identity across prose, exploration, and tested code.

Before an idea belongs to a numbered domain, it can live in `docs/ideas/INNN-title.md`. Requested
agent-session continuation context lives separately in `docs/sessions/YYYY-MM-DD-title.md`; a handoff
points to durable research records and never replaces them.

## Research identity

Each program receives an immutable directory name:

```text
R<NN>-<title>
```

- `NN` is a zero-padded sequence beginning at `01`.
- `title` is a stable lowercase kebab-case domain slug.
- The number is identity, not priority; never recycle or renumber it.

The identity is mirrored across layers:

```text
docs/research/R01-crypto/       durable contracts, agenda, and findings
  hypothesis/HNN-title.md       frozen claims and rejection criteria
  experiments/ENN-title.md      preregistration, results, and outcome
  docs/                         supporting domain knowledge
notebooks/R01-crypto/           exploration and disposable analysis
data/R01-crypto/                local raw and processed research data
src/parallax/crypto/            tested crypto-domain code

docs/research/R02-language-models/
notebooks/R02-language-models/
data/R02-language-models/
src/parallax/language_models/   hyphens become underscores only for Python
```

## Five layers

1. **Common research kernel — `src/parallax/research/`.** Domain-neutral preregistration and
   immutable outcomes. It knows questions, baselines, metrics, cutoffs, and decisions—not trades,
   tokens, patients, or customers.
2. **Research record — `docs/research/RNN-title/`.** Domain charter and three typed collections:
   `hypothesis/HNN-title.md` for frozen claims, `experiments/ENN-title.md` for tests and outcomes,
   and `docs/` for supporting domain knowledge.
3. **Data — `data/RNN-title/`.** Local immutable observations under `raw/`, reproducible derived
   datasets under `processed/`, and domain-owned state such as research journals. A physical
   dataset has one owning research slug even when another program consumes it.
4. **Exploration — `notebooks/RNN-title/`.** Notebooks and transparent learning implementations.
   This layer optimizes for understanding and can be rewritten freely.
5. **Domain code — `src/parallax/title/`.** Tested, reusable logic supporting durable claims.
   Common modules stay at the package base only when they contain no domain assumption.

## Graduation rule

Notebook code does not support a durable claim directly. When research needs an exploratory
component:

1. state its behavioral and numerical contract;
2. add deterministic examples and comparison tests;
3. move reusable code into the matching domain package;
4. record the exact code revision in the experiment; and
5. retain a teaching version in notebooks when it explains the mechanism more clearly.

## Adding a research program

1. Assign the next unused `RNN` and a stable title.
2. Copy `docs/_templates/RESEARCH.md` and `RESEARCH_AGENDA.md` into the new docs directory.
3. Create `hypothesis/`, `experiments/`, and `docs/` registries inside it.
4. Create the identical directory name under `notebooks/` and `data/`; add `raw/` and `processed/`
   boundaries under the data directory.
5. Create `src/parallax/<title>/`, translating hyphens to underscores for Python.
6. Add the program to `docs/research/README.md` and connect all Markdown through `related`.
7. Create the first `HNN-title.md`, then preregister its first `ENN-title.md` experiment before
   opening final evaluation data.

Repository tests enforce the docs/notebooks/data mirror, source-package mapping, record and data
directories, file and frontmatter identities, hypothesis links, required experiment sections, and
Markdown graph.
