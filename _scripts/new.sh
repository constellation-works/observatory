#!/usr/bin/env bash
#
# new.sh — allocate the next id of a record kind and scaffold a valid record.
#
# Usage:
#   _scripts/new.sh --kind Q|H|T|R --title "…"        (or: make new KIND=R TITLE="…")
#
# The id is the highest existing id of that kind plus one; the slug is the
# kebab-case of the title at creation and is frozen from then on. Questions,
# hypotheses and theories are single files; a research item is the one kind that
# gets a directory, with its README.md, data/manifest.json, code/ and artifacts/.
set -euo pipefail

KIND=""
TITLE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --kind)  KIND="${2:-}"; shift 2 ;;
    --title) TITLE="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "new.sh: unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -n "$KIND" ]  || { echo 'new.sh: --kind is required (Q, H, T or R)' >&2; exit 2; }
[ -n "$TITLE" ] || { echo 'new.sh: --title is required' >&2; exit 2; }

cd "$(dirname "$0")/.."
exec python3 - "$KIND" "$TITLE" <<'PY'
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
SCHEMA = json.loads((ROOT / "_scripts" / "schema.json").read_text(encoding="utf-8"))
META = SCHEMA["x-observatory"]

kind = sys.argv[1].strip().upper()
title = " ".join(sys.argv[2].split())
if kind not in META["kinds"]:
    sys.exit(f"new.sh: kind must be one of {', '.join(META['kinds'])}, not {sys.argv[1]!r}")

spec = META["kinds"][kind]
directory = ROOT / spec["directory"]
slug = re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", title.lower())).strip("-")
if not re.match(META["slug_pattern"], slug or ""):
    sys.exit(f"new.sh: {title!r} does not reduce to a kebab-case slug")

pattern = re.compile(rf"^{kind}(\d{{3}})-")
existing = [int(m.group(1)) for m in (pattern.match(p.name) for p in directory.iterdir()) if m]
number = max(existing, default=0) + 1
if number > 999:
    sys.exit(f"new.sh: {kind} has reached 999 records; widen the id prefix in one migration")
record_id = f"{kind}{number:03d}"
today = dt.date.today().isoformat()

common = [
    f"id: {record_id}",
    f"title: {title}",
    "status: {status}",
    "tags: []",
    "derived_from: []",
    f"created: {today}",
    f"updated: {today}",
]
extra = {
    "Q": (["answered_by: []"], "open"),
    "H": (["revision: 1", "assessments: []"], "open"),
    "T": (["claims: []", "supersedes: []"], "active"),
    "R": (["tests: []"], "planned"),
}[kind]
front = "---\n" + "\n".join(common + extra[0]).format(status=extra[1]) + "\n---\n"

if spec["layout"] == "file":
    path = directory / f"{record_id}-{slug}.md"
    if path.exists():
        sys.exit(f"new.sh: {path.relative_to(ROOT)} already exists")
    body = {
        "Q": "\n## The question\n\nWhat would settle it, and why it is worth asking.\n",
        "H": "\n## The claim\n\nState it so that a run can come out against it.\n\n"
             "## What would refute it\n\nThe observation that would move this to `refuted`.\n",
        "T": "\n## What it says\n\nThe account that survived, and the hypotheses it rests on.\n\n"
             "## Where it stops\n\nWhat it does not explain.\n",
    }[kind]
    path.write_text(f"{front}\n# {record_id} — {title}\n{body}")
    created = [path]
else:
    path = directory / f"{record_id}-{slug}"
    if path.exists():
        sys.exit(f"new.sh: {path.relative_to(ROOT)} already exists")
    (path / "code").mkdir(parents=True)
    (path / "artifacts").mkdir()
    (path / "data").mkdir()
    readme = path / "README.md"
    sections = "\n\n".join(
        f"## {name}\n\n<!-- {hint} -->"
        for name, hint in zip(
            META["readme_sections"],
            [
                "The one question this run settles, and the hypothesis ids it tests.",
                "What is run, on what inputs, with which controls.",
                "The numbers. Execution success is not support.",
                "What is shaky, and what this cannot say.",
                "The next run, or why there is none.",
            ],
            strict=True,
        )
    )
    readme.write_text(f"{front}\n# {record_id} — {title}\n\n{sections}\n")
    manifest = path / "data" / "manifest.json"
    manifest.write_text(json.dumps({"inputs": []}, indent=2) + "\n")
    created = [readme, manifest]

for item in created:
    print(item.relative_to(ROOT))
PY
