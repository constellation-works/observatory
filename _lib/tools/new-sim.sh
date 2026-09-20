#!/usr/bin/env bash
#
# new-sim.sh — scaffold a sim inside an existing research item.
#
# Usage:
#   _lib/tools/new-sim.sh <R-id> <slug> [--kind web|py] [--title "Human Title"]
#
# Creates research/<R###-slug>/code/<slug>/ with a runnable starter + sim.json,
# then rebuilds the gallery. The research item must already exist; scaffold it
# with `make new KIND=R TITLE="..."` first. Slug is kebab-case; kind defaults
# to web.
set -euo pipefail

LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OBS="$(cd "$LIB/.." && pwd)"
RECORD="${1:?usage: new-sim.sh <R-id> <slug> [--kind web|py] [--title \"...\"]}"
SLUG="${2:?usage: new-sim.sh <R-id> <slug> [--kind web|py] [--title \"...\"]}"
shift 2
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

# Accept either the bare id (R003) or the full directory name (R003-network-force).
DIR=""
for candidate in "$OBS/research/$RECORD" "$OBS/research/$RECORD"-*; do
  [ -d "$candidate" ] || continue
  DIR="$candidate"
  break
done
[ -n "$DIR" ] || { echo "no research item $RECORD under research/; run 'make new KIND=R TITLE=\"...\"' first" >&2; exit 1; }

DEST="$DIR/code/$SLUG"
REL="${DEST#"$OBS/"}"
[ -e "$DEST" ] && { echo "$REL already exists" >&2; exit 1; }

mkdir -p "$DIR/code"
cp -R "$LIB/templates/$KIND" "$DEST"
DATE="$(date +%Y-%m-%d)"
for f in "$DEST"/*; do
  [ -f "$f" ] || continue
  sed -i.bak -e "s/__SLUG__/$SLUG/g" -e "s/__TITLE__/$TITLE/g" -e "s/__DATE__/$DATE/g" "$f"
  rm -f "$f.bak"
done

python3 "$LIB/tools/build-gallery.py"
echo "created $REL (kind=$KIND)"
[ "$KIND" = web ] && echo "view: make serve then http://localhost:8000/$REL/"
[ "$KIND" = py ] && echo "run:  uv run $REL/main.py"
