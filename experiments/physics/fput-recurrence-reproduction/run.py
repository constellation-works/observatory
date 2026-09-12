#!/usr/bin/env python3
"""The FPUT reproduction workbench: run, explore, report, browse evidence, export.

`baseline` executes the frozen protocol (v2 by default; `--protocol v1` reruns the
original for the record). `explore` executes an explicitly labelled exploratory run
with bounded parameter deviations. `report`, `evidence` and `export` present and
package an existing run and never recompute it.
"""

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
from fput import evidence as evidence_browser
from fput import export as export_package
from fput import report as study_report
from fput.compare import load_reference, matplotlib_version, plot_overlay, residual_table
from fput.explore import (
    ExplorationError,
    baseline_values,
    delta_hash,
    load_bounds,
    parse_assignments,
    resolve_delta,
)
from fput.integrate import simulate
from fput.metrics import evaluate_metrics
from fput.model import initial_state, total_energy
from fput.modes import mode_energies

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[2]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_outputs" / "physics" / EXPERIMENT_ROOT.name
# orbit-research refuses canonical record directories outside `research/`, so the
# owner-native records for this experiment live at the repository root; see
# research/README.md in this experiment directory.
DEFAULT_RECORDS_DIR = REPO_ROOT / "research" / "physics" / EXPERIMENT_ROOT.name / "records"


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


def _relative_token(token: str) -> str:
    """Record paths relative to the checkout: run.json must carry no absolute path."""
    if not token.startswith("/"):
        return token
    try:
        return Path(token).resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return "<outside-checkout>"


def recorded_invocation(arguments: list[str]) -> list[str]:
    runner = Path(__file__).resolve().relative_to(REPO_ROOT).as_posix()
    return ["uv", "run", runner, *(_relative_token(token) for token in arguments)]


