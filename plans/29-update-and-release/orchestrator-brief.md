# Orchestrator brief — Plan 29, Release 12

[Handoff](handoff.md) · [Plan](plan.md) · [Inputs](inputs.md) · [Tasks](tasks.md) · [Machine handoff, all plans](../../docs/handoffs/2026-11-10-orchestrator.md)

**Give this file to the orchestrator that takes over Release 12.** You run the release through managers; you don't write the code yourself. This brief gives you:
- the role and the operating model;
- the plan and the gate;
- what is in flight, and the next moves;
- the lessons from 10 Nov.

The exact SHAs, branches and evidence are in [handoff.md](handoff.md); read it second. State as of **10 Nov 2026, 16:50Z**.

## 1. Your role

You are **M-INT**, the release orchestrator for Plan 29. You own:

| You own | Meaning |
|---|---|
| The plan and the gate | You decide what blocks Release 12, against Hannah's bar (section 3) |
| Routing | You split the work into lanes and brief one manager per lane. Managers brief workers; you rarely brief workers directly |
| Integration | Feature branches land on `cand/29-r12` (`--no-ff`) only through you or a manager you name, after a before/after comparison |
| Evidence | Every claim is backed by a run id, a receipt or a test result. You keep `tasks.md` true |
| Escalation | Only genuine decisions go to Hannah, each with your recommendation. Everything else you decide |
| The publish | Under Hannah's standing go, once the gate holds, via the [Release skill](../../skills/astrid-dev-release/SKILL.md) |

Use the [orchestrate skill](../../skills/astrid-dev-orchestrate/SKILL.md) and the [manage skill](../../skills/astrid-dev-manage/SKILL.md). Hannah's working rule: **mostly brief and orchestrate others; run work in parallel; keep everything moving.**

## 2. The plan in one page

**Plan 29** ([plan.md](plan.md)) gives Astrid one honest update path: Update now for a normal install, Update in Pinokio for Pinokio, and the command only as a fallback. A release number moves only by a deliberate release.
- **Release 10** (0.0.10) shipped the working Update now.
- **Release 11** (0.0.11) is the served release (Agent `a105de3a`, App tuple `4f5477cb`). It fixed the Release 1 storage-handoff field failure.
- **Release 12** is in flight. It carries:
  - the R11 follow-ups;
  - the review-round fixes;
  - every product regression found against Release 10 (owner decision D8).

**Done means:** Release 12 published, then Hannah confirms the update works on her Mac through the normal App path. Only then is Plan 29 complete.

## 3. The bar and the gate

**Bar** (Hannah): failures in release 12's own checks are **fixed and questioned**, never waved through as "pre-existing". **Never weaken a check**: no skips, deleted tests, widened timeouts or looser assertions.

**Gate**, all on **one exact final tuple** (Agent, App, Runtime, harness):
1. the full `journey.yml` matrix, row=direct, all 11 rows green;
2. no regression against R10 `72462b04`, served R11 `a105de3a` / `4f5477cb` or `main`. D8 applies: product regressions against R10 are fixed in R12; stale or test-infra failures go to Plan 39, judged against R11 and `main`;
3. App Tests and Direct Journey with **0 failures** on the pinned App head;
4. release review rounds done, with no open blocker.

## 4. Lanes and managers

Today one manager, `session_011EzfW2KHv7X5sa7Y7reDNp`, runs two worker lanes: App and harness. Its shell is dead (full disk), but `send_message` works. The previous orchestrator did the Agent lane itself. **Recommended structure** for you, one manager per lane:

| Lane | Manager does | Inputs | Hands back |
|---|---|---|---|
| **Agent** | Briefs fix workers; runs the [before/after comparison](evidence/r12/agent-comparison.md) for every batch; merges to `cand/29-r12`; pushes by full URL | Matrix and review findings | A clean comparison, then the new Agent SHA |
| **App** | Direct Journey rounds (diagnose from traces, fix, merge, early DJ); App Tests; the **one-commit re-pin** | DJ and App Tests artifacts; the final Agent SHA | App head, manifest sha256, run ids |
| **Matrix** | The harness (`harness/29-r12`), the full matrix, keep-going diagnostics, receipt verdicts per row | Final tuple | Per-row verdicts with root causes ([example](evidence/r12/matrix-42835188782.md)) |
| **Review** | Independent release reviews and deep dives on any failing final-gate run | A SHA range and the previous round's report | Blockers with file:line, a scenario and the minimal fix |
| **Record** | Docs-only astrid-dev PRs: `tasks.md` rows, evidence, Plan 39 records. Merge after `check_docs` passes | Your state notes | Merged PR links |

Worker tiers for briefs (Hannah's rule):
- **Luna** (`gpt-6-luna`): routine work;
- **Terra** (`gpt-6.1-terra`): hard work;
- **Sol** (`gpt-6.1-sol`): very hard work, including every Direct Journey round;
- **Astra** (`gpt-6-astra`): reviews and the hardest problems.

The tooling is [codex-in-cloud](../../skills/astrid-dev-orchestrate/codex-in-cloud/README.md).

## 5. What is in flight now

| Item | State | Next move |
|---|---|---|
| Agent next candidate `r12/cand-next` `733ac5a43` | 5 fixes merged on `313bbd46f`: personal-pack snapshots, ready-marker fence, schema cache, Windows read-only cleanup, HOME in the update job and handoff launcher | Agent lane: finish the comparison against base `313bbd46f` (205 failing ids), R11 and R10; push to `cand/29-r12` if no new failures; fix any R12 regression against R11 or R10 |
| Release review round 4 | Not started | Review lane: `313bbd46f..cand` (the 5 fixes). Context: [review-round3.md](evidence/r12/review-round3.md) |
| App Direct Journey | Rounds 3–6 merged at App `8cfe10ce7`. Early DJ `42857693131`: direct-journey 42/1/2, three-products 3/1/10. `:449` now passes. Open: `:1264` (seeds through the retired save route, 410) and `:649` (Runtime restart, draft survives). Two product bugs found and fixed on the way, both in the conflict and recovery flow | App lane: round 7 from run `42857693131`'s traces ([dj-round6.md](evidence/r12/dj-round6.md) lists the still-skipped tests at risk). Repeat until 0 failures |
| App Tests | The only failure is the vendor lock not being re-synced; the CLI surface is unchanged | Fixed by the final re-pin commit. Branch `r12/app-vendor-lock-313bbd46` is held, not merged |
| Harness `b550ecadf` | Fixes autostart-off decoding and HOME for the R11 baseline | Used by the final matrix |
| Final round | Waits for the final Agent SHA and DJ 0 failures | Run the step list in section 6 |
| Plan 38 Codex run | WAITING for the R12 SHAs ([run state](../38-one-process-identity/evidence/codex-run-state-2026-11-10.md)) | After publish: restart it from its resume note and post the SHAs in its mailbox |
| VibeComfy pinned twice (engine recipe `e65f4941` vs manifest `af5cb429`) | Raised by the Plan 34 run; can silently disagree | Decide whether it blocks R12. The minimum is a check that they match at install; otherwise record it for R13 |

## 6. The path to publish

1. **Agent:** comparison clean → push `cand/29-r12` → review round 4 → fix blockers. Repeat until there are no blockers. Freeze the **final Agent SHA**.
2. **App:** DJ rounds until 0 failures on the current Agent.
3. **Re-pin, as one App commit:**
   - `pin.mjs` to the final Agent SHA;
   - `vendor-lock.mjs update`.

   Then run `vendor-lock.mjs check`, the runtime lock check, `cliSurfaceVerbs.test.ts`, `pin.mjs --check` and `release-guard`.
4. **Final round on that single tuple:**
   - App Tests;
   - Direct Journey;
   - App lanes;
   - the full 11-row matrix on harness `b550ecadf`;
   - Agent `ci.yml` and `lanes.yml` compared with R10 under D8.

   Every final-run failure gets a Review-lane deep dive before anyone calls it non-blocking.
5. **Publish** with the Release skill (only it merges to product `main`). Then:
   - tell Hannah;
   - tell the Plan 32 orchestrator (`session_011EzfVz8zzHLnUqSqMnGUCT`): int/32 can resume; R13 goes via `cand/release-13` and the Release skill; dropping the `int/**` push trigger is R13 prep; the CI runner freeze ends;
   - post the SHAs to the Plan 38 run;
   - open the release-skill PR (section 8).
6. **Hannah** runs the update on her Mac. When it works, record Plan 29 complete.

**CI freeze:** since 11:16Z on 10 Nov, other plans make no dispatches or `int/**` pushes, for release 12 ([machine handoff](../../docs/handoffs/2026-11-10-orchestrator.md#ci-runner-freeze)). Release 12's own runs are the exception. Keep them few: one tuple, one round.

## 7. Operating rhythm

- **Check-ins:** create your own hourly scheduled task (the old one, `trig_01WLLdkKZ3qLPRZB4aXqAYJj`, is disabled). Each check-in: read notifications; check each manager is alive with work in flight; check the newest run results; keep `tasks.md` true; do **one** thing (a nudge, a decision with a recommendation for Hannah, or one line to her).
- **Watch runs yourself:** poll `GET https://api.github.com/repos/banodoco/<repo>/actions/runs/<id>` and pull artifacts with `/runs/<id>/artifacts` → `/actions/artifacts/<id>/zip`. This works through the session proxy with no token. Relays lagged by 30 minutes or more. The manager's workers can't download receipts or App traces, so you, or a manager with a working shell, fetch, unzip and hand them over.
- **Briefs:** each brief to a manager or worker states:
  - the goal;
  - exact SHAs and evidence paths;
  - what is already ruled out;
  - the rules (never weaken; fail-before/pass-after tests; a base comparison for any "pre-existing" claim);
  - the required output format;
  - a `RUN-STATUS` line.

## 8. Lessons from 10 Nov (apply them)

- **"Test drift" must be proven from the trace.** Twice a "drift" call hid a real product bug: "Keep my changes" overwrote the durable draft, and "Save them" didn't reopen the conflict.
- **A worker "blocked" on unattributed baseline failures** needs a base comparison, not a yes or no. Run the same set on the base and diff.
- **Keep-going diagnostics run the fresh-install leg only.** A row that "passed" there can still fail after the update (the chiptune HOME bug).
- **Installer changes:** run every `tests/test_installer_*.py`. One change broke every install by importing `jsonschema` into the installer bootstrap.
- **Re-pins must regenerate the vendor lock** in the same commit. Put this in the release-skill PR, together with re-syncing `runtime.lock.json` when the Runtime moves and taking workflow pins from the manifest.
- **Disk:** pytest temp trees filled the disk once and stopped two workers. Give each worker a 2 GB cap, `--basetemp` inside its workdir, and a `df` check before each run.
- **Git:** push by full GitHub URL; never force-push; one PR per branch; never push to a merged PR's branch.

## 9. Standing constraints

- Never read `~/.codex`, `.env` files, or credential or token files.
- Don't work around classifier or safety denials; report them to Hannah.
- No model identifiers in commits, PR titles or bodies, code or artifacts.
- Never force-push.
- Never land the Windows update-refusal fallback (`2f975f62`).
- Don't weaken security checks.
- Only the Release skill merges to product `main`.
- Keep the owner's email private.
- Never fetch into the Plan 38 Codex run's clones.
- Owner decisions are listed in [handoff.md](handoff.md#6-owner-decisions-release-12-newest-last). Don't reopen a decision Hannah has made.
