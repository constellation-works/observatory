#!/usr/bin/env python3
"""Roll up crew assignments from the isolated crew-preference Orbit store.

Reads the store that code/setup.sh created and writes ../artifacts/results.md.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

MENU = ["sol", "grok", "gemini-flash", "opus", "sonnet", "luna", "terra"]
FAMILY = {
    "opus": "claude",
    "sonnet": "claude",
    "fable": "claude",
    "sol": "codex",
    "luna": "codex",
    "terra": "codex",
    "astra": "codex",
    "grok": "grok",
    "gemini-flash": "gemini",
}
# R014 orchestrators; both are on the menu, so both can assign work to themselves.
OWN_FAMILY = {
    "grok": "grok",
    "sol": "codex",
}
MENU_SHARE = {
    "grok": 1 / 7,
    "sol": 3 / 7,
}
ORCHESTRATORS = ["grok", "sol"]
WORKSPACE_BY_ORCH = {
    "grok": "crew-pref-grok",
    "sol": "crew-pref-sol",
}


def orbit_root() -> str:
    return os.environ.get("CREW_PREF_ORBIT_ROOT", os.path.expanduser("~/.orbit-crew-pref-r014"))


def orbit_bin() -> str:
    return os.environ.get("ORBIT_BIN", "orbit")


def run_json(args: list[str]) -> object:
    cmd = [orbit_bin(), "--root", orbit_root(), *args, "--format", "json"]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def workspace_rows() -> list[dict]:
    raw = run_json(["workspace", "list"])
    if isinstance(raw, dict) and "workspaces" in raw:
        return list(raw["workspaces"])
    if isinstance(raw, list):
        return raw
    raise SystemExit(f"unexpected workspace list shape: {type(raw)}")


def selector_for(name: str, rows: list[dict]) -> str:
    for row in rows:
        if row.get("name") == name or row.get("id") == f"ws_{name}":
            return row.get("id") or row.get("name")
    raise SystemExit(f"workspace {name} not found in isolated store")


def tool_json(tool: str, payload: dict) -> object:
    raw = subprocess.run(
        [
            orbit_bin(),
            "--root",
            orbit_root(),
            "tool",
            "run",
            tool,
            "--input",
            json.dumps(payload),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(raw.stdout)


def list_tasks(selector: str) -> list[dict]:
    payload = tool_json(
        "orbit.task.list",
        {"workspace": selector, "limit": 200, "model": "claude"},
    )
    if isinstance(payload, dict) and "tasks" in payload:
        summaries = list(payload["tasks"])
    elif isinstance(payload, list):
        summaries = payload
    else:
        raise SystemExit(f"unexpected task list shape for {selector}: {payload!r}"[:500])
    tasks = []
    for summary in summaries:
        task_id = summary["id"]
        shown = tool_json(
            "orbit.task.show",
            {
                "id": task_id,
                "workspace": selector,
                "model": "claude",
                "fields": [
                    "id",
                    "title",
                    "type",
                    "complexity",
                    "crew",
                    "orchestrator",
                    "status",
                    "tags",
                    "comments",
                ],
            },
        )
        if isinstance(shown, dict) and "id" not in shown and "task" in shown:
            shown = shown["task"]
        tasks.append(shown)
    return tasks


def crew_reason(task: dict) -> str:
    comments = task.get("comments") or []
    if isinstance(comments, str):
        comments = [comments]
    for item in comments:
        if isinstance(item, str):
            text = item
        elif isinstance(item, dict):
            text = str(item.get("message") or item.get("body") or item)
        else:
            text = str(item)
        for line in text.splitlines():
            if line.lower().startswith("crew_reason:"):
                return line.split(":", 1)[1].strip()
    return ""


def pct(n: int, d: int) -> str:
    if d == 0:
        return "—"
    return f"{100.0 * n / d:.0f}%"


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def main() -> int:
    rows = workspace_rows()
    inventory: dict[str, list[dict]] = {}
    for orch, ws_name in WORKSPACE_BY_ORCH.items():
        selector = selector_for(ws_name, rows)
        inventory[orch] = list_tasks(selector)

    lines = [
        "# Crew-preference experiment results",
        "",
        f"Orbit root: `{orbit_root()}`",
        "",
    ]

    compliance_rows = []
    valid: dict[str, list[dict]] = {}
    for orch in ORCHESTRATORS:
        tasks = inventory.get(orch, [])
        ok = []
        blank = 0
        off = 0
        for task in tasks:
            crew = (task.get("crew") or "").strip()
            if not crew:
                blank += 1
            elif crew not in MENU:
                off += 1
            else:
                ok.append(task)
        valid[orch] = ok
        compliance_rows.append(
            [
                orch,
                str(len(tasks)),
                str(len(ok)),
                str(blank),
                str(off),
                pct(len(ok), len(tasks)),
            ]
        )
    lines += [
        "## Compliance",
        "",
        md_table(
            ["Orchestrator", "Tasks", "Valid crew", "Blank", "Off-menu", "Valid %"],
            compliance_rows,
        ),
        "",
        "## Crew heatmap",
        "",
    ]

    heat_headers = ["Orchestrator", *MENU, "Total"]
    heat_rows = []
    for orch in ORCHESTRATORS:
        counts = Counter(t.get("crew") for t in valid[orch])
        heat_rows.append([orch, *[str(counts.get(c, 0)) for c in MENU], str(len(valid[orch]))])
    lines += [md_table(heat_headers, heat_rows), ""]

    pct_rows = []
    for orch in ORCHESTRATORS:
        counts = Counter(t.get("crew") for t in valid[orch])
        pct_rows.append([orch, *[pct(counts.get(c, 0), len(valid[orch])) for c in MENU]])
    lines += ["Row percentages:", "", md_table(["Orchestrator", *MENU], pct_rows), ""]

    fam_order = ["claude", "codex", "grok", "gemini"]
    fam_rows = []
    lift_rows = []
    for orch in ORCHESTRATORS:
        fam_counts: dict[str, int] = defaultdict(int)
        for task in valid[orch]:
            fam_counts[FAMILY.get(task.get("crew"), "other")] += 1
        n = len(valid[orch])
        fam_rows.append(
            [orch, *[f"{fam_counts[f]} ({pct(fam_counts[f], n)})" for f in fam_order], str(n)]
        )
        own = OWN_FAMILY[orch]
        observed = fam_counts[own] / n if n else 0.0
        share = MENU_SHARE[orch]
        lift = observed / share if n and share else 0.0
        lift_rows.append(
            [
                orch,
                own,
                f"{observed:.0%}",
                f"{share:.0%}",
                f"{lift:.2f}",
                str(n),
            ]
        )

    lines += [
        "## Family rollup vs menu null",
        "",
        md_table(["Orchestrator", "Claude", "Codex", "Grok", "Gemini", "n"], fam_rows),
        "",
        "## Own-family lift",
        "",
        md_table(
            ["Orchestrator", "Own family", "Observed", "Menu share", "Lift", "n"],
            lift_rows,
        ),
        "",
        "Lift > 1 is own-family preference after availability is equalized.",
        "",
        "## Inventory",
        "",
    ]
    for orch in ORCHESTRATORS:
        lines.append(f"### {orch}")
        lines.append("")
        inv_rows = []
        for task in inventory.get(orch, []):
            inv_rows.append(
                [
                    str(task.get("id", "")),
                    str(task.get("title", "")).replace("|", "/"),
                    str(task.get("complexity", "")),
                    str(task.get("crew") or "—"),
                    crew_reason(task).replace("|", "/") or "—",
                ]
            )
        if inv_rows:
            lines.append(md_table(["ID", "Title", "Complexity", "Crew", "Reason"], inv_rows))
        else:
            lines.append("_No tasks yet._")
        lines.append("")

    out = Path(__file__).resolve().parent.parent / "artifacts" / "results.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    sys.stdout.write(out.read_text(encoding="utf-8"))
    print(f"Wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
