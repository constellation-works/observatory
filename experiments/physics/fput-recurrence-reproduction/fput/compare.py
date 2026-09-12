"""Digitized-reference loading and reconstruction overlay plotting."""

from __future__ import annotations

import csv
import os
import tempfile
from pathlib import Path
from typing import Any

import numpy as np

_cache_root = Path(tempfile.gettempdir()) / "observatory-fput-cache"
_cache_root.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_cache_root / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402


def matplotlib_version() -> str:
    """The plotting library version, recorded so a figure comparison is meaningful."""
    return str(matplotlib.__version__)


def load_reference(path: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    feature_names = {
        "mode-1 first recurrence maximum (digitized)": "mode1_recurrence",
        "mode-2 first maximum (digitized)": "mode2_first_maximum",
        "mode-3 first maximum (digitized)": "mode3_first_maximum",
        "mode-4 first maximum (digitized)": "mode4_first_maximum",
        "mode-5 first maximum (digitized)": "mode5_first_maximum",
        "mode-3 second maximum near 19k cycles (digitized)": "mode3_second_maximum",
    }
    features: dict[str, dict[str, float]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            parsed = {
                "mode": row["mode"],
                "t_cycles": float(row["t_cycles"]),
                "energy_units": float(row["energy_units"]),
                "feature": row["feature"],
            }
            rows.append(parsed)
            if row["feature"] in feature_names:
                features[feature_names[row["feature"]]] = parsed
    missing = set(feature_names.values()) - set(features)
    if missing:
        raise ValueError(f"digitized reference is missing named features: {sorted(missing)}")
    return {
        "rows": rows,
        "features": features,
        "uncertainty": {"t_cycles": 250.0, "energy_units": 5.0},
    }


def plot_overlay(
    output: Path,
    cycles: np.ndarray,
    energy_units: np.ndarray,
    reference: dict[str, Any],
    protocol_version: str = "v2",
) -> None:
    fig, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    colours = plt.get_cmap("tab10").colors
    for mode in range(1, 6):
        axis.plot(
            cycles / 1000.0,
            energy_units[:, mode - 1],
            color=colours[mode - 1],
            linewidth=1.5,
            label=f"mode {mode} reconstruction",
        )
        points = [row for row in reference["rows"] if row["mode"] == str(mode)]
        if points:
            axis.errorbar(
                [row["t_cycles"] / 1000.0 for row in points],
                [row["energy_units"] for row in points],
                xerr=reference["uncertainty"]["t_cycles"] / 1000.0,
                yerr=reference["uncertainty"]["energy_units"],
                fmt="o",
                color=colours[mode - 1],
                markerfacecolor="white",
                capsize=2,
                label=f"mode {mode} digitized feature",
            )
    axis.axhline(20.0, color="0.35", linestyle=":", label="modes 6-31 caption ceiling")
    axis.set(
        xlim=(0, 30),
        ylim=(0, 300),
        xlabel="cycles (thousands)",
        ylabel="modal energy (report units)",
    )
    axis.set_title(f"LA-1940 Fig. 1 independent reconstruction (protocol {protocol_version})")
    axis.grid(alpha=0.2)
    axis.legend(ncol=2, fontsize=8, loc="upper center")
    fig.savefig(output, dpi=160)
    plt.close(fig)


def residual_table(metrics: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Return measured-minus-reference residuals for every digitized feature."""
    rows: list[dict[str, Any]] = []
    for metric_id in ("M1", "M2", "M4"):
        metric = metrics[metric_id]
        residual = None
        if metric["value"] is not None and metric["reference"] is not None:
            residual = metric["value"] - metric["reference"]
        rows.append(
            {
                "feature": metric_id,
                "value": metric["value"],
                "reference": metric["reference"],
                "residual": residual,
            }
        )
    for mode in (2, 3, 4):
        key = f"mode_{mode}"
        value = metrics["M3"]["value"][key]
        reference = metrics["M3"]["reference"][key]
        rows.append(
            {
                "feature": f"M3 mode {mode}",
                "value": value,
                "reference": reference,
                "residual": (
                    None
                    if value is None
                    else {
                        "t_cycles": value["t_cycles"] - reference["t_cycles"],
                        "fraction_e1": value["fraction_e1"] - reference["fraction_e1"],
                    }
                ),
            }
        )
    return rows
