# _scripts

Shared tooling. Nothing here is domain-specific.

| script | role |
|---|---|
| `check-layout.sh` | experiments and studies keyed by node id; no data or outputs tracked. Underscore-prefixed ids (`physics/_orrery`) are migration staging areas and are exempt |
| `new-experiment.sh` | scaffold `experiments/<domain>/<id>/` from `experiments/_template/` |
| `check-theory.sh` | principia's lock, unchanged, run over `knowledgebase/theory` with the orrery root wired |
