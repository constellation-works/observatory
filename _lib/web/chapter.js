// Renders a field-guide chapter from its chapter.json + validation.json, and
// compares a chapter's own JavaScript numerics against that validation file.
//
// The contract (chapter.json fields, hooks, regions) is documented in
// _lib/README.md. A chapter supplies the physics; this
// module supplies the page: question and prediction, model, keyboard-accessible
// controls, the sim/plot grid, the validation evidence table, limits,
// references, source revision and the static-figure download.
//
//   const { chapter, validation } = await loadChapter();
//   const ui = renderChapter({ mount: document.body, chapter, validation, hooks });
//   ui.regions.sim / ui.regions.plots      // where the chapter draws
//   ui.values.v0                           // current control values
//
// Nothing here touches the DOM at import time, so a headless runner (Node) can
// import validateChapter() and check a chapter without a browser.

import { createPanel } from './panel.js';

// --- numbers --------------------------------------------------------------
export function formatNumber(v, digits = 4) {
  if (v === null || v === undefined || Number.isNaN(v)) return '—';
  if (v === 0) return '0';
  const a = Math.abs(v);
  if (a < 1e-3 || a >= 1e5) return v.toExponential(digits - 1);
  return String(Number(v.toPrecision(digits)));
}

export function relativeDifference(actual, expected) {
  const denom = Math.abs(expected);
  if (denom === 0) return Math.abs(actual);
  return Math.abs(actual - expected) / denom;
}

// --- validation -----------------------------------------------------------
// `compute(case)` returns an object with the same keys as the stored case.
// Returns one row per stored case with the worst relative difference over the
// compared fields, so a chapter's page and its headless test share one verdict.
export function validateChapter(validation, compute, { fields, tolerance } = {}) {
  const tol = tolerance ?? validation.tolerance?.relative ?? 1e-9;
  const abs = validation.tolerance?.absolute ?? 0;
  const keys = fields ?? [
    'max_rel_energy_error',
    'final_rel_energy_error',
    'max_rel_angular_momentum_error',
    'final_position_error',
  ];
  const rows = validation.cases.map((expected) => {
    const actual = compute(expected);
    let worst = 0;
    let worstField = null;
    const compared = {};
    for (const key of keys) {
      if (typeof expected[key] !== 'number' || typeof actual[key] !== 'number') continue;
      const diff = Math.abs(actual[key] - expected[key]);
      const rel = diff <= abs ? 0 : relativeDifference(actual[key], expected[key]);
      compared[key] = { expected: expected[key], actual: actual[key], relative_difference: rel };
      if (rel > worst) { worst = rel; worstField = key; }
    }
    return {
      case: expected,
      compared,
      worst_relative_difference: worst,
      worst_field: worstField,
      pass: worst <= tol,
    };
  });
  return {
    tolerance: tol,
    absolute_tolerance: abs,
    rows,
    pass: rows.every((r) => r.pass),
    worst_relative_difference: rows.reduce((m, r) => Math.max(m, r.worst_relative_difference), 0),
  };
}

// --- parameter constraints -------------------------------------------------
// The sliders clamp themselves, but a chapter's runCase() is also reachable from
// the page's JS handle (window.__chapter) and from anything embedding the module.
// A value outside the range chapter.json declares is refused with a message that
// names the control, the value and the range, so a caller gets a constraint message
// instead of a result full of NaNs. `extra` declares bounds for arguments that are
// not controls (a case's step size, say), in the same {min, max, label} shape.
export function checkParameters(chapter, values, extra = {}) {
  const bounds = {};
  for (const c of chapter.controls ?? []) {
    bounds[c.key] = c.type === 'select'
      ? { label: c.label, options: c.options.map((o) => (typeof o === 'string' ? o : o.value)) }
      : { label: c.label, min: c.min, max: c.max, unit: c.unit };
  }
  for (const [key, def] of Object.entries(extra)) bounds[key] = { ...(bounds[key] ?? {}), ...def };
  for (const [key, value] of Object.entries(values ?? {})) {
    const b = bounds[key];
    if (!b) continue;
    const name = b.label ? `${key} (${b.label})` : key;
    if (b.options) {
      if (!b.options.includes(value)) {
        throw new Error(`${name} = ${JSON.stringify(value)} is not one of: ${b.options.join(', ')}`);
      }
      continue;
    }
    if (typeof value !== 'number' || !Number.isFinite(value)) {
      throw new Error(`${name} = ${value} is not a finite number`);
    }
    if (value < b.min || value > b.max) {
      const unit = b.unit && b.unit !== 'dimensionless' ? ` ${b.unit}` : '';
      throw new Error(`${name} = ${value}${unit} is outside the allowed range [${b.min}, ${b.max}]${unit}`);
    }
  }
  return values;
}

