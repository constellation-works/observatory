# Research policy

This is the procedure. `scripts/check-theory.py` is the lock. The essays in
`theory/` remain the argument; they are not the source of truth for claim
status, kind, or what work is allowed to start.

## Unit of work

New theory work is a **gate card** in `gates/`, not a new paragraph and not a
new sim. A card states one owed object, one family, and one of:

| kind | meaning |
|---|---|
| `existence` | does a regular solution / sector even exist? |
| `control` | the coupling-off / comparator-off run |
| `derivation` | a named postulate becomes a consequence of a local mechanism |
| `phenomenology` | numbers about nature (PPN, drag timescales, galaxies, clocks) |

Phenomenology is illegal while an existence claim it names in `blocked_by` is
not `supported`. Compute the ugly number in a notebook before filing a lattice
for a phenomenology card.

## Kinds of claim

Canonical files: `theory/<doc>/claims.json`. Every `## Evidence ledger` row in
`theory/<doc>/evidence-ledger.md` must appear there, byte-for-byte in `claim`.

| kind | what it is |
|---|---|
| `postulate` | we put this in. Not a discovery. Needs `named`, `expires`, `kill`. Cannot be `supported` (use `model-property` for lattice theorems of a postulate). |
| `derived` | follows from named postulates by algebra |
| `model-property` | true of the model / lattice (the ⊙ rows) |
| `nature` | a claim about the world |
| `hook` | a structural feature a later source law might couple to. Requires `control`. Cannot be `supported` unless `control_ran` is true. |

A coupling written into a Hamiltonian is a postulate or a hook. Measuring that
the model then contains the coupling's algebra is a model-property, not a
nature result.

## Families do not pay each other's debts

`family` is exactly one of the doc's families. `pays_debt_of` must point at a
claim in the same family. The shear law does not pay two-substance's source-law
debt. Two-substance does not inherit scarcity's closed system.

## Refuted wall

`schema/wall.json` lists claim ids that may not vanish. Reopening one requires
`reopens` on a new claim **and** `daniel_reopen: true`. Quiet resurrection
fails the checker.

## Preferred-frame confrontations

A claim tagged `preferred-frame` must name `comparator`. The comparator is the
theory in the frame the observation is actually in — for GR and uniform motion,
mass-frame Schwarzschild (U is gauge), not a Galilean \(U+v_{GP}\) picture.

## Live front

A `growing` or `exploratory` doc names `live_fronts`: gate ids. One live front
per family. Do not open a second phenomenology front on a family whose
existence card is still open.

## Named postulates expire

A postulate with `derived: false` past `expires` fails the check. Renew with a
reason (still a debt) or derive it. Default window is thirty days from naming.

## Evidence

Admissible evidence is a cataloged orrery sim or a sourced `studies/` note.
Analytic rows stay `untested` until one of those exists — including algebra
that is decisive on paper.

## What the checker cannot do

It cannot tell whether a comparator is the *right* GR frame beyond requiring
that one is named, whether a derivation is genuine, or whether a picture is
true. Those stay human. The lock makes it expensive to skip the question.
