---
type: runbook
summary: Start a research item: allocate the id, write the question, scaffold, fetch, run.
tags: [operations, research]
paths: ["research/**", "questions/**", "hypotheses/**"]
related_features: [research-layout-v2]
related_artifacts: []
last_validated: 2026-09-20
---

# New research item

A research item tests one hypothesis. If there is no hypothesis yet, that comes
first — and if the idea is not sharp enough to be a claim, capture it as a
question and stop there.

```sh
make new KIND=Q TITLE="Does ranking decay look like a half-life"
make new KIND=H TITLE="Ranking decay rate falls with age at every horizon"
```

Each prints the file it created. Fill in the body, set `tags`, and point
`derived_from` at the question. The hypothesis is worth writing only if you can
say in it what would move it to `refuted`.

## Scaffold

```sh
make new KIND=R TITLE="Ranking decay against a control period"
```

This creates `research/R###-slug/` with the README (frontmatter plus the five
sections), `data/manifest.json`, and empty `code/` and `artifacts/`. Set `tests`
to the hypothesis ids and `derived_from` to whatever it descends from. For a
physics sim, scaffold inside the item:

```sh
_lib/tools/new-sim.sh R013 my-sim --kind web   # or --kind py
```

## Data

Fetch into the item's own `data/` and describe every input in
`data/manifest.json`: `{name, source, sha256, size, fetch}`. Commit the manifest,
never the bytes. A dataset several items share lives in `_data/<name>/` with its
own manifest, referenced as `{"name": "...", "shared": "_data/<name>"}`. An item
that consumes nothing declares `{"inputs": []}` and says so in `note`.

## Run

Keep the entry point under `code/`. Run products go to the item's `output/`,
which is ignored. Record the driving Orbit task in the frontmatter if there is
one:

```yaml
orbit: {task: ORB-12636, run: jrun-20260920-0346-c2}
```

Set `status: running` while it runs — the checker warns if a `running` item goes
30 days without an update.

## When it has run

Write the result up and assess the hypothesis:
[promote-a-result.md](promote-a-result.md).