export async function loadChapter({ chapterUrl = 'chapter.json', validationUrl = 'validation.json' } = {}) {
  const [chapter, validation] = await Promise.all([
    fetch(chapterUrl).then((r) => r.json()),
    fetch(validationUrl).then((r) => r.json()),
  ]);
  return { chapter, validation };
}

// --- small DOM helpers ----------------------------------------------------
function h(tag, attrs = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === undefined || v === null) continue;
    if (k === 'class') el.className = v;
    else if (k === 'html') el.innerHTML = v;
    else if (k === 'text') el.textContent = v;
    else el.setAttribute(k, v);
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined) continue;
    el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return el;
}

function section(id, title) {
  const el = h('section', { class: 'fg-section', id });
  el.append(h('h2', { text: title }));
  return el;
}

// Exported so a chapter can render its own extra evidence (e.g. a convergence
// entry with a shape `showValidation`'s default columns don't cover) into
// `ui.regions.validation` without a second table implementation.
export { h, table };

function table(headers, rows, { caption } = {}) {
  const t = h('table', { class: 'fg-table' });
  if (caption) t.append(h('caption', { text: caption }));
  const thead = h('thead');
  thead.append(h('tr', {}, headers.map((x) => h('th', { scope: 'col', text: x }))));
  const tbody = h('tbody');
  for (const row of rows) {
    tbody.append(h('tr', { class: row.cls ?? null }, (row.cells ?? row).map(
      (c, i) => h(i === 0 ? 'th' : 'td', i === 0 ? { scope: 'row' } : {},
        c instanceof Node ? c : String(c)))));
  }
  t.append(thead, tbody);
  return t;
}

// --- controls -------------------------------------------------------------
// chapter.json control types map onto panel.js defs. 'log-range' drives the
// native range input in log10 space so the slider stays keyboard-operable with
// arrow keys while the model sees a logarithmic parameter.
function buildControls(chapter, mount, emit) {
  const defs = [];
  const meta = {};
  for (const c of chapter.controls) {
    const unit = c.unit && c.unit !== 'dimensionless' ? ` ${c.unit}` : '';
    if (c.type === 'log-range') {
      const lo = Math.log10(c.min);
      const hi = Math.log10(c.max);
      meta[c.key] = { def: c, log: true };
      defs.push({
        type: 'range', key: c.key, label: c.label,
        min: lo, max: hi, step: c.step ?? (hi - lo) / 100,
        value: Math.log10(c.default),
        format: (v) => `${formatNumber(Math.pow(10, v), 3)}${unit}`,
        onChange: (v) => emit(c.key, Math.pow(10, v)),
      });
    } else if (c.type === 'select') {
      meta[c.key] = { def: c };
      defs.push({
        type: 'select', key: c.key, label: c.label,
        options: c.options.map((o) => (typeof o === 'string' ? o : { value: o.value, label: o.label })),
        value: c.default,
        onChange: (v) => emit(c.key, v),
      });
    } else {
      meta[c.key] = { def: c };
      defs.push({
        type: 'range', key: c.key, label: c.label,
        min: c.min, max: c.max, step: c.step ?? 'any', value: c.default,
        format: (v) => `${formatNumber(v, 3)}${unit}`,
        onChange: (v) => emit(c.key, v),
      });
    }
  }
  const panel = createPanel(defs, { mount, className: 'orrery-controls fg-controls' });
  return { panel, meta };
}

