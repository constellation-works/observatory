#!/usr/bin/env python3
"""Principia owner mapping and projections; orbit-research owns record mechanics.

Historical imports remain v1. Native v2 appends live in research/records and are
selected explicitly, never by newest timestamp or a guessed upstream identity.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha1
import importlib.util
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
import tempfile

from orbit_research import make_record, protocol_digest, validate
from orbit_research.contract import reference, revision_digest
from orbit_research.importers import VERDICTS, strict_json
from orbit_research.native import Owner, safe_path
import wide_binary_records as pilot

ROOT = pilot.ROOT
BASE = "4e3b02c59b694d85016915177ef1ae157895ed7b"
ORRERY = "a1c430db54d585048ec85c4e7c47141db634f398"
AUTHORITY = Path("research/corpus")
ACTIVE = Path("research/active.json")
GUIDES = {"theory/README.md", "studies/README.md", "gates/README.md", "policy.md"}
LIMIT = "Exact historical verdict and stated assumptions only; migration makes no new scientific inference."
encoded, digest, require, git = pilot.encoded, pilot.digest, pilot.require, pilot.git


def policy():
    name = "principia_policy"
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, ROOT / "scripts/check-theory.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def local_paths(root):
    paths = git(root, "ls-tree", "-r", "--name-only", BASE).decode().splitlines()
    return [p for p in paths if p.startswith(("theory/", "studies/", "gates/", "schema/"))
            or p in {"ledger.md", "policy.md"}]


def snapshot(repository, revision, path, root):
    record = pilot.snapshot(repository, revision, path, root)
    # Retain the actual commit object as well as portable human-readable fields.
    record["legacy"]["commit_object"] = git(root, "cat-file", "commit", revision).decode()
    record["scope"] = "literature" if repository == "principia" and path.startswith("studies/") else "unknown"
    record["missingness"] = sorted(set(record["missingness"] + (["scope"] if record["scope"] == "unknown" else [])))
    record["revision_id"] = revision_digest(record)
    return record


def collect(root, orrery):
    sources = [snapshot("principia", BASE, p, root) for p in local_paths(root)]
    slugs = {m for s in sources for m in re.findall(r"orrery/lab/sims/([a-z0-9-]+)", s["legacy"]["text"])}
    # Catalog and textual result metadata only. Never execute/import sim code.
    listing = git(orrery, "ls-tree", "-r", "--name-only", ORRERY).decode().splitlines()
    selected = [p for p in listing if any(p.startswith(f"lab/sims/{slug}/") for slug in slugs)
                and p.endswith((".json", ".md"))]
    return sources + [snapshot("orrery", ORRERY, p, orrery) for p in selected]


def key(record):
    return record["id"], record["revision_id"], record["provenance"]["git_revision"]


def refkey(ref):
    return ref["id"], ref["revision_id"], ref["source_revision"]


def build(sources, pilot_manifest, pilot_records):
    local = {s["legacy"]["source_pin"]["path"]: s for s in sources
             if s["legacy"]["source_pin"]["repository"] == "principia"}
    require(len(local) == sum(s["legacy"]["source_pin"]["repository"] == "principia" for s in sources), "duplicate local source")
    require(all(s["legacy"]["source_pin"]["git_revision"] ==
                (BASE if s["legacy"]["source_pin"]["repository"] == "principia" else ORRERY) for s in sources), "wrong inventory pin")
    records = list(sources)
    accounting, programs, protocols = [], {}, {}

    def add(kind, alias, payload, src, legacy, selector="$", activity="unknown", scope="unknown", missing=()):
        r = make_record("principia", kind, alias, payload, pilot.provenance(src, selector),
                        legacy=legacy, activity=activity, scope=scope,
                        limitations=[LIMIT], missingness=missing)
        records.append(r)
        return r

    def account(src, selector, target, pointer, value, **extra):
        accounting.append(dict(source=reference(src), selector=selector, target=reference(target),
                               pointer=pointer, value_digest=digest(encoded(value)), **extra))

    for src in sources:
        path = src["legacy"]["source_pin"]["path"]
        text = src["legacy"]["text"]
        account(src, "$bytes", src, "/legacy/text", text, disposition="retained-source")
        if path.endswith(".json"):
            raw = strict_json(text)
            # Every owned leaf, and each upstream top-level subtree, has a locator.
            fields = pilot.leaves(raw) if src in local.values() else (("/" + k.replace("~", "~0").replace("/", "~1"), v) for k, v in raw.items())
            for ptr, value in fields:
                account(src, ptr, src, "/legacy/text", value, decode="json", disposition="retained-field")
        else:
            offset = 0
            for heading, section in pilot.sections(text):
                account(src, f"text:{offset}:{offset + len(section)}", src, "/legacy/text", section,
                        heading=heading, disposition="retained-prose")
                offset += len(section)

    for path, src in sorted(local.items()):
        if not path.endswith("/claims.json"):
            continue
        registry = strict_json(src["legacy"]["text"])
        slug = registry["doc"]
        if slug == pilot.FAMILY:
            phase = pilot_manifest["phases"]["original-outcome"]
            programs[slug] = deepcopy(phase)
            continue
        # Administrative retirement/resolution is distinct from each claim verdict.
        activity = {"retired": "retired", "resolved": "resolved", "refuted": "paused"}.get(registry["status"], "active")
        metadata = {k: v for k, v in registry.items() if k != "claims"}
        program = add("program", slug, dict(role="theory", title=registry["title"]), src, metadata, activity=activity)
        for ptr, value in pilot.leaves(metadata):
            account(src, ptr, program, "/legacy" + ptr, value, disposition="mapped")
        claims, assessments = [], []
        for i, row in enumerate(registry["claims"]):
            scope = "derivation" if row["kind"] == "derived" else "unknown"
            domain = "nature" if row["kind"] == "nature" else "model"
            claim = add("claim", row["id"], dict(role="postulate" if row["kind"] == "postulate" else "claim",
                        statement=row["claim"], domain=domain), src, row, f"/claims/{i}", activity, scope)
            assessment = add("assessment", row["id"] + ":legacy-verdict", dict(claim=reference(claim),
                        verdict=VERDICTS[row["status"]], legacy_verdict=row["status"], inference="historical",
                        basis="legacy-report", controls="unknown", rationale=row.get("evidence") or "No source evidence rationale supplied.",
                        evidence=[]), src, row, f"/claims/{i}", "unknown", scope,
                        missing=["exact-evidence-owner-references", "independently-verified-controls"])
            for ptr, value in pilot.leaves(row):
                account(src, f"/claims/{i}{ptr}", claim, "/legacy" + ptr, value, disposition="mapped")
            for field, target, pointer in [("claim", claim, "/payload/statement"), ("status", assessment, "/payload/legacy_verdict"),
                                           ("evidence", assessment, "/payload/rationale")]:
                if field in row:
                    account(src, f"/claims/{i}/{field}", target, pointer, row[field], disposition="mapped")
            claims.append(reference(claim))
            assessments.append(reference(assessment))
        programs[slug] = dict(program=reference(program), claims=claims, assessments=assessments)

    for path, src in sorted(local.items()):
        if not (path.startswith("gates/") and path.endswith(".json")):
            continue
        gate = strict_json(src["legacy"]["text"])
        if path == pilot.GATE:
            protocols[gate["id"]] = pilot_manifest["protocol"]
            continue
        # The full current gate and linked chapter are historical normative snapshots,
        # never a reconstructed prospective freeze or an asserted completed run.
        semantic = dict(gate=gate, linked_prose={p: s["legacy"]["text"] for p, s in local.items()
                        if p in {gate.get("chapter"), gate.get("analytic_attempt", {}).get("chapter")}})
        r = add("protocol", gate["id"], dict(semantic=semantic, semantic_digest=protocol_digest(semantic),
                freeze="historical-unverified", frozen_at=None, freeze_evidence=None), src, gate,
                activity="paused" if gate.get("status") == "closed" else "active",
                missing=["prospective-freeze-and-consumption-not-verified"])
        protocols[gate["id"]] = reference(r)
        for ptr, value in pilot.leaves(gate):
            account(src, ptr, r, "/payload/semantic/gate" + ptr, value, disposition="mapped")

    links = []
    for src in sources:
        pin, text = src["legacy"]["source_pin"], src["legacy"]["text"]
        if pin["repository"] != "principia":
            continue
        locators = [(f"text:{m.start(1)}:{m.end(1)}", m[1]) for m in re.finditer(r"\]\(([^)]+)\)", text)]
        if pin["path"].endswith(".json"):
            locators += [(ptr, v) for ptr, v in pilot.leaves(strict_json(text)) if isinstance(v, str)
                         and re.search(r"/(?:links)/\d+$", ptr)]
        for selector, locator in locators:
            target = posixpath.normpath(posixpath.join(posixpath.dirname(pin["path"]), locator.split("#")[0]))
            local_target = target + "/README.md" if locator.split("#")[0].endswith("/") else target
            source = local.get(local_target)
            links.append(dict(source=reference(src), selector=selector, locator=locator,
                              retained_target=reference(source) if source else None,
                              status="pending", reason="Retained locator is not an exact owner scientific evidence tuple; no consumption inferred."))

    views = {p: reference(s) for p, s in sorted(local.items()) if p not in GUIDES}
    manifest = dict(schema_version=1, migration="ORB-11394", baseline=BASE, foundation_baseline=pilot.BASE,
                    framework=dict(version="0.2.0", git_revision=pilot.INSTALLED_FRAMEWORK, historical_schema=1, native_schema=2),
                    source_pins=dict(principia=BASE, orrery=ORRERY),
                    sources=[dict(record=pilot.record_path(s), **s["legacy"]["source_pin"]) for s in sources],
                    records=[dict(path=pilot.record_path(r), id=r["id"], revision_id=r["revision_id"], sha256=digest(encoded(r))) for r in records],
                    retained_pilot_records=pilot_manifest["records"], programs=programs, protocols=protocols,
                    aliases=[dict(alias=a, record=reference(r)) for r in records + pilot_records for a in r["aliases"]],
                    compatibility=views, accounting=accounting, links=links,
                    pending_reconciliation=deepcopy(pilot_manifest["pending_reconciliation"]) + [dict(repository="orrery",
                        path=s["legacy"]["source_pin"]["path"], inventory_revision=ORRERY, consumed_revision=None,
                        id=None, revision_id=None, status="pending", source_artifact=reference(s),
                        reason="Read-only migration inventory snapshot, not a pin of historical consumption. Exact upstream owner manifest is not reconciled.")
                        for s in sources if s["legacy"]["source_pin"]["repository"] == "orrery"])
    all_records = {key(r): r for r in records + pilot_records}
    report = dict(baseline=BASE, foundation_baseline=pilot.BASE, programs=len(programs),
                  claims=sum(len(p["claims"]) for p in programs.values()), gates=len(protocols),
                  studies=sum(p.startswith("studies/") and p not in GUIDES for p in local),
                  compatibility_files=len(views), sources=len(sources), new_historical_records=len(records),
                  retained_pilot_records=len(pilot_records), accounted_selectors=len(accounting),
                  claim_statuses=dict(Counter(all_records[refkey(a)]["payload"]["legacy_verdict"] for p in programs.values() for a in p["assessments"])),
                  program_statuses={slug: strict_json(local[f"theory/{slug}/claims.json"]["legacy"]["text"])["status"] for slug in programs},
                  wall=strict_json(local["schema/wall.json"]["legacy"]["text"]),
                  pending_external_snapshots=len(manifest["pending_reconciliation"]), global_reconciliation=False,
                  foundation_difference="No program, claim, or gate differences; source pin comparison is tested against the foundation baseline.")
    active = dict(schema_version=1, migration="ORB-11394", baseline=BASE, sources=views, programs=programs,
                  protocols=protocols)
    outputs = {pilot.record_path(r): encoded(r) for r in records}
    require(len(outputs) == len(records), "record collision")
    for label, pin in [("source", BASE), ("archival", None)]:
        outputs[f"{label}-manifest.json"] = encoded(dict(schema_version=1, kind="manifest",
            repositories=[dict(id="principia", git_revision=pin)],
            references=[reference(r) for r in records if r["provenance"]["git_revision"] == pin]))
    outputs.update({"migration.json": encoded(manifest), "equivalence.json": encoded(report)})
    return outputs, active


def read_history(root):
    pilot_manifest, _ = pilot.inspect(root, compatibility=False)
    pilot_records = [strict_json((root / pilot.AUTHORITY / r["path"]).read_bytes()) for r in pilot_manifest["records"]]
    directory = root / AUTHORITY
    manifest = strict_json((directory / "migration.json").read_bytes())
    sources = []
    for item in manifest["sources"]:
        src = strict_json(safe_path(root, (AUTHORITY / item["record"]).as_posix()).read_bytes())
        data, pin = src["legacy"]["text"].encode(), src["legacy"]["source_pin"]
        require(digest(data) == pin["sha256"] == src["payload"]["snapshot_digest"] and len(data) == pin["bytes"], "source bytes changed")
        require(sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == pin["blob_oid"], "source blob changed")
        commit = src["legacy"]["commit_object"].encode()
        require(sha1(b"commit " + str(len(commit)).encode() + b"\0" + commit).hexdigest() == pin["git_revision"], "commit object changed")
        sources.append(src)
    outputs, active = build(sources, pilot_manifest, pilot_records)
    require({p.relative_to(directory).as_posix() for p in (directory / "records").glob("*.json")} ==
            {p for p in outputs if p.startswith("records/")}, "historical record inventory changed")
    for path, data in outputs.items():
        require(safe_path(root, (AUTHORITY / path).as_posix()).read_bytes() == data, f"immutable mapping drift: {path}")
        if path.startswith("records/") or path.endswith("-manifest.json"):
            errors = validate(strict_json(data))
            require(not errors, f"framework {path}: {errors}")
    records = [strict_json(data) for p, data in outputs.items() if p.startswith("records/")] + pilot_records
    return manifest, active, records


def selected(root, active, records):
    native = Owner(root, "principia").records() if (root / "research/records").exists() else []
    for r in native:
        closure, _ = Owner(root, "principia").closure([r])
        require(not validate(r, targets=[t for t in closure if key(t) != key(r)]), f"native validation failed: {r['id']}")
        if r["kind"] == "artifact" and r["payload"]["role"] == "source" and r["payload"]["availability"] == "available":
            source_bytes(root, r)  # Inactive historical content must survive too.
    by = {key(r): r for r in records + native}
    def resolve(ref):
        require(refkey(ref) in by, "selected exact owner record is missing")
        r = by[refkey(ref)]
        require(ref == reference(r), "activation must select the exact pending owner reference")
        return r
    return resolve


def source_bytes(root, record):
    require(record["kind"] == "artifact" and record["payload"]["role"] == "source", "view requires source artifact")
    if record["schema_version"] == 1:
        data = record["legacy"]["text"].encode()
    else:
        locator = record["payload"]["locator"]
        require(isinstance(locator, str) and locator.startswith("research/content/"), "native prose must use immutable research/content bytes")
        require(Path(locator).name.split(".")[0] == record["payload"]["snapshot_digest"][7:], "native content filename must bind its digest")
        data = safe_path(root, locator).read_bytes()
    require(digest(data) == record["payload"]["snapshot_digest"], "selected source digest mismatch")
    return data


def project(root, active, baseline, records):
    require(set(active) == set(baseline) and active["schema_version"] == 1 and active["baseline"] == BASE and active["migration"] == "ORB-11394", "invalid activation")
    for group in ("sources", "programs", "protocols"):
        require(set(active[group]) == set(baseline[group]), f"activation must retain every {group} identity")
    resolve = selected(root, active, records)
    views = {path: source_bytes(root, resolve(ref)) for path, ref in active["sources"].items()}
    # Core science is edited through typed records. Source artifacts own retained
    # metadata and prose; their old core fields are overwritten by these selections.
    for slug, entry in active["programs"].items():
        original = baseline["programs"][slug]
        require(set(entry) == set(original), "program selection fields changed")
        path = f"theory/{slug}/claims.json"
        doc = strict_json(views[path])
        source_doc = deepcopy(doc)
        original_doc = strict_json(source_bytes(root, resolve(baseline["sources"][path])))
        program = resolve(entry["program"])
        require(program["id"] == resolve(original["program"])["id"], "program identity changed")
        doc["title"] = program["payload"]["title"]
        if program["schema_version"] == 2:
            doc["headline"] = program["payload"]["question"]
        doc["status"] = program["legacy"]["status"] if program["schema_version"] == 1 else {
            "retired": "retired", "resolved": "resolved", "active": original_doc["status"]}[program["activity"]]
        if original_doc["status"] in {"retired", "refuted", "resolved"}:
            require(doc["status"] == original_doc["status"] and doc["live_fronts"] == [] and
                    program["activity"] == resolve(original["program"])["activity"], "closed program cannot reactivate through migration activation")
        require(len(entry["claims"]) == len(entry["assessments"]) == len(original["claims"]) == len(doc["claims"]), "claim inventory changed")
        changes = {}
        for i, (cr, ar) in enumerate(zip(entry["claims"], entry["assessments"])):
            claim, assessment = resolve(cr), resolve(ar)
            previous_claim = resolve(original["claims"][i])
            require(claim["id"] == previous_claim["id"] and doc["claims"][i]["id"] == previous_claim["aliases"][0], "claim identity/order changed")
            require(assessment["kind"] == "assessment" and refkey(assessment["payload"]["claim"]) == key(claim), "assessment must target exact selected claim")
            row = doc["claims"][i]
            require(claim["payload"]["domain"] == ("nature" if row["kind"] == "nature" else "model"), "claim domain contradicts retained kind")
            require((claim["payload"]["role"] == "postulate") == (row["kind"] == "postulate"), "postulate role contradicts retained kind")
            row["claim"] = claim["payload"]["statement"]
            ap = assessment["payload"]
            if assessment["schema_version"] == 2 and ap["controls"] in {"failed", "not-run"}:
                require(ap["verdict"] not in {"supported", "refuted"}, "failed or unrun controls cannot adjudicate a native claim")
            row["status"] = ap["legacy_verdict"] or {"inconclusive": "mixed"}.get(ap["verdict"], ap["verdict"])
            require(row["status"] in policy().CLAIM_STATUSES and VERDICTS[row["status"]] == ap["verdict"], "unrepresentable legacy verdict")
            if "evidence" in row or assessment["schema_version"] == 2:
                row["evidence"] = assessment["legacy"]["evidence"] if assessment["schema_version"] == 1 and "evidence" in assessment["legacy"] else ap["rationale"]
            if original_doc["status"] in {"retired", "refuted", "resolved"}:
                require(row == original_doc["claims"][i], "closed program scientific rows are archival")
            old = source_doc["claims"][i]
            if row != old:
                changes[old["claim"]] = (old, row)
        if doc != source_doc:
            views[path] = encoded(doc)
            hub_path = f"theory/{slug}/README.md"
            hub = views[hub_path].decode()
            for field in ("title", "status"):
                if doc[field] != source_doc[field]:
                    hub = re.sub(rf"(?m)^{field}: .*", f"{field}: " + json.dumps(doc[field], ensure_ascii=False), hub, count=1)
            views[hub_path] = hub.encode()
            ledger_path = f"theory/{slug}/evidence-ledger.md"
            lines = []
            for line in views[ledger_path].decode().splitlines(keepends=True):
                cells = policy().split_row(line) if line.startswith("|") else []
                if cells and cells[0] in changes:
                    old, row = changes[cells[0]]
                    parts = re.split(r"(?<!\\)\|", line)
                    parts[1] = " " + row["claim"] + " "
                    if old["status"] != row["status"]:
                        parts[2] = " " + row["status"] + " "
                    if old.get("evidence") != row.get("evidence"):
                        parts[3] = " " + row["evidence"].replace("|", "\\|").replace("\n", " ") + " "
                    line = "|".join(parts)
                lines.append(line)
            views[ledger_path] = "".join(lines).encode()

    for ident, ref in active["protocols"].items():
        protocol = resolve(ref)
        require(protocol["id"] == resolve(baseline["protocols"][ident])["id"], "protocol identity changed")
        # Existing historical gates cannot silently become newly registered protocols.
        require(ref == baseline["protocols"][ident], "new protocol activation requires a separately reviewed owner mapping")
        gate_path = f"gates/{ident}.json"
        require(views[gate_path] == source_bytes(root, resolve(baseline["sources"][gate_path])), "historical gate terms changed")
    require(views["schema/wall.json"] == source_bytes(root, resolve(baseline["sources"]["schema/wall.json"])), "immortal wall changed")
    # Rollup is wholly generated. Its historical source remains in the audit.
    with tempfile.TemporaryDirectory(prefix="principia-projection-") as temp:
        target = Path(temp)
        for path, data in views.items():
            out = target / path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        docs, gates, errors, wall = policy().load_corpus(target)
        require(not errors, str(errors))
        views["ledger.md"] = policy().render_ledger(docs, gates, wall).encode()
    return views


def inspect(root, *, compatibility=True, active_path=None):
    manifest, baseline, records = read_history(root)
    active = strict_json((active_path or root / ACTIVE).read_bytes())
    views = project(root, active, baseline, records)
    if compatibility:
        for path, data in views.items():
            require((root / path).read_bytes() == data, f"compatibility drift: {path}; project selected owner records")
        actual = {p.relative_to(root).as_posix() for top in ("theory", "studies", "gates", "schema")
                  for p in (root / top).rglob("*") if p.is_file() and p.relative_to(root).as_posix() not in GUIDES}
        require(actual == set(views) - {"ledger.md"}, "unaccounted scientific file or deleted view")
    return manifest, views


def validate_views(root, views, orrery=None):
    """Apply the unchanged scientific policy to a candidate before exporting it."""
    with tempfile.TemporaryDirectory(prefix="principia-policy-") as temp:
        target = Path(temp)
        extras = {p: (root / p).read_bytes() for p in GUIDES | {"README.md", "research/README.md"} if (root / p).is_file()}
        for path, data in (extras | views).items():
            out = target / path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        checker = policy()
        configured = checker.parse_external_roots([f"orrery={orrery}"]) if orrery else checker.external_roots(root)
        docs, gates, errors, wall = checker.load_corpus(target)
        errors += checker.check_docs(target, docs, checker.dt.date.today(), configured)
        errors += checker.check_cross(docs, gates, wall, target)
        errors += checker.check_markdown_links(target, configured)
        errors += checker.check_ledger(target, checker.render_ledger(docs, gates, wall))
        require(not errors, "owner policy: " + "; ".join(errors))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["migrate", "check", "project", "rollback", "verify-history"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--orrery-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--active", type=Path, help="candidate activation; never silently selects latest")
    args = parser.parse_args(argv)
    try:
        pilot.package_check()
        root = args.root.resolve()
        if args.command == "migrate":
            require(args.output is not None and args.orrery_root is not None, "migrate requires --output and --orrery-root")
            pm, _ = pilot.inspect(root, compatibility=False)
            pr = [strict_json((root / pilot.AUTHORITY / r["path"]).read_bytes()) for r in pm["records"]]
            sources = collect(root, args.orrery_root)
            outputs, active = build(sources, pm, pr)
            pilot.export(root, args.output, {(AUTHORITY / p).as_posix(): v for p, v in outputs.items()} | {ACTIVE.as_posix(): encoded(active)})
        else:
            manifest, baseline, records = read_history(root)
            if args.command == "rollback":
                # Export the baseline while retaining every later append/content file.
                views = project(root, baseline, baseline, records)
            else:
                manifest, views = inspect(root, compatibility=args.command in {"check", "verify-history"}, active_path=args.active)
            if args.command == "verify-history":
                require(args.orrery_root is not None, "verify-history requires --orrery-root")
                require(set(local_paths(root)) == {s["path"] for s in manifest["sources"] if s["repository"] == "principia"}, "historical local inventory differs")
                for item in manifest["sources"]:
                    owner = root if item["repository"] == "principia" else args.orrery_root
                    fresh = snapshot(item["repository"], item["git_revision"], item["path"], owner)
                    archived = strict_json((root / AUTHORITY / item["record"]).read_bytes())
                    require(pilot.historical_equal(fresh, archived), f"historical source differs: {item['path']}")
                for path in baseline["sources"]:
                    require(git(root, "show", f"{pilot.BASE}:{path}") == git(root, "show", f"{BASE}:{path}"), f"foundation difference: {path}")
            elif args.command in {"project", "rollback"}:
                require(args.output is not None, "export requires --output")
                validate_views(root, views, args.orrery_root)
                pilot.export(root, args.output, views)
        print("Principia owner records valid; historical science preserved; external reconciliation pending")
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f"corpus records: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
