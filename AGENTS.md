# observatory — agent guide

Cross-provider rules. Claude-specific notes are in [CLAUDE.md](CLAUDE.md).

## What this repository is

The single home for research: the idea ledger, experiments, study notes and
theory. It is private. It holds the **personal** nebula corpus under
`knowledgebase/lineage/`; the work corpus is a different corpus elsewhere and
never comes here.

## Boundaries that must hold

1. **Data and outputs never enter git.** `_data/` and `_outputs/` are ignored
   except for `manifest.json` and `README.md` files. An experiment that needs a
   dataset writes a manifest (source, hash, size, fetch command); a result that
   matters is promoted into `knowledgebase/studies/` as a note with its figure.
   Do not add exceptions to `.gitignore` for a "small" file.
2. **Every experiment is keyed by a nebula node.** `experiments/<domain>/<id>/`
   where `<id>` is the node id from `neb show`. No experiment without a node;
   capture the idea first, promote it, then scaffold. Kaggle competitions are
   projects under the `kaggle` domain and are the one exception: their id is
   the competition slug, and the node that tracks the competition names it.
   Underscore-prefixed directories are never experiments: `_lib` is shared
   apparatus, `_orrery` and `_parallax` are migration staging areas, exempt until
   their material is tied to nodes.
3. **Studies are filed under the same id.** `knowledgebase/studies/<domain>/<id>.md`.
   A study without an experiment directory, or an experiment without a study
   once it has run, is a `make check` finding.
4. **The theory lock stays locked.** `knowledgebase/theory/` carries principia's
   `policy.md`, claim registries, gates and refuted wall, checked by
   `_scripts/check-theory.sh`. Reopening a refuted claim, or filing a
   phenomenology card on a family whose existence claim is open, is refused
   there for reasons that still apply. Read `knowledgebase/theory/policy.md`
   before touching it.
5. **The almanac is not here.** `knowledgebase/almanac` in constellation stays
   the personal vault for everything that is not research. If a note is about
   an idea under test, it belongs here; if it is about life, projects or
   logistics, it belongs there. Do not mirror content between the two.
6. **Ranking-signals and other work material never enters this repository**, in
   nodes, studies, data manifests or notebooks.

## Working here

- `make check` is the gate: `neb check` on the corpus, the theory checker, ruff,
  pytest. Run it before handing off.
- Notebooks are committed with outputs stripped (`nbstripout` via the pre-commit
  hook `make setup` installs). Heavy outputs go to `_outputs/`.
- One `pyproject.toml` at the root, managed by `uv`. Per-experiment dependencies
  are extras, not separate environments, unless an experiment documents why.
- Orbit: this repository is one workspace. Tag tasks with the domain
  (`physics`, `economics`, `social`, `kaggle`) so drains and reviews can be
  filtered per area.
- Record provenance: `neb evidence --task <id>` and `neb new --task <id>` when
  an Orbit task produced the node or the finding.

## Migration status

orrery, principia, parallax and kaggle are being folded in with their git
history via `git subtree add`. Until [docs/runbooks/migration.md](docs/runbooks/migration.md)
marks a source as landed, its original repository remains authoritative.
