# Checklist template schema (v1)

A template is one JSON document:

```json
{
  "id": "fire-door-annual",
  "version": 3,
  "title": "Fire door annual inspection",
  "sections": [
    {
      "id": "frame",
      "title": "Frame and hinges",
      "when": null,
      "items": [
        {"id": "gap", "type": "measurement", "label": "Gap at head", "unit": "mm", "min": 2, "max": 4, "required": true},
        {"id": "hinges", "type": "passfail", "label": "Three hinges present", "required": true, "photo": "on_fail"},
        {"id": "notes", "type": "text", "label": "Notes", "required": false}
      ]
    }
  ]
}
```

Item types: `passfail` (pass / fail / n/a), `measurement` (number with a unit
and optional range), `choice` (one of `options[]`), `text`, `photo`.

`photo` on any item is `never`, `optional`, `on_fail` or `required`.
`when` makes a section conditional on another item's answer, e.g.
`{"item": "frame.hinges", "equals": "fail"}`.

`id` plus `version` identifies a template. Published versions are immutable.
