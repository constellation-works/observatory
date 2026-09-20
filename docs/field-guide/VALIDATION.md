---
title: Physics field guide — validation record
kind: reference
origin_node: _archive/lineage/nodes/physics-field-guide.md
ran_on: 2026-09-12
verdict: supports
strength: strong
---

# Physics field guide

## What was run

Three browser chapters, each a node-keyed directory under
`docs/field-guide/` with `chapter.json` (the declared
model, controls, presets, validation cases and limits), `reference.py` (the
independent Python reference, float64, which writes `validation.json`),
`index.html` + the chapter's own JavaScript, and `tests/`:

| chapter | question | validation cases |
|---|---|---|
| `orbits-numerical-error` | what integrator choice and step size do to the conserved quantities of a Kepler orbit | 16 |
| `waves-boundaries` | modes, interference and fixed/free reflection on the linear (α = 0) chain | 12 |
| `resonance-damping` | amplitude and phase of a driven damped oscillator against drive and damping | 6 |

Integrated acceptance (ORB-12365, 2026-09-12, 23:34–23:59 UTC, checkout
`d604ff5` — `main` minus the two record commits `7fc678a`/`721f693`) drove all
three in headless Chromium at 1280 px and 375 px:

```sh
LD_LIBRARY_PATH=$HOME/.local/chromium-deps/root/usr/lib/x86_64-linux-gnu \
  uv run --with playwright python \
  docs/field-guide/<chapter>/tests/browser_check.py
uv run --extra research pytest -q docs/field-guide
```

plus a separate acceptance pass written for this milestone (kept outside the
checkout) that does not reuse the chapters' own scripts: console cleanliness,
Tab order against every labelled control, arrow-key operation with a required
change in the plotted numbers, every preset, pause/single-step/reset, the
`prefers-reduced-motion: reduce` path, the on-page validation table against
`validation.json` recomputed through each chapter's own `runCase`, and invalid
parameters through the page's JS handle.

## What came out

- **Numerics.** Every chapter's browser numerics agree with its
  `validation.json` at the declared 1e-9 relative tolerance, worst relative
  difference **0** in all three (16, 12 and 6 cases). The page's verdict line
  and the independent recomputation agree; the on-page table has one row per
  stored case, every row `agrees`, no NaN or empty cell.
- **Browser scripts.** `orbits-numerical-error` 28/28, `waves-boundaries`
  28/28, `resonance-damping` 29/29 checks passed (the 29th is new below).
- **Independent acceptance.** 150/150 checks across the three chapters at both
  widths, including reduced motion: no console or page errors; every labelled
  control reachable by Tab, with presets, transport and the download button in
  the tab order; arrow keys move each control *and* the plotted numbers;
  single step advances exactly one step and reset returns to step 0; under
  `prefers-reduced-motion` the static path completes (`animating=false`,
  `steps == totalSteps`), Play and Single step are disabled, and the same
  observable is reported.
- **`make check`** was green at the delivered tree: 344 passed, 5 skipped; the
  then-current lineage check reported 10 nodes, 0 errors, 6 warnings (all
  pre-existing evidence-locator spellings, unchanged by that work). `ruff check`
  clean. That gate has since been replaced by `_scripts/check.py`.

### One plotted number per chapter, traced

| chapter | plotted number | chapter.json | JavaScript | reference.py |
|---|---|---|---|---|
| orbits | `max_rel_energy_error = 0.6398398999136308`, the table's *max ΔE/E₀* column (v₀ = 1.0, Δt = 0.05, explicit Euler, 10 periods) | equation *Specific energy* `E = v²/2 − 1/r` | `orbits.js:60` `specificEnergy`, accumulated in `createRun`'s observer (`orbits.js:163–168`) and surfaced by `summary()` (`orbits.js:214`) | `reference.py:135` `specific_energy`, reported at `reference.py:240` as `max_rel_energy_error` |
| waves | `period_measured = 64.0254523925434` (mode 1, N = 32, Δt = 0.1) | equation *Normal-mode frequency* `ω_k = 2 sin(πk/2N)` | `waves.js:46` `modeFrequency`, used by `dispersionCase` (`waves.js:153–160`) | `reference.py:115` `mode_frequency`, measured at `reference.py:223` `zero_crossing_period` |
| resonance | `A_analytic = 3` (ω = ω₀ = 1, ζ = 0.05, F = 0.3) | equation *Steady-state amplitude* `A(ω) = F/√((ω₀²−ω²)² + (2ζω₀ω)²)` | `resonance.js:20–28` `analyticAmplitudePhase` | `reference.py:83–91` `analytic_amplitude_phase` |

### Two defects found and fixed here

- **Invalid parameters returned NaNs instead of a constraint message.** The
  sliders clamp themselves, but `window.__chapter.runCase` accepted anything:
  ζ = 0, ω = 0 or Δt = 0 produced `NaN` amplitudes and phases, mode 99 on a
  32-mass chain integrated silently. `checkParameters` in
  `_lib/web/chapter.js` now validates an argument against the range
  `chapter.json` declares for that control (plus a small per-chapter bound for
  arguments that are not controls) and throws a message naming the control,
  the value and the range — e.g. *“zeta (damping ratio ζ) = 0 is outside the
  allowed range [0.01, 1.5]”*. Each chapter's JS handle is wired through it,
  and each chapter's test file exercises the guard under Node.
- **A preset could land on the nearest slider notch.** `ζ = 0.02` and
  `ζ = 1.2` are not on the log-range slider's step grid, so the *Light damping
  at resonance* and *Heavy damping* presets applied 0.0199526… and 1.20226…
  (Q = 25.06 rather than the labelled 25). `applyPreset` now lifts the step
  for the assignment, so the model and the readout get the declared value and
  the arrow keys keep their declared granularity. The resonance chapter's
  browser script gained a check that pins this.

## What is shaky

- The 1e-9 agreement is between two implementations of the *same* algorithm in
  float64 (each chapter's `validation.json` says so in its `rationale`). It
  bounds transcription error, not modelling error; the physics tolerances —
  the dispersion-relation comparison, the steady-state and transient
  tolerances, the convergence orders — are separate and looser, and they are
  what would catch a wrong model.
- The reference values are regenerated by `reference.py` at a recorded
  revision; a chapter edited without regenerating `validation.json` would be
  caught by `test_validation_file_is_current`, but nothing pins the reference
  to an *independent author* — the same person wrote both sides.
- After a preset that is off the slider's step grid, the slider element itself
  re-snaps to its nearest notch while the model and the readout hold the exact
  value, so the thumb can sit a fraction of a step from the reported number
  until the control is next moved.
- The chapters run their physics in the browser at interactive step counts;
  the reduced-motion path completes the same run without animating, but very
  long runs are still bounded by what a page can do in a frame budget.
- `resonance-damping`'s nonlinear (pendulum) toggle has no analytic reference:
  its validation cases are the linear model only, and the foldover preset is
  qualitative.

## Next

The chapters ship as a shareable tree via `_scripts/export-field-guide.sh`
(allowlisted; 41 files, no `knowledgebase/`, `_data`, `.orbit`, `.env*`, no
absolute paths, no secret-looking strings; all three chapters and the FPUT
study report open over relative links when the directory is served
statically). A fourth chapter should reuse the same contract rather than
extend the shared apparatus; anything that needs a new control type belongs in
`_lib/web/panel.js` with the same keyboard guarantees.
