import test from 'node:test';
import assert from 'node:assert/strict';
import { Fabric, RHO, T, ELL, SLAB_DT, factor, boost, precedes, insideDiamond, longestChain, measure, origin, slabPolygon } from './model.mjs';
const box = { xmin: -6.1, xmax: 6.1, tmin: 0, tmax: 6.1 };
const close = (a, b, tol = 1e-8) => assert.ok(Math.abs(a - b) <= tol, `${a} != ${b} (tol ${tol})`);
const withNull = p => ({ ...p, u: p.t - p.x, w: p.t + p.x });
const mean = a => a.reduce((s, x) => s + x, 0) / a.length;
function bruteChain(points) {
  const ordered = [...points].sort((a, b) => a.t - b.t);
  const lengths = ordered.map(() => 1);
  for (let i = 0; i < ordered.length; i++) for (let j = 0; j < i; j++) {
    if (precedes(ordered[j], ordered[i])) lengths[i] = Math.max(lengths[i], lengths[j] + 1);
  }
  return Math.max(0, ...lengths);
}

test('Lorentz transform preserves interval, causal order, null rays and inverts', () => {
  const a = { x: 1.2, t: 3 }, b = { x: -.1, t: 5 };
  for (const v of [-.99, -.8, 0, .6, .99]) {
    const q = boost(a, v), r = boost(q, -v);
    close(q.t ** 2 - q.x ** 2, a.t ** 2 - a.x ** 2);
    close(r.x, a.x); close(r.t, a.t);
    assert.equal(precedes(q, boost(b, v)), precedes(a, b));
    for (const sign of [-1, 1]) { const n = boost({ x: sign * 4, t: 4 }, v); close(n.t, Math.abs(n.x)); }
  }
});
test('sampler is reproducible and tile count has Poisson mean AND variance', () => {
  const counts = Array.from({ length: 800 }, (_, seed) => new Fabric(seed).tile(2, -3).length);
  const m = mean(counts), variance = mean(counts.map(n => (n - m) ** 2));
  close(m, RHO, 1); close(variance, RHO, 8);
  const f = new Fabric(2026), original = f.tile(-2, 3);
  f.cache.clear(); assert.deepEqual(f.tile(-2, 3), original);
  assert.deepEqual(new Fabric(2026).tile(-2, 3), original);
  assert.notDeepEqual(new Fabric(2027).tile(-2, 3), original);
});
test('boosted viewport has no finite-source holes and matches brute enumeration', () => {
  const bounds = { xmin: -.8, xmax: 1.1, tmin: -.4, tmax: 1.3 };
  const f = new Fabric();
  for (const v of [-.99, 0, .99]) {
    const actual = f.window(bounds, v);
    const expected = [];
    for (let x = -20; x <= 20; x++) for (let t = -20; t <= 20; t++) for (const p of f.tile(x, t)) {
      const q = boost(p, v);
      if (q.x >= bounds.xmin && q.x < bounds.xmax && q.t >= bounds.tmin && q.t < bounds.tmax) expected.push(p.id);
    }
    assert.deepEqual(actual.map(p => p.id).sort(), expected.sort());
    assert.equal(new Set(actual.map(p => p.id)).size, actual.length);
  }
});
test('LIS matches independent quadratic causal DAG oracle, including lattice null ties', () => {
  for (const lattice of [false, true]) for (let seed = 0; seed < 8; seed++) {
    const points = new Fabric(seed, lattice).window({ xmin: -1, xmax: 1, tmin: 0, tmax: 1.5 });
    const chain = longestChain(points);
    assert.equal(chain.length, bruteChain(points));
    for (let i = 1; i < chain.length; i++) assert.ok(precedes(chain[i - 1], chain[i]));
  }
  assert.deepEqual(longestChain([]), []);
});
test('selected causal chain and count are invariant under boosts', () => {
  const points = new Fabric().window(box), b = { x: 3.6, t: T };
  const selected = points.filter(p => insideDiamond(p, origin, b));
  for (const v of [-.99, .8, .99]) {
    const transformed = points.map(p => withNull({ ...boost(p, v), id: p.id }));
    const chosen = transformed.filter(p => insideDiamond(p, boost(origin, v), boost(b, v)));
    assert.deepEqual(chosen.map(p => p.id), selected.map(p => p.id));
    assert.equal(longestChain(chosen).length, longestChain(selected).length);
  }
});
test('twin chain is an actual causal chain constrained through virtual K, never longer', () => {
  for (const lattice of [false, true]) for (let seed = 0; seed < 6; seed++) {
    const points = new Fabric(seed, lattice).window(box);
    for (const v of [-.99, -.8, 0, .8, .99]) {
      const m = measure(points, v, true), constrained = [...m.first, ...m.second];
      assert.ok(constrained.length <= m.chain.length);
      assert.equal(new Set(constrained.map(p => p.id)).size, constrained.length);
      const path = [origin, ...m.first, m.kink, ...m.second, m.end];
      for (let i = 1; i < path.length; i++) assert.ok(precedes(path[i - 1], path[i]));
      close(m.tau, T * factor(v));
    }
  }
});
test('slab geometry gives ell/gamma in observer coordinates at fixed observer thickness', () => {
  for (const v of [-.99, -.6, 0, .6, .99]) {
    const polygon = slabPolygon(v), transformed = polygon.map(p => boost(p, v));
    close(transformed[0].t, transformed[1].t);
    close(transformed[2].t - transformed[1].t, SLAB_DT);
    close(transformed[1].x - transformed[0].x, ELL * factor(v));
    close(polygon[1].t - polygon[0].t, v * ELL);
  }
});
test('ensemble reproduces diamond area, proper-time ratio and slab contraction', () => {
  const rest = [], fast = [], areas = [], slabs = [], visible = [];
  for (let seed = 0; seed < 100; seed++) {
    const f = new Fabric(seed), points = f.window(box), m = measure(points, .8);
    rest.push(measure(points, 0).chain.length); fast.push(m.chain.length);
    areas.push(m.selected.length); slabs.push(m.slab.length);
    visible.push(f.window({ xmin: -2, xmax: 2, tmin: 0, tmax: 4 }, .95).length);
  }
  close(mean(fast) / mean(rest), .6, .04);
  close(mean(areas), RHO * T * T * .36 / 2, 8);
  close(mean(slabs), RHO * ELL * SLAB_DT * .6, 3);
  close(mean(visible), RHO * 16, 12);
});
test('square lattice counts coordinate-time layers instead of proper time', () => {
  const points = new Fabric(2026, true).window(box);
  for (const v of [-.99, -.8, 0, .8, .99]) assert.equal(measure(points, v).chain.length, 47);
});
