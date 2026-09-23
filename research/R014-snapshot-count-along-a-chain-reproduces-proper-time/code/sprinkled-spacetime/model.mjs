// Units c = 1. Sampling and measurements are independent of the camera and DOM.
export const RHO = 64, T = 6, ELL = 3.5, SLAB_DT = 0.55, SLAB_T = 3;
export const origin = { x: 0, t: 0 };
export const factor = v => Math.sqrt(1 - v * v);
export function boost(p, v) {
  const g = 1 / factor(v);
  return { x: g * (p.x - v * p.t), t: g * (p.t - v * p.x) };
}
export function random(seed) {
  return () => {
    seed |= 0;
    seed = seed + 0x6D2B79F5 | 0;
    let a = Math.imul(seed ^ seed >>> 15, 1 | seed);
    a ^= a + Math.imul(a ^ a >>> 7, 61 | a);
    return ((a ^ a >>> 14) >>> 0) / 4294967296;
  };
}
function tileSeed(seed, x, t) {
  let a = (seed ^ Math.imul(x, 0x9E3779B1) ^ Math.imul(t, 0x85EBCA77)) >>> 0;
  a = Math.imul(a ^ a >>> 16, 0x21F0AAAD);
  a = Math.imul(a ^ a >>> 15, 0x735A2D97);
  return (a ^ a >>> 15) >>> 0;
}

// Independent Poisson tiles extend the SAME realization beyond the viewport.
// Exponential arrivals give N ~ Poisson(rho), not a fixed number of random dots.
// Eviction changes no point: a tile is determined by seed + coordinates.
export class Fabric {
  constructor(seed = 2026, lattice = false) {
    this.seed = seed;
    this.lattice = lattice;
    this.cache = new Map();
  }
  tile(x, t) {
    const key = `${x},${t}`;
    if (this.cache.has(key)) return this.cache.get(key);
    const points = [];
    const add = (px, pt) => points.push({ x: px, t: pt, u: pt - px, w: pt + px, id: `${key}:${points.length}` });
    if (this.lattice) {
      for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) add(x + i / 8, t + j / 8);
    } else {
      const rng = random(tileSeed(this.seed, x, t));
      let arrival = -Math.log(1 - rng());
      while (arrival < RHO) {
        add(x + rng(), t + rng());
        arrival += -Math.log(1 - rng());
      }
    }
    if (this.cache.size >= 1024) this.cache.delete(this.cache.keys().next().value);
    this.cache.set(key, points);
    return points;
  }
  // Original-coordinate events in a rectangular boosted window, with no holes.
  window(bounds, v = 0) {
    const { xmin, xmax, tmin, tmax } = bounds;
    const corners = [{ x: xmin, t: tmin }, { x: xmax, t: tmin }, { x: xmax, t: tmax }, { x: xmin, t: tmax }];
    const preimage = corners.map(p => boost(p, -v));
    const left = Math.floor(Math.min(...preimage.map(p => p.x)));
    const right = Math.ceil(Math.max(...preimage.map(p => p.x)));
    const bottom = Math.floor(Math.min(...preimage.map(p => p.t)));
    const top = Math.ceil(Math.max(...preimage.map(p => p.t)));
    const out = [];
    for (let x = left; x < right; x++) for (let t = bottom; t < top; t++) {
      const c = [{ x, t }, { x: x + 1, t }, { x: x + 1, t: t + 1 }, { x, t: t + 1 }].map(p => boost(p, v));
      if (Math.max(...c.map(p => p.x)) < xmin || Math.min(...c.map(p => p.x)) > xmax ||
          Math.max(...c.map(p => p.t)) < tmin || Math.min(...c.map(p => p.t)) > tmax) continue;
      for (const p of this.tile(x, t)) {
        const q = boost(p, v);
        if (q.x >= xmin && q.x < xmax && q.t >= tmin && q.t < tmax) out.push(p);
      }
    }
    return out;
  }
}
const EPS = 1e-10;
export function precedes(a, b) {
  return b.t - a.t >= Math.abs(b.x - a.x) - EPS && b.t > a.t + EPS;
}
export function insideDiamond(p, a, b) { return precedes(a, p) && precedes(p, b); }
export function diamond(a, b) {
  const u0 = a.t - a.x, u1 = b.t - b.x, w0 = a.t + a.x, w1 = b.t + b.x;
  const point = (u, w) => ({ x: (w - u) / 2, t: (w + u) / 2 });
  return [a, point(u0, w1), b, point(u1, w0)];
}
// Nondecreasing LIS in w after (u,w) sort. Null links count, including lattice
// ties. Predecessor indices reconstruct an actual longest chain in O(n log n).
export function longestChain(points) {
  const sorted = [...points].sort((a, b) => a.u - b.u || a.w - b.w);
  const tails = [], indices = [], previous = new Int32Array(sorted.length).fill(-1);
  sorted.forEach((p, i) => {
    let lo = 0, hi = tails.length;
    while (lo < hi) {
      const mid = (lo + hi) >>> 1;
      if (tails[mid] <= p.w) lo = mid + 1;
      else hi = mid;
    }
    if (lo) previous[i] = indices[lo - 1];
    tails[lo] = p.w;
    indices[lo] = i;
  });
  const chain = [];
  for (let i = indices.at(-1) ?? -1; i !== -1; i = previous[i]) chain.push(sorted[i]);
  return chain.reverse();
}
export function inSlab(p, v) {
  const lower = SLAB_T + v * p.x;
  return p.x >= -ELL / 2 && p.x < ELL / 2 && p.t >= lower && p.t < lower + SLAB_DT * factor(v);
}
export function slabPolygon(v) {
  const a = { x: -ELL / 2, t: SLAB_T - v * ELL / 2 };
  const b = { x: ELL / 2, t: SLAB_T + v * ELL / 2 };
  return [a, b, { x: b.x, t: b.t + SLAB_DT * factor(v) }, { x: a.x, t: a.t + SLAB_DT * factor(v) }];
}
export function measure(points, v, twins = false, slabV = v) {
  const end = { x: twins ? 0 : v * T, t: T }, kink = { x: v * T / 2, t: T / 2 };
  const selected = points.filter(p => insideDiamond(p, origin, end));
  const chain = longestChain(selected);
  const first = twins ? longestChain(selected.filter(p => insideDiamond(p, origin, kink))) : [];
  const second = twins ? longestChain(selected.filter(p => insideDiamond(p, kink, end))) : [];
  const slab = points.filter(p => inSlab(p, slabV));
  return { end, kink, selected, chain, first, second, slab,
    tau: T * factor(v), area: T * T * (twins ? 1 : 1 - v * v) / 2,
    lengthEstimate: slab.length / (RHO * SLAB_DT) };
}
