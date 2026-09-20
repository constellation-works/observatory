# _data

Datasets shared across research items. Bytes live here on disk and never in git:
`_data/**` is ignored except for `README.md` and any `manifest.json`.

An input used by one research item belongs in that item's own `data/`, with its
manifest, so that everything about R001 lives in R001. This directory is only for
a dataset several items read, and a research item references it from its own
manifest:

```json
{ "inputs": [{ "name": "astrolabe-processed", "shared": "_data/physics/astrolabe" }] }
```

`physics/astrolabe/` is the one such dataset: astrolabe's processed catalogue,
ephemeris and derived stores, which `ASTROLABE_DATA_DIR` points at.
