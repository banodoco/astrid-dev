#!/usr/bin/env bash
# TEST runner for every VibeComfy card. Run from the checkout root after vc-setup.sh. Args go to pytest verbatim.
set -euo pipefail
CO=$(pwd -P); E="$CO.env"
test -x "$E/venv/bin/python" || { echo "ENV: run vc-setup.sh first in $CO" >&2; exit 3; }
BT="$E/basetemp/$(date +%s%N)"
# env -i wipes the caller env: pass through what verify.sh sets (PYTEST_ADDOPTS="-rA ..." gives per-node PASSED lines;
# VERIFY_SIDE = base|head). TMPDIR stays $E/tmp: <checkout>.env is already per side and per run.
exec env -i PATH="$E/venv/bin:$(cat "$E/uv-dir"):/usr/local/bin:/usr/bin:/bin" HOME="$E/home" TMPDIR="$E/tmp" \
  PYTEST_ADDOPTS="${PYTEST_ADDOPTS:-}" VERIFY_SIDE="${VERIFY_SIDE:-}" \
  XDG_CACHE_HOME="$E/cache" LANG=C.UTF-8 PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 \
  "$E/venv/bin/python" -m pytest -p no:cacheprovider --basetemp="$BT" "$@"
