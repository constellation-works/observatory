# observatory — Claude-specific guide

Read [AGENTS.md](AGENTS.md) first; the boundaries there are the whole point of
this repository and are easy to violate by accident.

Two that bite most often: never commit anything under `_data/` or `_outputs/`
except a manifest or README, and never create an experiment directory without a
nebula node id to name it. `make check` catches both.

The nebula CLI is `neb`, pointed at `knowledgebase/lineage/` by `make setup`
(`NEBULA_ROOT`). If a command says "no corpus", the variable is unset in this
shell, not the corpus missing.
