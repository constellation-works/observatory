import { createCanvas2D } from '../../../../_lib/web/canvas2d.js';
import { createPanel } from '../../../../_lib/web/panel.js';
import { createLoop } from '../../../../_lib/web/loop.js';
import { Fabric, RHO, T, ELL, SLAB_T, SLAB_DT, origin, factor, boost, diamond, slabPolygon, measure } from './model.mjs';

const $ = id => document.getElementById(id);
const state = { v: 0, w: 0, linked: true, twins: false, rod: false, boosted: false,
  dots: true, diamond: true, chain: true, cone: true, seed: 2026, lattice: false, animate: false };
let fabric, core, measurements, visible = [], camera, geometryDirty = true, viewDirty = true, paintDirty = true;
let selectedIds = new Set(), slabIds = new Set(), twinIds = new Set();
// Keep the viewport around the experiment instead of adding tall, empty time
// ranges on narrow screens. Pixel scales still remain equal on both axes.
const canvasHeight = () => Math.max(235, Math.min(650, ($('wrap').clientWidth - 54) * 8.2 / 13.2 + 68));
const surface = createCanvas2D({ mount: $('wrap'), height: canvasHeight() });
// Run before the shared canvas resize handler so its DPR backing size agrees.
window.addEventListener('resize', () => { surface.canvas.style.height = `${canvasHeight()}px`; }, { capture: true });
surface.canvas.setAttribute('role', 'img');
surface.canvas.setAttribute('aria-label', 'Spacetime diagram: time increases upward, space across. Use the adjacent controls to change worldlines, slab and frame. Counts are available as text beside the canvas.');
function invalidate(geometry = true, view = true) {
  geometryDirty ||= geometry;
  viewDirty ||= view;
  paintDirty = true;
  if (!loop.running) loop.renderOnce();
}
function regenerate() {
  fabric = new Fabric(state.seed, state.lattice);
  // All possible measurement diamonds and slabs are contained here, even when
  // their display is clipped by a boost. Camera never changes the measured set.
  core = fabric.window({ xmin: -6.1, xmax: 6.1, tmin: 0, tmax: 6.1 });
}
function setToggle(panel, key, value) {
  if (panel.get(key) !== value) panel.element(key).click();
}
const velocity = createPanel([{ type: 'range', key: 'v', label: 'Velocity v', min: -.99, max: .99, step: .01, value: 0,
  format: v => `${v >= 0 ? '+' : ''}${v.toFixed(2)} c`, onChange: v => {
    state.v = v;
    if (state.linked) {
      state.w = v;
      // Keep the shared control's value/readout synchronized without treating
      // this programmatic update as an independent observer choice.
      syncingSlab = true;
      slabVelocity.set('w', v);
      syncingSlab = false;
    }
    invalidate();
  } }], { mount: $('velocity') });
const modes = createPanel([
  { type: 'toggle', key: 'twins', label: 'Twin turnaround', value: false, onChange: value => { state.twins = value; invalidate(true, false); } },
  { type: 'toggle', key: 'animate', label: 'Animate v', value: false, onChange: value => {
    state.animate = value;
    if (value) { phase = Math.asin(state.v / .99); loop.start(); }
    else loop.pause();
  } },
  { type: 'button', label: 'At rest', onClick: () => { setToggle(modes, 'animate', false); velocity.set('v', 0); } },
], { mount: $('modes') });
let syncingSlab = false;
const rodControls = createPanel([{ type: 'toggle', key: 'rod', label: 'Rod + tilted slab', value: false,
  onChange: value => { state.rod = value; invalidate(false, false); } }], { mount: $('rod-controls') });
const slabVelocity = createPanel([{ type: 'range', key: 'w', label: 'Slab observer w', min: -.99, max: .99, step: .01, value: 0,
  format: v => `${v >= 0 ? '+' : ''}${v.toFixed(2)} c`, onChange: v => {
    state.w = v;
    if (!syncingSlab) {
      setToggle(slabLink, 'linked', false);
      setToggle(rodControls, 'rod', true);
      invalidate(true, false);
    }
  } }], { mount: $('slab-velocity') });
const slabLink = createPanel([{ type: 'toggle', key: 'linked', label: 'Slab follows v', value: true,
  onChange: value => {
    state.linked = value;
    if (value) { state.w = state.v; syncingSlab = true; slabVelocity.set('w', state.v); syncingSlab = false; }
    invalidate(true, false);
  } }], { mount: $('slab-link') });
