---
title: "R04 Tracking Universe"
summary: "Frozen provider set, query mode, category index, and event contract for AI-assistant attention elasticity."
tags: [parallax, ai-assistants, tracking-universe, search-attention, elasticity]
related: ["docs/research/R04-ai-assistants/README.md", "docs/research/R04-ai-assistants/docs/LAUNCH_REGISTRY.md", "docs/research/R04-ai-assistants/hypothesis/README.md"]
created_on: 2026-08-03
updated_on: 2026-08-03
status: active
research_id: R04
domain: ai-assistants
---

# R04 tracking universe

Universe version `v1`, frozen 2026-08-03.

## Unit of study

`provider × week`, and the quantity of interest is a **response coefficient**, not a level. R04
does not ask who has the most attention — that is known, stable, and available from any analyst
report. It asks how much each provider's attention *moves* per unit of shock, and whether that
responsiveness decays as a product matures.

## Why levels are not the measure

Google Trends divides every series in a comparison by one global maximum and rounds to integers.
The scale factor is common to all series and constant in time, so it **cancels in a log
difference**: `Δlog(index) = Δlog(volume)`. A response coefficient estimated in log differences is
therefore recoverable from a badly normalised index, while a level comparison is not.

The rounding does not cancel. Quantisation is the binding constraint on this design and is checked
before anything is modelled — see the resolution gate below.

## The category index

`AI` is carried in every basket as the **market index**, and every provider is measured relative to
it rather than in absolute terms. Two things are absorbed by doing this:

1. **Diffusion decay.** Search for a named product is largely an act of discovery. A person who
   already uses a tool has it bookmarked and stops searching for it, so the flow of searches tracks
   *new adoption* while the installed base is a stock. As the susceptible population saturates, the
   flow falls even as cumulative adoption keeps rising. Raw attention will therefore decline for
   every provider for reasons that have nothing to do with that provider.
2. **Common shocks.** Category-wide news moves all providers together.

Without an index, a maturity-decay finding would be indistinguishable from ordinary market
saturation. With one, the diffusion envelope sits in the index and the provider coefficient
measures excess response. This is the same discipline R01 applies with its Bitcoin benchmark: an
absolute number that has not been differenced against its market is not a result.

### Known weaknesses of `AI` as an index

- **Query migration.** As a category matures, people stop searching the generic word and search the
  brand — or stop searching at all and ask the assistant directly. `AI` may therefore decay faster
  than true category interest, biasing provider betas upward. `AI` is a proxy index, not the market.
- **Self-composition.** A dominant provider is a large component of the category it is being
  regressed on, which attenuates its coefficient toward 1 by construction. The effect is severe for
  the largest provider and negligible for small ones. Any provider exceeding roughly a quarter of
  basket attention must be estimated against a leave-one-out index instead; record which index was
  used with every coefficient.
- **Polysemy.** `AI` also matches unrelated senses. It is retained anyway because the alternative —
  building a category aggregate from provider terms — would make the index endogenous to the very
  competition being measured.

## Query mode: Topics for entities, exact terms for the index

R03 freezes "exact search terms, not Topics". That rule is correct for generic product types like
`air fryer` and **wrong for branded entities**, so R04 splits it:

- **Providers and products use Google Trends Topics**, which resolve to a disambiguated entity.
- **The category index uses the exact term** `AI`, since no single entity represents it.

The reason is measurement, not taste. `Gemini` as a search term carries the zodiac sign, whose
annual cycle peaks 21 May – 20 June and would inject exactly the calendar artefact R03 spent E03
and E04 learning to distrust. `Claude` carries a common French given name — Monet, Debussy,
Shannon. `Grok` carries Heinlein. Left as terms, these baselines could exceed the product signal
and would not be constant over time.

Every export records which mode each query used. Term-mode and Topic-mode series for the same
provider are different measurements and are never mixed in one analysis.

## Frozen providers

| Provider | Entity tracked | Consumer product | Notes |
|---|---|---|---|
| OpenAI | ChatGPT | ChatGPT | Category creator; first mover 2022-11-30 |
| Anthropic | Claude | Claude | Given-name polysemy; Topic mode mandatory |
| Google | Gemini | Gemini | Zodiac polysemy; renamed from Bard 2024-02-08 |
| xAI | Grok | Grok | Provider rebranded to SpaceXAI 2026-07; entity continuity must be checked |
| DeepSeek | DeepSeek | DeepSeek | Consumer product often upgraded in place under unchanged names |
| Meta | Meta AI | Meta AI | Llama retired as consumer flagship 2026-04-08 in favour of Muse |
| Mistral | Le Chat | Le Chat | Smallest; expected to fail the resolution gate |

`AI` is carried alongside as the index in every basket.

Two structural renames break longitudinal joins and must be handled explicitly rather than
silently: **Bard → Gemini** (2024-02-08) and **xAI → SpaceXAI** (2026-07). A rename is a
discontinuity in the measurement, not in the product.

## Basket design

One basket cannot hold every provider at usable resolution, because ChatGPT's launch would set the
maximum and crush the rest toward the integer floor. Baskets are therefore built as:

`{one or two providers} + AI`

so each provider is measured against a mid-sized reference rather than against the category leader.
`AI` appears in every basket and is the join key across them: because the scale factor cancels in
log differences, coefficients estimated in separate baskets remain comparable, while **levels do
not** and must never be compared across baskets.

## Resolution gate

Run before any modelling, on every series, and record the result:

- count of distinct integer values over the window;
- share of weeks at or below 2;
- the log-ratio jump implied by a one-unit tick at the series' median level, as a multiple of the
  standard deviation of its weekly change.

A series whose smallest expressible increment approaches its typical weekly movement cannot support
an elasticity estimate and is **excluded with that finding recorded**, not modelled with a caveat.
R03's E01 would have been stopped by this gate: its emerging series sat at 1–3 integers across the
whole training window.

Exclusion is a result. A provider too small to measure in consumer search is itself a fact about
where that provider's attention lives.

## Event contract

Shocks come from [`LAUNCH_REGISTRY.md`](LAUNCH_REGISTRY.md). Its rules:

- every event carries an announcement date, a general-availability date when it differs, an event
  class, a source URL, and a confidence mark;
- events are filed from provider newsrooms wherever possible, and a date that could not be verified
  against a fetched source is marked `uncertain` and excluded from primary estimation;
- **announcement, not availability, is the shock** for attention purposes, since attention responds
  to news; a large announcement-to-GA gap makes an event a candidate for exclusion because it has
  two plausible shock dates;
- events within 14 days of another provider's event are marked **clustered** and cannot support
  cross-provider attribution, only own-response estimation.

## Change control

Universe `v1` freezes the provider set, query mode, index term, basket rule, and resolution gate. A
quarterly review may propose `v2`; it cannot rewrite `v1` history. A newly tracked provider gets an
explicit entry date and is ineligible for claims about earlier periods.
