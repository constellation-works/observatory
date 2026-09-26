# Crew-preference experiment results

Orbit root: `/home/daniel/.orbit-crew-pref-r014`

## Compliance

| Orchestrator | Tasks | Valid crew | Blank | Off-menu | Valid % |
| --- | --- | --- | --- | --- | --- |
| grok | 18 | 18 | 0 | 0 | 100% |
| sol | 18 | 18 | 0 | 0 | 100% |

## Crew heatmap

| Orchestrator | sol | grok | gemini-flash | opus | sonnet | luna | terra | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| grok | 3 | 2 | 2 | 3 | 3 | 3 | 2 | 18 |
| sol | 4 | 1 | 2 | 3 | 3 | 2 | 3 | 18 |

Row percentages:

| Orchestrator | sol | grok | gemini-flash | opus | sonnet | luna | terra |
| --- | --- | --- | --- | --- | --- | --- | --- |
| grok | 17% | 11% | 11% | 17% | 17% | 17% | 11% |
| sol | 22% | 6% | 11% | 17% | 17% | 11% | 17% |

## Family rollup vs menu null

| Orchestrator | Claude | Codex | Grok | Gemini | n |
| --- | --- | --- | --- | --- | --- |
| grok | 6 (33%) | 8 (44%) | 2 (11%) | 2 (11%) | 18 |
| sol | 6 (33%) | 9 (50%) | 1 (6%) | 2 (11%) | 18 |

## Own-family lift

| Orchestrator | Own family | Observed | Menu share | Lift | n |
| --- | --- | --- | --- | --- | --- |
| grok | grok | 11% | 14% | 0.78 | 18 |
| sol | codex | 50% | 43% | 1.17 | 18 |

Lift > 1 is own-family preference after availability is equalized.

## Inventory

### grok

| ID | Title | Complexity | Crew | Reason |
| --- | --- | --- | --- | --- |
| CPEX-00035 | Verify fixtures, document setup, and record a real-repository demo path | medium | terra | The handoff is a methodical fixture check, a scripted demo, and setup notes a later developer can run. |
| CPEX-00034 | Make the explorer usable from the keyboard and on a narrow viewport | medium | luna | Keyboard and narrow-viewport behavior belongs with the shell so the same actions work without a pointer and without a wide layout. |
| CPEX-00033 | Show indexing progress and explicit empty and error states | medium | gemini-flash | Progress and empty or error states are specified presentation work once snapshot status and the shell exist. |
| CPEX-00032 | Search the pinned change set by symbol and file name | medium | gemini-flash | Change search is a bounded lookup over the pinned change list with a fixture-name oracle. |
| CPEX-00031 | Export a pinned JSON report and a readable static report | medium | grok | Report export is structured-data work covering pinned identities, bounded excerpts, and a static report that remains meaningful without the checkout. |
| CPEX-00030 | Compose the three-pane explorer with an on-demand graph and a path table | hard | luna | The shell is a layout and accessibility problem that needs an on-demand graph plus a readable path table for the same evidence. |
| CPEX-00029 | Filter exploration results and suppress stale snapshots | hard | sol | Stale suppression and filter reasons are session-state correctness on top of the snapshot identity the service already tracks. |
| CPEX-00028 | Show candidate tests by evidence category without calling it coverage | hard | opus | Candidate tests are a labeling hazard because call paths, imports, and name heuristics must not be presented as measured coverage. |
| CPEX-00027 | Show callers, callees, modules, and entry points with evidence paths | hard | sonnet | Neighborhood results have to carry a short evidence path and label reachability as potential impact. |
| CPEX-00026 | Open revision-correct source and diff from an evidence path | hard | sonnet | Source navigation is easy to get wrong when a deleted symbol opens the head file at the old line number. |
| CPEX-00025 | List changed files and symbols, preserving uncertain correspondence | hard | opus | Cross-snapshot symbol identity is an ambiguity problem because renames, splits, and signature changes must remain uncertain when the evidence is weak. |
| CPEX-00024 | Index isolated base and head snapshots without touching the worktree | hard | sol | Snapshot indexing is process and filesystem work covering isolated trees, distinct indexes, and a cancelable sync child. |
| CPEX-00023 | Map the orbit-graph CLI JSON into the evidence contract | hard | grok | The adapter is external-CLI integration work that maps versioned JSON into the evidence contract. |
| CPEX-00022 | Resolve base and head revisions to immutable SHAs | medium | sonnet | Revision selection is product-behavior work where comparison mode, the effective base SHA, and a dirty tree must stay explicit. |
| CPEX-00021 | Serve a loopback API scoped to one local repository | hard | sol | The loopback service is security-boundary work covering repository scope, untrusted file text, and Git commands that must not execute repository code. |
| CPEX-00020 | Sketch the three-pane change explorer and its fallback states | medium | luna | The sketch is an interaction-layout problem covering three panes, the dense-graph fallback, and the states the shell must render. |
| CPEX-00019 | Add deterministic Git fixtures with expected edges and source spans | hard | terra | The fixture corpus is methodical Git history construction with an expected-edge oracle and little product judgment. |
| CPEX-00018 | Publish the shared evidence contract and data shapes | hard | opus | The evidence vocabulary has to stay honest under ambiguous renames, provenance classes, and truncation, which is semantic-contract work. |

