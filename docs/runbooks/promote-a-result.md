---
type: runbook
summary: Turn a run into a written result and an assessment on the hypothesis it tested.
tags: [operations, research]
paths: ["research/**", "hypotheses/**", "theories/**"]
related_features: [research-layout-v2]
related_artifacts: []
last_validated: 2026-09-20
---

# Promote a result

Outputs are regenerable and never committed. A result exists once it is written
in the item's README and recorded as an assessment on the hypothesis it tested.

## Write the result

Fill in the research item's own README — `## Result`, then `## Limitations`, then
`## Next`. Give the numbers, not an impression. If a figure carries the argument,
promote that one figure into `artifacts/` (small, and cited from the README);
everything else stays in `output/` and regenerates.

Set `status: done` when the run is finished, or `abandoned` if it was stopped.
`done` means the run completed, not that it came out the way you hoped.

## Assess the hypothesis

Append one entry to the hypothesis's `assessments` — never edit an existing one:

```yaml
assessments:
  - date: 2026-09-21
    research: R013
    revision: 1
    verdict: inconclusive    # supports | refutes | inconclusive
    strength: suggestive     # anecdote | suggestive | strong
    note: control run failed; see R013 README §Limitations
```

`revision` is the statement revision the verdict is about. If the statement
itself changed, bump the hypothesis's `revision` first: an assessment against an
older revision stays in the log and does not carry to the current statement.

**Execution success is not support.** A `done` item with a `refutes` or
`inconclusive` verdict is a complete, valid result, and `inconclusive` is a normal
outcome. The checker warns if a `done` item leaves no assessment on any hypothesis
it tests — that warning is the one to act on.

## Move the status

`status` on the hypothesis is yours to set — `open`, `supported`, `refuted`,
`inconclusive` or `dropped`. The checker warns when it disagrees with the latest
assessment and never overwrites it. If the statement needs sharpening instead,
bump `revision` and say what changed in the body, or write a new hypothesis with
`derived_from` pointing at this one.

## Graduate

A supported hypothesis can become a theory. That is a person's decision and is
not automated:

```sh
make new KIND=T TITLE="What the surviving account says"
```

Set `claims` to the hypothesis ids it rests on and `supersedes` to the theories it
replaces. Theories that cite into principia's archived lock
(`_archive/principia/`) point at it and never restate or overrule a claim it owns.

## Check it

```sh
make check
```
