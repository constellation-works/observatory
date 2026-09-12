from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import pytest

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENT_ROOT.parents[2]
RUNNER = EXPERIMENT_ROOT / "run.py"


def run_short(tmp_path: Path, *extra: str) -> tuple[subprocess.CompletedProcess[str], Path, float]:
    started = time.monotonic()
    completed = subprocess.run(
        [
            "uv",
            "run",
            str(RUNNER),
            "baseline",
            "--cycles",
            "200",
            "--output-root",
            str(tmp_path),
            *extra,
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    elapsed = time.monotonic() - started
    outputs = list(tmp_path.glob("baseline-*"))
    assert len(outputs) == 1
    return completed, outputs[0], elapsed


def test_short_cycle_override_is_auditable_and_fast(tmp_path: Path) -> None:
    completed, output, elapsed = run_short(tmp_path)
    assert completed.returncode == 10, completed.stdout + completed.stderr
    assert elapsed < 10
    assert {"run.json", "energies.csv", "metrics.json", "figure.png", "log.txt"} <= {
        path.name for path in output.iterdir()
    }
    run = json.loads((output / "run.json").read_text())
    assert run["kind"] == "exploratory"
    assert run["baseline_eligible"] is False
    assert run["effective_parameters"]["cycle_override"] == 200
    assert run["status"] == "inconclusive"
    assert run["protocol_version"] == "v2"


def test_protocol_v1_flag_still_runs_the_original(tmp_path: Path) -> None:
    completed, output, _ = run_short(tmp_path, "--protocol", "v1")
    assert completed.returncode == 10, completed.stdout + completed.stderr
    run = json.loads((output / "run.json").read_text())
    assert run["protocol_version"] == "v1"
    assert output.name.startswith("baseline-v1-")


def test_protocol_v1_forced_c3_failure_still_gates_status(tmp_path: Path) -> None:
    """v1 has no gating_controls override, so C3 still gates as it did originally."""
    completed, output, _ = run_short(
        tmp_path, "--protocol", "v1", "--force-control-failure", "C3"
    )
    assert completed.returncode == 20, completed.stdout + completed.stderr
    run = json.loads((output / "run.json").read_text())
    assert run["status"] == "failed"
    assert run["protocol_version"] == "v1"


@pytest.mark.parametrize("control", ["C1", "C2"])
def test_forced_gating_control_failure_has_distinct_failed_state(
    tmp_path: Path, control: str
) -> None:
    """C1 and C2 gate execution status under protocol v2 (default)."""
    completed, output, _ = run_short(tmp_path, "--force-control-failure", control)
    assert completed.returncode == 20, completed.stdout + completed.stderr
    run = json.loads((output / "run.json").read_text())
    metrics = json.loads((output / "metrics.json").read_text())
    assert run["status"] == "failed"
    assert run["control_results"][control] is False
    assert run["scientific_assessment"] == "inconclusive"
    assert metrics[control]["pass"] is False


def test_forced_c3_failure_is_reported_but_does_not_gate_status(tmp_path: Path) -> None:
    """Under protocol v2, C3 is a reported sensitivity check, not a gating control."""
    completed, output, _ = run_short(tmp_path, "--force-control-failure", "C3")
    assert completed.returncode == 10, completed.stdout + completed.stderr
    run = json.loads((output / "run.json").read_text())
    metrics = json.loads((output / "metrics.json").read_text())
    assert run["status"] == "inconclusive"
    assert run["control_results"]["C3"] is False
    assert metrics["C3"]["pass"] is False
