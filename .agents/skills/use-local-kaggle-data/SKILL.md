---
name: use-local-kaggle-data
description: Discover, assess, and consume versioned local Kaggle datasets from Parallax with the `datasets` CLI. Use when an agent needs to list available local datasets, inspect metadata or licenses, inspect inferred columns and data types, locate exact versioned files, evaluate whether a dataset supports a research question, or record Kaggle provenance for a Parallax experiment. Keep the Kaggle store read-only unless the user explicitly asks to update it; do not bulk-copy datasets, treat inferred types as authoritative, or treat uploader descriptions as validated evidence.
---

# Use Local Kaggle Data

Use the machine-local Kaggle store as an external, versioned source library. Inspect provenance and
fitness before opening large files or designing an analysis.

## Locate the catalog

Prefer the command already on `PATH`:

```sh
command -v datasets
datasets list
```

If it is unavailable, try the user-scoped installation without hard-coding a username:

```sh
"$HOME/.local/bin/datasets" list
```

The underlying store normally lives at `$HOME/data/kaggle`. Treat everything under that directory
as read-only source data. Do not edit dataset files, manifests, metadata, or schemas in place.

## Inspect before selecting

Run all three views for a candidate:

```sh
datasets show <owner/slug-or-name>
datasets schema <owner/slug-or-name>
datasets json <owner/slug-or-name>
```

Use `show` to inspect:

- the exact local version and resolved path;
- license and expected update frequency;
- uploader description, source note, and explicit caveats;
- download date, checksums, file count, and size.

Use `schema` to inspect logical table groups, columns, inferred types, sampling, ignored files, and
inference errors. Types are analytical hints inferred from sampled rows and files. Validate parsing,
nullability, identifiers, timestamps, units, and category encodings in tested Parallax code before
enforcing a schema or making a claim.

Use `json` for machine-readable provenance. Extract only the fields needed instead of copying a
large inventory into the prompt:

```sh
datasets json <dataset> | jq '{
  handle,
  version,
  resolved_path: .local.resolved_path,
  retrieved_at: .local.retrieved_at,
  license: [.kaggle.info.licenses[]?.name],
  source_note: .kaggle.info.userSpecifiedSources,
  schema_status: .schema.status,
  schema_groups: [.schema.groups[] | {
    format,
    file_count,
    columns: [.columns[] | {name, data_type}]
  }]
}'
```

Inspect per-file checksums only for files the study will actually consume:

```sh
datasets json <dataset> | jq '.local.files[] | {path, bytes, sha256}'
```

## Evaluate research fitness

Before choosing a dataset, answer:

1. What construct does it directly observe, and what does it only proxy?
2. Is it observed, synthetic, scraped, transformed, or an uploader mirror of another source?
3. Does its time coverage and information cutoff support the proposed evaluation split?
4. Could selection, survivorship, look-ahead, geographic, or reporting bias determine the result?
5. Is there a credible baseline and a falsifiable rejection criterion?
6. Does the license permit the intended use, especially commercial or redistributed use?
7. Are update cadence, staleness, missingness, and schema drift acceptable?

Do not infer validity from Kaggle popularity or usability ratings. Do not turn a proxy into a causal
or behavioral measure. Flag synthetic data prominently; use it for testing or demonstrations, not
for factual population claims without independent validation.

## Use the data in Parallax

Assign every selected dataset to exactly one existing `RNN-title` research program. If no program
fits, stop and follow the repository process for proposing or creating one rather than placing data
under a generic directory.

For exploration, read files directly from the exact versioned `resolved_path`; never resolve a
mutable "latest" location. Avoid duplicating multi-gigabyte sources merely for convenience.

Before a recorded experiment depends on the dataset, preserve at least:

- Kaggle handle and numeric version;
- exact relative source file paths and SHA-256 checksums;
- retrieval timestamp and local schema record;
- license, upstream source, and material uploader caveats;
- owning Parallax research slug;
- transformation code revision and output checksum;
- information cutoff and leakage-relevant timing assumptions.

Record these through the owning program's data contract or a tested domain-specific immutable
import under `data/RNN-title/raw/`. Put derived outputs under `processed/`. Do not silently move or
reclassify a physical dataset when another program consumes it; link the owning snapshot and
transformation instead.

Keep notebooks exploratory. Move reusable readers, validators, and transformations into the
matching `src/parallax/<domain>/` package with deterministic tests before they support a durable
claim. Freeze the experiment design before opening final evaluation data.

## Mutation boundary

This skill is read-only by default. Do not run the Kaggle pull script, refresh schemas, delete old
versions, modify credentials, import everything into Postgres, or alter the external store unless
the user explicitly requests that action. If an update is authorized, use the store's existing
pull workflow and retain prior versions.

## Report the decision

When recommending or using a dataset, report the handle, version, selected files, size, license,
schema summary, source caveats, intended construct, major validity risks, owning research program,
and whether the work is exploratory or preregistered. State why rejected candidates were rejected.
