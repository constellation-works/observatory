# `_lib` — shared apparatus

Underscore-prefixed directories are apparatus, not research content (see
[AGENTS.md](../AGENTS.md)): this one holds the harness every sim and field-guide
chapter imports. Nothing here belongs to one research item, and nothing here may
import from one.

```text
_lib/astrolabe/  the celestial data collection and analysis library (a uv workspace member)
_lib/web/        browser modules, imported relatively — see below
_lib/templates/  `new-sim.sh` scaffolding for a bare sim
_lib/tools/      build-gallery.py, serve.sh, new-sim.sh
_lib/gallery/    generated sim catalog (make gallery / make check-gallery)
_lib/vendor/     third-party bundles
```

Everything is served from the repository root (`make serve`), so a page's imports
are relative to where it lives:

| page | prefix |
|---|---|
| a sim at `research/<R###-slug>/code/<slug>/` | `../../../../_lib/web/plot.js` |
| a chapter at `docs/field-guide/<chapter>/` | `../../../_lib/web/plot.js` |

The examples below use the sim form.

## The sim harness

| module | what it gives you |
|---|---|
| `loop.js` | `createLoop({ step, render, dt, speed })` — fixed-timestep rAF loop with play/pause. |
| `panel.js` | `createPanel(defs, { mount, className })` — declarative range / select / toggle / button / readout controls. |
| `canvas2d.js` | DPR-aware canvas, pan/zoom camera, HUD overlay. |
| `integrators.js` | `explicitEuler`, `semiImplicitEuler`, `leapfrogKDK`, `rk4`, `nBodyGravity` over flat `Float64Array` state. |
| `vec.js` | small vector helpers. |
| `style.css` | the shared dark theme and `.orrery-controls`. |

`panel.js` is accessible by construction and chapters rely on it: every labelled
control gets a generated id with a matching `<label for>`, the value readout is
an `aria-live="polite"` region referenced by `aria-describedby`, toggles carry
`aria-pressed`, and the controls are native `input` / `select` / `button`
elements, so Tab, arrow keys, Enter and Space work with no extra key handling.

## The chapter apparatus

`plot.js`, `chapter.js` and `chapter.css` are the field-guide chapter contract.
A chapter supplies its physics and its `chapter.json`; these three supply the
page. The exemplar is
[`docs/field-guide/orbits-numerical-error/`](../docs/field-guide/orbits-numerical-error/);
the remaining chapters reuse these modules unchanged.

### `plot.js`

```js
import { createPlot, plotsToSVG, SERIES_COLORS } from '../../../../_lib/web/plot.js';

const plot = createPlot({
  mount,                 // element the <figure> is appended to
  title,                 // figcaption above the canvas
  xLabel, yLabel,        // axis titles — always carry the units
  logY: false,           // log10 y-axis with decade ticks
  equalAspect: false,    // one world unit is the same pixel count on both axes
  logDecades: 14,        // cap on the decades a log axis spans
  height: 260,           // CSS pixels; the width fills the mount
  legend: true,
});

plot.setSeries([
  { id: 'energy', label: '|E(t) − E₀| / |E₀|', points: [[x, y], ...],
    style: 'solid' | 'dashed' | 'dotted' | 'dash-dot',
    color: SERIES_COLORS[0], width: 2, marker: false, hidden: false },
]);
plot.draw();                      // call after setSeries and on new data
plot.setTitle(str);
plot.setAxisLabels({ x, y });
plot.setDescription(str);         // visually hidden text for screen readers
const svg = plot.toSVG();         // the same drawing, as a standalone SVG string
const sheet = plotsToSVG([a, b]); // several plots stacked into one SVG
```

Canvas and SVG go through one drawing backend, so the downloaded figure is the
drawing on screen rather than a second implementation of it. Non-finite points
and (under `logY`) non-positive points break the line instead of dropping the
series. Resize is handled internally.

`SERIES_COLORS` is the categorical order validated against the `#050510`
surface (blue, orange, aqua, yellow; adjacent CVD ΔE ≥ 8.4, normal-vision
ΔE ≥ 19.8, contrast ≥ 3:1). **Colour is never the only channel**: give each
series a line style, and the legend and axis labels carry the meaning.

### `chapter.json`

