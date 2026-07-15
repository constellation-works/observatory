"""Geometric baseline models (ablation ladder rungs A-C).

Every model implements the ``Model`` protocol: ``fit`` sees only training
wells (loaders, not frames, so implementations control what they read) and
``predict`` sees only inference-time columns of the held-out well. Baselines
here are fit-free, but the interface is shared with the learned models so the
harness treats everything uniformly.
"""

from __future__ import annotations

from typing import Callable, Protocol

import numpy as np

from .data import WellPair

WellLoader = Callable[[str], WellPair]


class Model(Protocol):
    name: str

    def fit(self, train_wells: list[str], loader: WellLoader) -> None: ...

    def predict(self, pair: WellPair) -> np.ndarray:
        """Predicted TVT for every masked-suffix row of ``pair``."""
        ...


class ConstantTVT:
    """Rung A: hold the last observed TVT_input (target-following steering)."""

    name = "A_const"

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        pass

    def predict(self, pair: WellPair) -> np.ndarray:
        ps = pair.prediction_start
        anchor = pair.horizontal["TVT_input"].to_numpy()[ps - 1]
        return np.full(len(pair.horizontal) - ps, anchor)


class FlatLayer:
    """Rung B: flat topology, so all Z movement converts to TVT movement."""

    name = "B_flat"

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        pass

    def predict(self, pair: WellPair) -> np.ndarray:
        ps = pair.prediction_start
        z = pair.horizontal["Z"].to_numpy()
        anchor = pair.horizontal["TVT_input"].to_numpy()[ps - 1]
        return anchor - (z[ps:] - z[ps - 1])


class LinearTopology:
    """Rung C: extrapolate a robust line through the recent prefix topology.

    Topology is ``s = TVT_input + Z``; the fitted line is re-anchored to pass
    through the last known row so absolute-level error cancels.
    """

    name = "C_linear"

    def __init__(self, window_ft: float = 1000.0):
        self.window_ft = window_ft
        self.name = f"C_linear_{int(window_ft)}ft"

    def fit(self, train_wells: list[str], loader: WellLoader) -> None:
        pass

    def predict(self, pair: WellPair) -> np.ndarray:
        ps = pair.prediction_start
        h = pair.horizontal
        md = h["MD"].to_numpy()
        z = h["Z"].to_numpy()
        tvt_in = h["TVT_input"].to_numpy()
        anchor_tvt, anchor_z, anchor_md = tvt_in[ps - 1], z[ps - 1], md[ps - 1]

        lo = int(np.searchsorted(md[:ps], md[ps - 1] - self.window_ft))
        s_fit = tvt_in[lo:ps] + z[lo:ps]
        x_fit = md[lo:ps]
        ok = np.isfinite(s_fit)
        if ok.sum() < 2:
            return anchor_tvt - (z[ps:] - anchor_z)

        beta, alpha = np.polyfit(x_fit[ok], s_fit[ok], 1)
        s_hat = alpha + beta * md[ps:]
        s_hat += (anchor_tvt + anchor_z) - (alpha + beta * anchor_md)
        return s_hat - z[ps:]


def default_baselines() -> list[Model]:
    return [ConstantTVT(), FlatLayer(), LinearTopology(window_ft=1000.0)]
