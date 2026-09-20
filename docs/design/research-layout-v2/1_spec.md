---
title: Research Layout v2 — Specification
owner: fable
last_updated: 2026-09-20
last_validated: 2026-09-20
status: Accepted
feature: research-layout-v2
doc_role: design
type: design
summary: Observatory as the single research knowledgebase — four record kinds keyed by short ids, one directory per experiment, apparatus under underscore directories, no Nebula.
tags: [research-layout-v2, observatory, orbit-research]
paths: ["questions/**", "hypotheses/**", "theories/**", "research/**", "_scripts/**", "_archive/**"]
related_features: [unified-research-platform]
related_artifacts: []
---

# Research Layout v2 — Specification

Orchestrator assignment: Constellation ORB-12626. Companion: ORB-12624 (orbit-research
redesign). Supersedes [unified-research-platform](../unified-research-platform/1_overview.md).
This document specifies the target; the restructure is a separate implementation task.

## Problem

The current layout partitions research by *tool boundary*: `knowledgebase/lineage` (Nebula's
corpus), `knowledgebase/studies`, `knowledgebase/theory` (principia's lock), `experiments/`,
`research/` (orbit-research JSON records). Each has its own checker and its own id, joined by
a Nebula node id that only `neb` can allocate. One experiment touches four trees. Nobody,
human or agent, can hold that in their head, and Nebula is being abandoned.

## Layout

```
observatory/
  README.md          what this is, the five rules, the id scheme
  AGENTS.md          agent boundaries (rewritten for this layout)
  questions/         Q001-slug.md      capture inbox; one question per file
  hypotheses/        H001-slug.md      precise claim; append-only assessment log
  theories/          T001-slug.md      what survived; cites H and R ids
  research/          R001-slug/        the only directory kind: one per experiment
                       README.md       question, method, result, limitations, next
                       code/           scripts that produced the result
                       artifacts/      promoted figures/tables the README cites (committed, small)
                       data/           inputs (gitignored; data/manifest.json committed)
                       output/         raw run products (gitignored)
  notebooks/         free-form human exploration; outputs stripped on commit
  docs/              design records and runbooks (this file)
  _lib/              shared Python package(s): astrolabe, physics sim apparatus
  _data/             shared datasets reused across R items (gitignored; manifests committed)
  _scripts/          check, new, fetch
  _archive/          frozen, read-only history: principia lock, orrery/parallax staging,
                     retired JSON records, the old Nebula corpus
```

Bare directories hold research content or things a person reads. Underscore directories hold
apparatus. The check gate walks only the four record kinds.

## The five rules

1. **The id is the join key.** `Q###`, `H###`, `T###`, `R###`: three digits, zero-padded,
   monotonic per kind, allocated by `_scripts/new.sh` from the highest existing id. The slug
   is kebab-case of the title at creation and is frozen. Never rename a file or directory;
   a title change edits the frontmatter only.
2. **Three kinds are flat files, one kind is a directory.** Questions, hypotheses and theories
   have no code, so they are single markdown files. Research is the only kind that produces
   code and outputs, so it is the only kind that gets a directory. There is no other layering.
3. **Everything about R001 lives in R001.** Code, data manifest, outputs, promoted artifacts
   and the write-up. An agent working on one experiment touches one directory, which is what
   makes many parallel research agents mergeable without conflicts.
4. **Links are frontmatter, not directory structure.** `derived_from`, `tests`, `supports`,
   `tags`. Lineage is a field. Projects and subjects are tags, not directories, because
   projects go stale and directories cannot.
5. **Bytes are never committed, manifests always are.** `data/` and `output/` are ignored
   everywhere. `artifacts/` is the one place a committed figure may live, and only when the
   README cites it.

## Records

### Common frontmatter

```yaml
id: H001
title: Estimator A is biased under MCAR missingness above 30%
status: open
tags: [statistics]
derived_from: [Q001]        # ids of any kind this descends from; empty for roots
created: 2026-09-19
updated: 2026-09-19
```

### Per-kind fields and status vocabulary

| Kind | Extra fields | Status |
| --- | --- | --- |
| Q question | `answered_by: [H/R ids]` | `open`, `answered`, `dropped` |
| H hypothesis | `revision: 1` (bumped when the statement changes), `assessments: [...]` | `open`, `supported`, `refuted`, `inconclusive`, `dropped` |
| R research | `tests: [H ids]`, `orbit: {task, run}` (optional provenance) | `planned`, `running`, `done`, `abandoned` |
| T theory | `claims: [H ids]`, `supersedes: [T ids]` | `active`, `superseded`, `refuted` |

An assessment is an entry appended to the hypothesis frontmatter:

```yaml
assessments:
  - date: 2026-09-21
    research: R004
    revision: 1          # the statement revision this verdict is about
    verdict: inconclusive # supports | refutes | inconclusive
    strength: suggestive  # anecdote | suggestive | strong
    note: control run failed; see R004 README §Limitations
```

Entries are never edited or removed. Disagreeing entries coexist. `status` on the hypothesis
is set by a person; the checker warns when it disagrees with the latest assessment but does
not overwrite it. An assessment against an older `revision` does not carry to the current
statement.

Execution success is not support. A `done` research item with a `refutes` or `inconclusive`
assessment is a complete, valid result.

### Research README

Fixed section order so agents and the dashboard can find things: Question, Method, Result,
Limitations, Next. `data/manifest.json` lists every input as `{name, source, sha256, size,
fetch}`; shared datasets are referenced by their `_data/<name>` manifest.

### What is not a record

`notebooks/`, `docs/`, `_lib/` and `_archive/` carry no frontmatter contract and are skipped
by the gate. A notebook that produces a result worth keeping is promoted into an R item.

## The check gate

`make check` runs `_scripts/check.py`, then ruff and pytest over `_lib/`. The checker fails on:

- duplicate or non-monotonic ids within a kind; a filename whose id or slug disagrees with its frontmatter;
- any `derived_from`, `tests`, `claims`, `supersedes`, `answered_by` or assessment `research`
  reference that does not resolve;
- an R item without `README.md` or `data/manifest.json`, or missing a required README section;
- tracked bytes under any `data/`, `output/` or `_data/` path other than `manifest.json` and `README.md`;
- an assessment whose `revision` exceeds the hypothesis's current `revision`;
- an unknown status value or a frontmatter key outside the schema.

It warns on: hypothesis `status` disagreeing with the latest assessment; an R item `done` with
no assessment on any hypothesis it `tests`; an R item `running` with no update for 30 days.

This replaces `neb check`, `check-layout.sh`, the study/experiment pairing check and
`check-records`. The principia checker survives only as `make check-archive`, optional and
read-only over `_archive/principia/`.

## orbit-research boundary

Canonical records are the markdown files with their frontmatter. There is no second structured
store in this repository; orbit-research's index is a rebuildable projection of these files and
its JSON record format is retired here (existing records move to `_archive/records/`).

- **Owner per kind:** Observatory owns Q, H, T, R and their assessments. Orbit owns tasks and
  runs. An R item's `orbit` field is a link to the operational owner, not copied authority.
- **One validated writer:** whatever writes a record (person, `_scripts/new.sh`, orbit-research)
  must produce a file the checker accepts. orbit-research validates against the same schema the
  checker uses, exported as `_scripts/schema.json`.
- **Revision identity:** the git blob sha of the file is the expected head for a conditional
  write; the git commit is the corpus revision in a delivery receipt.
- **Opaque paths:** orbit-research reads frontmatter and READMEs; it never interprets `code/`,
  `notebooks/` or `_lib/`.
- **Artifacts:** `artifacts/` and manifests are the evidence surface. Missing or changed bytes
  are reported by the checker, never repaired.
- **Delivery:** an agent run lands its files in one R directory (and appends assessments to the
  hypotheses it tests) and commits. Task completion is gated on that commit existing, not on
  the agent's report.

Coordination questions recorded on both ORB-12624 and ORB-12626:

1. ORB-12624 assumed structured JSON records with a Rust owner writer. This specification makes
   markdown frontmatter canonical. The writer/index/receipt contract still holds; the storage
   format changes.
2. Where the delivery receipt persists: recommendation is the Orbit task artifact only, with the
   corpus commit sha inside it, so the repository carries no operational state.
3. "Study" in ORB-12624 maps to the R README, not a separate record kind. "Project" maps to a tag.

## Nebula deprecation

- `knowledgebase/lineage/` moves verbatim to `_archive/lineage/` (nodes, inbox, config). Each
  node becomes a Q, H, T or R record per the migration table; the new record's `derived_from`
  is empty and its README or body cites `_archive/lineage/nodes/<id>.md` as origin.
- `neb` leaves `Makefile`, `pyproject.toml`, `AGENTS.md`, `CLAUDE.md` and `_scripts/`. `NEBULA_ROOT` is gone.
- The `~/.claude/skills/nebula` symlink and the `nebula` skill are removed; `docs/runbooks/*`
  are rewritten without `neb` verbs.
- Outside this repository (separate task): deregister Mac `ws_nebula`, mark the `nebula`
  codebase card retired in Constellation `INDEX.md` and `about.md`, and leave archiving the
  GitHub repository to Daniel.

## Migration

Mechanical moves use `git mv` so history follows. Nothing is deleted; anything without a new
home goes under `_archive/`. Proposed classification of the existing nodes (the implementer
confirms each from content; a node may yield more than one record):

| Today | Becomes |
| --- | --- |
| `bell-tests`, `pendulum-driven`, `network-force`, `wide-binary-selection-methodology` | one R each; add an H where the node states a claim |
| `fput-recurrence-reproduction` | R; its study becomes the README, `.png` to `artifacts/`; `research/physics/.../records` to `_archive/records/fput/` |
| `gravity-as-scarcity` (24 sims, abandoned) | T `refuted`/`superseded` citing `_archive/principia/theory/gravity-as-scarcity`; one legacy R holding the sims under `code/<sim>/` |
| `retarded-scarcity-wake`, `swirl-photon`, `two-substance-vortex-vacuum` | H (+ T where a principia family exists) and one R each |
| `physics-field-guide` | reference material: `docs/field-guide/`, not a record; `export-field-guide.sh` follows it |
| `experiments/kaggle/{arc,rogii-…,stellar}` | one R each, tag `kaggle` |
| `experiments/physics/_lib` (gallery) | `_lib/gallery/`; `make gallery` and `make serve` keep working |
| `experiments/physics/_orrery`, `experiments/economics/_parallax` | `_archive/orrery/`, `_archive/parallax/`; parallax notebooks may be copied to `notebooks/parallax/` |
| `knowledgebase/theory/` (principia lock, 22 MB) | `_archive/principia/` byte-for-byte; one T per family under `theory/theory/*` citing into it; `make check-archive` runs its checker |
| `knowledgebase/studies/` | merged into the matching R README; directory removed |
| `lib/astrolabe` | `_lib/astrolabe`; its notebooks to `notebooks/astrolabe/` |
| `_outputs/` | removed; per-R `output/` |
| `docs/design/unified-research-platform` | kept, status Superseded |
| `pyproject` extra `research` (pinned Python orbit-research) | kept only if `make check-archive` needs it; otherwise dropped |

A legacy R may hold several sims under `code/`. New R items are one question, one run.

## Bounded first version

The implementation task is done when:

1. The layout above exists and every path in the migration table has moved or been archived,
   with `git log --follow` intact for moved files.
2. `make check` is green on the new checker; `make check-archive` runs principia's checker
   against `_archive/principia/` unchanged.
3. `make new KIND=R TITLE="…"` scaffolds a valid R item; a deliberately broken link fails `make check`.
4. `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `Makefile`, `pyproject.toml` and the
   runbooks describe only the new layout, with no `neb` reference outside `_archive/`.
5. No tracked bytes under any ignored path; repository size does not grow beyond the archive moves.

Validation scenario: create `Q` "does X hold", derive `H` from it, scaffold `R` testing `H`, mark
`R` done, append an `inconclusive` assessment, and confirm the checker warns that `H` is still
`open` with an inconclusive latest assessment but does not fail. Then edit `H` to reference `R999`
and confirm the checker fails.

## Non-goals

No dashboard, no orbit-research changes, no agent routines, no data fetching, no rewriting of
principia's ledgers, no new record kinds. The theory-graduation workflow (when an H becomes a T)
is a person's decision and is not automated.
