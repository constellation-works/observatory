#!/usr/bin/env python3
"""The research-layout-v2 gate: one checker for the whole corpus.

Walks the four record kinds — `questions/Q###-slug.md`, `hypotheses/H###-slug.md`,
`theories/T###-slug.md` and `research/R###-slug/` — validates their frontmatter
against `_scripts/schema.json` (the same contract orbit-research validates
against), resolves every cross-reference, and refuses tracked bytes under any
ignored path. `notebooks/`, `docs/`, `_lib/` and `_archive/` carry no frontmatter
contract and are skipped.

Failures exit 1; warnings are reported and do not.

Usage: python3 _scripts/check.py [--root DIR] [--no-git]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - environment, not logic
    sys.exit(
        "check.py needs PyYAML: run it as `make check`, or `uv run python _scripts/check.py`"
    )

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.json"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
# Nebula lives upstream of this repository: its corpus is in the almanac and it
# cites Observatory records, never the reverse. Nothing operative here may depend
# on its tooling. Design records under docs/design/ and the frozen archive (which
# holds the pre-v2 corpus) describe history and are exempt.
NEBULA_TOOLING = re.compile(r"(?<![\w-])neb(?![\w-])|NEBULA_ROOT|knowledgebase/lineage")
NEBULA_TOOLING_SKIP = ("_archive/", "docs/design/", "notebooks/", "_scripts/check.py")


# --------------------------------------------------------------------------
# schema
# --------------------------------------------------------------------------
class Schema:
    """Just enough of JSON Schema to validate frontmatter without a dependency."""

    def __init__(self, document: dict[str, Any]) -> None:
        self.doc = document
        self.meta = document["x-observatory"]
        self.kinds = self.meta["kinds"]
        self.sections: list[str] = self.meta["readme_sections"]
        self.reference_fields: dict[str, list[str]] = self.meta["reference_fields"]
        self.verdict_status: dict[str, str] = self.meta["verdict_status"]
        self.stale_days: int = self.meta["stale_running_days"]
        self.id_re = re.compile(self.meta["id_pattern"])
        self.slug_re = re.compile(self.meta["slug_pattern"])

    def deref(self, node: dict[str, Any]) -> dict[str, Any]:
        seen = 0
        while "$ref" in node:
            target: Any = self.doc
            for part in node["$ref"].lstrip("#/").split("/"):
                target = target[part]
            node = target
            seen += 1
            if seen > 8:
                raise RuntimeError("schema $ref cycle")
        return node

    def definition(self, name: str) -> dict[str, Any]:
        return self.doc["$defs"][name]

    def statuses(self, kind: str) -> list[str]:
        return self.definition(self.kinds[kind]["def"])["properties"]["status"]["enum"]

    def validate(self, name: str, value: Any, where: str) -> list[str]:
        """Validate `value` against the named $def; return human-readable errors."""
        return self._object(self.definition(name), value, where)

    def _object(self, node: dict[str, Any], value: Any, where: str) -> list[str]:
        node = self.deref(node)
        errors: list[str] = []
        if not isinstance(value, dict):
            return [f"{where} must be a mapping"]
        properties = node.get("properties", {})
        for key in node.get("required", []):
            if key not in value:
                errors.append(f"{where} is missing required key `{key}`")
        if node.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{where} has key `{key}` outside the schema")
        for key, item in value.items():
            if key in properties:
                errors.extend(self._value(properties[key], item, f"{where} `{key}`"))
        return errors

    def _value(self, node: dict[str, Any], value: Any, where: str) -> list[str]:
        node = self.deref(node)
        types = node.get("type")
        types = [types] if isinstance(types, str) else (types or [])
        errors: list[str] = []
        if types and not self._type_ok(types, value):
            errors.append(f"{where} must be {' or '.join(types)}, got {type(value).__name__}")
            return errors
        if "enum" in node and value not in node["enum"]:
            errors.append(f"{where} is `{value}`, not one of {', '.join(map(str, node['enum']))}")
        if "pattern" in node and isinstance(value, str) and not re.search(node["pattern"], value):
            errors.append(f"{where} `{value}` does not match {node['pattern']}")
        if "minLength" in node and isinstance(value, str) and len(value) < node["minLength"]:
            errors.append(f"{where} must not be empty")
        if "minimum" in node and isinstance(value, int) and value < node["minimum"]:
            errors.append(f"{where} must be at least {node['minimum']}")
        if "items" in node and isinstance(value, list):
            for index, item in enumerate(value):
                errors.extend(self._value(node["items"], item, f"{where}[{index}]"))
        if isinstance(value, dict) and ("properties" in node or "required" in node):
            errors.extend(self._object(node, value, where))
        return errors

    @staticmethod
    def _type_ok(types: list[str], value: Any) -> bool:
        for name in types:
            if name == "string" and isinstance(value, str):
                return True
            if name == "integer" and isinstance(value, int) and not isinstance(value, bool):
                return True
            if name == "array" and isinstance(value, list):
                return True
            if name == "object" and isinstance(value, dict):
                return True
            if name == "null" and value is None:
                return True
        return False


# --------------------------------------------------------------------------
# records
# --------------------------------------------------------------------------
@dataclass
class Record:
    kind: str
    number: int
    slug: str
    path: Path            # the markdown file carrying the frontmatter
    where: str            # repository-relative label used in messages
    front: dict[str, Any]
    body: str
    directory: Path | None = None   # R items only


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def kebab(text: str) -> str:
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", text.lower())).strip("-")


def as_date(value: Any) -> dt.date | None:
    if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value)
        except ValueError:
            return None
    return None


def normalize_dates(front: dict[str, Any]) -> dict[str, Any]:
    """YAML parses bare dates into `datetime.date`; the schema speaks strings."""
    out = dict(front)
    for key in ("created", "updated"):
        if isinstance(out.get(key), dt.date):
            out[key] = out[key].isoformat()
    for entry in out.get("assessments") or []:
        if isinstance(entry, dict) and isinstance(entry.get("date"), dt.date):
            entry["date"] = entry["date"].isoformat()
    return out


def split_frontmatter(path: Path, where: str, report: Report) -> tuple[dict[str, Any], str] | None:
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        report.error(where, "has no `---` frontmatter block")
        return None
    try:
        front = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        report.error(where, f"frontmatter is not valid YAML: {exc}")
        return None
    if not isinstance(front, dict):
        report.error(where, "frontmatter must be a mapping")
        return None
    return normalize_dates(front), match.group(2)


def collect(root: Path, schema: Schema, report: Report) -> list[Record]:
    records: list[Record] = []
    for kind, spec in schema.kinds.items():
        directory = root / spec["directory"]
        if not directory.is_dir():
            report.error(spec["directory"], "record directory is missing")
            continue
        for entry in sorted(directory.iterdir()):
            if entry.name in ("README.md", ".gitkeep"):
                continue
            if spec["layout"] == "file":
                records.extend(_flat_record(kind, entry, schema, report) or [])
            else:
                records.extend(_dir_record(kind, entry, root, schema, report) or [])
    return records


def _flat_record(kind: str, entry: Path, schema: Schema, report: Report) -> list[Record]:
    where = f"{entry.parent.name}/{entry.name}"
    name_re = re.compile(rf"^{kind}(\d{{3}})-({schema.meta['slug_pattern'][1:-1]})\.md$")
    match = name_re.match(entry.name)
    if not entry.is_file() or not match:
        report.error(where, f"is not a `{kind}###-slug.md` record file")
        return []
    parts = split_frontmatter(entry, where, report)
    if parts is None:
        return []
    front, body = parts
    return [Record(kind, int(match.group(1)), match.group(2), entry, where, front, body)]


def _dir_record(kind: str, entry: Path, root: Path, schema: Schema, report: Report) -> list[Record]:
    where = f"{entry.parent.name}/{entry.name}"
    name_re = re.compile(rf"^{kind}(\d{{3}})-({schema.meta['slug_pattern'][1:-1]})$")
    match = name_re.match(entry.name)
    if not entry.is_dir() or not match:
        report.error(where, f"is not a `{kind}###-slug/` record directory")
        return []
    readme = entry / "README.md"
    if not readme.is_file():
        report.error(where, "has no README.md")
        return []
    parts = split_frontmatter(readme, f"{where}/README.md", report)
    if parts is None:
        return []
    front, body = parts
    return [Record(kind, int(match.group(1)), match.group(2), readme, where, front, body, entry)]


# --------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------
def check_identity(records: list[Record], schema: Schema, report: Report) -> None:
    for record in records:
        front = record.front
        expected = f"{record.kind}{record.number:03d}"
        if front.get("id") != expected:
            report.error(
                record.where,
                f"frontmatter id `{front.get('id')}` disagrees with the filename id `{expected}`",
            )
        declared = front.get("slug")
        if declared is not None:
            if declared != record.slug:
                report.error(
                    record.where,
                    f"frontmatter slug `{declared}` disagrees with the filename slug "
                    f"`{record.slug}`",
                )
        elif isinstance(front.get("title"), str) and kebab(front["title"]) != record.slug:
            report.error(
                record.where,
                f"filename slug `{record.slug}` is not the kebab-case of the title "
                f"(`{kebab(front['title'])}`); the slug is frozen, so record it as "
                f"`slug: {record.slug}`",
            )


def check_numbering(records: list[Record], schema: Schema, report: Report) -> None:
    for kind, spec in schema.kinds.items():
        numbers = sorted(r.number for r in records if r.kind == kind)
        seen: set[int] = set()
        for number in numbers:
            if number in seen:
                report.error(spec["directory"], f"duplicate id {kind}{number:03d}")
            seen.add(number)
        unique = sorted(seen)
        for position, number in enumerate(unique, start=1):
            if number != position:
                report.error(
                    spec["directory"],
                    f"non-monotonic ids: expected {kind}{position:03d} next, "
                    f"found {kind}{number:03d}",
                )
                break


def check_schema(records: list[Record], schema: Schema, report: Report) -> None:
    for record in records:
        name = schema.kinds[record.kind]["def"]
        for message in schema.validate(name, record.front, "frontmatter"):
            report.error(record.where, message)


def check_references(records: list[Record], schema: Schema, report: Report) -> None:
    known = {r.front.get("id"): r for r in records if isinstance(r.front.get("id"), str)}

    def resolve(where: str, field_name: str, value: Any, kinds: list[str]) -> None:
        for reference in value or []:
            if not isinstance(reference, str):
                continue
            target = known.get(reference)
            if target is None:
                report.error(where, f"`{field_name}` reference `{reference}` does not resolve")
            elif target.kind not in kinds:
                report.error(
                    where,
                    f"`{field_name}` reference `{reference}` is a {target.kind} record; "
                    f"expected {' or '.join(kinds)}",
                )

    for record in records:
        for field_name, kinds in schema.reference_fields.items():
            if field_name in record.front:
                resolve(record.where, field_name, record.front[field_name], kinds)
        for index, entry in enumerate(record.front.get("assessments") or []):
            if isinstance(entry, dict):
                resolve(
                    record.where,
                    f"assessments[{index}].research",
                    [entry.get("research")],
                    ["R"],
                )


def check_assessment_revisions(records: list[Record], report: Report) -> None:
    for record in records:
        if record.kind != "H":
            continue
        revision = record.front.get("revision")
        if not isinstance(revision, int):
            continue
        for index, entry in enumerate(record.front.get("assessments") or []):
            if isinstance(entry, dict) and isinstance(entry.get("revision"), int):
                if entry["revision"] > revision:
                    report.error(
                        record.where,
                        f"assessments[{index}] is against revision {entry['revision']}, "
                        f"beyond the hypothesis's current revision {revision}",
                    )


def check_research_items(records: list[Record], schema: Schema, report: Report) -> None:
    for record in records:
        if record.kind != "R" or record.directory is None:
            continue
        found = [name.strip() for name in SECTION_RE.findall(record.body)]
        wanted = schema.sections
        if [name for name in found if name in wanted] != wanted:
            report.error(
                f"{record.where}/README.md",
                f"sections must be exactly `## {'`, `## '.join(wanted)}` in that order; found "
                + (", ".join(found) or "none"),
            )
        manifest_path = record.directory / "data" / "manifest.json"
        if not manifest_path.is_file():
            report.error(record.where, "has no data/manifest.json")
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.error(f"{record.where}/data/manifest.json", f"is not valid JSON: {exc}")
            continue
        where = f"{record.where}/data/manifest.json"
        for message in schema.validate("data_manifest", manifest, "manifest"):
            report.error(where, message)
        for index, entry in enumerate(manifest.get("inputs") or []):
            if not isinstance(entry, dict):
                continue
            if "shared" in entry:
                target = ROOT / entry["shared"] / "manifest.json"
                if not target.is_file():
                    report.error(
                        where,
                        f"inputs[{index}] shared dataset `{entry['shared']}` "
                        "has no manifest.json",
                    )
                continue
            missing = [key for key in ("source", "sha256", "size", "fetch") if key not in entry]
            if missing:
                report.error(
                    where,
                    f"inputs[{index}] `{entry.get('name')}` is missing {', '.join(missing)} "
                    "(or a `shared` pointer to a _data/<name> manifest)",
                )


def check_warnings(records: list[Record], schema: Schema, report: Report, today: dt.date) -> None:
    by_id = {r.front.get("id"): r for r in records}
    for record in records:
        if record.kind == "H":
            _warn_hypothesis_status(record, schema, report)
        elif record.kind == "R":
            _warn_research(record, by_id, schema, report, today)


def _warn_hypothesis_status(record: Record, schema: Schema, report: Report) -> None:
    status = record.front.get("status")
    revision = record.front.get("revision")
    current = [
        entry
        for entry in record.front.get("assessments") or []
        if isinstance(entry, dict) and entry.get("revision") == revision
    ]
    if not current or status == "dropped":
        return
    # Append-only log: the latest entry is the last one written on the newest date.
    latest = max(
        enumerate(current),
        key=lambda pair: (as_date(pair[1].get("date")) or dt.date.min, pair[0]),
    )[1]
    implied = schema.verdict_status.get(latest.get("verdict"))
    if implied and implied != status:
        report.warn(
            record.where,
            f"status `{status}` disagrees with the latest assessment "
            f"({latest.get('date')}, {latest.get('research')}, verdict `{latest.get('verdict')}` "
            f"implies `{implied}`); a person owns the status, so this is a warning",
        )


def _warn_research(
    record: Record, by_id: dict[Any, Record], schema: Schema, report: Report, today: dt.date
) -> None:
    status = record.front.get("status")
    tested = [t for t in record.front.get("tests") or [] if t in by_id]
    if status == "done" and tested:
        assessed = any(
            isinstance(entry, dict) and entry.get("research") == record.front.get("id")
            for target in tested
            for entry in by_id[target].front.get("assessments") or []
        )
        if not assessed:
            report.warn(
                record.where,
                f"is `done` but no hypothesis it tests ({', '.join(tested)}) carries an assessment "
                "naming it; execution success is not support, and an inconclusive verdict "
                "is a result",
            )
    if status == "running":
        updated = as_date(record.front.get("updated"))
        if updated and (today - updated).days > schema.stale_days:
            report.warn(
                record.where,
                f"is `running` and has not been updated for {(today - updated).days} days",
            )


def git_paths(root: Path, *arguments: str) -> list[str] | None:
    try:
        completed = subprocess.run(
            ["git", "ls-files", "-z", *arguments],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return [name for name in completed.stdout.split("\0") if name]


def committable(root: Path, report: Report) -> list[str] | None:
    """Everything a commit from here would carry: tracked files that still exist,
    plus untracked files git does not ignore."""
    tracked = git_paths(root)
    untracked = git_paths(root, "--others", "--exclude-standard")
    if tracked is None or untracked is None:
        report.warn("git", "ls-files failed; the checks that need it did not run")
        return None
    return sorted({name for name in tracked if (root / name).exists()} | set(untracked))


def check_ignored_bytes(root: Path, report: Report, use_git: bool) -> None:
    """No committed bytes under any data/, output/ or _data/ path. The archive keeps
    whatever it was committed with and is out of scope."""
    if not use_git:
        return
    names = committable(root, report)
    if names is None:
        return
    for name in names:
        if name.startswith("_archive/"):
            continue
        parts = name.split("/")
        if not ({"data", "output"} & set(parts[:-1]) or parts[0] == "_data"):
            continue
        if parts[-1] in ("manifest.json", "README.md"):
            continue
        report.error(
            name, "is under an ignored path; only manifest.json and README.md may be committed"
        )


def check_nebula_tooling(root: Path, report: Report, use_git: bool) -> None:
    """Nebula is upstream: nothing operative here may depend on its tooling."""
    if not use_git:
        return
    names = committable(root, report)
    if names is None:
        return
    for name in names:
        if name.startswith(NEBULA_TOOLING_SKIP) or name.endswith(".ipynb"):
            continue
        path = root / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if NEBULA_TOOLING.search(line):
                report.error(
                    f"{name}:{number}", "depends on the Nebula tooling, which lives upstream"
                )


# --------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root to check")
    parser.add_argument("--no-git", action="store_true", help="skip the checks that need git")
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    arguments = parser.parse_args()
    root = arguments.root.resolve()
    use_git = not arguments.no_git

    schema = Schema(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    report = Report()
    records = collect(root, schema, report)

    check_identity(records, schema, report)
    check_numbering(records, schema, report)
    check_schema(records, schema, report)
    check_references(records, schema, report)
    check_assessment_revisions(records, report)
    check_research_items(records, schema, report)
    check_ignored_bytes(root, report, use_git)
    check_nebula_tooling(root, report, use_git)
    check_warnings(records, schema, report, arguments.today)

    for message in report.warnings:
        print(f"check: warning: {message}")
    for message in report.errors:
        print(f"check: error: {message}", file=sys.stderr)

    counts = {kind: sum(1 for r in records if r.kind == kind) for kind in schema.kinds}
    summary = " ".join(f"{kind}={counts[kind]}" for kind in schema.kinds)
    if report.errors:
        print(
            f"check: {len(report.errors)} error(s), "
            f"{len(report.warnings)} warning(s) over {summary}",
            file=sys.stderr,
        )
        return 1
    print(f"check: ok — {summary}, {len(report.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
