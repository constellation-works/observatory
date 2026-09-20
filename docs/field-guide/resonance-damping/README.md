# Resonance and damping

Chapter 3 of the physics field guide (node `physics-field-guide`). The driven,
damped linear oscillator integrated with RK4, with the steady-state amplitude
and phase, the closed-form underdamped transient, the resonance peak and the
quality factor each checked against an independent Python reference. A
pendulum toggle (extending `research/R002-pendulum-driven/code/`) shows where
the linear model stops describing the motion.

Open it with `make serve` (from the repository root) at
`/docs/field-guide/resonance-damping/index.html`, or from
the gallery at `/_lib/gallery/index.html`. The page needs
HTTP, not `file://`: it imports `../../../_lib/web/*.js` and fetches `chapter.json`
and `validation.json`.

## Files

| file | role |
|---|---|
| `index.html` | the page: wires `_lib/web/chapter.js` and `plot.js` to the chapter's numerics. |
| `resonance.js` | the numerics -- the same code path the page animates, the in-page validation table re-runs, and the Node test checks. |
| `chapter.json` | question, prediction, model, controls, presets, limits, references, source revision. |
| `reference.py` | the independent Python reference (numpy, float64); writes `validation.json`. |
| `validation.json` | generated, and tracked: the page fetches it, and `reference.py --check` keeps it honest. |
| `sim.json` | chapter manifest: title, kind, entry, provenance. Chapters are reference material, not gallery sims. |
| `tests/test_resonance_chapter.py` | runs `resonance.js` under Node against `validation.json` (part of `make test`). |
| `tests/browser_check.py` | headless-Chromium accessibility and layout pass; writes screenshots under the chapter's ignored `output/`. |

## Regenerating and checking

```sh
# reference values (6 validation cases + the dt^4 convergence entry)
uv run docs/field-guide/resonance-damping/reference.py
uv run docs/field-guide/resonance-damping/reference.py --check

# the JS-vs-Python agreement, the physics checks and the chapter contract
uv run --extra research pytest docs/field-guide/resonance-damping/tests

# headless browser: console errors, keyboard operation, 1280 px / 375 px, reduced motion
# (dk-server-1 has no sudo, so Chromium's libraries come from a user directory)
LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
  uv run --with playwright python \
  docs/field-guide/resonance-damping/tests/browser_check.py
```

## What the chapter shows

Driving exactly at omega_0 does not make the amplitude grow without bound:
the transient e^(-zeta t) term decays and x(t) settles onto the steady state
A(omega) cos(omega t - phi), whose height at resonance is fixed by the damping
(A = F/(2 zeta omega_0^2) for small zeta, Q = 1/(2 zeta)). The phase lag
crosses pi/2 exactly at omega = omega_0 for every damping ratio, and the
resonance peak sits slightly below omega_0 at omega_r = omega_0 sqrt(1 - 2
zeta^2), vanishing for zeta >= 1/sqrt(2). The dt^4 convergence entry recovers
RK4's fourth order.

`resonance.js` and `reference.py` execute the same operations in the same
order in float64, so they agree to floating-point roundoff; the declared
browser-vs-Python tolerance (1e-9 relative) is the chapter's kill condition.
The RK4-vs-analytic checks carry their own, looser tolerances (0.5% amplitude,
0.005 rad phase, 1e-6 transient) because they compare a numerical trajectory
with closed-form expressions.

With the pendulum toggle on, the restoring force becomes sin(x) and the
analytic curves on the page no longer apply: large drive amplitudes fold the
response over (the Duffing-like softening spring), which the validation grid
deliberately does not cover.
