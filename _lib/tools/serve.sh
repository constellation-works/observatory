#!/usr/bin/env bash
# Serve the observatory root so sims and chapters can import _lib/web and
# _lib/vendor relatively.
# Usage: _lib/tools/serve.sh [port]   (default 8000; gallery at /_lib/gallery/)
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
exec python3 -m http.server "${1:-8000}"