def worktree_clean() -> bool | None:
    completed = subprocess.run(
        ["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    if completed.returncode != 0:
        return None
    return not completed.stdout.strip()


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
        "protocol_json": sha256(protocol_path),
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


def assessment(
    metrics: dict[str, dict[str, Any]], gating_controls: tuple[str, ...] = ("C1", "C2", "C3")
) -> tuple[str, str]:
    controls = [metrics[key]["pass"] for key in gating_controls]
    primary = [metrics[key]["pass"] for key in ("M1", "M2")]
    if any(value is False for value in controls):
        return "failed", "inconclusive"
    if any(value is None for value in controls + primary):
        return "inconclusive", "inconclusive"
    if not all(primary):
        return "failed", "undermines"
    return "completed", "supports"


def execute_run(
    *,
    protocol_version: str,
    output_dir: Path,
    kind: str,
    baseline_eligible: bool,
    parameter_delta: dict[str, dict[str, Any]],
    cycle_override: int | None,
    force_control_failure: str | None,
    arguments: list[str],
) -> int:
    """Execute one run into `output_dir`; never touch any other run directory."""
    output_dir.mkdir(parents=True, exist_ok=False)
    logger = RunLogger(output_dir / "log.txt")
    started_wall = datetime.now(UTC)
    started_monotonic = time.monotonic()
    protocol_path = EXPERIMENT_ROOT / "protocol" / f"{protocol_version}.json"
    reference_path = EXPERIMENT_ROOT / "reference" / "fig1-digitized.csv"
    run_record: dict[str, Any] = {
        "protocol_version": protocol_version,
        "kind": kind,
        "baseline_eligible": baseline_eligible,
        "command": recorded_invocation(arguments),
        "parameter_delta": parameter_delta,
        "started_at": started_wall.isoformat(),
        "status": "running",
        "control_results": {},
        "scientific_assessment": "not_evaluated",
    }
    if parameter_delta:
        run_record["exploration_bounds"] = {
            "source": "protocol/exploration.json",
            "applies_to_protocol": protocol_version,
        }
    write_json(output_dir / "run.json", run_record)

    exit_code = 3
    try:
        protocol = read_json(protocol_path)
        gating_controls = tuple(
            protocol.get("decision_rules", {}).get("gating_controls", ["C1", "C2", "C3"])
        )
        model = protocol["model"]
        n = int(model["parameters"]["N"])
        alpha = float(parameter_delta.get("alpha", {}).get("value", model["parameters"]["alpha"]))
        dt = float(parameter_delta.get("dt", {}).get("value", model["parameters"]["dt"]))
        protocol_steps = int(protocol["numerics"]["solver_settings"]["steps"])
        steps = int(
            parameter_delta.get("cycles", {}).get("value", cycle_override or protocol_steps)
        )
        sample_every = int(protocol["expected_output"]["sample_every_cycles"])
        timeout = float(protocol["compute_envelope"]["bounded_timeout_seconds"])
        deadline = started_monotonic + timeout
        inputs = verify_inputs(protocol_path, reference_path)
        reference = load_reference(reference_path)
        logger.write(f"command: {' '.join(run_record['command'])}")
        logger.write(
            f"protocol={protocol_version} N={n} alpha={alpha} dt={dt:.16g} steps={steps} "
            f"sample_every={sample_every} timeout={timeout:g}s kind={kind}"
        )
        if parameter_delta:
            logger.write(
                "bounded exploratory deviation: "
                + ", ".join(
                    f"{key}={item['value']} (baseline {item['baseline']})"
                    for key, item in sorted(parameter_delta.items())
                )
            )
        if cycle_override is not None:
            logger.write("cycle override supplied: output is explicitly non-baseline/exploratory")

        x0, v0 = initial_state(n)
        logger.write("integration started")
        cycles, positions, velocities = simulate(
            x0,
            v0,
            alpha=alpha,
            dt=dt,
            steps=steps,
            sample_every=sample_every,
            deadline=deadline,
            progress=lambda cycle: logger.write(f"progress: {cycle}/{steps} cycles"),
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
            force_control_failure=force_control_failure,
        )
        energy_units = modal / modal[0, 0] * 300.0
        write_energies(output_dir / "energies.csv", cycles, energy_units, protocol_version)
        write_json(output_dir / "metrics.json", metrics)
        plot_overlay(output_dir / "figure.png", cycles, energy_units, reference, protocol_version)

        status, scientific_assessment = assessment(metrics, gating_controls)
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
                "artifact_sha256": {
                    name: sha256(output_dir / name)
                    for name in ("energies.csv", "metrics.json", "figure.png")
                },
                "git_revision": revision,
                "git_worktree_clean": worktree_clean(),
                "uv_lock_sha256": sha256(REPO_ROOT / "uv.lock"),
                "effective_parameters": {
                    "N": n,
                    "alpha": alpha,
                    "dt": dt,
                    "steps": steps,
                    "sample_every_cycles": sample_every,
                    "normalization": "E_k(t)/E_1(0)*300",
                    "cycle_override": cycle_override,
                },
                "runtime": {
                    "host": socket.gethostname(),
                    "platform": platform.platform(),
                    "python": platform.python_version(),
                    "numpy": np.__version__,
                    "matplotlib": matplotlib_version(),
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


def timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%S-%fZ")


def latest_baseline(output_root: Path) -> Path:
    """The newest completed baseline-eligible run directory under `output_root`."""
    candidates = []
    for directory in sorted(output_root.glob("baseline-*")):
        record_path = directory / "run.json"
        if not record_path.is_file():
            continue
        record = read_json(record_path)
        if record.get("kind") == "baseline" and record.get("status") != "running":
            candidates.append(directory)
    if not candidates:
        raise FileNotFoundError(
            f"no baseline run under {_report_path(output_root)}; run `run.py baseline` first"
        )
    return candidates[-1]


def resolve_run(args: argparse.Namespace) -> Path:
    if getattr(args, "run", None) is not None:
        run_dir = args.run.resolve()
        if not (run_dir / "run.json").is_file():
            raise FileNotFoundError(f"{args.run} is not a run directory (no run.json)")
        return run_dir
    return latest_baseline(args.output_root.resolve())


def site_directory(args: argparse.Namespace) -> Path:
    return (args.site or (args.output_root / "site")).resolve()


def command_baseline(args: argparse.Namespace, arguments: list[str]) -> int:
    if args.cycles is not None and args.cycles <= 0:
        print("--cycles must be positive", file=sys.stderr)
        return 2
    output_dir = args.output_root.resolve() / f"baseline-{args.protocol}-{timestamp()}"
    return execute_run(
        protocol_version=args.protocol,
        output_dir=output_dir,
        kind="baseline" if args.cycles is None else "exploratory",
        baseline_eligible=args.cycles is None,
        parameter_delta={},
        cycle_override=args.cycles,
        force_control_failure=args.force_control_failure,
        arguments=arguments,
    )


def command_explore(args: argparse.Namespace, arguments: list[str]) -> int:
    protocol_dir = EXPERIMENT_ROOT / "protocol"
    protocol = read_json(protocol_dir / f"{args.protocol}.json")
    try:
        bounds = load_bounds(protocol, protocol_dir, args.protocol)
        assignments = parse_assignments(args.set)
        if args.cycles is not None:
            if "cycles" in assignments:
                raise ExplorationError("supply the cycle budget either as --cycles or --set cycles")
            assignments["cycles"] = str(args.cycles)
        delta = resolve_delta(assignments, bounds, baseline_values(protocol))
    except ExplorationError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    output_dir = (
        args.output_root.resolve()
        / f"explore-{delta_hash(args.protocol, delta)}-{timestamp()}"
    )
    return execute_run(
        protocol_version=args.protocol,
        output_dir=output_dir,
        kind="exploratory",
        baseline_eligible=False,
        parameter_delta=delta,
        cycle_override=delta.get("cycles", {}).get("value"),
        force_control_failure=None,
        arguments=arguments,
    )


def command_report(args: argparse.Namespace, _arguments: list[str]) -> int:
    try:
        run_dir = resolve_run(args)
    except FileNotFoundError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    output_root = args.output_root.resolve()
    explorations = [path for path in sorted(output_root.glob("explore-*")) if path.is_dir()]
    index = study_report.render(
        run_dir=run_dir,
        experiment_root=EXPERIMENT_ROOT,
        repo_root=REPO_ROOT,
        site_dir=site_directory(args),
        exploratory_runs=explorations,
    )
    print(json.dumps({"study_page": _report_path(index), "exploratory_runs": len(explorations)}))
    return 0


def command_evidence(args: argparse.Namespace, _arguments: list[str]) -> int:
    if args.bundle is not None and args.records is not None:
        print("refused: supply either --bundle or --records, not both", file=sys.stderr)
        return 2
    bundle = args.bundle.resolve() if args.bundle else None
    records = None
    if bundle is None:
        records = (args.records or DEFAULT_RECORDS_DIR).resolve()
    if bundle is not None and not bundle.is_file():
        print(f"refused: no export bundle at {args.bundle}", file=sys.stderr)
        return 2
    try:
        index = evidence_browser.render(
            evidence_dir=site_directory(args) / "evidence",
            bundle_path=bundle,
            records_dir=records,
        )
    except ValueError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "evidence_browser": _report_path(index),
                "source": "export-bundle" if bundle else "working-tree-records",
            }
        )
    )
    return 0


