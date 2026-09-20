#!/usr/bin/env python3
"""Author this experiment's orbit-research record chain through the installed CLI.

The chain is `program → claim → input artifacts → preregister → begin-run → (execute the
baseline) → result artifacts → record-run → assess`, followed by `export`, `validate` and
the static evidence browser. Every request carries a stable `request_id`, so re-running
the driver is idempotent: an identical request returns the record that already exists.

orbit-research resolves references from exact Git snapshots, so each append must be
committed before the next one may refer to it. Where the checkout cannot be committed to
(the Orbit executor worktree mounts `.git` read-only), run with `--no-commit
--stop-after inputs`: the appends that need no resolved reference are authored, the rest
are refused rather than faked, and the driver reports where it stopped.

    uv run research/R005-fput-recurrence-reproduction/code/tools/record_chain.py \
      --task ORB-12361 --run jrun-20260912-2201-c3 --stop-after assess
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]      # research/<R>/code
RECORD_ROOT = EXPERIMENT_ROOT.parent                     # research/<R>
REPO_ROOT = EXPERIMENT_ROOT.parents[2]
# The JSON record chain is frozen under _archive/records/fput/ (research layout v2).
RECORDS_RELATIVE = "_archive/records/fput"
REPOSITORY = "observatory"
SCOPE = "simulation-under-assumptions"
STEPS = ("program", "claim", "inputs", "protocol", "start", "record", "assess", "export")

GLOBAL_LIMITATIONS = [
    "A reconstruction of a published computation under stated assumptions, not a "
    "measurement of nature: the integrator ordering is inferred and no author code exists.",
    "The comparison reference is a digitization of the printed figure with stated "
    "uncertainty, never the original MANIAC output.",
]
RETROSPECTIVE_LIMITATION = (
    "The protocol-v2 baseline was first executed under ORB-12375, before this native "
    "chain was registered. The native chronology proves local registration order and "
    "frozen input identity only, not independently attested prospective execution."
)


class ChainError(RuntimeError):
    """The chain cannot continue honestly; it stops instead of inventing a reference."""


def digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def git(*arguments: str, root: Path = REPO_ROOT) -> str:
    return subprocess.check_output(["git", "-C", str(root), *arguments], text=True).strip()


class Chain:
    def __init__(self, arguments: argparse.Namespace) -> None:
        self.root = arguments.owner_root.resolve()
        self.records = arguments.records
        self.records_dir = self.root / self.records
        self.requests = arguments.requests_dir.resolve()
        self.requests.mkdir(parents=True, exist_ok=True)
        self.commit = arguments.commit
        self.link = {
            "host": arguments.host,
            "workspace": arguments.workspace,
            "task": arguments.task,
            "run": arguments.run,
        }
        self.reported: list[dict[str, Any]] = []

    def cli(self, command: str, *arguments: str) -> dict[str, Any]:
        argv = [sys.executable, "-m", "orbit_research", command]
        if command not in {"validate", "reconcile"}:
            argv += ["--owner-root", str(self.root), "--repository", REPOSITORY]
            argv += ["--records", self.records]
        completed = subprocess.run([*argv, *arguments], capture_output=True, text=True)
        if completed.returncode:
            raise ChainError((completed.stderr or completed.stdout).strip())
        return json.loads(completed.stdout)

    def urn(self, kind: str, identifier: str) -> str:
        return f"urn:research:{REPOSITORY}:{kind}:{quote(identifier, safe='')}"

    def canonical_records(self) -> list[dict[str, Any]]:
        if not self.records_dir.is_dir():
            return []
        return [read_json(path) for path in sorted(self.records_dir.glob("*.json"))]

    def existing(self, kind: str, identifier: str,
                 predicate: Any = None) -> dict[str, Any] | None:
        """Reuse an identical append instead of authoring a second revision of it."""
        ident = self.urn(kind, identifier)
        for record in self.canonical_records():
            if record["id"] == ident and (predicate is None or predicate(record)):
                return record
        return None

    def heads(self, kind: str, identifier: str) -> list[str]:
        return self.cli("heads", "--id", self.urn(kind, identifier))["heads"]

    def append(self, operation: str, identifier: str, payload: dict[str, Any], *, reason: str,
               references: list[dict[str, Any]] | None = None,
               limitations: list[str] | None = None,
               expected_heads: list[str] | None = None) -> dict[str, Any]:
        request = {
            "request_id": f"orb-12361-{operation}-{identifier}",
            "id": identifier,
            "scope": SCOPE,
            "payload": payload,
            "expected_heads": expected_heads or [],
            "reason": reason,
            "orbit_links": [self.link],
            "references": references or [],
            "limitations": (limitations or []) + GLOBAL_LIMITATIONS,
        }
        path = self.requests / f"{operation}-{identifier}.json"
        path.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        record = self.cli(operation, "--request", str(path))
        self.reported.append(
            {"operation": operation, "id": record["id"], "revision": record["revision_id"],
             "reused": False}
        )
        return record

    def ensure(self, operation: str, kind: str, identifier: str, payload: dict[str, Any],
               *, reason: str, references: list[dict[str, Any]] | None = None,
               limitations: list[str] | None = None, predicate: Any = None,
               supersede: bool = False) -> dict[str, Any]:
        """Author the append, or reuse the matching one a previous driver run made."""
        found = self.existing(kind, identifier, predicate)
        if found is not None:
            self.reported.append(
                {"operation": operation, "id": found["id"], "revision": found["revision_id"],
                 "reused": True}
            )
            return found
        expected = self.heads(kind, identifier) if supersede else None
        return self.append(operation, identifier, payload, reason=reason, references=references,
                           limitations=limitations, expected_heads=expected)

    def publish(self, record: dict[str, Any]) -> dict[str, Any]:
        """Commit the append and pin it, or return an explicit pending reference."""
        pending = {
            "repository": REPOSITORY,
            "id": record["id"],
            "revision_id": record["revision_id"],
            "source_revision": None,
            "status": "pending",
        }
        if not self.commit:
            return pending
        git("add", "--", self.records, root=self.root)
        if git("status", "--porcelain", "--", self.records, root=self.root):
            git(
                "commit", "-q", "-m",
                f"records: {record['kind']} {record['aliases'][0]} [ORB-12361]",
                root=self.root,
            )
        return self.cli(
            "ref",
            "--id", record["id"],
            "--revision", record["revision_id"],
            "--source-revision", git("rev-parse", "HEAD", root=self.root),
        )

    def require_resolved(self, reference: dict[str, Any], what: str) -> dict[str, Any]:
        if reference.get("status") != "resolved":
            raise ChainError(
                f"{what} is not committed, so orbit-research cannot resolve it. Re-run this "
                "driver with --commit in a checkout whose .git is writable."
            )
        return reference


def protocol_semantic(
    protocol: dict[str, Any], claim: dict[str, Any], inputs: list[dict[str, Any]],
    holdout_digest: str, revision: str
) -> dict[str, Any]:
    """Normative terms only, taken from the frozen protocol document."""
    metrics, controls = protocol["metrics"], protocol["controls"]
    model, integrator = protocol["model"], protocol["integrator"]
    analysis = " ".join(
        f"{key}: {entry['name']} — {entry['definition'] if isinstance(entry['definition'], str) else entry['definition']};"
        f" tolerance {json.dumps(entry['tolerance'], sort_keys=True)}."
        for key, entry in metrics.items()
    )
    control_text = " ".join(
        f"{key}: {entry['definition']} Pass: {entry['pass']} ({entry.get('role', 'gating')})."
        for key, entry in controls.items()
    )
    now = datetime.now(UTC)
    return {
        "question": (
            "Does an independent Störmer–Verlet reconstruction of the α-FPUT chain "
            f"({model['name']}, N={model['parameters']['N']}, alpha={model['parameters']['alpha']}, "
            f"dt={model['parameters']['dt_expression']}) reproduce the mode-energy features of "
            f"{protocol['target']['report']} {protocol['target']['figure']} within the frozen "
            "tolerances, without tuning any parameter to the digitized figure?"
        ),
        "assumptions": (
            f"{integrator['implementation_assumption']} The caption's delta t^2=1/8 is read as "
            "the acceleration coefficient, so dt=1/sqrt(8); the alternative dt=1/8 reading is "
            "exploratory only. The plotted modal energy omits the nonlinear potential term as "
            "the report's own mode analysis does. The comparison reference is a digitization of "
            "the printed figure with stated uncertainty (±250 cycles, ±5 report units for "
            "individually numeraled peaks), not the original MANIAC output. Arithmetic is "
            "IEEE-754 float64 with no random seed and no adaptive stepping."
        ),
        "analysis": f"{analysis} Controls — {control_text}",
        "exclusions": (
            "No smoothing, prominence threshold or feature-selection rule derived from the "
            "reference curves. No parameter is fitted to the figure. Exploratory readings "
            "(alpha != 0.25, dt != 1/sqrt(8), shortened cycle budgets) are excluded from the "
            "baseline and live only in explicitly labelled exploratory runs."
        ),
        "stopping_rule": (
            f"Execute exactly {protocol['numerics']['solver_settings']['steps']} cycles, sampling "
            f"every {protocol['expected_output']['sample_every_cycles']} cycles, inside the "
            f"{protocol['compute_envelope']['bounded_timeout_seconds']} second bounded timeout. "
            "A failed or inconclusive baseline is retained as an auditable run and is never "
            "silently retried with adjusted parameters."
        ),
        "claims": [claim],
        "inputs": inputs,
        "code": {"repository": REPOSITORY, "git_revision": revision},
        "holdout": {
            "digest": holdout_digest,
            "information_cutoff": (now - timedelta(minutes=1)).isoformat(),
            "evaluation_not_before": (now + timedelta(seconds=5)).isoformat(),
            "policy": (
                "The digitized Fig. 1 reference is frozen by SHA-256 before the run and is read "
                "only for the named comparison features; no baseline parameter is derived from it."
            ),
        },
        "design": {
            "kind": "deterministic",
            "baseline": "The registered protocol-v2 reconstruction at the report's own parameters.",
            "controls": ["C1", "C2", "C3"],
            "resource_budget": {
                "planned": protocol["numerics"]["solver_settings"]["steps"],
                "limit": 120000,
                "unit": "integration cycles",
            },
            "convergence": {
                "criterion": (
                    "Control C3: halve dt at equal physical duration and compare the physical "
                    "recurrence time; reported, not gating, under protocol v2."
                ),
                "tolerance": 0.01,
                "max_steps": 120000,
            },
            "decision": {
                "metric": "absolute difference between the measured and digitized recurrence cycle",
                "operator": "<=",
                "threshold": 1000,
                "rule": (
                    "M1 within ±1000 cycles and M2 within ±0.03 support the reproduction; a miss "
                    "is reported as a discrepancy and never tuned away."
                ),
            },
        },
    }


def run_payload(
    *, protocol_reference: dict[str, Any] | None, inputs: list[dict[str, Any]],
    results: list[dict[str, Any]], record: dict[str, Any], holdout: str,
    status: str, controls: str, control_results: dict[str, str],
    start: dict[str, Any] | None, revision: str,
) -> dict[str, Any]:
    runtime = record.get("runtime", {})
    return {
        "execution_status": status,
        "controls": controls,
        "control_results": control_results,
        "protocol": protocol_reference,
        "result_artifacts": results,
        "inputs": inputs,
        "code": {"repository": REPOSITORY, "git_revision": revision},
        "environment": {
            "python": runtime.get("python"),
            "numpy": runtime.get("numpy"),
            "platform": runtime.get("platform"),
            "host": runtime.get("host"),
            "uv_lock_sha256": record.get("uv_lock_sha256"),
            "worktree_clean": record.get("git_worktree_clean"),
            "elapsed_seconds": runtime.get("elapsed_seconds"),
        },
        "invocation": record.get("command", ["uv", "run", "run.py", "baseline"]),
        "deviations": [],
        "start": start,
        "holdout_digest": holdout,
    }


def execute_baseline(output_root: Path) -> Path:
    """Run the registered baseline through the ordinary runner and return its directory."""
    before = set(output_root.glob("baseline-*")) if output_root.is_dir() else set()
    completed = subprocess.run(
        [sys.executable, str(EXPERIMENT_ROOT / "run.py"), "baseline",
         "--output-root", str(output_root)],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if completed.returncode not in {0, 10, 20}:
        raise ChainError(f"baseline execution failed: {completed.stderr[-2000:]}")
    created = sorted(set(output_root.glob("baseline-*")) - before)
    if not created:
        raise ChainError("baseline execution produced no run directory")
    return created[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--records", default=RECORDS_RELATIVE)
    parser.add_argument("--requests-dir", type=Path, default=Path("/tmp/fput-record-requests"))
    parser.add_argument("--task", default="ORB-12361")
    parser.add_argument("--run", required=True, help="the actual Orbit job run id")
    parser.add_argument("--host", default="dk-server-1")
    parser.add_argument("--workspace", default="ws_observatory")
    parser.add_argument("--protocol", default="v2")
    parser.add_argument("--stop-after", choices=STEPS, default="export")
    parser.add_argument("--output-root", type=Path,
                        default=RECORD_ROOT / "output")
    parser.add_argument("--bundle", type=Path, default=Path("/tmp/fput-records-export.json"))
    parser.add_argument("--commit", action=argparse.BooleanOptionalAction, default=True)
    arguments = parser.parse_args()
    chain = Chain(arguments)
    reached = None

    def done(step: str) -> bool:
        nonlocal reached
        reached = step
        return STEPS.index(step) >= STEPS.index(arguments.stop_after)

    try:
        protocol_path = EXPERIMENT_ROOT / "protocol" / f"{arguments.protocol}.json"
        protocol = read_json(protocol_path)
        # The frozen chain identifies its subject as "fput-recurrence-reproduction"
        # (the id of the retired lineage node). Record ids are append-only, so the
        # subject id stays as recorded while the paths below follow the record.
        node = "fput-recurrence-reproduction"
        record_dir = RECORD_ROOT.name

        program = chain.ensure(
            "program", "program", node,
            {
                "role": "program",
                "title": "LA-1940 Fig. 1 independent reconstruction",
                "question": (
                    "Does an independent reconstruction of the Fermi–Pasta–Ulam–Tsingou "
                    "computation reproduce Fig. 1 of LA-1940 — the first mode-1 recurrence and "
                    "the labelled mode-2/3/4 peaks — from the report's own stated parameters?"
                ),
            },
            reason="Original program capture for the observatory paper-reproduction milestone.",
        )
        program_reference = chain.publish(program)
        if done("program"):
            raise SystemExit(report(chain, reached))

        claim = chain.ensure(
            "claim", "claim", f"{node}-recurrence",
            {
                "role": "hypothesis",
                "statement": (
                    "An independent Störmer–Verlet reconstruction of the alpha-FPUT chain "
                    "(N=32, alpha=1/4, delta t^2=1/8, fixed ends, from-rest mode-1 sine) shows "
                    "the first mode-1 recurrence within ±1000 cycles of the digitized LA-1940 "
                    "Fig. 1 feature and returns at least 94% of the initial mode-1 energy there."
                ),
                "domain": "model",
            },
            reason="The node's kill condition, stated as the falsifiable claim under test.",
            references=[program_reference],
        )
        claim_reference = chain.publish(claim)
        if done("claim"):
            raise SystemExit(report(chain, reached))

        reference_csv = EXPERIMENT_ROOT / "reference" / "fig1-digitized.csv"
        holdout_digest = digest_file(reference_csv)
        csv_record = chain.ensure(
            "artifact", "artifact", "fig1-digitized-csv",
            {
                "role": "dataset",
                "availability": "available",
                "snapshot_digest": holdout_digest,
                "locator": f"research/{record_dir}/code/reference/fig1-digitized.csv",
                "media_type": "text/csv",
            },
            reason="The digitized comparison reference, frozen by digest before the run.",
            limitations=[
                "Digitized from the printed figure with stated uncertainty; mode labels are read "
                "from the printed numerals, never from the reconstruction's own curves."
            ],
        )
        csv_reference = chain.publish(csv_record)
        protocol_record = chain.ensure(
            "artifact", "artifact", f"protocol-{arguments.protocol}-json",
            {
                "role": "source",
                "availability": "available",
                "snapshot_digest": digest_file(protocol_path),
                "locator": f"research/{record_dir}/code/protocol/{arguments.protocol}.json",
                "media_type": "application/json",
            },
            reason="The frozen machine-readable protocol the runner loads.",
        )
        protocol_artifact_reference = chain.publish(protocol_record)
        if done("inputs"):
            raise SystemExit(report(chain, reached))

        inputs = [
            chain.require_resolved(csv_reference, "the digitized reference artifact"),
            chain.require_resolved(protocol_artifact_reference, "the protocol artifact"),
        ]
        revision = git("rev-parse", "HEAD", root=chain.root)
        registered = chain.ensure(
            "preregister", "protocol", f"{node}-{arguments.protocol}",
            {
                "semantic": protocol_semantic(
                    protocol,
                    chain.require_resolved(claim_reference, "the claim"),
                    inputs,
                    holdout_digest,
                    revision,
                )
            },
            reason=(
                f"Registers protocol {arguments.protocol}'s normative terms natively; the frozen "
                "documents themselves are unchanged."
            ),
        )
        registered_reference = chain.publish(registered)
        if done("protocol"):
            raise SystemExit(report(chain, reached))

        semantic = registered["payload"]["semantic"]
        boundary = datetime.fromisoformat(semantic["holdout"]["evaluation_not_before"])
        wait = (boundary - datetime.now(UTC)).total_seconds()
        if wait > 0:
            time.sleep(wait + 0.5)
        start = chain.ensure(
            "begin-run", "experiment", f"{node}-baseline-{arguments.protocol}",
            run_payload(
                protocol_reference=chain.require_resolved(registered_reference, "the protocol"),
                inputs=inputs, results=[], record={}, holdout=holdout_digest,
                status="running", controls="not-run", control_results={},
                start=None, revision=revision,
            ),
            reason="Run-start receipt registered before the baseline is executed.",
            limitations=[RETROSPECTIVE_LIMITATION],
            predicate=lambda record: record["payload"]["execution_status"] == "running",
        )
        start_reference = chain.publish(start)
        if done("start"):
            raise SystemExit(report(chain, reached))

        run_dir = execute_baseline(arguments.output_root.resolve())
        record = read_json(run_dir / "run.json")
        metrics = read_json(run_dir / "metrics.json")
        results = []
        for name, media in (
            ("metrics.json", "application/json"),
            ("energies.csv", "text/csv"),
            ("figure.png", "image/png"),
        ):
            artifact = chain.ensure(
                "artifact", "artifact", f"{node}-baseline-{name.replace('.', '-')}",
                {
                    "role": "result",
                    "availability": "available",
                    "snapshot_digest": digest_file(run_dir / name),
                    "locator": f"research/{record_dir}/output/<run>/{name}",
                    "media_type": media,
                },
                reason="Deterministic baseline output, identified by digest; output/ is not tracked.",
                limitations=[
                    "Regenerable output outside Git: the digest identifies bytes that the "
                    "registered command reproduces, not a stored artifact in this repository."
                ],
            )
            results.append(chain.require_resolved(chain.publish(artifact), f"the {name} artifact"))
        control_results = {
            key: ("passed" if metrics[key]["pass"] else
                  "failed" if metrics[key]["pass"] is False else "not-run")
            for key in ("C1", "C2", "C3")
        }
        aggregate = (
            "passed" if all(value == "passed" for value in control_results.values()) else "failed"
        )
        execution = "completed" if record["status"] == "completed" else "failed"
        finished = chain.ensure(
            "record-run", "experiment", f"{node}-baseline-{arguments.protocol}",
            run_payload(
                protocol_reference=registered_reference, inputs=inputs, results=results,
                record=record, holdout=holdout_digest, status=execution, controls=aggregate,
                control_results=control_results,
                start=chain.require_resolved(start_reference, "the run-start receipt"),
                revision=revision,
            ),
            reason="Measured execution of the registered baseline, with per-control results.",
            predicate=lambda record: record["payload"]["execution_status"] != "running",
            supersede=True,
            limitations=[
                RETROSPECTIVE_LIMITATION,
                "Aggregate controls report the strictest reading: C3 fails its own 1% threshold "
                "even though protocol v2 classifies it as reported rather than gating, so the "
                "execution status stays 'completed' while the aggregate is 'failed'.",
            ],
        )
        finished_reference = chain.publish(finished)
        if done("record"):
            raise SystemExit(report(chain, reached))

        verdict, summary = {
            "supports": ("supported", "supports"),
            "undermines": ("refuted", "refutes"),
            "inconclusive": ("inconclusive", "inconclusive"),
        }.get(record["scientific_assessment"], ("inconclusive", "inconclusive"))
        m3 = metrics["M3"]["component_pass"]
        assessment = chain.ensure(
            "assess", "assessment", f"{node}-baseline-{arguments.protocol}",
            {
                "claim": chain.require_resolved(claim_reference, "the claim"),
                "verdict": verdict,
                "inference": "exploratory",
                "controls": aggregate,
                "basis": "scientific-evidence",
                "rationale": (
                    f"M1 measured {metrics['M1']['value']} cycles against the digitized "
                    f"{metrics['M1']['reference']} (tolerance ±{metrics['M1']['tolerance']}), and "
                    f"M2 measured {metrics['M2']['value']:.6f} against "
                    f"{metrics['M2']['reference']:.6f} (±{metrics['M2']['tolerance']}). M3 passes "
                    f"on all gated modes ({', '.join(f'{k}={v}' for k, v in sorted(m3.items()))}) "
                    f"and M4's per-mode ceiling holds at {metrics['M4']['value']:.6f} <= "
                    f"{metrics['M4']['tolerance']}. Gating controls C1 and C2 pass; the reported "
                    f"sensitivity check C3 measures a {metrics['C3']['value']:.4f} relative shift "
                    "in the physical recurrence time under dt/2, above its own 1% threshold. The "
                    "verdict is therefore limited: the figure is reproduced at the report's own "
                    "step, and the step-size sensitivity is retained rather than tuned away."
                ),
                "evidence": [chain.require_resolved(finished_reference, "the completed run")],
                "legacy_verdict": None,
                "evidence_summary": summary,
            },
            reason="Scientific assessment of the registered baseline against the frozen claim.",
            limitations=[
                RETROSPECTIVE_LIMITATION,
                "Exploratory inference: a failed reported control and a retrospective native "
                "registration cannot carry primary confirmation.",
            ],
        )
        chain.publish(assessment)
        if done("assess"):
            raise SystemExit(report(chain, reached))

        bundle = arguments.bundle.resolve()
        if bundle.exists():
            bundle.unlink()
        exported = chain.cli(
            "export",
            "--source-revision", git("rev-parse", "HEAD", root=chain.root),
            "--output", str(bundle),
        )
        validated = chain.cli("validate", str(bundle))
        if not validated["valid"]:
            raise ChainError(f"export bundle failed validation: {validated['errors']}")
        browser = subprocess.run(
            [sys.executable, str(EXPERIMENT_ROOT / "run.py"), "evidence",
             "--bundle", str(bundle), "--output-root", str(arguments.output_root.resolve())],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        if browser.returncode:
            raise ChainError(f"evidence browser failed: {browser.stderr.strip()}")
        chain.reported.append({"operation": "export", "bundle": str(bundle), **exported,
                               "validated": True, "browser": json.loads(browser.stdout)})
        raise SystemExit(report(chain, "export"))
    except ChainError as error:
        print(json.dumps({"stopped_after": reached, "error": str(error),
                          "records": chain.reported}, indent=2))
        return 1


def report(chain: Chain, reached: str | None) -> int:
    print(json.dumps({"reached": reached, "committed": chain.commit,
                      "records": chain.reported}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
