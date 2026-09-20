---
title: Unified Research Platform — Overview
owner: claude
last_updated: 2026-09-07
last_validated: 2026-09-07
status: Superseded
feature: unified-research-platform
doc_role: overview
type: design
summary: Why orrery, principia, parallax and kaggle collapse into one repository, and what the flow through it is.
tags: [unified-research-platform]
paths: ["experiments/**", "knowledgebase/**", "_scripts/**"]
related_features: [unified-research-platform]
related_artifacts: []
superseded_by: docs/design/research-layout-v2/1_spec.md
---

# Unified Research Platform — Overview

## Problem

Research lived in four repositories split by topic: orrery (physics sims),
principia (theory prose and claim registry), parallax (empirical studies,
crypto first) and kaggle (competitions). Each had its own conventions, its own
environment and its own notion of "done". Ideas crossing a boundary had nowhere
to go, so they went nowhere. The split was never about ownership or trust; all
four belong to one person. It was about topic, and topic is exactly the wrong
axis, because the ideas worth having are the ones that cross topics.

## Shape

One private repository, partitioned by view: a domain is a directory name and
a tag, not a repository. The same argument nebula makes for domains inside one
corpus, one level up.

Four layers, in the order an idea moves through them:

| layer | holds | keyed by |
|---|---|---|
| `knowledgebase/lineage/` | the nebula corpus: ideas, hypotheses, evidence, provenance | node id |
| `experiments/<domain>/<id>/` | the code and notebooks that test one node | node id |
| `knowledgebase/studies/<domain>/<id>.md` | what came out, which way it cuts | node id |
| `knowledgebase/theory/` | claims that survived, under principia's lock | claim id |

`_data/` and `_outputs/` sit beside these on disk and are never committed.

## Non-goals

Not a place for work material. Not a replacement for the almanac, which stays
the personal vault for everything that is not research. Not a monorepo of
services: nebula, orbit and the rest remain their own codebases.
