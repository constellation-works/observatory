"""Minimal Tiny Recursive Model (TRM) — the recursion core.

Reimplements the central mechanism from Alexia Jolicoeur-Martineau,
"Less is More: Recursive Reasoning with Tiny Networks" (arXiv:2510.04871).

What this captures faithfully
  - A SINGLE shared tiny network (here 2 transformer layers) reused for every
    recursion step. That weight sharing is what keeps the parameter count tiny.
  - Two latent states: ``z`` (low-level scratchpad, never decoded directly) and
    ``y`` (the answer-carrying state, decoded by the output head).
  - The nested recursion inside one improvement step:
        repeat n_inner times:  z <- f(x + y + z)   # refine scratchpad
        once:                  y <- f(y + z)       # refine the answer
    wrapped in n_outer cycles, and the whole thing wrapped in n_sup
    deep-supervision steps, detaching state between supervision steps so each
    step trains against the target from a fresh graph.

What this omits for brevity (see the paper / official repo for the SOTA recipe)
  - Heavy geometric + colour-permutation augmentation, EMA weights, the exact
    ACT halting loss, and test-time ensembling that the headline numbers need.
  - Real ARC I/O encoding (multiple train pairs packed into the context,
    variable grid sizes, padding). Here a sample is one fixed-length grid.

Gradient-scheme note
  This implements the straightforward version: backprop flows through one
  supervision step's recursion, and states are detached *between* supervision
  steps (deep supervision). HRM instead used a 1-step/implicit fixed-point
  gradient; TRM deliberately moved away from that. If you want to mirror the
  memory-saving 1-step variant, wrap the recursion in ``torch.no_grad()`` and
  run a single differentiable update at the end — see ``_refine`` for where.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn


class TinyBlock(nn.Module):
    """One pre-norm transformer block. A small stack of these is the whole net."""

    def __init__(self, dim: int, n_heads: int, mlp_ratio: int = 4) -> None:
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = nn.MultiheadAttention(dim, n_heads, batch_first=True)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, mlp_ratio * dim),
            nn.GELU(),
            nn.Linear(mlp_ratio * dim, dim),
        )

    def forward(self, h: torch.Tensor) -> torch.Tensor:
        normed = self.norm1(h)
        h = h + self.attn(normed, normed, normed, need_weights=False)[0]
        h = h + self.mlp(self.norm2(h))
        return h


class TinyRecursiveModel(nn.Module):
    """The TRM recursion. Decode order: y is the answer, z is the scratchpad."""

    def __init__(
        self,
        vocab_size: int,
        seq_len: int,
        dim: int = 512,
        n_heads: int = 8,
        n_layers: int = 2,
        n_sup: int = 16,     # deep-supervision / improvement steps  (paper: 16)
        n_outer: int = 6,    # outer cycles per supervision step      (n_H)
        n_inner: int = 3,    # inner z refinements per outer cycle     (n_L)
    ) -> None:
        super().__init__()
        self.seq_len = seq_len
        self.n_sup = n_sup
        self.n_outer = n_outer
        self.n_inner = n_inner

        self.token_embed = nn.Embedding(vocab_size, dim)
        self.pos_embed = nn.Parameter(torch.zeros(1, seq_len, dim))
        # The single shared network, reused for every z and y update.
        self.net = nn.ModuleList(TinyBlock(dim, n_heads) for _ in range(n_layers))
        # Normalising the recurrent state keeps it bounded: without this, each
        # update re-adds (x + y + z) onto a residual stream and magnitudes blow
        # up over the many recursion steps.
        self.state_norm = nn.LayerNorm(dim)
        self.output_head = nn.Linear(dim, vocab_size)
        self.halt_head = nn.Linear(dim, 1)
        # Learned initial answer / scratchpad, broadcast over batch and position.
        self.y_init = nn.Parameter(torch.zeros(1, 1, dim))
        self.z_init = nn.Parameter(torch.zeros(1, 1, dim))

        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            nn.init.trunc_normal_(module.weight, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.trunc_normal_(module.weight, std=0.02)

    def _f(self, h: torch.Tensor) -> torch.Tensor:
        for block in self.net:
            h = block(h)
        return self.state_norm(h)

    def _refine(
        self, x: torch.Tensor, y: torch.Tensor, z: torch.Tensor
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """One supervision step's recursion. Returns the updated (y, z).

        For the memory-saving 1-step gradient, run all but the final update
        under ``torch.no_grad()`` and keep only the last ``y <- f(y + z)``
        differentiable.
        """
        for _ in range(self.n_outer):
            for _ in range(self.n_inner):
                z = self._f(x + y + z)   # update scratchpad z given (x, y, z)
            y = self._f(y + z)           # update answer y given (y, z)
        return y, z

    def forward(
        self, input_ids: torch.Tensor
    ) -> list[tuple[torch.Tensor, torch.Tensor]]:
        """Run deep supervision.

        Args:
            input_ids: ``[batch, seq_len]`` integer grid tokens.

        Returns:
            One ``(logits, halt_logit)`` pair per supervision step, where
            ``logits`` is ``[batch, seq_len, vocab]`` and ``halt_logit`` is
            ``[batch, 1]``.
        """
        batch = input_ids.size(0)
        x = self.token_embed(input_ids) + self.pos_embed
        y = self.y_init.expand(batch, self.seq_len, -1).contiguous()
        z = self.z_init.expand(batch, self.seq_len, -1).contiguous()

        outputs: list[tuple[torch.Tensor, torch.Tensor]] = []
        for _ in range(self.n_sup):
            y, z = self._refine(x, y, z)
            logits = self.output_head(y)
            halt_logit = self.halt_head(y.mean(dim=1))
            outputs.append((logits, halt_logit))
            # Deep supervision: next step starts a detached graph.
            y, z = y.detach(), z.detach()
        return outputs

    @torch.no_grad()
    def predict(self, input_ids: torch.Tensor, halt_threshold: float = 0.0):
        """Inference with ACT-style early halting on the halt head."""
        batch = input_ids.size(0)
        x = self.token_embed(input_ids) + self.pos_embed
        y = self.y_init.expand(batch, self.seq_len, -1).contiguous()
        z = self.z_init.expand(batch, self.seq_len, -1).contiguous()

        logits = self.output_head(y)
        for _ in range(self.n_sup):
            y, z = self._refine(x, y, z)
            logits = self.output_head(y)
            if (self.halt_head(y.mean(dim=1)) > halt_threshold).all():
                break
        return logits.argmax(dim=-1)


def deep_supervision_loss(
    outputs: list[tuple[torch.Tensor, torch.Tensor]],
    target: torch.Tensor,
) -> torch.Tensor:
    """Cross-entropy summed over every supervision step.

    Supervising every step (not just the last) is what teaches the model to
    keep improving a partial answer rather than commit early.
    """
    vocab = outputs[0][0].size(-1)
    loss = target.new_zeros((), dtype=torch.float32)
    for logits, _halt in outputs:
        loss = loss + F.cross_entropy(logits.reshape(-1, vocab), target.reshape(-1))
    return loss / len(outputs)


if __name__ == "__main__":
    # Smoke test: can a tiny TRM memorise a fixed grid->grid mapping by
    # iteratively refining its answer? If the recursion + deep supervision are
    # wired correctly, training loss should fall toward zero.
    torch.manual_seed(0)

    vocab_size, seq_len, batch = 10, 81, 8   # 9x9 grids, 10 ARC colours
    model = TinyRecursiveModel(
        vocab_size=vocab_size,
        seq_len=seq_len,
        dim=64,
        n_heads=4,
        n_sup=4,
        n_outer=3,
        n_inner=2,
    )
    n_params = sum(p.numel() for p in model.parameters())
    print(f"parameters: {n_params/1e6:.3f}M")

    inputs = torch.randint(0, vocab_size, (batch, seq_len))
    targets = torch.roll(inputs, shifts=1, dims=1)  # a deterministic transform

    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    for step in range(120):
        outputs = model(inputs)
        loss = deep_supervision_loss(outputs, targets)
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 20 == 0 or step == 119:
            acc = (model.predict(inputs) == targets).float().mean().item()
            print(f"step {step:3d}  loss {loss.item():.4f}  token_acc {acc:.3f}")
