# studies

One note per experiment result: `studies/<domain>/<node-id>.md`. This is what
`neb evidence --source` points at, and `neb check` verifies the path exists.

A study says what was run, what came out, which way it cuts on the node's kill
condition, and what is shaky about it. Include the figure; the raw outputs stay
in `_outputs/` and are regenerable.

Principia's `studies/` (sourced notes on established physics) lands here under
`studies/physics/` with its history.

Template:

```markdown
---
node: <node-id>
domain: <domain>
experiment: experiments/<domain>/<node-id>
ran_on: YYYY-MM-DD
verdict: supports | undermines | inconclusive
strength: decisive | strong | suggestive
---

# <title>

## What was run
## What came out
## What is shaky
## Next
```
