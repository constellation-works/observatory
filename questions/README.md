# questions

One file per question: `Q###-slug.md`. This is the capture inbox — the place an
idea lands before it is sharp enough to be a claim.

A question has no code and no result, so it is a single markdown file. When it
becomes a precise claim, write a hypothesis and leave the question where it is;
`answered_by` points at the hypotheses and research items that settled it.

`make new KIND=Q TITLE="..."` allocates the next id. The slug is the kebab-case
of the title at creation and is frozen: a later title change edits the
frontmatter, never the filename.
