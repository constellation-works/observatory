"""Bounded exploratory deviations from the frozen baseline protocol.

Exploratory runs may only move parameters that a protocol artifact declares
explorable, inside the range it declares. The bounds live in the protocol's own
`exploration` block when it has one, and otherwise in the presentation-only
sidecar `protocol/exploration.json` (protocol v1 and v2 are frozen files).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SIDECAR_NAME = "exploration.json"


class ExplorationError(ValueError):
    """A usage error in an exploratory request: unknown key or out-of-range value."""


def load_bounds(protocol: dict[str, Any], protocol_dir: Path, protocol_version: str) -> dict[str, Any]:
    """Return the declared exploration block for this protocol version."""
    if isinstance(protocol.get("exploration"), dict):
        return protocol["exploration"]
    sidecar_path = protocol_dir / SIDECAR_NAME
    if not sidecar_path.is_file():
        raise ExplorationError(
            f"protocol {protocol_version} declares no exploration block and "
            f"{sidecar_path.name} is missing; exploratory runs are refused"
        )
    with sidecar_path.open(encoding="utf-8") as handle:
        sidecar = json.load(handle)
    applies_to = sidecar.get("applies_to", [])
    if protocol_version not in applies_to:
        raise ExplorationError(
            f"{sidecar_path.name} does not declare bounds for protocol {protocol_version} "
            f"(it applies to {', '.join(applies_to) or 'nothing'})"
        )
    block = sidecar.get("exploration")
    if not isinstance(block, dict) or not isinstance(block.get("parameters"), dict):
        raise ExplorationError(f"{sidecar_path.name} has no exploration.parameters block")
    return block


def baseline_values(protocol: dict[str, Any]) -> dict[str, Any]:
    """The baseline value of every explorable key, read from the named protocol."""
    parameters = protocol["model"]["parameters"]
    return {
        "alpha": float(parameters["alpha"]),
        "dt": float(parameters["dt"]),
        "cycles": int(protocol["numerics"]["solver_settings"]["steps"]),
    }


def parse_assignments(assignments: list[str]) -> dict[str, str]:
    """Parse --set key=value pairs, refusing duplicates and malformed input."""
    parsed: dict[str, str] = {}
    for assignment in assignments:
        key, separator, value = assignment.partition("=")
        key, value = key.strip(), value.strip()
        if not separator or not key or not value:
            raise ExplorationError(f"--set expects key=value, got {assignment!r}")
        if key in parsed:
            raise ExplorationError(f"--set {key} was supplied more than once")
        parsed[key] = value
    return parsed


def _coerce(key: str, value: str, declared: dict[str, Any]) -> float | int:
    kind = declared.get("type", "number")
    try:
        return int(value) if kind == "integer" else float(value)
    except ValueError as error:
        raise ExplorationError(f"{key} expects {'an integer' if kind == 'integer' else 'a number'}, got {value!r}") from error


def resolve_delta(
    assignments: dict[str, str], bounds: dict[str, Any], baseline: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """Validate requested deviations and return the recorded delta against baseline."""
    declared_parameters: dict[str, Any] = bounds["parameters"]
    delta: dict[str, dict[str, Any]] = {}
    for key in sorted(assignments):
        declared = declared_parameters.get(key)
        if declared is None:
            allowed = ", ".join(sorted(declared_parameters))
            raise ExplorationError(
                f"{key} is not an explorable parameter; the protocol declares only: {allowed}"
            )
        value = _coerce(key, assignments[key], declared)
        minimum, maximum = declared["minimum"], declared["maximum"]
        if not minimum <= value <= maximum:
            raise ExplorationError(
                f"{key}={value} is outside the declared exploration range "
                f"[{minimum}, {maximum}]; the run is refused"
            )
        if value == baseline[key]:
            raise ExplorationError(
                f"{key}={value} equals the baseline value; an exploratory run must differ "
                "from the registered baseline in at least one parameter"
            )
        delta[key] = {
            "baseline": baseline[key],
            "value": value,
            "path": declared.get("path"),
            "units": declared.get("units"),
            "declared_range": [minimum, maximum],
        }
    if not delta:
        raise ExplorationError("an exploratory run requires at least one --set key=value")
    return delta


def delta_hash(protocol_version: str, delta: dict[str, dict[str, Any]]) -> str:
    """Short, stable hash of the parameter delta: the run-directory discriminator."""
    payload = json.dumps(
        {"protocol": protocol_version, "delta": {k: v["value"] for k, v in delta.items()}},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:10]
