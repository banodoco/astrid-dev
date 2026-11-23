> **Where things are in this folder.** The links below were written for the original run container. Here, `../failing-first.log`, `../pb7b-*.log`, `../mmap-stat-repro.{py,txt}` and `../profile.md` are in [`logs/`](logs/) (with the PB-7c focused and count-hook logs and the rejected follow-up diff); the PB-7b timing before the repair (6.2597 s to 4.9344 s, saving 1.3253 s) is in [`timing-pb7b-prefix/`](timing-pb7b-prefix/); the repaired-head timing (6.234 s to 5.064 s, saving 1.170 s) is in [`timing-pb7c/`](timing-pb7c/); the PB-7a trace is in [`trace/`](trace/). The product code is astrid-agent PR #557, branch `p81/pb7b-discover-once`, head `9e243ac4`. Local `/home/user/...` paths do not exist outside that container.

# PB-7b handoff: RN-4

## Branch and disposition

- Review target: #557, branch `p81/pb7b-discover-once`.
- Current product head: `9e243ac48` (`Preserve admission and custody during scoped pack discovery`). The corrected PB-7c head contains the latest admission-order fix.
- PB-7b is parked. No further attempts or merge work are authorized by this handoff.
- Intended destination: Plan 87, RN-4 session, via the orchestrator only. This document does not send or authorize an external message.

## Review admission-order reproduction

The original review regression and its test live in `tests/core/pack/test_discovery_admission_order.py`. The saved failing-first output is [`/home/user/p81b/run/pb7c/failing-first.log`](../../pb7c/failing-first.log). It demonstrates that scoped discovery evaluated dirty managed inventory before refusing a duplicate pack ID, and that cached discovery/projection paths missed a pending transaction busy refusal. The exact expected failures were 3 failed / 3 passed / 4 deselected in the selected shard; the failing cases were:

- `test_action_entries_refuse_duplicate_before_dirty_managed_inventory[True]`: raised `SourceSetupError: dirty managed checkout` instead of `PackValidationError` for duplicate `generation`.
- `test_discovery_refuses_busy_collection_after_warm_metadata[True]`: no `PackInstallError` after the pending exchange.
- `test_action_entries_refuse_busy_collection_after_warm_projection[True]`: no `PackInstallError` after the pending exchange.

The corrected focused follow-up is recorded in [`../pb7b-root-followup-focused.log`](../pb7b-root-followup-focused.log): 33 passed. The admission-order scope log [`../pb7b-admission-scopes.log`](../pb7b-admission-scopes.log) records 11 passed. The broader final source logs include [`../pb7b-admission-final.log`](../pb7b-admission-final.log) (27 passed), [`../pb7b-review-fix-final.log`](../pb7b-review-fix-final.log) (34 passed), and [`../pb7b-command-compat.log`](../pb7b-command-compat.log) (command compatibility, 11 passed).

A compact runnable reproduction script is in this directory. From any shell with the project test dependencies installed:

```sh
./reproduce-admission-order.sh /path/to/base/source /home/user/p81b/wt/pb7b
```

It runs only the three review test families, parameterized for scoped and unscoped discovery. The original saved failing-first run above is the baseline receipt: expect the three scoped regressions to fail, while the corrected candidate is expected to pass all six selected cases. The script intentionally does not run here as requested. The candidate source checkout is `/home/user/p81b/wt/pb7b`; the matching pre-correction source snapshot is retained at `/home/user/p81b/box/pb7-merged/sources/agent-B-pb7c` if a future reviewer wants to reproduce both sides. That snapshot may require selecting the exact earlier base revision if it has since been updated.

## Review findings and coverage

- **Directory-name reuse and mmap/stat:** a direct Linux reproduction exists at [`../mmap-stat-repro.py`](../mmap-stat-repro.py), with its saved observation in [`../mmap-stat-repro.txt`](../mmap-stat-repro.txt). The review discussed the weakness of relying on directory metadata witnesses (mtime/ctime/stat) to validate cached immediate names, including mmap-related metadata behavior. This deserves renewed scrutiny if broadening or changing the witness; it is not a claim that the reproduction invalidates the current narrow Linux behavior.
- **Command-boundary coverage:** the scope is command-local, and nested command entry/exit compatibility received focused regression coverage. The saved suite receipts above include scope and compatibility runs. Keep checking that reuse cannot cross a command boundary or leak across nested commands.
- **Admission order:** duplicate declarations must be rejected before managed-source inventory validation, preserving the duplicate `PackValidationError` even when managed inventory is dirty. Busy transactions must also be checked after warm metadata and warm action projections.
- **Transaction-busy behavior:** both metadata discovery and `action_entries()` need to refuse a pending managed exchange consistently, including when a scoped cache/projection is warm. The three reproduced regressions above cover the original missed refusals.

## Timing evidence

- Earlier PB-7 receipt: [`/home/user/p81b/box/pb7/evidence/timing-run-1/RUN-1-RESULT.md`](../../../box/pb7/evidence/timing-run-1/RUN-1-RESULT.md). Five-sample medians were A `6.2597 s` and B `4.9344 s`, saving `1.3253 s`; this is earlier than the corrected-head result and must not be described as the final head's timing.
- Corrected PB-7c A/B receipt: [`/home/user/p81b/box/pb7-merged/evidence/pb7c-run-1/summary-ab.json`](../../../box/pb7-merged/evidence/pb7c-run-1/summary-ab.json), with supporting raw records and setup receipts in the same `pb7c-run-1` and `receipts/pb7c` directories. A median `6.234 s`; B median `5.064 s`; saving `1.170 s` (18.8%). The recorded qualification failed its `1.3 s` median-savings gate, so this is evidence of an improvement, not acceptance under that gate. The run used installed CPU builds, a stand-in ComfyUI, and `--no-wait`; it does not establish real ComfyUI node-info behavior or GPU work. It also records runtime source/listener attestation as off.
- PB-7a trace limitation: [`/home/user/p81b/run/pb7/attempt-20261123-profile3/trace.json`](../attempt-20261123-profile3/trace.json) directly traced 15 of 16 timed `pack discovery` calls. The unmatched 16th call is source-level inference at [`/home/user/p81b/wt/pb7b/astrid/sdk/generation.py:1801`](../../../wt/pb7b/astrid/sdk/generation.py:1801), where `discovery.users` is passed to `timed_call("pack discovery", ...)`; it was not directly mapped to a traced frame. See [`/home/user/p81b/run/pb7/profile.md`](../profile.md) for the timing attribution limits.

## Accepted residuals and next handoff

PB-7a's remaining discovery-call attribution is 15/16 traced; the 16th `discovery.users` source attribution remains inference. The timing result is below the PB-7c 1.3-second gate, and the test proof does not cover real ComfyUI answers or GPU work. Keep these as explicit residuals for RN-4 review; do not imply they are resolved by the admission-order fix.

The next owner is the Plan 87 RN-4 session, launched and routed only through the orchestrator. This handoff records the evidence and current state; it does not request more profiling, attempts, tests, or a merge.
