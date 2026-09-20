# experiments/kaggle

Kaggle competitions. The competition slug is the id: `experiments/kaggle/<slug>/`
holds the code and notes, `_data/kaggle/<slug>/` the downloaded data,
`_outputs/kaggle/<slug>/` every derived artifact (results, caches, submissions).
Kaggle is the one domain whose ids are not nebula nodes; `check-layout` exempts it.

```
experiments/kaggle/<slug>/
  README.md          task, metric, CV-vs-leaderboard log
  manifest.json      data and output locations, status
  src/               reusable code: features, models, training, submit
  approaches/        write-ups of what was tried (optional)
  data-dictionary.md what each column means (optional)
_data/kaggle/<slug>/manifest.json   where the data comes from and how to fetch it
```

## Flow

1. `mkdir experiments/kaggle/<slug>` and copy `manifest.json` from a sibling.
2. Fetch: the `fetch` command in `_data/kaggle/<slug>/manifest.json`
   (`kaggle competitions download -c <slug> -p _data/kaggle/<slug>`).
   Credentials live in `~/.kaggle/kaggle.json` (chmod 600).
3. Explore in a notebook, promote stable code into `src/`.
4. Write submissions to `_outputs/kaggle/<slug>/submissions/`, then
   `kaggle competitions submit -c <slug> -f <file> -m "<description>"`.
5. Log CV and leaderboard scores in the competition README.

## Principles

- **Reproducibility first.** Seed every source of randomness; make splits
  deterministic; note exact data versions.
- **Validate before submitting.** Build a trustworthy cross-validation scheme
  early and trust it over the public leaderboard. Watch for leakage and shift.
- **Be explicit about the metric.** Optimize and report the competition's
  exact metric, not a proxy.
- **Nothing derived in git.** Results and submissions regenerate from `src/`;
  the write-up of what they showed goes in the README or `approaches/`.

## Environment

The root `pyproject.toml` covers these: `uv sync --extra ml` for the tabular
competitions (scikit-learn, lightgbm, kaggle CLI), `--extra arc` adds torch.
Scripts resolve `_data` and `_outputs` from the observatory root, so run them
from anywhere: `uv run python -m src.submit` inside a competition directory,
or set `ROGII_DATA_DIR` / `ROGII_OUTPUTS_DIR` to point elsewhere.
