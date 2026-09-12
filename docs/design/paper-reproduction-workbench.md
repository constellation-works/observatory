---
title: Paper reproduction and interactive physics field guide
owner: observatory
last_updated: 2026-09-12
last_validated: 2026-09-12
status: Accepted
feature: paper-reproduction-workbench
doc_role: design
type: design
summary: Contracts for a reproducible LA-1940 figure workbench and three browser-based physics chapters.
tags: [physics, research, paper-reproduction, field-guide]
paths: ["experiments/physics/fput-recurrence-reproduction/**", "experiments/physics/physics-field-guide/**", "_lib/web/**", "_scripts/export-field-guide.sh"]
related_features: [unified-research-platform]
related_artifacts: []
---

# Paper reproduction and interactive physics field guide

This document freezes the integration boundaries for the LA-1940 Fig. 1
reproduction and the later three-chapter field guide. Milestone 1 creates
records and contracts; it does not implement `run.py`, the integrator, or any
chapter.

## Repository layout

The experiment and study join on the Nebula node id. The PDF and generated
outputs remain outside Git according to the observatory data boundary.

```text
experiments/physics/fput-recurrence-reproduction/
  README.md
  manifest.json
  protocol/v1.json
  protocol/v1.md
  protocol/v2.json
  protocol/v2.md
  reference/fig1-digitized.csv
  reference/README.md
  reference/la-1940-fig1.png
experiments/physics/physics-field-guide/
  README.md
_data/physics/fput-recurrence-reproduction/manifest.json
_outputs/physics/fput-recurrence-reproduction/<run-id>/
knowledgebase/studies/physics/fput-recurrence-reproduction.md
```

The reference image is a credited crop of the public-domain OSTI/LANL scan.
The CSV is digitization evidence with uncertainty, not an original data dump.

## Reproduction runner contract

The future runner is `experiments/physics/fput-recurrence-reproduction/run.py`.
It has a small, scriptable CLI:

| invocation | contract |
|---|---|
| `run.py baseline` | Load the registered protocol (v2 by default; `--protocol v1` reruns the original for the record), execute the deterministic baseline, write a new completed/failed/inconclusive run directory, and register no exploratory parameters. |
| `run.py explore --set key=value [--set key=value ...]` | Execute a run labelled `kind: exploratory`; validate keys against the protocol; never overwrite or relabel the registered baseline. The alternative `dt=1/8` interpretation is allowed only here and must be named in the run metadata. |
| `run.py report <run-directory>` | Render the run's study-report HTML from `metrics.json`, `run.json`, logs and the declared reference material. It does not recompute or mutate the run. |
| `run.py export <run-directory>` | Create the allowlisted evidence tarball described below, with relative archive names only and no `_data` payload. |

Exit codes are stable: `0` means scientific status `completed`; `10` means
scientific status `inconclusive`; `20` means scientific status `failed`
(the distinct `FAILED` state, including a failed control or a declared discrepancy); `2` means CLI or
input usage error; and `3` means an infrastructure error such as timeout or
missing required input. A failed scientific result is distinct from an
inconclusive result in both `run.json` and the process exit code. Every
invocation writes `log.txt`, including failures before the first numerical
sample.

## Run-directory contract

Each run is under
`_outputs/physics/fput-recurrence-reproduction/<run-id>/`. The directory is
regenerable and ignored by Git. It contains:

| file | required content |
|---|---|
| `run.json` | Protocol version, `kind` (`baseline` or `exploratory`), git revision, SHA-256 of `uv.lock`, input hashes, effective parameters, host/runtime metadata, wall-clock start/end, and `status` in `{completed, failed, inconclusive}`. |
| `energies.csv` | Sampled cycle and mode-energy observables, with the protocol's sample interval and normalization recorded in the header or metadata. |
| `metrics.json` | One object per M1–M4 and C1–C3 containing measured value, reference, tolerance, pass/fail (or not-evaluable), and explanatory notes. |
| `figure.png` | Reproduction plot with the digitized reference overlay and a legend identifying baseline versus reference. |
| `log.txt` | Commands, environment, progress, warnings, timing, and traceback/diagnostic text when applicable. |

