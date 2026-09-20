---
title: Research Layout v2 — Decisions
owner: fable
last_updated: 2026-09-19
last_validated: 2026-09-19
status: Proposed
feature: research-layout-v2
doc_role: decisions
type: design
summary: Why flat over grouped, why markdown is canonical, why Nebula goes, and what is still open for Daniel.
tags: [research-layout-v2, observatory]
paths: ["questions/**", "hypotheses/**", "theories/**", "research/**"]
related_features: [unified-research-platform]
related_artifacts: []
---

# Research Layout v2 — Decisions

Agreed with Daniel in session on 2026-09-19 (ORB-12626). Each decision names the condition
that would reverse it.

## Flat and wide, not knowledgebase/codebases/operations

Daniel's first sketch grouped the tree into `knowledgebase/`, `codebases/` and `operations/`
with `R001` appearing under both `knowledgebase/research` and `codebases/experiments`.
Rejected: keying one experiment in two trees is the same disease as the node-id join across
`lineage/`, `experiments/` and `studies/`, only with fewer layers. The prose-versus-code
split the grouping wanted is served by `README.md` versus `code/` inside one directory.
Reverse if a second owner ever needs a different trust boundary for code than for records.

## Underscore marks apparatus

`_lib`, `_data`, `_scripts`, `_archive`. A glance at the root separates what is known from
what is plumbing, and the checker's skip rule is one glob. `docs/` and `notebooks/` stay bare
because a person reads them.

## Short sequential ids, frozen slugs

`R001-slug`. Considered slug-only (Nebula's choice) and UUIDs. Slug-only breaks when a title
changes or two ideas share a name; UUIDs are unreadable in a directory listing. A three-digit
prefix is sortable, typeable and unique per kind; the slug is decoration and never changes.
Reverse if a kind passes 999 items, by widening the prefix in one migration.

## One directory per research item

Rule 3. Colocation is what makes parallel research agents safe: each run's write footprint is
one directory plus assessment appends, so merges do not conflict. Considered keeping
`_outputs/<id>` at the root as today; rejected because it re-creates the join.

## Markdown frontmatter is canonical

orbit-research's v2 JSON records were a second, machine-only authority beside the markdown a
person actually reads. One of them had to win. Markdown wins because it is what Daniel edits,
diffs and reviews; the index is a projection. Existing JSON records are archived, not
converted. Reverse if conditional writes over frontmatter prove unreliable in practice; the
fallback is a sidecar `record.json` per item, still one per directory.

## Lineage survives as a field

Nebula's one durable idea was that a hypothesis has ancestry and dead branches stay visible.
`derived_from` keeps that at zero cost. A separate lineage corpus does not.

## Projects are tags

Projects go inactive without a decision to abandon them. A directory per project would either
sprawl or need archiving; a tag costs nothing to leave alone and is filterable. Reverse if the
dashboard needs project-level metadata that a tag cannot carry, in which case a `P###` file
kind is the extension, not a directory.

## principia's lock is archived, not migrated

It is byte-pinned, physics-specific and the one part of the corpus with real accumulated value
(refuted wall, gates, ledgers). Moving it under `_archive/principia/` unchanged and citing into
it from T files preserves all of that with no schema translation. Its checker stays runnable as
`make check-archive`. Reverse only if a T file needs to change a claim the lock owns; then the
claim is re-stated as an H in the live corpus and the lock is left as history.

## Legacy multi-sim R items are allowed

`gravity-as-scarcity` has 24 sims. Splitting it into 24 R items during migration would
manufacture 24 write-ups nobody wrote. One legacy R with `code/<sim>/` keeps history honest;
the rule that new R items are one question, one run applies going forward.

## Open for Daniel

1. **Hypothesis status: explicit or derived?** Specified as explicit with a checker warning on
   disagreement. Derived would remove a field but let an agent's assessment flip a verdict.
2. **`assessments` in frontmatter or a markdown section?** Specified as frontmatter so the
   checker and orbit-research parse one structure. A section reads better in the file.
3. **Keep `make check-archive` in the default `make check`?** Specified as separate so the gate
   stays fast and the archive stays untouched.
4. **Archive the `nebula` GitHub repository?** Outward-facing; left to Daniel.
5. **`docs/` bare or `_docs/`?** Specified bare because Orbit's docs roots and people both read it.
