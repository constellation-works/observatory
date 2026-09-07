# experiments

One directory per idea under test: `experiments/<domain>/<node-id>/`. The id is
the nebula node the experiment exists to settle, which is what lets you go from
a node to its experiment to its study and back without a search.

Scaffold with `make experiment DOMAIN=physics ID=<node-id>`. The scaffold
refuses an id that is not a node, because an experiment that tests nothing
named is how results end up orphaned.

Each directory holds:

- `README.md` — what is being tested, the kill condition copied from the node,
  how to run it.
- `manifest.json` — the node, the data it depends on (by manifest path), the
  outputs it produces, and the study it feeds.
- code and notebooks. Notebooks are committed with outputs stripped.

Domains match the corpus config: `physics`, `economics`, `social`, `kaggle`,
`general`. Kaggle competitions are projects, so `experiments/kaggle/<slug>/`
uses the competition slug as the id and the node that tracks the competition
names it in its references.

Orrery's simulations arrive under `experiments/physics/`, parallax's studies
under `experiments/economics/`, and the kaggle workspace under
`experiments/kaggle/`, each keeping its git history.
