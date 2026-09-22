# Waves, interference and boundaries

Chapter 2 of the physics field guide (node `physics-field-guide`). The linear
N-mass chain -- the alpha = 0 case of the FPUT model reproduced in
`experiments/physics/fput-recurrence-reproduction/` -- integrated with
Stormer-Verlet. Standing waves, two counter-propagating pulses, and reflection
off a fixed versus a free end, with every predefined validation point checked
against an independent Python reference.

Open it with `make serve` (from the repository root) at
`/experiments/physics/physics-field-guide/waves-boundaries/index.html`, or from
the gallery at `/experiments/physics/_lib/gallery/index.html`. The page needs
HTTP, not `file://`: it imports `../../_lib/web/*.js` and fetches `chapter.json`
and `validation.json`.

## Files

| file | role |
|---|---|
| `index.html` | the page: wires `_lib/web/chapter.js` and `plot.js` to the chapter's numerics. |
| `waves.js` | the numerics -- the same code path the page animates, the in-page validation table re-runs, and the Node test checks. |
| `chapter.json` | question, prediction, model, controls, presets, limits, references, source revision. |
| `reference.py` | the independent Python reference (numpy, float64); writes `validation.json`. |
| `validation.json` | generated, and tracked: the page fetches it, and `reference.py --check` keeps it honest. |
| `sim.json` | gallery entry (`make gallery`). |
| `tests/test_waves_chapter.py` | runs `waves.js` under Node against `validation.json` (part of `make test`). |
| `tests/browser_check.py` | headless-Chromium accessibility and layout pass; writes screenshots under `_outputs/`. |

## Regenerating and checking

```sh
# reference values (12 validation cases + the dt^2 convergence entry)
uv run experiments/physics/physics-field-guide/waves-boundaries/reference.py
uv run experiments/physics/physics-field-guide/waves-boundaries/reference.py --check

# the JS-vs-Python agreement, the physics checks and the chapter contract
uv run --extra research pytest experiments/physics/physics-field-guide/waves-boundaries/tests

# headless browser: console errors, keyboard operation, 1280 px / 375 px, reduced motion
# (dk-server-1 has no sudo, so Chromium's libraries come from a user directory)
LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
  uv run --with playwright python \
  experiments/physics/physics-field-guide/waves-boundaries/tests/browser_check.py
```

`validation.json` is byte-identical across runs apart from `source_revision`,
which `--check` ignores.

## What the chapter shows

The chain is exactly linear (alpha = 0), so superposition is exact: two pulses
launched toward each other add pointwise, doubling at the crossing when they
are in phase and cancelling when they are in antiphase, and the validation
table confirms the combined run agrees with the linear sum of the two pulses
run separately to floating-point roundoff. A pulse reflecting off the always
present left wall or a fixed right wall comes back inverted; off a free right
wall it comes back upright. Standing-wave modes k = 1..8 recover the analytic
dispersion relation omega_k = 2 sin(pi k / 2N) to well under the declared 1%,
and the dt^2 convergence entry recovers Stormer-Verlet's second order.

`waves.js` and `reference.py` execute the same operations in the same order in
float64, so they currently agree to floating-point roundoff (worst relative
difference on the order of 1e-15); the declared tolerance is 1e-9 relative /
1e-9 absolute, which is the chapter's kill condition for the browser-vs-Python
check. The measured-period-vs-analytic-dispersion check is a separate, looser
1% tolerance, because Stormer-Verlet carries an O(dt^2) discretisation error
that the closed-form dispersion relation does not.

The FPUT reproduction study
(`knowledgebase/studies/physics/fput-recurrence-reproduction.md`) runs the same
chain with a small cubic term (alpha = 1/4) added: that is the case where
superposition stops being exact and modes exchange energy, which nothing in
this chapter (alpha = 0, by construction) can show.
