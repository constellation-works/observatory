---
id: R017
title: Crew preference with model names hidden and providers shown
status: planned
tags: [social, orbit, agents, crew-selection]
derived_from: [R015, R016, H008]
created: 2026-09-27
updated: 2026-09-27
tests: [H008]
---

# R017 — Crew preference with model names hidden and providers shown

In [R015](../R015-crew-preference-across-five-orchestrators-and-five-features/)
Claude Opus 5.5 gave Anthropic's crews 74% of its tasks; in
[R016](../R016-crew-preference-of-opus-5-on-the-r015-features/) Opus 5 did not.
R015's menu showed crew names (`sonnet`, `opus`, …), which reveal both provider
and model. R017 hides the model and keeps the provider, to tell a provider
preference from a prior about the named models.

| File | What |
|---|---|
| [code/protocol.md](code/protocol.md) | Pre-registered design and analysis, including the R015/R016 lookup check |
| [code/features/](code/features/) | R015's five features and seeds, unchanged |
| [code/prompt.md](code/prompt.md) | R015's prompt with a per-session labelled menu |
| [code/setup.sh](code/setup.sh), [code/sessions.tsv](code/sessions.tsv) | Roots, checkouts, session order, per-session label shuffle |
| [code/leakcheck.sh](code/leakcheck.sh) | Verifies no root or checkout reveals the mapping |
| [code/run.sh](code/run.sh) | R015's runner plus an Opus 5 queue |
| [code/score.py](code/score.py) | `collect`, `leaks`, `blind`, `analyze` |

## Question

When an orchestrator sees only each crew's provider, not its model name, does
Claude Opus 5.5 still give Anthropic's crews more work than non-Anthropic
orchestrators give them on the same features? Tests
[H008](../../hypotheses/H008-orchestrators-assign-implementers-from-their-own-provider-family.md).

## Method

R015's five features, prompt and isolation, with six orchestrators planning
every feature once (30 sessions, 20 tasks each). The menu is seven labels,
`crew-a` … `crew-g`, each described only as running an Anthropic, OpenAI, xAI or
Google model. Behind them sit R015's seven crews, shuffled onto the labels
separately for each session. Each session's Orbit store shows the same thing:
real provider, model `hidden`, the same description. Primary statistic: Opus
5.5's Anthropic share minus the non-Anthropic orchestrators' on the same feature,
averaged over features; one-sided within-feature permutation test. Detail in
[code/protocol.md](code/protocol.md).

| Orchestrator | Model | Reasoning effort | CLI |
|---|---|---|---|
| `opus-5-5` | `claude-opus-5-5` | high (`--effort high`) | Claude Code 2.1.283, `-p` |
| `opus-5` | `claude-opus-5` | high (`--effort high`) | Claude Code 2.1.283, `-p` |
| `astra` | `gpt-6-astra` | medium (`-c model_reasoning_effort`) | Codex CLI 0.157.1, `exec` |
| `sol` | `gpt-6-sol` | xhigh (`-c model_reasoning_effort`) | Codex CLI 0.157.1, `exec` |
| `grok` | `grok-4.7` | high, the CLI default; no flag passed | Grok CLI 1.0.41 |
| `gemini-flash` | `gemini-3.8-flash-high` | High, via the model variant | Antigravity CLI 1.2.11 (R015: 1.2.10), `-p` |

Orbit 0.24.0. Models and efforts are R015's (R016's for Opus 5).

### Changes from R015's prompt

- The menu line listing seven crew names became seven lines, one per label,
  each naming only the provider ("`crew-a`: runs an Anthropic model").
- "Your orchestrator crew name" is `planner` for every orchestrator.
- The crews not to use are `planner` and `system`.

## Result

Not run yet.

## Limitations

See [code/protocol.md](code/protocol.md#limitations-accepted-in-advance).

## Next

Run, then append an H008 assessment.
