---
title: "R04 AI Assistants"
summary: "Paused charter for measuring attention elasticity of AI assistant providers; Google Trends was found too coarse to measure the smaller providers."
tags: [parallax, ai-assistants, attention-elasticity, search-attention, paused]
related: ["docs/research/R04-ai-assistants/docs/TRACKING_UNIVERSE.md", "docs/research/R04-ai-assistants/docs/LAUNCH_REGISTRY.md", "docs/research/R04-ai-assistants/docs/WHOISUSINGAI_API.md", "docs/research/R04-ai-assistants/hypothesis/README.md", "docs/research/R04-ai-assistants/experiments/README.md", "docs/research/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-16
status: paused
research_id: R04
domain: ai-assistants
---

# R04 AI assistants

**Paused 2026-08-03, pending a data source that can resolve providers below the category leader.**
No hypothesis is registered. The charter and the measurement findings below are kept because the
findings are what a future attempt needs first.

## Purpose

Measure the **elasticity of attention** for AI assistant providers — how much a provider's
attention moves per unit of shock — and whether that responsiveness declines as a product matures.

This is deliberately not a market-share question. Who has the most attention is known, stable, and
available from any analyst report. Elasticity is orthogonal to size: a small provider can be highly
responsive and a large one barely responsive, and the gap between them is a measure of whether
attention is earned by events or carried by an installed base.

## Boundary

- **In scope:** response coefficients, their decay with product maturity, and cross-provider
  substitution at launch events.
- **Out of scope:** level comparisons, market share, revenue, or usage. Search attention is not
  usage, and for a mature tool it is close to the opposite — a habituated user has the tab
  bookmarked and stops searching.
- **Consequential actions disabled by default:** none are contemplated; R04 is observational.

## Evidence contract

- **Observational unit:** provider × week, and eventually provider × region × week.
- **Quantity:** a response coefficient in log differences, never a level.
- **Baseline:** constant elasticity per provider, with no maturity term.
- **Required split:** chronological; events are the replication unit, not weeks.
- **Uncertainty:** clustered by week, because a global launch hits every provider and region at once.

## Why it is paused

The pilot data source — Google Trends — cannot resolve the providers the question is about.
[`TRACKING_UNIVERSE.md`](docs/TRACKING_UNIVERSE.md) carries the resolution gate and the numbers.
Summary of what was measured on 2026-08-03:

| Series | Median index | Tick ÷ weekly sd | Verdict |
|---|---|---|---|
| chatgpt | 61–66 | 0.12–0.18 | usable |
| AI | 46 | 0.32 | usable |
| gemini | 9–11 | 0.63–0.75 | marginal |
| claude | 3–4 | 1.23–1.36 | **unusable** |
| grok | 2–3 | 0.99–1.41 | **unusable** |

The smallest increment Trends can express for Claude is larger than Claude's typical weekly
movement. Three mitigations were tried and measured rather than assumed:

1. **Drop the leader from the basket** — no effect. Trends scales to the window *maximum*, so any
   remaining series with a launch spike anchors the scale just as hard.
2. **Region-specific export (US)** — negligible. Claude's median moves 3 → 4.
3. **Short per-event windows plus basket surgery together** — this does work on paper, predicting a
   Claude level of 22–83 and a ratio of 0.05–0.20. It requires one export per event per region per
   basket, which is where manual UI collection stops being viable.

The instrument, not the question, is the blocker. The question is well posed and the design below
is sound; it needs a source with per-query volume rather than a within-basket integer index.

## What a replacement source must provide

- absolute or comparable volume, not an index rescaled per request;
- enough resolution that the smallest expressible increment is well under a typical weekly move for
  the *smallest* provider of interest, not the largest;
- regional breakdown, to support the panel identification described in the universe; and
- a stable definition over several years, since maturity decay is a multi-year claim.

## Design that survives the pause

Two decisions were reached and should not be relitigated from scratch:

- **No index.** A category index built from the tracked providers is ~0.89 correlated with the
  leader — it is a monopoly proxy, and regressing the leader on it subtracts the signal. The `AI`
  search term is not a usable substitute: it explains about a third of the aggregate's variance and
  drifts in meaning as users migrate from generic to branded queries.
- **Panel with region-week fixed effects, not differencing.** Fixed effects absorb the diffusion
  envelope and every common shock nonparametrically, without an index. Second differencing also
  removes the envelope but inflates noise ~1.4–1.6× and induces a lag-1 autocorrelation near −0.5,
  the signature of over-differencing. Staggered regional rollouts recorded in
  [`LAUNCH_REGISTRY.md`](docs/LAUNCH_REGISTRY.md) — EU delays, US/CA-first releases, long
  announcement-to-availability gaps — give treated and not-yet-treated regions in the same week,
  which is the cleanest identification available.

## First question, when it resumes

Own-launch attention elasticity declines as a provider's product matures. Register it as
`hypothesis/H01-*.md` only once a source clears the resolution gate for at least three providers.
