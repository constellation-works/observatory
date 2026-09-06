"""Migration regressions: scientific meaning, completeness, corruption and rollback."""
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

import wide_binary_records as pilot
from orbit_research import protocol_digest, reconcile, validate
from orbit_research.contract import reference, revision_digest


def pointer(value, path):
    for key in path.split("/")[1:]:
        key = key.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.views = pilot.inspect(pilot.ROOT)
        cls.records = [json.loads((pilot.ROOT / pilot.AUTHORITY / item["path"]).read_text())
                       for item in cls.manifest["records"]]
        cls.by_ref = {(r["id"], r["revision_id"]): r for r in cls.records}
        cls.sources = [r for r in cls.records if r["kind"] == "artifact"]

    def record(self, ref):
        return self.by_ref[(ref["id"], ref["revision_id"])]

    def test_all_records_use_owner_framework_and_exact_refs(self):
        pilot.package_check()
        self.assertEqual(len(self.sources), 21)
        for record in self.records:
            self.assertTrue(record["id"].startswith("urn:research:principia:"))
            self.assertEqual(validate(record), [])
        for phase in self.manifest["phases"].values():
            for ref in phase.get("assessments", []):
                assessment = self.record(ref)
                targets = [self.record(assessment["payload"]["claim"])]
                targets += [self.record(r) for r in assessment["payload"]["evidence"]]
                self.assertEqual(validate(assessment, targets=targets), [])

    def test_all_accounted_values_equal_exact_source_and_target(self):
        for item in self.manifest["accounting"]:
            source_text = self.record(item["source"])["legacy"]["text"]
            selector = item["selector"]
            if selector.startswith("text:"):
                _, a, b = selector.split(":")
                value = source_text[int(a):int(b)]
            elif selector in ("$bytes", "$text"):
                value = source_text
            else:
                value = pointer(json.loads(source_text), selector)
            self.assertEqual(item["value_digest"], pilot.digest(pilot.encoded(value)))
            target = pointer(self.record(item["target"]), item["pointer"])
            if item.get("decode") == "json":
                target = pointer(json.loads(target), selector)
            elif selector.startswith("text:"):
                target = target[int(a):int(b)]
            self.assertEqual(value, target, item["selector"])

    def test_json_leaves_and_all_prose_characters_covered(self):
        for source in self.sources:
            pin = source["legacy"]["source_pin"]
            entries = [i for i in self.manifest["accounting"] if i["source"] == reference(source)]
            self.assertIn("$bytes", {i["selector"] for i in entries})
            if pin["repository"] == "principia" and pin["path"] in (pilot.CLAIMS, pilot.GATE):
                self.assertTrue({p for p, v in pilot.leaves(json.loads(source["legacy"]["text"]))}
                                <= {i["selector"] for i in entries})
            if pin["path"].endswith(".md"):
                spans = [list(map(int, i["selector"].split(":")[1:])) for i in entries if i["selector"].startswith("text:")]
                self.assertEqual(spans[0][0], 0)
                self.assertEqual(spans[-1][1], len(source["legacy"]["text"]))
                self.assertTrue(all(a[1] == b[0] for a, b in zip(spans, spans[1:])))

    def test_freeze_separate_from_outcomes_and_arithmetic_not_repaired(self):
        protocol = self.record(self.manifest["protocol"])
        semantic = protocol["payload"]["semantic"]
        self.assertEqual(protocol["payload"]["freeze"], "historical-unverified")
        self.assertIsNone(protocol["payload"]["frozen_at"])
        self.assertIsNone(protocol["payload"]["freeze_evidence"])
        self.assertNotIn("## Dated outcome", semantic["protocol_text"])
        self.assertIn("47 total realizations", semantic["protocol_text"])
        rows = [line for line in semantic["protocol_text"].splitlines() if re.match(r"\| R\d", line)]
        self.assertEqual(len(rows), 12)
        self.assertEqual(sum(int(line.split("|")[-2]) for line in rows), 44)
        self.assertEqual({c["status"] for c in semantic["registry"]["claims"]}, {"untested"})
        changed = deepcopy(semantic)
        changed["protocol_text"] = changed["protocol_text"].replace("47 total realizations", "44 total realizations")
        self.assertNotEqual(protocol_digest(changed), protocol["revision_id"])
        moved = deepcopy(protocol)
        moved["presentation"] = {"title": "Presentation edit"}
        self.assertEqual(validate(moved), [])

    def test_historical_verdicts_and_diagnostic_annotation_not_promoted(self):
        for phase in ("original-outcome", "later-diagnostic-annotation"):
            assessments = [self.record(r) for r in self.manifest["phases"][phase]["assessments"]]
            self.assertEqual([a["payload"]["verdict"] for a in assessments], ["inconclusive"] * 4 + ["supported"])
            self.assertEqual([a["payload"]["controls"] for a in assessments], ["failed"] * 4 + ["passed"])
            for assessment in assessments:
                self.assertEqual(assessment["scope"], "synthetic-calibration")
                self.assertEqual(assessment["payload"]["inference"], "historical")
        self.assertIn("ORB-11241 owns diagnosis", self.views[pilot.CLAIMS].decode())
        self.assertIn("not yet run", self.views[pilot.CLAIMS].decode())
        self.assertIn("diagnostic-internal-shift-discrepancy", {e["id"] for e in self.manifest["exceptions"]})

    def test_framework_rejects_strengthening_and_failed_control_confirmation(self):
        assessment = deepcopy(self.record(self.manifest["phases"]["original-outcome"]["assessments"][0]))
        assessment["payload"]["verdict"] = "supported"
        assessment["revision_id"] = revision_digest(assessment)
        self.assertIn("historical verdict was strengthened or changed", validate(assessment))
        assessment["provenance"]["historical"] = False
        assessment["payload"]["inference"] = "confirmatory-primary"
        assessment["payload"]["basis"] = "scientific-evidence"
        assessment["revision_id"] = revision_digest(assessment)
        self.assertIn("confirmatory primary inference requires passing controls", validate(assessment))
        self.assertIn("pending references cannot be current confirmatory evidence", validate(assessment))

    def test_pending_owner_links_not_fabricated_or_silently_resolved(self):
        for ref in self.manifest["pending_reconciliation"]:
            self.assertEqual(ref["status"], "pending")
            self.assertIsNone(ref["id"])
            self.assertIsNone(ref["revision_id"])
        for name in self.manifest["framework_manifests"].values():
            manifest = json.loads((pilot.ROOT / pilot.AUTHORITY / name).read_text())
            self.assertTrue(all(r["status"] == "pending" for r in manifest["references"]))
            self.assertEqual(validate(manifest), [])
            resolved = reconcile(manifest, self.records)
            self.assertEqual(validate(resolved, targets=self.records), [])
            self.assertTrue(all(r["status"] == "resolved" for r in resolved["references"]))
            wrong = deepcopy(self.records)
            for r in wrong:
                r["provenance"]["git_revision"] = "0" * 40
            self.assertTrue(all(r["status"] == "pending" for r in reconcile(manifest, wrong)["references"]))

    def test_projection_and_rollback_roundtrip_and_overwrite_guard(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "legacy"
            pilot.export(pilot.ROOT, target, self.views)
            self.assertEqual({p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}, self.views)
            with self.assertRaisesRegex(ValueError, "must not exist"):
                pilot.export(pilot.ROOT, target, self.views)

    def test_corruption_and_view_drift_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(pilot.ROOT / pilot.AUTHORITY, root / pilot.AUTHORITY)
            for path, data in self.views.items():
                p = root / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
            (root / pilot.CLAIMS).write_bytes(self.views[pilot.CLAIMS] + b"\n")
            with self.assertRaisesRegex(ValueError, "compatibility drift"):
                pilot.inspect(root)
            (root / pilot.CLAIMS).write_bytes(self.views[pilot.CLAIMS])
            file = root / pilot.AUTHORITY / self.manifest["records"][-1]["path"]
            record = json.loads(file.read_text())
            record["provenance"]["selector"] = "/wrong-pin"
            file.write_bytes(pilot.encoded(record))
            with self.assertRaisesRegex(ValueError, "immutable record/mapping drift"):
                pilot.inspect(root)


if __name__ == "__main__":
    unittest.main()
