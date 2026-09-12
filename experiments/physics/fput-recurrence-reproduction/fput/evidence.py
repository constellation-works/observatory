"""Static evidence browser over orbit-research records.

The pinned `orbit-research` 0.2.0 exposes `export` (a validated static JSON bundle)
but no `index`/`browse-export` command, so the browser below is rendered here. It reads
either a validated export bundle or, when the records cannot be committed yet and no
bundle exists, the canonical record files themselves — labelled as such, never presented
as a validated export. It is a disposable view under `_outputs/`: the canonical records
stay in the owner's append-only `research/.../records` directory and are never rewritten.
"""

from __future__ import annotations

import html
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

KIND_ORDER = ["program", "claim", "artifact", "protocol", "experiment", "assessment"]

STYLE = """
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; max-width: 100%; overflow-x: hidden; }
body { font: 15px/1.55 -apple-system, "Segoe UI", Roboto, Arial, sans-serif; color: #16202c; background: #fff; }
main { width: 100%; max-width: 1120px; margin: 0 auto; padding: 1.25rem; }
h1 { font-size: 1.5rem; margin: 0 0 .3rem; }
h2 { font-size: 1.1rem; margin: 1.8rem 0 .5rem; border-bottom: 2px solid #d5dde7; padding-bottom: .3rem; }
p, li { overflow-wrap: break-word; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .86em; overflow-wrap: anywhere; }
.subtitle { color: #56657a; margin: 0 0 1rem; }
.pairs { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: .6rem 1.2rem; margin: 0; }
.pair dt { font-size: .76rem; text-transform: uppercase; letter-spacing: .04em; color: #56657a; }
.pair dd { margin: .15rem 0 0; overflow-wrap: anywhere; }
.panel { background: #f6f8fb; border: 1px solid #d5dde7; border-radius: 10px; padding: .9rem 1rem; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; min-width: 520px; font-size: .9rem; }
th, td { text-align: left; padding: .4rem .5rem; border-bottom: 1px solid #d5dde7; vertical-align: top; }
thead th { font-size: .76rem; text-transform: uppercase; color: #56657a; letter-spacing: .04em; }
table code { word-break: normal; overflow-wrap: break-word; }
details { border: 1px solid #d5dde7; border-radius: 8px; padding: .55rem .8rem; margin: .5rem 0; background: #fbfcfe; }
details summary { cursor: pointer; font-weight: 600; overflow-wrap: anywhere; }
pre { overflow-x: auto; background: #f3f5f9; border-radius: 6px; padding: .6rem; font-size: .8rem; }
.note { color: #56657a; font-size: .87rem; }
.banner { border: 2px solid #8a4b00; background: #fffaf3; color: #6d3b00; border-radius: 10px; padding: .7rem .9rem; margin: 0 0 1rem; font-size: .9rem; }
.tag { display: inline-block; border: 1px solid #d5dde7; border-radius: 999px; padding: .05rem .55rem; font-size: .75rem; background: #f6f8fb; }
a { color: #14507d; }
@media (max-width: 480px) { main { padding: .9rem; } table { min-width: 420px; } }
"""


