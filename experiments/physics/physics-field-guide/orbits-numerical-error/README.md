# Orbits and numerical error

Chapter 1 of the physics field guide (node `physics-field-guide`). The Kepler
two-body problem integrated four ways, with the energy and angular-momentum
error plotted against the analytic ellipse, and every predefined validation
point checked against an independent Python reference.

Open it with `make serve` (from the repository root) at
`/experiments/physics/physics-field-guide/orbits-numerical-error/index.html`, or
from the gallery at `/experiments/physics/_lib/gallery/index.html`. The page
needs HTTP, not `file://`: it imports `../../_lib/web/*.js` and fetches
`chapter.json` and `validation.json`.

## Files

| file | role |
|---|---|
| `index.html` | the page: wires `_lib/web/chapter.js` and `plot.js` to the chapter's numerics. |
| `orbits.js` | the numerics — the same code path the page animates, the in-page validation table re-runs, and the Node test checks. |
| `chapter.json` | question, prediction, model, controls, presets, limits, references, source revision. |
| `reference.py` | the independent Python reference (numpy, float64); writes `validation.json`. |
| `validation.json` | generated, and tracked: the page fetches it, and `reference.py --check` keeps it honest. |
| `sim.json` | gallery entry (`make gallery`). |
| `tests/test_orbits_chapter.py` | runs `orbits.js` under Node against `validation.json` (part of `make test`). |
| `tests/browser_check.py` | headless-Chromium accessibility and layout pass; writes screenshots under `_outputs/`. |

## Regenerating and checking

```sh
# reference values (16 validation cases + the convergence table)
uv run experiments/physics/physics-field-guide/orbits-numerical-error/reference.py
uv run experiments/physics/physics-field-guide/orbits-numerical-error/reference.py --check

# the JS-vs-Python agreement, the convergence orders and the chapter contract
uv run --extra research pytest experiments/physics/physics-field-guide/orbits-numerical-error/tests

# headless browser: console errors, keyboard operation, 1280 px / 375 px, reduced motion
# (dk-server-1 has no sudo, so Chromium's libraries come from a user directory)
LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
  uv run --with playwright python \
  experiments/physics/physics-field-guide/orbits-numerical-error/tests/browser_check.py
```

`validation.json` is byte-identical across runs apart from `source_revision`,
which `--check` ignores.

## What the chapter shows

Explicit Euler gains energy secularly and spirals out at any step size; the two
symplectic schemes hold the energy error in a bounded oscillation and conserve
angular momentum to roundoff; RK4 is far more accurate over ten periods but
drifts rather than oscillating. The convergence table recovers Δt¹ for both
Euler schemes, Δt² for leapfrog and Δt⁴ for RK4 from `reference.py`.

`orbits.js` and `reference.py` execute the same operations in the same order in
float64, so they currently agree bit for bit (worst relative difference 0); the
declared tolerance is 1e-9 relative, which is the chapter's kill condition.
