#!/usr/bin/env python3
"""Independent Python reference for the "Resonance and damping" chapter.

Integrates the driven damped linear oscillator ``x'' + 2*zeta*x' + x = F cos(omega t)``
(omega_0 = 1, dimensionless) with RK4 over the autonomous state ``y = [x, v, t]``
(the same trick ``resonance.js`` uses so both implementations can call the shared,
unmodified ``rk4(y, dt, deriv)`` from ``_lib/web/integrators.js``), and writes
``validation.json``: the analytic steady-state amplitude/phase, the closed-form
underdamped transient, the resonance peak omega_r and quality factor Q, the RK4
measurement of the same quantities at each predefined point, and a dt^4
convergence entry.

The browser is never its own oracle. ``resonance.js`` mirrors the arithmetic here
operation for operation, so agreement at the 1e-9 relative tolerance declared in
``chapter.json`` is a real cross-implementation check and not a tautology.

Usage:
    uv run experiments/physics/physics-field-guide/resonance-damping/reference.py
    uv run .../reference.py --check     # recompute and diff against validation.json
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "validation.json"

OMEGA0 = 1.0  # natural frequency, dimensionless

# Validation grid: every (omega, zeta) point the browser must reproduce, at a
# fixed drive amplitude and step. All points are underdamped (zeta < 1) so the
# closed-form transient applies at every one of them.
VALIDATION_OMEGA = (0.8, 1.0, 1.6)
VALIDATION_ZETA = (0.05, 0.3)
VALIDATION_F = 0.5
VALIDATION_DT = 0.01

# How long to run before measuring the steady state: enough decay lengths
# (1/gamma) that the transient is negligible at the *start* of the measurement
# window, plus the window itself (a handful of drive periods), so the window
# length never has to double as the settling time.
SETTLE_DECAY_LENGTHS = 15.0
WINDOW_PERIODS = 5.0

STEADY_STATE_TOLERANCE = {
    "amplitude_relative": 0.005,
    "phase_absolute": 0.005,
}
TRANSIENT_TOLERANCE_ABSOLUTE = 1e-6
BROWSER_TOLERANCE = {
    "relative": 1e-9,
    "absolute": 1e-12,
    "rationale": (
        "resonance.js and reference.py run the same RK4 algorithm (the shared "
        "_lib/web/integrators.js stepper, over the autonomous state [x, v, t]) in the "
        "same operation order in float64, so the two implementations agree to "
        "floating-point roundoff. This is distinct from the physics tolerances below: "
        "the RK4 steady-state measurement always carries a discretisation error against "
        "the analytic amplitude/phase (declared separately as steady_state_tolerance), "
        "and the RK4 trajectory always carries a discretisation error against the "
        "closed-form transient (declared separately as transient_tolerance_absolute)."
    ),
}

# dt^4 convergence: RK4 position error against the closed-form transient at a
# fixed time, for shrinking dt. t_probe divides every dt exactly, so each run
# lands on it without interpolation.
CONVERGENCE_CASE = {"omega": 1.0, "zeta": 0.3, "f": 0.5}
CONVERGENCE_DTS = (0.04, 0.02, 0.01, 0.005)
CONVERGENCE_T_PROBE = 4.0


# --------------------------------------------------------------------------
# Analytic response
# --------------------------------------------------------------------------
def analytic_amplitude_phase(omega: float, zeta: float, f: float, omega0: float = OMEGA0) -> tuple[float, float]:
    """Steady-state A(omega) and phi(omega) for x_p(t) = A cos(omega t - phi)."""
    gamma = zeta * omega0
    re = omega0 * omega0 - omega * omega
    im = 2.0 * gamma * omega
    d = math.hypot(re, im)
    amplitude = f / d
    phase = math.atan2(im, re)  # in (0, pi) for omega, zeta > 0
    return amplitude, phase


def resonance_frequency(zeta: float, omega0: float = OMEGA0) -> float | None:
    """omega_r = omega0 sqrt(1 - 2 zeta^2); None when the amplitude has no interior peak."""
    disc = 1.0 - 2.0 * zeta * zeta
    return omega0 * math.sqrt(disc) if disc > 0 else None


def quality_factor(zeta: float) -> float:
    return 1.0 / (2.0 * zeta)


def damped_natural_frequency(zeta: float, omega0: float = OMEGA0) -> float:
    """omega_d, underdamped only (zeta < 1)."""
    return omega0 * math.sqrt(1.0 - zeta * zeta)


def closed_form_transient(t: float, omega: float, zeta: float, f: float, omega0: float = OMEGA0) -> float:
    """Full closed-form x(t) from rest (x(0) = 0, v(0) = 0), underdamped only.

    x(t) = A cos(omega t - phi) + e^{-gamma t} [C1 cos(omega_d t) + C2 sin(omega_d t)],
    with C1, C2 fixed by the zero initial conditions.
    """
    a, phi = analytic_amplitude_phase(omega, zeta, f, omega0)
    gamma = zeta * omega0
    wd = damped_natural_frequency(zeta, omega0)
    c1 = -a * math.cos(phi)
    c2 = -a * (gamma * math.cos(phi) + omega * math.sin(phi)) / wd
    return a * math.cos(omega * t - phi) + math.exp(-gamma * t) * (
        c1 * math.cos(wd * t) + c2 * math.sin(wd * t)
    )


# --------------------------------------------------------------------------
# RK4 over the autonomous state y = [x, v, t]; mirrors _lib/web/integrators.js
# rk4(y, dt, deriv) operation for operation, so both implementations can share
# the same stepper unmodified.
# --------------------------------------------------------------------------
def deriv(y: list[float], dy: list[float], omega: float, zeta: float, f: float,
          omega0: float = OMEGA0, model: str = "linear") -> None:
    x, v, t = y
    restoring = math.sin(x) if model == "pendulum" else omega0 * omega0 * x
    dy[0] = v
    dy[1] = -2.0 * zeta * omega0 * v - restoring + f * math.cos(omega * t)
    dy[2] = 1.0


def step_rk4(y: list[float], dt: float, omega: float, zeta: float, f: float, model: str = "linear") -> None:
    n = 3
    k1, k2, k3, k4, tmp = ([0.0] * n for _ in range(5))
    deriv(y, k1, omega, zeta, f, model=model)
    for i in range(n):
        tmp[i] = y[i] + k1[i] * dt / 2
    deriv(tmp, k2, omega, zeta, f, model=model)
    for i in range(n):
        tmp[i] = y[i] + k2[i] * dt / 2
    deriv(tmp, k3, omega, zeta, f, model=model)
    for i in range(n):
        tmp[i] = y[i] + k3[i] * dt
    deriv(tmp, k4, omega, zeta, f, model=model)
    for i in range(n):
        y[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * dt / 6


# --------------------------------------------------------------------------
# One validation case: run from rest, track the transient error against the
# closed form, then demodulate the tail window at the drive frequency to
# measure the steady-state amplitude and phase (a two-line-fit / lock-in
# amplifier: solve the 2x2 least-squares system for A cos(phi), A sin(phi)).
# --------------------------------------------------------------------------
def run_case(omega: float, zeta: float, f: float, dt: float) -> dict:
    gamma = zeta * OMEGA0
    settle_time = SETTLE_DECAY_LENGTHS / gamma
    period = 2.0 * math.pi / omega
    window_length = WINDOW_PERIODS * period
    total_time = settle_time + window_length
    steps_total = round(total_time / dt)
    steps_window = round(window_length / dt)
    window_start_step = steps_total - steps_window

    y = [0.0, 0.0, 0.0]
    transient_max_abs_error = 0.0
    sxx = sxy = syy = sxb = syb = 0.0
    for step in range(steps_total):
        step_rk4(y, dt, omega, zeta, f, model="linear")
        cf = closed_form_transient(y[2], omega, zeta, f)
        err = abs(y[0] - cf)
        if err > transient_max_abs_error:
            transient_max_abs_error = err
        if step + 1 > window_start_step:
            c = math.cos(omega * y[2])
            s = math.sin(omega * y[2])
            sxx += c * c
            sxy += c * s
            syy += s * s
            sxb += y[0] * c
            syb += y[0] * s

    det = sxx * syy - sxy * sxy
    in_phase = (sxb * syy - syb * sxy) / det
    quadrature = (sxx * syb - sxy * sxb) / det
    amplitude_measured = math.hypot(in_phase, quadrature)
    phase_measured = math.atan2(quadrature, in_phase)

    amplitude_analytic, phase_analytic = analytic_amplitude_phase(omega, zeta, f)
    omega_r = resonance_frequency(zeta)
    q = quality_factor(zeta)
    amplitude_relative_error = abs(amplitude_measured - amplitude_analytic) / amplitude_analytic
    phase_absolute_error = abs(phase_measured - phase_analytic)

    return {
        "omega": omega,
        "zeta": zeta,
        "F": f,
        "dt": dt,
        "settle_time": settle_time,
        "window_periods": WINDOW_PERIODS,
        "period": period,
        "total_time": total_time,
        "steps": steps_total,
        "analytic": {
            "amplitude": amplitude_analytic,
            "phase": phase_analytic,
            "omega_r": omega_r,
            "Q": q,
            "omega_d": damped_natural_frequency(zeta),
        },
        "rk4_amplitude": amplitude_measured,
        "rk4_phase": phase_measured,
        "amplitude_relative_error": amplitude_relative_error,
        "phase_absolute_error": phase_absolute_error,
        "steady_state_within_tolerance": (
            amplitude_relative_error <= STEADY_STATE_TOLERANCE["amplitude_relative"]
            and phase_absolute_error <= STEADY_STATE_TOLERANCE["phase_absolute"]
        ),
        "transient_max_abs_error": transient_max_abs_error,
        "transient_within_tolerance": transient_max_abs_error <= TRANSIENT_TOLERANCE_ABSOLUTE,
        "final_state": {"x": y[0], "v": y[1], "t": y[2]},
    }


def convergence_table() -> dict:
    """RK4 position error against the closed-form transient, at shrinking dt."""
    omega = CONVERGENCE_CASE["omega"]
    zeta = CONVERGENCE_CASE["zeta"]
    f = CONVERGENCE_CASE["f"]
    t_probe = CONVERGENCE_T_PROBE
    errors = []
    for dt in CONVERGENCE_DTS:
        steps = round(t_probe / dt)
        y = [0.0, 0.0, 0.0]
        for _ in range(steps):
            step_rk4(y, dt, omega, zeta, f, model="linear")
        errors.append(abs(y[0] - closed_form_transient(t_probe, omega, zeta, f)))
    log_dt = np.log(np.array(CONVERGENCE_DTS))
    log_err = np.log(np.array(errors))
    observed_order = float(np.polyfit(log_dt, log_err, 1)[0])
    return {
        "omega": omega,
        "zeta": zeta,
        "F": f,
        "t_probe": t_probe,
        "dts": list(CONVERGENCE_DTS),
        "position_errors": errors,
        "observed_order": observed_order,
        "expected_order": 4,
        "note": (
            "RK4 is fourth order: the position error against the closed-form transient "
            "at a fixed probe time should shrink as dt^4 as the step shrinks."
        ),
    }


def git_revision() -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(HERE), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def build() -> dict:
    cases = [
        run_case(omega, zeta, VALIDATION_F, VALIDATION_DT)
        for omega in VALIDATION_OMEGA
        for zeta in VALIDATION_ZETA
    ]
    return {
        "schema_version": 1,
        "chapter": "resonance-damping",
        "generator": "reference.py (numpy, float64)",
        "source_revision": git_revision(),
        "units": (
            "dimensionless: omega_0 = 1 sets the time scale, so omega, the damping "
            "ratio zeta = gamma/omega_0, and the drive amplitude F are all given in "
            "these units. RK4 integrates the autonomous state [x, v, t] at the stated "
            "step dt; the stability/accuracy bound for this stiffness is dt << 1/omega_0."
        ),
        "steady_state_tolerance": STEADY_STATE_TOLERANCE,
        "transient_tolerance_absolute": TRANSIENT_TOLERANCE_ABSOLUTE,
        "tolerance": BROWSER_TOLERANCE,
        "cases": cases,
        # Named dt_convergence, not convergence: renderChapter()'s built-in
        # convergence table assumes the orbits-numerical-error shape
        # (validation.convergence.rows[*] for several integrators); this
        # chapter has one integrator and one probe point, so it renders its
        # own table from this field instead (see index.html).
        "dt_convergence": convergence_table(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="recompute and fail if validation.json is stale")
    args = parser.parse_args()
    data = build()
    text = json.dumps(data, indent=2, sort_keys=False, allow_nan=False) + "\n"
    if args.check:
        if not OUT.is_file():
            print(f"error: {OUT} is missing; run reference.py")
            return 1
        stored = json.loads(OUT.read_text())
        fresh = json.loads(text)
        stored.pop("source_revision", None)
        fresh.pop("source_revision", None)
        if stored != fresh:
            print(f"error: {OUT.name} is stale; re-run reference.py")
            return 1
        print(f"{OUT.name}: {len(data['cases'])} cases (exact)")
        return 0
    OUT.write_text(text)
    print(f"{OUT.name}: {len(data['cases'])} cases, "
          f"convergence order {data['dt_convergence']['observed_order']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
