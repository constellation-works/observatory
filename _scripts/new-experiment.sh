#!/usr/bin/env bash
# Scaffold experiments/<domain>/<id>/ from the template. The id must be a node.
set -euo pipefail
cd "$(dirname "$0")/.."
domain="${1:-}"; id="${2:-}"
[ -n "$domain" ] && [ -n "$id" ] || { echo "usage: new-experiment.sh <domain> <node-id>" >&2; exit 2; }
root="${NEBULA_ROOT:-knowledgebase/lineage}"
if [ "$domain" != "kaggle" ] && [ ! -f "$root/nodes/$id.md" ]; then
  echo "no node \`$id\` in $root/nodes. Capture and promote the idea first:  neb capture ...; neb promote <entry>" >&2
  exit 1
fi
dest="experiments/$domain/$id"
[ -e "$dest" ] && { echo "$dest already exists" >&2; exit 1; }
mkdir -p "$dest"
sed -e "s/{{domain}}/$domain/g" -e "s/{{id}}/$id/g" -e "s/{{date}}/$(date +%F)/g" experiments/_template/README.md > "$dest/README.md"
sed -e "s/{{domain}}/$domain/g" -e "s/{{id}}/$id/g" -e "s/{{date}}/$(date +%F)/g" experiments/_template/manifest.json > "$dest/manifest.json"
mkdir -p "_data/$domain/$id" "_outputs/$domain/$id"
echo "$dest"
echo "data:    _data/$domain/$id   (write a manifest.json there when you fetch something)"
echo "outputs: _outputs/$domain/$id"
echo "study:   knowledgebase/studies/$domain/$id.md   (create when there is a result)"
