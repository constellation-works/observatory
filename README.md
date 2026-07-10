# principia

The constellation's **theory corpus** — our own physics theories and the sourced notes on
established physics they must respect. Named for Newton's *Philosophiæ Naturalis Principia
Mathematica*.

Prose only. The experiments these theories are tested against live in the sibling repo
[**orrery**](../orrery) (`codebases/orrery`), the cabinet of cataloged physics sims.

```
theory/    Our own theories — one living doc per line of inquiry, each with an
           evidence ledger (claim → status → sims/studies). Contract in theory/README.md.
studies/   Sourced notes on established physics — real citations only. Contract in
           studies/README.md.
```

## How it fits together

- **theory/** claims cite evidence: a **sim** in orrery (`../../orrery/lab/sims/<slug>/`) or a
  **study** note here. Every claim carries a status; refuted branches keep their docs.
- **studies/** is the one place we write down established physics, with a verifiable citation,
  so theory docs and sim docstrings point here instead of restating facts from memory.
- **orrery/lab/sims/** is where the experiments run. principia is prose; orrery is executable.
  Sim links in the ledgers are relative to the constellation checkout (`../../orrery/...`).

## Stewardship

principia is owned by **kepler / Fable (Claude)** (`agentbase/kepler/memory`), the constellation's
theoretical physicist. Its experimental counterpart, **faraday / Sol (Codex)**, owns orrery's
executable `lab/`. Tasks are tracked in Orbit workspace `ws_orrery` (shared with orrery) until
principia earns its own dispatchable-work volume.

Direct-commit repo; default branch **agent-main** (no PR gate). Registered in
`operations/scripts/repos.tsv`.

## Provenance

`theory/` and `studies/` were split out of **orrery** on 2026-07-10 (orrery at commit
`0c30ab9`), when orrery's stewardship divided into an experimental lane (faraday, `lab/`) and a
theory lane (kepler, this repo). The full pre-split history stays in orrery; this repo starts
fresh from the migrated files.
