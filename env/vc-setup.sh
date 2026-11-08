#!/usr/bin/env bash
# Shared astrid-dev utility for single-repo cloud workers; see env/README.md. Copied from plans/02-consistent-generation/env/, unchanged below this line.
# Run from the root of a VibeComfy checkout. Builds <checkout>.env/ next to the checkout (never inside it).
# Needs: uv, git, network reads to PyPI. Any failure here is an ENV error, never a test result.
set -euo pipefail
for t in uv git; do command -v "$t" >/dev/null || { echo "ENV: missing tool $t" >&2; exit 3; }; done
CO=$(pwd -P); E="$CO.env"
grep -q '^name = "vibecomfy"' "$CO/pyproject.toml" 2>/dev/null || { echo "ENV: not a VibeComfy checkout: $CO" >&2; exit 3; }
rm -rf "$E"; mkdir -p "$E/home" "$E/tmp" "$E/cache" "$E/basetemp"
UV_PROJECT_ENVIRONMENT="$E/venv" uv sync --frozen --extra dev --python 3.13 --project "$CO"
uv pip install --python "$E/venv/bin/python" --exclude-newer 2026-10-31T00:00:00Z pip "build==1.4.0" "hatchling>=1.20"
dirname "$(command -v uv)" > "$E/uv-dir"
"$E/venv/bin/python" -c 'import sys, vibecomfy; print(sys.version.split()[0], vibecomfy.__file__)' > "$E/setup.txt"
cat "$E/setup.txt"
