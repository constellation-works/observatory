#!/usr/bin/env python3
"""Execute the frozen protocol-v1 FPUT recurrence reconstruction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
import time
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from fput.compare import load_reference, plot_overlay, residual_table
from fput.integrate import simulate
from fput.metrics import evaluate_metrics
from fput.model import initial_state, total_energy
from fput.modes import mode_energies

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[2]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_outputs" / "physics" / EXPERIMENT_ROOT.name


class RunLogger:
    def __init__(self, path: Path) -> None:
        self._handle = path.open("w", encoding="utf-8")

    def write(self, message: str) -> None:
        line = f"{datetime.now(UTC).isoformat()} {message}"
        print(line, flush=True)
        self._handle.write(line + "\n")
        self._handle.flush()

    def close(self) -> None:
        self._handle.close()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def verify_inputs(protocol_path: Path, reference_path: Path) -> dict[str, str]:
    experiment_manifest = read_json(EXPERIMENT_ROOT / "manifest.json")
    if experiment_manifest.get("node") != EXPERIMENT_ROOT.name:
        raise ValueError("experiment manifest node does not match its directory")
    data_manifest_path = REPO_ROOT / experiment_manifest["data"][0]
    data_manifest = read_json(data_manifest_path)
    for required in ("source_url", "sha256", "size_bytes", "fetch_command"):
        if required not in data_manifest:
            raise ValueError(f"data manifest is missing {required}")
    return {
        "protocol_v1_json": sha256(protocol_path),
        "reference_fig1_digitized_csv": sha256(reference_path),
        "experiment_manifest": sha256(EXPERIMENT_ROOT / "manifest.json"),
        "source_data_manifest": sha256(data_manifest_path),
        "source_pdf_declared_sha256": data_manifest["sha256"],
    }


def sampled_total_energies(
    positions: np.ndarray, velocities: np.ndarray, alpha: float
) -> np.ndarray:
    return np.asarray(
        [total_energy(x, v, alpha) for x, v in zip(positions, velocities, strict=True)],
        dtype=np.float64,
    )


def write_energies(
    path: Path, cycles: np.ndarray, units: np.ndarray, protocol_version: str
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["cycle", "protocol_version", "normalization"]
            + [f"energy_mode_{mode}_units" for mode in range(1, 6)]
        )
        for cycle, row in zip(cycles, units[:, :5], strict=True):
            writer.writerow(
                [int(cycle), protocol_version, "E_k/E_1(0)*300"]
                + [f"{float(value):.12g}" for value in row]
            )


def result_table(metrics: dict[str, dict[str, Any]]) -> list[str]:
    lines = ["metric  value  reference  tolerance  pass"]
    for metric_id in ("M1", "M2", "M3", "M4", "C1", "C2", "C3"):
        metric = metrics[metric_id]
        lines.append(
            f"{metric_id:>3}  {metric['value']}  {metric['reference']}  "
            f"{metric['tolerance']}  {metric['pass']}"
        )
    return lines


def assessment(metrics: dict[str, dict[str, Any]]) -> tuple[str, str]:
    controls = [metrics[key]["pass"] for key in ("C1", "C2", "C3")]
    primary = [metrics[key]["pass"] for key in ("M1", "M2")]
    if any(value is False for value in controls):
        return "failed", "inconclusive"
    if any(value is None for value in controls + primary):
        return "inconclusive", "inconclusive"
    if not all(primary):
        return "failed", "undermines"
    return "completed", "supports"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    baseline = subparsers.add_parser("baseline", help="run frozen protocol v1")
    baseline.add_argument(
        "--cycles",
        type=int,
        help="short diagnostic budget; labels the output non-baseline",
    )
    baseline.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    baseline.add_argument(
        "--force-control-failure",
        choices=("C1", "C2", "C3"),
        help="validation hook: retain a distinct failed-control run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cycles is not None and args.cycles <= 0:
        print("--cycles must be positive", file=sys.stderr)
        return 2

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S-%fZ")
    output_dir = args.output_root.resolve() / f"baseline-v1-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=False)
    logger = RunLogger(output_dir / "log.txt")
    started_wall = datetime.now(UTC)
    started_monotonic = time.monotonic()
    protocol_path = EXPERIMENT_ROOT / "protocol" / "v1.json"
    reference_path = EXPERIMENT_ROOT / "reference" / "fig1-digitized.csv"
    run_record: dict[str, Any] = {
        "protocol_version": "v1",
        "kind": "baseline" if args.cycles is None else "exploratory",
        "baseline_eligible": args.cycles is None,
        "command": [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]],
        "started_at": started_wall.isoformat(),
        "status": "running",
        "control_results": {},
        "scientific_assessment": "not_evaluated",
    }
    write_json(output_dir / "run.json", run_record)

    exit_code = 3
    try:
        protocol = read_json(protocol_path)
        model = protocol["model"]
        n = int(model["parameters"]["N"])
        alpha = float(model["parameters"]["alpha"])
        dt = float(model["parameters"]["dt"])
        protocol_steps = int(protocol["numerics"]["solver_settings"]["steps"])
        steps = args.cycles if args.cycles is not None else protocol_steps
        sample_every = int(protocol["expected_output"]["sample_every_cycles"])
        timeout = float(protocol["compute_envelope"]["bounded_timeout_seconds"])
        deadline = started_monotonic + timeout
        inputs = verify_inputs(protocol_path, reference_path)
        reference = load_reference(reference_path)
        logger.write(f"command: {' '.join(run_record['command'])}")
        logger.write(
            f"protocol=v1 N={n} alpha={alpha} dt={dt:.16g} steps={steps} "
            f"sample_every={sample_every} timeout={timeout:g}s"
        )
        if args.cycles is not None:
            logger.write("cycle override supplied: output is explicitly non-baseline/exploratory")

        x0, v0 = initial_state(n)
        logger.write("baseline integration started")
        cycles, positions, velocities = simulate(
            x0,
            v0,
            alpha=alpha,
            dt=dt,
            steps=steps,
            sample_every=sample_every,
            deadline=deadline,
            progress=lambda cycle: logger.write(f"baseline progress: {cycle}/{steps} cycles"),
        )
        modal = mode_energies(positions, velocities, n)
        totals = sampled_total_energies(positions, velocities, alpha)

        c1_steps = min(10_000, steps)
        logger.write(f"C1 linear-chain control started ({c1_steps} cycles)")
        c1_cycles, c1_positions, c1_velocities = simulate(
            x0,
            v0,
            alpha=0.0,
            dt=dt,
            steps=c1_steps,
            sample_every=sample_every,
            deadline=deadline,
        )
        del c1_cycles
        c1_modal = mode_energies(c1_positions, c1_velocities, n)[:, 0]

        half_steps = 2 * steps
        logger.write(f"C3 dt/2 control started ({half_steps} cycles at equal physical duration)")
        half_cycles, half_positions, half_velocities = simulate(
            x0,
            v0,
            alpha=alpha,
            dt=dt / 2.0,
            steps=half_steps,
            sample_every=sample_every,
            deadline=deadline,
        )
        half_modal = mode_energies(half_positions, half_velocities, n)

        metrics = evaluate_metrics(
            cycles=cycles,
            modal_energies=modal,
            total_energies=totals,
            linear_control_energies=c1_modal,
            half_cycles=half_cycles,
            half_modal_energies=half_modal,
            dt=dt,
            reference=reference,
            protocol=protocol,
            force_control_failure=args.force_control_failure,
        )
        energy_units = modal / modal[0, 0] * 300.0
        write_energies(output_dir / "energies.csv", cycles, energy_units, "v1")
        write_json(output_dir / "metrics.json", metrics)
        plot_overlay(output_dir / "figure.png", cycles, energy_units, reference)

        status, scientific_assessment = assessment(metrics)
        control_results = {key: metrics[key]["pass"] for key in ("C1", "C2", "C3")}
        ended = datetime.now(UTC)
        runtime = time.monotonic() - started_monotonic
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        run_record.update(
            {
                "status": status,
                "control_results": control_results,
                "scientific_assessment": scientific_assessment,
                "input_hashes": inputs,
                "git_revision": revision,
                "uv_lock_sha256": sha256(REPO_ROOT / "uv.lock"),
                "effective_parameters": {
                    "N": n,
                    "alpha": alpha,
                    "dt": dt,
                    "steps": steps,
                    "sample_every_cycles": sample_every,
                    "normalization": "E_k(t)/E_1(0)*300",
                    "cycle_override": args.cycles,
                },
                "runtime": {
                    "host": socket.gethostname(),
                    "platform": platform.platform(),
                    "python": platform.python_version(),
                    "numpy": np.__version__,
                    "pid": os.getpid(),
                    "elapsed_seconds": runtime,
                    "timeout_seconds": timeout,
                },
                "ended_at": ended.isoformat(),
                "exit_code": {"completed": 0, "inconclusive": 10, "failed": 20}[status],
            }
        )
        write_json(output_dir / "run.json", run_record)
        for line in result_table(metrics):
            logger.write(line)
        logger.write("digitized feature residuals (measured minus reference)")
        for row in residual_table(metrics):
            logger.write(str(row))
        logger.write(
            f"final status={status} controls={control_results} "
            f"assessment={scientific_assessment} elapsed={runtime:.3f}s output={output_dir}"
        )
        exit_code = int(run_record["exit_code"])
    except Exception as error:  # every infrastructure failure must remain auditable
        ended = datetime.now(UTC)
        runtime = time.monotonic() - started_monotonic
        diagnostic = "".join(traceback.format_exception(error))
        logger.write(f"FAILED: {error}\n{diagnostic}")
        run_record.update(
            {
                "status": "failed",
                "control_results": run_record.get("control_results", {}),
                "scientific_assessment": "not_evaluated",
                "ended_at": ended.isoformat(),
                "runtime": {"elapsed_seconds": runtime},
                "exit_code": 3,
                "error": {"type": type(error).__name__, "message": str(error)},
            }
        )
        write_json(output_dir / "run.json", run_record)
        exit_code = 3
    finally:
        logger.close()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
