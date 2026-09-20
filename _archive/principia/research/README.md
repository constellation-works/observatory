# Principia scientific record owner — ORB-11394

All ten theory programs, 121 claims, four gates, 19 study notes, the refuted wall,
chapters and ledgers now have one declared editing authority: immutable owner records,
selected explicitly by [active.json](active.json). The original 110 scientific files are
generated/checked views. This migration changes no statement, verdict, scientific scope,
retirement, gate term, citation or experiment. The [migration report](migration-report.md)
and [machine comparison](corpus/equivalence.json) record the boundary and remaining gaps.

`corpus/records/` contains deterministic historical v1 imports. All 48 original
`wide-binary/records/` objects and the pilot manifests retain their exact bytes and IDs.
New authoring uses **orbit-research 0.2.0**, record schema v2, pinned to
`0a9cf756e1c2522b9d5ee71c1cf462b8676f4281`. The framework owns identity, semantic hashes,
validation, appends, idempotency, concurrency, trace and export. The owner adapter owns
only field mapping, selection, compatibility projection and Principia's existing policy.
No second record engine, simulation runner or sibling write is introduced.

## Install and check a separate checkout

Python 3.11+, Git and the exact requirements are required. Environments and caches belong
outside the checkout. An absolute Orrery checkout containing the pinned history is needed
for historical verification and existing crossrepo links; record checks and the archived
sources themselves remain readable without it.

```sh
UV_CACHE_DIR=/tmp/principia-research-cache uv venv /tmp/principia-research-env
UV_CACHE_DIR=/tmp/principia-research-cache uv pip install --python /tmp/principia-research-env/bin/python -r requirements-research.txt
export PATH="/tmp/principia-research-env/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/corpus_records.py check
python3 scripts/wide_binary_records.py check
python3 -m unittest discover -s scripts -p 'test_*records.py' -v
python3 scripts/check-theory.py --external-root orrery=<observatory>/experiments/physics/_orrery
python3 scripts/check-theory.py --selftest
python3 scripts/corpus_records.py verify-history --orrery-root <observatory>/experiments/physics/_orrery
python3 scripts/wide_binary_records.py verify-history --orrery-root <observatory>/experiments/physics/_orrery
orbit-research validate research/corpus/source-manifest.json
orbit-research validate research/corpus/archival-manifest.json
git diff --check
```

A standard venv plus `python -m pip install -r requirements-research.txt` also works.
The VCS install identity is checked; an unpinned editable sibling is refused. Nothing
fetches, updates or runs Orrery during validation. The existing link resolver uses Git
worktree metadata or the explicit `--external-root` mapping. Missing sibling paths remain
errors, distinct from unknown scientific identity/consumption, which remains pending.

## Field ownership

| Field | Selected authority | Compatibility behavior |
| --- | --- | --- |
| Claim statement, model/nature domain and postulate role | `programs[slug].claims[i]` exact claim record | Registry and matching table statement generated together; kind/domain must agree. |
| Individual verdict and registry evidence rationale | `programs[slug].assessments[i]` exact assessment of that claim revision | Original five verdict strings retained; native inconclusive maps to mixed. No historical assessment is overwritten. |
| Program title, native question and administrative state | `programs[slug].program` | Native question generates the registry headline; title/status and hub fields are generated together. Refuted remains paused activity plus refuted document status; retired/resolved stay independent of individual verdicts. |
| Family, dates, kill, comparator, blocked obligations, tags, control flags and other retained registry metadata | Selected registry source artifact | Every original leaf has an exact source selector and destination in `corpus/migration.json`. Historical core fields in this artifact are archival; the typed selections above override them. |
| Prose, frontmatter not derived above, historical evidence-table commentary | Selected source artifact for that path | Exact bytes preserved until an explicit replacement artifact is selected. A changed typed rationale updates its corresponding table evidence cell. |
| Gate/protocol terms and wall membership | Historical protocol selection and source artifacts | Complete terms stay frozen; gate or wall changes require a separately reviewed owner mapping, never an implicit newest-record selection. |
| `ledger.md` | Existing policy renderer over projected registries/gates/wall | Entire rollup regenerated; original rollup bytes remain archived. |

The owner checks all historical mappings against their immutable sources, so duplicate
historical representations are not independent editable sources. Prose outside structured
fields remains an argument owned by its source artifact. Editing a view directly fails.
The four directory/policy guides are workflow documentation; their baseline versions are
archived but their current prose is not a scientific compatibility view.

The adapter retains all original scientific identities and the current gate inventory.
Adding a program, claim or protocol mapping is a separately scoped owner change under
`policy.md`, not permission supplied by the migration. Retired/refuted/resolved programs,
their rows, closed gates and the wall cannot be reopened through activation. Daniel's
explicit authorization and a reviewed policy/mapping change are still required.

## Native authoring and explicit activation

Use the installed package workflow (`orbit-research resource --version 1`) and its
`docs/native-workflow.md` at the pinned package commit. Do not convert old records to v2
or enter an old freeze date: native registration is observed now, while old v1 history
remains historical. New work still requires its authorized gate/task; experiments belong
to Orrery. The following operations describe authoring, not a new scientific assignment.

1. Obtain the actual assigned Orbit host/workspace/task/run and persist the plan there.
   Build a request JSON outside the checkout. Use the existing legacy alias for a revised
   claim. `expected_heads: []` is correct for its first **native** revision: the v1 object
   is not a native append-chain head. Retain an explicit reference to the old owner object
   and a reason. Later requests use the exact complete `heads` result, including conflicts.
