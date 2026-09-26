#!/usr/bin/env bash
# Create the 25 R015 sessions: one isolated Orbit root, one workspace and one
# fresh seed checkout per (orchestrator, feature). Writes sessions.tsv.
# Does not touch ~/.orbit or live checkouts. Idempotent.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ORBIT_BASE="${CREW_PREF_ORBIT_BASE:-$HOME/.orbit-crew-pref-r015}"
# Outside $HOME: Claude Code loads instruction files from every ancestor of the
# working directory, and $HOME/.claude/CLAUDE.md is the host's agent guide.
WORK_BASE="${CREW_PREF_WORK_BASE:-/var/tmp/crew-pref-r015/work}"
ORBIT="${ORBIT_BIN:-orbit}"

ORCHESTRATORS=(astra opus gemini-flash grok sol)
FEATURES=(change-explorer field-sync build-cache docs-site ledger-import)

command -v "$ORBIT" >/dev/null || { echo "orbit binary not on PATH" >&2; exit 1; }
mkdir -p "$ORBIT_BASE" "$WORK_BASE"

# Latin square: at step r, orchestrator i plans feature (i + r) mod 5, so every
# orchestrator sees every feature once and every feature runs once per step.
# Session ids are shuffled with a fixed seed so paths do not encode the design.
python3 - "$HERE/sessions.tsv" "${ORCHESTRATORS[*]}" "${FEATURES[*]}" <<'PY'
import random, sys
out, orchs, feats = sys.argv[1], sys.argv[2].split(), sys.argv[3].split()
cells = [(r, o, feats[(i + r) % 5]) for r in range(5) for i, o in enumerate(orchs)]
ids = [f"s{n:02d}" for n in range(1, 26)]
random.Random(15).shuffle(ids)
with open(out, "w") as f:
    f.write("session\tstep\torchestrator\tfeature\n")
    for sid, (r, o, feat) in zip(ids, cells):
        f.write(f"{sid}\t{r + 1}\t{o}\t{feat}\n")
print(f"wrote {out}")
PY

patch_config() {
  python3 - "$1/config.toml" <<'PY'
"""Keep only experiment crews, force default_crew=system (as R013/R014)."""
from pathlib import Path
import sys

path = Path(sys.argv[1])
keep = {"system", "astra", "sol", "luna", "terra", "opus", "sonnet", "grok", "gemini-flash"}
out, skip = [], False
for line in path.read_text(encoding="utf-8").splitlines(True):
    if line.startswith("default_crew"):
        out.append('default_crew = "system"\n')
        continue
    s = line.strip()
    if s.startswith("[crews.") and s.endswith("]"):
        skip = s[len("[crews."):-1] not in keep
        if skip:
            continue
    elif s.startswith("[") and s.endswith("]"):
        skip = False
    if not skip:
        out.append(line)
text = "".join(out)
if "[crews.gemini-flash]" not in text:
    text += '\n\n[crews.gemini-flash]\nprovider = "gemini"\nmodel = "gemini-flash"\n'
if "[crews.system]" not in text:
    text += '\n\n[crews.system]\nprovider = "codex"\nmodel = "gpt-6-luna"\n'
path.write_text(text, encoding="utf-8")
PY
}

bind_prompt() {
  python3 - "$HERE/prompt.md" "$1/PROMPT.md" "$2" "$3" "$1" "$4" <<'PY'
from pathlib import Path
import sys
src, dest, root, selector, checkout, crew = sys.argv[1:]
text = Path(src).read_text(encoding="utf-8")
for k, v in {"ORBIT_ROOT": root, "WORKSPACE_SELECTOR": selector,
             "CHECKOUT": checkout, "ORCHESTRATOR_CREW": crew}.items():
    text = text.replace("{{" + k + "}}", v)
Path(dest).write_text(text, encoding="utf-8")
PY
}

tail -n +2 "$HERE/sessions.tsv" | while IFS=$'\t' read -r sid step orch feat; do
  root="$ORBIT_BASE/$sid"
  dest="$WORK_BASE/$sid"
  if [[ ! -f "$root/config.toml" ]]; then
    "$ORBIT" --root "$root" init --non-interactive --machine-name crew-pref-r015 \
      --task-prefix CPEX >/dev/null
  fi
  patch_config "$root"

  if [[ ! -d "$dest/.git" ]]; then
    mkdir -p "$dest"
    rsync -a "$HERE/features/$feat/seed/" "$dest/"
    cp "$HERE/features/$feat/FEATURE.md" "$dest/FEATURE.md"
    cp "$HERE/prompt.md" "$dest/PROMPT.md"
    git -C "$dest" init -q -b main
    git -C "$dest" add .
    git -C "$dest" -c user.email=crew-pref@local -c user.name=crew-pref \
      commit -q -m "seed: $feat"
  fi

  if ! "$ORBIT" --root "$root" workspace list --format json \
      | python3 -c "import json,sys; raise SystemExit(0 if any(r.get('name')=='crew-pref' for r in json.load(sys.stdin)) else 1)"; then
    (cd "$dest" && "$ORBIT" --root "$root" workspace init --name crew-pref \
      --base-branch main --ship-mode local >/dev/null)
  fi
  bind_prompt "$dest" "$root" "ws_crew-pref" "$orch"
  echo "$sid step $step $orch $feat ready"
done
