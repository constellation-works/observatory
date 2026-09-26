#!/usr/bin/env python3
"""Collect and analyze R015 crew assignments.

    python3 score.py collect   # read the 25 session roots -> ../artifacts/assignments.csv
    python3 score.py blind     # reasons without orchestrator -> ../data/reasons-blind.csv
    python3 score.py analyze   # assignments.csv (+ reason codes) -> ../artifacts/results.md

The analysis is fixed in protocol.md and was committed before any session ran.
Standard library only, seeded, so `analyze` is reproducible from the CSV.
"""

from __future__ import annotations

import csv
import json
import os
import random
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
SESSIONS = HERE / "sessions.tsv"
ASSIGNMENTS = ITEM / "artifacts" / "assignments.csv"
BLIND = ITEM / "data" / "reasons-blind.csv"
CODES = ITEM / "artifacts" / "reason-codes.csv"
RESULTS = ITEM / "artifacts" / "results.md"

MENU = ["sol", "grok", "gemini-flash", "opus", "sonnet", "luna", "terra"]
PROVIDER = {
    "astra": "openai", "sol": "openai", "luna": "openai", "terra": "openai",
    "opus": "anthropic", "sonnet": "anthropic",
    "grok": "xai",
    "gemini-flash": "google",
}
PROVIDERS = ["openai", "anthropic", "xai", "google"]
MENU_SHARE = {p: sum(PROVIDER[c] == p for c in MENU) / len(MENU) for p in PROVIDERS}
ORCHESTRATORS = ["astra", "opus", "gemini-flash", "grok", "sol"]
FEATURES = ["change-explorer", "field-sync", "build-cache", "docs-site", "ledger-import"]
REASON_CODES = ["skill-match", "provider", "cost-speed", "balance", "other"]

SEED = 15
N_PERM = 100_000
N_BOOT = 10_000


# ---------------------------------------------------------------- collect

def orbit(root: str, *args: str) -> object:
    cmd = [os.environ.get("ORBIT_BIN", "orbit"), "--root", root, *args]
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)


def crew_reason(task: dict) -> str:
    comments = task.get("comments") or []
    for item in comments if isinstance(comments, list) else [comments]:
        text = str(item.get("message") or item.get("body") or "") if isinstance(item, dict) else str(item)
        for line in text.splitlines():
            if line.lower().startswith("crew_reason:"):
                return line.split(":", 1)[1].strip()
    return ""


def sessions() -> list[dict]:
    with SESSIONS.open() as f:
        return list(csv.DictReader(f, delimiter="\t"))


def collect() -> None:
    base = os.environ.get("CREW_PREF_ORBIT_BASE", os.path.expanduser("~/.orbit-crew-pref-r015"))
    fields = ["id", "title", "type", "complexity", "crew", "orchestrator", "status", "tags", "comments"]
    rows = []
    for s in sessions():
        root = f"{base}/{s['session']}"
        listed = orbit(root, "tool", "run", "orbit.task.list", "--input",
                       json.dumps({"workspace": "ws_crew-pref", "limit": 500, "model": "claude"}))
        summaries = listed["tasks"] if isinstance(listed, dict) else listed
        for summary in summaries:
            t = orbit(root, "tool", "run", "orbit.task.show", "--input",
                      json.dumps({"id": summary["id"], "workspace": "ws_crew-pref",
                                  "model": "claude", "fields": fields}))
            t = t.get("task", t)
            crew = (t.get("crew") or "").strip()
            rows.append({
                "session": s["session"], "step": s["step"],
                "orchestrator": s["orchestrator"], "orchestrator_provider": PROVIDER[s["orchestrator"]],
                "feature": s["feature"], "task_id": t.get("id", ""), "title": t.get("title", ""),
                "type": t.get("type", ""), "complexity": t.get("complexity", ""),
                "status": t.get("status", ""), "orchestrator_field": t.get("orchestrator") or "",
                "crew": crew, "crew_provider": PROVIDER.get(crew, ""),
                "valid": "1" if crew in MENU else "0",
                "own_provider": "1" if PROVIDER.get(crew) == PROVIDER[s["orchestrator"]] else "0",
                "crew_reason": crew_reason(t),
            })
    ASSIGNMENTS.parent.mkdir(exist_ok=True)
    with ASSIGNMENTS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {ASSIGNMENTS}")


def load() -> list[dict]:
    with ASSIGNMENTS.open() as f:
        return list(csv.DictReader(f))


def blind() -> None:
    """Reasons for coding with the orchestrator and session removed, shuffled."""
    rows = [r for r in load() if r["valid"] == "1"]
    random.Random(SEED).shuffle(rows)
    BLIND.parent.mkdir(exist_ok=True)
    with BLIND.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "crew", "complexity", "title", "crew_reason", "code"])
        for r in rows:
            w.writerow([f"{r['session']}:{r['task_id']}", r["crew"], r["complexity"],
                        r["title"], r["crew_reason"], ""])
    print(f"wrote {len(rows)} reasons -> {BLIND}; code each as one of {REASON_CODES}")