def command_export(args: argparse.Namespace, _arguments: list[str]) -> int:
    try:
        run_dir = resolve_run(args)
    except FileNotFoundError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    export_dir = (args.export_dir or (args.output_root / "export")).resolve()
    try:
        if args.check:
            archive = args.archive
            if archive is None:
                record = read_json(run_dir / "run.json")
                archive = export_dir / export_package.archive_name(
                    record["protocol_version"], run_dir.name
                )
            summary = export_package.check(archive.resolve())
        else:
            archive, manifest = export_package.build(
                run_dir=run_dir,
                experiment_root=EXPERIMENT_ROOT,
                repo_root=REPO_ROOT,
                site_dir=site_directory(args),
                records_dir=(args.records or DEFAULT_RECORDS_DIR).resolve(),
                export_dir=export_dir,
            )
            summary = {
                "archive": _report_path(archive),
                "members": len(manifest["members"]),
                "records": manifest["records"],
                "run_id": manifest["run_id"],
            }
    except export_package.ExportError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    print(json.dumps(summary))
    return 0


def _report_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.name


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    baseline = subparsers.add_parser("baseline", help="run the frozen protocol (v2 default)")
    baseline.add_argument(
        "--cycles",
        type=int,
        help="short diagnostic budget; labels the output non-baseline",
    )
    baseline.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    baseline.add_argument(
        "--protocol",
        choices=("v1", "v2"),
        default="v2",
        help="protocol version to load; v2 is the corrected-reference default",
    )
    baseline.add_argument(
        "--force-control-failure",
        choices=("C1", "C2", "C3"),
        help="validation hook: retain a distinct failed-control run",
    )
    baseline.set_defaults(handler=command_baseline)

    explore = subparsers.add_parser(
        "explore", help="run a bounded, explicitly labelled exploratory deviation"
    )
    explore.add_argument(
        "--set",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="bounded parameter deviation, e.g. --set alpha=1.0 (repeatable)",
    )
    explore.add_argument("--cycles", type=int, help="cycle budget; equivalent to --set cycles=N")
    explore.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    explore.add_argument("--protocol", choices=("v1", "v2"), default="v2")
    explore.set_defaults(handler=command_explore)

    report = subparsers.add_parser("report", help="render the static study page for a run")
    report.add_argument("--run", type=Path, help="run directory; default is the newest baseline")
    report.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    report.add_argument("--site", type=Path, help="site directory; default <output-root>/site")
    report.set_defaults(handler=command_report)

    evidence = subparsers.add_parser(
        "evidence", help="render the evidence browser from an orbit-research export bundle"
    )
    evidence.add_argument("--bundle", type=Path, help="validated orbit-research export.json")
    evidence.add_argument(
        "--records",
        type=Path,
        help="canonical records directory to browse when no export bundle exists yet",
    )
    evidence.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    evidence.add_argument("--site", type=Path, help="site directory; default <output-root>/site")
    evidence.set_defaults(handler=command_evidence)

    export = subparsers.add_parser(
        "export", help="build or verify the allowlisted evidence package"
    )
    export.add_argument("--run", type=Path, help="run directory; default is the newest baseline")
    export.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    export.add_argument("--site", type=Path, help="site directory; default <output-root>/site")
    export.add_argument(
        "--records", type=Path, help="records directory; default research/physics/<node>/records"
    )
    export.add_argument(
        "--export-dir", type=Path, help="archive directory; default <output-root>/export"
    )
    export.add_argument("--check", action="store_true", help="verify an existing archive instead")
    export.add_argument("--archive", type=Path, help="archive to verify with --check")
    export.set_defaults(handler=command_export)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    args = parse_args(arguments)
    return int(args.handler(args, arguments))


if __name__ == "__main__":
    raise SystemExit(main())
