# observatory

The single research knowledgebase: the questions, the claims, the runs that test
them, and the accounts that survived. Private, one owner.

## The five rules

1. **The id is the join key.** `Q###`, `H###`, `T###`, `R###` — three digits,
   zero-padded, monotonic per kind, allocated by `make new`. The slug is the
   kebab-case of the title at creation and is frozen. A file is never renamed; a
   title change edits the frontmatter.
2. **Three kinds are flat files, one kind is a directory.** Questions, hypotheses
   and theories produce no code, so they are single markdown files. Research is
   the only kind that produces code and outputs, so it is the only kind with a
   directory. There is no other layering.
3. **Everything about R001 lives in R001.** Code, data manifest, outputs,
   promoted artifacts and the write-up. One experiment, one directory — which is
   what makes many research agents mergeable.
4. **Links are frontmatter, not directory structure.** `derived_from`, `tests`,
   `supports`, `tags`. Projects and subjects are tags, because projects go stale
   and directories cannot.
5. **Bytes are never committed, manifests always are.** `data/` and `output/` are
   ignored everywhere. `artifacts/` is the one place a committed figure may live,
   and only when the README cites it.

## Layout

```
questions/     Q001-slug.md   capture inbox; one question per file
hypotheses/    H001-slug.md   precise claim; append-only assessment log
theories/      T001-slug.md   what survived; cites H and R ids
research/      R001-slug/     the only directory kind: one per experiment
                 README.md      Question, Method, Result, Limitations, Next — in that order
                 code/          the scripts that produced the result
                 artifacts/     promoted figures the README cites (committed, small)
                 data/          inputs (ignored; data/manifest.json committed)
                 output/        raw run products (ignored)
notebooks/     free-form exploration; outputs stripped on commit
docs/          design records, runbooks, and the physics field guide
_lib/          shared apparatus: astrolabe, the browser sim harness, the gallery
_data/         datasets shared across research items (ignored; manifests committed)
_scripts/      check, new, the archive checker, the field-guide export
_archive/      frozen history: principia's lock, the retired Nebula corpus, orrery, parallax
```

Bare directories hold research content or things a person reads. Underscore
directories hold apparatus. The gate walks only the four record kinds.

## The flow

```
questions/Q001  →  hypotheses/H001  →  research/R001-slug/  →  assessment on H001  →  theories/T001
   (worth asking)    (a claim a run can refute)   (test it)       (what it showed)      (what survived)
```

An assessment is an entry appended to the hypothesis's frontmatter: date,
research id, statement revision, verdict, strength, note. Entries are never
edited, disagreeing entries coexist, and `status` stays a person's call.
Execution success is not support — a `done` research item with an `inconclusive`
verdict is a complete result.

## Getting started

```sh
make setup                            # uv sync and the pre-commit hook
make check                            # the gate: records, ruff, tests
make new KIND=Q TITLE="Does X hold"   # allocate the next id and scaffold
make new KIND=R TITLE="X under Y"
make serve                            # static server for the sims and field-guide chapters
```

`make check-archive` runs principia's own checker over the frozen lock in
`_archive/principia/`. It is deliberately not part of `make check`: the gate stays
fast and the archive stays untouched.

See [docs/runbooks](docs/runbooks) for the daily loop and
[docs/design/research-layout-v2](docs/design/research-layout-v2) for why it is
shaped this way.
