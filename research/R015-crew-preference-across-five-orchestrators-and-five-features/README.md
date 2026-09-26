---
id: R015
title: Crew preference across five orchestrators and five features
status: running
tags: [social, orbit, agents, crew-selection]
derived_from: [R013, R014, H008]
created: 2026-09-26
updated: 2026-09-26
tests: [H008]
---

# R015 — Crew preference across five orchestrators and five features

R013 and R014 were pilots: one feature, one session per orchestrator, 83 tasks
in all, scored only against the menu. This run has five orchestrators each plan
five features in separate sessions of 20 tasks (500 tasks), and compares each
orchestrator with the others on the same work. The protocol and analysis were
committed before any session ran.

| File | What |
|---|---|
| [code/protocol.md](code/protocol.md) | Pre-registered design, primary test, exclusions |
| [code/features/](code/features/) | The five feature briefs and seed repositories |
| [code/prompt.md](code/prompt.md) | Orchestrator prompt (R013's, edits below) |
| [code/setup.sh](code/setup.sh), [code/sessions.tsv](code/sessions.tsv) | Roots, checkouts, Latin-square session plan |
| [code/run.sh](code/run.sh) | Runs the sessions, each under a fresh isolated `HOME` |
| [code/score.py](code/score.py) | `collect`, `blind`, `analyze` |
| [artifacts/results.md](artifacts/results.md) | Scored results |

## Question

Do orchestrating agents give their own provider's crews more work than
orchestrators from other providers give those crews, on the same features?
Tests [H008](../../hypotheses/H008-orchestrators-assign-implementers-from-their-own-provider-family.md),
which R013 marked refuted on a pilot and says would be revived by a lift well
above 1 on a second feature.

## Method

Five orchestrators (`astra` GPT-6 Astra, `opus` Claude Opus 5.5, `gemini-flash`
Gemini 3.8 Flash High, `grok` Grok 4.7, `sol` GPT-6 Sol) each plan five features
(`change-explorer` from R013, plus `field-sync`, `build-cache`, `docs-site`,
`ledger-import`), one session per pair, in a Latin-square order. Each session
files exactly 20 tasks, each assigned to one of R013's seven menu crews with a
one-line reason. Every session has its own Orbit root, seed checkout and
throwaway `HOME`. Nothing is dispatched.

Primary statistic: for each orchestrator, its own-provider share minus the share
other-provider orchestrators gave that provider on the same feature, averaged
over features and then over orchestrators (D). One-sided permutation test that
shuffles orchestrator labels within each feature. Full detail, secondary
analyses and exclusion rules in [code/protocol.md](code/protocol.md).

### Changes from R013's prompt

- "Aim for **8–20** tasks" became "File **exactly 20** implementation tasks".
- The line naming R013's one dependency doc became "Treat the files under
  `docs/` as the documented dependencies".
- Internal system and workspace names were removed ("live Constellation MCP",
  `ws_orbit-graph`, `ws_constellation`, `ws_orbit-research`); the instructions
  to stay inside the given root and workspace remain.

## Result

Pending.

## Limitations

- Crew names reveal the provider.
- The operator wrote four of the five features and will code the reasons, and
  is an Anthropic model with Anthropic crews on the menu. Reasons are coded
  blind to orchestrator.
- One session per orchestrator per feature.
- The `opus` orchestrator is Opus 5.5 here and was Opus 5 in R013; `sol` is
  GPT-6 Sol here and GPT-5.6 then.

## Next

Pending.
