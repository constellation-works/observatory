#!/usr/bin/env python3
"""Collect and analyze R017 (crew labels hidden, providers shown).

    python3 score.py collect   # 30 session roots + mapping -> ../artifacts/assignments.csv, sessions.csv
    python3 score.py leaks     # session logs that touched the mapping or the observatory
    python3 score.py blind     # reasons without orchestrator -> ../data/reasons-blind.csv
    python3 score.py analyze   # assignments.csv (+ reason codes) -> ../artifacts/results.md

The analysis is fixed in protocol.md and was committed before any session ran.
R015's scorer supplies the statistics; R015's and R016's committed assignments
are the comparison. Standard library only, seeded.
"""

from __future__ import annotations

import csv
import importlib.util
import itertools
import json
import os
import random
import sys
from collections import Counter
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
ITEM = HERE.parent
RESEARCH = ITEM.parent
R015 = RESEARCH / "R015-crew-preference-across-five-orchestrators-and-five-features"
R016 = RESEARCH / "R016-crew-preference-of-opus-5-on-the-r015-features"
MAPPING = ITEM / "data" / "mapping.tsv"
ASSIGNMENTS = ITEM / "artifacts" / "assignments.csv"
SESSION_TIMES = ITEM / "artifacts" / "sessions.csv"
BLIND = ITEM / "data" / "reasons-blind.csv"
CODES = ITEM / "artifacts" / "reason-codes.csv"
RESULTS = ITEM / "artifacts" / "results.md"

SEED = 17
LABELS = [f"crew-{c}" for c in "abcdefg"]
ORCHESTRATORS = ["opus-5-5", "opus-5", "astra", "gemini-flash", "grok", "sol"]
NON_ANTHROPIC = ["astra", "gemini-flash", "grok", "sol"]
REASON_CODES = ["provider-skill", "provider-affinity", "cost-speed", "balance", "other"]
# Leak markers: the mapping file and the repository that holds it.
LEAK_MARKERS = ["mapping.tsv", "observatory"]

_spec = importlib.util.spec_from_file_location("r015", R015 / "code" / "score.py")
r015 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r015)
MENU, FEATURES, PROVIDERS, MENU_SHARE = r015.MENU, r015.FEATURES, r015.PROVIDERS, r015.MENU_SHARE
PROVIDER = {**r015.PROVIDER, "opus-5-5": "anthropic", "opus-5": "anthropic"}
r015.PROVIDER = PROVIDER  # self_pref and permutation read it
r015.SEED = SEED
N_PERM = r015.N_PERM
table, fp, pct = r015.table, r015.fp, r015.pct


def mapping() -> dict:
    with MAPPING.open() as f:
        return {(r["session"], r["label"]): r["crew"] for r in csv.DictReader(f, delimiter="\t")}


def collect() -> None:
    base = os.environ.get("CREW_PREF_ORBIT_BASE", os.path.expanduser("~/.orbit-crew-pref-r017"))
    m = mapping()
    fields = ["id", "title", "type", "complexity", "crew", "orchestrator", "status", "tags", "comments"]
    rows = []
    for s in sessions():
        root = f"{base}/{s['session']}"
        listed = r015.orbit(root, "tool", "run", "orbit.task.list", "--input",
                            json.dumps({"workspace": "ws_crew-pref", "limit": 500, "model": "claude"}))
        for summary in listed["tasks"] if isinstance(listed, dict) else listed:
            t = r015.orbit(root, "tool", "run", "orbit.task.show", "--input",
                           json.dumps({"id": summary["id"], "workspace": "ws_crew-pref",
                                       "model": "claude", "fields": fields}))
            t = t.get("task", t)
            label = (t.get("crew") or "").strip()
            crew = m.get((s["session"], label), "")
            rows.append({
                "session": s["session"], "step": s["step"],
                "orchestrator": s["orchestrator"], "orchestrator_provider": PROVIDER[s["orchestrator"]],
                "feature": s["feature"], "task_id": t.get("id", ""), "title": t.get("title", ""),
                "type": t.get("type", ""), "complexity": t.get("complexity", ""),
                "status": t.get("status", ""), "orchestrator_field": t.get("orchestrator") or "",
                "label": label, "crew": crew, "crew_provider": PROVIDER.get(crew, ""),
                "valid": "1" if label in LABELS else "0",
                "own_provider": "1" if PROVIDER.get(crew) == PROVIDER[s["orchestrator"]] else "0",
                "crew_reason": r015.crew_reason(t),
            })
    ASSIGNMENTS.parent.mkdir(exist_ok=True)
    with ASSIGNMENTS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {ASSIGNMENTS}")
    r015.SESSIONS, r015.ITEM, r015.SESSION_TIMES = HERE / "sessions.tsv", ITEM, SESSION_TIMES
    r015.MODEL_EFFORT = {**r015.MODEL_EFFORT,
                         "opus-5-5": r015.MODEL_EFFORT["opus"],
                         "opus-5": ("claude-opus-5", "high (Claude Code --effort)")}
    r015.timings()


