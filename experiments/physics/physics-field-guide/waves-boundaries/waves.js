// Linear N-mass chain numerics for the "Waves, interference and boundaries"
// chapter -- the alpha=0 case of the FPUT model reproduced in
// experiments/physics/fput-recurrence-reproduction/.
//
// ddot(x)_i = x_{i+1} + x_{i-1} - 2 x_i, i = 1..N-1, x_0 = 0 always; the right
// end is either fixed (x_N = 0) or free (x_N = x_{N-1}). Integrated with
// Stormer-Verlet at a fixed step dt (stability bound dt < 2/omega_max = 1).
//
// This is the one code path the chapter uses everywhere: the animated page,
// the in-page validation table, and the headless Node check in tests/. It
// mirrors reference.py operation for operation so the two implementations can
// be compared at the tolerance declared in chapter.json.

export const N = 32;
export const DT = 0.1;
export const PULSE_AMPLITUDE = 1.0;

export function latticeIndices(n = N) {
  const out = new Float64Array(n - 1);
  for (let j = 0; j < n - 1; j++) out[j] = j + 1;
  return out;
}

// acc <- accelerations(x, boundary); overwrites, never accumulates.
export function accelerations(x, boundary, acc = new Float64Array(x.length)) {
  const n = x.length;
  const right = boundary === 'fixed' ? 0.0 : x[n - 1];
  for (let j = 0; j < n; j++) {
    const left = j === 0 ? 0.0 : x[j - 1];
    const rightNeighbor = j === n - 1 ? right : x[j + 1];
    acc[j] = rightNeighbor + left - 2 * x[j];
  }
  return acc;
}

// Stormer-Verlet (velocity form), mutating x, v, acc in place.
export function verletStep(x, v, acc, dt, boundary) {
  const n = x.length;
  for (let j = 0; j < n; j++) v[j] += 0.5 * dt * acc[j];
  for (let j = 0; j < n; j++) x[j] += dt * v[j];
  accelerations(x, boundary, acc);
  for (let j = 0; j < n; j++) v[j] += 0.5 * dt * acc[j];
}

// --- normal modes (LA-1940 protocol formulas, reused unchanged) -----------
export function modeFrequency(k, n = N) {
  return 2.0 * Math.sin((Math.PI * k) / (2.0 * n));
}

// a_k = sum_i x_i sin(i*pi*k/N), i = 1..N-1.
export function modeAmplitude(state, k, n = N) {
  let sum = 0;
  for (let j = 0; j < state.length; j++) {
    const i = j + 1;
    sum += state[j] * Math.sin((Math.PI * i * k) / n);
  }
  return sum;
}

// E_k = 1/2 (adot_k^2 + omega_k^2 a_k^2), for every k = 1..N-1.
export function modeEnergies(x, v, n = N) {
  const m = n - 1;
  const out = new Float64Array(m);
  for (let kk = 1; kk <= m; kk++) {
    const a = modeAmplitude(x, kk, n);
    const adot = modeAmplitude(v, kk, n);
    const omega = modeFrequency(kk, n);
    out[kk - 1] = 0.5 * (adot * adot + omega * omega * a * a);
  }
  return out;
}

// --- initial conditions -----------------------------------------------------
export function standingWaveInit(k, n = N) {
  const i = latticeIndices(n);
  const x = new Float64Array(i.length);
  const v = new Float64Array(i.length);
  for (let j = 0; j < i.length; j++) x[j] = Math.sin((Math.PI * i[j] * k) / n);
  return { x, v };
}

export function pulseDisplacement(i, i0, amplitude, sigma) {
  const d = i - i0;
  return amplitude * Math.exp(-(d * d) / (2 * sigma * sigma));
}

// Initial velocity for a d'Alembert packet f(i - direction*t - i0), c = 1.
export function pulseVelocity(i, i0, amplitude, sigma, direction) {
  const profile = pulseDisplacement(i, i0, amplitude, sigma);
  return (direction * (i - i0) * profile) / (sigma * sigma);
}

export function twoPulseInit(i1, i2, amplitude, sigma, phase, n = N) {
  const i = latticeIndices(n);
  const amplitude2 = amplitude * Math.cos(phase);
  const x = new Float64Array(i.length);
  const v = new Float64Array(i.length);
  for (let j = 0; j < i.length; j++) {
    x[j] = pulseDisplacement(i[j], i1, amplitude, sigma) + pulseDisplacement(i[j], i2, amplitude2, sigma);
    v[j] = pulseVelocity(i[j], i1, amplitude, sigma, +1)
      + pulseVelocity(i[j], i2, amplitude2, sigma, -1);
  }
  return { x, v, amplitude2 };
}

export function singlePulseInit(i0, amplitude, sigma, direction, n = N) {
  const i = latticeIndices(n);
  const x = new Float64Array(i.length);
  const v = new Float64Array(i.length);
  for (let j = 0; j < i.length; j++) {
    x[j] = pulseDisplacement(i[j], i0, amplitude, sigma);
    v[j] = pulseVelocity(i[j], i0, amplitude, sigma, direction);
  }
  return { x, v };
}

// --- one run, sampling a scalar observable every step ----------------------
export function runObservable(x0, v0, dt, boundary, steps, observe) {
  const x = Float64Array.from(x0);
  const v = Float64Array.from(v0);
  const acc = accelerations(x, boundary);
  const times = [0];
  const values = [observe(x, v)];
  for (let step = 1; step <= steps; step++) {
    verletStep(x, v, acc, dt, boundary);
    times.push(step * dt);
    values.push(observe(x, v));
  }
  return { times, values, x, v };
}

