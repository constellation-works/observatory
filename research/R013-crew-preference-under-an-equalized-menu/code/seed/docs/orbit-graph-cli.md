# orbit-graph CLI contract (for this product)

`orbit-graph` indexes a source tree into local SQLite and answers graph queries
through a terminal CLI. Scripts must use `--format json`. Query commands never
refresh the index; run `sync` after source changes.

Commands used by this product (see upstream `--help` for flags):

| Command | Role |
|---|---|
| `orbit-graph --format json sync --full` | Build or rebuild an index for the current Git worktree |
| `orbit-graph --format json search <name> --kind symbol` | Find symbols |
| `orbit-graph --format json show <selector>` | Show a symbol or file |
| `orbit-graph --format json refs <selector> --kind call` | Incoming references |
| `orbit-graph --format json callees <selector>` | Outgoing callees |
| `orbit-graph --format json impact …` | Changed-symbol / impact queries when comparing revisions |
| `orbit-graph --format json trace …` | Bounded path between symbols |

Selectors are canonical (`file:`, `dir:`, `symbol:path#name:kind`).

Known limits to surface in the UI, not hide:

- syntax-driven extraction; missing or lower-confidence edges for dynamic
  dispatch, macros, generated code, and ambiguous symbols
- “no path found” means no path in the indexed evidence
- depth, node, and time bounds truncate results and must be visible

This product must not check out over the user’s working tree to compare two
commits. Use isolated snapshot trees or another supported snapshot mechanism,
then point `orbit-graph` at each snapshot separately so base and head indexes
stay distinct.
