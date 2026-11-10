#!/usr/bin/env bash
# Run one Agent test set at one commit, for a before/after comparison (Release 12, A2).
# Usage: env/cmp-run.sh <agent-clone> <label> <commit> <outdir> [pytest selectors...]
# Makes a worktree <outdir>/wt-<label> at <commit>, builds its env with the checkout's own
# scripts/worker-env/agent-setup.sh (Runtime and VibeComfy at the checkout's pins), runs pytest
# with -rA, and writes <outdir>/<label>.log. Compare logs with env/baseline-diff.py.
# Run several labels in parallel (one per commit). Exit 3 = environment problem.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)   # astrid-dev env/
CLONE=${1:?agent clone}; LABEL=${2:?label}; COMMIT=${3:?commit}; OUT=${4:?outdir}; shift 4
SEL=("$@")
[ ${#SEL[@]} -eq 0 ] && SEL=(tests/core/pack tests/core/execution tests/test_generic_host.py)
mkdir -p "$OUT/tmp-$LABEL" || exit 3
avail=$(df -k "$OUT" | awk 'NR==2{print $4}')
[ "$avail" -lt 3000000 ] && { echo "less than 3 GB free on $OUT" >&2; exit 3; }
WT="$OUT/wt-$LABEL"
git -C "$CLONE" worktree remove --force "$WT" 2>/dev/null
git -C "$CLONE" worktree add -q --detach "$WT" "$COMMIT" || exit 3
cd "$WT" || exit 3
SETUP=scripts/worker-env/agent-setup.sh; PYT=scripts/worker-env/agent-pytest.sh
# Older commits (e.g. R10 72462b04) predate the in-repo copies: use astrid-dev's env/ copies.
[ -f "$SETUP" ] || { SETUP="$HERE/agent-setup.sh"; PYT="$HERE/agent-pytest.sh"; }
bash "$SETUP" || exit 3
# Existing test paths only: older commits may not have every selector.
PATHS=(); for p in "${SEL[@]}" $(ls tests/test_installer_*.py 2>/dev/null); do [ -e "${p%%::*}" ] && PATHS+=("$p"); done
TMPDIR="$OUT/tmp-$LABEL" PYTEST_ADDOPTS=-rA bash "$PYT" -q -p no:cacheprovider --basetemp="$OUT/tmp-$LABEL/run" \
  --ignore=tests/core/pack/test_build_hook_contract.py -k 'not browser' "${PATHS[@]}" > "$OUT/$LABEL.log" 2>&1
rc=$?
rm -rf "${OUT:?}/tmp-$LABEL"
tail -1 "$OUT/$LABEL.log"
exit $rc