def sessions() -> list[dict]:
    with (HERE / "sessions.tsv").open() as f:
        return list(csv.DictReader(f, delimiter="\t"))


def leaks() -> None:
    """Sessions whose log mentions the mapping file or the observatory (protocol: rerun)."""
    found = False
    for s in sessions():
        text = (ITEM / "output" / f"{s['session']}.jsonl").read_text(encoding="utf-8", errors="replace")
        hits = [k for k in LEAK_MARKERS if k in text]
        if hits:
            found = True
            print(f"{s['session']} {s['orchestrator']} {s['feature']}: {', '.join(hits)}")
    print("leaks found" if found else "no session log mentions the mapping or the observatory")


def load() -> list[dict]:
    with ASSIGNMENTS.open() as f:
        return list(csv.DictReader(f))


def blind() -> None:
    """Reasons for coding with orchestrator and session removed, shuffled."""
    rows = [r for r in load() if r["valid"] == "1"]
    random.Random(SEED).shuffle(rows)
    BLIND.parent.mkdir(exist_ok=True)
    with BLIND.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "crew_provider", "complexity", "title", "crew_reason", "code"])
        for r in rows:
            w.writerow([f"{r['session']}:{r['task_id']}", r["crew_provider"], r["complexity"],
                        r["title"], r["crew_reason"], ""])
    print(f"wrote {len(rows)} reasons -> {BLIND}; code each as one of {REASON_CODES}")


def feature_diffs(sh: dict, o: str, others: list[str]) -> dict:
    """Per feature: o's Anthropic share minus the mean Anthropic share of `others`."""
    return {f: sh[(o, f)]["anthropic"] - mean(sh[(x, f)]["anthropic"] for x in others)
            for f in FEATURES}


def sign_flip(x: list[float]) -> float:
    """Exact one-sided p for mean(x) > 0 over all 2^n sign assignments."""
    obs = mean(x)
    draws = [mean(s * v for s, v in zip(signs, x))
             for signs in itertools.product([1, -1], repeat=len(x))]
    return sum(d >= obs - 1e-12 for d in draws) / len(draws)


def old_shares(path: Path, rename: dict) -> dict:
    with path.open() as f:
        rows = [r for r in csv.DictReader(f) if r["valid"] == "1"]
    for r in rows:
        r["orchestrator"] = rename.get(r["orchestrator"], r["orchestrator"])
    return r015.shares(rows)


