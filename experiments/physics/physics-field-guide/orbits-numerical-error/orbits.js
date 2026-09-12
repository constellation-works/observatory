// Kepler two-body numerics for the "Orbits and numerical error" chapter.
//
// GM = 1, r0 = 1, planar, dimensionless; time is in units of sqrt(r0^3/GM).
// The satellite starts at (1, 0) with a purely tangential velocity (0, v0), so
// the start is an apsis of the orbit: periapsis for v0 > 1, apoapsis for v0 < 1.
//
// This is the one code path the chapter uses everywhere: the animated page, the
// in-page validation table, and the headless Node check in tests/. It mirrors
// reference.py operation for operation so the two implementations can be
// compared at the 1e-9 relative tolerance declared in chapter.json.

import { explicitEuler, leapfrogKDK, rk4, semiImplicitEuler } from '../../_lib/web/integrators.js';

export const MU = 1.0;
export const R0 = 1.0;

export const INTEGRATORS = ['euler', 'semi-implicit-euler', 'leapfrog-kdk', 'rk4'];
export const INTEGRATOR_LABELS = {
  euler: 'explicit Euler',
  'semi-implicit-euler': 'semi-implicit Euler',
  'leapfrog-kdk': 'leapfrog (KDK)',
  rk4: 'RK4',
};

export function computeAcc(pos, acc) {
  const r2 = pos[0] * pos[0] + pos[1] * pos[1];
  const r = Math.sqrt(r2);
  const inv = MU / (r2 * r);
  acc[0] = -pos[0] * inv;
  acc[1] = -pos[1] * inv;
}

function deriv(y, dy) {
  dy[0] = y[2];
  dy[1] = y[3];
  const r2 = y[0] * y[0] + y[1] * y[1];
  const r = Math.sqrt(r2);
  const inv = MU / (r2 * r);
  dy[2] = -y[0] * inv;
  dy[3] = -y[1] * inv;
}

const rk4State = new Float64Array(4);

function stepRK4(pos, vel, acc, dt) {
  rk4State[0] = pos[0]; rk4State[1] = pos[1];
  rk4State[2] = vel[0]; rk4State[3] = vel[1];
  rk4(rk4State, dt, deriv);
  pos[0] = rk4State[0]; pos[1] = rk4State[1];
  vel[0] = rk4State[2]; vel[1] = rk4State[3];
}

const STEPPERS = {
  euler: (pos, vel, acc, dt) => explicitEuler(pos, vel, acc, dt, computeAcc),
  'semi-implicit-euler': (pos, vel, acc, dt) => semiImplicitEuler(pos, vel, acc, dt, computeAcc),
  'leapfrog-kdk': (pos, vel, acc, dt) => leapfrogKDK(pos, vel, acc, dt, computeAcc),
  rk4: stepRK4,
};

export function specificEnergy(pos, vel) {
  const v2 = vel[0] * vel[0] + vel[1] * vel[1];
  const r = Math.sqrt(pos[0] * pos[0] + pos[1] * pos[1]);
  return 0.5 * v2 - MU / r;
}

export function angularMomentum(pos, vel) {
  return pos[0] * vel[1] - pos[1] * vel[0];
}

// --- analytic Kepler solution --------------------------------------------
export function elements(v0) {
  const energy = 0.5 * v0 * v0 - MU / R0;
  const ang = R0 * v0;
  const ecc2 = 1 + (2 * energy * ang * ang) / (MU * MU);
  const ecc = ecc2 > 0 ? Math.sqrt(ecc2) : 0.0;
  const ex = (v0 * ang) / MU - 1.0;
  const omega = ex !== 0.0 ? Math.atan2(0.0, ex) : 0.0;
  const bound = energy < 0;
  const a = bound ? (-0.5 * MU) / energy : NaN;
  const period = bound ? 2 * Math.PI * a * Math.sqrt(a) : NaN;
  return {
    v0,
    energy,
    angular_momentum: ang,
    eccentricity: ecc,
    semi_major_axis: a,
    semi_latus_rectum: (ang * ang) / MU,
    periapsis: bound ? a * (1 - ecc) : NaN,
    apoapsis: bound ? a * (1 + ecc) : NaN,
    period,
    argument_of_periapsis: omega,
    bound,
    start_apsis: v0 > 1 ? 'periapsis' : (v0 < 1 ? 'apoapsis' : 'circular'),
  };
}

// Position on the exact ellipse at time t. A fixed 60 Newton iterations with no
// convergence branch, so Python and JavaScript execute the same operations.
export function analyticPosition(el, t) {
  const a = el.semi_major_axis;
  const ecc = el.eccentricity;
  const omega = el.argument_of_periapsis;
  const n = 1.0 / (a * Math.sqrt(a));
  const m0 = el.start_apsis === 'apoapsis' ? Math.PI : 0.0;
  const twoPi = 2 * Math.PI;
  let m = m0 + n * t;
  m = m - twoPi * Math.floor(m / twoPi);
  let eccAnom = m;
  for (let i = 0; i < 60; i++) {
    const f = eccAnom - ecc * Math.sin(eccAnom) - m;
    const fp = 1 - ecc * Math.cos(eccAnom);
    eccAnom = eccAnom - f / fp;
  }
  const xp = a * (Math.cos(eccAnom) - ecc);
  const yp = a * Math.sqrt(1 - ecc * ecc) * Math.sin(eccAnom);
  const cw = Math.cos(omega);
  const sw = Math.sin(omega);
  return [xp * cw - yp * sw, xp * sw + yp * cw];
}

