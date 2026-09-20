"""Velocity-Verlet integration with the frozen protocol's explicit startup."""

from __future__ import annotations

import time
from collections.abc import Callable

import numpy as np

from .model import FloatArray, accelerations


def velocity_verlet_step(
    x: FloatArray, v: FloatArray, acceleration: FloatArray, dt: float, alpha: float
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Advance one full step and return x, v, and acceleration at the new time."""
    v_half = v + 0.5 * dt * acceleration
    x_next = x + dt * v_half
    acceleration_next = accelerations(x_next, alpha)
    v_next = v_half + 0.5 * dt * acceleration_next
    return x_next, v_next, acceleration_next


def simulate(
    x0: FloatArray,
    v0: FloatArray,
    *,
    alpha: float,
    dt: float,
    steps: int,
    sample_every: int,
    deadline: float | None = None,
    progress: Callable[[int], None] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Integrate and return sampled cycle numbers, positions, and velocities."""
    if steps < 0 or sample_every <= 0:
        raise ValueError("steps must be non-negative and sample_every must be positive")

    sample_cycles = list(range(0, steps + 1, sample_every))
    if sample_cycles[-1] != steps:
        sample_cycles.append(steps)
    positions = np.empty((len(sample_cycles), x0.size), dtype=np.float64)
    velocities = np.empty_like(positions)
    positions[0] = x0
    velocities[0] = v0

    x = np.array(x0, dtype=np.float64, copy=True)
    v = np.array(v0, dtype=np.float64, copy=True)
    acceleration = accelerations(x, alpha)
    sample_index = 1

    for cycle in range(1, steps + 1):
        x, v, acceleration = velocity_verlet_step(x, v, acceleration, dt, alpha)
        if not (np.all(np.isfinite(x)) and np.all(np.isfinite(v))):
            raise FloatingPointError(f"non-finite state at cycle {cycle}")
        if sample_index < len(sample_cycles) and cycle == sample_cycles[sample_index]:
            positions[sample_index] = x
            velocities[sample_index] = v
            sample_index += 1
        if progress is not None and cycle % 1000 == 0:
            progress(cycle)
        if deadline is not None and cycle % 100 == 0 and time.monotonic() > deadline:
            raise TimeoutError(f"protocol timeout exceeded at cycle {cycle}")

    return np.asarray(sample_cycles, dtype=np.int64), positions, velocities
