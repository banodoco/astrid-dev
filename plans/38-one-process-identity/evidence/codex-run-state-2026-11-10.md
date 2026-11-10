# Plan 38 Codex run: state handed off on 10 Nov 2026

[Plan](../plan.md) · [Tasks](../tasks.md) · [Plan 29 handoff](../../29-update-and-release/handoff.md)

State of the Codex run on 10 Nov 2026, copied from the run directory `/home/user/codex/plan38/run` on the old machine. **Status: WAITING** for the release 12 SHAs; T0 starts once M-INT posts them. The runner was `codex-runner.sh /home/user/codex/plan38 run/prompt-resume.md run 6 gpt-6.1-terra`. One unpushed astrid-dev commit was backed up to branch `backup/plan38-progress-d32f958` (one commit ahead of `progress/38-run`).

## run/resume-note.md



#### RESUMING AFTER A RESTART (read this first)
Your previous Codex process was killed at about 23:09Z by a container worker restart. This was not your fault. This is a fresh process with the same brief. Rebuild your state from durable records, not from memory:
- **Mailbox:** run/to-orchestrator.md (your notes so far) and run/to-codex.md (M-INT's replies, all still in force).
- **Run state:** plans/38-one-process-identity/.otto/runs/*/run.yaml and tasks.md in astrid-dev.
- **Branches and worktrees:** int/38 in astrid-agent and astrid-runtime, and any task/38-* branches and worktrees under this directory. Check `git worktree list` in each base clone, and remove stale worktrees whose task already landed.
- **Merged so far:** W0 landed (astrid-dev #210, Runtime int/38 74a1be1), and the ledger (#211) and starting baselines (#212) are merged.
- **Next:** T0 still waits for release 12. M-INT will post its SHAs in run/to-codex.md. Prepare the P1, P2r, A1–A3, L1 and F1 task cards meanwhile.

Your sub-agent cap is now 12. Keep at most 10 open, and close each one when its result is in. If you find half-done work from the killed process, check it before you trust it.

## run/to-codex.md


#### 2026-11-09 23:01Z — M-INT
- Agreed. Run the Agent baseline now, in parallel with W0. Run the Runtime baseline as soon as W0's scripts work. That's the right reading of "baseline before the first task" when the baseline needs W0.
- Your mapping is right too. The manage skill's cloud-session rules (one-repo sessions, allow lists, `list_sessions`) don't apply under Codex. Keep the intent: one repository's scope per task brief, one worktree per task, add commits only, and evidence for every claim. I'll fold your notes into the skills after the run, so keep logging them.
- Release 12 isn't published yet. I'll write here with its SHAs.

#### 2026-11-09 23:05Z — M-INT
- You hit "agent thread limit reached". Codex caps open agent threads (`agents.max_threads`, 6 by default), and finished subagents keep holding a slot until they're closed. Close each subagent's thread as soon as its result is in. Keep at most 5 running at once, so one slot is always free for a reviewer.

#### 2026-11-09 23:08Z — M-INT
- On shared worktrees: agreed, and make it a standing rule for this run. Each worker brief names its own `git worktree add` path, and the matching `<worktree>.env`, under this directory. Workers never touch the base clones `astrid-agent/`, `astrid-runtime/` or `astrid-dev/`; only you fetch and branch there. For W0, fix the wrong-pin exit and the package isolation before you accept it, as you said.

#### 2026-11-09 23:14Z — M-INT: baseline scope (this overrides the manage skill's "full suite" line for this run)
- Do NOT run either repo's full suite locally. If a starting-version baseline worker is running a full suite now, stop it.
- The local baseline is only:
  - (a) the plan's test inventory (tasks.md, "Test inventory");
  - (b) the files named in each task's focused proof, at the starting SHAs, with `-rA`, sorted by `astrid-dev/env/baseline-diff.py`.
- The full-suite comparison happens on CI only: one CI per repo on the integrated `int/38` head before each review round, judged against main's latest CI run by the regression rule. Don't run it per task.
- A worker runs only its task's focused proof.
- I'll fix the manage skill to say this.

#### 2026-11-09 23:10Z — M-INT
- I've merged astrid-dev #210 (W0 shared scripts, at 3e6dffd) and #211 (the ledger entry). W0 is done once the Runtime copies match main; mark it [x] in your next progress PR.
- Carry on with the scoped baselines and the task cards. T0 still waits for release 12.

#### 2026-11-09 23:55Z — M-INT (a note for the A2 card, no new work)
- Plan 32 (generation placement, `int/32-one-generation-path` in astrid-agent) also changes two files in A2's scope: `astrid/core/generation/engine_custody.py` (`_installed_models_root`, the `_Supervisor` start request, the `--engine` default) and `astrid/core/generation/target_launch.py`. On engine_custody.py these are different functions from A2's birth-id code, so the scopes are disjoint under the manage skill. Run them in parallel and land by merge, never rebase.
- At A2's dispatch, run `git diff $(git merge-base origin/main origin/int/32-one-generation-path) origin/int/32-one-generation-path -- astrid/core/generation/engine_custody.py astrid/core/generation/target_launch.py`. If it touches a function A2 changes, ask me before dispatching. If Plan 32 has reached Agent main by then, merge main into int/38 first.
- Nothing else changes. T0 still waits for the release 12 SHAs. Add this to A2's card, then go back to WAITING.

## run/to-orchestrator.md


#### 2026-11-09 — integration branches and Codex trial

Created and pushed Agent `int/38` at `a105de3a4852cb61b9647dfe2c920118bd29f272` and Runtime `int/38` at `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f`. W0 and starting-version baseline workers are running; T0 awaits the published Release 12 heads.

Codex trial note: the manager skill assumes Claude one-repository sessions, Claude settings allowlists, Write/Bash tools, and list_sessions, whereas this Codex environment provides shared-workspace agents and different tools. Mapping those instructions to Codex requires judgment; one-repository task scope is being enforced in briefs. The skill also asks for full baselines before any task, while W0 is needed to set up the Runtime baseline; the user explicitly requests these in parallel.

#### 2026-11-09 — Codex trial: shared worktrees

Codex agents share the same filesystem and checkout. A mistakenly scoped smoke worker attempted the Agent setup concurrently with the Agent baseline worker, causing a temporary Git lock conflict. It was stopped; the Agent worker is checking and will retry in its own worktree if needed. Future briefs must name distinct worktree and environment paths. Astrid-dev has no own smoke mode; its smoke helper targets product repositories. W0 shared scripts have an initial commit, but wrong-pin exit behavior and installed-package isolation require correction before acceptance.

#### 2026-11-09 — run setup progress PR

Progress PR https://github.com/banodoco/astrid-dev/pull/209 (`fb0a4ad`) passes `python3 scripts/check_docs.py`; please merge it. W0 shared scripts are at `1c694611`, with Runtime copies and smoke being checked; T0 awaits Release 12.

Codex trial note: the GitHub proxy appended a Claude Code attribution and an unrelated Claude session link to the REST-created PR body, although the submitted body had neither. This misattributes Codex work and should be corrected in the proxy/runner.

#### 2026-11-09 — Codex agent lifecycle

The exposed collaboration tools include spawn, follow-up, interrupt and list but no close-thread operation; the thread-limit message appeared even after a worker had completed. I reused the finished worker with follow-up and will keep concurrency within the exposed limit. The Agent smoke passed; its full-suite attempt is being relocated inside the workspace to satisfy the environment-location rule.

#### 2026-11-09 — W0 Runtime half landed

Runtime `int/38` merged the W0 scripts at `74a1be1` (task `445320cb`); `runtime` smoke passed with 70 passed and one platform skip, and all three scripts compare byte-for-byte with astrid-dev `1c694611`. Shared scripts PR https://github.com/banodoco/astrid-dev/pull/210 is open; W0 remains incomplete until that PR lands. Starting-version scoped baseline workers continue; T0 awaits Release 12. Process-ledger PR https://github.com/banodoco/astrid-dev/pull/211 records the trial.

#### 2026-11-09 — Agent starting baseline

Agent `a105de3a` scoped inventory/focused files: 778 passed, 19 deselected; `run/agent-focused-a105de3a.log`. New test files do not exist at the starting SHA. `baseline-diff.py` against the same starting log produced 0 in every difference bucket; evidence is being committed. Earlier full-suite collection had four errors (unset `ASTRID_BUILD_TEST_ESBUILD`, a too-shallow temporary checkout, and two imports of missing `_FIRST_PARTY_PACK_IDS`); the full run was stopped under the revised scoped-baseline instruction. No pods were used.

Codex trial note: the worker reported its cleanup command rejected by the shell restriction, leaving temporary checkouts/environments in place pending investigation.

#### 2026-11-09 — scoped baselines recorded

Runtime starting `4f5477cb`: 157 passed, 15 failed, 14 deselected, two subtests passed; failures are the inventory stale-owner, local-composition and real-bootstrap cases. The Windows shutdown-owner selector is absent at this starting SHA. Self-comparison with `baseline-diff.py` classifies 15 preexisting and zero regressions; this is a starting baseline, not a candidate result. Agent self-comparison has zero differences. The generated evidence and id lists are on PR https://github.com/banodoco/astrid-dev/pull/211 at `d0b03d0`, alongside the process entry. Shared W0 scripts PR #210 has focused proof and Runtime smoke/cmp evidence and is ready for review/merge. Next is Release 12 publication and T0.

#### 2026-11-09 23:15Z — recovery and W0

Recovered run state after restart; W0 is confirmed landed at astrid-dev `3e6dffd` and Runtime `74a1be1`, with all three scripts byte-identical. Progress PR https://github.com/banodoco/astrid-dev/pull/213 (`755d524`) passes check_docs and is ready to merge. T0 awaits the published Release 12 SHAs; task-card preparation is underway. No pods used.

Codex trial note: mailbox, Git and run state made restart recovery possible. The skill's Claude-specific worker lifecycle and baseline instructions required the mailbox overrides to interpret; no close-thread tool is exposed. The REST proxy again appended a false Claude attribution to PR #213. A supplementary process entry is at https://github.com/banodoco/astrid-dev/pull/214 (`2e09bff`), check_docs passed.

#### 2026-11-09 23:16Z — task-card preparation and release gate

Drafts for P1, P2r, A1–A3, L1 and F1 are in `run/task-cards.md`. Their exact bases, environment paths and final literal commands must be filled at dispatch; the T0 and RS1 gates remain in force. No implementation workers or CI are running.

When Release 12 is published, what are the exact Agent and Runtime `main` SHAs? T0 and all subsequent phase-1 work depend on those published heads. No pods are in use.

#### 2026-11-09 — restart recovery check

Recovered again from the mailbox, run record and worktrees. Progress PR #213 merged as `a353fd21`, and process-ledger PR #214 merged as `16dbb4af`; W0 is marked complete on astrid-dev main. Agent `int/38` remains `a105de3a`, Runtime `int/38` remains `74a1be1`; the draft task cards are present. No release-12 SHAs have arrived in the mailbox, and T0 remains blocked on them. No workers, CI or pods are running.

Codex trial note: a second container restart was recoverable from the same durable records; checking PR merge status separately was necessary because the mailbox recorded them while still open. A durable run status that reconciles remote PR state automatically would reduce restart work.

The corresponding ledger entry is in https://github.com/banodoco/astrid-dev/pull/218 (`f8281f8`); `check_docs.py` passes.

#### 2026-11-09 — subsequent restart

Rechecked run state and worktrees: W0 remains complete, T0 remains pending, and the integration heads are unchanged. Ledger PR #218 is merged at `2c8e979f`. The earlier question requesting published release-12 SHAs remains outstanding; no workers, CI or pods are active.

## run/task-cards.md

### Plan 38 task cards (draft)

Prepared from `astrid-dev/plans/38-one-process-identity/{plan,tasks,inputs}.md` and read-only inspection of the checked-out Agent and Runtime code. These cards are preparation only; no product repository was changed and no implementation was dispatched.

#### Shared start gate and source identity

- **Release 12 is pending.** Product tasks start only after it is published to both `main` branches. The initial main bases are Runtime `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` and Agent `a105de3a4852cb61b9647dfe2c920118bd29f272`; neither is the published release-12 base.
- The `int/38` branches are already cut. When M-INT supplies the published SHAs, merge each published `main` into its `int/38` with a merge commit. Record those SHAs and run T0, confirming the boot-hash fixture fix, harness fix and strict xfail. W0 supplies the Runtime worker setup. Before dispatch, fill in each card's exact starting SHA, individual worktree and environment paths, literal setup and test commands, manager follow-up authority, no AskUserQuestion, and add-commits-only rule; X and S leads delegate bounded work to N helpers. Use the repository worker scripts for local tests, not the illustrative direct pytest commands below.
- Dependency spine: `T0 + W0 → (P1 || P2r) → RS1 → (A1, A2, L1, F1; A3 also needs P2r)`. G1 follows P1/P2r/L1; G2 follows A1/A2/A3; E1 follows A1/A2/A3/F1; T1 follows A1/A3/E1. RS1 is a hard review stop (at most 2 rounds). Capture task base SHA and focused proof in each task's PR/run record.
- Runtime code inspection confirms `runtime_protocol.process_binding` currently selects Linux only and says Darwin/Windows are unchanged; `verified_host_launch.py` owns an inline `_COMPONENTS` map and a stdlib-only import boundary; `platform.process_identity` already contains the shared identity implementation. Agent inspection confirms its own custody identity and closure implementations remain. Runtime's current `NativeProcessCustody.publish()` raises the unnamed-by-task `Linux pidfd custody is unavailable` error in unsupported environments; L1 scopes this to a named refusal.

#### P1 — Runtime per-OS process binding provider

**Outcome:** `runtime_protocol.process_binding` is the single portable peer/token/details/signal/resume/census interface. Move the Darwin backend into `runtime_protocol`, complete/use Windows handoff support, and remove duplicate Darwin and dispatcher primitives from `astrid_runtime.custody_broker`. Preserve the stdlib/ctypes-only verified-host import boundary.

**Depends on:** T0 and W0. RS1 reviews P1 together with P2r; A1/A2/L1/F1 wait for RS1.

**Touched areas:** `runtime_protocol/process_binding.py`, `linux_process_binding.py`, new `darwin_process_binding.py`, `platform.py` Windows handoff backend, `posix_handoff.py` peer UID/PID support, `astrid_runtime/custody_broker.py`, new `tests/test_process_binding_provider.py`.

**Focused proof (Runtime checkout):**

```sh
python -m pytest -q tests/test_process_binding_provider.py tests/test_role_custody_authority.py tests/test_local_worker_handoff.py
```

Run locally on Linux and in blocking hosted `unit` on Ubuntu/macOS plus `windows-realm-publication`. Contract covers own token/details round trip; peer token over socketpair equals child's token; signal with 0; reused-PID rejection; and importing the provider does not load `runtime_protocol.service`, `.store`, or `.daemon`. Record backend-only tests on their native OS per D4.

**Unknowns / handoff:** exact release-12 Runtime base SHA, provider API accepted at RS1, and hosted run IDs are unknown pending publication/run. Do not start Agent callers before RS1 clears.

#### P2r — Runtime shared source-closure definition and vectors

**Outcome:** add Runtime-owned `runtime_protocol/schemas/host-source-closure-v1.json` with component mapping, installed-pair rule, and golden vectors. Make Runtime verifier consume it while remaining stdlib-only; list it in `contract/artifacts.json`.

**Depends on:** T0 and W0; may proceed in parallel with P1. A3 also depends on RS1.

**Touched areas:** new schema/vectors file; `runtime_protocol/verified_host_launch.py`; `contract/artifacts.json`; new `tests/test_host_source_closure_vectors.py`.

**Focused proof (Runtime checkout):**

```sh
python -m pytest -q tests/test_host_source_closure_vectors.py tests/test_local_worker_composition.py
```

Vectors build fixture trees under `tmp_path` and check components plus digest for a source checkout, installed pair (`runtime_protocol/` and `astrid_runtime/` beside `astrid/`), and symlinked-component refusal. Retain/run the existing standalone stdlib-import check for `verified_host_launch.py`.

**Unknowns / handoff:** published release-12 base and resulting provider/schema digest are unknown. RS1 must approve the exact schema/API before Agent vendoring.

#### A1 — Agent custody and birth identity on provider

**Outcome:** replace Agent-local Darwin custody primitives, Darwin-only peer token, and local birth encoding with Runtime provider calls; route selected-birth comparison through shared `platform.process_birth_matches`. Vendor the exact RS1 Runtime SHA in `runtime.lock.json`. This closes private-peer verification on Linux/Windows and aligns birth IDs.

**Depends on:** RS1 (and therefore P1). A1 is a prerequisite for G2/E1/T1.

**Touched areas:** `astrid/core/execution/custody_broker.py`, `generic_host.py`, `runtime.lock.json`, new `tests/core/execution/test_custody_provider.py`.

**Focused proof (Agent checkout):**

```sh
python -m pytest -q tests/core/execution/test_custody_provider.py tests/core/execution/test_custody_broker.py tests/integrations/test_generic_host_activation_acceptance.py
python scripts/vendor_lock.py check runtime.lock.json --producer <Runtime checkout at RS1 SHA>
```

New tests: `AuthenticatedCleanupActor.private_peer(sock).verify()` succeeds over socketpair on each OS; Agent and Runtime identities match for self and child; host-only peer check accepts Runtime `proc-start-ticks:…` owner. Run hosted `unit-shard`, `windows-native-and-installer`, and `darwin-native`.

**Unknowns / handoff:** release-12 published SHAs, RS1 Runtime SHA, exact vendored artifact hashes, and hosted run IDs. Preserve custody formats/designation versions and fail-closed behavior.

#### A2 — Agent's remaining birth-ID copies

**Outcome:** route process-group, zombie/census, leader, VibeComfy, engine-custody, target-launch, host-bootstrap zombie probe and qualification-script observers to shared `runtime_protocol.platform` identity. For any script retaining a stdlib reader, add its one-line rationale to G2's allowlist. Old `<boot-uuid>:<ticks>` journals read as unknown and must never be signalled.

**Depends on:** RS1/P1. Can proceed alongside A1; G2 waits for A1, A2 and A3.

**Plan 32 coordination at dispatch:** Fetch current Agent refs, then run `git diff $(git merge-base origin/main origin/int/32-one-generation-path) origin/int/32-one-generation-path -- astrid/core/generation/engine_custody.py astrid/core/generation/target_launch.py`. If this touches a function A2 changes, ask M-INT before dispatching. If Plan 32 has reached Agent main, merge main into `int/38` first. Plan 32's `_installed_models_root`, `_Supervisor` start request and `--engine` default are disjoint from A2's birth-id code; run disjoint work in parallel and land by merge, never rebase.

**Touched areas:** `astrid/core/execution/process_group.py`, `platform_helpers.py`, `vibecomfy_engine_adapter.py`, `astrid/core/generation/engine_custody.py`, `target_launch.py`, `astrid/sdk/host_bootstrap.py`, and the four scripts named in `inputs.md` duplicate inventory.

**Focused proof (Agent checkout, Linux):**

```sh
python -m pytest -q tests/core/execution/test_process_group.py tests/test_generic_host_vibecomfy_lifecycle.py tests/sdk/test_host_bootstrap_source_identity.py
```

Add explicit compatibility/refusal assertion for release-12 journal birth IDs: treated as unknown and never signalled. Inspect each listed observer for provider use or documented stdlib exception. G2's planted-copy test is downstream proof.

**Unknowns / handoff:** published Agent base and RS1 provider SHA, CI job runs, and which listed scripts still require a justified stdlib-only read are not yet established.

#### A3 — Agent consumes shared closure definition

**Outcome:** vendor Runtime's accepted closure JSON through `runtime.lock.json` into `astrid/core/execution/`; make `astrid/core/source_identity.py` consume the same definition and vectors. Keep pre-Runtime-import measurement ordering intact.

**Depends on:** P2r and RS1. G2/E1 wait for A3.

**Touched areas:** `astrid/core/source_identity.py`, `runtime.lock.json`, new `tests/core/test_host_source_closure_vectors.py`.

**Focused proof (Agent checkout):**

```sh
python -m pytest -q tests/core/test_host_source_closure_vectors.py tests/sdk/test_installed_runtime_source_identity.py
python scripts/vendor_lock.py check runtime.lock.json --producer <Runtime checkout containing accepted schema>
```

Agent measurer matches every vendored vector digest. Verify `verify_installed_host_startup()` leaves `runtime_protocol` absent from `sys.modules`, and execution package import ordering remains unchanged.

**Unknowns / handoff:** schema artifact SHA and Runtime commit are unknown until P2r is accepted at RS1; Agent base and hosted run IDs also await release 12.

#### L1 — Linux custody boundary lane

**Outcome:** Linux boundary tests pass in ordinary Ubuntu unit CI and stop erroring in sandbox CI when real pidfd support is absent. Put all four real-pidfd tests behind `needs_real_pidfd`; unsupported custody publication emits named gate refusal (`Linux custody gate: pidfd unavailable`), not a crash. No sandbox fallback is added here (Plan 15 owns it).

**Depends on:** RS1/P1.

**Touched areas:** Runtime `tests/test_linux_runtime_boundary_native.py` marks and `astrid_runtime/custody_broker.py` refusal text only.

**Focused proof:** hosted Ubuntu `unit` runs all four tests and they PASS; `sandbox-process-control` no longer errors on them. Add sandbox case for exact named refusal. Include run URLs/job IDs in evidence.

**Unknowns / handoff:** published Runtime base and RS1 SHA; hosted lane identifiers and results pending release-12 baseline T0.

#### F1 — Remaining inventory failures

**Outcome:** resolve only remaining Plan 38 inventory rows identified by T0, keeping fixes within P1 provider or A1/A2 files. For `No module named 'astrid'`, repair CI's Agent install from `tests/astrid-agent.pin`; do not skip tests. Record each row's cause and result in run state.

**Depends on:** T0 and RS1. Do not absorb failures already owned by P1/P2r/A1/A2/L1; route each failure to its named task or referenced plan first.

**Likely touched areas only if T0 demonstrates need:** Runtime `tests/test_bootstrap.py::StaleOwnerTests`, `tests/test_runtime_local_composition.py` host-only cases, `tests/test_real_bootstrap.py` identity cases, `tests/test_windows_runtime_launch.py::test_runtime_checkout_is_not_a_selectable_shutdown_owner`; product fixes stay inside provider/A1/A2 areas.

**Focused proof:** rerun each failing inventory row in its original named hosted job after correction; each row is PASS. Focused test command is determined from T0's first-error record and must be written into this card/run record before edits.

**Unknowns / handoff:** all failing rows, their causes, test commands, release-12 job run IDs, and exact post-RS1 Runtime SHA are unknown until T0 and RS1. F1 scope must not be guessed before that inventory exists.

#### Cross-card cautions

- Do not treat current candidate checkout SHAs as post-release bases or infer successful release publication from local files.
- P1/P2r task-level proof is not the cross-repo proof. A3 must vendor the exact P2r artifact; E1 later proves the pinned Agent/Runtime pair end to end on all three OSes.
- Provider/security contract review (RS1) precedes all consumer work. Windows may reveal a host-control transport change beyond P1; if so, plan row E1.1 (S) before implementation. Linux without pidfd stays an explicit refusal here and routes fallback to Plan 15.
- Requested task cards stop at F1; G1/G2/E1/T1 and final review/publication remain downstream tasks in `tasks.md`.

## run/prompt.md

You are the MANAGER of Astrid Plan 38, "One process identity for Agent and Runtime". Follow the `astrid-dev-manage` skill exactly. It is installed as a skill, and its source is in `astrid-dev/skills/astrid-dev-manage/SKILL.md` inside your working directory. Read it, the run contract (`astrid-dev/skills/astrid-dev-shared/run-contract.md`) and the plan before doing anything else.

This run is also a trial of running managers under Codex. Note anything about the Codex setup or the skills that slows you down or confuses you, as you go. Write each note in the mailbox, and in a process-ledger entry at the end (see "Report").

#### Your workspace (this directory)
- `astrid-dev/`: the planning repo. The plan is `astrid-dev/plans/38-one-process-identity/` (`plan.md`, `tasks.md`, `inputs.md`).
- `astrid-agent/` and `astrid-runtime/`: the product repos, as partial clones (blobs are fetched on demand). The run touches both.
- `run/`: this run's folder, which holds the mailbox. Don't edit `run/prompt.md`.
- You can write only inside this directory and `/tmp`. The network is on, through the session proxy. Git push and the GitHub REST API (`https://api.github.com/...` via `curl`) work through that proxy with no token from you. Never read `~/.codex`, `.env` files or any credential or token file.

#### Your advisor
Your advisor is the Claude orchestrator (M-INT), which reads your mailbox. Send it questions only: blockers, conflicting evidence, and judgment calls the plan can't settle. Progress goes in the plan's `tasks.md`. M-INT relays to Hannah (the owner) when a decision is hers.

#### Routes and models
Your subagents run on these routes. Record the exact IDs in the run's `run.yaml` under `plans/38-one-process-identity/.otto/runs/<run-id>/`; that folder is git-ignored. Never put model IDs in commits, PRs, code or docs.

| Route | Model ID |
| --- | --- |
| N | gpt-6-luna |
| X | gpt-6.1-terra |
| S | gpt-6.1-sol |
| T, and review or judgment | gpt-6-astra |

You yourself run on Terra at medium effort. Send X and S work to subagents rather than doing it all yourself. Run independent tasks at the same time.

#### Timing and branches
- **Release 12 isn't on main yet.** It's expected within a few hours. The plan says T0 measures "at the published release-12 heads".
- **Start now with the tasks that don't depend on release 12:**
  - Manage step 1: `run.yaml`, the environment smoke and the baseline record (the manage skill's new "Record the baseline" rule, using `astrid-dev/env/baseline-diff.py`);
  - **W0** (the astrid-dev runner scripts `env/runtime-setup.sh` and `env/runtime-pytest.sh`, plus the `runtime` smoke mode);
  - reading and preparing the task cards for P1, P2r, A1–A3, L1 and F1.
- **Integration branches:** create `int/38` in astrid-agent and astrid-runtime, cut from current `main` (Agent `a105de3a`, Runtime `4f5477cb`). When M-INT writes in `run/to-codex.md` that release 12 is published, with its SHAs, merge main into each `int/38` with a merge commit, never a rebase. Then run T0 at those heads, then the rest of phase 1.
- Phase 2 (C1, C2, R2) starts only after phase 1's review and publication, as the plan says.

#### Hard rules
- **Never push to `main`** in any repo, and never publish or tag a release; that is the Release skill's job, not yours.
- **Task branches** land in `int/38` through merge commits. For astrid-dev, push a branch and open a PR with the GitHub REST API (`POST /repos/banodoco/astrid-dev/pulls`). If the API refuses, push the branch and tell M-INT the branch name.
- **Add commits only.** Never force-push or rebase, even on your own branch.
- **CI:** dispatch with `curl -sS -X POST https://api.github.com/repos/banodoco/<repo>/actions/workflows/ci.yml/dispatches -d '{"ref":"int/38"}'`, then poll the runs API. This week's Agent unit shards take 42–76 minutes at the median. Treat a shard past 1.5 times its median (minimum 50 minutes) as a hang: cancel it and reproduce it locally with faulthandler.
- **Regressions:** a regression is a test that ran and passed on a baseline and fails at head. Compare with `astrid-dev/env/baseline-diff.py`, on `-rA` logs. Known pre-existing failures are recorded in `astrid-dev/plans/39-green-mains/evidence/`. Don't fix them in this plan unless the plan's F1 row covers them.
- **Tests:** run the Agent's tests with `astrid-dev/env/agent-setup.sh` and `agent-pytest.sh`, from the checkout root of an astrid-agent worktree. Build the Runtime equivalents in W0. Keep each worktree's `.env` inside this directory, and delete worktrees and their envs once their task lands, because disk is limited (about 14 GB free).
- **Spending:** CPU only. No RunPod, no GPU, no paid APIs.
- **Questions:** never ask the owner directly. If you can't continue without an answer, write the question to the mailbox and end with `

#### Report
- Keep `astrid-dev/plans/38-one-process-identity/tasks.md` current, per the manage skill. Push progress as an astrid-dev PR (it touches only `tasks.md`); M-INT merges it.
- At each milestone (run set up, W0 landed, int/38 cut, T0 done, each phase-1 task landed, review done), append a short dated note to the mailbox: what landed and its SHA, what's next, and anything blocked.
- End this turn when phase 1 is complete and reviewed (`

## Codex-in-cloud lessons (/home/user/codex/LESSONS.md)


These go into the codex-in-cloud README, the orchestrate skill, the manage skill and the plan skill once the Plan 38 trial proves them.

#### Runner (codex-in-cloud/codex-runner.sh)
- **`--skip-git-repo-check`:** pass it, because the workdir holds several clones and isn't itself a repo. Without it Codex refuses to start.
- **`CODEX_EFFORT`:** a new environment variable that sets `model_reasoning_effort`, low, medium or high.
- **Sub-agent cap:** `agents.max_threads` defaults to 6, and finished sub-agents keep their slot until they're closed. Add a `CODEX_MAX_THREADS` variable, set by `-c agents.max_threads=N` (accepted, tested), and tell managers to close finished threads.
- **No nested `codex exec`:** a Codex worker inside the sandbox can't start another Codex. `~/.codex` is read-only there ("failed to initialize in-process app-server client: Read-only file system"). Parallel work comes from sub-agents, not child Codex processes.
- **Model IDs for a ChatGPT sign-in:** these were checked and work. Record them in `run.yaml` only.
  - N: gpt-6-luna
  - X: gpt-6.1-terra (not "gpt-6-terra")
  - S: gpt-6.1-sol (gpt-6-sol also works)
  - T: gpt-6-astra
- **Through the proxy:** git push, `POST /pulls` and artifact downloads all work with no token. The proxy appends a Claude Code attribution to PR bodies Codex creates, which misattributes Codex work.

#### Skills under Codex
- **Install:** copy astrid-dev `skills/` to `~/.agents/skills/`. Codex discovers them there, and we don't touch `~/.codex`.
- **Cloud-session rules:** the manage skill's rules for cloud sessions (one-repo sessions, allow lists, `list_sessions`, Write/Bash, `send_message`) don't apply under Codex. Keep the intent: one repo's scope per brief, one worktree per task, add commits only, evidence for every claim. The manage skill needs a short "under Codex" section.
- **Shared filesystem:** sub-agents share one filesystem, and two workers in one clone collided on a git lock. Every brief names its own `git worktree add` path and `<worktree>.env`. Only the manager touches the base clones.
- **The mailbox replaces `send_message`.** The watcher wakes the orchestrator. It works.

#### Test scope (manage and plan skills)
- **Baseline, as written:** the "Record the baseline" rule I added (#204) says to run the full suite locally. That's too expensive: Agent shards are 42–76 minutes each.
- **Better rule:**
  - the local baseline covers only the plan's test inventory and each task's focused-proof files, at the starting SHAs, with `-rA`;
  - the full-suite comparison happens on CI only, once per repo on the integrated head before review, against main's latest CI by the regression rule.
- **Plan skill:** each plan should name its test inventory and each task's focused proof, as Plan 38 does, so the baseline scope comes straight from the plan.
- **Plan 39 dependency:** CI logs lack per-test results (no `-rA` or junit), so a CI-to-CI comparison can't run today. Plan 39 should add per-test result artifacts, so baseline-diff can read CI.

#### Orchestration
- **Ordering inside W0:** W0 (the Runtime runner scripts) has to come before the Runtime baseline, so "baseline before the first task" needs an exception for the environment task itself.

#### Survival
- **Worker restarts:** a restart of the Claude session's worker kills every process in the container, including the setsid/nohup runner. The run then shows status `running` with a stale heartbeat. Each check-in must check the heartbeat and `pgrep codex-runner`. If they're dead, restart the run with a resume note that rebuilds state from the durable records (mailbox, run.yaml, tasks.md, branches, worktrees). The runner could do this itself: an `--resume-from <run-dir>` mode that resumes the last Codex session id from codex.log.
- **Late pushes:** Codex pushed evidence to a PR branch after the orchestrator had merged that PR (#211, then #212). Rule: one PR per branch, and never push to a merged PR's branch. Use a fresh branch per PR.
- **bubblewrap:** it's missing on PATH, so Codex uses its bundled copy. That works.

## Keep-alive log (/home/user/codex/KEEPALIVE.md)


Goal: the Codex runner survives, or comes straight back from, every container restart, with no human involved.

#### Evidence so far
- At least 3 container restarts on 9 Nov (about 23:08, about 23:24, and one earlier). Each kills every process.
- The 23:24 restart came in the middle of an active turn (a Bash call at 23:23:02, then uptime 0 at about 23:24:36), while codex-hold.sh was running in the background. So it isn't an idle shutdown, and keeping the session busy can't prevent it.
- Resources at 23:38: 16 GB RAM with 0.5 GB used, 4 CPUs, 9.8 GB disk free. No memory or disk pressure. No logs inside the VM say why it restarted. environment-manager restarts the session with `--session-mode resume`.
- What survives a restart: /home/user, /root/.claude (settings and transcript), /tmp. All processes die.

#### Layers in place (23:38)
| # | Approach | Survives a restart | Status |
|---|---|---|---|
| A | codex-hold.sh as a background Bash task | No | Re-armed at each check-in |
| B | codex-hold-daemon.sh via the SessionStart hook in ~/.claude/settings.json | Relaunched when the session resumes | Live since 23:38; logs to restarts.log |
| C | Server-side send_later check-ins every 15 min, plus the hourly one at :41 | Yes | Live |

#### How to judge
After each restart, restarts.log gains a line with its time, the uptime and the previous container's last beat, so the gap is the downtime. hold.log shows who restarted the runner (the daemon or the hold), and when.
- **Works:** after a restart, the daemon starts within about a minute of the session resuming, and the runner is back within 30 s of that.
- **Fails:** the runner stays dead until a check-in. Then try the next approach.

#### Next approaches, in order
1. **No SessionStart line after a restart** (the hook didn't fire on resume): also start the daemon from the shell profile (~/.bashrc), so it starts with the session's first shell.
2. **Restarts keep coming fast** (more than one an hour): move Codex out of this heavy session (93 MB transcript) into a dedicated, light host session. It needs Hannah to sign in to Codex there.
3. **Long downtime between the restart and the resume:** shorten the check-ins to 10 minutes, since only a server-side event resumes a session.

#### Log
- 23:38: B is live, with the first start logged. Next: confirm B fires on the next real restart.
- 23:45–23:46: real restart #1 under B. Previous container's last beat 23:45:23; new container up at about 23:45:50; the SessionStart hook started the daemon at 23:46:13 (uptime 23 s); runner restarted 23:46:14 and resumed the same Codex session. Downtime under 1 min. **B works when the session resumes.** Open question: does the session resume on its own after a restart, or only on a message or check-in? (This one resumed with Hannah's message.) The next restart with nobody messaging will tell us.
- 02:38–02:41: real restart #2 under B. The previous container's last beat was 02:38:53. The daemon started at 02:41:57 (uptime 23 s) and restarted the runner at once; Codex resumed and went back to WAITING. Codex downtime was about 3 min. **B works again.**
- **New finding, the orchestrator session itself:** messages queued from 01:49 onwards, and the 02:02 check-in, were not delivered until 02:42. So this Claude session was stalled for about 50 minutes, after a "worker process was restarted" event, while the container stayed up. Codex was fine throughout. Approach C (send_later) didn't wake it either. Next step: if that recurs, put an hourly scheduled task on its own as the backstop (it fired at 02:41), and record when each event is delivered against when it was queued.
- 02:47–04:06: the orchestrator session was unreachable again for about 80 min. Messages queued from 02:45 and the 03:01 and 03:41 check-ins were all delivered at 04:06. The container's last beat was 03:46:34 and the new container started at 04:06:35, so it was down 20 min, and for the hour before that the session was alive but not being driven. Codex: the daemon restarted the runner at 04:06; it lost nothing and went back to WAITING. **The daemon approach (B) is proven for Codex: 3 of 3 restarts recovered.** The weak link is now the orchestrator session's own delivery. Server-side events queue up but don't wake it until the session is resumed, and that happens on the next container start or a human message.
