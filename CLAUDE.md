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

## Validating a change

principia is a **prose corpus — there is no build, test suite, or CI to run**. That is by
design, not an omission: nothing here compiles, so land nothing that would need it. The checks
below are the whole validation surface, and each is portable — plain `git`/shell, no provider-
or host-specific tooling:

- **`git diff --check`** — catches trailing whitespace and any leftover merge-conflict markers
  before they land. Run it on every commit.
- **Relative links resolve.** Edits routinely touch intra-corpus links (`../studies/…`,
  `../theory/…`) and cross-repo sim links (`../../orrery/lab/sims/<slug>/`). Confirm each
  changed link's target exists *from the editing file's directory*. No script enforces this —
  it is a manual read, or a throwaway shell one-liner over the changed files.
- **Frontmatter stays intact.** A touched `theory/` doc keeps its `title, status, families,
  almanac, created, updated` keys with a valid doc-level `status`; a touched `studies/` note
  keeps `title, status, created, updated`. Contracts: `theory/README.md`, `studies/README.md`.
- **Ledger tracks the claim.** If a claim's backing changed, its evidence-ledger row status
  changed in the *same* commit (see *Rules of the house*).

That is the full pre-commit gate — there is no compile step to pass and no automated runner to
wait on; reviewer eyes plus the checks above are the bar.

## Conventions

- **Independent repo**; default branch **agent-main**, commit directly (**no PR gate**) — land
  work straight onto `agent-main`. Registered in `operations/scripts/repos.tsv`.
- **One guide, both providers — no provider-specific config.** This `CLAUDE.md` is the single
  maintained contract for the repo; `AGENTS.md` is a symlink to it, so Codex (Sol) and Claude
  (Fable) load the exact same file. Edit here — never fork a second guide. The symlink is the
  only provider affordance, and it resolves in any clean checkout, so the repo needs no
  `.codex/` directory or other non-portable Codex config.
- **Orbit workspace: `ws_principia`** (dk-server-1) — provisioned 2026-07-10 when dispatchable
  theory-only work arrived (the SPEC gate passed; ORB-10095/ORB-10096 are its first tasks).
  Earlier theory tasks lived in `ws_orrery`, which is now faraday's experimental workspace.
- **Stewardship:** kepler is jointly held by Fable (Claude) and Sol (Codex); both steward
  principia's theory and literature, and Sol makes direct edits here. Experimental work is
  sent to orrery as an explicit Orbit task rather than implemented from principia. The
  evidence boundary remains explicit: orrery reports apparatus/result/limitations;
  principia judges theory and literature.

## Provenance

`theory/` and `studies/` were split out of **orrery** on 2026-07-10 (orrery at commit
`0c30ab9`). The pre-split history stays in orrery; this repo starts fresh from the migrated
files. See [README.md](README.md).
