---
title: "R04 Data"
summary: "Local Google Trends exports for the paused AI-assistant attention program, with their known resolution limits."
tags: [parallax, ai-assistants, data-contract, google-trends]
related: ["docs/research/R04-ai-assistants/README.md", "docs/research/R04-ai-assistants/docs/TRACKING_UNIVERSE.md", "data/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: paused
research_id: R04
domain: ai-assistants
---

# R04 data

Exploratory Google Trends UI exports under `raw/`, ignored by git. These are **exploratory pulls,
not a manifested snapshot**: they carry the browser default filenames, have no manifest and no
checksum, and were downloaded by hand while shaping the question.

They are retained because the resolution finding was measured on them and should be reproducible.
They must not be used for a preregistered result. If R04 resumes on Trends, exports go through an
import step that records collection time, source, expected terms, and SHA-256, as R03 does.

## Known limits of what is here

- Providers below the category leader quantize to 2–4 integer levels, so their week-to-week changes
  are dominated by rounding. See the resolution gate in the tracking universe.
- Scaling is per export. Levels are never comparable across files; only log differences are.
- Query mode is exact terms, so `gemini` carries the zodiac sign and `claude` a common given name.
  The universe calls for Topics mode instead, which these files predate.
