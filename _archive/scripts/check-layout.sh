#!/usr/bin/env bash
# The layout invariants. Fails on the first violation of the boundaries in AGENTS.md.
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
say() { echo "check-layout: $*" >&2; fail=1; }

# 1. Nothing tracked under _data or _outputs except manifests and READMEs.
while IFS= read -r f; do
  case "$f" in
    _data/README.md|_outputs/README.md|*/manifest.json) ;;
    *) say "tracked data/output file: $f" ;;
  esac
done < <(git ls-files _data _outputs 2>/dev/null)

# 2. Every experiment directory is keyed by a node in the corpus, or is a kaggle
#    competition, or is the template.
root="${NEBULA_ROOT:-knowledgebase/lineage}"
for dir in experiments/*/*/; do
  [ -d "$dir" ] || continue
  domain=$(basename "$(dirname "$dir")"); id=$(basename "$dir")
  [ "$domain" = "_template" ] && continue
  [ "$domain" = "kaggle" ] && continue
  # Underscore-prefixed ids are migration staging areas (e.g. physics/_orrery):
  # a whole source repository parked until each family is tied to a node.
  case "$id" in _*) continue ;; esac
  [ -f "$root/nodes/$id.md" ] || say "experiments/$domain/$id has no node $id in $root/nodes"
  [ -f "$dir/manifest.json" ] || say "experiments/$domain/$id has no manifest.json"
done

# 3. Every study names an experiment that exists.
for f in knowledgebase/studies/*/*.md; do
  [ -f "$f" ] || continue
  domain=$(basename "$(dirname "$f")"); id=$(basename "$f" .md)
  [ "$id" = "README" ] && continue
  [ -d "experiments/$domain/$id" ] || say "study $f has no experiments/$domain/$id"
done

[ "$fail" -eq 0 ] && echo "check-layout: ok"
exit "$fail"
