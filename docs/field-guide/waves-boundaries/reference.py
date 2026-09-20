#!/usr/bin/env python3
"""Independent Python reference for the "Waves, interference and boundaries" chapter.

Integrates the linear N-mass chain (the alpha=0 case of the FPUT model
reproduced in ``research/R005-fput-recurrence-reproduction/code/``) with
Stormer-Verlet and writes ``validation.json``: the file the browser must match
at every predefined validation point.

The browser is never its own oracle. ``waves.js`` mirrors the arithmetic here
operation for operation, so agreement at the declared tolerance in
``chapter.json`` is a real cross-implementation check. A second, independent
comparison -- the measured period against the closed-form dispersion relation
omega_k = 2 sin(pi k / 2N) -- checks the physics itself, at a looser tolerance
because Stormer-Verlet has an O(dt^2) discretisation error that the analytic
formula does not.

Usage:
    uv run docs/field-guide/waves-boundaries/reference.py
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

N = 32          # masses, including the two (possibly fixed) endpoints
DT = 0.1        # fixed Stormer-Verlet step; stability bound is dt < 2/omega_max = 1
PULSE_AMPLITUDE = 1.0

# Dispersion / standing-wave validation: k = 1..8, N = 32, fixed ends.
DISPERSION_MODES = tuple(range(1, 9))
DISPERSION_PERIODS = 6.0          # periods of run, for a clean zero-crossing measurement
PERIOD_TOLERANCE = 0.01           # measured period vs analytic dispersion, relative

# Two-pulse superposition: pulses launched from the quarter points, meeting at
# the midpoint well before either reaches a wall (safe for t < 24).
SUPERPOSITION_I1 = N / 4          # 8
SUPERPOSITION_I2 = 3 * N / 4      # 24
SUPERPOSITION_SIGMA = 2.0
SUPERPOSITION_STEPS = 160         # t up to 16
SUPERPOSITION_PHASES = (0.0, math.pi)  # in phase (doubles), antiphase (cancels)

# Single-pulse reflection: launched near the boundary under test so the round
# trip is short and the pulse has not yet reached the far (always-fixed) end.
REFLECTION_I0 = 3 * N / 4         # 24, so the right wall is 8 lattice units away
REFLECTION_SIGMA = 1.5
REFLECTION_STEPS = 300            # t up to 30
REFLECTION_SEARCH_START = 100     # step index; skip the outgoing pulse itself
REFLECTION_BOUNDARIES = ("fixed", "free")

# dt^2 convergence: the same period measurement at shrinking dt.
CONVERGENCE_MODE = 4
CONVERGENCE_DTS = (0.2, 0.1, 0.05, 0.025)
CONVERGENCE_PERIODS = 6.0

TOLERANCE = {
    "relative": 1e-9,
    "absolute": 1e-9,
    "rationale": (
        "waves.js and reference.py run the same Stormer-Verlet algorithm in the same "
        "operation order in float64, so the two implementations agree to floating-point "
        "roundoff (the declared 1e-9 relative / 1e-9 absolute tolerance covers a legitimate "
        "difference in summation order). This is distinct from the physics tolerance below: "
        "a measured period always carries an O(dt^2) Stormer-Verlet discretisation error "
        "against the closed-form dispersion relation, declared separately per case as "
        "period_tolerance_relative."
    ),
}


# --------------------------------------------------------------------------
# Dynamics
# --------------------------------------------------------------------------
def lattice_indices(n: int = N) -> np.ndarray:
    """The N-1 movable lattice sites i = 1..N-1 (x_0 and, if fixed, x_N are walls)."""
    return np.arange(1, n, dtype=np.float64)


def accelerations(x: np.ndarray, boundary: str, n: int = N) -> np.ndarray:
    """ddot(x)_i = x_{i+1} + x_{i-1} - 2 x_i, with x_0 = 0 always.

    boundary='fixed': x_N = 0. boundary='free': x_N = x_{N-1} (zero-slope end).
    """
    right = 0.0 if boundary == "fixed" else x[-1]
    padded = np.empty(x.size + 2, dtype=np.float64)
    padded[0] = 0.0
    padded[1:-1] = x
    padded[-1] = right
    return padded[2:] + padded[:-2] - 2.0 * padded[1:-1]


def verlet_step(
    x: np.ndarray, v: np.ndarray, acc: np.ndarray, dt: float, boundary: str
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Stormer-Verlet (velocity form): advance one full step."""
    v_half = v + 0.5 * dt * acc
    x_next = x + dt * v_half
    acc_next = accelerations(x_next, boundary)
    v_next = v_half + 0.5 * dt * acc_next
    return x_next, v_next, acc_next


# --------------------------------------------------------------------------
# Normal modes (LA-1940 protocol formulas, reused unchanged)
# --------------------------------------------------------------------------
def mode_frequency(k: int, n: int = N) -> float:
    return 2.0 * math.sin(math.pi * k / (2.0 * n))


def mode_amplitude(state: np.ndarray, k: int, n: int = N) -> float:
    """a_k = sum_i x_i sin(i*pi*k/N), i = 1..N-1."""
    i = lattice_indices(n)
    return float(np.dot(state, np.sin(math.pi * i * k / n)))