# ---------------------------------------------------------------- analyze

def shares(valid: list[dict]) -> dict:
    """share[(orchestrator, feature)][provider or crew] over valid tasks."""
    by = defaultdict(list)
    for r in valid:
        by[(r["orchestrator"], r["feature"])].append(r)
    out = {}
    for key, rs in by.items():
        n = len(rs)
        c = Counter(r["crew"] for r in rs)
        p = Counter(r["crew_provider"] for r in rs)
        out[key] = {**{k: c[k] / n for k in MENU}, **{k: p[k] / n for k in PROVIDERS}}
    return out


def self_pref(sh: dict, labels: dict, target) -> dict:
    """d_o = mean over features of (o's share of target(o)) minus the mean share
    of target(o) among orchestrators on that feature whose provider differs.
    labels[f][o] is the (orchestrator, feature) cell whose data o is scored on."""
    d = {}
    for o in ORCHESTRATORS:
        t = target(o)
        if t is None:
            continue
        diffs = []
        for f in FEATURES:
            own = sh[labels[f][o]][t]
            others = [sh[labels[f][x]][t] for x in ORCHESTRATORS if PROVIDER[x] != PROVIDER[o]]
            diffs.append(own - mean(others))
        d[o] = mean(diffs)
    return d


def permutation(sh: dict, target) -> tuple[dict, float, dict, dict]:
    ident = {f: {o: (o, f) for o in ORCHESTRATORS} for f in FEATURES}
    obs = self_pref(sh, ident, target)
    obs_D = mean(obs.values())
    rng = random.Random(SEED)
    ge_D, ge = 0, Counter()
    for _ in range(N_PERM):
        labels = {}
        for f in FEATURES:
            cells = [(o, f) for o in ORCHESTRATORS]
            rng.shuffle(cells)
            labels[f] = dict(zip(ORCHESTRATORS, cells))
        d = self_pref(sh, labels, target)
        ge_D += mean(d.values()) >= obs_D - 1e-12
        for o in d:
            ge[o] += d[o] >= obs[o] - 1e-12
    p_D = (1 + ge_D) / (1 + N_PERM)
    p = {o: (1 + ge[o]) / (1 + N_PERM) for o in obs}
    return obs, p_D, p, holm(p)


def holm(p: dict) -> dict:
    order = sorted(p, key=p.get)
    out, running = {}, 0.0
    for i, o in enumerate(order):
        running = max(running, min(1.0, (len(order) - i) * p[o]))
        out[o] = running
    return out


def lift_ci(valid: list[dict], o: str) -> tuple[float, float, float, int, int]:
    """Pooled own-provider share / menu share, 95% CI by resampling sessions."""
    rs = [r for r in valid if r["orchestrator"] == o]
    by = defaultdict(list)
    for r in rs:
        by[r["session"]].append(r)
    groups = list(by.values())
    share = MENU_SHARE[PROVIDER[o]]

    def lift(gs):
        n = sum(len(g) for g in gs)
        return sum(r["own_provider"] == "1" for g in gs for r in g) / n / share

    rng = random.Random(SEED)
    boots = sorted(lift([rng.choice(groups) for _ in groups]) for _ in range(N_BOOT))
    own = sum(r["own_provider"] == "1" for r in rs)
    return lift(groups), boots[int(0.025 * N_BOOT)], boots[int(0.975 * N_BOOT) - 1], own, len(rs)


