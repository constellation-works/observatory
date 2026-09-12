#!/usr/bin/env bash
# Recreate la-1940-fig1.png from a verified temporary LA-1940 PDF.
set -euo pipefail

pdf_path="${1:?usage: extract_figure.sh /path/to/la-1940.pdf [output.png]}"
output_path="${2:-la-1940-fig1.png}"
expected_sha="3155813b1851da4fa6fba5818986718b197d68873d38965f3cd7489c14f396f1"
actual_sha="$(sha256sum "$pdf_path" | awk '{print $1}')"
[ "$actual_sha" = "$expected_sha" ] || {
  echo "unexpected LA-1940 PDF SHA-256: $actual_sha" >&2
  exit 1
}

temporary_dir="$(mktemp -d)"
trap 'rm -rf "$temporary_dir"' EXIT
gs -q -dSAFER -dBATCH -dNOPAUSE \
  -sDEVICE=pngalpha -r150 -dFirstPage=14 -dLastPage=14 \
  -sOutputFile="$temporary_dir/page-14.png" "$pdf_path"
python3 "$(dirname "$0")/crop_png.py" \
  "$temporary_dir/page-14.png" "$output_path" 210 300 1160 1300
