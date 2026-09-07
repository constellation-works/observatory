#!/usr/bin/env bash
# principia's lock, unchanged, run against knowledgebase/theory.
# The checker resolves `../../../orrery/lab/sims/<slug>/` links through --external-root.
set -euo pipefail
cd "$(dirname "$0")/.."
THEORY=knowledgebase/theory
ORRERY=experiments/physics/_orrery
args=(--root "$THEORY")
[ -d "$ORRERY" ] && args+=(--external-root "orrery=$ORRERY")
python "$THEORY/scripts/check-theory.py" "${args[@]}" "$@"
