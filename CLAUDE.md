# principia

The constellation's **theory corpus**: our own physics theories (`theory/`) and the sourced
notes on established physics they must respect (`studies/`). Named for Newton's *Principia*.

principia is **prose plus a machine-checked claim registry**. The experiments its claims are
tested against are cataloged sims in the sibling repo [**orrery**](../orrery)
(`codebases/orrery/lab/sims/`). The split is deliberate: one repo accumulates *theory*, the
other accumulates *runnable evidence*, and neither can silently drift from the other because
every claim links across the gap. New theory work starts as a gate card; see
[policy.md](policy.md).

## Layout

```
policy.md   Research procedure (gate cards, kinds, family split, expiry). The lock is
            scripts/check-theory.py; this file is the English.
theory/     One directory per theory: hub README.md, claims.json, evidence-ledger.md,
            related.md, open-questions.md, optional chapters. Contract in theory/README.md.
gates/      One JSON card per live front / owed object. New work starts here.
schema/     Claim and gate field docs; wall.json is the immortal refuted-id list.
studies/    Sourced notes on established physics. Contract in studies/README.md.
scripts/    check-theory.py — the pre-commit research-policy gate.
ledger.md   Generated rollup. Never hand-edit; --write-ledger regenerates it.
```

## The evidence-ledger contract

Each `theory/<slug>/` directory has a matching `claims.json` (canonical) and an
**evidence ledger** table in `evidence-ledger.md` that must match it byte-for-byte in the
`claim` column. Claim statuses:

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

Standing rules, machine-checked by `scripts/check-theory.py` on every theory change:

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
  it is cataloged under `orrery/lab/sims/<slug>/` with its `sim.json` and provenance. A
  theory question that needs a new or changed experiment becomes an orrery Orbit task —
  theory work here does not silently implement or redesign the sim that tests it.
- **New work is a gate card.** Before a new untested row or a new sim, add `gates/<id>.json`
  with one owed object, one family, a this-week kill, and a control. Phenomenology cards are
  rejected until the family's existence claim is `supported`. See [policy.md](policy.md).
- **Named postulates expire.** `kind: postulate` cannot be `supported`. Underived postulates
  past `expires` fail the check. A coupling written into a Hamiltonian is a postulate or a
  `hook`, not a nature result.
- **Families do not pay each other's debts.** `pays_debt_of` must be same-family. Reopening a
  wall id in `schema/wall.json` requires `daniel_reopen: true`.

## Cross-links to orrery

Sim references in ledgers point at the sibling checkout. From a file in `theory/<slug>/`,
sims are `../../../orrery/lab/sims/<sim>/` and studies are `../../studies/<note>.md`. From
a `studies/` note, sims stay `../../orrery/lab/sims/<sim>/` and theories are
`../theory/<slug>/`. These resolve in a standard constellation checkout (principia and
orrery are siblings under `codebases/`). In an isolated Git worktree the checker discovers that
sibling root from Git metadata, or accepts an overriding
`--external-root orrery=/absolute/path/to/orrery` mapping; see `README.md` for the runnable
command and failure diagnostics. Open a theory hub at `theory/<slug>/README.md`.

Provenance runs both ways: a `theory/` claim cites the sim that tests it; the sim's almanac
note (via orrery `sim.json` `provenance.almanac`) records the discussion it was born in.

## Validating a change

principia is still a **prose corpus** — nothing here compiles — but the research policy is
machine-checked. The checks below are the whole validation surface; they are portable (stdlib
`python3` and `git`, no host-specific tooling):

- **`python3 scripts/check-theory.py`** — required on every `theory/`, `gates/`, `schema/`,
  `policy.md`, or `ledger.md` change. Validates claim registries against essay tables, gate
  cards, the refuted wall, postulate expiry, hook controls, family-split, preferred-frame
  comparators, link resolution, and that `ledger.md` matches the generated rollup.
  `--write-ledger` regenerates `ledger.md`. `--selftest` runs the fixture checks.
- **`git diff --check`** — trailing whitespace and leftover merge-conflict markers.
- **Frontmatter stays intact.** A touched theory hub (`theory/<slug>/README.md`) keeps its
  `title, status, families, almanac, created, updated` keys with a valid doc-level `status`,
  matching `claims.json` on `title` / `status` / `families`; a touched `studies/` note
  keeps `title, status, created, updated`. Contracts: `theory/README.md`, `studies/README.md`.
- **Ledger tracks the claim.** If a claim's backing changed, its registry status **and** the
  essay table status changed in the *same* commit. The checker will refuse a split.

Do not land theory work that fails `scripts/check-theory.py`. Reviewer eyes still own
whether a derivation is genuine and whether a comparator is the right GR frame.

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
