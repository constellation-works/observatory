---
id: R010
title: ARC
status: done
tags: [kaggle, arc, machine-learning]
derived_from: []
created: 2026-09-07
updated: 2026-09-20
tests: []
---

# R010 — ARC

Origin: the `arc` competition workspace, migrated with the kaggle domain. A
competition is a project, so it is a tag, not a directory
(`docs/design/research-layout-v2/2_decisions.md`). `tests` is empty: nothing here
bears on a hypothesis in this corpus.

## Question

Can a Tiny Recursive Model — the recursion core of Jolicoeur-Martineau,
*Less is More: Recursive Reasoning with Tiny Networks*
([arXiv:2510.04871](https://arxiv.org/abs/2510.04871)) — be reimplemented
faithfully enough to learn an ARC-AGI-style grid→grid transform?

## Method

`code/sample.py` is a self-contained reimplementation of the TRM recursion core
with a smoke test that trains it to memorise a fixed grid→grid transform.
`code/main.py` is the playground entry point. Competition data is fetched per
`data/manifest.json` and never committed.

## Result

The reference model trains: 0.107M parameters, loss 2.3172 → 0.0151 and token
accuracy 0.102 → 1.000 over 120 steps on the memorisation task. The
reimplementation is therefore usable as a starting point.

## Limitations

A memorisation smoke test is not an ARC result: nothing here is evaluated against
the real task set, and no submission was made. The playground was never taken
past the reference model.

## Next

Evaluate against real ARC-AGI tasks, as a new R item with a question of its own.

---

# Competition notes

Kept as written, from `experiments/kaggle/arc/README.md`.
Paths in it are the old layout's: the code is now `code/`, the data
`data/` and the run products `output/`, both ignored by git.

A small playground for experimenting with [ARC-AGI](https://arcprize.org/) reasoning
models. The reference model in [sample.py](sample.py) is a minimal **Tiny Recursive
Model (TRM)** — a faithful reimplementation of the recursion core from Jolicoeur-Martineau,
*"Less is More: Recursive Reasoning with Tiny Networks"* ([arXiv:2510.04871](https://arxiv.org/abs/2510.04871)).

## Setup

Uses [uv](https://docs.astral.sh/uv/). Install everything (creates `.venv`, writes `uv.lock`):

```bash
uv sync
```

## Run

The reference model ships with a self-contained smoke test — it trains a tiny TRM to
memorise a fixed grid→grid transform. Loss should fall toward zero:

```bash
uv run python sample.py
```

```
parameters: 0.107M
step   0  loss 2.3172  token_acc 0.102
...
step 119  loss 0.0151  token_acc 1.000
```

## Playing around

```bash
uv run ipython          # interactive REPL
uv run jupyter lab      # notebooks for scratch experiments
```

From a REPL, import and poke at the model:

```python
import torch
from sample import TinyRecursiveModel, deep_supervision_loss

model = TinyRecursiveModel(vocab_size=10, seq_len=81, dim=64, n_heads=4)
print(sum(p.numel() for p in model.parameters()) / 1e6, "M params")
```

Apple Silicon GPU (MPS) is available — move tensors and the model with
`.to("mps")` to use it.

## Layout

- [sample.py](sample.py) — the TRM recursion core + a runnable training smoke test.
- [main.py](main.py) — empty entry point; a scratchpad for your own experiments.

## Dev tooling

```bash
uv run ruff check       # lint
uv run ruff format      # format
```
