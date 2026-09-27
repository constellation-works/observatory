# Help JSON format

`tool help --format json` prints the whole command tree for the installed
version:

```json
{
  "tool": "tool",
  "version": "4.12.0",
  "schema": 2,
  "commands": [
    {
      "path": ["repo", "sync"],
      "summary": "Fetch and fast-forward tracked branches",
      "description": "Markdown text",
      "flags": [
        {"name": "--prune", "short": "-p", "type": "bool", "default": false,
         "summary": "Delete local branches whose upstream is gone",
         "deprecated": null, "renamed_from": ["--clean"], "since": "4.3.0"}
      ],
      "args": [{"name": "remote", "required": false, "variadic": false}],
      "examples": [{"command": "tool repo sync --prune", "note": "..."}],
      "hidden": false
    }
  ]
}
```

- `schema` 1 (tags before 4.0) lacks `since`, `renamed_from` and `examples`.
- `hidden` commands are omitted from docs but keep their anchors reserved.
- `description` is Markdown and may contain fenced code.
- Since 4.8 the CLI prints `https://docs.example.dev/<version>/cli/<path>#<flag>`
  in some error messages; those URLs must resolve.
