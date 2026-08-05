---
title: "Parallax Repository Guide"
summary: "Operating rules and structural conventions for the Parallax research platform."
tags: [parallax, repository-guide, research-conventions]
related: ["README.md", "docs/ARCHITECTURE.md", "docs/research/README.md"]
created_on: 2026-07-31
updated_on: 2026-08-03
status: active
---

# Parallax — repository guide

Parallax is a domain-neutral platform for falsifiable, reproducible empirical research. Crypto is
the first numbered program and remains the most developed domain adapter; it is not the platform
boundary.

## Operating rules

- Research and simulation are the default. Do not add or enable live trading, external actions,
  deployment, or consequential recommendations unless Daniel explicitly authorizes that scope.
- Never commit API keys, wallet material, account identifiers, private market data, or `.env`
  files.
- Treat timestamps as UTC and preserve raw observations unchanged. Derived datasets must record
  their inputs and transformation version.
- Every result requires a prespecified baseline, primary metric, information cutoff, appropriate
  holdout design, uncertainty, and an explicit reject/revise/advance decision.
- Within the crypto domain, a strategy result is incomplete without the matching Bitcoin
  buy-and-hold benchmark, turnover, fees, slippage assumptions, and an out-of-sample interval.
- Prevent look-ahead and survivorship leakage by construction. Signals become executable only
  after the data used to compute them was observable.
- Notebooks are exploratory. Move reusable logic and every claimed result into tested code under
  `src/`.
- Keep exchange integrations behind interfaces and make all side-effecting operations dry-run by
  default.

## Layers

- `docs/research/RNN-title/` — durable contracts, agenda, and findings for one numbered research
  domain.
- `docs/research/RNN-title/hypothesis/` — one durable `HNN-title.md` claim per hypothesis.
- `docs/research/RNN-title/experiments/` — one preregistered `ENN-title.md` methodology and outcome
  record per experiment.
- `docs/research/RNN-title/docs/` — supporting domain knowledge that is neither a hypothesis nor an
  experiment.
- `docs/ideas/` — repository-wide raw idea intake using permanent `INNN-title.md` identities.
- `docs/sessions/` — requested agent-session handoffs named `YYYY-MM-DD-title.md`.
- `notebooks/RNN-title/` — exploratory notebooks and transparent learning implementations for the
  same research id and title.
- `data/RNN-title/` — local raw observations, processed datasets, and domain state owned by that
  same research program.
- `src/parallax/title/` — tested domain code, using underscores when a title contains hyphens.
- `src/parallax/research/` and other base modules — common infrastructure with no domain-specific
  assumptions.
- `docs/ARCHITECTURE.md` — the complete boundary and graduation rules.

## Research directory convention

- Research directories are named `R<NN>-<title>`, beginning with `R01`; titles are stable,
  lowercase kebab-case slugs.
- The exact directory name must exist under `docs/research/`, `notebooks/`, and `data/`. Every data
  partition contains `raw/` and `processed/`; never write domain data directly to `data/raw/` or
  `data/processed/`.
- The title maps to a Python package under `src/parallax/`; replace hyphens with underscores only
  because Python package names cannot contain hyphens.
- Current assignments are `R01-crypto`, `R02-language-models`, and `R03-consumer-goods`. Never
  renumber an existing research program; numbers are durable identities, not priority ranks.
- Each dataset has one owning research slug. Cross-program consumers link its immutable snapshot
  and provenance instead of silently moving or reclassifying it.
- `docs/research/README.md` is the canonical index. Generic reusable templates live under
  `docs/_templates/`; only instantiated research project directories use the `RNN-title` pattern.

## Hypothesis and experiment convention

- Hypotheses are named `H<NN>-<title>.md`; experiments are named `E<NN>-<title>.md`. Numbers are
  zero-padded, scoped to their research program, permanent, and never reused or renumbered.
- A hypothesis freezes one falsifiable claim, its mechanism, predicted observables, baseline,
  alternatives, and rejection criteria. Its `hypothesis_id` must match the filename.
- An experiment tests exactly one primary hypothesis. Its `experiment_id` and `hypothesis_id` must
  match an existing local record, and `related` must link that hypothesis document.
- Freeze the experiment's methodology before opening final evaluation data. Append results,
  deviations, and one outcome—`reject`, `revise`, `advance`, or `inconclusive`—without rewriting the
  preregistration.
- Every experiment declares `preregistered: true` or `false`. A `false` record — data seen before
  the design was written — is legitimate and worth keeping, but can never carry `advance`; only a
  new preregistered experiment on unseen data promotes a claim. Enforced by repository tests.
- Exploratory surprises create a new hypothesis and experiment. They never become confirmatory by
  editing an earlier record after the fact.
- Copy the generic `docs/_templates/HYPOTHESIS.md` and `EXPERIMENT.md` templates. Add each created
  record to the registry README in its directory.

## Ideas and session handoffs

- Capture a raw idea in `docs/ideas/I<NNN>-<title>.md`. The three-digit counter is repository-wide,
  permanent, and never reused. An idea may graduate into a hypothesis, experiment, supporting
  document, numbered research program, or external venture; append links and retain the source idea.
- Write `docs/sessions/<YYYY-MM-DD>-<title>.md` only when Daniel requests a session summary. It is a
  concise handoff containing objective, context, decisions, completed work, evidence, open threads,
  and the exact place to resume—not a transcript or automatic activity log.
- Use lowercase kebab-case titles and the generic `IDEA.md` and `SESSION.md` templates. Never put
  credentials, secrets, private data, or unnecessary transcript content in either record.

## Markdown frontmatter

Every Markdown file in the repository starts with YAML frontmatter containing at least:

- `tags`: a YAML list of lowercase kebab-case connection terms;
- `title`: a human-readable document title;
- `summary`: a non-empty, single-line description;
- `related`: a YAML list of repository-relative Markdown paths;
- `created_on` and `updated_on`: ISO dates (`YYYY-MM-DD`);
- `status`: one of `active`, `draft`, `paused`, `completed`, `archived`, or `superseded`.

Markdown inside a numbered research directory also includes `research_id` (for example `R01`) and
`domain` (for example `crypto`). Keep `related` paths current when moving a document; the fields are
the graph contract, not decorative metadata.

## Development

```sh
uv sync --group dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv sync --group notebook  # once, when notebook work is needed
make notebook
```

The integration branch is `agent-main`; the repository uses Constellation's direct gate.
