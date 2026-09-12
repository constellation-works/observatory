// Minimal dependency-free line plot: axes with tick labels, axis titles carrying
// units, a legend, an optional log y-axis, equal-aspect mode for trajectories,
// resize handling, and toSVG() for a static download.
//
//   const plot = createPlot({
//     mount: document.getElementById('energy'),
//     title: 'Relative energy error',
//     xLabel: 'time t / T₀ (orbital periods)',
//     yLabel: '|E(t) − E₀| / |E₀| (dimensionless)',
//     logY: true,
//   });
//   plot.setSeries([{ id: 'E', label: 'energy', points: pts, style: 'solid' }]);
//   plot.draw();
//   const svg = plot.toSVG();          // string, same drawing, for download
//
// Every series carries a line style as well as a colour, so the plot stays
// readable without colour (print, CVD, forced-colors). Colours default to the
// validated categorical order in chapter.css.
//
// A series is { id, label, points, style, color, width, hidden }. `points` is an
// array of [x, y] pairs; a non-finite pair, or a non-positive y under logY,
// breaks the line rather than dropping the series.

export const SERIES_COLORS = ['#3987e5', '#d95926', '#199e70', '#c98500'];
const DASH = { solid: [], dashed: [7, 4], dotted: [2, 3], 'dash-dot': [8, 3, 2, 3] };

const AXIS = '#6a7090';
const GRID = 'rgba(106,112,144,0.22)';
const INK = '#c9cede';
const MUTED = '#8b93b8';
const FONT = 12;

// --- drawing backends -----------------------------------------------------
// Both backends take the same calls, so the SVG download is the drawing the
// reader is looking at rather than a second implementation of it.
function canvasBackend(ctx) {
  return {
    clip(x, y, w, h) {
      ctx.save();
      ctx.beginPath();
      ctx.rect(x, y, w, h);
      ctx.clip();
    },
    endClip() { ctx.restore(); },
    line(pts, { color, width = 2, dash = [] }) {
      if (pts.length < 2) return;
      ctx.save();
      ctx.strokeStyle = color;
      ctx.lineWidth = width;
      ctx.setLineDash(dash);
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';
      ctx.beginPath();
      pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
      ctx.stroke();
      ctx.restore();
    },
    dot(x, y, r, color) {
      ctx.save();
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    },
    text(x, y, str, { color = MUTED, size = FONT, anchor = 'start', baseline = 'middle', rotate = 0 } = {}) {
      ctx.save();
      ctx.fillStyle = color;
      ctx.font = `${size}px ui-monospace, SFMono-Regular, Menlo, monospace`;
      ctx.textAlign = anchor === 'middle' ? 'center' : anchor === 'end' ? 'right' : 'left';
      ctx.textBaseline = baseline;
      ctx.translate(x, y);
      if (rotate) ctx.rotate(rotate);
      ctx.fillText(str, 0, 0);
      ctx.restore();
    },
  };
}

let clipSeq = 0;

function svgBackend(parts) {
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return {
    clip(x, y, w, h) {
      const id = `fg-clip-${++clipSeq}`;
      parts.push(`<clipPath id="${id}"><rect x="${x}" y="${y}" width="${w}" height="${h}"/></clipPath>`);
      parts.push(`<g clip-path="url(#${id})">`);
    },
    endClip() { parts.push('</g>'); },
    line(pts, { color, width = 2, dash = [] }) {
      if (pts.length < 2) return;
      const d = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(2)} ${y.toFixed(2)}`).join(' ');
      const da = dash.length ? ` stroke-dasharray="${dash.join(' ')}"` : '';
      parts.push(`<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}"`
        + ` stroke-linejoin="round" stroke-linecap="round"${da}/>`);
    },
    dot(x, y, r, color) {
      parts.push(`<circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="${r}" fill="${color}"/>`);
    },
    text(x, y, str, { color = MUTED, size = FONT, anchor = 'start', baseline = 'middle', rotate = 0 } = {}) {
      const a = anchor === 'middle' ? 'middle' : anchor === 'end' ? 'end' : 'start';
      const bl = baseline === 'middle' ? 'central' : baseline === 'top' ? 'hanging' : 'auto';
      const tr = rotate ? ` transform="rotate(${(rotate * 180) / Math.PI} ${x.toFixed(2)} ${y.toFixed(2)})"` : '';
      parts.push(`<text x="${x.toFixed(2)}" y="${y.toFixed(2)}" fill="${color}" font-size="${size}"`
        + ` font-family="ui-monospace, Menlo, monospace" text-anchor="${a}"`
        + ` dominant-baseline="${bl}"${tr}>${esc(str)}</text>`);
    },
  };
}

