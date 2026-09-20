"""Workbench slice: study-page renderer, exploratory isolation, evidence package."""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

import pytest

EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENT_ROOT.parents[2]
RUNNER = EXPERIMENT_ROOT / "run.py"


def runner(*arguments: str, expect: int | None = 0) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["uv", "run", str(RUNNER), *arguments],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    if expect is not None:
        assert completed.returncode == expect, completed.stdout + completed.stderr
    return completed


def directory_digest(directory: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.iterdir())
        if path.is_file()
    }


@pytest.fixture(scope="module")
def workbench(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    """One short baseline, one exploratory run, a rendered site and an export."""
    root = tmp_path_factory.mktemp("workbench")
    output_root = root / "runs"
    runner("baseline", "--cycles", "600", "--output-root", str(output_root), expect=10)
    baseline = next(iter(output_root.glob("baseline-*")))
    runner(
        "explore",
        "--set",
        "alpha=1.0",
        "--cycles",
        "600",
        "--output-root",
        str(output_root),
        expect=10,
    )
    exploratory = next(iter(output_root.glob("explore-*")))
    site = output_root / "site"
    runner(
        "report",
        "--run",
        str(baseline),
        "--output-root",
        str(output_root),
        "--site",
        str(site),
    )
    records = root / "records"
    records.mkdir()
    (records / "00000001-example.json").write_text(
        json.dumps({"kind": "program", "id": "urn:research:observatory:program:example"}) + "\n",
        encoding="utf-8",
    )
    runner(
        "export",
        "--run",
        str(baseline),
        "--output-root",
        str(output_root),
        "--site",
        str(site),
        "--records",
        str(records),
        "--export-dir",
        str(root / "export"),
    )
    archive = next(iter((root / "export").glob("*.tar.gz")))
    return {
        "root": root,
        "output_root": output_root,
        "baseline": baseline,
        "exploratory": exploratory,
        "site": site,
        "records": records,
        "archive": archive,
    }


# --- study page -------------------------------------------------------------------


def test_report_renders_every_required_section(workbench: dict[str, Path]) -> None:
    page = (workbench["site"] / "index.html").read_text(encoding="utf-8")
    for heading in (
        "1. Target",
        "2. Provenance and assumptions",
        "3. Original figure beside the reconstruction",
        "4. Residuals at the digitized feature points",
        "5. Metrics",
        "6. Execution status",
        "7. Control results",
        "8. Scientific assessment",
        "9. Provenance panel",
        "10. Exploratory runs",
        "11. Scientific records and evidence",
    ):
        assert heading in page, f"missing section: {heading}"
    record = json.loads((workbench["baseline"] / "run.json").read_text())
    assert record["uv_lock_sha256"] in page
    assert record["git_revision"] in page
    assert record["input_hashes"]["reference_fig1_digitized_csv"] in page
    assert record["artifact_sha256"]["energies.csv"] in page
    assert 'href="data/metrics.json"' in page
    assert "independent reconstruction" in page
    assert "10.2172/4376203" in page
    assert "EXPLORATORY" in page


def test_report_is_self_contained_without_remote_resources(workbench: dict[str, Path]) -> None:
    page = (workbench["site"] / "index.html").read_text(encoding="utf-8")
    assert page.count('src="data:image/png;base64,') >= 4
    assert "<style>" in page and 'rel="stylesheet"' not in page
    assert 'src="http' not in page and "@import" not in page
    for copied in ("data/metrics.json", "data/run.json"):
        assert (workbench["site"] / copied).is_file()


def test_report_reports_and_never_recomputes(workbench: dict[str, Path]) -> None:
    before = directory_digest(workbench["baseline"])
    runner(
        "report",
        "--run",
        str(workbench["baseline"]),
        "--output-root",
        str(workbench["output_root"]),
        "--site",
        str(workbench["site"]),
    )
    assert directory_digest(workbench["baseline"]) == before


def test_report_without_a_baseline_is_a_usage_error(tmp_path: Path) -> None:
    completed = runner("report", "--output-root", str(tmp_path), expect=2)
    assert "no baseline run" in completed.stderr


# --- exploratory isolation --------------------------------------------------------


def test_exploratory_run_is_labelled_and_records_its_delta(workbench: dict[str, Path]) -> None:
    record = json.loads((workbench["exploratory"] / "run.json").read_text())
    assert record["kind"] == "exploratory"
    assert record["baseline_eligible"] is False
    assert record["parameter_delta"]["alpha"] == {
        "baseline": 0.25,
        "value": 1.0,
        "path": "model.parameters.alpha",
        "units": "dimensionless cubic-spring coefficient",
        "declared_range": [0.0, 2.0],
    }
    assert record["effective_parameters"]["alpha"] == 1.0
    assert record["exploration_bounds"]["source"] == "protocol/exploration.json"
    assert workbench["exploratory"].name.startswith("explore-")


def test_exploratory_run_never_touches_the_baseline(tmp_path: Path) -> None:
    runner("baseline", "--cycles", "300", "--output-root", str(tmp_path), expect=10)
    baseline = next(iter(tmp_path.glob("baseline-*")))
    before = directory_digest(baseline)
    for arguments in (["--set", "dt=0.125"], ["--set", "alpha=1.0", "--set", "dt=0.25"]):
        runner("explore", *arguments, "--cycles", "300", "--output-root", str(tmp_path), expect=10)
    assert directory_digest(baseline) == before
    assert len(list(tmp_path.glob("baseline-*"))) == 1
    assert len(list(tmp_path.glob("explore-*"))) == 2


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (["--set", "alpha=5"], "outside the declared exploration range"),
        (["--set", "dt=0.0001"], "outside the declared exploration range"),
        (["--set", "beta=1.0"], "not an explorable parameter"),
        (["--set", "alpha=0.25"], "equals the baseline value"),
        (["--set", "alpha"], "expects key=value"),
        ([], "requires at least one --set"),
    ],
)
def test_out_of_range_and_unknown_parameters_are_refused(
    tmp_path: Path, arguments: list[str], message: str
) -> None:
    completed = runner("explore", *arguments, "--output-root", str(tmp_path), expect=2)
    assert message in completed.stderr
    assert not list(tmp_path.glob("explore-*"))


