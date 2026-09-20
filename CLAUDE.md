# observatory — Claude-specific guide

Read [AGENTS.md](AGENTS.md) first; the boundaries there are the whole point of
this repository and are easy to violate by accident.

Three that bite most often:

- **Never rename or renumber a record.** The id and slug are frozen at creation.
  A title change edits frontmatter only, and `make new` is the only thing that
  allocates an id.
- **Never commit bytes under `data/` or `output/`.** Only `manifest.json` and
  `README.md` may be tracked there, anywhere in the tree.
- **Never edit `_archive/`.** It is frozen history, including principia's
  byte-pinned lock. If a claim it owns needs restating, restate it as a new
  hypothesis in the live corpus.

`make check` catches all three.

Work in one research item at a time: everything about `R001` lives in
`research/R001-slug/`, so a run's write footprint is that directory plus
assessment entries appended to the hypotheses it tests. That is what keeps
parallel work mergeable.
