# research

One directory per research item: `R###-slug/`. This is the only kind that gets a
directory, because it is the only kind that produces code and outputs.

```
R###-slug/
  README.md     frontmatter, then Question, Method, Result, Limitations, Next — in that order
  code/         the scripts that produced the result
  artifacts/    promoted figures and tables the README cites (committed, small)
  data/         inputs (ignored; data/manifest.json is committed)
  output/       raw run products (ignored)
```

Everything about R001 lives in R001. That is what makes many research agents
mergeable: one run's write footprint is one directory plus assessment entries
appended to the hypotheses it tests.

`tests` names those hypotheses; `orbit` optionally records the task and run that
drove the work. A new item is one question, one run — `make new KIND=R
TITLE="..."`. Several of the migrated items are legacy records holding a whole
family of sims under `code/<sim>/`, which is history, not a pattern to copy.

Sims with a `sim.json` appear in the generated catalogue at `_lib/gallery/`
(`make gallery`); serve the repository root with `make serve` to open them.
