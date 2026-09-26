---
id: R016
title: Crew preference of Opus 5 on the R015 features
status: running
tags: [social, orbit, agents, crew-selection]
derived_from: [R015, R013, H008]
created: 2026-09-26
updated: 2026-09-26
tests: [H008]
---

# R016 — Crew preference of Opus 5 on the R015 features

In [R015](../R015-crew-preference-across-five-orchestrators-and-five-features/)
Claude Opus 5.5 gave Anthropic's crews about three quarters of its tasks while
the other orchestrators gave them about a third. R013's Opus 5 did not show this,
on one feature. R016 reruns R015's design for the `opus` orchestrator with Opus 5
to see whether the preference predates Opus 5.5.

| File | What |
|---|---|
| [code/protocol.md](code/protocol.md) | Pre-registered comparison, written after seeing R015's Opus 5.5 result |
| [code/features/](code/features/), [code/prompt.md](code/prompt.md) | R015's features, seeds and prompt, unchanged |
| [code/setup.sh](code/setup.sh), [code/run.sh](code/run.sh), [code/sessions.tsv](code/sessions.tsv) | R015's scripts: Opus 5, five parallel sessions, own roots |
| [code/score.py](code/score.py) | `collect`, `analyze` (uses R015's data as the comparison) |
| [artifacts/results.md](artifacts/results.md) | Results |

## Question

Does Claude Opus 5, as orchestrator, give Anthropic's crews more work than the
non-Anthropic orchestrators in R015 give them on the same features? Tests
[H008](../../hypotheses/H008-orchestrators-assign-implementers-from-their-own-provider-family.md).

## Method

R015's features, prompt, menu, isolation and scripts, with `claude-opus-5`
(Claude Code, effort high) in place of `claude-opus-5-5`. Five sessions of 20
tasks, one per feature. Primary statistic: Opus 5's Anthropic share minus the
mean share R015's `astra`, `gemini-flash`, `grok` and `sol` gave Anthropic on
the same feature, averaged over features; one-sided within-feature permutation
test. Detail in [code/protocol.md](code/protocol.md).

## Result

Pending.

## Limitations

- The question was prompted by R015's Opus 5.5 result.
- Comparison sessions are R015's, run about an hour earlier, not alongside.
- Crew names reveal the provider; the operator is an Anthropic model.

## Next

Pending.