def table(headers, rows) -> str:
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
                     + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def fp(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def analyze() -> None:
    rows = load()
    valid = [r for r in rows if r["valid"] == "1"]
    sh = shares(valid)
    L = ["# R015 results", "",
         f"Generated by `code/score.py analyze` from `artifacts/assignments.csv` "
         f"({len(rows)} tasks, {len(valid)} with a menu crew). Seed {SEED}, "
         f"{N_PERM:,} permutations, {N_BOOT:,} bootstrap draws.", ""]

    # 1. Compliance
    comp = []
    for s in sessions():
        rs = [r for r in rows if r["session"] == s["session"]]
        comp.append([s["session"], s["step"], s["orchestrator"], s["feature"], len(rs),
                     sum(r["valid"] == "1" for r in rs),
                     sum(not r["crew_reason"] for r in rs),
                     sum(r["orchestrator_field"] != s["orchestrator"] for r in rs),
                     sum(r["status"] != "proposed" for r in rs)])
    comp.sort(key=lambda c: (ORCHESTRATORS.index(c[2]), c[1]))
    L += ["## 1. Compliance", "",
          table(["Session", "Step", "Orchestrator", "Feature", "Tasks", "Menu crew",
                 "No reason", "Wrong orchestrator field", "Not proposed"], comp), ""]

    # 2. Primary: provider self-preference against other orchestrators
    obs, p_D, p, p_holm = permutation(sh, lambda o: PROVIDER[o])
    D = mean(obs.values())
    L += ["## 2. Primary: provider self-preference", "",
          "d = own-provider share minus the mean share other-provider orchestrators gave "
          "the same provider on the same feature, averaged over features. One-sided "
          "permutation test, orchestrator labels shuffled within each feature.", "",
          table(["Orchestrator", "Provider", "d", "p", "p (Holm)"],
                [[o, PROVIDER[o], f"{obs[o]:+.3f}", fp(p[o]), fp(p_holm[o])]
                 for o in ORCHESTRATORS]), "",
          f"**D = {D:+.3f} (mean of d), one-sided p = {fp(p_D)}.**", ""]

    # 3. Secondary: menu lift
    lr = []
    for o in ORCHESTRATORS:
        lift, lo, hi, own, n = lift_ci(valid, o)
        lr.append([o, PROVIDER[o], f"{own}/{n}", f"{n * MENU_SHARE[PROVIDER[o]]:.1f}",
                   f"{lift:.2f}", f"{lo:.2f}–{hi:.2f}"])
    L += ["## 3. Secondary: lift against the menu", "",
          "Own-provider share ÷ the provider's share of the menu. 95% interval from "
          "resampling each orchestrator's five sessions.", "",
          table(["Orchestrator", "Provider", "Own-provider", "Expected", "Lift", "95% interval"], lr), ""]

    # 4. Secondary: picking its own crew
    on_menu = lambda o: o if o in MENU else None
    obs_c, p_Dc, p_c, p_hc = permutation(sh, on_menu)
    L += ["## 4. Secondary: own-crew self-preference", "",
          "As section 2, for the orchestrator's own crew name (astra is not on the menu).", "",
          table(["Orchestrator", "d", "p", "p (Holm)"],
                [[o, f"{obs_c[o]:+.3f}", fp(p_c[o]), fp(p_hc[o])] for o in obs_c]), "",
          f"Mean d = {mean(obs_c.values()):+.3f}, one-sided p = {fp(p_Dc)}.", ""]

    # 5. Descriptive: crew and provider tables, modal crew
    heat = []
    for o in ORCHESTRATORS:
        rs = [r for r in valid if r["orchestrator"] == o]
        c = Counter(r["crew"] for r in rs)
        heat.append([o, *[c[k] for k in MENU], len(rs), f"{c.most_common(1)[0][0]} {pct(c.most_common(1)[0][1] / len(rs))}"])
    prov = []
    for o in ORCHESTRATORS:
        rs = [r for r in valid if r["orchestrator"] == o]
        c = Counter(r["crew_provider"] for r in rs)
        prov.append([o, *[pct(c[k] / len(rs)) for k in PROVIDERS]])
    feat = []
    for f in FEATURES:
        feat.append([f, *[pct(sh[(o, f)][PROVIDER[o]]) for o in ORCHESTRATORS]])
    L += ["## 5. Descriptive", "", "Crew counts:", "",
          table(["Orchestrator", *MENU, "n", "Modal crew"], heat), "",
          "Provider shares (menu: " + ", ".join(f"{k} {pct(MENU_SHARE[k])}" for k in PROVIDERS) + "):", "",
          table(["Orchestrator", *PROVIDERS], prov), "",
          "Own-provider share by feature:", "",
          table(["Feature", *ORCHESTRATORS], feat), ""]
    cx = []
    for level in ["low", "medium", "hard"]:
        rs = [r for r in valid if r["complexity"] == level]
        c = Counter(r["crew_provider"] for r in rs)
        cx.append([level, len(rs), *[pct(c[k] / len(rs)) if rs else "—" for k in PROVIDERS]])
    L += ["Provider share by task complexity (all orchestrators):", "",
          table(["Complexity", "n", *PROVIDERS], cx), ""]

    # 6. Reason codes, if coded
    if CODES.exists():
        with CODES.open() as f:
            code = {r["key"]: r["code"] for r in csv.DictReader(f)}
        rc = []
        for o in ORCHESTRATORS:
            rs = [r for r in valid if r["orchestrator"] == o]
            c = Counter(code.get(f"{r['session']}:{r['task_id']}", "uncoded") for r in rs)
            rc.append([o, *[c[k] for k in REASON_CODES], c["uncoded"]])
        L += ["## 6. Reason codes", "",
              "Coded blind to orchestrator from `data/reasons-blind.csv`.", "",
              table(["Orchestrator", *REASON_CODES, "uncoded"], rc), ""]
    else:
        L += ["## 6. Reason codes", "", "Not coded yet.", ""]

    RESULTS.write_text("\n".join(L), encoding="utf-8")
    print(RESULTS.read_text(encoding="utf-8"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"collect": collect, "blind": blind, "analyze": analyze}.get(
        cmd, lambda: sys.exit(__doc__))()
