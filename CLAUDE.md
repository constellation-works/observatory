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
