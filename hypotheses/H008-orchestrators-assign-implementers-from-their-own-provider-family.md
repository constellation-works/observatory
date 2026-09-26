---
id: H008
title: Orchestrators assign implementers from their own provider family
status: refuted
tags: [social, orbit, agents, crew-selection]
derived_from: []
created: 2026-09-20
updated: 2026-09-26
revision: 1
assessments:
  - date: 2026-09-20
    research: R013
    revision: 1
    verdict: refutes
    strength: suggestive
    note: >-
      With the feature, a closed seven-crew menu and availability held constant, own-family
      lift was 1.00 (astra), 0.92 (opus) and 1.50 (gemini-flash, three self-picks of 14).
      No one-crew dump; every orchestrator used every menu crew; no crew_reason mentions
      provider. The live 50–68% own-family rates are not reproduced. One feature, three
      sessions, n = 47.
  - date: 2026-09-26
    research: R014
    revision: 1
    verdict: refutes
    strength: suggestive
    note: >-
      R013's design with the two live-table orchestrators it did not run: own-provider lift
      0.78 (grok, 2 of 18; 2.6 expected) and 1.17 (sol, 9 of 18; 7.7 expected), against
      about 4.4 and 1.6 implied by the live rates. Both spread work nearly evenly over all
      seven crews. Same single feature, one session each, n = 36; different host, Orbit
      version and operator from R013.
---

# H008 — Orchestrators assign implementers from their own provider family

Origin: the live Orbit store, counted orchestrator × implementer crew, shows
own-family shares of 50–68% (astra 63% Codex, opus 50% Claude, sol 68% Codex,
grok 63% Grok). Stated here as the claim the mock in R013 was pre-registered
against; the confounds that made the live table unfair are listed in R013.

## The claim

Each orchestrator's own-family share of assigned implementer crews is higher
than that family's share of the closed crew menu, when every crew on the menu
is available and no default fills blanks. Primary number: lift = observed
own-family share ÷ menu share; the claim is lift > 1 for each orchestrator.

Family rollup: Claude = opus, sonnet; Codex = sol, luna, terra, astra;
Grok = grok; Gemini = gemini-flash.

## What would refute it

Lift near 1 for every orchestrator with crews spread across families, under a
design that holds the feature, the menu and availability constant. That is
what R013 found for three orchestrators on one feature. The claim would be
revived by a lift well above 1 on a second feature, or with anonymised crew
labels that hide the family.
