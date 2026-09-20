---
title: Paper reproduction and interactive physics field guide
owner: observatory
last_updated: 2026-09-13
last_validated: 2026-09-13
status: Accepted
feature: paper-reproduction-workbench
doc_role: design
type: design
summary: Contracts for a reproducible LA-1940 figure workbench and three browser-based physics chapters.
tags: [physics, research, paper-reproduction, field-guide]
paths: ["research/R005-fput-recurrence-reproduction/**", "docs/field-guide/**", "_lib/web/**", "_scripts/export-field-guide.sh"]
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
research/R005-fput-recurrence-reproduction/code/
  README.md
  manifest.json
  protocol/v1.json
  protocol/v1.md
  protocol/v2.json
  protocol/v2.md
  reference/fig1-digitized.csv
  reference/README.md
  reference/la-1940-fig1.png
docs/field-guide/
  README.md
_data/physics/fput-recurrence-reproduction/manifest.json
research/R005-fput-recurrence-reproduction/output/<run-id>/
research/R005-fput-recurrence-reproduction/README.md
```

The reference image is a credited crop of the public-domain OSTI/LANL scan.
The CSV is digitization evidence with uncertainty, not an original data dump.

## Reproduction runner contract

The future runner is `research/R005-fput-recurrence-reproduction/code/run.py`.
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
`research/R005-fput-recurrence-reproduction/output/<run-id>/`. The directory is
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
--records _archive/records/fput
```

The planned record sequence is `program → claim → preregister → begin-run →
record-run → assess`. The index configuration lives outside this checkout;
the record directory contains only native records and task-local provenance.
The browser consumes a browse-export written under the item's ignored `output/`, never a second
hand-maintained record database. A record points to the run directory and
protocol version, so baseline/exploratory identity and amendments remain
recoverable.

## Chapter presentation contract

Every field-guide chapter is a node-keyed directory beneath
`docs/field-guide/` and has these files:

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
`docs/field-guide/README.md`: Kepler orbits and
integrator error; the linear chain's waves, interference and boundaries; and a
driven damped oscillator's resonance and damping.

## Field-guide export contract

`_scripts/export-field-guide.sh` rebuilds `output/field-guide-export/` from
an explicit allowlist (not an exclude list). It is runnable from any cwd; pass
`--output DIR` to write somewhere else. The export root mirrors
the repository root so chapter imports of `../../../_lib/web/…` resolve
unchanged.

```sh
./_scripts/export-field-guide.sh
./_scripts/export-field-guide.sh --output /tmp/field-guide-export
```

Allowlisted members:

```text
physics-field-guide/<chapter>/     # every dir with chapter.json
  index.html, *.js, chapter.json, sim.json, validation.json,
  README.md, static figures
_lib/web/**                        # _lib/web/**
physics-field-guide/README.md
index.html                         # generated; relative links only
LICENSES.md
reference/la-1940-fig1.png
reference/README.md                # public-domain credit line
study/fput-recurrence-reproduction/**   # if research/R005-fput-recurrence-reproduction/output/site/ exists
```

`tests/`, `reference.py`, `__pycache__`, `_lib/vendor`, `_archive/**`
(including lineage and studies), every other experiment, `_data`, `.orbit`,
`.env*`, and `.git` are not copied. `_lib/vendor/three` is added only when an
exported chapter actually imports it.

The script ends with a self-check that fails non-zero if the output tree
contains a forbidden path, an absolute `/home/` string, a secret-looking
token, or an HTML `href`/`src` / JS `import` that resolves outside the export
root. It prints the chapter count. `_scripts/test_export_field_guide.py`
rebuilds into a temp dir and asserts these invariants.

## Delivered

Integrated acceptance ran on 2026-09-12 (ORB-12365) against the checkout at
`d604ff5`, whose tree is `main` minus the last two record commits. Every
command below was rerun for that acceptance; the numbers are its own output.

### Runnable commands

```sh
uv sync --extra research
R=research/R005-fput-recurrence-reproduction/code
uv run $R/run.py baseline                 # the registered protocol-v2 baseline
uv run $R/run.py explore --set alpha=1.0  # bounded exploration, never the baseline
uv run $R/run.py explore --set dt=0.125
uv run $R/run.py report                   # study page from the newest baseline
uv run $R/run.py evidence --bundle <orbit-research export.json>
uv run $R/run.py export && uv run $R/run.py export --check
uv run $R/tools/record_chain.py --run <job-run-id> --stop-after export
./_scripts/export-field-guide.sh          # shareable chapter tree
make check                                # records, ruff, pytest (make check-archive for the lock)
```

Browser passes (headless Chromium at 1280 px and 375 px):

```sh
LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
  uv run --with playwright python $R/tools/browser_check.py \
  research/R005-fput-recurrence-reproduction/output/site/index.html
LD_LIBRARY_PATH=... uv run --with playwright python \
  docs/field-guide/<chapter>/tests/browser_check.py
```

### Artifact locations

