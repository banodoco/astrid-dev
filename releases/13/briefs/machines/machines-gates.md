# Candidate gates for the machines lane (Release 13 manager, binding)

1. **mypy net zero over Release 12 in machines files.** Release 13 added 102 findings over Release 12: `packs/runpod/machine.py` 28, `remote_placement.py` 18, `target_selection.py` 14, `worker_owner.py` 11, `adapter.py` 5, `generation.py` 4, `provider.py` 3, `core/execution/generic_host.py` 7, `core/machines_cli.py` 5, `installer/progress.py` 3. **The binding per-finding list** is `/home/user/wt/briefs/wave3/machines-mypy-new-findings.tsv` (path, code, message, count_delta; copied from astrid-dev `r13-progress/decision-log` `d0ed7ce`, `releases/13/evidence/tests/mypy/new-findings.tsv`). The introducing commit per file is in `machines-mypy-REPORT.md` next to it. Fix the rows for the files your card edits; match by path, code and message, since line numbers move. Fix the findings in the files your card already edits. No blanket ignores: any `# type: ignore[code]` carries a one-line reason. Measure with the venv's mypy (`pyproject.toml` pins `python_version = "3.11"` like CI): `/home/user/astrid-agent.env/venv/bin/python -m mypy <your files> 2>&1 | grep -c ': error:'`, before and after, on your card's files only and one mypy run at a time (the machine is shared). Report both counts per file. The count must fall by the listed R13 findings you fixed and must never rise.
2. **The core/pack boundary ratchet is never raised.** Release 13 added crossings in `astrid/core/execution/generic_host.py`, `machine_run.py` and `machines_cli.py`, from claim, keep and setup (`c0f505d4`, `d3c44023`, `74862541`, `4960d98d`) and from receipts (`09724310`). Move each crossing your card touches behind the existing neutral interface. If one needs a new interface, stop and report it; don't invent one. Never run `--write-baseline`. Check with `/home/user/astrid-agent.env/venv/bin/python scripts/check_core_pack_boundary.py --check` before and after, and report its output.

## Cross-check (optional): measure the Release 12 / Release 13 split yourself
Release 12 is `0e1543e0`. For the files your card edits:
```
git -C <your clone> worktree add --detach <your clone>-r12 0e1543e0
cd <your clone>-r12 && /home/user/astrid-agent.env/venv/bin/python -m mypy <files> 2>&1 | grep ': error:' | sed -E 's/:[0-9]+:( [0-9]+:)? error:/:/' | sort > $TMPDIR/r12.txt
```
Do the same in your clone, and compare by file and error code; line numbers move. The findings in your clone that are not in Release 12 are the ones to fix. Remove the `-r12` worktree when done (`git worktree remove --force`). A file that does not exist in Release 12 counts all its findings as Release 13's.

## Card ownership (manager)
- `remote_placement.py` (18), `provider.py` (3), `failure_receipt.py` (1) and `pod_fields.py` (1): the K1 follow-up card.
- `machine.py` (28), `adapter.py` (5), `generation.py` (4), `generic_host.py` (7) and `sdk/generation.py` (20): M2.
- `target_selection.py` (14): M2 and M6.
- `worker_owner.py` (11): M5.
- `machines_cli.py` (5) and the claim, keep and setup boundary crossings: M7.
- `installer/progress.py`: not this lane (IU-20, the test lane).
