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

## Sims

Physics sims are experiments too: `experiments/physics/<node-id>/<slug>/` with a
`sim.json` (title, kind `web`|`py`, entry, family, summary, provenance). The
shared apparatus is `experiments/physics/_lib/` (web harness, vendored three.js,
templates, tools, gallery). Web sims import it relatively (`../../_lib/web/loop.js`),
run from a static server (`make serve`, then
`http://localhost:8000/experiments/physics/<node>/<slug>/`); py sims run with
`uv run experiments/physics/<node>/<slug>/<entry>` and seed their RNG. Scaffold
with `experiments/physics/_lib/tools/new-sim.sh <node-id> <slug> --kind web|py`,
then `make gallery`. Attach the result to the node with `neb evidence`.

Staging areas (`experiments/physics/_orrery/`, `experiments/economics/_parallax/`)
hold migrated material not yet tied to nodes; `_orrery/lab/sims/` is a symlink
farm that keeps principia's frozen ledger links resolving.