def mode_energies(x: np.ndarray, v: np.ndarray, n: int = N) -> np.ndarray:
    """E_k = 1/2 (adot_k^2 + omega_k^2 a_k^2), for every k = 1..N-1."""
    i = lattice_indices(n)
    k = lattice_indices(n)
    basis = np.sin(np.pi * i[:, None] * k[None, :] / n)
    amplitudes = x @ basis
    velocity_amplitudes = v @ basis
    omega = 2.0 * np.sin(np.pi * k / (2.0 * n))
    return 0.5 * (velocity_amplitudes**2 + (amplitudes * omega) ** 2)


# --------------------------------------------------------------------------
# Initial conditions
# --------------------------------------------------------------------------
def standing_wave_init(k: int, n: int = N) -> tuple[np.ndarray, np.ndarray]:
    i = lattice_indices(n)
    x = np.sin(math.pi * i * k / n)
    return x, np.zeros_like(x)


def pulse_displacement(i: np.ndarray, i0: float, amplitude: float, sigma: float) -> np.ndarray:
    return amplitude * np.exp(-((i - i0) ** 2) / (2.0 * sigma * sigma))


def pulse_velocity(
    i: np.ndarray, i0: float, amplitude: float, sigma: float, direction: float
) -> np.ndarray:
    """Initial velocity for a d'Alembert packet f(i - direction*t - i0), c=1.

    v(i,0) = direction * (i-i0)/sigma^2 * f(i-i0); direction = +1 travels toward
    increasing i (rightward), -1 toward decreasing i (leftward).
    """
    profile = pulse_displacement(i, i0, amplitude, sigma)
    return direction * (i - i0) / (sigma * sigma) * profile


def two_pulse_init(
    i1: float, i2: float, amplitude: float, sigma: float, phase: float, n: int = N
) -> tuple[np.ndarray, np.ndarray]:
    i = lattice_indices(n)
    amplitude2 = amplitude * math.cos(phase)
    x = pulse_displacement(i, i1, amplitude, sigma) + pulse_displacement(i, i2, amplitude2, sigma)
    v = (
        pulse_velocity(i, i1, amplitude, sigma, +1.0)
        + pulse_velocity(i, i2, amplitude2, sigma, -1.0)
    )
    return x, v


def single_pulse_init(
    i0: float, amplitude: float, sigma: float, direction: float, n: int = N
) -> tuple[np.ndarray, np.ndarray]:
    i = lattice_indices(n)
    x = pulse_displacement(i, i0, amplitude, sigma)
    v = pulse_velocity(i, i0, amplitude, sigma, direction)
    return x, v


# --------------------------------------------------------------------------
# One run, sampling a scalar observable every step
# --------------------------------------------------------------------------
def run_observable(x0, v0, dt, boundary, steps, observe):
    x, v = np.array(x0, dtype=np.float64), np.array(v0, dtype=np.float64)
    acc = accelerations(x, boundary)
    times = [0.0]
    values = [observe(x, v)]
    for step in range(1, steps + 1):
        x, v, acc = verlet_step(x, v, acc, dt, boundary)
        times.append(step * dt)
        values.append(observe(x, v))
    return times, values


def zero_crossing_period(times: list[float], values: list[float]) -> float:
    """Period from twice the mean spacing between consecutive zero crossings."""
    crossings = []
    for j in range(len(values) - 1):
        a, b = values[j], values[j + 1]
        if a == 0.0:
            crossings.append(times[j])
        elif a * b < 0.0:
            t = times[j] + (times[j + 1] - times[j]) * (-a) / (b - a)
            crossings.append(t)
    spacings = [crossings[j + 1] - crossings[j] for j in range(len(crossings) - 1)]
    return 2.0 * (sum(spacings) / len(spacings))


# --------------------------------------------------------------------------
# Validation cases
# --------------------------------------------------------------------------
def dispersion_case(k: int, n: int = N, periods: float = DISPERSION_PERIODS, dt: float = DT) -> dict:
    omega_analytic = mode_frequency(k, n)
    period_analytic = 2.0 * math.pi / omega_analytic
    steps = round(periods * period_analytic / dt)
    x0, v0 = standing_wave_init(k, n)
    times, amps = run_observable(
        x0, v0, dt, "fixed", steps, lambda x, v: mode_amplitude(x, k, n)
    )
    period_measured = zero_crossing_period(times, amps)
    rel_error = abs(period_measured - period_analytic) / period_analytic
    return {
        "kind": "dispersion",
        "mode": k,
        "N": n,
        "dt": dt,
        "boundary": "fixed",
        "periods": periods,
        "steps": steps,
        "omega_k_analytic": omega_analytic,
        "period_analytic": period_analytic,
        "period_measured": period_measured,
        "period_relative_error": rel_error,
        "period_tolerance_relative": PERIOD_TOLERANCE,
        "period_within_tolerance": rel_error <= PERIOD_TOLERANCE,
    }


