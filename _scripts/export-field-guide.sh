#!/usr/bin/env bash
# Allowlisted rebuild of the shareable physics field-guide export.
# Usage (any cwd):  _scripts/export-field-guide.sh [--output DIR]
# Default output:   <repo>/_outputs/field-guide-export/
set -euo pipefail

die() { echo "export-field-guide: $*" >&2; exit 1; }

ORIG_PWD=$(pwd -P)
REPO=$(cd "$(dirname "$0")/.." && pwd -P)
OUT_DEFAULT="$REPO/_outputs/field-guide-export"
OUT=""

abspath() {
  python3 -c 'import os, sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$1"
}

usage() {
  cat <<EOF
Usage: $(basename "$0") [--output DIR]

Rebuild the shareable physics field-guide export from an explicit allowlist.
Default output: $OUT_DEFAULT
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      [[ $# -ge 2 ]] || die "--output requires a directory"
      OUT=$2
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

if [[ -z "$OUT" ]]; then
  OUT=$OUT_DEFAULT
elif [[ "$OUT" != /* ]]; then
  OUT=$(abspath "$ORIG_PWD/$OUT")
else
  OUT=$(abspath "$OUT")
fi

[[ -n "$OUT" && "$OUT" != "/" ]] || die "refusing to rebuild '$OUT'"
[[ "$OUT" != "$REPO" ]] || die "refusing to rebuild the repository root"
case "$OUT" in
  "$REPO/_outputs"|"$REPO/_outputs"/*) ;;
  "$REPO"|"$REPO"/*)
    die "refusing to rebuild a path inside the repository outside _outputs/"
    ;;
esac
[[ -e "$OUT/.git" ]] && die "refusing to rebuild a git checkout at $OUT"

GUIDE="$REPO/experiments/physics/physics-field-guide"
WEB="$REPO/experiments/physics/_lib/web"
FPUT_SITE="$REPO/_outputs/physics/fput-recurrence-reproduction/site"
FPUT_FIG="$REPO/experiments/physics/fput-recurrence-reproduction/reference/la-1940-fig1.png"
VENDOR_THREE="$REPO/experiments/physics/_lib/vendor/three"

rm -rf "$OUT"
mkdir -p "$OUT"

copy_file() {
  local src=$1 dest=$2
  [[ -f "$src" ]] || return 0
  mkdir -p "$(dirname "$dest")"
  cp -a "$src" "$dest"
}

# --- chapters --------------------------------------------------------------
CHAPTERS=()
shopt -s nullglob
for dir in "$GUIDE"/*/; do
  [[ -f "$dir/chapter.json" ]] || continue
  slug=$(basename "$dir")
  dest="$OUT/physics-field-guide/$slug"
  mkdir -p "$dest"
  copy_file "$dir/index.html" "$dest/index.html"
  copy_file "$dir/chapter.json" "$dest/chapter.json"
  copy_file "$dir/sim.json" "$dest/sim.json"
  copy_file "$dir/validation.json" "$dest/validation.json"
  copy_file "$dir/README.md" "$dest/README.md"
  for f in "$dir"/*.js; do
    copy_file "$f" "$dest/$(basename "$f")"
  done
  for f in "$dir"/*.{png,svg,jpg,jpeg,gif,webp}; do
    copy_file "$f" "$dest/$(basename "$f")"
  done
  [[ -f "$dest/index.html" ]] || die "chapter $slug is missing index.html"
  CHAPTERS+=("$slug")
done
shopt -u nullglob

[[ ${#CHAPTERS[@]} -gt 0 ]] || die "no chapter.json directories under $GUIDE"

# --- shared harness (layout mirrors experiments/physics/) -------------------
[[ -d "$WEB" ]] || die "missing $WEB"
mkdir -p "$OUT/_lib/web"
while IFS= read -r -d '' f; do
  rel=${f#"$WEB"/}
  copy_file "$f" "$OUT/_lib/web/$rel"
done < <(find "$WEB" -type f ! -path '*/__pycache__/*' -print0)

copy_file "$GUIDE/README.md" "$OUT/physics-field-guide/README.md"

# --- FPUT study site (optional) + public-domain figure ----------------------
FPUT_INCLUDED=0
if [[ -d "$FPUT_SITE" ]]; then
  mkdir -p "$OUT/study/fput-recurrence-reproduction"
  # Copy only files; keep relative layout inside the site root.
  while IFS= read -r -d '' f; do
    rel=${f#"$FPUT_SITE"/}
    copy_file "$f" "$OUT/study/fput-recurrence-reproduction/$rel"
  done < <(find "$FPUT_SITE" -type f ! -path '*/__pycache__/*' -print0)
  FPUT_INCLUDED=1
  [[ -f "$OUT/study/fput-recurrence-reproduction/index.html" ]] || FPUT_INCLUDED=0
else
  echo "export-field-guide: FPUT study site not present at $FPUT_SITE; skipping" >&2
fi

[[ -f "$FPUT_FIG" ]] || die "missing public-domain figure $FPUT_FIG"
copy_file "$FPUT_FIG" "$OUT/reference/la-1940-fig1.png"
mkdir -p "$OUT/reference"
cat > "$OUT/reference/README.md" <<'EOF'
# LA-1940 Fig. 1

Source: [OSTI public copy](https://www.osti.gov/servlets/purl/4376203), DOI
[10.2172/4376203](https://doi.org/10.2172/4376203). The report is a US
Government work and the scan is public domain.

Credit: E. Fermi, J. Pasta, S. Ulam (with M. Tsingou), LANL/OSTI, LA-1940
(1955), Fig. 1; crop prepared for this observatory experiment.
EOF

# --- vendor/three only if an exported chapter actually imports it -----------
USES_THREE=0
if grep -RIlE 'three\.min\.js|_lib/vendor/three|vendor/three|window\.THREE' \
    "$OUT/physics-field-guide" >/dev/null 2>&1; then
  USES_THREE=1
  [[ -d "$VENDOR_THREE" ]] || die "a chapter imports three.js but $VENDOR_THREE is missing"
  mkdir -p "$OUT/_lib/vendor/three"
  while IFS= read -r -d '' f; do
    rel=${f#"$VENDOR_THREE"/}
    copy_file "$f" "$OUT/_lib/vendor/three/$rel"
  done < <(find "$VENDOR_THREE" -type f -print0)
fi

# --- LICENSES / credits ----------------------------------------------------
{
  cat <<'EOF'
# Licences and credits

## LA-1940 (Fig. 1)

E. Fermi, J. Pasta, S. Ulam (with M. Tsingou), *Studies of Nonlinear
Problems, I*, Los Alamos report LA-1940, May 1955.

US Government work, public domain.
OSTI: https://www.osti.gov/servlets/purl/4376203
DOI: https://doi.org/10.2172/4376203

## Chapter code

Licensed as in the observatory repository (no separate licence file is
declared in this checkout).
EOF
  if [[ "$USES_THREE" -eq 1 ]]; then
    cat <<'EOF'

## three.js (r128)

Vendored only because an exported chapter imports it. MIT licence; fetched
from https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js.

Copyright © 2010-2021 three.js authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
EOF
  fi
} > "$OUT/LICENSES.md"

# --- generated root index (relative links only) -----------------------------
CHAPTERS_CSV=$(IFS=,; echo "${CHAPTERS[*]}")
python3 - "$OUT" "$CHAPTERS_CSV" "$FPUT_INCLUDED" <<'PY'
import html
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
slugs = [s for s in sys.argv[2].split(",") if s]
fput_included = sys.argv[3] == "1"
items = []
for slug in slugs:
    chapter = json.loads((out / "physics-field-guide" / slug / "chapter.json").read_text())
    title = html.escape(chapter.get("title") or slug)
    href = html.escape(f"physics-field-guide/{slug}/index.html")
    items.append(f'      <li><a href="{href}">{title}</a></li>')
study = ""
if fput_included:
    study = (
        '    <p>FPUT study report: '
        '<a href="study/fput-recurrence-reproduction/index.html">'
        "fput-recurrence-reproduction</a></p>\n"
    )
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Physics field guide</title>
<link rel="stylesheet" href="_lib/web/style.css">
</head>
<body>
<main>
  <h1>Physics field guide</h1>
  <p>Shareable chapters from the observatory physics field guide. Serve this
  directory over HTTP so the modules resolve.</p>
  <ul>
{chr(10).join(items)}
  </ul>
  <p><a href="physics-field-guide/README.md">Field-guide README</a>
  · <a href="LICENSES.md">Licences and credits</a>
  · <a href="reference/la-1940-fig1.png">LA-1940 Fig. 1</a></p>
{study}</main>
</body>
</html>
"""
(out / "index.html").write_text(page, encoding="utf-8")
PY

# --- self-check -------------------------------------------------------------
self_check() {
  local rel hits
  while IFS= read -r rel; do
    case "$rel" in
      *knowledgebase/*|*lineage*|*_data/*|*.orbit*|*/*.orbit*|*/.orbit*|*.env*|*/*.env*|*/.env*|*.git*|*/*.git*|*/.git*|*tests/*|*reference.py*)
        die "forbidden path in export: $rel"
        ;;
    esac
  done < <(cd "$OUT" && find . -mindepth 1)

  if hits=$(grep -rIl "/home/" "$OUT"); then
    echo "$hits" >&2
    die "absolute /home/ path in export"
  fi
  if hits=$(grep -rIlE "(BEGIN (RSA|OPENSSH|EC) PRIVATE|api[_-]?key|token=)" "$OUT"); then
    echo "$hits" >&2
    die "secret-looking string in export"
  fi

  python3 - "$OUT" <<'PY'
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

root = Path(sys.argv[1]).resolve()
ATTR_RE = re.compile(r"""\b(?:href|src)\s*=\s*(['"])(.*?)\1""", re.I)
IMPORT_RE = re.compile(
    r"""(?:import|export)\s+(?:type\s+)?(?:\{[\s\S]*?\}|\*\s+as\s+\w+|\w+)\s*from\s*['"]([^'"]+)['"]"""
    r"""|import\s*\(\s*['"]([^'"]+)['"]\s*\)"""
    r"""|import\s+['"]([^'"]+)['"]"""
)
SKIP_SCHEMES = {"http", "https", "mailto", "data", "javascript", "blob"}


def skip(url: str) -> bool:
    url = url.strip()
    if not url or url.startswith("#"):
        return True
    scheme = urlparse(url).scheme.lower()
    return scheme in SKIP_SCHEMES


def check(url: str, source: Path) -> None:
    if skip(url):
        return
    raw = url.split("#", 1)[0].split("?", 1)[0]
    if not raw:
        return
    if raw.startswith("/") or urlparse(raw).scheme:
        raise SystemExit(f"{source.relative_to(root)}: href/src/import leaves the export: {url!r}")
    target = (source.parent / raw).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise SystemExit(
            f"{source.relative_to(root)}: {url!r} resolves outside the export root"
        ) from exc
    if not target.exists():
        raise SystemExit(f"{source.relative_to(root)}: {url!r} does not exist in the export")


errors = 0
for path in root.rglob("*"):
    if not path.is_file():
        continue
    suffix = path.suffix.lower()
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    if suffix in {".html", ".htm"}:
        for _, url in ATTR_RE.findall(text):
            try:
                check(url, path)
            except SystemExit as exc:
                print(exc, file=sys.stderr)
                errors += 1
        for match in IMPORT_RE.finditer(text):
            url = next(g for g in match.groups() if g)
            try:
                check(url, path)
            except SystemExit as exc:
                print(exc, file=sys.stderr)
                errors += 1
    elif suffix == ".js":
        for match in IMPORT_RE.finditer(text):
            url = next(g for g in match.groups() if g)
            try:
                check(url, path)
            except SystemExit as exc:
                print(exc, file=sys.stderr)
                errors += 1
if errors:
    raise SystemExit(f"link check failed on {errors} target(s)")
PY
}

self_check

echo "field-guide export: ${#CHAPTERS[@]} chapter(s) -> $OUT"
printf 'chapters: %s\n' "${CHAPTERS[*]}"