// --- the page -------------------------------------------------------------
export function renderChapter({ mount, chapter, validation, hooks = {} }) {
  const root = h('article', { class: 'fg-chapter' });
  const values = {};

  // Header
  const header = h('header', { class: 'fg-header' },
    h('h1', { text: chapter.title }),
    chapter.summary ? h('p', { class: 'fg-lede', text: chapter.summary }) : null);
  root.append(header);

  // 1. Question and prediction, before anything moves.
  const qs = section('question', 'The question');
  qs.append(h('p', { class: 'fg-question', text: chapter.question }));
  const fieldset = h('fieldset', { class: 'fg-prediction' });
  fieldset.append(h('legend', { text: chapter.prediction_prompt }));
  const name = 'fg-prediction';
  for (const opt of chapter.prediction_options ?? []) {
    const id = `pred-${opt.id}`;
    const row = h('div', { class: 'fg-radio' },
      h('input', { type: 'radio', id, name, value: opt.id }),
      h('label', { for: id, text: opt.label }));
    fieldset.append(row);
  }
  const predictionNote = h('p', { class: 'fg-note', role: 'status', 'aria-live': 'polite',
    text: 'Pick a prediction to start the simulation.' });
  const startBtn = h('button', { type: 'button', class: 'fg-primary', text: 'Record prediction and run' });
  fieldset.append(startBtn, predictionNote);
  qs.append(fieldset);
  root.append(qs);

  startBtn.addEventListener('click', () => {
    const picked = fieldset.querySelector('input[name="' + name + '"]:checked');
    if (!picked) { predictionNote.textContent = 'Pick one of the three options first.'; return; }
    const opt = (chapter.prediction_options ?? []).find((o) => o.id === picked.value);
    predictionNote.textContent = `Recorded: “${opt.label}”. ${opt.feedback ?? ''}`;
    startBtn.textContent = 'Run again';
    hooks.onPrediction?.(picked.value);
  });

  // 2. Model
  const ms = section('model', 'The model');
  const m = chapter.model;
  if (m.summary) ms.append(h('p', { text: m.summary }));
  if (m.equations?.length) {
    const dl = h('dl', { class: 'fg-equations' });
    for (const eq of m.equations) {
      dl.append(h('dt', { text: eq.name }), h('dd', {},
        h('code', { class: 'fg-eq', text: eq.latex ?? eq.text }),
        eq.note ? h('span', { class: 'fg-note', text: ` ${eq.note}` }) : null));
    }
    ms.append(dl);
  }
  if (m.state_variables?.length) {
    ms.append(h('p', { class: 'fg-note' },
      h('strong', { text: 'State: ' }), m.state_variables.join(', ')));
  }
  if (m.units) ms.append(h('p', { class: 'fg-note' }, h('strong', { text: 'Units: ' }), m.units));
  if (m.assumptions?.length) {
    ms.append(h('p', { class: 'fg-note', text: 'Assumptions:' }),
      h('ul', { class: 'fg-list' }, m.assumptions.map((a) => h('li', { text: a }))));
  }
  root.append(ms);

  // 3. Controls + simulation + plots
  const es = section('explore', 'Explore');
  const controlsMount = h('div', { class: 'fg-controls-region' });
  es.append(controlsMount);
  // While a preset is being applied the individual control changes are recorded
  // but not announced, so the chapter restarts once rather than once per control.
  let applyingPreset = false;
  const emit = (key, value) => {
    values[key] = value;
    if (applyingPreset) return;
    hooks.onControlChange?.(key, value, values);
  };
  const { panel } = buildControls(chapter, controlsMount, emit);
  for (const c of chapter.controls) {
    values[c.key] = c.type === 'log-range' ? c.default : (c.type === 'select' ? c.default : c.default);
  }

  // Presets and transport share the control region and the same panel styling.
  const presetMount = h('div', { class: 'orrery-controls fg-controls fg-presets' });
  presetMount.append(h('span', { class: 'fg-group-label', id: 'fg-preset-label', text: 'Presets' }));
  presetMount.setAttribute('role', 'group');
  presetMount.setAttribute('aria-labelledby', 'fg-preset-label');
  for (const p of chapter.presets ?? []) {
    const b = h('button', { type: 'button', text: p.label, title: p.note ?? null });
    b.addEventListener('click', () => applyPreset(p));
    presetMount.append(b);
  }
  controlsMount.append(presetMount);

  const transport = h('div', { class: 'orrery-controls fg-controls fg-transport', role: 'group',
    'aria-label': 'Simulation transport' });
  const playBtn = h('button', { type: 'button', text: 'Pause', 'aria-pressed': 'true' });
  const stepBtn = h('button', { type: 'button', text: 'Single step' });
  const resetBtn = h('button', { type: 'button', text: 'Reset' });
  const motionBtn = h('button', { type: 'button', text: 'Animation' });
  transport.append(playBtn, stepBtn, resetBtn, motionBtn);
  controlsMount.append(transport);

  const status = h('p', { class: 'fg-status', role: 'status', 'aria-live': 'polite' });
  es.append(status);

  const grid = h('div', { class: 'fg-grid' });
  const simRegion = h('div', { class: 'fg-panel fg-sim' });
  const plotRegion = h('div', { class: 'fg-panel fg-plots' });
  grid.append(simRegion, plotRegion);
  es.append(grid);
  root.append(es);

  function applyPreset(p) {
    applyingPreset = true;
    try {
      for (const [k, v] of Object.entries(p.values)) {
        const def = chapter.controls.find((c) => c.key === k);
        if (!def) continue;
        const raw = def.type === 'log-range' ? Math.log10(v) : v;
        const input = panel.element(k);
        // A range input snaps to its own step grid, so a preset value that falls
        // between two steps would silently land somewhere else — a preset labelled
        // ζ = 0.02 must apply ζ = 0.02, not the nearest slider notch. The step is
        // lifted for the assignment and restored, so the arrow keys keep their
        // declared granularity.
        const step = input && input.tagName === 'INPUT' ? input.step : null;
        if (step && step !== 'any') input.step = 'any';
        // panel.set dispatches the control's own event, so the slider, its
        // readout and `values` stay in step with the value that was applied.
        panel.set(k, raw);
        if (step && step !== 'any') input.step = step;
      }
    } finally {
      applyingPreset = false;
    }
    hooks.onPreset?.(p, values);
  }

  // Reduced motion: the visible toggle wins over the media query, and the
  // chapter is told which path to take rather than the animation being removed.
  const media = typeof window !== 'undefined' && window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  let animate = !(media && media.matches);
  function paintMotion() {
    motionBtn.setAttribute('aria-pressed', String(animate));
    motionBtn.classList.toggle('active', animate);
    motionBtn.textContent = animate ? 'Animation: on' : 'Animation: reduced (static)';
    playBtn.disabled = !animate;
    stepBtn.disabled = !animate;
  }
  motionBtn.addEventListener('click', () => {
    animate = !animate;
    paintMotion();
    hooks.onMotionChange?.(animate);
  });
  paintMotion();
  media?.addEventListener?.('change', (ev) => {
    animate = !ev.matches;
    paintMotion();
    hooks.onMotionChange?.(animate);
  });

  let playing = true;
  playBtn.addEventListener('click', () => {
    playing = hooks.onTogglePlay?.() ?? !playing;
    playBtn.textContent = playing ? 'Pause' : 'Play';
    playBtn.setAttribute('aria-pressed', String(playing));
  });
  stepBtn.addEventListener('click', () => hooks.onStep?.());
  resetBtn.addEventListener('click', () => hooks.onReset?.());

  // 4. What the controls do to the result (optional, chapter-supplied prose).
  if (chapter.explanation?.length) {
    const xs = section('explanation', chapter.explanation_title ?? 'What you should see');
    for (const item of chapter.explanation) {
      if (item.heading) xs.append(h('h3', { text: item.heading }));
      for (const para of [].concat(item.body)) xs.append(h('p', { text: para }));
    }
    root.append(xs);
  }

  // 5. Validation evidence
  const vs = section('validation', 'Validation evidence');
  vs.append(h('p', {},
    'Every number in the first three value columns is read from ',
    h('code', { text: 'validation.json' }),
    ', written by the independent Python reference (',
    h('code', { text: 'reference.py' }),
    `, float64, revision ${validation.source_revision}). The browser re-runs the same
     cases in this page and the last column reports the worst relative difference
     between the two implementations.`));
  const vStatus = h('p', { class: 'fg-status', role: 'status', 'aria-live': 'polite',
    text: 'Validation: not run yet.' });
  const vTableMount = h('div', { class: 'fg-table-wrap' });
  vs.append(vStatus, vTableMount);

  const convergence = validation.convergence;
  if (convergence) {
    vs.append(h('h3', { text: 'Convergence order' }));
    vs.append(h('p', { class: 'fg-note', text: convergence.note ?? '' }));
    const dts = convergence.rows[0].dts;
    const headers = ['integrator', ...dts.map((d) => `Δt = ${d}`),
      'order (|Δx|)', 'order (|ΔE|)', 'expected'];
    const rows = convergence.rows.map((r) => [
      r.integrator,
      ...r.position_errors.map((e) => formatNumber(e, 3)),
      r.observed_order_position.toFixed(2),
      r.observed_order_energy.toFixed(2),
      String(r.expected_order),
    ]);
    vs.append(h('div', { class: 'fg-table-wrap' }, table(headers, rows, {
      caption: `Final position error |Δx| (units of r₀) after ${convergence.periods} period at `
        + `v₀ = ${convergence.v0}, from reference.py; the last three columns are the fitted `
        + 'least-squares slope in log–log for the position error and for the energy error, '
        + 'against the order of the method.',
    })));
  }
  root.append(vs);

  // 6. Limits, references, provenance
  const ls = section('limits', 'Where this stops applying');
  for (const item of [].concat(chapter.limits ?? [])) ls.append(h('p', { text: item }));
  root.append(ls);

  const rs = section('references', 'References and provenance');
  rs.append(h('ul', { class: 'fg-list' }, (chapter.references ?? []).map((r) => h('li', {},
    r.url ? h('a', { href: r.url, rel: 'noreferrer' }, r.citation ?? r.url) : (r.citation ?? ''),
    r.note ? h('span', { class: 'fg-note', text: ` — ${r.note}` }) : null))));
  const rev = chapter.source_revision ?? {};
  rs.append(h('p', { class: 'fg-note' },
    `Source revision: ${rev.revision ?? 'unknown'} (${rev.note ?? 'chapter'}). `
    + `Reference values generated at revision ${validation.source_revision} by `
    + `${validation.generator}.`));
  const dl = h('button', { type: 'button', class: 'fg-primary', text: 'Download static figure (SVG)' });
  dl.addEventListener('click', () => hooks.onDownload?.());
  rs.append(dl);
  root.append(rs);

  mount.appendChild(root);

  return {
    el: root,
    values,
    panel,
    regions: { controls: controlsMount, sim: simRegion, plots: plotRegion, validation: vTableMount },
    get animating() { return animate; },
    get playing() { return playing; },
    setPlaying(v) {
      playing = v;
      playBtn.textContent = playing ? 'Pause' : 'Play';
      playBtn.setAttribute('aria-pressed', String(playing));
    },
    setStatus(text) { status.textContent = text; },
    applyPreset,
    // Renders the comparison table and the one-line verdict. `columns` is an
    // optional array of `{ header, cell(row) }` for the value columns before
    // the always-present "browser vs reference" / "status" pair; it defaults
    // to the original orbits-numerical-error column set so a chapter that
    // does not pass it renders exactly as before.
    showValidation(result, { columns, caption } = {}) {
      const cols = columns ?? [
        { header: 'case', cell: (r) => `v₀ = ${r.case.v0}, Δt = ${r.case.dt}, ${r.case.integrator}` },
        { header: 'max |ΔE|/|E₀|', cell: (r) => formatNumber(r.case.max_rel_energy_error, 4) },
        { header: 'max |ΔL|/|L₀|', cell: (r) => formatNumber(r.case.max_rel_angular_momentum_error, 4) },
        { header: '|Δx| after 10 periods', cell: (r) => formatNumber(r.case.final_position_error, 4) },
      ];
      const headers = [...cols.map((c) => c.header), 'browser vs reference', 'status'];
      const rows = result.rows.map((r) => ({
        cls: r.pass ? 'ok' : 'bad',
        cells: [
          ...cols.map((c) => c.cell(r)),
          formatNumber(r.worst_relative_difference, 3),
          r.pass ? 'agrees' : 'DIFFERS',
        ],
      }));
      vTableMount.replaceChildren(table(headers, rows, {
        caption: caption ?? `Reference values from validation.json (${result.rows.length} cases, 10 periods each); `
          + `agreement tolerance ${result.tolerance} relative.`,
      }));
      vStatus.textContent = result.pass
        ? `Validation: all ${result.rows.length} cases agree with reference.py; worst relative `
          + `difference ${formatNumber(result.worst_relative_difference, 3)} `
          + `(tolerance ${result.tolerance}).`
        : `Validation: ${result.rows.filter((r) => !r.pass).length} of ${result.rows.length} cases `
          + `exceed the ${result.tolerance} tolerance.`;
      vStatus.classList.toggle('bad', !result.pass);
    },
  };
}

// Hand the reader a file without a server round-trip.
export function downloadSVG(svg, filename) {
  const blob = new Blob([svg], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