export function zeroCrossingPeriod(times, values) {
  const crossings = [];
  for (let j = 0; j < values.length - 1; j++) {
    const a = values[j];
    const b = values[j + 1];
    if (a === 0) {
      crossings.push(times[j]);
    } else if (a * b < 0) {
      const t = times[j] + (times[j + 1] - times[j]) * (-a) / (b - a);
      crossings.push(t);
    }
  }
  let sum = 0;
  for (let j = 0; j < crossings.length - 1; j++) sum += crossings[j + 1] - crossings[j];
  return 2 * (sum / (crossings.length - 1));
}

// --- validation cases, mirroring reference.py -------------------------------
export const DISPERSION_PERIODS = 6.0;
export const PERIOD_TOLERANCE = 0.01;

export function dispersionCase({ mode: k, n = N, periods = DISPERSION_PERIODS, dt = DT }) {
  const omegaAnalytic = modeFrequency(k, n);
  const periodAnalytic = (2 * Math.PI) / omegaAnalytic;
  const steps = Math.round((periods * periodAnalytic) / dt);
  const { x: x0, v: v0 } = standingWaveInit(k, n);
  const { times, values } = runObservable(x0, v0, dt, 'fixed', steps, (x) => modeAmplitude(x, k, n));
  const periodMeasured = zeroCrossingPeriod(times, values);
  const relError = Math.abs(periodMeasured - periodAnalytic) / periodAnalytic;
  return {
    kind: 'dispersion', mode: k, N: n, dt, boundary: 'fixed', periods, steps,
    omega_k_analytic: omegaAnalytic,
    period_analytic: periodAnalytic,
    period_measured: periodMeasured,
    period_relative_error: relError,
    period_tolerance_relative: PERIOD_TOLERANCE,
    period_within_tolerance: relError <= PERIOD_TOLERANCE,
  };
}

export const SUPERPOSITION_I1 = N / 4;
export const SUPERPOSITION_I2 = (3 * N) / 4;
export const SUPERPOSITION_SIGMA = 2.0;
export const SUPERPOSITION_STEPS = 160;

function maxAbs(arr) {
  let best = arr[0];
  for (const v of arr) if (Math.abs(v) > Math.abs(best)) best = v;
  return best;
}

export function superpositionCase({ phase, dt = DT, steps = SUPERPOSITION_STEPS }) {
  const boundary = 'fixed';
  const midIndex = Math.floor(N / 2) - 1;
  const midpointSeries = (x0, v0) =>
    runObservable(x0, v0, dt, boundary, steps, (x) => x[midIndex]).values;

  const p1 = singlePulseInit(SUPERPOSITION_I1, PULSE_AMPLITUDE, SUPERPOSITION_SIGMA, +1);
  const amplitude2 = PULSE_AMPLITUDE * Math.cos(phase);
  const p2 = singlePulseInit(SUPERPOSITION_I2, amplitude2, SUPERPOSITION_SIGMA, -1);
  const series1 = midpointSeries(p1.x, p1.v);
  const series2 = midpointSeries(p2.x, p2.v);
  const predicted = series1.map((a, j) => a + series2[j]);

  const combined = twoPulseInit(SUPERPOSITION_I1, SUPERPOSITION_I2, PULSE_AMPLITUDE, SUPERPOSITION_SIGMA, phase);
  const measured = midpointSeries(combined.x, combined.v);

  return {
    kind: 'superposition', N, dt, boundary, phase, steps,
    amplitude: PULSE_AMPLITUDE, amplitude2, sigma: SUPERPOSITION_SIGMA,
    i1: SUPERPOSITION_I1, i2: SUPERPOSITION_I2,
    predicted_max: maxAbs(predicted),
    measured_max: maxAbs(measured),
  };
}

export const REFLECTION_I0 = (3 * N) / 4;
export const REFLECTION_SIGMA = 1.5;
export const REFLECTION_STEPS = 300;
export const REFLECTION_SEARCH_START = 100;

export function reflectionCase({ boundary, dt = DT, steps = REFLECTION_STEPS }) {
  const { x: x0, v: v0 } = singlePulseInit(REFLECTION_I0, PULSE_AMPLITUDE, REFLECTION_SIGMA, +1);
  const detectIndex = Math.round(REFLECTION_I0) - 1;
  const { values } = runObservable(x0, v0, dt, boundary, steps, (x) => x[detectIndex]);
  const window = values.slice(REFLECTION_SEARCH_START);
  const extremum = maxAbs(window);
  const measuredSign = extremum >= 0 ? 1.0 : -1.0;
  const expectedSign = boundary === 'fixed' ? -1.0 : 1.0;
  return {
    kind: 'reflection', N, dt, boundary, steps,
    i0: REFLECTION_I0, sigma: REFLECTION_SIGMA, search_start_step: REFLECTION_SEARCH_START,
    extremum,
    measured_sign: measuredSign,
    expected_sign: expectedSign,
    sign_matches_expected: measuredSign === expectedSign,
  };
}

// Dispatch a stored validation.json case to its recomputation, by kind.
export function runCase(c) {
  if (c.kind === 'dispersion') return dispersionCase({ mode: c.mode, n: c.N, periods: c.periods, dt: c.dt });
  if (c.kind === 'superposition') return superpositionCase({ phase: c.phase, dt: c.dt, steps: c.steps });
  if (c.kind === 'reflection') return reflectionCase({ boundary: c.boundary, dt: c.dt, steps: c.steps });
  throw new Error(`waves: unknown validation case kind '${c.kind}'`);
}

export const CONVERGENCE_MODE = 4;
export const CONVERGENCE_DTS = [0.2, 0.1, 0.05, 0.025];
export const CONVERGENCE_PERIODS = 6.0;
