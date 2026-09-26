#!/usr/bin/env bash
# Create an isolated Orbit root and three mock workspaces for the
# crew-preference experiment. Does not touch ~/.orbit or live checkouts.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ORBIT_ROOT="${CREW_PREF_ORBIT_ROOT:-$HOME/.orbit-crew-pref-r014}"
FIXTURE_ROOT="${CREW_PREF_FIXTURE_ROOT:-$HOME/workspace/crew-pref-r014}"
ORBIT="${ORBIT_BIN:-orbit}"

# R014: the two live-table orchestrators R013 did not run. Everything else is R013.
ORCHESTRATORS=(grok sol)

if ! command -v "$ORBIT" >/dev/null 2>&1; then
  echo "orbit binary not on PATH" >&2
  exit 1
fi

mkdir -p "$ORBIT_ROOT" "$FIXTURE_ROOT"

if [[ ! -f "$ORBIT_ROOT/config.toml" ]]; then
  echo "Initializing isolated Orbit root at $ORBIT_ROOT"
  "$ORBIT" --root "$ORBIT_ROOT" init \
    --non-interactive \
    --machine-name crew-pref-r014 \
    --task-prefix CPEX
else
  echo "Reusing isolated Orbit root at $ORBIT_ROOT"
fi

python3 - "$ORBIT_ROOT/config.toml" <<'PY'
"""Keep only experiment crews and force default_crew=system."""
from pathlib import Path
import sys

path = Path(sys.argv[1])
keep = {
    "system",
    "astra",
    "sol",
    "luna",
    "terra",
    "opus",
    "sonnet",
    "grok",
    "gemini-flash",
}
out = []
skip = False
for line in path.read_text(encoding="utf-8").splitlines(True):
    if line.startswith("default_crew"):
        out.append('default_crew = "system"\n')
        continue
    stripped = line.strip()
    if stripped.startswith("[crews.") and stripped.endswith("]"):
        name = stripped[len("[crews.") : -1]
        skip = name not in keep
        if skip:
            continue
    elif stripped.startswith("[") and stripped.endswith("]"):
        skip = False
    if skip:
        continue
    out.append(line)
text = "".join(out)
if "[crews.gemini-flash]" not in text:
    text += """

[crews.gemini-flash]
provider = "gemini"
model = "gemini-flash"
"""
# R014: orbit 0.24 seeds crews from the agents it detects and may not define the
# `system` sentinel that default_crew names. It is off the menu; mirror the live
# store's definition so workspace init accepts the default.
if "[crews.system]" not in text:
    text += """

[crews.system]
provider = "codex"
model = "gpt-6-luna"
"""
path.write_text(text, encoding="utf-8")
print(f"Patched {path}: default_crew=system, menu crews only")
PY

workspace_registered() {
  local name="$1"
  "$ORBIT" --root "$ORBIT_ROOT" workspace list --format json \
    | python3 -c "import json,sys; rows=json.load(sys.stdin); raise SystemExit(0 if any(r.get('name')==sys.argv[1] for r in rows) else 1)" "$name"
}

seed_checkout() {
  local name="$1"
  local dest="$FIXTURE_ROOT/$name"
  mkdir -p "$dest"
  rsync -a --delete \
    --exclude '.git/' \
    --exclude '.orbit/' \
    "$HERE/seed/" "$dest/"
  cp "$HERE/feature.md" "$dest/FEATURE.md"
  cp "$HERE/prompt.md" "$dest/PROMPT.md"
  if [[ ! -d "$dest/.git" ]]; then
    git -C "$dest" init -b main
    git -C "$dest" add .
    git -C "$dest" -c user.email=crew-pref@local -c user.name=crew-pref \
      commit -m "seed: visual change explorer mock"
  else
    git -C "$dest" add .
    if ! git -C "$dest" diff --cached --quiet; then
      git -C "$dest" -c user.email=crew-pref@local -c user.name=crew-pref \
        commit -m "seed: refresh visual change explorer mock"
    fi
  fi
}

bind_prompt() {
  local dest="$1"
  local selector="$2"
  local crew="$3"
  python3 - "$HERE/prompt.md" "$dest/PROMPT.md" "$ORBIT_ROOT" "$selector" "$dest" "$crew" <<'PY'
from pathlib import Path
import sys
src, dest, root, selector, checkout, crew = sys.argv[1:]
text = Path(src).read_text(encoding="utf-8")
text = (
    text.replace("{{ORBIT_ROOT}}", root)
    .replace("{{WORKSPACE_SELECTOR}}", selector)
    .replace("{{CHECKOUT}}", checkout)
    .replace("{{ORCHESTRATOR_CREW}}", crew)
)
Path(dest).write_text(text, encoding="utf-8")
PY
}

CREW_NAME_grok=grok
CREW_NAME_sol=sol

for name in "${ORCHESTRATORS[@]}"; do
  seed_checkout "$name"
  dest="$FIXTURE_ROOT/$name"
  ws_name="crew-pref-$name"
  if workspace_registered "$ws_name"; then
    echo "Reusing workspace $ws_name"
  else
    echo "Initializing workspace $ws_name"
    (
      cd "$dest"
      "$ORBIT" --root "$ORBIT_ROOT" workspace init \
        --name "$ws_name" \
        --base-branch main \
        --ship-mode local
    )
  fi
  crew_var="CREW_NAME_$name"
  bind_prompt "$dest" "ws_$ws_name" "${!crew_var}"
done

echo
echo "Isolated root: $ORBIT_ROOT"
"$ORBIT" --root "$ORBIT_ROOT" workspace list --format json
echo
echo "default_crew:"
"$ORBIT" --root "$ORBIT_ROOT" config get workflow.default_crew
echo
echo "Fill prompt bindings from the workspace list (use id ws_crew-pref-*)."
echo "Do not pass --mcp; do not dispatch."
