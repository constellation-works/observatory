# observatory

One place where research happens: the idea ledger, the experiments that test
ideas, the notes that record what was found, and the theory that survived.

It replaces the scatter of orrery (physics sims), principia (theory corpus),
parallax (empirical research platform) and the kaggle workspace. Those were
split by topic, and topic splits are what make ideas get lost. Everything here
belongs to one owner, so it is partitioned by *view* inside one repository,
the same way [nebula](../nebula) partitions one corpus into domains.

## Layout

```
_data/          datasets. Never in git; a manifest per experiment says how to fetch.
_outputs/       run products. Never in git; what matters is promoted to a study.
_scripts/       shared tooling: checks, scaffolding, fetchers.
knowledgebase/
  lineage/      the nebula corpus: config.yaml, nodes/, inbox/
  studies/      one note per experiment result, <domain>/<node-id>.md
  theory/       essays, claims, gates, refuted wall (principia's lock, kept)
experiments/
  <domain>/<node-id>/   one directory per idea under test, keyed by its node
  kaggle/<competition>/ competitions are projects inside the kaggle domain
docs/           design and runbooks, Orbit conventions
```

## The flow

```
neb capture  →  neb promote/sharpen  →  experiments/<domain>/<id>/  →  studies/<domain>/<id>.md  →  theory/
  (idea)          (hypothesis, kill)      (test it)                      (what we found)              (what survived)
```

The join key throughout is the nebula node id. `neb show <id>` names the
experiment directory; the experiment's manifest names the node; the study is
filed under the same id; `neb evidence --source studies/<domain>/<id>.md` is a
relative path the checker verifies exists.

## Getting started

```sh
make setup            # uv sync, neb pointed at knowledgebase/lineage
make check            # lineage invariants, theory lock, lint, tests
make experiment DOMAIN=physics ID=<node-id>   # scaffold from the template
```

See [docs/runbooks](docs/runbooks) for the daily loop and
[docs/design/unified-research-platform](docs/design/unified-research-platform)
for why it is shaped this way.
