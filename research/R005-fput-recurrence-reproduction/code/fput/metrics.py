"""Protocol-driven scientific metrics and numerical controls."""

from __future__ import annotations

import re
from typing import Any

import numpy as np


def _number(text: str, pattern: str) -> float:
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"cannot parse numeric tolerance from {text!r}")
    return float(match.group(1))


def protocol_tolerances(protocol: dict[str, Any]) -> dict[str, Any]:
    """Parse every threshold from protocol v1 rather than duplicating constants."""
    metrics = protocol["metrics"]
    controls = protocol["controls"]
    m3 = metrics["M3"]["tolerance"]
    return {
        "M1": _number(metrics["M1"]["tolerance"], r"<=\s*([0-9.]+)"),
        "M2": _number(metrics["M2"]["tolerance"], r"<=\s*([0-9.]+)"),
        "M3": {
            "time_relative": _number(m3["time"], r"([0-9.]+)\s*percent") / 100.0,
            "height_fraction_e1": _number(m3["height"], r"([0-9.]+)\s*percent") / 100.0,
        },
        "M4": _number(metrics["M4"]["tolerance"], r"=\s*([0-9.]+)\s+of"),
        "C1": _number(controls["C1"]["pass"], r"<=\s*([0-9.]+)"),
        "C2": _number(controls["C2"]["pass"], r"<=\s*([0-9.]+)"),
        "C3": _number(controls["C3"]["pass"], r"<\s*([0-9.]+)"),
    }


def first_local_maximum(cycles: np.ndarray, values: np.ndarray) -> tuple[int, float] | None:
    """Return the first strict discrete local maximum after cycle zero."""
    if values.size < 3:
        return None
    indices = np.flatnonzero((values[1:-1] >= values[:-2]) & (values[1:-1] > values[2:]))
    if indices.size == 0:
        return None
    index = int(indices[0] + 1)
    return int(cycles[index]), float(values[index])


def recurrence_peak(
    cycles: np.ndarray, values: np.ndarray, lower_cycle: int, upper_cycle: int
) -> tuple[int, float] | None:
    mask = (cycles >= lower_cycle) & (cycles <= upper_cycle)
    if not np.any(mask):
        return None
    selected = np.flatnonzero(mask)
    index = int(selected[np.argmax(values[mask])])
    return int(cycles[index]), float(values[index])


def relative_max_drift(values: np.ndarray) -> float:
    initial = float(values[0])
    if initial == 0.0:
        raise ValueError("cannot measure relative drift from zero")
    return float(np.max(np.abs(values / initial - 1.0)))


def _reported_feature(
    peak: tuple[int, float] | None, target: dict[str, Any] | None
) -> dict[str, Any]:
    value = None if peak is None else {"t_cycles": peak[0], "fraction_e1": peak[1]}
    reference = (
        None
        if target is None
        else {"t_cycles": target["t_cycles"], "fraction_e1": target["energy_units"] / 300.0}
    )
    residual = None
    if value is not None and reference is not None:
        residual = {
            "t_cycles": value["t_cycles"] - reference["t_cycles"],
            "fraction_e1": value["fraction_e1"] - reference["fraction_e1"],
        }
    return {"value": value, "reference": reference, "residual": residual}


def _m3_additional_reporting(
    cycles: np.ndarray,
    normalised: np.ndarray,
    ref_features: dict[str, Any],
    mode3_first: dict[str, Any] | None,
) -> dict[str, Any]:
    """Report (never gate) mode 5's first major peak and mode 3's second maximum."""
    mode5_peak = recurrence_peak(cycles, normalised[:, 4], 0, 20_000)
    mode3_second_peak = None
    if mode3_first is not None:
        # Skip well past the first peak's own shoulder so its decaying tail
        # cannot be mistaken for the (much later, ~19k cycle) second maximum.
        mode3_second_peak = recurrence_peak(
            cycles, normalised[:, 2], mode3_first["t_cycles"] + 2_000, 20_000
        )
    return {
        "mode5_first_major_peak": _reported_feature(
            mode5_peak, ref_features.get("mode5_first_maximum")
        ),
        "mode3_second_maximum": _reported_feature(
            mode3_second_peak, ref_features.get("mode3_second_maximum")
        ),
    }


