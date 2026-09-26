---
id: R016
title: Crew preference of Opus 5 on the R015 features
status: done
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
| [artifacts/results.md](artifacts/results.md) | Results (`score.py analyze`) |
| [artifacts/assignments.csv](artifacts/assignments.csv) | All 100 tasks with crew and reason |
| [artifacts/sessions.csv](artifacts/sessions.csv) | Per session: model, effort, start, end, minutes, exit, turns, output tokens, cost |

## Question

Does Claude Opus 5, as orchestrator, give Anthropic's crews more work than the
non-Anthropic orchestrators in R015 give them on the same features? Tests
[H008](../../hypotheses/H008-orchestrators-assign-implementers-from-their-own-provider-family.md).

## Method

R015's features, prompt, menu, isolation and scripts, with `claude-opus-5`
(Claude Code 2.1.283, `--effort high`, the same effort R015 gave Opus 5.5) in
place of `claude-opus-5-5`. The comparison orchestrators' models and efforts
are in R015's README: `astra` GPT-6 Astra medium, `gemini-flash` Gemini 3.8
Flash High, `grok` Grok 4.7 high (CLI default), `sol` GPT-6 Sol xhigh. Five sessions of 20
tasks, one per feature. Primary statistic: Opus 5's Anthropic share minus the
mean share R015's `astra`, `gemini-flash`, `grok` and `sol` gave Anthropic on
the same feature, averaged over features; one-sided within-feature permutation
test. Detail in [code/protocol.md](code/protocol.md).

## Result

All five sessions exited 0 and filed exactly 20 compliant tasks (menu crew,
`crew_reason`, `proposed`). Full tables in [artifacts/results.md](artifacts/results.md).

**Primary (pre-registered): not supported.** d = −0.043, one-sided p = 0.974.
Opus 5 gave Anthropic's crews 32 of 100 tasks (menu 28.6; lift 1.12), in line
with R015's non-Anthropic orchestrators on every feature.

| Feature | Opus 5 | Opus 5.5 (R015) | Others (R015 mean) |
|---|---|---|---|
| change-explorer | 30% | 75% | 34% |
| field-sync | 35% | 40% | 40% |
| build-cache | 35% | 70% | 35% |
| docs-site | 30% | 95% | 32% |
| ledger-import | 30% | 90% | 40% |

- Opus 5 minus Opus 5.5: lower on all five features, mean −0.42; the exact
  sign-flip p = 0.062 is the smallest five features allow.
- Own crew: d = −0.005 (p = 0.685).
- Opus 5 spread work almost evenly: 11–17 tasks per crew over the 100, two to
  four per crew in each session. It tallied crews while filing and reported
  "crew spread … all seven used" in its summaries (exploratory observation;
  no reason mentions balancing).
- Time and cost (`artifacts/sessions.csv`): 6.4–11.6 minutes and $10.40 for the
  five sessions, against 3.1–3.8 minutes and $4.30 for Opus 5.5 in R015; median
  35k output tokens a session against 19k.

R013's Opus 5 result (lift 0.92 on one feature) holds on five. The Anthropic
preference in R015 came with Opus 5.5.

## Limitations

- The question was prompted by R015's Opus 5.5 result.
- Comparison sessions are R015's, run about an hour earlier, not alongside.
- Crew names reveal the provider; the operator is an Anthropic model.

## Next

See R015's Next: the anonymised-crew rerun applies to Opus 5.5 in particular.