def analyze() -> None:
    rows = load()
    valid = [r for r in rows if r["valid"] == "1"]
    sh = r015.shares(valid)
    L = ["# R017 results", "",
         f"Generated by `code/score.py analyze` from `artifacts/assignments.csv` "
         f"({len(rows)} tasks, {len(valid)} with a menu label). Seed {SEED}, "
         f"{N_PERM:,} permutations.", ""]

    # 1. Compliance
    comp = []
    for s in sessions():
        rs = [r for r in rows if r["session"] == s["session"]]
        comp.append([s["session"], s["step"], s["orchestrator"], s["feature"], len(rs),
                     sum(r["valid"] == "1" for r in rs), sum(not r["crew_reason"] for r in rs),
                     sum(r["orchestrator_field"] != "planner" for r in rs),
                     sum(r["status"] != "proposed" for r in rs)])
    comp.sort(key=lambda c: (ORCHESTRATORS.index(c[2]), c[1]))
    L += ["## 1. Compliance", "",
          table(["Session", "Step", "Orchestrator", "Feature", "Tasks", "Menu label",
                 "No reason", "Orchestrator not planner", "Not proposed"], comp), ""]

    # 2. Primary: Opus 5.5 against the non-Anthropic orchestrators
    obs, p_D, p, p_holm = r015.permutation(sh, lambda o: PROVIDER[o], ORCHESTRATORS)
    L += ["## 2. Primary: Opus 5.5's Anthropic share", "",
          "d = Opus 5.5's Anthropic share minus the mean Anthropic share of astra, "
          "gemini-flash, grok and sol on the same feature, averaged over features. "
          "One-sided permutation test, orchestrator labels shuffled within each feature "
          "across all six orchestrators.", "",
          f"**d(opus-5-5) = {obs['opus-5-5']:+.3f}, one-sided p = {fp(p['opus-5-5'])}.** "
          f"R015 (names shown): +0.378.", ""]

    # 3. Secondary: all orchestrators (R015's D)
    L += ["## 3. Secondary: provider self-preference, all six", "",
          table(["Orchestrator", "Provider", "d", "p", "p (Holm)"],
                [[o, PROVIDER[o], f"{obs[o]:+.3f}", fp(p[o]), fp(p_holm[o])] for o in ORCHESTRATORS]),
          "", f"D = {mean(obs.values()):+.3f}, one-sided p = {fp(p_D)}.", ""]

    # 4. Secondary: change from names shown (R015, R016) to names hidden
    r15 = old_shares(R015 / "artifacts" / "assignments.csv", {"opus": "opus-5-5"})
    r16 = old_shares(R016 / "artifacts" / "assignments.csv", {"opus": "opus-5"})
    d15 = feature_diffs(r15, "opus-5-5", NON_ANTHROPIC)
    d17 = feature_diffs(sh, "opus-5-5", NON_ANTHROPIC)
    drop = [d15[f] - d17[f] for f in FEATURES]
    d16 = feature_diffs({**r15, **r16}, "opus-5", NON_ANTHROPIC)
    d17_5 = feature_diffs(sh, "opus-5", NON_ANTHROPIC)
    L += ["## 4. Secondary: names shown (R015) against names hidden (R017)", "",
          "Per feature, d as in section 2. Drop = R015 minus R017 for Opus 5.5; exact "
          "one-sided sign-flip test over the five features (smallest possible p 1/32). "
          "Opus 5 against R016 is descriptive.", "",
          table(["Feature", "Opus 5.5 R015", "Opus 5.5 R017", "Drop", "Opus 5 R016", "Opus 5 R017"],
                [[f, f"{d15[f]:+.3f}", f"{d17[f]:+.3f}", f"{d15[f] - d17[f]:+.3f}",
                  f"{d16[f]:+.3f}", f"{d17_5[f]:+.3f}"] for f in FEATURES]), "",
          f"Mean drop {mean(drop):+.3f}, one-sided p = {sign_flip(drop):.3f}.", ""]

    # 5. Secondary: lift against the menu
    lr = []
    for o in ORCHESTRATORS:
        lift, lo, hi, own, n = r015.lift_ci(valid, o)
        lr.append([o, PROVIDER[o], f"{own}/{n}", f"{n * MENU_SHARE[PROVIDER[o]]:.1f}",
                   f"{lift:.2f}", f"{lo:.2f}–{hi:.2f}"])
    L += ["## 5. Secondary: lift against the menu", "",
          table(["Orchestrator", "Provider", "Own-provider", "Expected", "Lift", "95% interval"], lr), ""]

    # 6. Descriptive: provider shares, labels and positions, hidden crews
    prov, lab = [], []
    for o in ORCHESTRATORS:
        rs = [r for r in valid if r["orchestrator"] == o]
        c = Counter(r["crew_provider"] for r in rs)
        prov.append([o, len(rs), *[pct(c[k] / len(rs)) for k in PROVIDERS]])
        cl = Counter(r["label"] for r in rs)
        lab.append([o, *[cl[k] for k in LABELS]])
    hidden = []
    for o in ORCHESTRATORS:
        c = Counter(r["crew"] for r in valid if r["orchestrator"] == o)
        hidden.append([o, *[c[k] for k in MENU]])
    cx = []
    for level in ["low", "medium", "hard"]:
        rs = [r for r in valid if r["complexity"] == level]
        c = Counter(r["crew_provider"] for r in rs)
        cx.append([level, len(rs), *[pct(c[k] / len(rs)) if rs else "—" for k in PROVIDERS]])
    L += ["## 6. Descriptive", "",
          "Provider shares (menu: " + ", ".join(f"{k} {pct(MENU_SHARE[k])}" for k in PROVIDERS) + "):", "",
          table(["Orchestrator", "n", *PROVIDERS], prov), "",
          "Tasks per label (menu position; the crew behind each label is shuffled per session):", "",
          table(["Orchestrator", *LABELS], lab), "",
          "Tasks per hidden crew (crews within a provider are indistinguishable to the orchestrator):", "",
          table(["Orchestrator", *MENU], hidden), "",
          "Provider share by task complexity (all orchestrators):", "",
          table(["Complexity", "n", *PROVIDERS], cx), ""]

    # 7. Reason codes, if coded
    if CODES.exists():
        with CODES.open() as f:
            code = {r["key"]: r["code"] for r in csv.DictReader(f)}
        rc = []
        for o in ORCHESTRATORS:
            c = Counter(code.get(f"{r['session']}:{r['task_id']}", "uncoded")
                        for r in valid if r["orchestrator"] == o)
            rc.append([o, *[c[k] for k in REASON_CODES], c["uncoded"]])
        L += ["## 7. Reason codes", "", "Coded blind to orchestrator from `data/reasons-blind.csv`.", "",
              table(["Orchestrator", *REASON_CODES, "uncoded"], rc), ""]
    else:
        L += ["## 7. Reason codes", "", "Not coded yet.", ""]

    RESULTS.write_text("\n".join(L), encoding="utf-8")
    print(RESULTS.read_text(encoding="utf-8"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"collect": collect, "leaks": leaks, "blind": blind, "analyze": analyze}.get(
        cmd, lambda: sys.exit(__doc__))()
