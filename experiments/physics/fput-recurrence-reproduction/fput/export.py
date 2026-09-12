"""Allowlisted evidence package: build and verify.

`build` writes a tar.gz whose members are named explicitly, one at a time. Nothing is
walked, so a stray cache, a `_data` payload or an unrelated worktree file cannot enter.
`check` extracts the archive into a temporary directory, verifies every digest recorded
in its MANIFEST.json, and refuses absolute paths, traversal and unlisted members.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import shutil
import tarfile
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ARCHIVE_STEM = "fput-reproduction"
MANIFEST_NAME = "MANIFEST.json"

# Absolute-path shapes that must never reach a recipient. `/tmp/...` is deliberately
# allowed: REPRODUCE.md tells the reader to create a throwaway environment there.
ABSOLUTE_PATH_PATTERNS = (
    r"/home/",
    r"/Users/",
    r"/root/",
    r"/private/var/folders/",
)

TEXT_SUFFIXES = {".md", ".json", ".csv", ".txt", ".html", ".lock", ".toml", ".py"}


class ExportError(ValueError):
    """The export or its verification failed; the archive is not trustworthy."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def archive_name(protocol_version: str, run_id: str) -> str:
    return f"{ARCHIVE_STEM}-{protocol_version}-{run_id}.tar.gz"


def _commands(experiment: str, run_dir_name: str) -> str:
    runner = f"experiments/physics/{experiment}/run.py"
    return "\n".join(
        [
            "# Exact commands that produced this package, from the observatory checkout root.",
            "# Paths are repository-relative; nothing here depends on the author's home directory.",
            "uv sync --extra research",
            f"uv run {runner} baseline",
            f"uv run {runner} explore --set alpha=1.0",
            f"uv run {runner} explore --set dt=0.125",
            f"uv run {runner} report --run _outputs/physics/{experiment}/{run_dir_name}",
            f"uv run {runner} export",
            f"uv run {runner} export --check",
            "",
        ]
    )


def _environment_readme(record: dict[str, Any], manifest: dict[str, Any], lock_digest: str) -> str:
    runtime = record.get("runtime", {})
    return "\n".join(
        [
            "# Environment",
            "",
            "`uv.lock` in this directory is the observatory workspace lock as committed at the",
            f"code revision recorded in `run/run.json` (`{record.get('git_revision')}`), with",
            f"SHA-256 `{lock_digest}`. The run recorded Python `{runtime.get('python')}`,",
            f"NumPy `{runtime.get('numpy')}` and Matplotlib `{runtime.get('matplotlib')}` on",
            f"platform `{runtime.get('platform')}`.",
            "",
            "`metrics.json` and `energies.csv` are byte-reproducible from the NumPy version",
            "alone; `figure.png` additionally depends on the Matplotlib version.",
            "",
            "## Source document",
            "",
            f"- Work: {manifest['title']} ({', '.join(manifest['authors'])}), {manifest['published']}.",
            f"- Public source: {manifest['source_url']} (DOI {manifest['doi']}).",
            f"- Licence: {manifest['licence']}.",
            f"- PDF SHA-256: `{manifest['sha256']}` ({manifest['size_bytes']} bytes).",
            "",
            "The PDF itself is intentionally **not** included: this package identifies it by",
            "digest and fetch command instead, exactly as the repository's data manifest does.",
            "",
            f"    {manifest['fetch_command']}",
            f"    {manifest['verify_command']}",
            "",
        ]
    )