2. Append using the installed CLI. It returns the canonical record and never changes a
   compatibility view or active selection:

   ```sh
   orbit-research heads --owner-root "$PWD" --repository principia --id 'urn:research:principia:claim:EXISTING-ALIAS'
   orbit-research claim --owner-root "$PWD" --repository principia --request /tmp/claim-request.json > /tmp/claim-record.json
   orbit-research assess --owner-root "$PWD" --repository principia --request /tmp/assessment-request.json > /tmp/assessment-record.json
   ```

   A claim payload is `{"role":"claim","statement":"exact statement","domain":"model"}`.
   The request also requires `request_id`, `id`, `scope`, `reason`, `expected_heads` and
   `orbit_links` (each with actual `host`, `workspace`, `task`, `run`). An assessment must
   reference the exact claim revision, record controls and evidence honestly, and supply
   `evidence_summary`; the packaged example/schema defines the complete request. Unknown
   upstream IDs remain missing, never fabricated. A historical assessment is not promoted
   by appending a newer record, and a model result cannot become a nature verdict.
3. For retained metadata or prose, save the revised UTF-8 content once under
   `research/content/<SHA256>.<extension>`, then append a native **source artifact** with
   its exact `snapshot_digest`, that relative `locator`, `availability: "available"`,
   `role: "source"` and MIME type. Use `orbit-research artifact` with the same required
   request envelope and historical reference. The owner verifies bytes and refuses
   symlinks or paths outside `research/content/`. Do not hide normative content in the
   framework's presentation field. Its scientific content digest must cover those bytes.
4. Copy `research/active.json` to `/tmp/active-candidate.json`. Replace only the affected
   source/claim/assessment slots with `orbit_research.contract.reference(record)` from
   the returned canonical JSON. These owner-local selectors deliberately remain pending
   references with the record's author-time provenance; selection is not publication or
   scientific reconciliation. Keep every ID and every unaffected selection. A revised
   claim needs a matching assessment of that exact revision; an old assessment cannot
   silently adjudicate the revised statement.
5. Generate a candidate and run the retained scientific policy before copying anything:

   ```sh
   python3 scripts/corpus_records.py project --active /tmp/active-candidate.json --output /tmp/principia-candidate --orrery-root <observatory>/experiments/physics/_orrery
   ```

   The output directory must not exist and must be outside the checkout. Review the
   candidate diff, copy its files to their original paths and adopt the candidate
   `active.json` in the same change. Run the checks above. An append that is not selected
   remains history, not an automatically accepted verdict. Selection may be incremental,
   one program/claim/source at a time, provided the projected whole corpus passes policy.
6. Publish through the repository's authorized delivery workflow. The framework never
   commits or pushes. After publication, use `orbit-research ref` for a native record with
   the actual full delivery commit and use `trace`/`export` for its exact closure. These
   published references are distinct from the internal activation selectors. For v1
   archival records, a consumer can resolve their ID/revision at the actual owner delivery
   commit using `Owner.resolve`; their retained original source provenance stays intact.
   Unknown sibling tuples remain pending until exact owner manifests are supplied.

The tests `test_native_source_activation_and_rollback_preserve_all_appends` and
`test_native_claim_and_assessment_generate_both_views` execute runnable examples in fresh
temporary Git owners using the installed package. They author only fixture records,
exercise idempotency, select exact revisions, generate both views, and retain all appends
after rollback. They never modify this corpus or run a simulation.

## Reproduction and rollback

Migration reads fixed source commits, never a sibling's current working files:

```sh
python3 scripts/corpus_records.py migrate --orrery-root <observatory>/experiments/physics/_orrery --output /tmp/principia-migration
diff -r research/corpus /tmp/principia-migration/research/corpus
cmp research/active.json /tmp/principia-migration/research/active.json
python3 scripts/corpus_records.py project --output /tmp/principia-selected --orrery-root <observatory>/experiments/physics/_orrery
python3 scripts/corpus_records.py rollback --output /tmp/principia-baseline --orrery-root <observatory>/experiments/physics/_orrery
```

`rollback` exports all 110 original scientific files, regardless of later native
selections. It deletes nothing: v1 history, every v2 append, evidence/content bytes and
the current activation all remain untouched. For an actual authority rollback, retain
the current activation as an audit artifact, select the baseline `active.json` from the
reproduction output, and copy the baseline views in one reviewed change. Run the checks.
Do **not** revert away `research/` after new records have arrived. A prior activation
can likewise be restored while keeping subsequent immutable revisions.

To inspect the former source-only workflow without touching the owner checkout, export
baseline views and obtain the pre-pilot checker at the foundation pin. Restore the
archived policy guide alongside the scientific views so its existing study link resolves:

```sh
git show 13866b2848fbcce9a1f1ef2d4b97051a65f7e626:scripts/check-theory.py > /tmp/check-theory-source.py
git show 4e3b02c59b694d85016915177ef1ae157895ed7b:policy.md > /tmp/principia-baseline/policy.md
python3 /tmp/check-theory-source.py --root /tmp/principia-baseline --external-root orrery=<observatory>/experiments/physics/_orrery
python3 /tmp/check-theory-source.py --selftest
```

The executable compatibility oracle in `test_policy_behavior_survives_on_projected_records`
loads projected sources through the same stdlib policy functions, independent of record
schema validation. Native verdicts without a faithful five-status projection (such as
`conditional`) fail activation until a separately reviewed mapping is supplied; conditional
historical claim statements and their original verdicts remain unchanged. The current `check-theory.py --selftest` retains the old fixtures.
The original pilot reproduction/export commands remain in [wide-binary/README.md](wide-binary/README.md);
its `check` means original-source compatibility, while the full owner checker honors
new explicit selections.
