# _scripts

Shared tooling. Nothing here is domain-specific.

| script | role |
|---|---|
| `check.py` | the gate: record frontmatter against `schema.json`, id allocation, every cross-reference, the required README sections, and no tracked bytes under an ignored path. `make check` |
| `schema.json` | the record contract, exported so orbit-research validates against the same file the checker reads |
| `new.sh` | allocate the next id of a kind and scaffold a valid record. `make new KIND=R TITLE="..."` |
| `check-theory.sh` | principia's own checker, unchanged, run over the frozen `_archive/principia/`. `make check-archive`, never part of `make check` |
| `export-field-guide.sh` | rebuild the shareable field-guide tree from an explicit allowlist, into the ignored `output/` |
