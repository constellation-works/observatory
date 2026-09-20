---
type: runbook
summary: Where every path came from — the four source repositories folded in, and the v1-to-v2 layout move.
tags: [operations, research]
paths: ["research/**", "_archive/**", "_lib/**", "docs/field-guide/**"]
related_features: [research-layout-v2]
related_artifacts: []
last_validated: 2026-09-20
---

# Migration

Nothing in this repository was written from scratch. This is the record of where
each path came from, so that `git log --follow` on a file is enough to understand
it.

## Stage 1 — folding four repositories in (2026-09-07)

Each source was added with `git subtree add`, so its history survives. All five
rows landed; the original repositories are no longer authoritative.

| source | landed as, today |
|---|---|
| principia, whole | `_archive/principia/` — the lock, its checker and its records |
| orrery sims | `research/R00*/code/<sim>/`, one research item per sim family |
| orrery apparatus (`lab/lib/web`, `vendor`, `templates`, `tools`, `gallery`) | `_lib/` |
| orrery catalogue, scripts and docs | `_archive/orrery/` |
| parallax, whole minus `.orbit/` and `.agents/` | `_archive/parallax/` |
| kaggle `<competition>/` | `research/R010-arc/`, `research/R011-rogii-wellbore-geology-prediction/`, `research/R012-stellar/` |
| astrolabe, whole | `_lib/astrolabe/`, with its notebooks at `notebooks/astrolabe/` |

## Stage 2 — research layout v2 (2026-09-20)

The v1 layout keyed one experiment across four trees — the Nebula lineage corpus,
a studies directory, an experiments directory and a JSON record store — joined by
a node id only Nebula's own CLI could allocate. v2 replaced all of it with four record kinds
and a short id, specified in
[docs/design/research-layout-v2/1_spec.md](../design/research-layout-v2/1_spec.md).

| was | is |
|---|---|
| the Nebula lineage corpus | `_archive/lineage/`, verbatim. Each node became a question, hypothesis, theory or research item, which cites it as its origin |
| `knowledgebase/studies/<domain>/<id>.md` | the matching research item's `README.md` |
| `knowledgebase/theory/` (principia's lock) | `_archive/principia/`, byte-for-byte, with one theory record per family citing into it |
| `experiments/<domain>/<id>/<sim>/` | `research/R###-slug/code/<sim>/` |
| `experiments/physics/physics-field-guide/` | `docs/field-guide/` — reference material, not a record |
| `experiments/physics/_lib/` | `_lib/` |
| `experiments/physics/_orrery/`, `experiments/economics/_parallax/` | `_archive/orrery/`, `_archive/parallax/` |
| `research/physics/<id>/records/` (orbit-research JSON) | `_archive/records/fput/`, read-only; the JSON record format is retired here |
| `_data/<domain>/<id>/manifest.json` | the item's own `data/manifest.json`; `_data/` now holds only datasets several items share |
| `_outputs/<domain>/<id>/` | the item's own `output/` |
| `lib/astrolabe/` | `_lib/astrolabe/` |
| per-experiment `manifest.json`, `experiments/_template/`, `check-layout.sh`, `new-experiment.sh` | `_archive/experiments/`, `_archive/scripts/` — replaced by record frontmatter and `_scripts/new.sh` |

What changed beyond moving files:

- **Nebula is gone.** No environment variable, no CLI verb, no lineage corpus in
  the live tree. `_scripts/check.py` fails if any of them reappears outside
  `_archive/` and the design records — it greps for the exact spellings, which is
  why this runbook does not write them out.
- **One checker.** `_scripts/check.py` replaced the corpus check, `check-layout.sh`,
  the study/experiment pairing check and `check-records`. principia's checker
  survives as `make check-archive`, read-only over `_archive/principia/`.
- **`_archive/orrery/lab/sims/<slug>`** are still symlinks, re-pointed at the
  research items that now hold the sims, so principia's frozen ledger links keep
  resolving through `--external-root`.
- **The gallery** is generated from `research/*/code/*/sim.json` into
  `_lib/gallery/` (`make gallery`). Field-guide chapters are reference material
  and are no longer gallery entries.

Frozen inputs were not rewritten: `research/R005-fput-recurrence-reproduction/code/protocol/*.json`
are digest-pinned protocols and still name their v1 paths, and each migrated sim's
own README is the frozen record of its run.
