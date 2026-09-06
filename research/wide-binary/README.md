# Wide-binary record authority — ORB-11378

This is the first owning-repository pilot, using **orbit-research 0.1.0 / contract v1**
at `7b6c1b2380bc915d6ff7cca50f288ed716a99c74` (foundation code
`51b117d18f32550dbfca49ce96d2d72474a78b47`; the later revision adds recovery hygiene).
It is not completion of the four-repository migration.

## Authority and scope

The immutable `records/` corpus is the pilot's sole scientific editing authority.
Historical records are append-only: use the framework to create a new revision and
explicitly update the owner mapping in a scoped follow-up; never overwrite an old
record or alter historical source bytes. Native authoring commands are a later framework
milestone. `scripts/wide_binary_records.py` supplies this pilot's mapping; identity,
semantic hashing, validation and reconciliation use the installed framework.

The seven files listed in `migration.json` → `compatibility` remain byte-identical
views of Principia source `13866b2848fbcce9a1f1ef2d4b97051a65f7e626`: the five original
theory files, gate and protocol study. They must not be edited independently. The checker
checks these bytes and the deterministic structured mapping, retaining all existing
policy, ledger, link, expiry, family and refuted-wall checks. The shared parent Gaia study
is an archived reference; its current authority does not change. No other family,
retired/refuted record, gate or rollup changes authority.

`migration.json` contains full Git revisions, blob OIDs, SHA-256 and byte lengths,
stable aliases, record revisions and byte hashes, phase selections, field mappings and
explicit exceptions. `$bytes` retains the entire source. JSON pointers cover every pilot
registry/gate leaf (including empty containers); `text:start:end` partitions every
Markdown character, using Unicode character offsets and exact UTF-8 value digests.
Catalog/result JSON additionally has top-level field accounting; all nested bytes remain
in its source record. Tests compare every accounted value to its source and destination.

`legacy` retains every original field and complete prose, including obsolete wording.
Claims keep exact statements and model domain. `mixed` maps to `inconclusive` only in the
framework verdict; `legacy_verdict` and compatibility statuses remain unchanged. All
assessments are historical, with original evidence scope and failed controls. None is
current primary confirmation. All committed scientific references remain pending.

## Historical sequence

The protocol semantic object conservatively contains the **entire original study,
gate and registry**, preserving every hypothesis, control, threshold, seed, uncertainty
method, assumption, power requirement and crossrepo term. This avoids omitting normative
terms through editorial extraction. Later outcomes are absent from that semantic object.
Presentation edits do not alter identity; edits to the preserved original normative
object require a new semantic revision.

| Stage | Exact source revision | Preserved evidence |
| --- | --- | --- |
| ORB-11221 original protocol | Principia `c04f2ed1ae91d6c126bc60863b5e48f46abe4576` | Study blob `ae7cf43c26fd7bc41c33f4877cd64a499b105633`, SHA-256 `50fc37ac41bdbdc0e14ae3c079de3d8ed582d0fb4bf2e740270dc0fd5dfb9443`, 24073 bytes; gate blob `351510c7f05af85a3c3c922ce5532cd701234636`, SHA-256 `88609aed585cdbbd18586d5dcbeaf59f691965bbce2536152eabdb1bd51d7a89`, 3186 bytes. |
| ORB-11222 frozen run | Orrery `28dd5c72bb670517b93b556f1d2483402c8e8655` | Actual catalog, run report, fixture and results; reported consumed hashes match the original protocol and gate. |
| ORB-11234 source assessment | Principia `f4be1b0c34403a95be57ee2a04d85017219bac57`, retained at pilot baseline `13866b2848fbcce9a1f1ef2d4b97051a65f7e626` | Four mixed claims, oracle supported, dated outcome; then-pending ORB-11241 wording and stale headline retained. |
| ORB-11241 later diagnosis | Orrery `2e097e606bc751ba1a8b29ebdc5aab6bbd961c43` | Separate diagnostic annotations and complete catalog sources; original frozen verdict remains unresolved. |

Recorded commit times are respectively 03:48:46Z, 04:14:50Z, 04:24:41Z and 06:56:59Z
on 2026-09-05. Matching consumption hashes in the actual run and later diagnostic establish
a recoverable historical sequence. Git timestamps and retrospective reports are not
independent external proof of prospective preregistration. The protocol therefore uses
`freeze: historical-unverified`, with no asserted `frozen_at` or `freeze_evidence`.
The original source's own preregistration wording remains archival.

The **47 stated versus 44 enumerated realizations** discrepancy is preserved. No seed,
threshold or control was repaired. Four current claim assessments remain inconclusive
because negative/estimator/power controls failed; candidate-oracle agreement remains
supported only for the enumerated synthetic model regression.

