---
type: runbook
summary: Fold orrery, principia, parallax and kaggle into observatory with history; landing order, mapping, and what marks a source landed.
tags: [operations, research]
paths: ["experiments/**", "knowledgebase/**"]
related_features: [unified-research-platform]
related_artifacts: []
last_validated: 2026-09-07
---

# Migration

Each source is added with `git subtree add` so its history survives. The
original repository stays authoritative until its row below says landed.

## Mapping

| source | lands at | notes |
|---|---|---|
| principia, whole | `knowledgebase/theory/` | the lock, checker and records included; `_scripts/check-theory.sh` wraps `scripts/check-theory.py` |
| principia `studies/` | stays at `knowledgebase/theory/studies/` | literature notes claims cite, not results; see decisions |
| orrery, whole | `experiments/physics/_orrery/` (staging), then per-node directories as each sim family is tied to a node | `research/catalog` stays the authoritative record; `scripts/research_records.py` learned to run as a subtree (clone the enclosing repo, select its own files, pin repository identity explicitly). orrery is a uv workspace member so `uv run` py sims resolve |
| parallax `src/`, `notebooks/`, `docs/` | `experiments/economics/_parallax/` then per-node | `data/` (2.1 GB) is **not** migrated; write manifests |
| kaggle `<competition>/` | `experiments/kaggle/<competition>/` | competition slug is the id; tracked `results/` and `submissions/` moved out of git to `_outputs/kaggle/<slug>/` (history keeps them); `data/README.md` → `data-dictionary.md` |
| nebula personal corpus | `knowledgebase/lineage/` | `neb init` here; `~/.nebula` retired after |

## Procedure per source

```sh
git remote add <src> <url>
git fetch <src>
git subtree add --prefix=<dest> <src> <branch>
```

Then, in one follow-up commit: move files into the mapping above, fix paths in
Makefiles and docs, add `manifest.json` where data was, run `make check`. Only
when `make check` is green does the row flip to landed, and the source
repository gets an archive note in its README pointing here.

## Order

1. principia — smallest, and the lock is needed by `make check-theory`.
2. kaggle — cleanest mapping.
3. orrery — sims need node ids; file a node per sim family first.
4. parallax — largest; data manifests before anything else.

## Status

| source | status | landed on |
|---|---|---|
| principia | landed | 2026-09-07 |
| kaggle | landed | 2026-09-07 |
| orrery | landed (staging) | 2026-09-07 |
| parallax | pending | |
