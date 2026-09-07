---
title: Unified Research Platform — Decisions
owner: claude
last_updated: 2026-09-07
last_validated: 2026-09-07
status: Accepted
feature: unified-research-platform
doc_role: decisions
type: design
summary: Decisions with reasoning: one repo not four, view partition, node-id keying, data boundary, corpus location, name.
tags: [unified-research-platform]
paths: ["experiments/**", "knowledgebase/**", "_scripts/**"]
related_features: [unified-research-platform]
related_artifacts: []
---

# Unified Research Platform — Decisions

## One repository, partitioned by view

Considered keeping four repositories and adding a cross-index. Rejected: an
index is a fifth thing to maintain, and the ideas that matter cross topics.
One owner means one trust boundary, so one repository.

## Keyed by nebula node id

Considered numeric experiment ids and free names. Rejected: both need a lookup
table to reach the idea. The node id is already unique, permanent and
human-readable, and it makes the checker able to verify the join.

## Data out of git, manifests in

Considered git-lfs and DVC. Rejected for now: both add a daemon and a remote
to keep alive, and the actual need is reproducibility, which a manifest with a
hash and a fetch command satisfies. Revisit if datasets need versioning beyond
"which snapshot".

## The personal corpus lives here

Considered leaving it in `~/.nebula`. Rejected: evidence sources would then be
absolute paths the checker cannot verify from a fresh clone, and the corpus
would not be backed up with the research it describes. This repository is
private, which is what made it safe.

## Principia's lock survives as-is

Considered replacing `check-theory.py` with nebula invariants. Rejected: the
theory lock encodes physics-specific policy (postulate expiry, comparators,
retirement) that nebula deliberately does not know about. They are different
layers with a graduation edge between them.

Considered moving principia's `studies/` into `knowledgebase/studies/physics/`.
Rejected on landing (2026-09-07): those notes are literature, not results, every
theory document links to them relatively, and the checker resolves them under
the lock root. Two kinds of "study" with two homes is clearer than one directory
with two contracts.

## Migration with history

Considered copying files. Rejected: a platform for tracing where ideas came
from should not begin by discarding where its own content came from.
`git subtree add` keeps every commit.

## Named "observatory"

"Sextant" was the first instinct and is already spent: a retired constellation
service whose retirement is baked into migration manifests. Observatory is the
building where instruments, data and theory converge, which is the job.