| artifact | path |
|---|---|
| run directory (regenerable, untracked) | `research/R005-fput-recurrence-reproduction/output/<run-id>/` |
| study page and evidence browser | `research/R005-fput-recurrence-reproduction/output/site/` |
| evidence package | `research/R005-fput-recurrence-reproduction/output/export/fput-reproduction-v2-<run-id>.tar.gz` |
| canonical scientific records | `research/physics/fput-recurrence-reproduction/records/` |
| chapters | `docs/field-guide/{orbits-numerical-error,waves-boundaries,resonance-damping}/` |
| shareable export | `output/field-guide-export/` |
| study notes | `research/R005-fput-recurrence-reproduction/README.md and docs/field-guide/VALIDATION.md` |

### Frozen protocol and measured values

The registered baseline runs **protocol v2** (`protocol/v2.json`, frozen;
`protocol/v1.*` stays frozen as the pre-repair reading, and
`protocol/exploration.json` is a presentation-only sidecar that bounds
exploratory deviations). Measured on 2026-09-12, `status: completed`,
`scientific_assessment: supports`:

| id | measured | reference | tolerance | result |
|---|---|---|---|---|
| M1 first mode-1 recurrence | 28,400 cycles | 28,600 | ±1,000 | pass |
| M2 mode-1 energy returned | 0.9777532985498025 | 0.9666666666666667 | 0.03 | pass |
| M3 mode-2 major peak | 14,100 cycles / 0.8817707004889854 | 14,000 / 0.8833333333333333 | 5% time, 0.10 height | pass |
| M3 mode-3 major peak | 9,250 / 0.7122695735332155 | 9,400 / 0.7 | as above | pass |
| M3 mode-4 major peak | 6,550 / 0.45443492092262405 | 6,500 / 0.45 | as above | pass |
| M4 higher-mode ceiling (per mode) | 0.06316980197954705 | 0.0666666667 | 0.0666666667 | pass |
| C1 linear-chain conservation | 0.00030083236612377107 | 0 | 0.01 | pass (gating) |
| C2 total-energy drift | 0.002015601922728094 | 0 | 0.01 | pass (gating) |
| C3 δt/2 recurrence movement | 0.05105633802816894 | 0 | 0.01 | **fail** (reported, not gating) |

Artifact digests, identical in the repository run and in a clean `/tmp`
environment built only from the evidence package: `metrics.json`
`1570191f…e86721`, `energies.csv` `c145ec40…f270c4ee`, `figure.png`
`4614da6d…56f2d768`. They match the digests registered in the
`…-baseline-metrics-json`, `…-baseline-energies-csv` and
`…-baseline-figure-png` artifact records.

The evidence package holds 30 members and 11 canonical records, verifies every
SHA-256 and reports 0 absolute paths. `uv run orbit-research validate` accepts
the exported bundle (21 record entries collapsing to 11 distinct records, 8
manifests, 2 unresolved references).

### The three chapters

| chapter | question it answers | validation cases |
|---|---|---|
| `orbits-numerical-error` | how integrator choice and step size show up as drift in conserved quantities | 16 |
| `waves-boundaries` | how modes, interference and a fixed/free end behave on the linear chain | 12 |
| `resonance-damping` | how a driven damped oscillator's amplitude and phase depend on drive and damping | 6 |

Each chapter's browser numerics agree with its `validation.json` (written by
`reference.py`) to a worst relative difference of 0 at the declared 1e-9
tolerance. `window.__chapter.runCase` validates its arguments against the
ranges declared in `chapter.json` (plus the per-chapter bounds for arguments
that are not controls) and refuses an out-of-range value with a message naming
the control, the value and the range, rather than returning NaNs.

### Limitations

- **Digitization uncertainty.** The comparison reference is a digitization of
  the printed Fig. 1 (±250 cycles, ±5 report units on each read point, with a
  wider ±1,000 cycle / ±10 unit calibration bound), never the original MANIAC
  output. Mode 3's second maximum is the softest read point.
- **Linear-energy approximation in E_k.** The mode energies use the linear
  normal-mode form `E_k = ½(ȧ_k² + ω_k² a_k²)`, the same quantity the report
  plots; the cubic term's contribution to the energy is not partitioned into
  modes.
- **The δt² interpretation.** The caption's `δt² = 1/8` is read as
  `δt = 1/√8 = 0.35355…`. The naive reading `δt = 1/8` is available only as a
  labelled exploratory run, where the recurrence falls outside the figure's
  own abscissa.
- **Independent reconstruction, not a rerun.** No author code exists; the
  integrator ordering is inferred from the report's description. Agreement is
  evidence about the physics, not about the original program.
- **C3 remains unresolved.** Halving δt moves the physical recurrence time by
  5.106%, over its own 1% threshold. Protocol v2 reports it rather than gating
  on it; no tolerance was relaxed to obtain a pass, and it stays listed here.
- **Chain provenance.** The protocol-v2 baseline was first executed under
  ORB-12375, before the native record chain was registered, so the chain
  proves local registration order and frozen input identity, not
  independently attested prospective execution; the assessment is authored
  `inference: exploratory`. The bundle also carries 2 `pending` claim→program
  references, authored before the program record could be committed.
- **Presets on a log-range slider.** A preset applies its declared value
  exactly to the model and to the readout; the slider element itself re-snaps
  to its nearest step notch, so the thumb can sit a fraction of a step away
  from the value the page reports until the control is next moved.