createPanel([{ type: 'toggle', key: 'boosted', label: 'Moving-observer view', value: false,
  onChange: value => { state.boosted = value; invalidate(false, true); } }], { mount: $('view-controls') });
const fabricControls = createPanel([
  { type: 'button', key: 'regrid', label: 'Regrid: square lattice', onClick: () => {
    state.lattice = !state.lattice;
    fabricControls.setLabel('regrid', state.lattice ? 'Restore Poisson' : 'Regrid: square lattice');
    fabricControls.element('resprinkle').disabled = state.lattice;
    regenerate(); invalidate();
  } },
  { type: 'button', key: 'resprinkle', label: 'Resprinkle', onClick: () => { state.seed++; regenerate(); invalidate(); } },
], { mount: $('fabric-controls') });
createPanel([
  ['dots', 'Sprinkling'], ['diamond', 'Diamond'], ['chain', 'Longest chain'], ['cone', 'Light cone'],
].map(([key, label]) => ({ type: 'toggle', key, label, value: true,
  onChange: value => { state[key] = value; invalidate(false, false); } })), { mount: $('layers') });

function updateReadouts() {
  const m = measurements, f = factor(state.v), sf = factor(state.w);
  $('fabric-name').textContent = state.lattice ? 'SQUARE LATTICE · a = 0.125' : 'POISSON SPRINKLING';
  $('seed-label').textContent = state.lattice ? 'ρ = 64 · PREFERRED FRAME' : `ρ = 64 · SEED ${state.seed}`;
  $('count').textContent = m.selected.length.toLocaleString();
  $('chain').textContent = m.chain.length;
  $('count-label').textContent = state.twins ? 'Events in shared diamond' : 'Events in diamond';
  $('chain-label').textContent = state.twins ? 'Unconstrained chain' : 'Longest chain';
  $('twin-metric').hidden = !state.twins;
  $('twin-count').textContent = m.first.length + m.second.length;
  $('rate').textContent = f.toFixed(3);
  $('proper').textContent = m.tau.toFixed(3);
  $('proper-label').textContent = state.twins ? 'Traveler τ / stay-home τ = 6' : 'Path proper time / T = 6';
  $('chain-note').textContent = state.twins
    ? `Orange: ${m.first.length} + ${m.second.length} events, forced through K. Markers excluded; finite-count ties are possible.`
    : `Diamond area ${m.area.toFixed(2)} · Poisson mean N = ${(RHO * m.area).toFixed(1)}. ${state.lattice ? 'Lattice rows pick a preferred time.' : 'Markers excluded; finite counts fluctuate.'}`;
  $('rod-length').textContent = m.lengthEstimate.toFixed(2);
  // Same bar scale for both observers, enlarged if a rare count exceeds range.
  const extent = Math.max(ELL / .75, m.lengthEstimate);
  document.querySelector('.rod-bar.rest').style.width = `${100 * ELL / extent}%`;
  $('moving-bar').style.width = `${100 * m.lengthEstimate / extent}%`;
  $('expected-tick').style.left = `${100 * ELL * sf / extent}%`;
  $('slab-note').textContent = `${m.slab.length} events · Poisson mean ${(RHO * ELL * SLAB_DT * sf).toFixed(1)}\nRest-frame end-to-end Δt = ${(state.w * ELL).toFixed(2)}`;
  const frame = state.boosted ? `Boost v = ${state.v.toFixed(2)}. Same events and counts; fixed viewport may clip paths.` : 'Rest-frame view. Boost follows the worldline velocity v.';
  $('view-note').textContent = frame + (state.boosted && !state.linked ? ' Slab observer w is independent.' : '');
  $('scene-caption').textContent = state.lattice
    ? 'The lattice has a cadence. Its chain count follows coordinate time; boosting exposes the regular rows.'
    : state.twins ? 'Same departure. Same reunion. Orange must pass through the turnaround; cyan is free to take the longest chain.'
    : state.rod ? 'The rod stays put in its rest frame. The tilted lower edge samples its two ends at different times.'
    : state.boosted ? 'Every dot is transformed. The light cone stays at 45°; the random fabric has no preferred alignment.'
    : 'Drag velocity. The endpoint moves; the diamond narrows; fewer events can join the chain.';
}
function setupCamera() {
  const { w, h } = surface.size();
  const scale = Math.min((w - 54) / 13.2, (h - 68) / 8.2);
  // Equal x/t scale is essential: light must always draw at 45 degrees.
  const cx = w / 2, cy = h / 2 + 3.2 * scale;
  const bounds = { xmin: (25 - cx) / scale, xmax: (w - 25 - cx) / scale,
    tmin: (cy - (h - 25)) / scale, tmax: (cy - 25) / scale };
  camera = { w, h, scale, cx, cy, bounds, v: state.boosted ? state.v : 0 };
  visible = fabric.window(bounds, camera.v);
}
function screen(p) {
  const q = boost(p, camera.v);
  return { x: camera.cx + q.x * camera.scale, y: camera.cy - q.t * camera.scale };
}
function path(points, color, width = 1, fill = null, dash = []) {
  const ctx = surface.ctx;
  ctx.beginPath();
  points.forEach((p, i) => { const q = screen(p); if (i) ctx.lineTo(q.x, q.y); else ctx.moveTo(q.x, q.y); });
  if (fill) { ctx.closePath(); ctx.fillStyle = fill; ctx.fill(); }
  ctx.strokeStyle = color; ctx.lineWidth = width; ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
}
function dot(p, color, r = 1.2) {
  const q = screen(p), ctx = surface.ctx;
  ctx.beginPath(); ctx.arc(q.x, q.y, r, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
}
function label(p, text, color = '#91a6af', dx = 8, dy = -10) {
  const q = screen(p), ctx = surface.ctx;
  if (q.x < 15 || q.x > camera.w - 15 || q.y < 15 || q.y > camera.h - 15) return;
  ctx.font = '11px ui-monospace, monospace';
  const width = ctx.measureText(text).width;
  const x = Math.max(28, Math.min(camera.w - width - 28, q.x + dx));
  const y = Math.max(38, Math.min(camera.h - 30, q.y + dy));
  ctx.fillStyle = '#0a151bee'; ctx.fillRect(x - 4, y - 12, width + 8, 17);
  ctx.fillStyle = color; ctx.fillText(text, x, y);
}
function drawAxes() {
  const ctx = surface.ctx, { w, h, cx, cy, scale, bounds } = camera;
  const sx = x => cx + scale * x, sy = t => cy - scale * t;
  ctx.strokeStyle = '#20343e'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(25, sy(0)); ctx.lineTo(w - 25, sy(0)); ctx.moveTo(sx(0), 25); ctx.lineTo(sx(0), h - 25); ctx.stroke();
  ctx.font = '10px ui-monospace, monospace'; ctx.fillStyle = '#6d8791';
  const tickStep = scale < 35 ? 2 : 1;
  for (let x = Math.ceil(bounds.xmin); x < bounds.xmax; x += tickStep) {
    if (!x) continue;
    ctx.fillText(String(x), sx(x) - 3, sy(0) + 17);
    ctx.fillRect(sx(x), sy(0) - 3, 1, 6);
  }
  for (let t = Math.ceil(bounds.tmin); t < bounds.tmax; t += tickStep) {
    if (!t) continue;
    ctx.fillText(String(t), sx(0) - 18, sy(t) + 3);
    ctx.fillRect(sx(0) - 3, sy(t), 6, 1);
  }
  ctx.fillStyle = '#c8d8df'; ctx.fillText(state.boosted ? 't′ ↑' : 't ↑', sx(0) + 10, 19);
  ctx.fillText(state.boosted ? 'x′ →' : 'x →', w - 37, sy(0) - 10);
  ctx.fillStyle = '#6d8791'; ctx.fillText(`${visible.length.toLocaleString()} events in view`, 28, h - 8);
  const stamp = state.boosted ? `MOVING VIEW · v ${state.v.toFixed(2)}` : 'REST VIEW';
  ctx.fillText(stamp, Math.max(28, w - ctx.measureText(stamp).width - 28), h - 8);
}
function render() {
  if (!paintDirty) return;
  if (geometryDirty) {
    measurements = measure(core, state.v, state.twins, state.w);
    selectedIds = new Set(measurements.selected.map(p => p.id));
    slabIds = new Set(measurements.slab.map(p => p.id));
    twinIds = new Set([...measurements.first, ...measurements.second].map(p => p.id));
  }
  if (viewDirty) setupCamera();
  updateReadouts();
  const ctx = surface.ctx, m = measurements;
  surface.clear('#0a151b');
  ctx.save(); ctx.beginPath(); ctx.rect(25, 25, camera.w - 50, camera.h - 50); ctx.clip();
  if (state.rod) {
    path([{ x: -ELL / 2, t: -120 }, { x: ELL / 2, t: -120 }, { x: ELL / 2, t: 120 }, { x: -ELL / 2, t: 120 }], '#59657366', 1, '#a8a3d709');
    path(slabPolygon(state.w), '#bda4ee', 1.3, '#bda4ee24');
    // The entire observer's now extends across space; the counted intersection
    // is only the finite highlighted parallelogram inside the rod.
    path([{ x: -120, t: SLAB_T - 120 * state.w }, { x: 120, t: SLAB_T + 120 * state.w }], '#bda4ee66', 1, null, [4, 6]);
  }
  if (state.diamond) {
    path(diamond(origin, m.end), '#65b7ac77', 1.2, '#79dfd00a');
    if (state.twins) {
      path(diamond(origin, m.kink), '#f1bb7866', 1, '#f1bb780d');
      path(diamond(m.kink, m.end), '#f1bb7866', 1, '#f1bb780d');
    }
  }
  if (state.cone) {
    path([{ x: -1000, t: -1000 }, { x: 1000, t: 1000 }], '#78949e88', 1, null, [5, 6]);
    path([{ x: 1000, t: -1000 }, { x: -1000, t: 1000 }], '#78949e88', 1, null, [5, 6]);
  }
  if (state.dots) {
    for (const p of visible) {
      const inD = state.diamond && selectedIds.has(p.id), inS = state.rod && slabIds.has(p.id);
      dot(p, inS ? '#c5a9fa' : inD ? '#72c4b8' : '#526d7b99', inS ? 1.9 : inD ? 1.55 : 1.0);
    }
  }
  if (state.chain) {
    path([origin, ...m.chain, m.end], '#79dfd0', 1.7);
    for (const p of m.chain) dot(p, '#a4f3e3', 2.2);
    if (state.twins) {
      path([origin, ...m.first, m.kink, ...m.second, m.end], '#f1bb78', 1.7);
      for (const p of [...m.first, ...m.second]) dot(p, '#f8cc94', 2.2);
    }
  }
  path(state.twins ? [origin, m.kink, m.end] : [origin, m.end], '#f1bb78', 1.5, null, [6, 5]);
  if (state.twins) {
    path([origin, m.end], '#79dfd0aa', 1, null, [3, 6]);
    dot(m.kink, '#f1bb78', 4);
    label(m.kink, 'K · turnaround', '#f1bb78');
  }
  dot(origin, '#e4eff0', 4); dot(m.end, '#f1bb78', 4);
  ctx.restore();
  drawAxes();
  label(origin, 'O · here', '#dce7eb', 9, 32);
  label(m.end, state.twins ? 'B · reunion' : state.boosted ? `B · t′=${boost(m.end, camera.v).t.toFixed(2)}` : 'B · T = 6', '#f1bb78', 10, -12);
  if (state.rod) {
    const corners = slabPolygon(state.w);
    const timeSymbol = state.boosted ? 't′' : 't';
    label(corners[0], `left · ${timeSymbol}=${boost(corners[0], camera.v).t.toFixed(2)}`, '#c2a4f0', -100, 25);
    label(corners[1], `right · ${timeSymbol}=${boost(corners[1], camera.v).t.toFixed(2)}`, '#c2a4f0', 10, -15);
  }
  // Text alternative includes what remains selected even outside the viewport.
  surface.canvas.setAttribute('aria-description', `${m.selected.length} events in diamond, longest chain ${m.chain.length}, proper time ${m.tau.toFixed(3)}. ${state.twins ? `Turnaround chain ${twinIds.size}.` : ''} Slab contains ${m.slab.length} events.`);
  geometryDirty = false; viewDirty = false; paintDirty = false;
}
let phase = 0;
const loop = createLoop({ dt: 1 / 30, step: dt => {
  if (state.animate) { phase += dt * .28; velocity.set('v', Number((.99 * Math.sin(phase)).toFixed(2))); }
}, render });
// Explicit manual dragging takes control back from the optional velocity sweep.
velocity.element('v').addEventListener('pointerdown', () => setToggle(modes, 'animate', false));
velocity.element('v').addEventListener('keydown', () => setToggle(modes, 'animate', false));
surface.onResize(() => invalidate(false, true));
regenerate();
loop.renderOnce();
