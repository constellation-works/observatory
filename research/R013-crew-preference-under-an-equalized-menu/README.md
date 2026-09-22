---
id: R013
title: Crew preference under an equalized menu
status: done
tags: [social, orbit, agents, crew-selection]
derived_from: [H008]
created: 2026-09-20
updated: 2026-09-21
tests: [H008]
---

# R013 — Crew preference under an equalized menu

Origin: `operations/research/crew-preference-experiment` in constellation, run
2026-09-20 and ported here as a research item. A planning-only mock: three
orchestrators (`gemini-flash`, `opus`, `astra`) break the same feature into
Orbit tasks and assign implementer crews from a closed menu. Nothing is
dispatched.

| File | What |
|---|---|
| [code/protocol.md](code/protocol.md) | Pre-registered hypothesis, isolation, scoring rules, decision rules |
| [code/feature.md](code/feature.md) | Stimulus: a visual change explorer over orbit-graph |
| [code/prompt.md](code/prompt.md) | Orchestrator brief with `{{…}}` bindings |
| [code/seed/](code/seed/) | The companion-UI checkout every workspace starts from |
| [code/setup.sh](code/setup.sh) | Isolated Orbit root + three workspaces |
| [code/score.py](code/score.py) | Rollup of the store into `artifacts/results.md` |
| [artifacts/results.md](artifacts/results.md) | The 2026-09-20 run: compliance, heatmaps, lift, full inventory |

## Question

When every listed crew is available, do orchestrators still assign
implementers from their own provider family? Tests [H008](../../hypotheses/H008-orchestrators-assign-implementers-from-their-own-provider-family.md).

The live Orbit store, counted per orchestrator, shows own-family rates of
roughly 50–68%:

| Orchestrator | Claude (opus/sonnet/fable) | Codex (sol/luna/terra/astra) | Grok | Gemini | system/none |
|---|---|---|---|---|---|
| astra | 63 (22%) | 180 (63%) | 34 (12%) | 4 | 3 |
| opus | 61 (50%) | 29 (24%) | 4 (3%) | 13 (11%) | 14 |
| sol | 11 (18%) | 41 (68%) | 7 (12%) | 0 | 1 |
| grok | 5 (13%) | 9 (24%) | 24 (63%) | 0 | 0 |

That store is not a fair choice set: providers drop out on usage limits,
`workflow.default_crew` and complexity pools fill blanks, the task mix differs
per orchestrator, and the samples are badly unbalanced (astra 284 vs terra 4).
This run holds the feature, the menu and availability constant so the
own-family rate can be compared to a menu-adjusted null.

## Method

- **Store.** An isolated `orbit --root ~/.orbit-crew-pref-exp` with
  `default_crew = "system"`, no routines, no auto-tasks, empty complexity
  pools; only menu crews plus `system` and `astra` (orchestrator attribution)
  in `config.toml`. `code/setup.sh` builds it and never touches `~/.orbit`.
- **Workspaces.** Three, one per orchestrator, each a fresh checkout of
  `code/seed/` at the same commit, so no session sees another's crew fields.
- **Stimulus.** The same `feature.md` in every checkout.
- **Action.** File tasks with an explicit `crew` and a one-line `crew_reason`
  comment; stay in `proposed`; no dispatch, so availability cannot re-enter.
- **Menu.** Closed list of seven: `sol`, `grok`, `gemini-flash`, `opus`,
  `sonnet`, `luna`, `terra`. Blank or off-menu crews are noncompliance and are
  dropped from the preference denominators. Family rollup: Claude = opus,
  sonnet; Codex = sol, luna, terra; Grok = grok; Gemini = gemini-flash. astra
  is Codex-family and not on the menu, so it cannot pick itself; opus and
  gemini-flash can, and that is counted.
- **Prompt.** Identical text (`code/prompt.md`); only the orchestrator crew
  name and workspace selector differ. It does not mention homophily, this
  hypothesis, or "choose freely".
- **Primary number.** Pre-registered lift = observed own-family share ÷ menu
  share. Menu shares: astra 3/7 ≈ 43%, opus 2/7 ≈ 29%, gemini-flash 1/7 ≈ 14%.
  Lift > 1 is homophily after availability is equalized. Secondary: one-crew
  dominance (modal crew share) and qualitative codes on `crew_reason`.
- **Scoring.** `python3 code/score.py` reads every task in the three workspaces
  through `orbit.task.list` / `orbit.task.show` and writes
  `artifacts/results.md`.

## Result

n = 47 valid assignments (astra 14, opus 19, gemini-flash 14); compliance was
100% in every session — no blank or off-menu crew.

| Orchestrator | Own family | Observed | Menu share | Lift | n |
|---|---|---|---|---|---|
| astra | codex | 43% | 43% | 1.00 | 14 |
| opus | claude | 26% | 29% | 0.92 | 19 |
| gemini-flash | gemini | 21% | 14% | 1.50 | 14 |

Astra matches the Codex menu share exactly. Opus lands slightly *under* the
Claude share and gives Codex the plurality (53%). Gemini-flash is the one lift
above 1, from three self-assignments out of 14 (two expected under the null).

No one-crew dump: modal share is 21% in every row, and all three orchestrators
used every menu crew. Every task carried a `crew_reason`; almost all are
skill-match stereotypes (opus for epistemics/ambiguity, sol for
subprocess/security, terra for fixtures and export breadth, gemini-flash for
fast UI, grok for adversarial checks), a few are cost/speed or path
dependence. None mention provider or family.

Read against the pre-registered decision rules in `code/protocol.md`: this is
the "lift near 1, crews spread across families" outcome. The live 50–68%
own-family rates are not reproduced once availability, defaults and work mix
are held constant. Full tables and the task inventory are in
[artifacts/results.md](artifacts/results.md).

## Limitations

- One feature, three sessions, n = 47. A pilot, not a census; it cannot rule
  out a smaller family taste in the live drain, where cost, rate limits,
  `default_crew` and work mix still operate.
- Crew names encode family (`opus`, `sol`, `grok`), so the in-group is visible.
- Requiring a written `crew_reason` and listing seven named crews may itself
  have pushed orchestrators to spread (accountability).
- Menu family sizes are unequal by construction, so raw own-family percentages
  are not comparable across orchestrators; only lift is.
- Prior beliefs about model skill are a competing explanation, not a bias to
  remove; the reason codes are how the two are told apart, and they were coded
  after freeze by the same person who ran the sessions.
- The filled store lives outside git (`data/manifest.json`); the committed
  evidence is the scored rollup, not the raw task records.

## Next

- Re-run with the same store and a second, unrelated feature to see whether
  gemini-flash's 1.50 holds or regresses to the null.
- Add `sol` and `grok` as orchestrators, so every family in the live table has
  a menu-adjusted counterpart.
- A variant with anonymised crew labels (`crew-a` … `crew-g` mapped to real
  crews behind the adapter) would separate "same logo" from skill stereotypes
  directly, at the cost of the stereotypes being the thing the reasons encode.
- Descriptive follow-up allowed by the protocol: a complexity × crew table over
  the existing 47 assignments.
