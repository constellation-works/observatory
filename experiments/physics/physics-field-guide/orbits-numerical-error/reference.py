#!/usr/bin/env python3
"""Independent Python reference for the "Orbits and numerical error" chapter.

Integrates the two-body Kepler problem (GM = 1, r0 = 1, planar, dimensionless)
with four schemes and writes ``validation.json``: the file the browser must
match at every predefined validation point, plus the convergence-order table
the page renders.

The browser is never its own oracle. ``orbits.js`` mirrors the arithmetic here
operation for operation, so agreement at the 1e-9 relative tolerance declared in
``chapter.json`` is a real cross-implementation check and not a tautology.

Usage:
    uv run experiments/physics/physics-field-guide/orbits-numerical-error/reference.py
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

MU = 1.0  # GM, dimensionless
R0 = 1.0  # initial radius, dimensionless

# Validation grid: every (v0, dt, integrator) point the browser must reproduce.
VALIDATION_V0 = (1.0, 0.6)
VALIDATION_DT = (0.05, 0.005)
VALIDATION_PERIODS = 10.0

# Convergence study: a mildly eccentric orbit over its first quarter period.
# The fit needs every scheme inside its asymptotic regime; over a full period the
# first-order schemes already carry an O(1) phase error and the fitted slope
# measures saturation rather than the order of the method.
CONVERGENCE_V0 = 0.8
CONVERGENCE_PERIODS = 0.25
CONVERGENCE_DTS = (0.01, 0.005, 0.0025, 0.00125)
EXPECTED_ORDER = {
    "euler": 1,
    "semi-implicit-euler": 1,
    "leapfrog-kdk": 2,
    "rk4": 4,
}
INTEGRATORS = tuple(EXPECTED_ORDER)


# --------------------------------------------------------------------------
# Dynamics. Plain float64 scalars in a fixed operation order; orbits.js does
# the same operations in the same order over Float64Array state.
# --------------------------------------------------------------------------
def compute_acc(pos: list[float], acc: list[float]) -> None:
    """acc <- -mu * pos / |pos|^3 (overwrites, never accumulates)."""
    r2 = pos[0] * pos[0] + pos[1] * pos[1]
    r = math.sqrt(r2)
    inv = MU / (r2 * r)
    acc[0] = -pos[0] * inv
    acc[1] = -pos[1] * inv


def deriv(y: list[float], dy: list[float]) -> None:
    """dy/dt for the first-order state y = [x, y, vx, vy]."""
    dy[0] = y[2]
    dy[1] = y[3]
    r2 = y[0] * y[0] + y[1] * y[1]
    r = math.sqrt(r2)
    inv = MU / (r2 * r)
    dy[2] = -y[0] * inv
    dy[3] = -y[1] * inv


def step_euler(pos, vel, acc, dt):
    """Explicit (forward) Euler: both updates use the state at the step start."""
    compute_acc(pos, acc)
    for i in range(2):
        pos[i] += vel[i] * dt
        vel[i] += acc[i] * dt


def step_semi_implicit_euler(pos, vel, acc, dt):
    """Symplectic Euler: velocity first, position with the *new* velocity."""
    compute_acc(pos, acc)
    for i in range(2):
        vel[i] += acc[i] * dt
        pos[i] += vel[i] * dt


def step_leapfrog_kdk(pos, vel, acc, dt):
    """Kick-drift-kick leapfrog; `acc` must already hold compute_acc(pos)."""
    h = dt / 2
    for i in range(2):
        vel[i] += acc[i] * h
    for i in range(2):
        pos[i] += vel[i] * dt
    compute_acc(pos, acc)
    for i in range(2):
        vel[i] += acc[i] * h


def step_rk4(pos, vel, acc, dt):
    """Classic RK4 over the packed state, mirroring _lib/web/integrators.js."""
    y = [pos[0], pos[1], vel[0], vel[1]]
    n = 4
    k1, k2, k3, k4, tmp = ([0.0] * n for _ in range(5))
    deriv(y, k1)
    for i in range(n):
        tmp[i] = y[i] + k1[i] * dt / 2
    deriv(tmp, k2)
    for i in range(n):
        tmp[i] = y[i] + k2[i] * dt / 2
    deriv(tmp, k3)
    for i in range(n):
        tmp[i] = y[i] + k3[i] * dt
    deriv(tmp, k4)
    for i in range(n):
        y[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) * dt / 6
    pos[0], pos[1], vel[0], vel[1] = y[0], y[1], y[2], y[3]


STEPPERS = {
    "euler": step_euler,
    "semi-implicit-euler": step_semi_implicit_euler,
    "leapfrog-kdk": step_leapfrog_kdk,
    "rk4": step_rk4,
}


def specific_energy(pos, vel) -> float:
    v2 = vel[0] * vel[0] + vel[1] * vel[1]
    r = math.sqrt(pos[0] * pos[0] + pos[1] * pos[1])
    return 0.5 * v2 - MU / r


def angular_momentum(pos, vel) -> float:
    return pos[0] * vel[1] - pos[1] * vel[0]


# --------------------------------------------------------------------------
# Analytic Kepler solution
# --------------------------------------------------------------------------
def elements(v0: float) -> dict:
    """Orbital elements for the state (r0, 0), (0, v0) with GM = 1.

    r0 is an apsis of the orbit: periapsis when v0 > 1, apoapsis when v0 < 1.
    """
    energy = 0.5 * v0 * v0 - MU / R0
    ang = R0 * v0
    ecc2 = 1 + 2 * energy * ang * ang / (MU * MU)
    ecc = math.sqrt(ecc2) if ecc2 > 0 else 0.0
    # Eccentricity vector e = (v x L)/mu - r_hat; here it is purely radial.
    ex = v0 * ang / MU - 1.0
    omega = math.atan2(0.0, ex) if ex != 0.0 else 0.0
    bound = energy < 0
    a = -0.5 * MU / energy if bound else float("nan")
    period = 2 * math.pi * a * math.sqrt(a) if bound else float("nan")
    return {
        "v0": v0,
        "energy": energy,
        "angular_momentum": ang,
        "eccentricity": ecc,
        "semi_major_axis": a,
        "semi_latus_rectum": ang * ang / MU,
        "periapsis": a * (1 - ecc) if bound else float("nan"),
        "apoapsis": a * (1 + ecc) if bound else float("nan"),
        "period": period,
        "argument_of_periapsis": omega,
        "bound": bound,
        "start_apsis": "periapsis" if v0 > 1 else ("apoapsis" if v0 < 1 else "circular"),
    }


def analytic_position(el: dict, t: float) -> tuple[float, float]:
    """Position at time t on the exact ellipse, via Kepler's equation.

    A fixed 60 Newton iterations (no convergence branch) so the Python and the
    JavaScript solvers execute an identical operation sequence.
    """
    a = el["semi_major_axis"]
    ecc = el["eccentricity"]
    omega = el["argument_of_periapsis"]
    n = 1.0 / (a * math.sqrt(a))
    m0 = math.pi if el["start_apsis"] == "apoapsis" else 0.0
    m = m0 + n * t
    two_pi = 2 * math.pi
    m = m - two_pi * math.floor(m / two_pi)
    ecc_anom = m
    for _ in range(60):
        f = ecc_anom - ecc * math.sin(ecc_anom) - m
        fp = 1 - ecc * math.cos(ecc_anom)
        ecc_anom = ecc_anom - f / fp
    xp = a * (math.cos(ecc_anom) - ecc)
    yp = a * math.sqrt(1 - ecc * ecc) * math.sin(ecc_anom)
    cw = math.cos(omega)
    sw = math.sin(omega)
    return (xp * cw - yp * sw, xp * sw + yp * cw)


# --------------------------------------------------------------------------
# One validation case
# --------------------------------------------------------------------------
def run_case(v0: float, dt: float, integrator: str, periods: float) -> dict:
    el = elements(v0)
    steps = math.floor(periods * el["period"] / dt + 0.5)
    pos = [R0, 0.0]
    vel = [0.0, v0]
    acc = [0.0, 0.0]
    compute_acc(pos, acc)  # leapfrog needs a primed acceleration
    e0 = specific_energy(pos, vel)
    l0 = angular_momentum(pos, vel)
    stepper = STEPPERS[integrator]
    max_e = 0.0
    max_l = 0.0
    for _ in range(steps):
        stepper(pos, vel, acc, dt)
        rel_e = abs(specific_energy(pos, vel) - e0) / abs(e0)
        rel_l = abs(angular_momentum(pos, vel) - l0) / abs(l0)
        if rel_e > max_e:
            max_e = rel_e
        if rel_l > max_l:
            max_l = rel_l
    t_final = steps * dt
    ax, ay = analytic_position(el, t_final)
    dx = pos[0] - ax
    dy = pos[1] - ay
    return {
        "v0": v0,
        "dt": dt,
        "integrator": integrator,
        "periods": periods,
        "steps": steps,
        "t_final": t_final,
        "final_rel_energy_error": abs(specific_energy(pos, vel) - e0) / abs(e0),
        "max_rel_energy_error": max_e,
        "final_rel_angular_momentum_error": abs(angular_momentum(pos, vel) - l0) / abs(l0),
        "max_rel_angular_momentum_error": max_l,
        "final_position_error": math.sqrt(dx * dx + dy * dy),
        "final_state": {"x": pos[0], "y": pos[1], "vx": vel[0], "vy": vel[1]},
    }


def convergence_table() -> dict:
    """Error at shrinking dt, with the order fitted by least squares in log-log."""
    el = elements(CONVERGENCE_V0)
    log_dt = np.log(np.array(CONVERGENCE_DTS))
    rows = []
    for integrator in INTEGRATORS:
        cases = [
            run_case(CONVERGENCE_V0, dt, integrator, CONVERGENCE_PERIODS)
            for dt in CONVERGENCE_DTS
        ]
        pos_err = [c["final_position_error"] for c in cases]
        energy_err = [c["max_rel_energy_error"] for c in cases]
        rows.append(
            {
                "integrator": integrator,
                "dts": list(CONVERGENCE_DTS),
                "position_errors": pos_err,
                "energy_errors": energy_err,
                "observed_order_position": float(np.polyfit(log_dt, np.log(pos_err), 1)[0]),
                "observed_order_energy": float(np.polyfit(log_dt, np.log(energy_err), 1)[0]),
                "expected_order": EXPECTED_ORDER[integrator],
            }
        )
    return {
        "v0": CONVERGENCE_V0,
        "periods": CONVERGENCE_PERIODS,
        "period": el["period"],
        "note": (
            "Fitted over the first quarter period, where every scheme is still in its "
            "asymptotic regime. Over a full period the first-order schemes already carry "
            "an O(1) phase error and the fitted slope no longer measures the method order."
        ),
        "rows": rows,
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
        run_case(v0, dt, integrator, VALIDATION_PERIODS)
        for v0 in VALIDATION_V0
        for dt in VALIDATION_DT
        for integrator in INTEGRATORS
    ]
    return {
        "schema_version": 1,
        "chapter": "orbits-numerical-error",
        "generator": "reference.py (numpy, float64)",
        "source_revision": git_revision(),
        "units": "dimensionless: GM = 1, r0 = 1, time in units of sqrt(r0^3/GM)",
        "tolerance": {"relative": 1e-9, "absolute": 1e-14},
        "analytic_elements": {f"v0={v0:g}": elements(v0) for v0 in (*VALIDATION_V0, CONVERGENCE_V0)},
        "cases": cases,
        "convergence": convergence_table(),
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
        # source_revision is provenance, not a number: it moves with every commit
        # and must not make the numeric payload look stale.
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
          f"{len(data['convergence']['rows'])} convergence rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