def _text(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _alias(record: dict[str, Any]) -> str:
    aliases = record.get("aliases") or []
    return aliases[0] if aliases else record["id"].rsplit(":", 1)[-1]


def _summary(record: dict[str, Any]) -> str:
    payload = record["payload"]
    kind = record["kind"]
    if kind == "program":
        return payload["question"]
    if kind == "claim":
        return payload["statement"]
    if kind == "artifact":
        return f"{payload['role']} · {payload['availability']} · {payload['locator']}"
    if kind == "protocol":
        return f"{payload['freeze']} · {payload['semantic']['question']}"
    if kind == "experiment":
        return (
            f"{payload['execution_status']} · controls {payload['controls']} · "
            + ", ".join(f"{k}={v}" for k, v in sorted(payload.get("control_results", {}).items()))
        )
    if kind == "assessment":
        return f"{payload['verdict']} ({payload['inference']}, evidence {payload['evidence_summary']})"
    return kind


def load_bundle(bundle_path: Path) -> dict[str, Any]:
    with bundle_path.open(encoding="utf-8") as handle:
        bundle = json.load(handle)
    if bundle.get("kind") != "export" or bundle.get("schema_version") != 2:
        raise ValueError(f"{bundle_path.name} is not an orbit-research v2 export bundle")
    return bundle


def load_records(records_dir: Path) -> dict[str, Any]:
    """Read the canonical append-only records directly; no manifests, no resolved pins."""
    paths = sorted(records_dir.glob("*.json")) if records_dir.is_dir() else []
    if not paths:
        raise ValueError(f"no canonical records under {records_dir.name}")
    records = []
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            records.append(json.load(handle))
    unresolved = [
        {"reference": reference, "reason": "authored in the working tree; not committed yet"}
        for record in records
        for reference in record.get("references", [])
        if reference.get("status") != "resolved"
    ]
    return {
        "schema_version": 2,
        "kind": "export",
        "records": records,
        "manifests": [],
        "unresolved": unresolved,
        "working_tree": True,
    }


def render(*, evidence_dir: Path, bundle_path: Path | None = None,
           records_dir: Path | None = None) -> Path:
    """Write the evidence browser into `evidence_dir` and return its index.html."""
    if (bundle_path is None) == (records_dir is None):
        raise ValueError("supply exactly one of a bundle path or a records directory")
    bundle = load_bundle(bundle_path) if bundle_path else load_records(records_dir)
    working_tree = bundle.pop("working_tree", False)

    evidence_dir.mkdir(parents=True, exist_ok=True)
    copied = evidence_dir / "export.json"
    copied.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    records: list[dict[str, Any]] = sorted(
        bundle["records"],
        key=lambda record: (
            KIND_ORDER.index(record["kind"]) if record["kind"] in KIND_ORDER else len(KIND_ORDER),
            record["authorship"]["sequence"],
        ),
    )
    def _links(record: dict[str, Any]) -> str:
        return ", ".join(
            "{} / {}".format(link["task"], link.get("run", "?")) for link in record["orbit_links"]
        )

    rows = "\n".join(
        "<tr>"
        f'<td><span class="tag">{_text(record["kind"])}</span></td>'
        f"<td><code>{_text(_alias(record))}</code></td>"
        f"<td>{_text(_summary(record))}</td>"
        f"<td><code>{_text(record['revision_id'][:19])}…</code></td>"
        f"<td>{_text(record['authorship']['registered_at'])}</td>"
        f"<td>{_text(record['activity'])} / {_text(record['scope'])}</td>"
        "</tr>"
        for record in records
    )
    details = "\n".join(
        "<details>"
        f"<summary>{_text(record['kind'])} · {_text(_alias(record))} · seq "
        f"{_text(record['authorship']['sequence'])}</summary>"
        f'<dl class="pairs">'
        f'<div class="pair"><dt>canonical id</dt><dd><code>{_text(record["id"])}</code></dd></div>'
        f'<div class="pair"><dt>revision</dt><dd><code>{_text(record["revision_id"])}</code></dd></div>'
        f'<div class="pair"><dt>source revision</dt><dd><code>{_text(record["provenance"]["git_revision"])}</code></dd></div>'
        f'<div class="pair"><dt>record path</dt><dd><code>{_text(record["provenance"]["path"])}</code></dd></div>'
        f'<div class="pair"><dt>orbit links</dt><dd>{_text(_links(record))}</dd></div>'
        f'<div class="pair"><dt>reason</dt><dd>{_text(record["authorship"]["reason"])}</dd></div>'
        "</dl>"
        f"<pre>{_text(json.dumps(record, indent=2, sort_keys=True))}</pre>"
        "</details>"
        for record in records
    )
    manifests = "\n".join(
        "<tr>"
        f"<td><code>{_text(entry['repositories'][0]['id'])}</code></td>"
        f"<td><code>{_text(entry['repositories'][0]['git_revision'])}</code></td>"
        f"<td>{_text(len(entry['references']))}</td>"
        f"<td>{_text(sum(1 for ref in entry['references'] if ref['status'] == 'resolved'))}</td>"
        "</tr>"
        for entry in bundle["manifests"]
    )
    manifest_section = (
        "<h2>Export manifests</h2><div class=\"scroll\"><table><thead><tr><th>repository</th>"
        "<th>pinned commit</th><th>references</th><th>resolved</th></tr></thead><tbody>"
        f"{manifests}</tbody></table></div>"
        if bundle["manifests"]
        else '<h2>Export manifests</h2><p class="note">None: an export manifest pins records at '
        "an exact commit, which requires the records to be committed.</p>"
    )
    unresolved = bundle.get("unresolved", [])
    counts = {kind: sum(1 for record in records if record["kind"] == kind) for kind in KIND_ORDER}
    generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%SZ")
    banner = (
        '<div class="banner"><strong>Working-tree records, not a validated export.</strong> '
        "These are the canonical record files as authored in the checkout. "
        "<code>orbit-research</code> resolves references and exports only from committed "
        "Git snapshots, so the protocol freeze, the run receipts and the assessment are "
        "appended once this task&rsquo;s delivery commit lands, with "
        "<code>tools/record_chain.py --stop-after export</code>. Nothing here is presented "
        "as a validated bundle or as a resolved evidence closure.</div>"
        if working_tree
        else '<p class="note">The bundle validates with <code>uv run orbit-research validate '
        "evidence/export.json</code>.</p>"
    )

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Scientific record evidence — FPUT recurrence reproduction</title>
<style>{STYLE}</style>
</head>
<body>
<main>
<h1>Scientific record evidence</h1>
<p class="subtitle">{"working-tree records" if working_tree else "orbit-research v2 export bundle"}
· {_text(len(records))} records · {_text(len(bundle["manifests"]))} manifest(s) ·
{_text(len(unresolved))} unresolved reference(s) · page generated {_text(generated)}</p>
{banner}
<div class="panel">
<dl class="pairs">
{"".join(f'<div class="pair"><dt>{_text(kind)}</dt><dd>{_text(count)}</dd></div>' for kind, count in counts.items())}
</dl>
</div>
<p class="note">This browser is a disposable static view: canonical records remain
append-only JSON in the owner checkout. The pinned orbit-research 0.2.0 has no
<code>index</code>/<code>browse-export</code> subcommand, so this page is rendered by
<code>run.py evidence</code>{" from the package's own validated export" if not working_tree else " directly from the canonical record files"}.</p>

<h2>Record chain</h2>
<div class="scroll">
<table>
<thead><tr><th>kind</th><th>id</th><th>summary</th><th>revision</th><th>registered</th><th>activity / scope</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</div>

<h2>Records in full</h2>
{details}

{manifest_section}
{'<h2>Unresolved references</h2><pre>' + _text(json.dumps(unresolved, indent=2, sort_keys=True)) + '</pre>' if unresolved else '<p class="note">Every reference resolved to an exact committed record.</p>'}

<p class="note"><a href="../index.html">← back to the study page</a> ·
<a href="export.json">raw export.json</a></p>
</main>
</body>
</html>
"""
    index = evidence_dir / "index.html"
    index.write_text(document, encoding="utf-8")
    return index
