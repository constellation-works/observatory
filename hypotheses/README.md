# hypotheses

One file per hypothesis: `H###-slug.md`. A hypothesis is a claim stated so that a
run can come out against it.

`assessments` is an append-only log in the frontmatter: one entry per verdict,
with the date, the research item, the statement `revision` it is about, the
verdict (`supports`, `refutes`, `inconclusive`) and its strength. Entries are
never edited or removed, and disagreeing entries coexist — that is the point.
Bump `revision` when the statement itself changes; an assessment against an older
revision does not carry to the current statement.

`status` is a person's call. The checker warns when it disagrees with the latest
assessment and never overwrites it. Execution success is not support: a `done`
research item with a `refutes` or `inconclusive` assessment is a complete result.

`make new KIND=H TITLE="..."` allocates the next id.
