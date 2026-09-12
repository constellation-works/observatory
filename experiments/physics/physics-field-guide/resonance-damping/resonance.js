// Driven damped oscillator numerics for the "Resonance and damping" chapter.
//
// x'' + 2*zeta*x' + x = F cos(omega t), omega_0 = 1, dimensionless. Integrated
// with RK4 over the autonomous state y = [x, v, t] (dt/dt = 1), so the page can
// call the shared, unmodified _lib/web/integrators.js rk4(y, dt, deriv) exactly
// as the pendulum-driven starter this chapter extends does for its own state.
// An optional "pendulum" toggle replaces the linear restoring term x with
// sin(x), showing where the linear analytic model stops applying.
//
// This is the one code path the chapter uses everywhere: the animated page, the
// in-page validation table, and the headless Node check in tests/. It mirrors
// reference.py operation for operation so the two implementations can be
// compared at the 1e-9 relative tolerance declared in chapter.json.

import { rk4 } from '../../_lib/web/integrators.js';

export const OMEGA0 = 1.0;

// --- analytic response -----------------------------------------------------
export function analyticAmplitudePhase(omega, zeta, F, omega0 = OMEGA0) {
  const gamma = zeta * omega0;
  const re = omega0 * omega0 - omega * omega;
  const im = 2.0 * gamma * omega;
  const d = Math.hypot(re, im);
  const amplitude = F / d;
  const phase = Math.atan2(im, re);
  return { amplitude, phase };
}

export function resonanceFrequency(zeta, omega0 = OMEGA0) {
  const disc = 1.0 - 2.0 * zeta * zeta;
  return disc > 0 ? omega0 * Math.sqrt(disc) : null;
}

export function qualityFactor(zeta) {
  return 1.0 / (2.0 * zeta);
}

export function dampedNaturalFrequency(zeta, omega0 = OMEGA0) {
  return omega0 * Math.sqrt(1.0 - zeta * zeta);
}

// Full closed-form x(t) from rest (x(0) = 0, v(0) = 0), underdamped only.
export function closedFormTransient(t, omega, zeta, F, omega0 = OMEGA0) {
  const { amplitude: a, phase: phi } = analyticAmplitudePhase(omega, zeta, F, omega0);
  const gamma = zeta * omega0;
  const wd = dampedNaturalFrequency(zeta, omega0);
  const c1 = -a * Math.cos(phi);
  const c2 = (-a * (gamma * Math.cos(phi) + omega * Math.sin(phi))) / wd;
  return a * Math.cos(omega * t - phi) + Math.exp(-gamma * t) * (c1 * Math.cos(wd * t) + c2 * Math.sin(wd * t));
}

// --- RK4 over y = [x, v, t] --------------------------------------------------
const yState = new Float64Array(3);

function makeDeriv(omega, zeta, F, model, omega0 = OMEGA0) {
  return (y, dy) => {
    const restoring = model === 'pendulum' ? Math.sin(y[0]) : omega0 * omega0 * y[0];
    dy[0] = y[1];
    dy[1] = -2.0 * zeta * omega0 * y[1] - restoring + F * Math.cos(omega * y[2]);
    dy[2] = 1.0;
  };
}

// One RK4 step of the driven oscillator, advancing (x, v, t) in place.
export function stepOscillator(state, dt, { omega, zeta, F, model = 'linear' }) {
  yState[0] = state.x; yState[1] = state.v; yState[2] = state.t;
  rk4(yState, dt, makeDeriv(omega, zeta, F, model));
  state.x = yState[0]; state.v = yState[1]; state.t = yState[2];
}

// --- validation grid: settle, then demodulate the tail window at the drive
// frequency (a two-line least-squares fit / lock-in amplifier) to measure the
// steady-state amplitude and phase, while tracking the transient error against
// the closed form along the way.
export const SETTLE_DECAY_LENGTHS = 15.0;
export const WINDOW_PERIODS = 5.0;