# --- evidence package -------------------------------------------------------------


def expected_members(records: Path) -> set[str]:
    return {
        "MANIFEST.json",
        "REPRODUCE.md",
        "study-report/index.html",
        "run/run.json",
        "run/metrics.json",
        "run/energies.csv",
        "run/figure.png",
        "protocol/v1.json",
        "protocol/v1.md",
        "protocol/v2.json",
        "protocol/v2.md",
        "protocol/exploration.json",
        "reference/fig1-digitized.csv",
        "reference/README.md",
        "reference/la-1940-fig1.png",
        "reproduction/commands.txt",
        "environment/uv.lock",
        "environment/README.md",
    } | {f"research/records/{path.name}" for path in records.glob("*.json")}


def test_export_contains_exactly_the_allowlist(workbench: dict[str, Path]) -> None:
    with tarfile.open(workbench["archive"], "r:gz") as handle:
        names = {info.name for info in handle.getmembers()}
        assert all(info.isfile() for info in handle.getmembers())
    assert names == expected_members(workbench["records"])
    assert not any(name.startswith("_data") or name.startswith("/") for name in names)
    assert not any("log.txt" in name for name in names)


def test_export_check_verifies_digests_and_absolute_paths(workbench: dict[str, Path]) -> None:
    completed = runner(
        "export",
        "--check",
        "--run",
        str(workbench["baseline"]),
        "--output-root",
        str(workbench["output_root"]),
        "--export-dir",
        str(workbench["root"] / "export"),
    )
    summary = json.loads(completed.stdout)
    assert summary["absolute_paths"] == 0
    assert summary["members_verified"] == len(expected_members(workbench["records"])) - 1


def rewrite_archive(source: Path, destination: Path, replacements: dict[str, bytes]) -> None:
    """Copy an archive, replacing named members; MANIFEST.json is passed through as-is."""
    with tarfile.open(source, "r:gz") as reader, tarfile.open(destination, "w:gz") as writer:
        for info in reader.getmembers():
            payload = reader.extractfile(info).read()
            payload = replacements.get(info.name, payload)
            info.size = len(payload)
            writer.addfile(info, io.BytesIO(payload))


def test_export_check_fails_on_a_tampered_member(workbench: dict[str, Path]) -> None:
    tampered = workbench["root"] / "tampered.tar.gz"
    rewrite_archive(workbench["archive"], tampered, {"run/metrics.json": b'{"M1": "edited"}\n'})
    completed = runner(
        "export",
        "--check",
        "--archive",
        str(tampered),
        "--run",
        str(workbench["baseline"]),
        "--output-root",
        str(workbench["output_root"]),
        expect=2,
    )
    assert "digest mismatch" in completed.stderr