// --- ticks ----------------------------------------------------------------
function niceStep(span, target) {
  const raw = span / Math.max(1, target);
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const norm = raw / mag;
  const mult = norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10;
  return mult * mag;
}

function linearTicks(lo, hi, target = 5) {
  if (!(hi > lo)) return [lo];
  const step = niceStep(hi - lo, target);
  const out = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + step * 1e-6; v += step) out.push(v);
  return out;
}

function decadeTicks(lo, hi) {
  const out = [];
  for (let e = Math.floor(lo); e <= Math.ceil(hi); e++) out.push(e);
  if (out.length > 9) return out.filter((e, i) => i % Math.ceil(out.length / 8) === 0);
  return out;
}

function fmtLinear(v, step) {
  if (v === 0) return '0';
  const a = Math.abs(v);
  if (a >= 1e5 || a < 1e-3) return v.toExponential(1).replace('e', 'e');
  const decimals = Math.max(0, Math.min(6, -Math.floor(Math.log10(step)) + 0));
  return v.toFixed(decimals);
}

const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
  5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
const fmtDecade = (e) => `10${String(e).split('').map((c) => SUP[c] ?? c).join('')}`;

// --- plot -----------------------------------------------------------------
export function createPlot({
  mount, title: titleInit = '', xLabel: xLabelInit = '', yLabel: yLabelInit = '',
  logY = false, equalAspect = false, logDecades = 14,
  height = 260, yFloor = 1e-18, legend = true, description = '',
} = {}) {
  let title = titleInit;
  const el = document.createElement('figure');
  el.className = 'fg-plot';
  const cap = document.createElement('figcaption');
  cap.className = 'fg-plot-title';
  cap.textContent = title;
  const canvas = document.createElement('canvas');
  canvas.style.height = `${height}px`;
  canvas.setAttribute('role', 'img');
  const legendEl = document.createElement('ul');
  legendEl.className = 'fg-legend';
  const srOnly = document.createElement('p');
  srOnly.className = 'fg-sr-only';
  el.append(cap, canvas, legendEl, srOnly);
  mount.appendChild(el);

  const ctx = canvas.getContext('2d');
  let xLabel = xLabelInit;
  let yLabel = yLabelInit;
  let series = [];
  let sizeW = 0;
  let sizeH = height;
  let lastGeom = null;

  function resize() {
    const dpr = window.devicePixelRatio || 1;
    sizeW = canvas.clientWidth || 320;
    sizeH = canvas.clientHeight || height;
    canvas.width = Math.max(1, Math.round(sizeW * dpr));
    canvas.height = Math.max(1, Math.round(sizeH * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener('resize', () => { resize(); draw(); });

  function visible() {
    return series.filter((s) => !s.hidden && s.points && s.points.length);
  }

  function bounds(w, h) {
    const pad = { l: 62, r: 14, t: 10, b: 46 };
    let xlo = Infinity, xhi = -Infinity, ylo = Infinity, yhi = -Infinity;
    for (const s of visible()) {
      for (const p of s.points) {
        const [x, y] = p;
        if (!Number.isFinite(x) || !Number.isFinite(y)) continue;
        if (logY && !(y > 0)) continue;
        const yy = logY ? Math.log10(Math.max(y, yFloor)) : y;
        if (x < xlo) xlo = x;
        if (x > xhi) xhi = x;
        if (yy < ylo) ylo = yy;
        if (yy > yhi) yhi = yy;
      }
    }
    if (!Number.isFinite(xlo)) { xlo = 0; xhi = 1; ylo = 0; yhi = 1; }
    if (xhi - xlo < 1e-30) { xhi = xlo + 1; }
    if (yhi - ylo < 1e-30) { yhi = ylo + (logY ? 1 : Math.max(1e-12, Math.abs(ylo) || 1)); }
    if (logY) {
      ylo = Math.floor(ylo);
      yhi = Math.ceil(yhi);
      // A single near-zero sample must not stretch the axis over thirty decades.
      if (yhi - ylo > logDecades) ylo = yhi - logDecades;
    }
    else {
      const padY = (yhi - ylo) * 0.08;
      ylo -= padY; yhi += padY;
    }
    const iw = w - pad.l - pad.r;
    const ih = h - pad.t - pad.b;
    if (equalAspect) {
      // One world unit is the same number of pixels on both axes.
      const cx = (xlo + xhi) / 2, cy = (ylo + yhi) / 2;
      const sx = (xhi - xlo) / iw, sy = (yhi - ylo) / ih;
      const s = Math.max(sx, sy) * 1.06;
      xlo = cx - (s * iw) / 2; xhi = cx + (s * iw) / 2;
      ylo = cy - (s * ih) / 2; yhi = cy + (s * ih) / 2;
    }
    const X = (x) => pad.l + ((x - xlo) / (xhi - xlo)) * iw;
    const Y = (y) => {
      const yy = logY ? Math.log10(Math.max(y, yFloor)) : y;
      return pad.t + ih - ((yy - ylo) / (yhi - ylo)) * ih;
    };
    return { pad, iw, ih, xlo, xhi, ylo, yhi, X, Y };
  }

  function render(be, w, h) {
    const g = bounds(w, h);
    lastGeom = g;
    const { pad, iw, ih, X, Y } = g;
    const xt = linearTicks(g.xlo, g.xhi, Math.max(3, Math.round(iw / 75)));
    const xstep = xt.length > 1 ? xt[1] - xt[0] : 1;
    const yt = logY ? decadeTicks(g.ylo, g.yhi) : linearTicks(g.ylo, g.yhi, Math.max(3, Math.round(ih / 55)));
    const ystep = yt.length > 1 ? yt[1] - yt[0] : 1;

    for (const t of xt) {
      const x = X(t);
      be.line([[x, pad.t], [x, pad.t + ih]], { color: GRID, width: 1 });
      be.text(x, pad.t + ih + 8, fmtLinear(t, xstep), { anchor: 'middle', baseline: 'top', size: 11 });
    }
    for (const t of yt) {
      const y = logY ? Y(Math.pow(10, t)) : Y(t);
      be.line([[pad.l, y], [pad.l + iw, y]], { color: GRID, width: 1 });
      be.text(pad.l - 8, y, logY ? fmtDecade(t) : fmtLinear(t, ystep), { anchor: 'end', size: 11 });
    }
    be.line([[pad.l, pad.t], [pad.l, pad.t + ih], [pad.l + iw, pad.t + ih]], { color: AXIS, width: 1 });

    be.clip(pad.l, pad.t, iw, ih);
    for (const s of visible()) {
      const color = s.color ?? SERIES_COLORS[series.indexOf(s) % SERIES_COLORS.length];
      const dash = DASH[s.style ?? 'solid'] ?? [];
      let run = [];
      for (const [x, y] of s.points) {
        const ok = Number.isFinite(x) && Number.isFinite(y) && (!logY || y > 0);
        if (!ok) { if (run.length > 1) be.line(run, { color, width: s.width ?? 2, dash }); run = []; continue; }
        run.push([X(x), Y(y)]);
      }
      if (run.length > 1) be.line(run, { color, width: s.width ?? 2, dash });
      else if (run.length === 1) be.dot(run[0][0], run[0][1], 3, color);
      if (s.marker && run.length) {
        const [mx, my] = run[run.length - 1];
        be.dot(mx, my, 4.5, color);
      }
    }
    be.endClip();

    be.text(pad.l + iw / 2, h - 8, xLabel, { anchor: 'middle', baseline: 'alphabetic', size: 11, color: MUTED });
    be.text(13, pad.t + ih / 2, yLabel, { anchor: 'middle', size: 11, color: MUTED, rotate: -Math.PI / 2 });
    return g;
  }

  function paintLegend() {
    legendEl.innerHTML = '';
    if (!legend) return;
    const vis = visible();
    legendEl.hidden = vis.length < 2;
    for (const s of vis) {
      const color = s.color ?? SERIES_COLORS[series.indexOf(s) % SERIES_COLORS.length];
      const li = document.createElement('li');
      const sw = document.createElement('span');
      sw.className = `fg-swatch ${s.style ?? 'solid'}`;
      sw.style.setProperty('--swatch', color);
      li.append(sw, document.createTextNode(s.label ?? s.id));
      legendEl.appendChild(li);
    }
  }

  function draw() {
    if (!sizeW) resize();
    ctx.save();
    ctx.clearRect(0, 0, sizeW, sizeH);
    ctx.restore();
    render(canvasBackend(ctx), sizeW, sizeH);
    paintLegend();
    const names = visible().map((s) => s.label ?? s.id).join(', ');
    canvas.setAttribute('aria-label',
      `${title || 'plot'}. ${xLabel} versus ${yLabel}.${names ? ` Series: ${names}.` : ''}`);
    srOnly.textContent = description;
  }

  function toSVG() {
    const w = Math.round(sizeW || 640);
    const h = Math.round(sizeH || height);
    const vis = visible();
    const rows = legend && vis.length > 1 ? vis.length : 0;
    const head = title ? 18 : 0;
    const foot = rows ? rows * 15 + 6 : 0;
    const parts = [];
    parts.push(`<rect width="${w}" height="${h}" fill="#050510"/>`);
    if (title) {
      parts.push(`<text x="${w / 2}" y="${-head + 3}" fill="${INK}" font-size="12"`
        + ' font-family="system-ui, sans-serif" text-anchor="middle"'
        + ` dominant-baseline="hanging">${title}</text>`);
    }
    render(svgBackend(parts), w, h);
    // The legend sits under the frame, left aligned, so the exported figure is
    // self-describing and long labels cannot run off the edge.
    vis.forEach((s, i) => {
      if (!rows) return;
      const color = s.color ?? SERIES_COLORS[series.indexOf(s) % SERIES_COLORS.length];
      const dash = DASH[s.style ?? 'solid'] ?? [];
      const y = h + 12 + i * 15;
      const da = dash.length ? ` stroke-dasharray="${dash.join(' ')}"` : '';
      parts.push(`<line x1="8" y1="${y}" x2="38" y2="${y}" stroke="${color}" stroke-width="2"${da}/>`);
      parts.push(`<text x="44" y="${y}" fill="${MUTED}" font-size="11"`
        + ' font-family="ui-monospace, Menlo, monospace" dominant-baseline="central">'
        + `${s.label ?? s.id}</text>`);
    });
    const total = head + h + foot;
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${total}" viewBox="0 0 ${w} ${total}">`
      + `<rect width="${w}" height="${total}" fill="#050510"/>`
      + `<g transform="translate(0,${head})">${parts.join('')}</g></svg>`;
  }

  queueMicrotask(() => { resize(); draw(); });

  return {
    el,
    canvas,
    get series() { return series; },
    setTitle(t) { cap.textContent = t; title = t; },
    setAxisLabels({ x, y } = {}) {
      if (x !== undefined) xLabel = x;
      if (y !== undefined) yLabel = y;
    },
    setDescription(t) { srOnly.textContent = t; },
    setSeries(next) { series = next; },
    geometry: () => lastGeom,
    draw,
    resize,
    toSVG,
  };
}

// Bundle several plots into one downloadable SVG, stacked vertically.
export function plotsToSVG(plots, { gap = 12 } = {}) {
  const svgs = plots.map((p) => p.toSVG());
  const dims = svgs.map((s) => {
    const w = Number(/width="(\d+)"/.exec(s)[1]);
    const h = Number(/height="(\d+)"/.exec(s)[1]);
    return { w, h };
  });
  const W = Math.max(...dims.map((d) => d.w));
  const H = dims.reduce((a, d) => a + d.h, 0) + gap * (svgs.length - 1);
  let y = 0;
  const body = svgs.map((s, i) => {
    const inner = s.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
    const g = `<g transform="translate(0,${y})">${inner}</g>`;
    y += dims[i].h + gap;
    return g;
  }).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">`
    + `<rect width="${W}" height="${H}" fill="#050510"/>${body}</svg>`;
}
