#!/usr/bin/env bash
# Serve the observatory root so sims can import ../../_lib/web and ../../_lib/vendor relatively.
# Usage: lab/tools/serve.sh [port]   (default 8000; gallery at /lab/gallery/)
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../../../.."
exec python3 -m http.server "${1:-8000}"
