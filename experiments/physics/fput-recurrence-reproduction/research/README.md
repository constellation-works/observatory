# Scientific records for this experiment

The canonical orbit-research records for this reproduction are **not** in this
directory. The pinned package (`orbit-research 0.2.0`, see the `research` extra in
`pyproject.toml`) refuses any canonical record directory whose path does not begin with
`research/` relative to the owner Git checkout root:

```text
$ uv run orbit-research program --owner-root <checkout> --repository observatory \
    --records experiments/physics/fput-recurrence-reproduction/research/records --request ...
{"error": {"code": "invalid-input",
           "message": "canonical records must live under research/ for exact source discovery"}}
```

The records therefore live at

```text
research/physics/fput-recurrence-reproduction/records/
```

in the repository root, and every command uses:

```sh
uv run orbit-research <operation> \
  --owner-root "$PWD" --repository observatory \
  --records research/physics/fput-recurrence-reproduction/records \
  --request /tmp/<request>.json
```

They are append-only JSON: never edit, rename or delete a numbered record file. The
chain for this experiment is `program → claim → artifact(s) → preregister → begin-run →
record-run → assess`, each append committed before the next one refers to it, because
`orbit-research` resolves references from exact Git snapshots.

`run.py export` copies the records into the evidence package under `research/records/`,
and `run.py evidence --bundle <export.json>` renders the static evidence browser under
`_outputs/physics/fput-recurrence-reproduction/site/evidence/`.
