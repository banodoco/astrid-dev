difficulty: terra (X, write)

# M7: `astrid machines` and `astrid machines show NAME` show the job, queue, wait reason, expiry and cost, as data

**Repo:** Astrid. **Clone:** `/home/user/wt/c-m7` (branch `r13/machines-m7`, base `r13/machines` at `__BASE__`, which includes M1–M5). Work in this clone only.

Read first (binding): `/home/user/wt/briefs/wave3/machines-design.md` (owner decision O8: "people can view the machine and what's actually happening on it"; the target experience lines for `astrid machines` and `astrid machines show bjork`; and "every failure or wait understandable from the product") and `/home/user/wt/briefs/wave3/machines-plan.md` (row **M7** and "Reuse: Show").

## Outcome
1. **`lease_row` carries the data** (`astrid/packs/runpod/machine.py:lease_row`): name (M3), GPU, datacenter, state, the current job (task id, entry or kind, phase, started at), the queue (count and task ids of Runtime tasks waiting for this machine), the wait reason when the machine is waiting (for stock, for preparation, for a job), the idle and paid expiry with which one ends it next, the idle time, the cap, the rate, and the cost so far. Fields are plain data; `--json` prints them.
2. **`astrid machines`** lists one row per machine: name, GPU, datacenter, state, current job, queue length, time left, cost. Keep `render` simple; M8 does the final layout and wording.
3. **`astrid machines show NAME`** (name or id) prints the same row in full, plus the queue's task ids, the last job's outcome and failure summary (the stored safe summary only, never secrets; reuse `failure_diagnostics.safe_stored_summary`), where the failure receipt and logs are, and the expiry, cap and cost. An unknown or ended name gives one line naming `astrid machines`; an ended machine still shows its ended reason.
4. **Sources:** the lease journal (no provider call), Runtime tasks filtered by `policy.machine` (or, for the single Release 13 machine, the tasks on the GPU queue), the host's progress where it is already recorded, and the failure receipts. Read only: `show` must never call the provider, start a host, or change state.

## Out of scope
Final layout, column names and wording (M8); docs (M9); several machines per account (M12); integration tests (M10: list what breaks, don't edit).

## Tests
New `tests/core/test_machines_show.py` (must fail before, pass after): an idle machine; an active machine with a running job and two queued; a machine waiting for stock with its reason; an ended machine with its ended reason and last failure summary; an unknown name; `--json` carrying every field; and a check that `show` makes no provider call and writes nothing. Proof, from `/home/user/wt/c-m7`, before (new file excluded) and after:
```
TMPDIR=$PWD/.tmp-tests PYTHONPATH="$PWD:/home/user/wt/vibecomfy-fe92ac7" /home/user/astrid-agent.env/venv/bin/python -m pytest -q tests/core/test_machines_show.py tests/core/test_machines_claim.py tests/core/generation/test_cli.py tests/core/generation/test_placement_machine_name.py --basetemp=$PWD/.tmp-tests/pt
```
Then ruff and `git diff --check`.

__RULES__
