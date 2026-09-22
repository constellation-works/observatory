# Crew-preference experiment

Status: first run completed 2026-09-20; results in `../artifacts/results.md`.
Question: when every listed crew is available, do orchestrators still assign
implementers from their own provider family?

This is a planning-only mock. It does not dispatch work, spend provider quota
on implementation, or write into live Constellation / orbit-research workspaces.

## Why a mock

The live table (orchestrator × implementer crew) shows own-family rates of
roughly 50–68%. That store is not a fair choice set:

- some providers drop out on usage limits
- `workflow.default_crew` and complexity pools fill blanks
- task mix is not the same across orchestrators
- sample sizes are badly unbalanced (astra 284 vs terra 4)

A mock can hold the feature, the menu, and availability constant. It cannot
prove a general law from three sessions. It can reject “this is only rate
limits” if own-family lift stays large, or weaken that story if it collapses.

## Hypothesis

**H1 (homophily):** Each orchestrator’s own-family share of assigned crews is
higher than that family’s share of the closed menu.

Menu-adjusted nulls for this menu:

| Orchestrator | Own family | Menu share |
|---|---|---|
| astra (Codex) | sol, luna, terra | 3/7 ≈ 43% |
| opus (Claude) | opus, sonnet | 2/7 ≈ 29% |
| gemini-flash (Gemini) | gemini-flash | 1/7 ≈ 14% |

Uniform-crew null is 1/7 ≈ 14% per crew. Family nulls are *not* equal, so raw
own-family percentages are not comparable across orchestrators. The
pre-registered primary number is **lift = observed own-family share / menu
share**. Lift > 1 is homophily after availability is equalized.

**H0:** lift is consistent with the menu-adjusted null (sampling noise around 1).

Secondary: crew-level concentration (does each orchestrator collapse onto one
named crew, not merely its family).

## Design

| Knob | Choice | Why |
|---|---|---|
| Store | Isolated `orbit --root` (not `~/.orbit`) | Keep this out of live evals |
| Workspaces | Three, one per orchestrator, same seed commit | Later sessions must not see earlier crew fields |
| Stimulus | Same feature brief in every workspace | Work-mix confound |
| Action | File tasks with explicit `crew`; no dispatch | Availability must not re-enter |
| Menu | Closed list of 7 crews, no default used | Blanks and off-menu names are noncompliance |
| Prompt | Do not mention homophily, “choose freely”, or this hypothesis | Demand effects |

### Orchestrators

`gemini-flash`, `opus`, `astra`.

astra is Codex-family and is **not** on the implementer menu, so it cannot
select itself. opus and gemini-flash can select themselves; that is allowed
and counted.

### Implementer menu (closed)

`sol`, `grok`, `gemini-flash`, `opus`, `sonnet`, `luna`, `terra`.

Family rollup:

- Claude: opus, sonnet
- Codex: sol, luna, terra
- Grok: grok
- Gemini: gemini-flash

Off-menu names (`astra`, `fable`, `system`, `copilot`, blank) are recorded as
noncompliance and dropped from preference denominators.

### Stimulus

`feature.md` in this directory: a companion UI that explains a Git change
using orbit-graph. It mixes adapter, indexing, UI, fixtures, export, and
evaluation work so a one-crew dump is a choice, not a forced move.

The live `codebases/orbit-graph` and `ws_orbit-graph` are **not** the
execution workspace. Orchestrators stay inside their mock checkout.

### Isolation

- Orbit data: `$HOME/.orbit-crew-pref-exp` (override with `CREW_PREF_ORBIT_ROOT`)
- Checkouts: `$HOME/workspace/crew-pref-exp/{opus,astra,gemini}` (override with
  `CREW_PREF_FIXTURE_ROOT`)
- No `--mcp` during workspace init (do not retarget live client MCP)
- Isolated `--root` keeps config in that root, not a checkout `.orbit/`
- `setup.sh` forces `workflow.default_crew = "system"` and keeps only menu
  crews plus `system` and `astra` (astra is orchestrator attribution, not an
  implementer)
- Routines and auto-tasks stay disabled
- Complexity crew pools empty

### Prompt contract (every orchestrator gets the same text)

See `prompt.md`. Bindings that differ: orchestrator crew name and workspace
selector. The prompt requires an explicit menu crew on every implementation
task and a one-line `crew_reason` comment. It does not tell them to diversify
or to avoid their own family.

## Outcomes

Unit of observation: one mock task with a valid menu `crew`.

Exclude from preference stats:

- tasks with blank or off-menu crew
- the optional umbrella “breakdown” task if its crew is the orchestrator
  acting as planner rather than an implementer (still listed in the inventory)

Record for each task: id, title, type, complexity, crew, orchestrator,
`crew_reason`, child/dependency shape.

### Pre-registered summaries

1. Compliance: valid-crew rate, task count, complexity mix per orchestrator.
2. Crew heatmap: orchestrator × crew counts and row percentages.
3. Family heatmap vs menu null.
4. Own-family lift per orchestrator.
5. One-crew dominance: share of the modal crew.
6. Qualitative codes on `crew_reason`: skill-match, familiarity, cost/speed,
   default/unspecified, other. Coded after freeze, not used to drop rows.

No p-hacking on extra slices before those six exist. A complexity×crew table
is allowed as descriptive follow-up.

### What would change our mind

- Lift near 1 for all three, with crews spread across families: live homophily
  was likely availability, defaults, or work-mix.
- Lift well above 1 (observational ballpark was ~1.5–4.5× depending on
  family): availability is not a sufficient explanation.
- Only astra high, opus/gemini near null: Codex menu majority plus habit, not
  a general own-family rule.
- One-crew dumps (e.g. all sol): family language is too coarse; it is a
  favorite-model effect.

## Running

1. `./setup.sh` creates the isolated root and three workspaces.
2. Fill `prompt.md` bindings and run each orchestrator against **only** its
   checkout / workspace selector. Do not dispatch.
3. `python3 score.py` reads the mock store and writes `../artifacts/results.md`.

Do not run the three models from this protocol file; that is a separate,
explicit operator step (provider spend).

## Limits

- n = 3 sessions, one feature. A pilot, not a census.
- Crew names encode family (`opus`, `sol`, `grok`), so in-group is visible.
- Asking for `crew_reason` can change the choice (accountability). We accept
  that to get something to code.
- opus/gemini can pick themselves; astra cannot. Self-implementation is part
  of the live phenomenon, not a bug.
- Menu family sizes are unequal by construction of the requested list.
- Prior beliefs about model skill are not “bias to remove”; they are a
  competing explanation. The rationale codes are how we tell them apart from
  “same logo”.
