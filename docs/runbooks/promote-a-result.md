---
type: runbook
summary: Turn a run's output into a study note and evidence on the node.
tags: [operations, research]
paths: ["experiments/**", "knowledgebase/**"]
related_features: [unified-research-platform]
related_artifacts: []
last_validated: 2026-09-07
---

# Promote a Result

Outputs are regenerable and never committed. A result only exists once it is
written down where the lineage can point at it.

## Write the study

Create `knowledgebase/studies/<domain>/<id>.md` from the template in
`knowledgebase/studies/README.md`. Include the figure (small PNG or SVG
committed beside it, under 500 KB), the numbers, and the paragraph on what is
shaky. Set `verdict` and `strength` honestly; `inconclusive` is a normal
outcome.

## Attach it to the node

```sh
neb evidence <id> --verdict undermines --strength strong \
  --source knowledgebase/studies/<domain>/<id>.md \
  --note "decay flattens after day 30; the half-life model over-predicts late decay" \
  --task DANI-10301
```

`neb check` verifies the source path exists. If the verdict is `undermines`,
the command echoes the kill condition so you can decide whether it fired.

## Move the node

```sh
neb status <id> refuted        # the kill condition fired
neb status <id> supported      # evidence with a supports verdict exists
```

Or refine instead: `neb new "<sharper claim>" --parent <id> --kill "..."`.

## Graduate

A supported node with a kill condition can move into the theory layer:

```sh
neb graduate <id> --to knowledgebase/theory/<doc>
```

Then file the claim in that document's registry under principia's policy.