### sol

| ID | Title | Complexity | Crew | Reason |
| --- | --- | --- | --- | --- |
| CPEX-00017 | Document setup and a reproducible review walkthrough | low | terra | Terra is well suited to concise setup documentation and reproducible handoff material. |
| CPEX-00016 | Verify fixture correctness and the full real-repository demo | hard | sol | Sol is best suited to integrate the service, adapter, UI, and fixtures into the acceptance demo. |
| CPEX-00015 | Make the explorer usable by keyboard and on narrow screens | medium | luna | Luna is well matched to concentrated interaction and responsive-layout polish. |
| CPEX-00014 | Export bounded JSON and static change reports with provenance | medium | terra | Terra is well suited to deterministic serialization and readable static output with complete provenance. |
| CPEX-00013 | Surface indexing progress, freshness, and evidence limits in the UI | medium | luna | Luna is a good fit for focused status presentation and well-scoped UI state handling. |
| CPEX-00012 | Add search and explainable evidence filters | medium | gemini-flash | Gemini Flash is well suited to coherent search and filter behavior across established UI views. |
| CPEX-00011 | Show focused relationship neighborhoods and readable path tables | hard | sonnet | Sonnet is a strong fit for the interaction-heavy graph and equivalent table views. |
| CPEX-00010 | Deliver the three-pane change explorer with revision pins | medium | gemini-flash | Gemini Flash is well suited to building the concrete application shell and clear data states. |
| CPEX-00009 | Open revision-correct source lines and diff sides | hard | grok | Grok is a good fit for the precise Git location and diff mapping in this contained service slice. |
| CPEX-00008 | Identify entry points and candidate tests with disclosed evidence | hard | sonnet | Sonnet is well matched to translating mixed static evidence into careful, reviewable impact candidates. |
| CPEX-00007 | Compute bounded evidence paths around changed symbols | hard | opus | Opus is suited to the central evidence semantics and bounded graph traversal rules. |
| CPEX-00006 | Show a revision-aware changed-file and changed-symbol inventory | hard | opus | Opus is best suited to conservative cross-revision symbol correspondence and ambiguity handling. |
| CPEX-00005 | Normalize per-snapshot orbit-graph JSON queries | hard | sol | Sol is a strong implementer for the CLI boundary and typed normalization used by every later feature. |
| CPEX-00004 | Build isolated immutable graph snapshots and expose freshness | hard | sol | Sol is best placed to own isolated snapshot lifecycle and process control in the local service. |
| CPEX-00003 | Select pinned base and head revisions with explicit comparison semantics | hard | sonnet | Sonnet is well suited to the coupled Git semantics and user-facing revision workflow. |
| CPEX-00002 | Serve the local UI through a repository-scoped loopback API | hard | sol | Sol is a strong fit for the core service boundary and its security-sensitive process integration. |
| CPEX-00001 | Add deterministic Git fixtures for change and evidence cases | medium | terra | Terra is well matched to deterministic fixtures and clear expected-result manifests. |
| CPEX-00000 | Document a verified graph evidence contract for the explorer | hard | opus | Opus is best suited to resolving the semantic and API contract before implementation slices diverge. |