// The analytic conic as drawable points, valid for ellipse and hyperbola alike.
export function conicPoints(el, n = 720) {
  const p = el.semi_latus_rectum;
  const e = el.eccentricity;
  const omega = el.argument_of_periapsis;
  const out = [];
  for (let i = 0; i <= n; i++) {
    const nu = -Math.PI + (2 * Math.PI * i) / n;
    const denom = 1 + e * Math.cos(nu);
    if (denom <= 1e-3) { out.push([NaN, NaN]); continue; } // asymptote of an open orbit
    const r = p / denom;
    if (r > 40) { out.push([NaN, NaN]); continue; }
    const th = nu + omega;
    out.push([r * Math.cos(th), r * Math.sin(th)]);
  }
  return out;
}

// --- a run ----------------------------------------------------------------
export function createRun({ v0, dt, integrator, periods = 10, sampleEvery = 0 }) {
  const el = elements(v0);
  const stepper = STEPPERS[integrator];
  if (!stepper) throw new Error(`orbits: unknown integrator '${integrator}'`);
  const pos = new Float64Array([R0, 0.0]);
  const vel = new Float64Array([0.0, v0]);
  const acc = new Float64Array(2);
  computeAcc(pos, acc); // leapfrog KDK needs a primed acceleration
  const e0 = specificEnergy(pos, vel);
  const l0 = angularMomentum(pos, vel);
  const timeUnit = el.bound ? el.period : 1;
  const totalSteps = el.bound ? Math.floor((periods * el.period) / dt + 0.5)
    : Math.floor((periods * 6.283185307179586) / dt + 0.5);

  const state = {
    el, v0, dt, integrator, periods, totalSteps, e0, l0, timeUnit,
    pos, vel, done: false, steps: 0,
    maxRelEnergyError: 0, maxRelAngularMomentumError: 0,
    relEnergyError: 0, relAngularMomentumError: 0, positionError: 0,
    samples: { trajectory: [], energy: [], angularMomentum: [], position: [] },
  };

  function observe(sample) {
    const e = specificEnergy(pos, vel);
    const l = angularMomentum(pos, vel);
    state.relEnergyError = Math.abs(e - e0) / Math.abs(e0);
    state.relAngularMomentumError = Math.abs(l - l0) / Math.abs(l0);
    if (state.relEnergyError > state.maxRelEnergyError) {
      state.maxRelEnergyError = state.relEnergyError;
    }
    if (state.relAngularMomentumError > state.maxRelAngularMomentumError) {
      state.maxRelAngularMomentumError = state.relAngularMomentumError;
    }
    if (sample) {
      const t = state.steps * dt;
      const tp = t / timeUnit;
      state.samples.trajectory.push([pos[0], pos[1]]);
      state.samples.energy.push([tp, state.relEnergyError]);
      state.samples.angularMomentum.push([tp, state.relAngularMomentumError]);
      if (el.bound) {
        const [ax, ay] = analyticPosition(el, t);
        const dx = pos[0] - ax;
        const dy = pos[1] - ay;
        state.positionError = Math.sqrt(dx * dx + dy * dy);
        state.samples.position.push([tp, state.positionError]);
      }
    }
  }

  state.advance = (n = 1) => {
    for (let k = 0; k < n && !state.done; k++) {
      stepper(pos, vel, acc, dt);
      state.steps += 1;
      const sample = sampleEvery > 0 && (state.steps % sampleEvery === 0);
      observe(sample);
      if (state.steps >= totalSteps) state.done = true;
    }
    return state;
  };

  state.summary = () => {
    const tFinal = state.steps * dt;
    let posErr = NaN;
    if (el.bound) {
      const [ax, ay] = analyticPosition(el, tFinal);
      const dx = pos[0] - ax;
      const dy = pos[1] - ay;
      posErr = Math.sqrt(dx * dx + dy * dy);
    }
    return {
      v0, dt, integrator, periods,
      steps: state.steps,
      t_final: tFinal,
      final_rel_energy_error: state.relEnergyError,
      max_rel_energy_error: state.maxRelEnergyError,
      final_rel_angular_momentum_error: state.relAngularMomentumError,
      max_rel_angular_momentum_error: state.maxRelAngularMomentumError,
      final_position_error: posErr,
      final_state: { x: pos[0], y: pos[1], vx: vel[0], vy: vel[1] },
    };
  };

  return state;
}

// One validation point, start to finish, with no sampling overhead.
export function runCase({ v0, dt, integrator, periods = 10 }) {
  const run = createRun({ v0, dt, integrator, periods });
  run.advance(run.totalSteps);
  return run.summary();
}