export function runCase({ omega, zeta, F, dt }) {
  const gamma = zeta * OMEGA0;
  const settleTime = SETTLE_DECAY_LENGTHS / gamma;
  const period = (2.0 * Math.PI) / omega;
  const windowLength = WINDOW_PERIODS * period;
  const totalTime = settleTime + windowLength;
  const stepsTotal = Math.round(totalTime / dt);
  const stepsWindow = Math.round(windowLength / dt);
  const windowStartStep = stepsTotal - stepsWindow;

  const state = { x: 0.0, v: 0.0, t: 0.0 };
  let transientMaxAbsError = 0.0;
  let sxx = 0, sxy = 0, syy = 0, sxb = 0, syb = 0;
  for (let step = 0; step < stepsTotal; step++) {
    stepOscillator(state, dt, { omega, zeta, F, model: 'linear' });
    const cf = closedFormTransient(state.t, omega, zeta, F);
    const err = Math.abs(state.x - cf);
    if (err > transientMaxAbsError) transientMaxAbsError = err;
    if (step + 1 > windowStartStep) {
      const c = Math.cos(omega * state.t);
      const s = Math.sin(omega * state.t);
      sxx += c * c; sxy += c * s; syy += s * s;
      sxb += state.x * c; syb += state.x * s;
    }
  }

  const det = sxx * syy - sxy * sxy;
  const inPhase = (sxb * syy - syb * sxy) / det;
  const quadrature = (sxx * syb - sxy * sxb) / det;
  const amplitudeMeasured = Math.hypot(inPhase, quadrature);
  const phaseMeasured = Math.atan2(quadrature, inPhase);

  const { amplitude: amplitudeAnalytic, phase: phaseAnalytic } = analyticAmplitudePhase(omega, zeta, F);
  const omegaR = resonanceFrequency(zeta);
  const q = qualityFactor(zeta);
  const amplitudeRelativeError = Math.abs(amplitudeMeasured - amplitudeAnalytic) / amplitudeAnalytic;
  const phaseAbsoluteError = Math.abs(phaseMeasured - phaseAnalytic);

  return {
    omega, zeta, F, dt,
    settle_time: settleTime,
    window_periods: WINDOW_PERIODS,
    period,
    total_time: totalTime,
    steps: stepsTotal,
    analytic: {
      amplitude: amplitudeAnalytic,
      phase: phaseAnalytic,
      omega_r: omegaR,
      Q: q,
      omega_d: dampedNaturalFrequency(zeta),
    },
    rk4_amplitude: amplitudeMeasured,
    rk4_phase: phaseMeasured,
    amplitude_relative_error: amplitudeRelativeError,
    phase_absolute_error: phaseAbsoluteError,
    steady_state_within_tolerance:
      amplitudeRelativeError <= 0.005 && phaseAbsoluteError <= 0.005,
    transient_max_abs_error: transientMaxAbsError,
    transient_within_tolerance: transientMaxAbsError <= 1e-6,
    final_state: { x: state.x, v: state.v, t: state.t },
  };
}

// --- an animated / interactive run: sampled trajectory plus live state -----
export function createRun({ omega, zeta, F, model = 'linear', dt = 0.01, sampleEvery = 0 }) {
  const state = { x: 0.0, v: 0.0, t: 0.0 };
  const gamma = zeta * OMEGA0;
  const period = (2.0 * Math.PI) / omega;

  const run = {
    omega, zeta, F, model, dt, gamma, period,
    x: 0, v: 0, t: 0, steps: 0,
    samples: { trajectory: [] },
  };

  run.advance = (n = 1) => {
    for (let k = 0; k < n; k++) {
      stepOscillator(state, dt, { omega, zeta, F, model });
      run.steps += 1;
      run.x = state.x; run.v = state.v; run.t = state.t;
      if (sampleEvery > 0 && run.steps % sampleEvery === 0) {
        run.samples.trajectory.push([state.t, state.x]);
      }
    }
    return run;
  };

  // Demodulated steady-state amplitude/phase from the last `periods` drive
  // cycles of what has actually run so far (used live, not just at validation
  // points): meaningless before at least one full window has elapsed.
  run.measureSteadyState = (periods = WINDOW_PERIODS) => {
    const windowLength = periods * period;
    if (run.t < windowLength) return null;
    const trail = run.samples.trajectory;
    let sxx = 0, sxy = 0, syy = 0, sxb = 0, syb = 0, n = 0;
    for (let i = trail.length - 1; i >= 0; i--) {
      const [t, x] = trail[i];
      if (run.t - t > windowLength) break;
      const c = Math.cos(omega * t);
      const s = Math.sin(omega * t);
      sxx += c * c; sxy += c * s; syy += s * s; sxb += x * c; syb += x * s;
      n++;
    }
    if (n < 4) return null;
    const det = sxx * syy - sxy * sxy;
    const inPhase = (sxb * syy - syb * sxy) / det;
    const quadrature = (sxx * syb - sxy * sxb) / det;
    return { amplitude: Math.hypot(inPhase, quadrature), phase: Math.atan2(quadrature, inPhase) };
  };

  return run;
}