The schema is fixed by
[`docs/design/paper-reproduction-workbench.md`](../docs/design/paper-reproduction-workbench.md);
`chapter.js` renders these fields and `tests/test_orbits_chapter.py` asserts
the required ones are present.

| field | contract |
|---|---|
| `title`, `summary` | page heading and lede. |
| `question` | the falsifiable or measurable question, stated before anything moves. |
| `prediction_prompt` | the ask. |
| `prediction_options` | three `{ id, label, feedback }` radio options; the run starts once one is recorded. |
| `model` | `{ summary, state_variables, units, equations: [{ name, text, note }], assumptions }`. |
| `controls` | 2–4 entries of `{ key, type, label, default, unit, ... }`; `type` is `range`, `log-range` (min/max/step in the parameter, driven in log10 space) or `select` (`options: [{ value, label }]`). |
| `presets` | `[{ id, label, note, values: { <control key>: value } }]`; preset values should be representable by the control's step. |
| `explanation` / `explanation_title` | optional prose section, `[{ heading, body }]`. |
| `validation_cases` | the predefined points, their observables and the declared `tolerance` with its rationale. |
| `limits` | where the model stops applying, as a list. |
| `references` | `[{ citation, url, note }]` — primary sources. |
| `source_revision` | `{ kind, revision, note }`. |

### `chapter.js`

```js
import { loadChapter, renderChapter, validateChapter, downloadSVG, formatNumber }
  from '../../../_lib/web/chapter.js';

const { chapter, validation } = await loadChapter();   // chapter.json + validation.json
const ui = renderChapter({ mount, chapter, validation, hooks: {
  onPrediction(id) {},          // a prediction was recorded — start the run
  onControlChange(key, value, values) {},
  onPreset(preset, values) {},  // fired once per preset, not once per control
  onReset() {}, onStep() {}, onTogglePlay() { return playing; },
  onMotionChange(animate) {},   // false: render the static path instead
  onDownload() {},              // wire to plotsToSVG + downloadSVG
}});

ui.regions.sim / ui.regions.plots   // where the chapter mounts its plots
ui.values                           // current control values, keyed as in chapter.json
ui.setStatus(text); ui.setPlaying(bool); ui.applyPreset(preset);
ui.showValidation(result);          // renders the comparison table and the verdict
```

`renderChapter` emits, in order: header, question + prediction, model, controls
(model controls, presets, transport: play/pause, single step, reset, and the
reduced-motion toggle), the sim/plot grid, the optional explanation, the
validation evidence and convergence tables, the limits, and the references with
the source revision and the static-figure download.

Reduced motion: the initial state follows `prefers-reduced-motion`, the visible
toggle wins over it, and `onMotionChange(false)` means *render the finished
static result with the same numbers*, never *drop the result*. Play and single
step are disabled on that path.

### `validate()` — the chapter's own numerics against its reference

```js
const result = validateChapter(validation, (c) => runCase(c) /* same code path as the sim */);
ui.showValidation(result);
```

`validateChapter(validation, compute, { fields, tolerance })` compares every
case in `validation.json` with the chapter's JavaScript and returns
`{ tolerance, pass, worst_relative_difference, rows }`. It touches no DOM, so a
headless Node runner can import it and check a chapter without a browser — which
is what `tests/test_orbits_chapter.py` does.

### `chapter.css`

Loaded after `style.css`. Two-column sim/plot grid, one column below 720 px,
stacked full-width controls below 480 px with no horizontal scrolling at 375 px,
visible `:focus-visible` rings, and the `.fg-*` classes the modules emit.

## Building a new chapter

1. `docs/field-guide/<chapter>/` — chapters are reference material about
   established physics, not research records, so they live under `docs/`.
2. Write `reference.py` (independent, numpy, float64) and generate
   `validation.json`. Mirror its arithmetic in the chapter's JavaScript module
   and declare a tolerance with a rationale in `chapter.json`.
3. Write `chapter.json`, then an `index.html` that wires `renderChapter` to
   `createPlot` and the chapter's own numerics.
4. Add `sim.json` (`kind: web`, `provenance` naming the reference sources). Only
   sims under a research item appear in the gallery; a chapter's `sim.json` is its
   own manifest.
5. Copy the chapter's `tests/` — `test_orbits_chapter.py` for the Node check and
   `browser_check.py` for the headless-Chromium accessibility pass.
6. `make check`.
