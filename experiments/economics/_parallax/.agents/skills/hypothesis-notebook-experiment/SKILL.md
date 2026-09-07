---
name: hypothesis-notebook-experiment
description: This skill should be used when creating or recording a Parallax hypothesis, experiment, or research notebook; when the user asks to "write a hypothesis", "create an experiment", "add experiment results", "test this hypothesis", "write the methodology notebook", or to follow hypothesis then notebook then experiment. It enforces the research loop: freeze HNN, implement methodology under notebooks/RNN-title, then write ENN from that notebook's output.
---

# Hypothesis → notebook → experiment

Do not write an experiment result from an ad hoc session. The durable loop is:

```text
hypothesis/HNN-title.md
    → notebooks/RNN-title/ENN-title.ipynb|.py
        → experiments/ENN-title.md
```

Copy templates from `docs/_templates/HYPOTHESIS.md` and `docs/_templates/EXPERIMENT.md`.
Naming, frontmatter, and outcome rules live in `CLAUDE.md` and `docs/RESEARCH_PROTOCOL.md`.
Do not restate those contracts here.

## When this skill applies

- New or revised `HNN` / `ENN` records under `docs/research/RNN-title/`
- Methodology, analysis, or "experiment results" for a numbered Parallax program
- Filling in a hypothesis that was explored in chat without a notebook

Skip only for edits that do not create or evaluate a claim (typos, registry links, unrelated docs).

## Sequence

### 1. Freeze the hypothesis

Create `docs/research/RNN-title/hypothesis/H<NN>-<title>.md` before implementing the test.

- Use the next unused `HNN` in that program. Never reuse or renumber.
- Freeze one claim, mechanism, predicted observables, baseline, alternatives, and rejection
  criteria.
- Leave `outcome: untested` until an experiment exists.
- Add the row to `hypothesis/README.md`.

If evaluation data were already viewed, still freeze the original claim. Do not restate the window
or metric after seeing results. Mark the later experiment `preregistered: false`.

### 2. Implement the notebook

Create the methodology as at least one of:

```text
notebooks/RNN-title/ENN-<title>.ipynb
notebooks/RNN-title/ENN-<title>.py
```

Name the file with the **experiment** id, not the hypothesis id. A linear `.py` is a valid
notebook-layer script when the method is a batch analysis. Prefer `.ipynb` when plots or narrative
cells help; keep one source of truth (script executed by the notebook, or a self-contained notebook).

The notebook must record and compute:

- `research_id`, `hypothesis_id`, `experiment_id`, `preregistered`
- exact source path, version, checksum, license, observation window, information cutoff
- frozen cuts (clock windows, filters) as named constants
- baseline, primary metric, uncertainty
- labeled printed outputs the experiment record can quote

Run it. For Kaggle tapes, load `.agents/skills/use-local-kaggle-data` and read the versioned
`resolved_path`; do not copy multi-gigabyte sources into `data/RNN-title/raw/` unless creating an
immutable R01 snapshot.

Do not graduate this code into `src/parallax/` until it supports a durable claim with tests.

### 3. Write the experiment from the notebook

Create `docs/research/RNN-title/experiments/E<NN>-<title>.md` only after the notebook has been run.

- Test exactly one primary hypothesis. Set `hypothesis_id` and put that `HNN` path in `related`.
- Set **Command or notebook** to the repo-relative methodology path. Quote primary metrics from
  that run, not from chat.
- Declare `preregistered: true` only if the method was frozen before opening evaluation data.
  `preregistered: false` may be `reject`, `revise`, or `inconclusive`, never `advance`.
- Append results and one outcome. Do not rewrite the frozen claim or plan.
- Link the experiment in the hypothesis **Experiment queue**, both registries, and the hypothesis
  `related` list when the experiment exists.

## Forbidden shortcuts

- Experiment markdown whose **Command or notebook** is empty, "ad hoc", or "none checked in"
- Numbers in `ENN` that were not printed by the named notebook
- Notebook without a frozen `HNN`
- `advance` on `preregistered: false`
- Restating frozen cuts in the hypothesis after seeing results — that is a new `HNN`

## Checklist before returning

- [ ] `HNN` exists and is in the hypothesis registry
- [ ] `notebooks/RNN-title/ENN-*` exists and was executed
- [ ] `ENN` exists, links `HNN` in `related`, and names that methodology file
- [ ] Both registries updated
- [ ] `preregistered` matches whether the data were seen first
