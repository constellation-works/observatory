#!/usr/bin/env bash
# Verify, before any session runs, that nothing an orchestrator can read in its
# Orbit root or checkout reveals which model sits behind a crew label.
# Exits non-zero on the first leak. Run after ./setup.sh.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ORBIT_BASE="${CREW_PREF_ORBIT_BASE:-$HOME/.orbit-crew-pref-r017}"
WORK_BASE="${CREW_PREF_WORK_BASE:-/var/tmp/crew-pref-r017/work}"
ORBIT="${ORBIT_BIN:-orbit}"
# Model and crew names from R015's menu and the orchestrators. Provider names
# (claude, codex, grok, gemini) are shown on purpose and are not leaks.
# Skipped: the root's skills/ and resources/, Orbit's bundled docs and policies.
# They are the same in every root (as in R015's), name models only as generic
# configuration examples, and hold no label; they cannot reveal the mapping.
LEAK='gpt-|opus|sonnet|luna|terra|\bsol\b|astra|grok-[0-9]|flash|claude-|gemini-[0-9]|fable'
fail=0

tail -n +2 "$HERE/sessions.tsv" | while IFS=$'\t' read -r sid _ _ _; do
  root="$ORBIT_BASE/$sid" dest="$WORK_BASE/$sid"
  hits="$(grep -r -a -o -i -E "$LEAK" "$root" "$dest" --exclude-dir=.git \
    --exclude-dir=skills --exclude-dir=resources 2>/dev/null \
    | sort | uniq -c || true)"
  crews="$("$ORBIT" --root "$root" config show 2>&1 | sed -n '/^Crews/,/^$/p')"
  models="$(awk 'NR > 2 && NF {print $4}' <<<"$crews" | sort -u | tr '\n' ' ')"
  labels="$(awk 'NR > 2 && NF {print $1}' <<<"$crews" | tr '\n' ' ')"
  if [[ -n "$hits" || "$models" != "hidden " \
        || "$labels" != "crew-a crew-b crew-c crew-d crew-e crew-f crew-g planner system " ]]; then
    echo "$sid LEAK"; echo "$hits"; echo "$crews"; exit 1
  fi
  echo "$sid clean"
done || fail=1
exit "$fail"
