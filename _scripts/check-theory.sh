#!/usr/bin/env bash
# principia's lock, unchanged, run against the frozen archive at _archive/principia.
# The checker resolves `../../../orrery/lab/sims/<slug>/` links through --external-root;
# those symlinks under _archive/orrery/lab/sims point at the research items that now
# hold the sims. Reached as `make check-archive`, never from `make check`.
set -euo pipefail
cd "$(dirname "$0")/.."
THEORY=_archive/principia
ORRERY=_archive/orrery
args=(--root "$THEORY")
[ -d "$ORRERY" ] && args+=(--external-root "orrery=$ORRERY")
python "$THEORY/scripts/check-theory.py" "${args[@]}" "$@"
