# _archive

Frozen history. Nothing here is edited, and the check gate skips it.

| path | what it is |
|---|---|
| `principia/` | the theory lock, byte-for-byte: policy, claim registries, gates, ledgers, refuted wall, literature studies and its own checker. `make check-archive` runs that checker over it; `theories/` cites into it. |
| `lineage/` | the retired Nebula corpus verbatim — `config.yaml`, `nodes/`, `inbox/`. Every migrated record cites the node it came from. |
| `orrery/` | the physics-sim repository's research catalogue, scripts and docs. `lab/sims/<slug>` are symlinks into the research items that now hold the sims, so principia's frozen ledger links keep resolving through `--external-root`. |
| `parallax/` | the empirical-research platform, as migrated. |
| `records/fput/` | the orbit-research JSON record chain for the FPUT reproduction. The JSON record format is retired here: these are read, never appended to. |
| `experiments/` | the retired scaffolding of the v1 layout — the experiment template and the per-node `manifest.json` files the record frontmatter replaced. |
| `studies/`, `outputs/`, `scripts/`, `data/` | the v1 study contract, the `_outputs/` convention, `check-layout.sh`, `new-experiment.sh`, and parallax's dataset manifest. |

Why archive rather than delete: refuted and abandoned work is what stops ground
being re-trodden, and a byte-pinned lock cannot be translated into a new schema
without losing the pinning. See
[`docs/design/research-layout-v2/2_decisions.md`](../docs/design/research-layout-v2/2_decisions.md).