def plan(
    *,
    run_dir: Path,
    experiment_root: Path,
    repo_root: Path,
    site_dir: Path,
    records_dir: Path,
) -> tuple[list[tuple[str, Path]], list[tuple[str, bytes]], dict[str, Any]]:
    """Return (file members, generated members, metadata) for one run: the whole allowlist."""
    record = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    data_manifest = json.loads(
        (repo_root / "_data" / "physics" / experiment_root.name / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    protocol_version = record["protocol_version"]
    files: list[tuple[str, Path]] = [
        ("REPRODUCE.md", experiment_root / "REPRODUCE.md"),
        ("study-report/index.html", site_dir / "index.html"),
        ("run/run.json", run_dir / "run.json"),
        ("run/metrics.json", run_dir / "metrics.json"),
        ("run/energies.csv", run_dir / "energies.csv"),
        ("run/figure.png", run_dir / "figure.png"),
        ("protocol/v1.json", experiment_root / "protocol" / "v1.json"),
        ("protocol/v1.md", experiment_root / "protocol" / "v1.md"),
        ("protocol/v2.json", experiment_root / "protocol" / "v2.json"),
        ("protocol/v2.md", experiment_root / "protocol" / "v2.md"),
        ("protocol/exploration.json", experiment_root / "protocol" / "exploration.json"),
        ("reference/fig1-digitized.csv", experiment_root / "reference" / "fig1-digitized.csv"),
        ("reference/README.md", experiment_root / "reference" / "README.md"),
        ("reference/la-1940-fig1.png", experiment_root / "reference" / "la-1940-fig1.png"),
        ("environment/uv.lock", repo_root / "uv.lock"),
    ]
    for name in ("index.html", "export.json"):
        candidate = site_dir / "evidence" / name
        if candidate.is_file():
            files.append((f"study-report/evidence/{name}", candidate))
    records = sorted(records_dir.glob("*.json")) if records_dir.is_dir() else []
    for path in records:
        files.append((f"research/records/{path.name}", path))
    missing = [name for name, path in files if not path.is_file()]
    if missing:
        raise ExportError("allowlisted member is missing: " + ", ".join(missing))

    lock_digest = sha256_bytes((repo_root / "uv.lock").read_bytes())
    generated: list[tuple[str, bytes]] = [
        (
            "reproduction/commands.txt",
            _commands(experiment_root.name, run_dir.name).encode("utf-8"),
        ),
        (
            "environment/README.md",
            _environment_readme(record, data_manifest, lock_digest).encode("utf-8"),
        ),
    ]
    metadata = {
        "experiment": experiment_root.name,
        "protocol_version": protocol_version,
        "run_id": run_dir.name,
        "run_kind": record.get("kind"),
        "run_status": record.get("status"),
        "scientific_assessment": record.get("scientific_assessment"),
        "code_revision": record.get("git_revision"),
        "uv_lock_sha256": lock_digest,
        "records": len(records),
        "excluded": [
            "_data payloads and the LA-1940 PDF (identified by digest and fetch command only)",
            "log.txt and every other run file outside the allowlist",
            "the nebula corpus, other experiments, caches and environment directories",
        ],
    }
    return files, generated, metadata


def _validate_member_name(name: str) -> None:
    if name.startswith("/") or ".." in Path(name).parts or not Path(name).parts:
        raise ExportError(f"refusing archive member name {name!r}")
    if name.split("/")[0] == "_data":
        raise ExportError(f"refusing _data payload {name!r}")


def build(
    *,
    run_dir: Path,
    experiment_root: Path,
    repo_root: Path,
    site_dir: Path,
    records_dir: Path,
    export_dir: Path,
) -> tuple[Path, dict[str, Any]]:
    """Write the allowlisted tar.gz and return its path with the manifest it embeds."""
    files, generated, metadata = plan(
        run_dir=run_dir,
        experiment_root=experiment_root,
        repo_root=repo_root,
        site_dir=site_dir,
        records_dir=records_dir,
    )
    members: list[tuple[str, bytes]] = []
    for name, path in files:
        _validate_member_name(name)
        members.append((name, path.read_bytes()))
    for name, payload in generated:
        _validate_member_name(name)
        members.append((name, payload))
    names = [name for name, _ in members]
    if len(set(names)) != len(names):
        raise ExportError("duplicate archive member")

    manifest = {
        "schema": "fput-evidence-package/1",
        "created": datetime.now(UTC).isoformat(),
        **metadata,
        "absolute_path_policy": (
            "No member may contain a home-directory absolute path; /tmp appears only as the "
            "throwaway environment location REPRODUCE.md asks the reader to create."
        ),
        "members": [
            {"name": name, "bytes": len(payload), "sha256": sha256_bytes(payload)}
            for name, payload in members
        ],
    }
    manifest_payload = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")

    export_dir.mkdir(parents=True, exist_ok=True)
    archive = export_dir / archive_name(metadata["protocol_version"], metadata["run_id"])
    temporary = archive.with_suffix(".tar.gz.partial")
    with tarfile.open(temporary, "w:gz") as handle:
        for name, payload in [*members, (MANIFEST_NAME, manifest_payload)]:
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            info.mtime = int(datetime.now(UTC).timestamp())
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            handle.addfile(info, io.BytesIO(payload))
    temporary.replace(archive)
    return archive, manifest


def _scan_absolute_paths(root: Path) -> list[str]:
    findings: list[str] = []
    pattern = re.compile("|".join(ABSOLUTE_PATH_PATTERNS))
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        data = path.read_bytes()
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = data.decode("utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            match = pattern.search(line)
            if match:
                findings.append(
                    f"{path.relative_to(root).as_posix()}:{number} contains {match.group(0)!r}"
                )
    return findings


def check(archive: Path) -> dict[str, Any]:
    """Extract, verify every recorded digest, and refuse absolute paths. Raises on failure."""
    if not archive.is_file():
        raise ExportError(f"no archive at {archive.name}")
    temporary = Path(tempfile.mkdtemp(prefix="fput-export-check-"))
    try:
        with tarfile.open(archive, "r:gz") as handle:
            entries = handle.getmembers()
            for info in entries:
                if not info.isfile():
                    raise ExportError(f"archive member {info.name!r} is not a regular file")
                _validate_member_name(info.name)
            handle.extractall(temporary, filter="data")
        manifest_path = temporary / MANIFEST_NAME
        if not manifest_path.is_file():
            raise ExportError("archive has no MANIFEST.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        listed = {entry["name"]: entry for entry in manifest["members"]}
        present = {
            path.relative_to(temporary).as_posix()
            for path in temporary.rglob("*")
            if path.is_file()
        } - {MANIFEST_NAME}
        unlisted = sorted(present - set(listed))
        if unlisted:
            raise ExportError("archive contains members outside the manifest: " + ", ".join(unlisted))
        absent = sorted(set(listed) - present)
        if absent:
            raise ExportError("manifest lists members the archive does not contain: " + ", ".join(absent))
        mismatched = []
        for name, entry in sorted(listed.items()):
            data = (temporary / name).read_bytes()
            if sha256_bytes(data) != entry["sha256"] or len(data) != entry["bytes"]:
                mismatched.append(name)
        if mismatched:
            raise ExportError("digest mismatch for: " + ", ".join(mismatched))
        findings = _scan_absolute_paths(temporary)
        if findings:
            raise ExportError("absolute paths found in the extracted tree: " + "; ".join(findings))
        return {
            "archive": archive.name,
            "members_verified": len(listed),
            "bytes": sum(entry["bytes"] for entry in listed.values()),
            "protocol_version": manifest["protocol_version"],
            "run_id": manifest["run_id"],
            "records": manifest["records"],
            "absolute_paths": 0,
        }
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
