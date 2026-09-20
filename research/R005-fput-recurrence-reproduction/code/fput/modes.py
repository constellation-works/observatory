"""Normal-mode observables as defined by LA-1940 protocol v1."""

from __future__ import annotations

import numpy as np

from .model import FloatArray


def normal_mode_frequencies(n: int) -> FloatArray:
    k = np.arange(1, n, dtype=np.float64)
    return 2.0 * np.sin(np.pi * k / (2.0 * n))


def sine_basis(n: int) -> FloatArray:
    i = np.arange(1, n, dtype=np.float64)[:, None]
    k = np.arange(1, n, dtype=np.float64)[None, :]
    return np.sin(np.pi * i * k / n)


def mode_amplitudes(states: FloatArray, n: int) -> FloatArray:
    """Return unnormalised sums a_k = sum_i x_i sin(i*pi*k/N)."""
    return np.asarray(states, dtype=np.float64) @ sine_basis(n)


def mode_energies(positions: FloatArray, velocities: FloatArray, n: int) -> FloatArray:
    """Return E_k=1/2(adot_k^2 + omega_k^2 a_k^2) for every mode."""
    amplitudes = mode_amplitudes(positions, n)
    velocity_amplitudes = mode_amplitudes(velocities, n)
    omega = normal_mode_frequencies(n)
    return 0.5 * (velocity_amplitudes**2 + (amplitudes * omega) ** 2)


def physical_energy_from_modes(energies: FloatArray, n: int) -> FloatArray:
    """Undo the protocol amplitude's N/2 orthogonality factor."""
    return (2.0 / n) * np.sum(energies, axis=-1)
