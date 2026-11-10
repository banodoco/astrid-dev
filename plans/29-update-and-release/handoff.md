# Handoff — Plan 29, Release 12

[Plan](plan.md) · [Inputs](inputs.md) · [Tasks](tasks.md) · [Release 12 evidence](evidence/r12/)

**Purpose:** everything a new advisor (M-INT) needs to continue Plan 29 on another machine without losing context. Read this file first, then `tasks.md` (Release 12 sections, newest last). State as of **2026-11-10 ~17:00Z**. Nothing important lives only on the old machine: every commit is on GitHub, and every result that matters is in this folder.

## 1. Goal and what "done" means

**Plan 29** ([plan.md](plan.md)) gives Astrid one honest update path (Update now, Update in Pinokio) and a release number that moves only by a deliberate release. Release 10 (0.0.10) and Release 11 (0.0.11, the served release: Agent `a105de3a`, App tuple `4f5477cb`) are published. **Release 12** is the release in flight: it carries the Release 11 field-failure follow-ups, the review-round fixes and the product regressions found against Release 10.

**Release 12 is published when all of this holds on one exact final tuple** (Agent, App, Runtime, harness):
1. the full `journey.yml` matrix, row=direct, 11 rows, is green;
2. no regression against R10 (`72462b04`), served R11 (`a105de3a` / `4f5477cb`) or `main`, with Plan 39 decision **D8** applied: product regressions against R10 are fixed in R12; stale or test-infra failures go to Plan 39 and are judged against R11 and `main`;
3. App Tests and Direct Journey have **0 failures** on the pinned App head;
4. the review rounds are done, with no open blocker.

Publishing is under Hannah's **standing conditional go** once the gate holds. Only the [Release skill](../../skills/astrid-dev-release/SKILL.md) merges to product `main`.

**Plan 29 is done** only after Hannah confirms the update works on her Mac through the normal App path. Then delete the hourly check-in scheduled task and tell her.

**The bar** (Hannah, 10 Nov ~01:12): failures in release 12's own checks are **fixed and questioned**, never waved through as "pre-existing". **Never weaken a check.** "Test drift" must be proven from the trace: twice today the App worker's "drift" call hid a real product bug (Direct Journey rounds 4 and 5).

## 2. Current tuple and branches

