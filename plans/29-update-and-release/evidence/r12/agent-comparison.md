# Agent before/after comparison method (release 12)

[Handoff](../../handoff.md) · [Tasks](../../tasks.md)

Every Agent batch is compared locally against the candidate it lands on, and against served R11 (`a105de3a`) and R10 (`72462b04`), on one fixed test set. A failure present only after the batch is a regression and blocks the push. A failure present on the candidate but passing on R11 or R10 is a release-12 regression and is fixed in release 12 (owner decision D8). A failure on all three goes to Plan 39 with its cause, after checking the messages match.

Limits: older versions run against today's environment (venv, Runtime `9fc53b77` from `runtime.lock.json`, vibecomfy), so an environment-only failure on R11/R10 can mask a regression. The Agent CI comparison against R10 in the final round is authoritative.

## Environment

- A venv with the Agent's test dependencies (pytest; xdist not needed), plus checkouts of the Runtime at the lock's revision and vibecomfy. Tests run with `PYTHONPATH` set to the Agent checkout.
- Excluded because they need pinned Node/esbuild env vars: `tests/core/pack/test_build_hook_contract.py` and the browser cases in `tests/core/pack/test_transaction.py`.
- Known order-dependent pair: `test_installer_bootstrap_imports` and `test_portable_python_action_and_dependency_use_snapshots[True]` fail only inside one large combined run, and pass alone, on every candidate.

## Script (`cmp-run.sh <label> <commit>`)

```bash
# Usage: cmp-run.sh <label> <commit>  — run the comparison set at <commit> and write the sorted failures.
set -u
S=${SCRATCH:?}
L=$1; C=$2; W=$S/cmp-$L
cd $S/merge/agent && git worktree remove --force $W 2>/dev/null; rm -rf "${W:?}"
git worktree add -q --detach $W $C || exit 1
mkdir -p $W/.tmp; cd $W
export TMPDIR=$W/.tmp PYTHONPATH=$W
PATHS=(); for p in tests/core/pack tests/core/execution tests/test_generic_host.py tests/sdk/test_host_attach_rejection.py \
  tests/sdk/test_timeline_element_schema_resolution.py $(ls tests/test_installer_*.py); do [ -e "$p" ] && PATHS+=("$p"); done
$VENV/bin/python -m pytest -q -p no:cacheprovider --basetemp=$W/.tmp/run -rfE "${PATHS[@]}" \
  --ignore=tests/core/pack/test_build_hook_contract.py --deselect tests/core/pack/test_transaction.py -k 'not browser' \
  > $S/cmp-$L.log 2>&1
grep -E '^(FAILED|ERROR) ' $S/cmp-$L.log | sed 's/ - .*//' | sort -u > $S/cmp-$L.fails
tail -1 $S/cmp-$L.log > $S/cmp-$L.summary
cd $S/merge/agent && git worktree remove --force $W; rm -rf "${W:?}"
echo "done $L $(cat $S/cmp-$L.summary)"
```

Set `SCRATCH` (work area holding the Agent clone at `merge/agent`) and `VENV`. Compare with `comm -13 cmp-base.fails cmp-merged.fails` (new failures) and `comm -12 cmp-base.fails cmp-r11.fails` (shared with R11).

## Results so far

- **Base `313bbd46f`:** 158 failed, 4,741 passed, 21 skipped, 47 errors (205 failing ids). By file: `test_installer_busy_fence` 59, Runtime custody d40 tests 45, `test_installer_acl` 14, `test_r8_prod_refusals` 13, `test_installer_app_update` 10, about 30 files with 1–6 each.
- **Batch `733ac5a43` (`r12/cand-next`), R11 and R10:** recorded in [tasks.md](../../tasks.md#release-12-round-5-state-at-1700z-2026-11-10) when they finish.
