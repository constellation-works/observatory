# CLAUDE.md

Guidance for Claude when working in this Kaggle workspace.

## Context

This directory holds Kaggle competitions and projects. Work spans both classic
tabular ML (pandas, scikit-learn, gradient boosting) and deep learning
(PyTorch/TensorFlow, CV/NLP). Each competition is a self-contained subfolder —
see `README.md` for the layout.

## Working principles

- **Reproducibility first.** Seed every source of randomness (`numpy`, `random`,
  framework RNGs). Make data splits deterministic. Note exact data versions.
- **Validate before submitting.** Build a trustworthy cross-validation scheme
  early; trust local CV over public leaderboard. Watch for train/test leakage
  and distribution shift.
- **Keep code reusable.** Notebooks are for exploration; promote stable feature
  engineering, training, and inference logic into `src/` as plain modules.
- **Be explicit about the metric.** Optimize and report the competition's exact
  evaluation metric, not a convenient proxy.

## Conventions

- Data goes in `<competition>/data/` and stays out of git (it's gitignored).
- Submissions are written to `<competition>/submissions/` and follow the
  competition's required format exactly.
- Prefer config-driven experiments over hardcoded constants; log CV scores so
  runs are comparable.
- Use the Kaggle CLI for downloads and submissions (see README).

## When asked to help

- Start from the competition's `README.md` and `data/` to understand the task,
  metric, and data shape before proposing solutions.
- For modeling, suggest a simple baseline first, then iterate.
- Flag potential leakage, overfitting to the public LB, or invalid CV.
- Don't fabricate scores or data statistics — compute them.

<!-- orbit-managed:start -->
## Orbit Workflow Rules

This block is managed by `orbit workspace init --inject-agent-rules`. Edit the asset at `crates/orbit-core/assets/agent-rules.md` (or your local fork) and re-run the command to refresh in place; content outside the markers is preserved.

- **Task before work.** File an Orbit task before non-trivial code changes. Use the `orbit-task` skill (or `orbit.task.add`). Don't invent task IDs — `orbit.task.add` allocates them.
- **Tool surface over file edits.** Use `orbit.task.*`, `orbit.adr.*`, `orbit.docs.*`, `orbit.learning.*` for their respective artifacts. Never edit files under `.orbit/` directly; the audit log and indexes will drift.
- **Commit attribution.** Set the author to your agent family (`codex`, `claude`, `gemini`, `grok`) — not a full model string. Include the relevant task ID in the commit message — `[ORB-NNNNN]` for repo-level tasks, `[T20260514-3]` for ad-hoc tasks. When a task has an `external_ref`, include that tag too for cross-engineer review.
- **Don't commit without approval.** Hold `git commit` until the Orbit task has been explicitly approved by the human. Mark the task `review` first; commit only after approval flips it to `done` (or the human says "commit").
- **Route via the `orbit` skill.** Start sessions by reading the `orbit` skill (`<orbit-root>/skills/orbit/SKILL.md`). It is the entry point that lists every workflow skill (`orbit-task`, `orbit-workflow`, `orbit-search`, `orbit-knowledge`).
<!-- orbit-managed:end -->