| Repo | Ref | SHA | Notes |
|---|---|---|---|
| Agent | `cand/29-r12` | `313bbd46f` | Pinned in the App today |
| Agent | `r12/cand-next` | `733ac5a43` | **Next candidate, not yet on `cand`**: `313bbd46f` plus 5 `--no-ff` merges (below). Push to `cand/29-r12` after its comparison is clean |
| Harness | `harness/29-r12` (astrid-agent) | `b550ecadf` | Final-round harness |
| App | `cand/29-r12` (astrid-app) | `e1d42be39` | Direct Journey rounds 3–5 merged; manifest sha256 `929c1a5e…1afab9`; Runtime `42ae24aff` |
| App | `r12/app-vendor-lock-313bbd46` | `c6454fcdc` | Held, **do not merge**. Proved the CLI surface is unchanged; the final re-pin regenerates the lock |
| App | `r12/app-dj-round6` | see [tasks.md](tasks.md#release-12-round-5-state-at-1700z-2026-11-10) | Round 6. If it isn't on GitHub, redo it from DJ run `42849600626` (section 4) |

Agent fix branches in `r12/cand-next`, each with regression tests that fail before and pass after:

| Branch | SHA | Fixes |
|---|---|---|
| `r12/personal-pack-snapshots` | `cbf7b4240` | Review round 3 P1×2: verified personal-pack snapshots were rejected by the reserved-directory guard and advertised as duplicate collections |
| `r12/marker-fence` | `bcb5ac48f` | Review round 3 P2: the ready marker is withdrawn when renewal fails or is fenced |
| `r12/schema-cache-invalidation` | `7d637370a` | Round 2 non-blocking: the schema cache is bound to its provider's identity |
| `r12/windows-readonly-cleanup` | `989cd0f6c` | Windows `packs add` failed deleting read-only git objects |
| `r12/pack-home-update-handoff` | `b2dc24ddb` | Chiptune not ready after update: HOME was not pinned in the Linux update job or the macOS handoff launcher ([evidence](evidence/r12/chiptune-home.md)) |

## 3. Next steps, in order

1. **Agent comparison** ([method](evidence/r12/agent-comparison.md)): base `313bbd46f` is done (205 failing ids). Run `733ac5a43`, R11 and R10 on the same set. New failures on `733ac5a43` block the push. Failures on `313bbd46f` that pass on R11 or R10 are release-12 regressions to fix; failures shared with R11 and R10 go on the Plan 39 record with their cause.
2. **Push** `733ac5a43` to Agent `cand/29-r12` (check that `cand` is still `313bbd46f` first; push by full URL, never force).
3. **Review round 4** (Astra-class reviewer) on `313bbd46f..cand` (the five fixes above). Blockers are fixed before the final round.
4. **App round 6**: merge into App `cand/29-r12` (`--no-ff`), run `tsc` and vitest on the touched files, and dispatch one early Direct Journey. Repeat rounds until Direct Journey is 0 failures. 11 three-products tests are still skipped behind failures; [dj-round5.md](evidence/r12/dj-round5.md) names their likely exposure.
5. **Final re-pin**, as **one** App commit: `pin.mjs` to the final Agent SHA, plus `vendor-lock.mjs update` (`vendor.lock.json` and `cli-surface.json`). Then run `vendor-lock.mjs check`, the runtime lock check, `cliSurfaceVerbs.test.ts`, `pin.mjs --check` and `release-guard` before the push.
6. **Final round on that one tuple:**
   - App Tests;
   - Direct Journey;
   - App lanes;
   - the full 11-row matrix on harness `b550ecadf`;
   - Agent `ci.yml` and `lanes.yml` compared with R10 (D8).

   Any failure gets an Astra-class deep dive before anyone calls it non-blocking.
7. **Publish** with the Release skill. Then:
   - write the SHAs to the Plan 38 Codex run's mailbox `run/to-codex.md` ([run state](../38-one-process-identity/evidence/codex-run-state-2026-11-10.md)); on a new machine, restart that run from its resume note first;
   - tell the Plan 32 orchestrator (section 5): int/32 waits until R12 publishes; R13 goes via `cand/release-13` and the Release skill; dropping the `int/**` push trigger is R13 prep; the runner hold ends;
   - tell Hannah;
   - open the astrid-dev release-skill PR: re-sync `runtime.lock.json` when the Runtime moves; workflows take their pins from the manifest; **every Agent re-pin regenerates the vendor lock in the same commit.**
8. Hannah confirms on her Mac, then Plan 29 completion (section 1).

## 4. Open items and how to restart each

| Item | State | Restart from |
|---|---|---|
| App Direct Journey round 6 | In progress at handoff: `:1189` (no workflow set `ASTRID_PACKS_AGENT`; fixed in `direct-journey.yml`), `:449` (test reads a nonexistent `show.head_revision_id`), `:2995` (waits for a removed retry button) | DJ run `42849600626`: download its artifacts (below) and brief a worker with the traces, the App at `e1d42be39` and the Agent at `313bbd46f` |
| Agent comparison of `733ac5a43`, R11, R10 | Running at handoff | [agent-comparison.md](evidence/r12/agent-comparison.md) |
| Review round 4 | Not started | Brief on `313bbd46f..733ac5a43`, giving [review-round3.md](evidence/r12/review-round3.md) as context |
| Matrix row `direct-linux-r11-update` | Harness fix `b550ecadf` is supported by evidence, not proven | The final matrix's receipt records the host's effective HOME |
| Off-Linux snapshot and Windows fixes | Proven locally in simulation only | The final matrix rows on macOS and Windows |

## 5. People, sessions and scheduled tasks

| Who | ID | Role |
|---|---|---|
| Hannah | — | Owner. Decisions below. Standing go for R12 |
| M-INT (this advisor) | `session_011EzfVzreGCJJQnTuXpbib9` | Orchestrator and advisor. Does the Agent merges, artifact downloads and worker briefs. The new advisor takes this role |
| Manager | `session_011EzfW2KHv7X5sa7Y7reDNp` | Owns the run loop through two workers: the App worker (re-pins, App Tests, Direct Journey) and the harness worker (matrix). Its shell is dead (full disk), but messaging works. Reach it with `send_message`. It reports verdicts and "TUPLE GREEN" |
| Plan 32 orchestrator | `session_011EzfVz8zzHLnUqSqMnGUCT` | Owns Plans 20 and 32. Holding its runners for R12 |
| Hourly check-in | scheduled task `trig_01WLLdkKZ3qLPRZB4aXqAYJj` | Fires into the old advisor session. **Disable it** when the new advisor takes over, and create its own |

## 6. Owner decisions (release 12), newest last

- **D8:** about 306 stale Agent tests and the Mypy debt stay on Plan 39 (AT1.1–AT1.7, AT2). R12 fixes every product regression against R10 ([evidence](../39-green-mains/evidence/release-12-r10-diff.md)).
- **Direct Journey `:426`:** keeps the user's draft visible on a second-writer conflict.
- **three-products `:444`:** test removed; no pinned Agent ships the capability.
- **Direct Journey `:708`:** keeps the product's auto-reload after an Astrid restart; the test changes to prove it.
- **Lanes integration (659 failures):** "if none break install or update, add to Plan 39". Verdict: none, at R11 parity. Recorded in [Plan 39](../39-green-mains/evidence/lanes-integration-triage.md).
- **Custody:** "doesn't block".
- **Working style:** orchestrate, don't do. Brief Codex workers in parallel: Luna for routine work, Terra for hard, Sol for very hard, Astra for the hardest. Use keep-going diagnostics to see past current failures. Clean disk aggressively.

## 7. How to work (tooling that matters)

- **Artifacts:** `GET https://api.github.com/repos/banodoco/<repo>/actions/runs/<id>/artifacts`, then `/actions/artifacts/<id>/zip`. This works through the session proxy with no token. The manager's workers can't download receipts, so the advisor fetches them, unzips the traces (the Codex sandbox can't extract), and hands them to a worker.
- **Keep-going diagnostic:** `journey.yml` with `direct_only=true`, `diagnostic_keep_going=true` and `diagnostic_leg=fresh-install`. It reports task sub-steps past a failed gate, and is diagnostic only. It runs the fresh-install leg only, so it can't see update-leg failures.
- **Codex workers:** [codex-in-cloud](../../skills/astrid-dev-orchestrate/codex-in-cloud/README.md) `codex-runner.sh <workdir> <prompt> <run-dir> 6 <model>`. Models: `gpt-6-luna`, `gpt-6.1-terra`, `gpt-6.1-sol`, `gpt-6-astra`.
  - Their sandbox makes `.git` read-only, so the advisor commits and pushes.
  - Give each worker its own `--shared` clone, `TMPDIR`/`--basetemp` inside its workdir, a 2 GB cap, and a `df` check before each test run.
  - A worker that says "blocked" on unattributed baseline failures usually means "needs a base comparison"; run one rather than accepting or rejecting the claim.
  - Mailboxes: `to-codex.md` and `to-orchestrator.md` in the run dir.
- **Git:** push by full GitHub URL, because local clones' origin can be a local path. Never force-push. Merge fix branches into `cand` with `--no-ff`.
- **Installer proofs** run every `tests/test_installer_*.py`, including `test_installer_bootstrap_imports.py`. A Windows-git change once broke every install by importing `jsonschema` into the installer.
- **Disk:** pytest temp trees filled the disk once (7.5 GB). Workers must clean up. Keep more than 3 GB free.

## 8. Standing constraints

- Never read `~/.codex`, `.env` files, or credential or token files.
- Don't work around classifier or safety denials; report them to Hannah.
- No model identifiers in commits, PR titles or bodies, code or artifacts.
- Never force-push.
- Never land the Windows update-refusal fallback (`2f975f62`).
- Don't weaken security checks.
- Only the Release skill merges to product `main`.
- Keep the owner's email private.
- Never fetch into the Plan 38 Codex run's clones.

## 9. Evidence index

| File | What it holds |
|---|---|
| [evidence/r12/matrix-42835188782.md](evidence/r12/matrix-42835188782.md) | Per-row verdicts of the last full matrix |
| [evidence/r12/review-round3.md](evidence/r12/review-round3.md) | Release review round 3: 3 blockers, all fixed in `r12/cand-next` |
| [evidence/r12/chiptune-home.md](evidence/r12/chiptune-home.md) | The HOME-mismatch root cause, receipts and tests |
| [evidence/r12/personal-pack-snapshots.md](evidence/r12/personal-pack-snapshots.md) | Snapshot fix test results |
| [evidence/r12/dj-round4.md](evidence/r12/dj-round4.md), [dj-round5.md](evidence/r12/dj-round5.md) | Direct Journey trace analyses, including two product bugs in the conflict and recovery flow |
| [evidence/r12/agent-comparison.md](evidence/r12/agent-comparison.md) | The before/after method, script and results |
| [Plan 39 Lanes triage](../39-green-mains/evidence/lanes-integration-triage.md) | No install/update breakers at R11 parity |
| [Plan 38 Codex run state](../38-one-process-identity/evidence/codex-run-state-2026-11-10.md) | The Plan 38 run, WAITING for R12 SHAs: mailbox, task cards, and Codex-in-cloud lessons |
