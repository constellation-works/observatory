# _data

Datasets live here on disk and never in git. Each experiment that needs data
keeps a `manifest.json` next to its files:

```json
{
  "node": "ranking-decay-half-life",
  "source": "https://www.kaggle.com/competitions/stellar/data",
  "fetch": "kaggle competitions download -c stellar -p _data/kaggle/stellar",
  "files": [{ "path": "train.csv", "sha256": "…", "bytes": 123456 }],
  "license": "competition rules",
  "fetched_on": "2026-09-07"
}
```

Manifests are committed; the files they describe are not. `make check-layout`
fails on any tracked file under `_data/` that is not a manifest or README.
