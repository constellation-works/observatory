# theories

One file per theory: `T###-slug.md`. What survived — the account that currently
holds, with `claims` naming the hypotheses it rests on and `supersedes` naming
the theories it replaced.

Graduating a hypothesis into a theory is a person's decision and is not
automated.

The ten records here are one per family of principia's frozen lock, which lives
read-only at [`_archive/principia/`](../_archive/principia/) and is still checked
by `make check-archive`. They cite into it and never restate or overrule a claim
it owns. If a claim the lock owns needs restating, it is restated as a hypothesis
in the live corpus and the lock is left as history.

`make new KIND=T TITLE="..."` allocates the next id.
