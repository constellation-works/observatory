---
type: runbook
summary: Fold orrery, principia, astrolabe, parallax and kaggle into observatory with history; landing order, mapping, and what marks a source landed.
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
| orrery sims | `experiments/physics/<node-id>/<slug>/`, one node per orrery family (8 nodes, 39 sims) | each sim is `neb evidence` on its node with a verdict derived from the principia claims that cite it |
| orrery apparatus (`lab/lib/web`, `vendor`, `templates`, `tools`, `gallery`) | `experiments/physics/_lib/` | sims import `../../_lib/web/…`; `make serve`, `make gallery`, `_lib/tools/new-sim.sh <node> <slug>` |
| orrery `research/catalog`, `scripts/`, `docs/`, `lab/lib/py/orrery` | stay in `experiments/physics/_orrery/` | frozen historical record; `lab/sims/<slug>` are symlinks into the node directories so principia's frozen ledger links still resolve through `--external-root`. The live-drift `research_records.py check` and its tests are retired as of observatory commit 707d27e (last commit where the catalog matched the live tree); orrery stays a uv workspace member for the `orrery` package |
| parallax, whole minus `.orbit/` and `.agents/` | `experiments/economics/_parallax/` (staging) then per-node | uv workspace member; `data/<program>/README.md` dictionaries stay (parallax's conventions tests check them); the 2.1 GB of untracked data moved to `_data/economics/_parallax/`, with `data/<program>/{raw,processed}` symlinks so `Path("data")` keeps working from the staging dir; `deploy/` kept as the record of the dk-server-1 capture services, which keep running from the box checkout. Four tests import a `parallax.consumer_goods` package absent from the Mac checkout's history (it had no remote configured), ignored in pytest until reconciled with the box |
| kaggle `<competition>/` | `experiments/kaggle/<competition>/` | competition slug is the id; tracked `results/` and `submissions/` moved out of git to `_outputs/kaggle/<slug>/` (history keeps them); `data/README.md` → `data-dictionary.md` |
| astrolabe, whole | `lib/astrolabe/` | reusable library + CLI, uv workspace member; `ASTROLABE_DATA_DIR` → `_data/physics/astrolabe/` (69 MB copied from the untracked `data/`); provenance accepts a tracked subtree as its owning checkout |
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
3. orrery — sims need node ids; one node per sim family (done).
4. parallax — largest; data manifests before anything else.

## Status

| source | status | landed on |
|---|---|---|
| principia | landed | 2026-09-07 |
| kaggle | landed | 2026-09-07 |
| orrery | landed, sims per node | 2026-09-07 |
| astrolabe | landed | 2026-09-07 |
| parallax | landed (staging; consumer-goods tests orphaned) | 2026-09-07 |
