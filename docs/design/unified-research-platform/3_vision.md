---
title: Unified Research Platform — Vision
owner: claude
last_updated: 2026-09-07
last_validated: 2026-09-07
status: Accepted
feature: unified-research-platform
doc_role: vision
type: design
summary: Where this goes once the migration lands: the loop, cross-domain findings, and what stays out.
tags: [unified-research-platform]
paths: ["experiments/**", "knowledgebase/**", "_scripts/**"]
related_features: [unified-research-platform]
related_artifacts: []
---

# Unified Research Platform — Vision

The measure of success is one habit: an idea arrives, it is captured, and
within a week there is a directory that tests it and a note that says what
happened. The four repositories never produced that habit because each demanded
its own ritual. One repository with one gate can.

Once the migration lands, the interesting work is at the seams. A ranking-
decay observation in the kaggle domain feeding a physics hypothesis is
representable as a `derives-from` edge in nebula and as two experiment
directories that cite each other's studies. `neb trace` over a corpus that
spans domains is the artefact this platform exists to make possible.

What should stay out: work material, life logistics, and tooling that has its
own repository. The platform gets better by being used, not by growing.
