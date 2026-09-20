---
title: "Who Is Using AI API Provider Note"
summary: "Verified public JSON endpoints and research caveats for the PIXIPACE Who Is Using AI tracker."
tags: [parallax, ai-assistants, data-provider, google-trends, public-api]
related: ["docs/research/R04-ai-assistants/README.md", "docs/research/R04-ai-assistants/docs/TRACKING_UNIVERSE.md", "data/R04-ai-assistants/README.md"]
created_on: 2026-08-16
updated_on: 2026-08-16
status: candidate
research_id: R04
domain: ai-assistants
---

# Who Is Using AI API provider note

Provider: **PIXIPACE / [Who Is Using AI?](https://whoisusingai.com/tracker/research)**.

The research console exposes static JSON files over unauthenticated `GET`. The site states that the
data is free for any use with attribution to `whoisusingai.com`; treat that statement as provider
terms, not as a substitute for a formal license review if the data is redistributed. The endpoints
send `Access-Control-Allow-Origin: *`, so browser and notebook clients can read them directly.

This is a **candidate source**, not an approved R04 instrument. It may remove the manual-export
burden that paused R04, but its underlying Google Trends measurement still has to clear the frozen
resolution gate and query-mode requirements in [`TRACKING_UNIVERSE.md`](TRACKING_UNIVERSE.md).

## Endpoint inventory

| Endpoint | Contents |
|---|---|
| `/history/research/index.json` | Available years, generation timestamp, and snapshot count |
| `/history/research/trends-<YYYY>.json` | Country × tool × date search-share bundle plus global weekly and daily series |
| `/history/research/signals-<YYYY>.json` | npm, PyPI, GitHub-star, and Wikipedia series |
| `/history/tracker/index.json` | Sorted dates for raw daily snapshots |
| `/history/tracker/<YYYY-MM-DD>.json` | One raw daily tracker snapshot |
| `/history/series/<ISO2>.json` | One country's full daily tool history |
| `/tracker_data.js` | Live dashboard object as JavaScript, not plain JSON |

Base URL: `https://whoisusingai.com`.

## Verified snapshot

Checked on 2026-08-16:

- `GET /history/research/index.json` returned HTTP 200 with `application/json` and permissive CORS.
- The index reported year `2026`, generation time `2026-08-07T14:10:27.045477+00:00`, and 27
  snapshots.
- `trends-2026.json` was 374,265 bytes and contained 26 tools, 86 country entries, and 27 date
  positions from 2026-07-07 through 2026-08-07.
- Bundle dates do not imply observations. The US series had trailing nulls; the last non-null values
  for ChatGPT, Gemini, and Claude were on 2026-07-19.

The provider describes search values as **anchor-normalized percentages of AI-tool searches**.
They measure relative search preference, not adoption, active users, or market share. Tool arrays
are index-aligned with `dates`; retain nulls rather than interpolating them silently.

## Candidate-use checks

Before using this source for R04:

1. Determine whether provider entities use Google Trends Topics or ambiguous exact terms. R04
   requires Topics for branded entities such as Claude and Gemini.
2. Run the frozen resolution gate for every provider and region. Decimal output alone does not prove
   that the underlying signal escapes Google Trends quantization.
3. Verify the provider's anchor-normalization method and whether revisions rewrite historical
   values.
4. Record retrieval time, resolved endpoint, response headers, SHA-256, provider generation stamp,
   and the exact non-null date range in a local raw-data manifest.
5. Preserve the fetched response immutably. Do not treat a later CDN response as the same dataset
   merely because the URL is unchanged.

## Minimal pull

```python
import json
from urllib.request import urlopen

url = "https://whoisusingai.com/history/research/trends-2026.json"
with urlopen(url) as response:
    bundle = json.load(response)

dates = bundle["dates"]
claude_us = bundle["values"]["US"]["claude"]
rows = [
    {"date": date, "value": value}
    for date, value in zip(dates, claude_us)
    if value is not None
]
```

For discovery, fetch `history/research/index.json` first rather than assuming a year bundle exists.
