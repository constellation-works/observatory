#!/usr/bin/env python3
"""ORB-11378 owner adapter: lossless historical migration, never an experiment runner.

Record identity, semantic hashing and scientific validation belong to orbit-research.
This adapter supplies only Principia's fixed pilot mapping and compatibility policy.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha1, sha256
from importlib.metadata import distribution
import json
from pathlib import Path
import re
import subprocess
import sys

from orbit_research import make_record, protocol_digest, validate
from orbit_research.contract import reference

BASE = "13866b2848fbcce9a1f1ef2d4b97051a65f7e626"
FREEZE = "c04f2ed1ae91d6c126bc60863b5e48f46abe4576"
ORIGINAL = "28dd5c72bb670517b93b556f1d2483402c8e8655"
DIAGNOSIS = "2e097e606bc751ba1a8b29ebdc5aab6bbd961c43"
FRAMEWORK = "7b6c1b2380bc915d6ff7cca50f288ed716a99c74"
FAMILY = "wide-binary-selection-methodology"
THEORY = f"theory/{FAMILY}"
CLAIMS = f"{THEORY}/claims.json"
GATE = "gates/wide-binary-selection-bias-control.json"
STUDY = "studies/wide-binary-selection-bias-preregistration.md"
ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = Path("research/wide-binary")
COMPATIBILITY = [f"{THEORY}/{name}" for name in (
    "README.md", "claims.json", "evidence-ledger.md", "open-questions.md", "related.md"
)] + [GATE, STUDY]
LIMIT = "Historical synthetic/model calibration only; no new scientific adjudication or nature-level inference."


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()


def digest(data):
    return "sha256:" + sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def package_check():
    dist = distribution("orbit-research")
    direct = json.loads(dist.read_text("direct_url.json") or "{}")
    require(dist.version == "0.1.0" and
            direct.get("vcs_info", {}).get("commit_id") == FRAMEWORK,
            "Install requirements-research.txt: exact orbit-research Git revision required")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def record_path(record):
    return f"records/{record['kind']}-{record['revision_id'].split(':')[1]}.json"


def source_spec():
    specs = [("principia", BASE, p) for p in COMPATIBILITY]
    specs += [("principia", FREEZE, p) for p in (CLAIMS, GATE, STUDY)]
    specs += [("principia", BASE, "studies/gaia-wide-binaries-low-acceleration.md")]
    for revision, slug in [(ORIGINAL, "wide-binary-selection-bias"),
                           (DIAGNOSIS, "wide-binary-control-diagnosis")]:
        specs += [("orrery", revision, f"lab/sims/{slug}/{name}") for name in (
            "README.md", "RUN-2026-09-05.md", "sim.json", "assets/results.json", "main.py"
        )]
    return specs


def snapshot(repository, revision, path, root):
    data = git(root, "show", f"{revision}:{path}")
    pin = dict(repository=repository, git_revision=revision, path=path,
               blob_oid=git(root, "rev-parse", f"{revision}:{path}").decode().strip(),
               sha256=digest(data), bytes=len(data),
               commit_metadata=git(root, "show", "-s", "--format=%H%n%aI%n%cI%n%s", revision).decode())
    # These are Principia-owned copies of sources, not invented Orrery records.
    local = repository == "principia"
    provenance = dict(repository="principia", git_revision=revision if local else None,
                      blob_oid=pin["blob_oid"] if local else None,
                      sha256=pin["sha256"], path=path if local else f"upstream-snapshot/{repository}/{revision}/{path}",
                      selector="$", historical=True, working_tree=False if local else True)
    return make_record("principia", "artifact", f"source:{repository}:{revision}:{path}",
                       dict(role="source", availability="available", snapshot_digest=pin["sha256"],
                            locator=None, media_type="application/json" if path.endswith(".json") else "text/plain"),
                       provenance, legacy=dict(source_pin=pin, text=data.decode()), activity="active",
                       scope="synthetic-calibration" if repository == "orrery" or path != "studies/gaia-wide-binaries-low-acceleration.md" else "literature",
                       limitations=["Immutable archival source copy; upstream scientific ownership is unchanged."],
                       missingness=[] if local else ["owner-ingestion-git-pin", "upstream-canonical-record"])


def source_key(source):
    p = source["legacy"]["source_pin"]
    return p["repository"], p["git_revision"], p["path"]


def provenance(source, selector="$"):
    p = deepcopy(source["provenance"])
    p["selector"] = selector
    return p


def leaves(value, pointer=""):
    """Every JSON leaf, including empty containers, has an exact source pointer."""
    if isinstance(value, dict) and value:
        for key, child in value.items():
            yield from leaves(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
    elif isinstance(value, list) and value:
        for i, child in enumerate(value):
            yield from leaves(child, pointer + f"/{i}")
    else:
        yield pointer, value


def sections(text):
    """Partition every byte, including frontmatter, blank lines and code fences."""
    starts = [0] + [m.start() for m in re.finditer(r"(?m)^## ", text) if m.start()]
    return [(text[a:b].splitlines()[0], text[a:b])
            for a, b in zip(starts, starts[1:] + [len(text)])]


def build(sources):
    """Deterministic pilot mapping from immutable source-artifact records."""
    lookup = {source_key(s): s for s in sources}
    require(set(lookup) == set(source_spec()) and len(sources) == len(lookup), "source inventory changed")
    source = lambda rev, path, repo="principia": lookup[(repo, rev, path)]
    raw = lambda rev, path, repo="principia": source(rev, path, repo)["legacy"]["text"]
    records = list(sources)
    accounting = []
    def add(kind, alias, payload, src, legacy, selector="$", missingness=()):
        record = make_record("principia", kind, alias, payload, provenance(src, selector),
                             legacy=legacy, activity="active", scope="synthetic-calibration",
                             limitations=[LIMIT], missingness=missingness)
        records.append(record)
        return record
    def account(src, selector, target, pointer, value):
        accounting.append(dict(source=reference(src), selector=selector,
                               target=reference(target), pointer=pointer,
                               value_digest=digest(encoded(value)), disposition="preserved"))

    # Exact bytes are always retained. Rich mappings below supplement, never replace them.
    for src in sources:
        account(src, "$bytes", src, "/legacy/text", src["legacy"]["text"])
    frozen = {p: json.loads(raw(FREEZE, p)) for p in (CLAIMS, GATE)}
    semantic = dict(protocol_text=raw(FREEZE, STUDY), gate=frozen[GATE], registry=frozen[CLAIMS])
    protocol = add("protocol", "wide-binary-selection-bias-control",
                   dict(semantic=semantic, semantic_digest=protocol_digest(semantic),
                        freeze="historical-unverified", frozen_at=None, freeze_evidence=None),
                   source(FREEZE, STUDY), None,
                   missingness=["independent-prospective-freeze-evidence"])
    for path, key in [(GATE, "gate"), (CLAIMS, "registry")]:
        for ptr, value in leaves(frozen[path]):
            account(source(FREEZE, path), ptr, protocol, f"/payload/semantic/{key}{ptr}", value)
    account(source(FREEZE, STUDY), "$text", protocol, "/payload/semantic/protocol_text", raw(FREEZE, STUDY))

    phases = {}
    programs = {}
    for revision, phase in [(FREEZE, "freeze"), (BASE, "original-outcome")]:
        registry = json.loads(raw(revision, CLAIMS))
        program = add("program", FAMILY, dict(role="program", title=registry["title"]),
                      source(revision, CLAIMS), {k: v for k, v in registry.items() if k != "claims"})
        # Unchanged program content is one revision, even across source commits.
        if program["revision_id"] in programs:
            records.pop()
            program = programs[program["revision_id"]]
        else:
            programs[program["revision_id"]] = program
        for ptr, value in leaves(program["legacy"]):
            account(source(revision, CLAIMS), ptr, program, "/legacy" + ptr, value)
        claims, assessments = [], []
        for i, row in enumerate(registry["claims"]):
            claim = add("claim", row["id"], dict(role="claim", domain="model", statement=row["claim"]),
                        source(revision, CLAIMS), row, f"/claims/{i}")
            claims.append(claim)
            account(source(revision, CLAIMS), f"/claims/{i}/claim", claim, "/payload/statement", row["claim"])
            for ptr, value in leaves(row):
                account(source(revision, CLAIMS), f"/claims/{i}{ptr}", claim, "/legacy" + ptr, value)
            verdict = {"mixed": "inconclusive", "supported": "supported", "untested": "untested"}[row["status"]]
            evidence = [] if phase == "freeze" else [reference(source(ORIGINAL, "lab/sims/wide-binary-selection-bias/assets/results.json", "orrery"))]
            assessment = add("assessment", f"{row['id']}:{phase}",
                             dict(claim=reference(claim), verdict=verdict, legacy_verdict=row["status"],
                                  inference="historical", basis="legacy-report",
                                  controls="not-run" if phase == "freeze" else ("passed" if verdict == "supported" else "failed"),
                                  rationale=row.get("evidence", "Untested in the original ORB-11221 registry."),
                                  evidence=evidence), source(revision, CLAIMS), row, f"/claims/{i}")
            assessments.append(assessment)
            account(source(revision, CLAIMS), f"/claims/{i}/status", assessment, "/payload/legacy_verdict", row["status"])
            if "evidence" in row:
                account(source(revision, CLAIMS), f"/claims/{i}/evidence", assessment, "/payload/rationale", row["evidence"])
        phases[phase] = dict(program=reference(program), claims=[reference(c) for c in claims],
                             assessments=[reference(a) for a in assessments])

    # Preserve the diagnostic as annotations on the original claim verdicts, not new verdicts.
    diagnostic_source = source(DIAGNOSIS, "lab/sims/wide-binary-control-diagnosis/assets/results.json", "orrery")
    diagnostic = json.loads(diagnostic_source["legacy"]["text"])
    later = []
    current_claims = [r for r in records if r["kind"] == "claim" and r["provenance"]["git_revision"] == BASE]
    for claim, control_index in zip(current_claims, [1, 1, 2, 3, 4]):
        row = claim["legacy"]
        control = diagnostic["verdict"]["controls"][control_index]
        assessment = add("assessment", f"{row['id']}:diagnostic-ORB-11241",
                         dict(claim=reference(claim), verdict="supported" if row["status"] == "supported" else "inconclusive",
                              legacy_verdict=row["status"], inference="historical", basis="legacy-report",
                              controls="passed" if row["status"] == "supported" else "failed",
                              rationale="ORB-11241 diagnostic annotation; original verdict unchanged.\n" + json.dumps(control, ensure_ascii=False, indent=2),
                              evidence=[reference(diagnostic_source)]), source(BASE, CLAIMS),
                         dict(status=row["status"], original_claim=row, diagnostic_control=control),
                         claim["provenance"]["selector"], missingness=["upstream-canonical-assessment"])
        later.append(reference(assessment))
        for ptr, value in leaves(control):
            account(diagnostic_source, f"/verdict/controls/{control_index}{ptr}", assessment,
                    "/legacy/diagnostic_control" + ptr, value)
    phases["later-diagnostic-annotation"] = dict(assessments=later)

    # Every current gate field and every prose section is explicitly accounted for.
    for src in sources:
        repo, revision, path = source_key(src)
        text = src["legacy"]["text"]
        if path.endswith(".md"):
            offset = 0
            for heading, section in sections(text):
                accounting.append(dict(source=reference(src), selector=f"text:{offset}:{offset + len(section)}",
                                       heading=heading, target=reference(src), pointer="/legacy/text",
                                       value_digest=digest(encoded(section)), disposition="preserved"))
                offset += len(section)
        elif repo == "principia" and path == GATE and revision == BASE:
            for ptr, value in leaves(json.loads(text)):
                accounting.append(dict(source=reference(src), selector=ptr,
                                       target=reference(src), pointer="/legacy/text", decode="json",
                                       value_digest=digest(encoded(value)), disposition="preserved"))
        elif path.endswith(".json") and not (repo == "principia" and path in (CLAIMS, GATE) and revision == FREEZE) and path != CLAIMS:
            # Keep catalog/result JSON as archival data, without inventing owner claims.
            for key, value in json.loads(text).items():
                accounting.append(dict(source=reference(src), selector="/" + key,
                                       target=reference(src), pointer="/legacy/text", decode="json",
                                       value_digest=digest(encoded(value)), disposition="preserved"))

    outputs = {record_path(r): encoded(r) for r in records}
    require(len(outputs) == len(records), "record file collision")
    manifests = {}
    for label, revision in [("freeze", FREEZE), ("source", BASE)]:
        manifest = dict(schema_version=1, kind="manifest",
                        repositories=[dict(id="principia", git_revision=revision)],
                        references=[reference(r) for r in records if r["provenance"]["git_revision"] == revision])
        manifests[label] = f"{label}-manifest.json"
        outputs[manifests[label]] = encoded(manifest)
    # v1 cannot represent an unknown scientific ID/revision. Do not fabricate one.
    pending = [dict(repository=repo, source_revision=rev, path=path,
                    source_artifact=reference(source(rev, path, repo)),
                    id=None, revision_id=None, status="pending",
                    reason="Owner has not supplied an exact canonical record/revision/source-pin tuple.")
               for repo, rev, path in source_spec() if repo != "principia" and path.endswith("sim.json")]
    pending.append(dict(repository="astrolabe", source_revision="90f5b58890da36c44286a4edbde7eead879410a8",
                        path="src/astrolabe/analysis/wide_binaries.py", id=None, revision_id=None,
                        status="pending", reason="Catalog-reported apparatus digest; no owner scientific record supplied or invented."))
    manifest = dict(schema_version=1, migration="ORB-11378", authority="immutable Principia-owned v1 records",
                    framework=dict(version="0.1.0", contract=1, git_revision=FRAMEWORK,
                                   foundation_revision="51b117d18f32550dbfca49ce96d2d72474a78b47"),
                    sources=[dict(record=record_path(s), **s["legacy"]["source_pin"]) for s in sources],
                    records=[dict(path=record_path(r), id=r["id"], revision_id=r["revision_id"],
                                  sha256=digest(encoded(r))) for r in records],
                    aliases=[dict(alias=a, id=r["id"], revision_id=r["revision_id"]) for r in records for a in r["aliases"]],
                    protocol=reference(protocol), phases=phases, framework_manifests=manifests,
                    compatibility=[dict(path=p, source=reference(source(BASE, p)), sha256=digest(raw(BASE, p).encode())) for p in COMPATIBILITY],
                    accounting=accounting, pending_reconciliation=pending,
                    legacy_links=[dict(source_artifact=reference(src), locator=match.group(1),
                                       status="pending", reason="Legacy locator retained; not a resolved canonical scientific reference.")
                                  for src in sources if source_key(src)[2].endswith(".md")
                                  for match in re.finditer(r"\]\(([^)]+)\)", src["legacy"]["text"])],
                    exceptions=[
                        dict(id="prospective-freeze-unverified", reason="Original run and later diagnosis report matching frozen byte hashes. Git timestamps and those historical reports establish a recoverable sequence, not independent prospective registration proof.", sources=[reference(source(FREEZE, STUDY)), reference(source(ORIGINAL, "lab/sims/wide-binary-selection-bias/RUN-2026-09-05.md", "orrery"))]),
                        dict(id="matrix-47-versus-44", reason="Original protocol says 47; its twelve rows enumerate 44. Both retained without repair.", sources=[reference(source(FREEZE, STUDY))]),
                        dict(id="historical-pending-diagnosis", reason="Current compatibility prose/headline retains then-pending ORB-11241 and stale not-yet-run wording. The later diagnostic annotations are separate and do not overwrite that source assessment.", sources=[reference(source(BASE, CLAIMS)), reference(diagnostic_source)]),
                        dict(id="diagnostic-internal-shift-discrepancy", reason="R3 positive_control says shift-insensitive; detailed D3 and open_questions report shift dependence. Preserve both; migration makes no choice between them.", sources=[reference(diagnostic_source)]),
                        dict(id="crossrepo-owner-records-pending", reason="Hash-pinned source copies are available here; canonical sibling scientific records remain pending. v1 typed references require known IDs and revisions, so unknown tuples are explicitly listed outside typed framework manifests.", sources=[reference(diagnostic_source)]),
                    ])
    outputs["migration.json"] = encoded(manifest)
    return outputs


def inspect(root, *, compatibility=True):
    """Fail closed on drift in source bytes, mapping, provenance, records or views."""
    directory = root / AUTHORITY
    manifest = json.loads((directory / "migration.json").read_text())
    sources = []
    for item in manifest["sources"]:
        path = directory / item["record"]
        require(path.resolve().is_relative_to(directory.resolve()), "source path escapes authority")
        src = json.loads(path.read_text())
        data = src["legacy"]["text"].encode()
        pin = src["legacy"]["source_pin"]
        require(digest(data) == pin["sha256"] == src["payload"]["snapshot_digest"], "source byte digest mismatch")
        require(len(data) == pin["bytes"], "source byte length mismatch")
        require(sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == pin["blob_oid"], "source Git blob mismatch")
        sources.append(src)
    outputs = build(sources)
    require(set(p.relative_to(directory).as_posix() for p in (directory / "records").glob("*.json")) ==
            {p for p in outputs if p.startswith("records/")}, "record inventory mismatch")
    for path, expected in outputs.items():
        require((directory / path).read_bytes() == expected, f"immutable record/mapping drift: {path}")
        if path != "migration.json":
            errors = validate(json.loads(expected))
            require(not errors, f"framework validation {path}: {errors}")
    by_ref = {(s["id"], s["revision_id"]): s for s in sources}
    views = {}
    for view in manifest["compatibility"]:
        ref = view["source"]
        data = by_ref[(ref["id"], ref["revision_id"])]["legacy"]["text"].encode()
        views[view["path"]] = data
        if compatibility:
            require((root / view["path"]).read_bytes() == data,
                    f"compatibility drift: {view['path']}; edit by appending an owner record revision, then project")
    # Principia baseline protocol is the original blob plus its clearly dated outcome.
    lookup = {source_key(s): s["legacy"]["text"] for s in sources}
    require(lookup[("principia", BASE, STUDY)].split("## Dated outcome —")[0].rstrip() ==
            lookup[("principia", FREEZE, STUDY)].rstrip(), "historical protocol body changed")
    frozen_digest = digest(lookup[("principia", FREEZE, STUDY)].encode())
    gate_digest = digest(lookup[("principia", FREEZE, GATE)].encode())
    require(frozen_digest == "sha256:50fc37ac41bdbdc0e14ae3c079de3d8ed582d0fb4bf2e740270dc0fd5dfb9443", "wrong original protocol")
    require(gate_digest == "sha256:88609aed585cdbbd18586d5dcbeaf59f691965bbce2536152eabdb1bd51d7a89", "wrong original gate")
    original = json.loads(lookup[("orrery", ORIGINAL, "lab/sims/wide-binary-selection-bias/assets/results.json")])
    diagnostic = json.loads(lookup[("orrery", DIAGNOSIS, "lab/sims/wide-binary-control-diagnosis/assets/results.json")])
    for key, expected in [("principia_commit", FREEZE), ("protocol_sha256", frozen_digest[7:]), ("gate_sha256", gate_digest[7:])]:
        require(original["sources"][key] == expected, "original experiment freeze pin mismatch")
    for key, expected in [("principia_frozen_commit", FREEZE), ("orb_11222_run_commit", ORIGINAL),
                          ("protocol_sha256_at_frozen_commit", frozen_digest[7:]), ("gate_sha256_at_frozen_commit", gate_digest[7:]),
                          ("orb_11222_evidence_sha256", digest(lookup[("orrery", ORIGINAL, "lab/sims/wide-binary-selection-bias/assets/results.json")].encode())[7:]),
                          ("orb_11222_fixture_sha256", digest(lookup[("orrery", ORIGINAL, "lab/sims/wide-binary-selection-bias/main.py")].encode())[7:])]:
        require(diagnostic["sources"][key] == expected, "later diagnostic historical pin mismatch")
    require(original["n_realizations"] == 44 and diagnostic["verdict"]["frozen_verdict_unchanged"] == "unresolved",
            "historical outcome changed")
    return manifest, views


def export(root, destination, views):
    require(not destination.exists(), "export destination must not exist")
    require(not destination.resolve().is_relative_to(root.resolve()), "export outside the checkout")
    destination.mkdir(parents=True)
    for path, data in views.items():
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["migrate", "check", "project", "rollback", "verify-history"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--orrery-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        package_check()
        root = args.root.resolve()
        if args.command == "migrate":
            require(args.orrery_root is not None, "migrate requires --orrery-root")
            require(args.output is not None and not args.output.exists(), "migrate requires a new --output directory")
            require(not args.output.resolve().is_relative_to(root), "migration output must be outside source checkout")
            sources = [snapshot(repo, rev, path, root if repo == "principia" else args.orrery_root)
                       for repo, rev, path in source_spec()]
            outputs = build(sources)
            for path, data in outputs.items():
                target = args.output / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            print(f"migrated {len(sources)} pinned sources into {args.output}")
            return 0
        manifest, views = inspect(root, compatibility=args.command != "project")
        if args.command == "verify-history":
            require(args.orrery_root is not None, "verify-history requires --orrery-root")
            for item in manifest["sources"]:
                repo = root if item["repository"] == "principia" else args.orrery_root
                current = snapshot(item["repository"], item["git_revision"], item["path"], repo)
                require(encoded(current) == (root / AUTHORITY / item["record"]).read_bytes(), "historical source differs")
        elif args.command in {"project", "rollback"}:
            require(args.output is not None, "export requires --output")
            export(root, args.output, views)
        print(f"wide-binary records ok: {len(manifest['records'])} records; {len(views)} exact compatibility views; sibling reconciliation pending")
        return 0
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"wide-binary records: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
