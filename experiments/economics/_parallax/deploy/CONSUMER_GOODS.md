---
title: "Importing Consumer Attention History"
summary: "One-time import instructions for the R03 wearable-health Google Trends pilot."
tags: [parallax, consumer-goods, google-trends, data-import, pilot]
related: ["docs/research/R03-consumer-goods/docs/DATA.md", "data/R03-consumer-goods/README.md", "deploy/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
---

# Importing consumer attention history

Google Trends already provides a rolling five-year history, so R03 does not run a weekly collector.
The pilot uses one frozen historical export. A later refresh is a new dataset version, not an
operational schedule.

## Export

In the official Google Trends UI, compare these exact search terms in this order:

1. `smart ring`
2. `smartwatch`
3. `fitness tracker`

Set United States, Past 5 years, All categories, and Web Search. Download the Interest-over-time CSV,
rename it `wearable-health.csv`, and place it in:

```text
data/R03-consumer-goods/inbox/google-trends/
```

Then import it:

```sh
make consumer-goods-import
```

The importer validates the ordered series labels and writes a dated immutable dataset with a
checksum manifest under `data/R03-consumer-goods/raw/history/`.

The official Google Trends API may replace this manual step if alpha access is granted. Parallax
does not use unofficial clients or undocumented endpoints.
