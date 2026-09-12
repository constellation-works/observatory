"""The alpha-FPUT chain with unit masses and fixed endpoints."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def initial_state(n: int) -> tuple[FloatArray, FloatArray]:
    """Return the protocol's from-rest, single-mode initial state."""
    indices = np.arange(1, n, dtype=np.float64)
    x = np.sin(np.pi * indices / n)
    return x, np.zeros_like(x)


def spring_extensions(x: FloatArray) -> FloatArray:
    """Return x[i+1]-x[i] for all N springs, including fixed endpoints."""
    padded = np.empty(x.size + 2, dtype=np.float64)
    padded[0] = padded[-1] = 0.0
    padded[1:-1] = x
    return np.diff(padded)


def accelerations(x: FloatArray, alpha: float) -> FloatArray:
    """Evaluate the alpha-FPUT acceleration at every interior mass."""
    delta = spring_extensions(x)
    return delta[1:] - delta[:-1] + alpha * (delta[1:] ** 2 - delta[:-1] ** 2)


def total_energy(x: FloatArray, v: FloatArray, alpha: float) -> float:
    """Return kinetic plus quadratic and cubic spring potential energy."""
    delta = spring_extensions(x)
    kinetic = 0.5 * np.dot(v, v)
    potential = np.sum(0.5 * delta**2 + (alpha / 3.0) * delta**3)
    return float(kinetic + potential)


def linear_energy(x: FloatArray, v: FloatArray) -> float:
    """Return physical energy for the alpha=0 chain."""
    return total_energy(x, v, alpha=0.0)
