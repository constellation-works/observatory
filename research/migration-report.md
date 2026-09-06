# Full-corpus preservation report — ORB-11394

The scientific cutover is pinned to Principia
`4e3b02c59b694d85016915177ef1ae157895ed7b`, the delivered pilot commit. Direct comparisons
against foundation source `13866b2848fbcce9a1f1ef2d4b97051a65f7e626` find **no differences
in any of the 110 scientific views**. The earlier inventory's ten programs and 121 claims
remain ten and 121; its four gates remain four. Additional source coverage includes all
19 studies, schema documents/wall and policy guides rather than only the protocol study.

| Preserved object | Count / disposition |
| --- | --- |
| Current claim verdicts | 45 supported, 26 mixed, 23 refuted, 18 untested, 9 conjecture |
| Administrative program state | Four retired, two refuted, two resolved, two exploratory |
| Live research fronts | Existing two only: two-substance photon sector and wide-binary selection control |
| Immortal wall | All 18 original IDs retained, each still refuted |
| Source snapshots | 114 Principia files and 75 Orrery metadata files |
| New historical v1 records | 433: 189 sources, nine programs, 116 claims, 116 assessments, three protocols |
| Original pilot objects | All 48 unchanged; current wide-binary selections reuse its program, five claims, five original-outcome assessments and original protocol |
| Compatibility views | 110 exact files; complete baseline rollback reproduces each byte |
| Field accounting | 4,104 located entries; each owned JSON leaf and every prose section, plus whole-source bytes and upstream JSON subtrees |

The four retired programs are gravity-as-scarcity, shear-sourced-consumption,
moving-sources-in-the-closed-system and ppn-reduction-of-the-settled-flow. Retirement
does not turn their surviving supported/mixed/untested statements into refutations.
Refuted branches retain paused administrative activity and their refuted document state.
Resolved programs retain resolved activity. All eight closed programs have empty live
fronts, and activation cannot reopen them or change their scientific rows.

Every source has a full Git commit, blob OID, SHA-256, byte length and retained raw commit
object. The mapping records exact JSON pointers or Unicode text spans and value digests.
Fields without a more specific typed meaning remain at a specifically named pointer in
the retained source; no catch-all unexplained exception removes them. Exact claim text,
family, kind, scope qualifiers, kill, control, comparator, evidence, expiry, postulate
names, tags, blocked obligations, frontmatter and historical rationale all survive.

Historical imports remain schema v1; they are not newly registered v2 science. Derived
claims retain derivation scope, nature/model domain follows the original kind, and
unestablished finer scope/controls remains explicitly unknown. Conditional findings are
not generalized: the original claim/evidence/prose carries its full assumptions. Mixed
maps to framework inconclusive and conjecture to untested while the exact original
verdict string remains in `legacy_verdict` and every view. No assessment becomes current
primary confirmation. The wide-binary failed controls, 47-versus-44 discrepancy, oracle
limitation, diagnostic disagreement and historical-unverified freeze remain unchanged.

The other three protocol records include complete historical gate terms and explicitly
linked normative chapters. They assert no prospective chronology and do not reclassify
closure reports as run receipts. Changing any semantic term changes its protocol digest.
Gate activation is held to those historical terms; a later protocol requires its own
reviewed owner mapping and scientific authorization.

## Explicit evidence gaps

Orrery metadata was inventoried read-only at
`a1c430db54d585048ec85c4e7c47141db634f398`, covering all JSON/Markdown metadata in the 27
sim directories linked by the source corpus. These are Principia archival source copies,
not Orrery-owned experiment/assessment records. The inventory pin is **not a claim that
historical runs consumed those exact bytes**. Each of the 75 entries explicitly has
`consumed_revision: null`, unknown canonical identity/revision, and pending reconciliation.
Historical short/full revisions written in the original prose remain verbatim; the
migration makes no guessed identity or chronology from them.

Together with the pilot's two exact historical Orrery catalog targets and its
catalog-reported Astrolabe apparatus pin, there are 78 explicit pending reconciliation
entries. Their source bytes can be audited here. Principia owner-ingestion Git pins for
external copies remain null/working-tree in the historical record rather than inventing
an earlier owner commit. Typed source and archival manifests validate that missingness.

All registry and Markdown locators retain source selectors; known local targets also
link to retained source artifacts. A local path resolving is not scientific reconciliation.
Literature citations remain exactly as sourced in their original study notes; this task
neither reinterprets nor freshly verifies the literature and fabricates no article records.
Unrecorded upstream run/input lineage, absent datasets, unverified finer control scope
and missing sibling canonical manifests remain unknown. The pilot's missing-input and
failed-calibration limits remain binding. **Global reconciliation is not claimed.**

## Equivalence, policy and rollback evidence

`corpus/equivalence.json` and `corpus/migration.json` are deterministic outputs checked
against immutable source records. Tests compare all 110 views to both exact Git pins,
every individual claim and verdict to its row, every accounted value to its source and
destination, and every source span to complete coverage. The installed framework validates
all 433 added and 48 retained records plus typed manifests. Original pilot tests retain
their freeze, failed-control, pending-reference and corruption coverage.

The original checker continues to run on every view. Its full selftest remains in place;
additional projected-corpus mutations exercise retirement, family mismatch, missing links,
wall disappearance, supported/expired postulates and failed hook controls. Native fixture
appends demonstrate exact claim/assessment and prose selection, coupled table generation,
idempotent retry, digest corruption rejection and rollback retaining later history.
Export rejects existing destinations and never writes to siblings. See the runnable
[validation and rollback workflow](README.md).

Historical-source verification now canonicalizes only the two Git ISO timestamp fields'
UTC `Z`/`+00:00` spelling before reconstruction/comparison. Archived objects and revision
IDs are never rewritten. Tests cover both archive spellings, unchanged Linux reconstruction,
subjects ending in `Z`, actual timestamp/offset/subject changes, changed Git pins/source
bytes and invalid derived identities. Full new sources additionally retain and hash-check
the actual raw Git commit object. This repairs the reported Apple Git portability failure
without weakening byte or commit integrity.
