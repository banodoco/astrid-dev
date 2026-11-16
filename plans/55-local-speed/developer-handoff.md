# Plan 55 developer handoff — 16 November 2026

[Plan](plan.md) · [Accepted decisions](inputs.md#owner-decisions) · [Task record](tasks.md) · [Review record](review.md)

This is the continuation and issue-reproduction guide requested by the owner. It is **not a completion submission, independent review, or replacement run**. Read the latest owner replies and current PR heads before changing anything. This dated guide explains the evidence and unresolved work; `tasks.md` remains the task-completion record. Only LS-11 is complete. Incomplete code, a draft PR, a passing calibration, and a microbenchmark do not complete a speed task.

## Final verified checkpoint — later on 16 November 2026

The Linux report-loss issue below is **resolved for the exact checked candidate**, not an open execution blocker. [Run 43918996289](https://github.com/banodoco/astrid-agent/actions/runs/43918996289), Linux job `133480864758`, completed successfully on Agent task head `dbf713822ced58f4e48416ddf32bece2af8430fd`; its checked PR merge was `62f9d67e0a06b0b101be6f4b62f0806a00580e9f`. Runtime, VibeComfy and lifecycle pins remain unchanged. The original downloaded artifact `14254042311` matches SHA-256 `5e349b655b203c2d010647a045e0d040487ba8590a762d86450f00ff292215e8`; both archived member manifests were verified. The [indexed result](evidence/continuation-20261116/linux-meter-43918996289.json) names the raw summary member and its SHA-256 `207c1865902d8004fb890f6f3a4950c12705ea51798973f748baa4d686477c50`. This derived index does not replace the original summary/trace/log/JUnit archive; the owner bundle retains the original summary bytes.

Actual results: 72 observer/collector cases passed; the separate latency invocation and instrumented invocation each passed both SDK and CLI generation cases, with zero JUnit failures, errors or skips. Both have distinct warmup/measured succeeded task IDs and verified caller-local outputs. Instrumented observations have zero reported observer/native coverage gaps and no failed native flushes. The previously missing worker telemetry is present.

| Actual second-job observation | Resident SDK | Fresh Python CLI |
| --- | ---: | ---: |
| Uninstrumented wall seconds, one sample, not a median | 22.279750706 | 16.829192314 |
| Requests to ComfyUI | 13 | 13 |
| Non-thread process starts, independently matched in native relations | 8: 1 pack worker + 7 other | 9: 1 CLI + 1 pack worker + 7 other |
| Workflow compile / bundle compile / emission calls | 8 / 2 / 3 | 8 / 2 / 3 |
| Observed completed Python output-hash streams | 25 | 25 |
| Successful native flushes in the instrumented caller interval | 166: 150 fsync + 16 fdatasync | 162: 150 fsync + 12 fdatasync |

These are **baseline observations, not an optimization result**. The fixture output is a **16×16 PNG of 82 bytes**, not the one-megapixel D1 workload. Counts come from a separate instrumented run, which substantially slows this workload and changes background activity. Runtime/host are fixture-process threads; flush/sleep totals cover activity in the interval rather than a causally isolated transaction budget. Python hash coverage does not prove arbitrary native hashing. Queue time is not subtracted. Repeated baseline/tolerance, representative output coverage and remaining attribution are still needed; `budget_certified` remains false and LS-2 is not complete.

Windows job `133480865371` is deliberately failed at the hold step: the previously refused generation command was skipped, not retried. Native calibration and pure checks do not qualify Windows generation. The Windows fixture diagnosis below remains source-backed but unproven by a corrected live run.

The preceding handoff commit `f5b4c2f07e8a7d0ce2559a89a73854dc0bbd9e67` passed both documentation and App-consumer jobs in run `43921655593`. That result applies to that exact commit; this checkpoint update requires its own repository check and hosted status. It is not independent review or merge approval.

## Resume the same work

Run: `2026-11-15-local-speed`. Accountable manager: `chatgpt-workspace-6ee41b0f0cca/root`. The original workspace is `/workspace/scratch/6ee41b0f0cca`; the local run configuration is `plans/55-local-speed/.otto/runs/2026-11-15-local-speed/run.yaml`; the unfinished original LS-2 worker is `worktrees/agent-meter-next`. Those were unavailable during this continuation. Do not invent their contents, reset their state, overwrite them, or claim that worker's diff/proof. A recovered source snapshot is not that original worktree. Route bindings are unknown here; direct manager checks are not independent N checking. RS1 and final R each remain **0/1**. Spend is **$0**. Plan 54 remains queued.

The owner's branch ruling replaces `int/55-local-speed` with **`release/14/plan-55`** in Agent, VibeComfy and astrid-dev. Task PRs target that plan branch. Product integration drafts target `release/14/main`, not product `main`. Integration drafts are [Agent #358](https://github.com/banodoco/astrid-agent/pull/358), [VibeComfy #172](https://github.com/banodoco/VibeComfy/pull/172), and [astrid-dev #753](https://github.com/banodoco/astrid-dev/pull/753). Do not push the old int branch. Incorporate new work by merge, never rebase, amend or force-push. Do not promote an integration draft without its authorization and checks. Every PR names Plan 55.

At this checkpoint the plan branches retain Agent `cb1a590e0008dde7e3fc2d3fbf341ef98401b32a`, VibeComfy `7fde33e2523281f840121b93a8a865a7f5d847de`, and dev `ab73cc12c8d90762e8e6e7e664ff5a32a360cc0d`. These are not all the dependencies used by the installed product: **Agent still pins VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b` and Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`**. The ComfyUI source used in the CPU floor is `6bfaacc67c2103481e5f0c84d75257cd0581d86a`. Do not silently substitute release-branch tips for those pins.

## Read these candidates rather than rebuild them

| Task contribution | Existing PR / exact candidate | What is actually available | What still prevents completion |
| --- | --- | --- | --- |
| Real ComfyUI CPU floor | [Agent #353](https://github.com/banodoco/astrid-agent/pull/353), `975a770ed5e26632bc5f7b271ebe665d6685065b` | Successful Linux and Windows CPU run 43858887774; six twenty-sample cells per OS, separately retained warmup | Not an installed-Agent meter, GPU result, or representative video qualification; task PR remains draft |
| Floor table and this handoff | [dev #756](https://github.com/banodoco/astrid-dev/pull/756), floor-record parent `3f3ecf754e5142b9f0658a1583dba2c39ba183b6` | Measured table replaces estimates; original source/artifact hashes in the [CPU summary](../../releases/14/evidence/ls1/real-cpu-20261116.json) | Review/merge and task-record reconciliation remain; an earlier chat called this #754 incorrectly |
| Running cancel refusal and corrected Python hash observation | [Agent #355](https://github.com/banodoco/astrid-agent/pull/355), `5d600a7cf77ec57799449b8241122b99af04167c` | Linux hosted selection: 74 baseline / 113 candidate passing tests; 39 new Windows cases passed | Existing Windows fixture failures, independent checking, real-Comfy cancellation proof and the other LS-9 cases remain |
| Child/Runtime/CLI, compile/emission, hash and native-flush observation | [Agent #359](https://github.com/banodoco/astrid-agent/pull/359), `dbf713822ced58f4e48416ddf32bece2af8430fd` | Native calibration, observation helpers, separate timing/count runs and repaired report capture | Linux generation/report capture passed at the exact checkpoint above; tolerance, attribution and Windows generation remain open |
| Cheaper fingerprint traversal | [Agent #361](https://github.com/banodoco/astrid-agent/pull/361), `33f269e424c6a04f3c49b1c8ae7ca750a71db373` | Full-content-compatible scandir walk; 16 focused cases pass on base and candidate | Complete affected-file checking, Windows proof and first-job meter effect; most of LS-12 remains |
| Earlier preparation | [dev #719](https://github.com/banodoco/astrid-dev/pull/719), `6309ad6ef546221a90899cef3e845a0726097de3`; [dev #729](https://github.com/banodoco/astrid-dev/pull/729) | Retained recovery/opt-in evidence; an earlier CPU execution proposal | Historical supporting work, not completion. Do not launch a duplicate floor run or recreate archived evidence |

The two hash-observer files in #355 and #359 are shared identical inputs, not separate competing implementations. Preserve their identity when combining those task branches. Do not push a qualifying ref while its current CI is in flight. All listed task PRs are drafts at this checkpoint; no new task is claimed merged.

## Issue P55-WIN-DACL — Windows generation is refused before any job

**Classification:** permission/security refusal; unresolved. A successful native calibration is not Windows generation proof. Owner approval is required before retrying or making permission-related changes.

**Exact failing tuple and evidence:** Agent `b79080f03b0c0d5e0d3930bb0dfb841629ea3d71`, Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`, VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b`; [run 43913596410, job 133461734871](https://github.com/banodoco/astrid-agent/actions/runs/43913596410/job/133461734871). Artifact `14247918947`, archive SHA-256 `b9bfafd6a8e953cf1ee1d3da9112a15ab22c53c16853e6a5a73dd140aca10946`. The archive retains exact commands, logs and calibration, including `plan55-meter-proof/summary.json` and its child command records. The [original refusal report](https://github.com/banodoco/astrid-agent/pull/359#issuecomment-6923395281) identifies both caller cases.

The refused command is reproduced here for diagnosis, **not as permission to execute it again**:

```text
python -m tests.local_speed_meter_run --output plan55-meter-proof --timeout 1800
```

Its inner integration test reaches `real_runtime()` → `RuntimeDaemon.start()` → `discovery.publish()` → `windows_security.private_directory()` and raises:

```text
PermissionError: [Errno 13] unsafe Windows owner/DACL: a protected, non-NULL DACL is required
```

Both SDK and CLI cases stop before generation. Windows generation latency and counters are **NO-RESULT**, not zero. Short source paths and the 58 then-existing observer tests passed before this failure. WPR calibration observed four completed successful flushes with zero reported event/buffer loss. Those successes do not bypass the Runtime security requirement.

**What was already tried:** an earlier run had an overlong Vibe checkout path; an extra cleanup then raised WinError 5 on a read-only shared Git pack. The source fixture was changed to short, private, pytest-owned paths while retaining the exact pin checks and removing that redundant deletion. The refused deletion was not retried. The new DACL failure is separate, not evidence that the path fix failed.

**Source-backed likely cause, not a proven repair:** Agent `cb1a590e` [tests/conftest.py:167–190](https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/tests/conftest.py#L167-L190) creates the support directory with `mkdir` and then `chmod(0o700)`. [Python 3.11 documents](https://docs.python.org/3.11/library/os.html#os.chmod) that Windows chmod controls only the read-only flag, not the protected owner-only DACL. Pinned Runtime's [private_directory](https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/runtime_protocol/windows_security.py#L237-L252) creates a new directory with its restricted security descriptor, but validates an existing directory rather than silently repairing its ACL. The successful standalone CPU-floor probe did not pre-create that support leaf. This explains a concrete fixture mismatch consistent with the observed refusal.

**Proposed next action, subject to owner approval:** retain POSIX setup; on Windows let the existing pinned Runtime securely create a fresh pytest-owned support leaf, or invoke its existing checked creation API before startup. Continue refusing an already-existing unsafe directory. Ask the owner to approve this fixture-only secure-creation correction and the exact refused meter command before implementing/retrying it. No Runtime re-pin is proposed. Read existing Windows fixes first; do not assume a database-mode fix also fixes discovery-directory DACLs. No permissions or credentials were changed, no elevation occurred, and this proposal has not been executed.

**Acceptance after approval:** prove that the actual directory has the required owner and protected non-NULL DACL, keep negative security tests refusing unsafe directories, then run the original two caller cases on the approved exact tuple. Require valid outputs, distinct succeeded task records and complete counters. Do not monkeypatch the security check, broaden the DACL, elevate privileges, or substitute calibration for generation.

**Enforced hold:** #359 at `dbf71382` skips execution of the refused Windows generation command, writes an explicit NO-RESULT summary referencing the original refusal, and fails the lane rather than manufacturing green. Pure observer tests and native calibration are separate. The hold must not be removed merely because another task is pushed.

## Issue P55-LINUX-REPORT — generated outputs passed, child telemetry was missing

**Classification:** meter evidence defect, resolved on the checked Linux run described in the final checkpoint above. The original failure and repair are retained below; LS-2 qualification remains incomplete.

**Original failure:** Agent `b79080f03b0c0d5e0d3930bb0dfb841629ea3d71`, [run 43913596410, job 133461735511](https://github.com/banodoco/astrid-agent/actions/runs/43913596410/job/133461735511). Artifact `14250700646`, archive SHA-256 `a9584b7b3df1e1238c5e1b7cee12c780062c455154b3e82d188e401ef2ed7dfd`. Both instrumented caller cases rejected a missing pack-worker process report (PIDs 73150 and 90093 in that run), despite valid output and succeeded task assertions. Do not retain their partial hash/compile totals as a complete baseline.

Uninstrumented second jobs in that run were **25.240420932 s SDK** and **18.104983477 s CLI**, with 13 Comfy requests each. The preceding run observed 34.1666 s and 22.3641 s. These are single samples under different host conditions, **not medians or an optimization comparison**. Instrumented durations must never be used as latency evidence.

**Code finding and repair:** the old meter searched `tmp_path.rglob("job.stderr")` after delivery. Normal `_cleanup_ephemeral_attempt` can delete the successful attempt and its `.host-logs/job.stderr` before that scan. The new `tests/_local_speed_capture.py` observes `_TaskOutputCapture._receive` and retains only bounded prefixed stderr telemetry in memory before cleanup. The original drain executes first, preserving its bytes, return value and exceptions. No source-admission, environment, descriptor, worker permission or cleanup policy changes. This is an evidence-backed collection failure mode; the full repaired run must still show it resolves the observed missing reports.

Focused proof on `dbf713822ced58f4e48416ddf32bece2af8430fd`: **14 cases passed**, including the real host drain followed by deleting its attempt directory. Split lines, interleaved children, malformed UTF-8, truncation, oversized lines, stream/report limits and original drain failures are covered. Source files and raw test proof are retained with the continuation evidence.

```text
python -m pytest -q -rA tests/core/generation/test_local_speed_report_capture.py --junitxml=report-capture-final.xml
```

**Next action:** use the completed repair run and preserved summary from the final checkpoint; do not rerun it merely to rediscover the same result. Establish repeated baseline/tolerance and the remaining attribution needed for LS-3. Linux job `133480864758` passed; Windows job `133480865371` is intentionally held, not a fresh DACL retry. On any later candidate, inspect inner exits, both caller cases, report PIDs/timestamps and native loss accounting. An absent child must still be traced through installation, emission, draining and matching, never removed from the expected count.

**Acceptance:** both Linux caller cases have valid separate warmup/measured outputs and succeeded tasks, exactly the expected child/CLI starts, complete compile/emission and output-hash streams, zero observation gaps, and native flushes joined within each caller interval. Missing, overflowed, truncated or post-reply evidence remains an error. Then set an explicit baseline/tolerance from actual repeated observations and distinguish a baseline regression budget from the later zero-repeat warm-path target.

## Issue P55-LS12-PROOF — traversal improvement is not complete first-job optimization

**Classification:** bounded implementation available; broader proof and work remain. Candidate #361 is based on Agent `cb1a590e`, with no dependency changes.

The new walk uses `os.scandir` and within-walk metadata to reduce Path allocation. It **still hashes every regular file on each lookup**. The exact old algorithm is the compatibility oracle; same-size changes with restored timestamps are detected. It is not yet the verify-on-admission mechanism and must not be described as one.

```text
python -m pytest -q -rA tests/core/pack/test_discovery_fingerprint_walk.py --junitxml=fingerprint.xml
```

Sixteen cases pass on original and candidate code, through ordinary repository conftest. A twenty-pair alternating microbenchmark on the recovered bundled pack tree retained the identical digest in all forty calls: median **153.065633 ms base / 100.8692475 ms candidate**, maximum **520.071165 / 133.433054 ms**. This is a component microbenchmark, not a generation improvement or LS-12 acceptance. Do not compare it directly with another host's earlier 92.77/66.82 ms observation.

The existing selector below fails on **both** the actual base and candidate: it expects one manifest load but sees two, the demo manifest and bundled `hivemind`. It is a recorded matching baseline failure, not fixed by weakening the assertion:

```text
python -m pytest -q -rA tests/core/generation/test_discovery_scope.py::test_cli_scope_is_per_dry_run_and_is_reset_on_failure
```

An earlier wider-file attempt was interrupted; its other failures remain unclassified and its overall result is NO-RESULT. The normal focused checks above are separate completed runs, not a relabeling of that interrupted attempt. The repository's `env/baseline-diff.py` compared their combined 17 test IDs per side: zero regressions, zero missing IDs and that one pre-existing failure, exit 0; this does not make either failed job green. Local Python was 3.13.5 and pytest 9.0.2; pytest-timeout was absent, producing the recorded unknown-config warning, so explicit external process timeouts bounded the checks.

**Next action:** run the affected discovery/projection files against the exact base and candidate on hosted CI, preserving the existing oracles and complete results. Check platform filename ordering and symlink cases on Windows without invoking the refused Runtime startup. Merge only after scoped proof and independent checking. Then measure the first job with the standing meter. Continue the remaining LS-12 work: verify admitted immutable pack bytes once, retain the content guarantee for development edits, remove per-job git processes, load only the named workflow and avoid repeated emissions. No speed target is fulfilled by this traversal change alone.

## Approval requests that remain open

**LS-5:** approve changing Agent's VibeComfy pin from `dba38f86` to `7fde33e2523281f840121b93a8a865a7f5d847de` so the held transport is importable; the risk is cross-version compatibility, requiring regenerated recipe digests and composed-path proof. See the [exact proposal](evidence/ls5-repin-request.md). The Vibe code already on its plan branch does not change the Agent's pin. Repeated general instructions to continue are not this explicit approval.

**LS-6:** approve the [bounded receipt/streaming/thumbnail scope proposal](evidence/ls6-scope-request.md) across Agent, VibeComfy and Runtime; the risks are output integrity, mutation during transfer and durable thumbnail admission after caller exit. Retain current verification and worker authority until reviewed replacements pass. The corrected Python hash test observes six cumulative output hash streams in its existing small fixture; it does not show one pass. No writable CAS alias, untracked thumbnail thread, wider worker permissions or success-before-durability is approved.

The exact Windows permission retry is a third, distinct owner gate. No paid action, GPU rental, tester engagement, publication, product-main merge or additional re-pin is authorized by this guide.

## Remaining plan work and order

D9 and the owner's subsequent ordering correction supersede older GPU-gated prose. The real CPU floor is available. Finish the meter, write LS-3 from measured costs, then perform the one RS1 on CPU/stand-in evidence. After RS1: **LS-4 → LS-8 → LS-15 → LS-7 → LS-10**. Independent work can continue alongside as stated below. Do not claim that this guide consumes RS1 or that the source-reading planning review in `review.md` was RS1.

| Area | Still required |
| --- | --- |
| LS-1 | Preserve the real CPU floor and distinguish its limited image workloads from representative video/new-input cases. Warm-model GPU cells are **waiting for GPU**; no 100-ms guarantee follows from the CPU floor |
| LS-2 | Complete generation counter proof, explicit tolerance, process/compile/emission/hash/native coverage and Windows generation after its permission gate; keep instrumentation separate from timing |
| LS-3 / RS1 | One design note covering all eight task points, measured write budget, immutable-template approval, target generation, crash/unknown-acceptance rules, fences and version agreement; independent review remains required |
| LS-4, LS-8, LS-15 | Prepared typed templates, supervised core resident capability, then VibeComfy's per-job-state-safe resident pack; first job full path, later jobs measured fast path |
| LS-5 / LS-6 | Complete approved transport/output portions; obtain the explicit pin/scope decisions above; test cached/error/interrupted/disconnected jobs, corruption/truncation, custody and post-reply thumbnail durability |
| LS-7 / LS-10 | Remove Runtime/SDK/host polling while retaining durable authority, then thin CLI and in-process tool caller; exact new Runtime pins still require approval |
| LS-9 | #355 covers the running-cancel refusal portion, not all cases: restart, missing model/node, edited workflow/update, unknown acknowledgement, two callers and typed refusal cases remain |
| LS-12 | Component patch #361 plus all remaining first-job reductions and actual meter proof described above |
| LS-13 | Finish Windows meter/code proof after the recorded permission decision; real Windows-with-GPU measurement is **waiting for GPU** |
| LS-14 | Complete standing required-PR budget check and demonstrate injected process/poll regressions fail it; live GPU proof is **waiting for GPU** |
| R | Final review is **waiting for GPU** and the completed integrated candidate; do not spend its one round on partial preparation |

The Windows tester baseline from [issue 652](https://github.com/banodoco/astrid-dev/issues/652), RTX 4060 Ti / Agent `4ae35ed0`, remains 114 s cold and 84/93 s warm wall time, with 31 s Comfy execution for the first. It is not interchangeable with either hosted CPU floor or stand-in meter.

## Evidence, integration and safe pickup checklist

1. Read current `inputs.md`, owner replies and PR heads. Preserve exact tested source/dependency identities. Do not reconstruct the inaccessible ignored run configuration. Obtain an actual independent reviewer where required; a manager reread or calibration does not count as one.
2. Keep raw new-run logs, JUnit, inner exit codes, commands, source identities and original failure outputs. Download the named Actions artifacts before expiry; do not rely solely on the existence of a green job or this prose. The [continuation proof index](evidence/continuation-20261116/proof-index.json) maps the [committed complete local logs](evidence/continuation-20261116/local-checks.txt), their hashes and commands, the [raw paired microbenchmark](evidence/continuation-20261116/ls12-fingerprint-benchmark.json), and the [repository-tool comparison](evidence/tests/astrid-agent/33f269e4/summary.md). The original separate logs and JUnit also accompany the owner bundle. These supporting local checks are not hosted/full-suite proof.
3. Reconcile `tasks.md` via the authorized tasks-only progress route, keeping at most one progress PR. Its old Now block still contains pre-D9 GPU-gate, old branch and earlier CI descriptions. This handoff does not silently mark tasks complete or claim that record has reached main. The owner's later branch instruction forbids creating new main-targeting work; resolve that destination with the release's current progress convention rather than pushing main or editing tasks on the plan branch without agreement.
4. Combine task contributions on `release/14/plan-55` only after required proof/review, preserving add-only history and byte-identical shared helpers. Reprove affected joins. Do not confuse a task PR's checked head with a later integrated tuple. No product-main or release publication is included.
5. The hidden receipt-file issue has an implemented fix on Agent `release/14/main`: `include-hidden-files: true` plus the manifest upload guard. Carry it through normal release integration, do not add a competing fix or regenerate historical receipts. The owner explicitly stopped archaeology of the eight old integration jobs; resume the current implementation/proof instead.
6. Finish code, integration and the required meter evidence before the completion PR. Use the existing completion template only when the remaining tasks and final review are genuinely closed. This document is a pickup guide, not a statement that every conceivable CPU change has been finished.
