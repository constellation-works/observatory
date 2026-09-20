# observatory — agent guide

Cross-provider rules. Claude-specific notes are in [CLAUDE.md](CLAUDE.md).

## What this repository is

The single home for research: the questions, the hypotheses, the runs that test
them, and the theories that survived. It is private and has one owner. The
layout is specified in
[docs/design/research-layout-v2/1_spec.md](docs/design/research-layout-v2/1_spec.md).

Four record kinds, joined by a short id:

| kind | lives at | is |
|---|---|---|
| `Q###` | `questions/Q###-slug.md` | a question worth asking |
| `H###` | `hypotheses/H###-slug.md` | a claim a run can come out against, with an append-only assessment log |
| `R###` | `research/R###-slug/` | one experiment: `README.md`, `code/`, `artifacts/`, `data/`, `output/` |
| `T###` | `theories/T###-slug.md` | what survived, citing the hypotheses it rests on |

Bare directories hold research content or things a person reads
(`questions/`, `hypotheses/`, `theories/`, `research/`, `notebooks/`, `docs/`).
Underscore directories hold apparatus (`_lib/`, `_data/`, `_scripts/`,
`_archive/`). The check gate walks only the four record kinds.

## Boundaries that must hold

1. **The id is allocated once and frozen.** `make new KIND=Q|H|T|R TITLE="..."`
   takes the highest existing id of that kind and adds one. The slug is the
   kebab-case of the title at creation. Never rename a record file or directory
   and never renumber one: a title change edits `title` in the frontmatter, and
   if the slug no longer matches the title, record the frozen slug as `slug:`.
2. **Everything about one research item lives in its directory.** Code, the data
   manifest, outputs, promoted artifacts and the write-up. Do not create a second
   home for an item's material anywhere else in the tree. A run's write footprint
   is one `research/R###-slug/` plus assessment entries appended to the
   hypotheses it `tests` — that is what makes parallel research mergeable.
3. **Bytes never enter git; manifests always do.** `data/` and `output/` are
   ignored everywhere in the tree, and only `manifest.json` and `README.md` may be
   tracked under them. `artifacts/` is the one place a committed figure may live,
   and only when the README cites it. Do not add an exception to `.gitignore` for
   a "small" file. Every research item has a `data/manifest.json`, listing each
   input as `{name, source, sha256, size, fetch}` or as a `shared` pointer to a
   `_data/<name>` manifest; `{"inputs": []}` is the honest manifest for an item
   that consumes nothing.
4. **The README's five sections, in order.** `## Question`, `## Method`,
   `## Result`, `## Limitations`, `## Next`. Extra sections and `###`
   subsections are fine; those five must be present and in that order, so a
   person or an agent can find the same thing in every item.
5. **Assessments are append-only and a person owns the status.** One entry per
   verdict on the hypothesis it bears on: `date`, `research`, the statement
   `revision` it is about, `verdict` (`supports` | `refutes` | `inconclusive`),
   `strength` (`anecdote` | `suggestive` | `strong`), `note`. Never edit or remove
   an entry, and let disagreeing entries coexist. Bump `revision` when the
   statement changes; an assessment against an older revision does not carry.
   The checker warns when `status` disagrees with the latest assessment and never
   overwrites it. **Execution success is not support**: a `done` research item
   with a `refutes` or `inconclusive` assessment is a complete, valid result, and
   recording one is the job.
6. **`_archive/` is frozen.** principia's byte-pinned lock, the retired Nebula
   corpus, orrery, parallax and the retired JSON record chain. Do not edit
   anything under it, do not rewrite principia's ledgers, and do not convert the
   archived records. If a claim the lock owns needs restating, restate it as a new
   hypothesis in the live corpus. `make check-archive` runs the lock's own checker
   over it and is not part of `make check`.
7. **Work material never enters this repository** — not in records, manifests or
   notebooks. Anything that is not research (life, projects, logistics) belongs in
   constellation's almanac, not here. Do not mirror content between the two.

## Working here

- `make check` is the gate: `_scripts/check.py` over the records, then ruff and
  pytest. Run it before handing off. It fails on a duplicate or gapped id, a
  filename that disagrees with its frontmatter, an unresolved reference, a
  missing README section or data manifest, an assessment against a future
  revision, an unknown status, a frontmatter key outside
  [`_scripts/schema.json`](_scripts/schema.json), and tracked bytes under an
  ignored path. It warns on a hypothesis status that disagrees with its latest
  assessment, a `done` item with no assessment on any hypothesis it tests, and a
  `running` item untouched for 30 days.
- `_scripts/schema.json` is the record contract, exported so that whatever writes
  a record — a person, `_scripts/new.sh` or orbit-research — validates against
  the same file the checker reads.
- Notebooks are committed with outputs stripped (`nbstripout`, via the pre-commit
  hook `make setup` installs). A notebook worth keeping is promoted into a
  research item.
- One `pyproject.toml` at the root, managed by `uv`. Per-item dependencies are
  extras, not separate environments, unless the item documents why.
- Sims: a `research/<R>/code/<slug>/` with a `sim.json` appears in the generated
  catalogue (`make gallery`, `make check-gallery`); `make serve` serves the
  repository root so a web sim resolves `../../../../_lib/web/…`. Scaffold one
  with `_lib/tools/new-sim.sh <R-id> <slug> --kind web|py`.
- Orbit: this repository is one workspace. Tag tasks with the domain
  (`physics`, `economics`, `social`, `kaggle`) so drains and reviews can be
  filtered per area. A research item may record the task and run that drove it in
  its `orbit` field; Orbit owns tasks and runs, this repository owns the records.

## Legacy records

Several migrated research items are legacy: one holds 24 sims under `code/<sim>/`
(`R006`), others hold a whole family (`R001`, `R004`, `R008`, `R009`). Splitting
them during migration would have manufactured write-ups nobody wrote. That is
history, not a pattern: a new research item is one question, one run.