def evaluate_metrics(
    *,
    cycles: np.ndarray,
    modal_energies: np.ndarray,
    total_energies: np.ndarray,
    linear_control_energies: np.ndarray,
    half_cycles: np.ndarray,
    half_modal_energies: np.ndarray,
    dt: float,
    reference: dict[str, Any],
    protocol: dict[str, Any],
    force_control_failure: str | None = None,
) -> dict[str, dict[str, Any]]:
    """Evaluate M1-M4 and C1-C3, retaining uncertainty and protocol wording."""
    tolerance = protocol_tolerances(protocol)
    version = protocol.get("protocol_version", "v1")
    initial_e1 = float(modal_energies[0, 0])
    normalised = modal_energies / initial_e1
    ref_features = reference["features"]

    recurrence = recurrence_peak(cycles, normalised[:, 0], 20_000, 30_000)
    half_recurrence = recurrence_peak(half_cycles, half_modal_energies[:, 0], 40_000, 60_000)

    def unevaluable(metric_id: str, note: str) -> dict[str, Any]:
        return {
            "value": None,
            "reference": None,
            "tolerance": tolerance[metric_id],
            "pass": None,
            "notes": note,
        }

    if recurrence is None:
        m1 = unevaluable("M1", "Cycle override does not cover the 20,000-30,000 window.")
        m2 = unevaluable("M2", "M1 recurrence is not evaluable.")
    else:
        recurrence_cycle, recurrence_fraction = recurrence
        reference_cycle = ref_features["mode1_recurrence"]["t_cycles"]
        reference_fraction = ref_features["mode1_recurrence"]["energy_units"] / 300.0
        m1 = {
            "value": recurrence_cycle,
            "reference": reference_cycle,
            "tolerance": tolerance["M1"],
            "pass": abs(recurrence_cycle - reference_cycle) <= tolerance["M1"],
            "notes": "Reference digitization uncertainty is +/-250 cycles.",
        }
        m2 = {
            "value": recurrence_fraction,
            "reference": reference_fraction,
            "tolerance": tolerance["M2"],
            "pass": abs(recurrence_fraction - reference_fraction) <= tolerance["M2"],
            "notes": "Reference digitization uncertainty is +/-5/300 of E1(0).",
        }

    m3_values: dict[str, Any] = {}
    m3_references: dict[str, Any] = {}
    m3_passes: dict[str, bool | None] = {}
    for mode in (2, 3, 4):
        if version == "v1":
            peak = first_local_maximum(cycles, normalised[:, mode - 1])
        else:
            peak = recurrence_peak(cycles, normalised[:, mode - 1], 0, 20_000)
        target = ref_features[f"mode{mode}_first_maximum"]
        key = f"mode_{mode}"
        m3_references[key] = {
            "t_cycles": target["t_cycles"],
            "fraction_e1": target["energy_units"] / 300.0,
        }
        if peak is None:
            m3_values[key] = None
            m3_passes[key] = None
            continue
        peak_cycle, peak_fraction = peak
        m3_values[key] = {"t_cycles": peak_cycle, "fraction_e1": peak_fraction}
        time_ok = abs(peak_cycle - target["t_cycles"]) <= (
            tolerance["M3"]["time_relative"] * target["t_cycles"]
        )
        height_ok = (
            abs(peak_fraction - target["energy_units"] / 300.0)
            <= tolerance["M3"]["height_fraction_e1"]
        )
        m3_passes[key] = bool(time_ok and height_ok)
    evaluable_m3 = all(value is not None for value in m3_passes.values())
    m3 = {
        "value": m3_values,
        "reference": m3_references,
        "tolerance": tolerance["M3"],
        "pass": bool(all(m3_passes.values())) if evaluable_m3 else None,
        "component_pass": m3_passes,
        "notes": (
            "Global maximum over cycles 0-20,000, per protocol v2."
            if version != "v1"
            else "First local maximum after cycle zero, per protocol v1."
        )
        + " Each digitized point carries +/-250 cycles and +/-5 energy units.",
    }
    if version != "v1":
        m3["additional_reporting"] = _m3_additional_reporting(
            cycles, normalised, ref_features, m3_values.get("mode_3")
        )

    if version == "v1":
        higher_mode_fraction = float(np.max(np.sum(normalised[:, 5:], axis=1)))
        m4 = {
            "value": higher_mode_fraction,
            "reference": tolerance["M4"],
            "tolerance": tolerance["M4"],
            "pass": higher_mode_fraction <= tolerance["M4"],
            "notes": "Compared with the caption ceiling of 20/300 of E1(0), summed over modes 6-31.",
        }
    else:
        per_mode_max = float(np.max(normalised[:, 5:]))
        summed_max = float(np.max(np.sum(normalised[:, 5:], axis=1)))
        m4 = {
            "value": per_mode_max,
            "reference": tolerance["M4"],
            "tolerance": tolerance["M4"],
            "pass": per_mode_max <= tolerance["M4"],
            "notes": "Compared with the caption ceiling of 20/300 of E1(0), per individual mode 6-31.",
            "additional_reporting": {"summed_modes_6_31_max": summed_max},
        }

    c1_value = relative_max_drift(linear_control_energies)
    c2_value = relative_max_drift(total_energies)
    c1 = {
        "value": c1_value,
        "reference": 0.0,
        "tolerance": tolerance["C1"],
        "pass": c1_value <= tolerance["C1"],
        "notes": protocol["controls"]["C1"]["definition"],
    }
    c2 = {
        "value": c2_value,
        "reference": 0.0,
        "tolerance": tolerance["C2"],
        "pass": c2_value <= tolerance["C2"],
        "notes": protocol["controls"]["C2"]["definition"],
    }

    if recurrence is None or half_recurrence is None:
        c3 = unevaluable("C3", "Cycle override does not cover both recurrence windows.")
    else:
        base_time = recurrence[0] * dt
        half_time = half_recurrence[0] * (dt / 2.0)
        movement = abs(half_time - base_time) / base_time
        c3 = {
            "value": movement,
            "reference": 0.0,
            "tolerance": tolerance["C3"],
            "pass": movement < tolerance["C3"],
            "notes": (
                f"Physical recurrence times: baseline={base_time:.9g}, dt/2={half_time:.9g}."
            ),
        }

    result = {"M1": m1, "M2": m2, "M3": m3, "M4": m4, "C1": c1, "C2": c2, "C3": c3}
    if force_control_failure is not None:
        result[force_control_failure]["pass"] = False
        result[force_control_failure]["notes"] += " Forced failure requested for validation."
    return result