def superposition_case(phase: float, dt: float = DT, steps: int = SUPERPOSITION_STEPS) -> dict:
    boundary = "fixed"
    mid_index = int(N // 2) - 1  # array index of lattice site i = N/2

    def midpoint_series(x0, v0):
        _, vals = run_observable(x0, v0, dt, boundary, steps, lambda x, v: x[mid_index])
        return vals

    x1_0, v1_0 = single_pulse_init(SUPERPOSITION_I1, PULSE_AMPLITUDE, SUPERPOSITION_SIGMA, +1.0)
    amplitude2 = PULSE_AMPLITUDE * math.cos(phase)
    x2_0, v2_0 = single_pulse_init(SUPERPOSITION_I2, amplitude2, SUPERPOSITION_SIGMA, -1.0)
    series1 = midpoint_series(x1_0, v1_0)
    series2 = midpoint_series(x2_0, v2_0)
    predicted = [a + b for a, b in zip(series1, series2, strict=True)]

    x0, v0 = two_pulse_init(
        SUPERPOSITION_I1, SUPERPOSITION_I2, PULSE_AMPLITUDE, SUPERPOSITION_SIGMA, phase
    )
    measured = midpoint_series(x0, v0)

    predicted_max = max(predicted, key=abs)
    measured_max = max(measured, key=abs)
    return {
        "kind": "superposition",
        "N": N,
        "dt": dt,
        "boundary": boundary,
        "phase": phase,
        "steps": steps,
        "amplitude": PULSE_AMPLITUDE,
        "amplitude2": amplitude2,
        "sigma": SUPERPOSITION_SIGMA,
        "i1": SUPERPOSITION_I1,
        "i2": SUPERPOSITION_I2,
        "predicted_max": predicted_max,
        "measured_max": measured_max,
    }


def reflection_case(boundary: str, dt: float = DT, steps: int = REFLECTION_STEPS) -> dict:
    x0, v0 = single_pulse_init(REFLECTION_I0, PULSE_AMPLITUDE, REFLECTION_SIGMA, +1.0)
    detect_index = int(round(REFLECTION_I0)) - 1
    _, series = run_observable(
        x0, v0, dt, boundary, steps, lambda x, v: x[detect_index]
    )
    window = series[REFLECTION_SEARCH_START:]
    extremum = max(window, key=abs)
    measured_sign = 1.0 if extremum >= 0 else -1.0
    expected_sign = -1.0 if boundary == "fixed" else 1.0
    return {
        "kind": "reflection",
        "N": N,
        "dt": dt,
        "boundary": boundary,
        "steps": steps,
        "i0": REFLECTION_I0,
        "sigma": REFLECTION_SIGMA,
        "search_start_step": REFLECTION_SEARCH_START,
        "extremum": extremum,
        "measured_sign": measured_sign,
        "expected_sign": expected_sign,
        "sign_matches_expected": measured_sign == expected_sign,
    }


def convergence_table() -> dict:
    """Period relative error at shrinking dt, for one standing-wave mode."""
    k = CONVERGENCE_MODE
    period_analytic = 2.0 * math.pi / mode_frequency(k, N)
    dts = list(CONVERGENCE_DTS)
    period_errors = []
    for dt in dts:
        c = dispersion_case(k, N, CONVERGENCE_PERIODS, dt)
        period_errors.append(c["period_relative_error"])
    log_dt = np.log(np.array(dts))
    # A relative error can be exactly 0 in principle; guard the log-log fit.
    safe_errors = [max(e, 1e-16) for e in period_errors]
    observed_order = float(np.polyfit(log_dt, np.log(np.array(safe_errors)), 1)[0])
    return {
        "mode": k,
        "N": N,
        "boundary": "fixed",
        "periods": CONVERGENCE_PERIODS,
        "period_analytic": period_analytic,
        "dts": dts,
        "period_errors": period_errors,
        "observed_order": observed_order,
        "expected_order": 2,
        "note": (
            "Stormer-Verlet is second order: the measured standing-wave period's relative "
            "error against the analytic dispersion relation should shrink as dt^2."
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
    cases = [dispersion_case(k) for k in DISPERSION_MODES]
    cases += [superposition_case(phase) for phase in SUPERPOSITION_PHASES]
    cases += [reflection_case(b) for b in REFLECTION_BOUNDARIES]
    return {
        "schema_version": 1,
        "chapter": "waves-boundaries",
        "generator": "reference.py (numpy, float64)",
        "source_revision": git_revision(),
        "units": (
            "dimensionless: unit masses, unit springs, time in units of sqrt(m/k); "
            f"N = {N} masses, fixed Stormer-Verlet step dt = {DT} "
            "(stability bound dt < 2/omega_max = 1)"
        ),
        "N": N,
        "dt": DT,
        "tolerance": TOLERANCE,
        "cases": cases,
        # Named dt_convergence, not convergence: renderChapter()'s built-in
        # convergence table assumes the orbits-numerical-error shape
        # (validation.convergence.rows[*].position_errors / .energy_errors for
        # several integrators); this chapter has one integrator and one
        # observable, so it renders its own table from this field instead.
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
