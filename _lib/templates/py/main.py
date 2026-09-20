"""__TITLE__

What this models, what question it answers, and which hypothesis it bears on go
here — the docstring is the sim's abstract. The research item's README is where
the result is written up.

Usage: uv run research/<R###-slug>/code/__SLUG__/main.py
"""

import numpy as np

r = np.random.default_rng(42)
N = 1_000_000

# --- replace below with the actual model -----------------------------------
pts = r.uniform(-1, 1, size=(N, 2))
inside = (pts**2).sum(axis=1) < 1
pi_est = 4 * inside.mean()

print(f"N = {N:,}")
print(f"pi estimate = {pi_est:.5f}  (error {abs(pi_est - np.pi):.2e})")
