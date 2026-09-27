#!/usr/bin/env bash
# Create the 30 R017 sessions: one isolated Orbit root, one workspace and one
# fresh seed checkout per (orchestrator, feature). Writes sessions.tsv and the
# per-session label -> crew mapping (../data/mapping.tsv, untracked).
# Does not touch ~/.orbit or live checkouts. Idempotent.
#
# R015's setup with two changes: the menu is seven neutral labels whose crew
# behind each label is shuffled per session, and every crew in the store is
# described by its provider only (model "hidden"). ./leakcheck.sh verifies the
# roots before any session runs.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ITEM="$(dirname "$HERE")"
ORBIT_BASE="${CREW_PREF_ORBIT_BASE:-$HOME/.orbit-crew-pref-r017}"
# Outside $HOME: Claude Code loads instruction files from every ancestor of the
# working directory, and $HOME/.claude/CLAUDE.md is the host's agent guide.
WORK_BASE="${CREW_PREF_WORK_BASE:-/var/tmp/crew-pref-r017/work}"
ORBIT="${ORBIT_BIN:-orbit}"

ORCHESTRATORS=(astra opus-5-5 opus-5 gemini-flash grok sol)
FEATURES=(change-explorer field-sync build-cache docs-site ledger-import)

command -v "$ORBIT" >/dev/null || { echo "orbit binary not on PATH" >&2; exit 1; }
mkdir -p "$ORBIT_BASE" "$WORK_BASE" "$ITEM/data"

# Staggered design: at step r, orchestrator i plans feature (i + r) mod 5, so
# every orchestrator sees every feature once (opus-5 shares astra's order).
# Session ids are shuffled with a fixed seed so paths do not encode the design.
# Each session gets its own shuffle of R015's seven crews onto crew-a..crew-g.
python3 - "$HERE/sessions.tsv" "$ITEM/data/mapping.tsv" "${ORCHESTRATORS[*]}" "${FEATURES[*]}" <<'PY'
import random, sys
out, mapping, orchs, feats = sys.argv[1], sys.argv[2], sys.argv[3].split(), sys.argv[4].split()
crews = ["sol", "grok", "gemini-flash", "opus", "sonnet", "luna", "terra"]
labels = [f"crew-{c}" for c in "abcdefg"]
cells = [(r, o, feats[(i + r) % 5]) for r in range(5) for i, o in enumerate(orchs)]
ids = [f"s{n:02d}" for n in range(1, len(cells) + 1)]
rng = random.Random(17)
rng.shuffle(ids)
with open(out, "w") as f:
    f.write("session\tstep\torchestrator\tfeature\n")
    for sid, (r, o, feat) in zip(ids, cells):
        f.write(f"{sid}\t{r + 1}\t{o}\t{feat}\n")
with open(mapping, "w") as f:
    f.write("session\tlabel\tcrew\n")
    for sid in sorted(ids):
        shuffled = crews[:]
        rng.shuffle(shuffled)
        for label, crew in zip(labels, shuffled):
            f.write(f"{sid}\t{label}\t{crew}\n")
print(f"wrote {out} and {mapping}")
PY

write_config() {  # root session orchestrator
  python3 - "$1/config.toml" "$ITEM/data/mapping.tsv" "$2" "$3" <<'PY'
"""Drop every crew table and every comment; add crew-a..crew-g (provider, model
"hidden", provider-only description), the orchestrator's `planner` crew and
`system`. default_crew and system_crew = system; complexity pools stay empty."""
import csv, sys
from pathlib import Path

path, mapping, sid, orch = Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
CLI = {"sol": "codex", "luna": "codex", "terra": "codex", "opus": "claude",
       "sonnet": "claude", "grok": "grok", "gemini-flash": "gemini"}
NAME = {"codex": "an OpenAI", "claude": "an Anthropic", "grok": "an xAI", "gemini": "a Google"}
ORCH_CLI = {"astra": "codex", "sol": "codex", "opus-5-5": "claude", "opus-5": "claude",
            "grok": "grok", "gemini-flash": "gemini"}

out, skip = [], False
for line in path.read_text(encoding="utf-8").splitlines(True):
    s = line.strip()
    if s.startswith("#"):
        continue
    if s.startswith("[crews."):
        skip = True
        continue
    if s.startswith("["):
        skip = False
    if skip:
        continue
    if line.startswith("default_crew"):
        line = 'default_crew = "system"\n'
    elif line.startswith("system_crew"):
        line = 'system_crew = "system"\n'
    out.append(line)
text = "".join(out).rstrip() + "\n"
with open(mapping) as f:
    rows = [r for r in csv.DictReader(f, delimiter="\t") if r["session"] == sid]
for r in rows:
    cli = CLI[r["crew"]]
    text += (f'\n[crews.{r["label"]}]\nprovider = "{cli}"\nmodel = "hidden"\n'
             f'description = "Runs {NAME[cli]} model."\n')
text += f'\n[crews.planner]\nprovider = "{ORCH_CLI[orch]}"\nmodel = "hidden"\n'
text += '\n[crews.system]\nprovider = "codex"\nmodel = "hidden"\n'
path.write_text(text, encoding="utf-8")
PY
}

bind_prompt() {  # checkout root selector session
  python3 - "$HERE/prompt.md" "$1/PROMPT.md" "$2" "$3" "$1" "$ITEM/data/mapping.tsv" "$4" <<'PY'
import csv, sys
from pathlib import Path
src, dest, root, selector, checkout, mapping, sid = sys.argv[1:]
CLI = {"sol": "an OpenAI", "luna": "an OpenAI", "terra": "an OpenAI", "opus": "an Anthropic",
       "sonnet": "an Anthropic", "grok": "an xAI", "gemini-flash": "a Google"}
with open(mapping) as f:
    rows = [r for r in csv.DictReader(f, delimiter="\t") if r["session"] == sid]
menu = "\n".join(f"- `{r['label']}`: runs {CLI[r['crew']]} model"
                 for r in sorted(rows, key=lambda r: r["label"]))
text = Path(src).read_text(encoding="utf-8")
for k, v in {"ORBIT_ROOT": root, "WORKSPACE_SELECTOR": selector, "CHECKOUT": checkout,
             "ORCHESTRATOR_CREW": "planner", "CREW_MENU": menu}.items():
    text = text.replace("{{" + k + "}}", v)
Path(dest).write_text(text, encoding="utf-8")
PY
}

tail -n +2 "$HERE/sessions.tsv" | while IFS=$'\t' read -r sid step orch feat; do
  root="$ORBIT_BASE/$sid"
  dest="$WORK_BASE/$sid"
  if [[ ! -f "$root/config.toml" ]]; then
    "$ORBIT" --root "$root" init --non-interactive --machine-name crew-pref \
      --task-prefix CPEX >/dev/null
  fi
  write_config "$root" "$sid" "$orch"

  if [[ ! -d "$dest/.git" ]]; then
    mkdir -p "$dest"
    rsync -a "$HERE/features/$feat/seed/" "$dest/"
    cp "$HERE/features/$feat/FEATURE.md" "$dest/FEATURE.md"
    bind_prompt "$dest" "$root" "ws_crew-pref" "$sid"
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
  bind_prompt "$dest" "$root" "ws_crew-pref" "$sid"
  echo "$sid step $step $orch $feat ready"
done
