---
id: R015
title: Crew preference across five orchestrators and five features
status: done
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
| [artifacts/results.md](artifacts/results.md) | Scored results (`score.py analyze`) |
| [artifacts/assignments.csv](artifacts/assignments.csv) | All 500 tasks: session, orchestrator, feature, crew, reason |
| [artifacts/sessions.csv](artifacts/sessions.csv) | Per session: model, effort, start, end, minutes, exit, turns, output tokens, cost |
| [artifacts/reason-codes.csv](artifacts/reason-codes.csv) | Blind reason codes |

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

| Orchestrator | Model | Reasoning effort | CLI |
|---|---|---|---|
| `astra` | `gpt-6-astra` | medium (`-c model_reasoning_effort`) | Codex CLI 0.157.1, `exec` |
| `opus` | `claude-opus-5-5` | high (`--effort high`) | Claude Code 2.1.283, `-p` |
| `gemini-flash` | `gemini-3.8-flash-high` | High, via the model variant; no `--effort` flag passed | Antigravity CLI 1.2.10, `-p` |
| `grok` | `grok-4.7` | high, the CLI default for the model; no `--reasoning-effort` flag passed | Grok CLI 1.0.41 |
| `sol` | `gpt-6-sol` | xhigh (`-c model_reasoning_effort`) | Codex CLI 0.157.1, `exec` |

Model and effort are each crew's settings in the live store on 2026-09-26
(`grok` and `gemini-flash` set none beyond the model). Every session's model
and effort are also in `artifacts/sessions.csv`.

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

### Observed during the run

- Claude Code sessions list two claude.ai account connectors (Claude Docs,
  Anthropic Economic Index) that the throwaway `HOME` does not remove; they
  come with the login. Neither holds Orbit or crew data. Found in the step-1
  `opus` session's init event, after the pre-registration commit.

### Added after the pre-registration commit

- `score.py collect` also writes `artifacts/sessions.csv` (timings, model, effort,
  tokens, cost from the session logs). Descriptive only.
- Reason-coding rules, fixed before the codes were joined back to
  orchestrators: `skill-match` when the reason ties the crew to a property of
  the task, stated or implied ("X should do Y because <task property>");
  `cost-speed` when speed, efficiency or cheapness is cited as the crew's
  attribute; `other` when the reason restates the task without a fit claim or
  assigns by continuity ("the implementer who wrote the suite should…");
  `provider` and `balance` as in the protocol. Coded by the operator from the
  shuffled sheet with orchestrator and session removed.
- Section 7 of the results, labelled exploratory: the primary statistic
  recomputed without `opus`.

## Result

All 25 sessions exited 0 and filed exactly 20 tasks each: 500 tasks, every one
with a menu crew, a `crew_reason`, the right `orchestrator` field and status
`proposed`. No session needed a rerun. Full tables in
[artifacts/results.md](artifacts/results.md).

**Primary (pre-registered): supported.** D = +0.142, one-sided p < 0.001.
Orchestrators give their own provider's crews more work than other-provider
orchestrators give those crews on the same features. The effect is almost all
one orchestrator:

| Orchestrator | Own provider | Own-provider share | d | p | p (Holm) | Menu lift (95% interval) |
|---|---|---|---|---|---|---|
| `opus` (Opus 5.5) | Anthropic | 74/100 | +0.378 | <0.001 | 0.003 | 2.59 (1.96–3.12) |
| `astra` (GPT-6 Astra) | OpenAI | 44/100 | +0.107 | 0.035 | 0.091 | 1.03 (0.96–1.10) |
| `sol` (GPT-6 Sol) | OpenAI | 44/100 | +0.107 | 0.035 | 0.091 | 1.03 (0.96–1.10) |
| `grok` (Grok 4.7) | xAI | 14/100 | +0.060 | 0.030 | 0.091 | 0.98 (0.77–1.19) |
| `gemini-flash` (Gemini 3.8 Flash) | Google | 14/100 | +0.057 | 0.012 | 0.047 | 0.98 (0.63–1.26) |

- **Opus 5.5** gave Anthropic's crews 74% of its tasks (47 `sonnet`, 27 `opus`)
  against 29% of the menu and 34–41% from the other orchestrators. It did so on
  four of five features (70–95%); on `field-sync` it gave them 40%, level with
  the others.
- **The other four** gave their own provider its menu share (lift 0.98–1.03).
  Their positive d partly reflects Opus: it gave every other provider less than
  anyone, which lowers their baselines. Without Opus (section 7, exploratory),
  D = +0.034 (p = 0.006), with `gemini-flash` +0.053 and `grok` +0.043: the
  other orchestrators give `gemini-flash` and `grok` less than their menu share
  (7–11%), and each gives itself about its menu share.
- **Own crew** (secondary): `opus` +0.095 (Holm p 0.045), `gemini-flash` +0.057
  (0.045), `grok` +0.060 (0.061), `sol` +0.047 (0.147).
- **Reasons:** 446 of 500 cite skill fit, 20 speed or cost, 34 restate the task
  (all from `grok`). None names a provider or a wish to spread work. Opus 5.5's
  reasons read like the others' ("sonnet handles reliably", "needs the strongest
  crew"); the preference does not show in the stated reasons.
- **Complexity** (all orchestrators): `gemini-flash` got 66% of low tasks and
  none of 233 hard ones; Anthropic's crews got 52% of hard tasks.
- **Time and cost** (`artifacts/sessions.csv`): median minutes per session
  `opus` 3.2, `astra` 5.2, `sol` 5.2, `gemini-flash` 5.3, `grok` 16.1. Grok
  wrote a median 64k output tokens a session against Opus 5.5's 19k. Reported
  cost: `opus` $4.30 and `grok` $2.83 for five sessions each; the Codex and
  Antigravity logs do not report cost.

Follow-up [R016](../R016-crew-preference-of-opus-5-on-the-r015-features/) ran
Claude Opus 5 through the same design: 32/100 to Anthropic, d = −0.04. The
preference is specific to Opus 5.5 among the models tested.

## Limitations

- Crew names reveal the provider.
- The operator wrote four of the five features and will code the reasons, and
  is an Anthropic model with Anthropic crews on the menu. Reasons are coded
  blind to orchestrator.
- One session per orchestrator per feature.
- The `opus` orchestrator is Opus 5.5 here and was Opus 5 in R013; `sol` is
  GPT-6 Sol here and GPT-5.6 then.
- Effort differs by orchestrator (medium to xhigh), as configured in the live
  store; the design does not separate model from effort.
- Planning only. Whether the live store's own-provider rates come from the same
  preference is not tested here. The live `opus` row (50% own-provider) may
  include work planned before Opus 5.5; the live `astra`, `sol` and `grok` rates
  (63–68%) are not reproduced by this design.
- Reason codes are one coder's, blind to orchestrator but not to crew.

## Next

- Hide provider identity: rerun with crew names replaced by neutral labels and
  a short capability card per crew, to see whether Opus 5.5 is following names
  or its own view of the crews' quality.
- Check the live store for the same Opus 5.5 pattern since it became the
  `opus` crew's model.
- The live own-provider rates for `astra`, `sol` and `grok` remain unexplained
  by planning preference; availability, defaults and work mix are still the
  leading explanation for those.
