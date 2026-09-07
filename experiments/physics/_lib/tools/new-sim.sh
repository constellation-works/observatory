#!/usr/bin/env bash
#
# new-sim.sh — scaffold a new sim from templates/ under a nebula node.
#
# Usage:
#   experiments/physics/_lib/tools/new-sim.sh <node-id> <slug> [--kind web|py] [--title "Human Title"]
#
# Creates experiments/physics/<node-id>/<slug>/ with a runnable starter + sim.json,
# then rebuilds the gallery. The node must exist in the corpus (neb show <node-id>).
# Slug is kebab-case; kind defaults to web.
set -euo pipefail

LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PHYS="$(cd "$LIB/.." && pwd)"
OBS="$(cd "$PHYS/../.." && pwd)"
NODE="${1:?usage: new-sim.sh <node-id> <slug> [--kind web|py] [--title \"...\"]}"
SLUG="${2:?usage: new-sim.sh <node-id> <slug> [--kind web|py] [--title \"...\"]}"
shift 2
CORPUS="${NEBULA_ROOT:-$OBS/knowledgebase/lineage}"
[ -f "$CORPUS/nodes/$NODE.md" ] || { echo "no node $NODE in $CORPUS/nodes; capture and promote it first" >&2; exit 1; }
KIND="web"
TITLE="$SLUG"

while [ $# -gt 0 ]; do
  case "$1" in
    --kind)  KIND="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
done

case "$KIND" in web|py) ;; *) echo "kind must be web or py" >&2; exit 1 ;; esac
[[ "$SLUG" =~ ^[a-z0-9][a-z0-9-]*$ ]] || { echo "slug must be kebab-case" >&2; exit 1; }

DEST="$PHYS/$NODE/$SLUG"
[ -e "$DEST" ] && { echo "experiments/physics/$NODE/$SLUG already exists" >&2; exit 1; }

mkdir -p "$PHYS/$NODE"
cp -R "$LIB/templates/$KIND" "$DEST"
DATE="$(date +%Y-%m-%d)"
for f in "$DEST"/*; do
  [ -f "$f" ] || continue
  sed -i.bak -e "s/__SLUG__/$SLUG/g" -e "s/__TITLE__/$TITLE/g" -e "s/__DATE__/$DATE/g" "$f"
  rm -f "$f.bak"
done

python3 "$LIB/tools/build-gallery.py"
echo "created experiments/physics/$NODE/$SLUG (kind=$KIND)"
[ "$KIND" = web ] && echo "view: make serve then http://localhost:8000/experiments/physics/$NODE/$SLUG/"
[ "$KIND" = py ] && echo "run:  uv run experiments/physics/$NODE/$SLUG/main.py"
