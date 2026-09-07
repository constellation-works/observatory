---
type: runbook
summary: Start an experiment from a nebula node: scaffold, manifest, data, run.
tags: [operations, research]
paths: ["experiments/**", "knowledgebase/**"]
related_features: [unified-research-platform]
related_artifacts: []
last_validated: 2026-09-07
---

# New Experiment

An experiment tests one node. If there is no node yet, that comes first:

```sh
neb capture "decay looks like a half-life, not a cliff"
neb promote <entry> --title "Ranking decay half-life" --domain economics
neb sharpen ranking-decay-half-life --kill "decay rate does not fall with age at any horizon"
```

## Scaffold

```sh
make experiment DOMAIN=economics ID=ranking-decay-half-life
```

This creates `experiments/economics/ranking-decay-half-life/` with a README and
`manifest.json`, plus matching directories under `_data/` and `_outputs/`. It
refuses an id that is not a node.

## Data

Fetch into `_data/<domain>/<id>/` and write `manifest.json` beside it: source,
fetch command, file hashes. Commit the manifest, never the files. Reference the
manifest path from the experiment's `manifest.json` under `data`.

## Run

Keep the entry point at `run.py` or a notebook named in the README. Outputs go
to `_outputs/<domain>/<id>/`. Record the Orbit task if one drives the work:

```sh
neb task ranking-decay-half-life DANI-10301 --why "run decay against a control period"
```

## When it has run

Promote the result: [promote-a-result.md](promote-a-result.md).
