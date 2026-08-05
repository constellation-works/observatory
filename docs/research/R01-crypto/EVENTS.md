---
title: "R01 Crypto Event Calendar"
summary: "Schema and provenance rules for scheduled mechanical-flow events in crypto markets."
tags: [parallax, crypto, events, data-contract]
related: ["docs/research/R01-crypto/README.md", "docs/research/R01-crypto/RESEARCH_AGENDA.md"]
created_on: 2026-08-01
updated_on: 2026-08-03
status: active
research_id: R01
domain: crypto
---

# Event calendar

The calendar is the data structure behind the forced-flow research program: scheduled events whose
associated trading is **mechanical rather than informational** — token unlocks, expiries,
delistings, rebalances. The counterparty hypothesis is that flow around these events must trade
regardless of price, which is one of the few durable reasons an edge can exist.

It is maintained by agents and humans, stored as append-only JSON lines at
`events/calendar.jsonl`, **tracked in git** (curated research data with provenance, not raw
market data), and enforced by `src/parallax/crypto/events.py`. Records that fail validation are not
written.

## The one rule that matters: `announced_time_utc`

Every event carries three times. `event_time_utc` is when the event happens.
`announced_time_utc` is when the event became publicly knowable — and it is **mandatory**,
because it is the look-ahead guard. A backtest that trades an unlock the market did not yet know
about is fiction, and this field is what makes that fiction mechanically detectable
(`EventStore.visible_at`).

`recorded_time_utc` is when *we* filed the record, and it is the second half of the same guard.
Backfilling a calendar is the normal case — we learn about last month's unlock today — and a
backtest dated last month could not have conditioned on a record that did not exist yet. So
`visible_at` uses **the later of announcement and filing**, exposed as `Event.visible_time`. An
event announced in January but filed in June is invisible to any experiment dated before June.

The practical consequence: file events as you find them, and never backdate `recorded_time_utc`
to make history look better covered than it was. A sparse calendar is a fact about the research;
a backdated one is a fabricated edge.

When the announcement time is unknown, agents record their best conservative estimate and mark
`confidence: "estimated"` — never a guess presented as fact.

## Schema

One JSON object per line:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `event_id` | str | generated | Deterministic hash of `(event_type, asset, venue, event_time_utc)`. |
| `event_type` | enum | yes | See the type table below. |
| `asset` | str | yes | Uppercase ticker (`BTC`, `ARB`) or `*` for market-wide events. |
| `venue` | str | no | Exchange or protocol it applies to; empty for global. |
| `event_time_utc` | ISO-8601 | yes | When the event occurs. `Z` suffix required. |
| `announced_time_utc` | ISO-8601 | yes | When it became publicly knowable. Must be ≤ `event_time_utc`. |
| `source_url` | str | yes | Where a reviewer can verify it. |
| `confidence` | enum | yes | `confirmed` \| `estimated` \| `rumored`. |
| `notional_usd` | float | no | Size of the mechanical flow, when quantifiable. |
| `pct_supply` | float | no | For unlocks: share of circulating supply released. |
| `notes` | str | no | Free text. |
| `recorded_time_utc` | ISO-8601 | generated | When this record was written. |
| `recorded_by` | str | yes | Agent or human who filed it. |
| `supersedes` | str | no | `event_id` of a record this one corrects. |

### Event types

| `event_type` | Mechanical flow |
|---|---|
| `token_unlock` | Vested tokens become sellable at a known instant. |
| `options_expiry` | Deribit/CME expiries; pinning and unwind flow. |
| `futures_expiry` | Quarterly futures roll. |
| `funding_settlement` | Perp funding exchange at fixed timestamps. |
| `index_rebalance` | Index and ETF basket changes force tracked flow. |
| `exchange_listing` | New listing; retail influx with a timestamped start. |
| `exchange_delisting` | Holders must exit or migrate by a deadline. |
| `network_upgrade` | Hard forks, halvings — dated protocol changes. |
| `macro_release` | CPI, FOMC — scheduled information, not flow, but a regime boundary. |
| `etf_flow_publication` | Daily creation/redemption publication timestamps. |
| `other` | Anything defensible that fits the announced-time discipline. |

## Correction discipline

The file is append-only. A wrong record is never edited or deleted: a new record is appended with
`supersedes` pointing at the wrong one, and readers resolve to the latest record in each
supersession chain (`EventStore.current`). This preserves what we believed and when we believed
it, which matters when auditing why a backtest saw the calendar it saw.

Corrections must target the record that is **currently** live, not the one you first wrote down.
Two records correcting the same superseded id fork the chain, and a fork has no single latest
record — so `append` rejects it. This is deliberately caught before the write: the file is
append-only, so once both lines are on disk there is no legal way to remove either. If a
correction is refused, read the chain with `EventStore.current()` and supersede its head.

## Agent workflow

Agents filing events are leaf executors with one job: find candidate events in a named source,
validate them through `parallax.crypto.events`, and append with `recorded_by` set to their name and a
working `source_url`. Curation (deduplication judgment, confidence upgrades, supersessions) is
orchestrator or human work. The calendar deliberately starts small and verified rather than large
and scraped: fifty events with clean provenance beat five thousand of unknown quality, because
every experiment downstream inherits the calendar's error rate.