The later diagnosis attributes R0 to protocol arithmetic, R3 to fixture and denominator
defects, and R4 to fixture/decision arithmetic; R1/cap isolation remains undetermined.
It retains the oracle finding. Complete reanalysis and live-probe results stay separate
from the original run, including the deliberately contaminated estimator probe,
reproducible overshoot and shift dependence, and inconclusive mechanism attribution.
Its R3 `positive_control` summary says “shift-insensitive” while detailed D3 and the open
question report shift dependence. Both are preserved and explicitly excepted. This pilot
does not resolve that inconsistency or adopt a stronger scientific verdict.

## Remaining reconciliation gaps

Orrery snapshots are **Principia-owned archival artifacts**, not invented Orrery experiments
or assessments. Their upstream Git/blob/digest pins are in `legacy.source_pin`; owner-ingestion
Git pins are honestly null and marked missing, since these copies did not exist in the
Principia baseline. The original bytes remain runnable under Orrery ownership; these textual
copies make the migration audit portable. No experimental code is imported or executed here.

`pending_reconciliation` lists the two Orrery catalog targets and the catalog-reported
Astrolabe apparatus pin. `legacy_links` retains all Markdown locators as unresolved
scientific links; registry link fields also remain verbatim. Sibling canonical record
IDs/revisions and owner source pins have not been supplied. v1 typed references require
known IDs and revisions, so unknown tuples are explicitly outside the typed manifests,
with null identity fields rather than invented URNs. Two typed Principia manifests
accommodate the freeze and later-source Git revisions separately. Exact in-repository
reconciliation through the package API cannot resolve sibling identities or establish
current confirmation. These are explicit migration gaps, not a new record engine.

## Install and validate in an isolated checkout

Python 3.11+ and Git are required. Keep environments and caches outside the worktree.
The requirements file pins the framework Git commit and runtime dependencies.

```sh
UV_CACHE_DIR=/tmp/principia-research-cache uv venv /tmp/principia-research-env
UV_CACHE_DIR=/tmp/principia-research-cache uv pip install --python /tmp/principia-research-env/bin/python -r requirements-research.txt
export PATH="/tmp/principia-research-env/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/wide_binary_records.py check
python3 -m unittest discover -s scripts -p 'test_wide_binary_records.py' -v
python3 scripts/check-theory.py --external-root orrery=/absolute/path/to/orrery
python3 scripts/check-theory.py --selftest
git diff --check
```

A standard venv and `python -m pip install -r requirements-research.txt` also work.
Installed VCS identity is checked: an unrelated 0.1.0 package or unpinned editable sibling
import is refused. Pilot check/tests need no siblings or historical Git objects; all source
bytes are archived. The whole-corpus checker still needs Orrery for existing link resolution,
using Git worktree discovery or the explicit mapping. No test reruns an experiment.

To verify all source pins against actual historical Git objects, provide an Orrery checkout
containing the pinned commits. This command reads only; it never fetches or writes there:

```sh
python3 scripts/wide_binary_records.py verify-history --orrery-root /absolute/path/to/orrery
```

## Reproduce migration and projections

Choose output paths that do not exist. `migrate` reads fixed historical Git objects,
never current sibling files, and writes a candidate authority outside the source tree.

```sh
python3 scripts/wide_binary_records.py migrate --orrery-root /absolute/path/to/orrery --output /tmp/wide-binary-migration
diff -r research/wide-binary/records /tmp/wide-binary-migration/records
cmp research/wide-binary/migration.json /tmp/wide-binary-migration/migration.json
cmp research/wide-binary/freeze-manifest.json /tmp/wide-binary-migration/freeze-manifest.json
cmp research/wide-binary/source-manifest.json /tmp/wide-binary-migration/source-manifest.json
python3 scripts/wide_binary_records.py project --output /tmp/wide-binary-views
```

`project` validates canonical records before exporting the seven compatibility files.
An independently edited view fails `check`; `project` regenerates authoritative bytes
into a separate directory for explicit restoration. Existing destinations and in-checkout
export targets are refused.

## Rollback

The reversible data migration has an exact inverse:

```sh
python3 scripts/wide_binary_records.py rollback --output /tmp/wide-binary-legacy
```

This validates the authority and exports the seven original files byte-for-byte. Tests
check the complete file set, bytes and overwrite guard. To undo the **authority cutover**
after delivery, run `git revert <ORB-11378-delivery-commit>` on a clean checkout: this
removes the records, dependency and checker/guide additions while preserving original
science files. Run the restored stdlib checker and selftest. Resolve overlap with any
later tasks explicitly. Git history remains intact in either direction. The export
command itself never removes records or silently switches authority.
