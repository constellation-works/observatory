# arc

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
