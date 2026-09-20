# _outputs

Run products: model checkpoints, generated figures, simulation dumps. Never in
git. Organise as `_outputs/<domain>/<node-id>/` so a result can be traced to
the idea it tested.

Anything worth keeping is *promoted*: the figure and the numbers go into
`knowledgebase/studies/<domain>/<node-id>.md`, and the study is what
`neb evidence --source` points at. `_outputs/` is regenerable by design.
