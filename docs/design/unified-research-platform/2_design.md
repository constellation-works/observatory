---
title: Unified Research Platform — Design
owner: claude
last_updated: 2026-09-07
last_validated: 2026-09-07
status: Superseded
feature: unified-research-platform
doc_role: design
type: design
summary: The layout, the node-id join, the data boundary, the theory lock, environments and Orbit registration.
tags: [unified-research-platform]
paths: ["experiments/**", "knowledgebase/**", "_scripts/**"]
related_features: [unified-research-platform]
related_artifacts: []
superseded_by: docs/design/research-layout-v2/1_spec.md
---

# Unified Research Platform — Design

## The node id is the join

Every experiment directory, every study and every evidence source is named by
the nebula node it concerns. This is the single convention that makes the
platform one thing rather than four things in one folder. `neb show <id>`
names the experiment; `manifest.json` names the node; the study sits at the same
id; `neb evidence --source knowledgebase/studies/<domain>/<id>.md` is a
relative path rule 14 checks. `_scripts/new-experiment.sh` refuses an id that
is not a node, and `check-layout.sh` fails on a study with no experiment.

Kaggle competitions are the one exception: they are projects, not hypotheses,
so their id is the competition slug and the tracking node references it.

## Data never enters git

`_data/` and `_outputs/` are gitignored except for `manifest.json` and README
files, enforced by both `.gitignore` and `check-layout.sh`. Parallax alone
carries 2.1 GB of data; committing any of it makes the repository unusable.
A manifest records source, hash, size and the fetch command, which is enough to
reproduce. Outputs are regenerable by definition; what matters is promoted into
a study.

## The corpus lives here

Nebula's tool repository is public, so the corpus stayed out of it. This
repository is private and holds the personal corpus at
`knowledgebase/lineage/`, which turns evidence sources into checkable relative
paths. The work corpus is a separate corpus elsewhere. `make setup` exports
`NEBULA_ROOT` to the lineage directory.

## The theory lock is kept

Principia's value was never the prose alone; it was `policy.md`, the claim
registries, the gates and the refuted wall, machine-checked. That moves intact
to `knowledgebase/theory/` whole, checker included (`scripts/check-theory.py`
and the record scripts stay where the lock expects them). `_scripts/check-theory.sh`
runs it with the orrery root wired, and `make check-theory` / `make check-records`
call it. Nebula sits upstream and graduates into it.

Principia's `studies/` stays inside the lock: those are sourced notes on
established physics that claims cite, not experiment results. Observatory's
`knowledgebase/studies/` is the latter, keyed by node id.

## Sims sit under their node; the apparatus under _lib

An interactive or numeric sim is evidence, so it lives at
`experiments/physics/<node-id>/<slug>/` with a `sim.json`, and is attached to
the node with `neb evidence`. What every sim shares (web harness, vendored
three.js, templates, scaffolding, the generated gallery) lives in
`experiments/physics/_lib/`; sims import it as `../../_lib/web/…`, so a sim's
depth is part of the contract. Underscore directories are never experiments.

## Shared instruments live in lib/

Code that experiments import rather than own (astrolabe's catalog, cross-match
and provenance) sits in `lib/<name>/` as a uv workspace member. It is not keyed
by a node because it serves many; its data root is `_data/physics/<name>/`.

## One environment

A root `pyproject.toml` managed by uv, with extras for notebooks, spark and ML.
Per-experiment environments are the exception and must say why. Notebooks are
committed with outputs stripped by a pre-commit hook.

## One Orbit workspace

The repository registers as a single workspace with one backlog and one drain.
Tasks carry a domain tag so reviews and drains can filter. Routines that review
code should be tuned by path: a notebook is not held to the standard of a
checker script.

## Migration

`git subtree add --prefix=<dest> <remote> <branch>` per source, so history is
preserved. Landing order and mapping are in
[docs/runbooks/migration.md](../../runbooks/migration.md). A source's original
repository stays authoritative until the runbook marks it landed.
