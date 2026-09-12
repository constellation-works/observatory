from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from fput.compare import load_reference
from fput.integrate import simulate
from fput.metrics import evaluate_metrics, first_local_maximum, protocol_tolerances
from fput.model import accelerations, initial_state, linear_energy, total_energy
from fput.modes import mode_energies, normal_mode_frequencies, physical_energy_from_modes

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = json.loads((EXPERIMENT_ROOT / "protocol" / "v1.json").read_text())


@pytest.mark.parametrize("mode", [1, 2, 7, 31])
def test_linear_mode_frequencies_match_force_eigenvalues(mode: int) -> None:
    n = 32
    indices = np.arange(1, n, dtype=np.float64)
    shape = np.sin(np.pi * mode * indices / n)
    omega = normal_mode_frequencies(n)[mode - 1]
    np.testing.assert_allclose(accelerations(shape, alpha=0.0), -(omega**2) * shape, atol=2e-14)


def test_total_energy_conservation_at_protocol_step() -> None:
    parameters = PROTOCOL["model"]["parameters"]
    x0, v0 = initial_state(parameters["N"])
    _, positions, velocities = simulate(
        x0,
        v0,
        alpha=parameters["alpha"],
        dt=parameters["dt"],
        steps=5_000,
        sample_every=25,
    )
    energies = np.asarray(
        [
            total_energy(x, v, parameters["alpha"])
            for x, v in zip(positions, velocities, strict=True)
        ]
    )
    assert np.max(np.abs(energies / energies[0] - 1.0)) < 0.01


def _linear_solution_error(dt: float, final_time: float = 10.0) -> float:
    n = 32
    mode = 3
    indices = np.arange(1, n, dtype=np.float64)
    x0 = np.sin(np.pi * mode * indices / n)
    v0 = np.zeros_like(x0)
    omega = normal_mode_frequencies(n)[mode - 1]
    steps = round(final_time / dt)
    _, positions, velocities = simulate(x0, v0, alpha=0.0, dt=dt, steps=steps, sample_every=steps)
    exact_x = x0 * np.cos(omega * final_time)
    exact_v = -omega * x0 * np.sin(omega * final_time)
    return float(np.linalg.norm(positions[-1] - exact_x) + np.linalg.norm(velocities[-1] - exact_v))


def test_velocity_verlet_has_second_order_dt_squared_convergence() -> None:
    coarse = _linear_solution_error(0.1)
    medium = _linear_solution_error(0.05)
    fine = _linear_solution_error(0.025)
    assert coarse / medium == pytest.approx(4.0, rel=0.08)
    assert medium / fine == pytest.approx(4.0, rel=0.08)


def test_mode_energy_sum_equals_total_linear_energy_after_normalization() -> None:
    rng = np.random.default_rng(321)
    n = 32
    positions = rng.normal(scale=0.1, size=(8, n - 1))
    velocities = rng.normal(scale=0.1, size=(8, n - 1))
    modal = mode_energies(positions, velocities, n)
    modal_total = physical_energy_from_modes(modal, n)
    direct = np.asarray([linear_energy(x, v) for x, v in zip(positions, velocities, strict=True)])
    np.testing.assert_allclose(modal_total, direct, rtol=2e-14, atol=2e-14)


def test_metric_functions_find_known_synthetic_features() -> None:
    cycles = np.arange(0, 30_001, 50)
    modal = np.full((cycles.size, 31), 1e-12)
    modal[:, 0] = 1.0 - 0.98 * np.sin(np.pi * cycles / (2 * 7_200)) ** 2
    for mode, peak_cycle, height in (
        (2, 6_200, 125 / 300),
        (3, 9_300, 210 / 300),
        (4, 13_500, 265 / 300),
    ):
        modal[:, mode - 1] = height * np.exp(-(((cycles - peak_cycle) / 1_000) ** 2))
    modal[:, 5:] = 0.001
    total = 1.0 + 1e-4 * np.sin(cycles / 100)
    linear = 1.0 + 1e-4 * np.cos(cycles / 100)
    half_cycles = np.arange(0, 60_001, 50)
    half_modal = np.full((half_cycles.size, 31), 1e-12)
    half_modal[:, 0] = 1.0 - 0.98 * np.sin(np.pi * half_cycles / (2 * 14_400)) ** 2

    metrics = evaluate_metrics(
        cycles=cycles,
        modal_energies=modal,
        total_energies=total,
        linear_control_energies=linear,
        half_cycles=half_cycles,
        half_modal_energies=half_modal,
        dt=PROTOCOL["model"]["parameters"]["dt"],
        reference=load_reference(EXPERIMENT_ROOT / "reference" / "fig1-digitized.csv"),
        protocol=PROTOCOL,
    )
    assert metrics["M1"]["value"] == 28_800
    assert metrics["M1"]["pass"] is True
    assert metrics["M3"]["pass"] is True
    assert metrics["M4"]["pass"] is True
    assert all(metrics[key]["pass"] for key in ("C1", "C2", "C3"))
    assert first_local_maximum(np.arange(5), np.array([0.0, 1.0, 3.0, 2.0, 1.0])) == (
        2,
        3.0,
    )
    assert protocol_tolerances(PROTOCOL)["M1"] == 1_000