def test_export_check_fails_on_an_absolute_path(workbench: dict[str, Path]) -> None:
    with tarfile.open(workbench["archive"], "r:gz") as handle:
        manifest = json.loads(handle.extractfile("MANIFEST.json").read())
    leaked = b"# Reproduce\n\nRun /home/someone/observatory/run.py baseline\n"
    for entry in manifest["members"]:
        if entry["name"] == "REPRODUCE.md":
            entry["sha256"] = hashlib.sha256(leaked).hexdigest()
            entry["bytes"] = len(leaked)
    payload = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    leaky = workbench["root"] / "leaky.tar.gz"
    rewrite_archive(
        workbench["archive"], leaky, {"REPRODUCE.md": leaked, "MANIFEST.json": payload}
    )
    completed = runner(
        "export",
        "--check",
        "--archive",
        str(leaky),
        "--run",
        str(workbench["baseline"]),
        "--output-root",
        str(workbench["output_root"]),
        expect=2,
    )
    assert "absolute paths found" in completed.stderr


# --- evidence browser -------------------------------------------------------------


def test_evidence_browser_over_working_tree_records_is_labelled(
    workbench: dict[str, Path], tmp_path: Path
) -> None:
    """Without a committed export bundle the browser says so instead of implying one."""
    records = workbench["root"] / "chain-records"
    records.mkdir()
    source = Path(
        "_archive/records/fput"
    )
    for path in sorted((REPO_ROOT / source).glob("*.json")):
        (records / path.name).write_bytes(path.read_bytes())
    site = tmp_path / "site"
    completed = runner(
        "evidence",
        "--records",
        str(records),
        "--output-root",
        str(workbench["output_root"]),
        "--site",
        str(site),
    )
    assert json.loads(completed.stdout)["source"] == "working-tree-records"
    page = (site / "evidence" / "index.html").read_text(encoding="utf-8")
    assert "Working-tree records, not a validated export" in page
    assert "urn:research:observatory:program:fput-recurrence-reproduction" in page
    assert (site / "evidence" / "export.json").is_file()


def test_evidence_refuses_a_bundle_that_is_not_an_export(tmp_path: Path) -> None:
    bundle = tmp_path / "not-an-export.json"
    bundle.write_text(json.dumps({"schema_version": 2, "kind": "trace"}), encoding="utf-8")
    completed = runner(
        "evidence", "--bundle", str(bundle), "--site", str(tmp_path / "site"), expect=2
    )
    assert "not an orbit-research v2 export bundle" in completed.stderr


def test_evidence_browser_shows_each_record_once_with_its_pinned_commits(
    tmp_path: Path,
) -> None:
    """A bundle repeats a record per export manifest; the browser is a view of the chain."""
    import sys

    sys.path.insert(0, str(EXPERIMENT_ROOT))
    from fput.evidence import dedupe_records, render

    def record(sequence: int, revision: str) -> dict:
        return {
            "id": "urn:research:observatory:claim:example",
            "kind": "claim",
            "activity": "active",
            "scope": "owner",
            "aliases": ["example-claim"],
            "revision_id": "sha256:" + "a" * 64,
            "authorship": {
                "sequence": sequence,
                "registered_at": "2026-09-12T00:00:00+00:00",
                "reason": "example",
            },
            "orbit_links": [{"task": "ORB-1", "run": "jrun-1"}],
            "payload": {"statement": "an example claim"},
            "provenance": {"git_revision": revision, "path": "research/records"},
        }

    duplicated = [record(2, "a" * 40), record(2, "b" * 40), record(2, "a" * 40)]
    entries = dedupe_records(duplicated)
    assert len(entries) == 1
    assert entries[0]["pinned_commits"] == ["a" * 40, "b" * 40]

    bundle = tmp_path / "export.json"
    bundle.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "kind": "export",
                "records": duplicated,
                "manifests": [],
                "unresolved": [],
            }
        ),
        encoding="utf-8",
    )
    index = render(evidence_dir=tmp_path / "evidence", bundle_path=bundle)
    page = index.read_text(encoding="utf-8")
    assert page.count("<details>") == 1, "one record, one entry"
    assert page.count("<tr>") == 2, "the chain table has one header row and one record row"
    assert "1 distinct records" in page
    assert "2 commit(s)" in page
