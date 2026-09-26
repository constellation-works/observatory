---
id: R014
title: Crew preference under an equalized menu with grok and sol orchestrating
status: done
tags: [social, orbit, agents, crew-selection]
derived_from: [R013, H008]
created: 2026-09-26
updated: 2026-09-26
tests: [H008]
---

# R014 — Crew preference under an equalized menu with grok and sol orchestrating

R013 ran three orchestrators (`astra`, `opus`, `gemini-flash`). The live table it
set out to explain also has `grok` (63% own-provider) and `sol` (68%), which R013
did not run. This item runs those two under R013's protocol, unchanged apart from
the deviations listed below.

| File | What |
|---|---|
| [code/protocol.md](code/protocol.md) | R013's protocol, copied unchanged |
| [code/feature.md](code/feature.md), [code/prompt.md](code/prompt.md), [code/seed/](code/seed/) | R013's stimulus, prompt and seed, unchanged |
| [code/setup.sh](code/setup.sh) | R013's setup with `ORCHESTRATORS=(grok sol)`, its own store, and the 0.24 fixes below |
| [code/score.py](code/score.py) | R013's scorer with the R014 orchestrators and menu shares |
| [artifacts/results.md](artifacts/results.md) | Scored rollup of this run |

## Question

When every listed crew is available, do `grok` and `sol` still assign implementers
from their own provider? Tests [H008](../../hypotheses/H008-orchestrators-assign-implementers-from-their-own-provider-family.md).

Both are on the menu, so both can assign work to themselves. Menu shares: `grok`
1/7 ≈ 14% (xAI: grok); `sol` 3/7 ≈ 43% (OpenAI: sol, luna, terra). Read against
the live rates, pure own-provider preference would score about 4.4 for `grok`
(63% ÷ 14%) and about 1.6 for `sol` (68% ÷ 43%).

## Method

As R013: an isolated Orbit root with `default_crew = "system"`, empty complexity
pools, no routines or auto-tasks; one workspace and fresh seed checkout per
orchestrator; the same `feature.md`; the same prompt text with only the bindings
changed; the same closed seven-crew menu; tasks stay `proposed`; nothing is
dispatched. Scored with `code/score.py`.

- Host: dk-server-1, Orbit 0.24.0, store `~/.orbit-crew-pref-r014`, checkouts
  `~/workspace/crew-pref-r014/{grok,sol}`.
- `grok`: Grok CLI 1.0.41, model `grok-4.7`, headless (`--prompt-file PROMPT.md`,
  `--always-approve`, web search off, memory off).
- `sol`: Codex CLI `exec`, model `gpt-6-sol`, reasoning effort `xhigh` (the `sol`
  crew's configured effort), sandbox `workspace-write` plus the isolated store.
- Operator: Claude (Opus 5.5) started both sessions with the bound prompt and did
  not intervene. Opus is on the menu.

### Deviations from R013

- **Session environment.** Each agent ran under a throwaway `HOME` holding only its
  login. Without it, Grok loaded the host's global agent instructions (which tell
  agents to search the live Orbit store first) and the Orbit crew-assignment
  skills, and Codex loaded an Orbit plugin hook and the live Orbit MCP server. Any
  of those could expose the live crew assignments this run is testing against.
  R013's session environment was not recorded.
- **Orbit 0.24.** `orbit init` takes `--machine-name` (was `--host-name`), and it
  seeds crews from the agents it detects, which here did not include the `system`
  sentinel; `setup.sh` now defines it (off the menu, `gpt-6-luna`).
- **Model versions.** Menu crew names are unchanged, but some point at newer models
  than on 2026-09-20 (`sol` is now GPT-6 Sol). Nothing is dispatched, so only the
  orchestrators' own models run.

## Result

Both sessions filed 18 tasks, all with a menu crew and a `crew_reason`, all
`proposed` ([artifacts/results.md](artifacts/results.md)). Grok ran 17m 26s,
Sol 4m 14s; both exited 0.

| Orchestrator | Own provider | Picked | Expected (n × menu share) | Lift |
|---|---|---|---|---|
| `grok` | grok (1/7) | 2/18 | 2.6 | 0.78 |
| `sol` | sol, luna, terra (3/7) | 9/18 | 7.7 | 1.17 |

Neither comes close to the lift its live rate would imply (about 4.4 for
`grok`, about 1.6 for `sol`). Both used all seven crews, with every crew
getting between one and four tasks: close to an even spread.

Reasons: Grok's describe the work ("security-boundary work", "a labeling
hazard") and never name a model. Sol's name the crew and attribute a strength
to it ("Sol is a strong fit for the core service boundary"); it gave itself 4
of its 11 hard tasks, all on core service or integration work. No reason in
either session mentions a provider.

## Limitations

- One feature, one session per orchestrator. Assignments within a session are not
  independent.
- Crew names encode the provider, and a written reason is required, as in R013.
- Different host, Orbit version and operator from R013, so the two runs are
  comparable in design, not identical in conditions.
- Reason codes are assigned by the operator, whose provider (Anthropic) is on the
  menu.

## Next

Still a pilot: one feature, one session each, scored only against the menu.
[R015](../R015-crew-preference-across-five-orchestrators-and-five-features/)
runs five orchestrators on five features (500 tasks) and compares each
orchestrator with the others on the same work. The near-even spread across
crews here and in R013 is worth checking there: a lift near 1 from an
orchestrator that deliberately balances work is not the same finding as one
from an orchestrator choosing freely.