The first successful baseline is the registered baseline. Exploratory runs get
unique run ids and must never replace its files or metadata. A failed or
inconclusive baseline remains an auditable run and is not silently retried
with adjusted parameters.

## Evidence export allowlist

`run.py export` creates a `.tar.gz` containing only the following relative
members:

```text
study-report/index.html
run/run.json
run/metrics.json
run/energies.csv
run/figure.png
protocol/v1.json
protocol/v1.md
protocol/v2.json
protocol/v2.md
reference/fig1-digitized.csv
reference/README.md
reproduction/commands.txt
environment/uv.lock
environment/README.md
```

The archive is allowlist-based, rejects absolute paths and `..` traversal, and
does not include `_data` payloads, the downloaded PDF, `.env*`, caches, or
unrelated worktree files. `environment/README.md` links to the public OSTI
source and identifies the manifest rather than copying the PDF.

## orbit-research record plan

The native record store belongs to the installed `orbit-research` package; it
is not forked or duplicated here. The owner root is the observatory checkout,
and records use:

```text
--owner-root <observatory checkout>
--records experiments/physics/fput-recurrence-reproduction/research/records
```

The planned record sequence is `program → claim → preregister → begin-run →
record-run → assess`. The index configuration lives outside this checkout;
the record directory contains only native records and task-local provenance.
The browser consumes a browse-export written under `_outputs/`, never a second
hand-maintained record database. A record points to the run directory and
protocol version, so baseline/exploratory identity and amendments remain
recoverable.

## Chapter presentation contract

Every field-guide chapter is a node-keyed directory beneath
`experiments/physics/physics-field-guide/` and has these files:

```text
<chapter>/chapter.json
<chapter>/reference.py
<chapter>/validation.json        # generated, ignored output
<chapter>/index.html
```

`chapter.json` must provide the following schema fields:

| field | contract |
|---|---|
| `question` | A falsifiable or measurable question for the visitor. |
| `prediction_prompt` | A prompt asking the visitor to predict before changing controls. |
| `model` | Summary with equations, units, assumptions, and named state variables. |
| `controls` | Each control's range, default, and units. |
| `presets` | Named, reproducible parameter sets. |
| `validation_cases` | Predefined parameter points with expected observables and numeric tolerances. |
| `references` | Analytic references and source links. |
| `source_revision` | Git revision or protocol revision used to produce the reference values. |
| `limits` | Explicit “where the model stops applying” statement. |

`reference.py` is the independent Python reference and produces
`validation.json`. The browser must match that file within each case's declared
tolerance at every predefined point; it cannot use the browser's own output as
its oracle. Controls are keyboard accessible, labels are programmatically
associated, and the layout works on a narrow screen. Under
`prefers-reduced-motion`, show a static path with the same plotted observable
and validation semantics rather than removing the result.

The three selected chapters are documented in
`experiments/physics/physics-field-guide/README.md`: Kepler orbits and
integrator error; the linear chain's waves, interference and boundaries; and a
driven damped oscillator's resonance and damping.

## Field-guide export contract

The future `_scripts/export-field-guide.sh` writes
`_outputs/field-guide-export/` using an allowlist. It may include only:

```text
experiments/physics/physics-field-guide/**
_lib/web/**
knowledgebase/studies/physics/fput-recurrence-reproduction.md
```

Here `_lib/web/**` is the export shorthand for the canonical repository path
`experiments/physics/_lib/web/**`.

It explicitly excludes `knowledgebase/lineage/**`, every other experiment,
`_data`, `.orbit`, `.env*`, and generated caches. The script must fail closed
when a requested member is outside this list and must preserve relative paths.
