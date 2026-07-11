# principia

The constellation's **theory corpus**: our own physics theories (`theory/`) and the sourced
notes on established physics they must respect (`studies/`). Named for Newton's *Principia*.

principia is **prose**. The experiments its claims are tested against are cataloged sims in the
sibling repo [**orrery**](../orrery) (`codebases/orrery/lab/sims/`). The split is deliberate:
one repo accumulates *theory*, the other accumulates *runnable evidence*, and neither can
silently drift from the other because every claim links across the gap.

## Layout

```
theory/     Our own theories — one living document per line of inquiry, each with an
            evidence ledger: a table mapping every claim to a status and the sims/studies
            that back it. Contract in theory/README.md.
studies/    Sourced notes on established physics — one note per fact-cluster (a bound, a
            measured value, an experiment lineage), each load-bearing fact carrying a
            verifiable citation. Contract in studies/README.md.
```

## The evidence-ledger contract

Each `theory/` doc carries frontmatter (`title`, `status`, `families`, `almanac`, `created`,
`updated`) and an **evidence ledger** table. Claim statuses:

| Claim status | Meaning |
|---|---|
| `supported` | a sim or study backs it, linked in the row |
| `mixed` | evidence cuts both ways — the row says how |
| `untested` | stated but not yet simulated/sourced |
| `refuted` | evidence kills it — the row links what did |
| `conjecture` | not yet backed by anything; flagged pending a study note |

Doc-level `status`: `exploratory` (being built), `growing` (active work), `refuted` (central
claim is dead — doc stays), `resolved` (converged with established physics; kept as a
correspondence record).

## Rules of the house

These are kepler's standing rules (`agentbase/kepler/memory/rules/`), enforced on every edit:

- **Theory bends to evidence, never the reverse.** A sim or study that contradicts a claim
  changes that claim's status **in the same change-set** that lands the evidence. Softening the
  evidence, cherry-picking parameters, or quietly dropping a claim are forbidden moves — the
  only legal move is updating the theory. Applies to pet theories exactly as strictly as to
  textbook physics.
- **A refuted branch is a result, not an embarrassment.** When evidence kills a line of inquiry
  the doc gets `status: refuted`, a plain statement of what killed it, and pointers to the
  refuting sims/studies. It is never deleted; its sims stay runnable in orrery (the *claim* was
  wrong, not the *sim*). Reopening a refuted branch, or deleting it, needs Daniel's explicit
  say-so.
- **Cite established physics or label it conjecture.** A load-bearing fact about established
  physics rests on a `studies/` note with a real, verified citation; a fact that can't be
  sourced right now is written `conjecture — to verify`, never stated as settled. Citations are
  checked against the actual source before being recorded.
- **Evidence enters through orrery's catalog.** A sim becomes admissible evidence only once
  faraday catalogs it under `orrery/lab/sims/<slug>/` with its `sim.json` and provenance. A
  theory question that needs a new or changed experiment becomes a **faraday task** — theory
  work here does not silently implement or redesign the sim that tests it.

## Cross-links to orrery

Sim references in ledgers point at the sibling checkout: from a `theory/` or `studies/` doc,
`../../orrery/lab/sims/<slug>/`. These resolve in a standard constellation checkout (principia
and orrery are siblings under `codebases/`). Intra-corpus links stay local: `../studies/…`
from a theory doc, `../theory/…` from a study.

Provenance runs both ways: a `theory/` claim cites the sim that tests it; the sim's almanac
note (via orrery `sim.json` `provenance.almanac`) records the discussion it was born in.

## Conventions

- **Independent repo**; default branch **agent-main**, commit directly (**no PR gate**).
  Registered in `operations/scripts/repos.tsv`.
- **Orbit workspace: `ws_principia`** (dk-server-1) — provisioned 2026-07-10 when dispatchable
  theory-only work arrived (the SPEC gate passed; ORB-10095/ORB-10096 are its first tasks).
  Earlier theory tasks lived in `ws_orrery`, which is now faraday's experimental workspace.
- **Stewardship:** kepler / Fable (Claude) (`agentbase/kepler/memory`) is primary. faraday /
  Sol (Codex) owns orrery's `lab/`. Cross-lane questions use explicit handoffs — faraday
  reports apparatus/result/limitations; kepler judges theory and literature.

## Provenance

`theory/` and `studies/` were split out of **orrery** on 2026-07-10 (orrery at commit
`0c30ab9`). The pre-split history stays in orrery; this repo starts fresh from the migrated
files. See [README.md](README.md).
