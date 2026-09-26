#!/usr/bin/env bash
# Run the five R016 sessions in parallel (R015's runner; the opus orchestrator
# runs Claude Opus 5 instead of Opus 5.5, everything else unchanged).
#
#   ./run.sh
#
# Every session gets a fresh HOME holding only its CLI's login, so no host agent
# instructions, skills, plugins, hooks, MCP servers or memories load, and nothing
# carries over between sessions. Logs go to ../output/<session>.*
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../output"
ORBIT_BASE="${CREW_PREF_ORBIT_BASE:-$HOME/.orbit-crew-pref-r016}"
WORK_BASE="${CREW_PREF_WORK_BASE:-/var/tmp/crew-pref-r016/work}"
HOME_BASE="${CREW_PREF_HOME_BASE:-/var/tmp/crew-pref-r016/homes}"
REAL_HOME="$HOME"
TIMEOUT=3600
mkdir -p "$OUT" "$HOME_BASE"

make_home() {  # session orchestrator -> prints HOME path
  local h="$HOME_BASE/$1"
  rm -rf "$h"
  case "$2" in
    astra|sol)
      mkdir -p "$h/.codex"
      ln -s "$REAL_HOME/.codex/auth.json" "$h/.codex/auth.json"
      printf '[projects."%s"]\ntrust_level = "trusted"\n' "$WORK_BASE/$1" > "$h/.codex/config.toml" ;;
    opus)
      mkdir -p "$h/.claude"
      ln -s "$REAL_HOME/.claude/.credentials.json" "$h/.claude/.credentials.json" ;;
    gemini-flash)
      mkdir -p "$h/.gemini/antigravity-cli"
      ln -s "$REAL_HOME/.gemini/antigravity-cli/antigravity-oauth-token" \
        "$h/.gemini/antigravity-cli/antigravity-oauth-token" ;;
    grok)
      mkdir -p "$h/.grok"
      ln -s "$REAL_HOME/.grok/auth.json" "$h/.grok/auth.json" ;;
  esac
  echo "$h"
}

run_session() {  # session orchestrator
  local sid="$1" orch="$2" root="$ORBIT_BASE/$1" dest="$WORK_BASE/$1" h rc
  if [[ -f "$OUT/$sid.exit" ]]; then echo "$sid done already, skipping"; return; fi
  h="$(make_home "$sid" "$orch")"
  date -u +%FT%TZ > "$OUT/$sid.started"
  set +e
  # Models and efforts are each crew's configured settings in the live store,
  # except opus: R016 runs Claude Opus 5 (R015 ran Opus 5.5).
  case "$orch" in
    astra|sol)
      local model=gpt-6-astra effort=medium
      [[ "$orch" == sol ]] && model=gpt-6-sol effort=xhigh
      (cd "$dest" && HOME="$h" timeout "$TIMEOUT" codex exec -m "$model" \
        -c "model_reasoning_effort=\"$effort\"" -C "$dest" -s workspace-write \
        --add-dir "$root" --json - < PROMPT.md) ;;
    opus)
      (cd "$dest" && HOME="$h" timeout "$TIMEOUT" claude -p --model claude-opus-5 \
        --effort high --dangerously-skip-permissions --add-dir "$root" \
        --output-format stream-json --verbose < PROMPT.md) ;;
    gemini-flash)
      (cd "$dest" && HOME="$h" timeout "$TIMEOUT" agy -p "$(cat PROMPT.md)" \
        --model gemini-3.8-flash-high --dangerously-skip-permissions \
        --add-dir "$root" --output-format stream-json) ;;
    grok)
      (cd "$dest" && HOME="$h" GROK_MEMORY=0 timeout "$TIMEOUT" grok -m grok-4.7 \
        --always-approve --disable-web-search --output-format streaming-messages-json \
        --prompt-file PROMPT.md) ;;
  esac > "$OUT/$sid.jsonl" 2> "$OUT/$sid.stderr"
  rc=$?
  set -e
  printf 'exit %s\n%s\n' "$rc" "$(date -u +%FT%TZ)" > "$OUT/$sid.exit"
  rm -rf "$h"  # drop the login symlink and any session state
  echo "$sid $orch exit $rc"
}

while IFS=$'\t' read -r sid step orch feat; do
  run_session "$sid" "$orch" &
done < <(tail -n +2 "$HERE/sessions.tsv")
wait
echo "all sessions finished"
