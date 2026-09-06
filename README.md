# principia

The constellation's **theory corpus** — our own physics theories and the sourced notes on
established physics they must respect. Named for Newton's *Philosophiæ Naturalis Principia
Mathematica*.

Prose only. The experiments these theories are tested against live in the sibling repo
[**orrery**](../orrery) (`codebases/orrery`), the cabinet of cataloged physics sims.

```
policy.md  Research procedure. Enforced by scripts/check-theory.py.
ledger.md  Generated rollup of every claim, grouped by verdict. Do not hand-edit.
theory/    One directory per theory (hub README, claims.json, evidence ledger, related, open questions).
gates/     Live fronts / owed objects. New work starts with a gate card.
schema/    Field docs and the refuted wall.
studies/   Sourced notes on established physics. Contract in studies/README.md.
scripts/   check-theory.py — run before landing theory changes.
```

## How it fits together

- **theory/** claims cite evidence: a **sim** in orrery (`../../../orrery/lab/sims/<slug>/`
  from a theory file) or a **study** note here. Every claim lives in
  `theory/<slug>/claims.json` (kind, status, kill, control) with a matching
  `evidence-ledger.md` table; refuted branches keep their docs. New work is a `gates/` card.
- **studies/** is the one place we write down established physics, with a verifiable citation,
  so theory docs and sim docstrings point here instead of restating facts from memory.
- **orrery/lab/sims/** is where the experiments run. principia is prose; orrery is executable.
  Sim links in the ledgers are relative to the constellation checkout (`../../orrery/...`).

## Checking an isolated worktree

The [wide-binary migration pilot](research/wide-binary/README.md) uses immutable
orbit-research v1 records with checked compatibility views. Install the exact
environment from `requirements-research.txt` before running the whole-corpus checker;
the linked guide includes record validation, migration reproduction and rollback.
Only this pilot changes authority; all other families keep their existing contract.

`scripts/check-theory.py` keeps links inside the candidate worktree local to that candidate.
For established relative links into sibling `orrery`, it derives the standard sibling root from
Git's common-worktree metadata. This lets an isolated Git worktree validate against the checkout
that owns it without creating symlinks or modifying either repo.

When that checkout is elsewhere (or deliberately needs a different root), pass an explicit
mapping. Explicit mappings take precedence over Git metadata:

```sh
python3 scripts/check-theory.py --external-root orrery=/absolute/path/to/orrery
```

The mapping name must be a simple repository name. A missing configured checkout is an error
labelled as unavailable; a missing path inside an available checkout remains a failing link with
its resolved path reported. Links that escape the candidate without a configured repository root,
or escape a mapped repository, are rejected.

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
