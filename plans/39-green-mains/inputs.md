# Inputs — Runtime and App main green

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted in part.
- **The split.** On 23 November 2026 the owner asked for the Agent's share to become its own project ([Plan 91](../91-agent-main-green/plan.md), its D2).
- **The release and base.** On 24 November, in this plan's session (https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV), the owner set both for this plan: "This should be for release 16, but we should build on top of release 15, obviously. And we should be mindful about rebasing that" ([D11](#owner-decisions)).
- **Plan 91's release.** The owner also moved Plan 91 to Release 16, and the Release 15 Lead recorded the same instruction.
- **Still to decide.** The owner asked whether this should be one project or two. The recommendation, two, is [D13](#owner-decisions), waiting for the owner's answer.

**Prior art:**
- The Release 14 plan, tasks, inputs and handover are in [evidence/release-14-record](evidence/release-14-record/plan.md), unchanged except their relative links.
- A status audit of each of its rows against the code on `release/15/main` is in [audit.md](evidence/release-15-measure/audit.md). Of 56 Runtime and App rows, 11 are done, 39 open, 2 stale and 4 unclear.
- Three claims in that record are wrong on `release/15/main`. K2 and K3 are ticked but no comparator exists in either repository. The App has no per-test results. The Runtime's quarantine cap is 20 against the plan's 10.
- The Release 14 plan-branch commits were never merged, so nothing is ported from them.
- Plan 91's approach, triage rules and tools are reused unchanged.

**Measurement (23–24 November):** ten read-only helpers measured the work and wrote card drafts, all in [evidence/release-15-measure](evidence/release-15-measure/README.md):
- the Runtime's CI and Nightly logs, clustered;
- the App's E2E, Lanes and Direct Journey logs;
- the fake Runtime against the real routes;
- the gate's design;
- the base and overlap analysis;
- a map of every old row and issue.

Each card says what was verified in code and what was inferred. No test was run.

**Negative findings:**
- **The Runtime's largest cause isn't a product bug.** The 1 November v33 fence (`v33_lifecycle.py:297-300`) is correct: only provider registration reaches `ready`, and the App always registers. 358 tests are stale ([rt-c1c2.md](evidence/release-15-measure/rt-c1c2.md)).
- **R-a and R-c are gone, and R-b is down to two IDs.** Those are the Release 14 environment causes: no Agent checkout, a hard-coded path and a shallow checkout.
- **The App's Vitest suite is green** (21,474 tests).
- **No App test is retired or redundant** ([app-stale.md](evidence/release-15-measure/app-stale.md)).
- **Pin drift explains no App failure.**
- **`env/baseline-diff.py` has three defects** ([gate-design.md](evidence/release-15-measure/gate-design.md)):
  - It cuts an ID at a space, so a Playwright regression reads as preexisting.
  - It exits 1 only for a regression, so a new failing test and a missing test pass.
  - Its four tests (`scripts/test_baseline_diff.py`) cover neither case.

  Plan 91's AG-1 fixes the missing bucket; GM-1 fixes the rest.

**Approach:** Plan 91's, per repository: a ceiling first, then the prune pass, then green by cause, then kept green.

**Rejected alternatives:**
- **One project with Plan 91** ([D13](#owner-decisions)). The repositories, test tools, CI capacity and decisions differ, and Plan 91's decisions are settled. Merging would hold it up.
- **Quarantining the old red** instead of a ceiling. The quarantine rule caps entries at 10 per repository, against about 660 failing Runtime IDs.
- **A per-PR gate for the App.** Pull requests into a plan branch start no App workflow.
- **Porting `release/14/plan-39`'s ceiling scripts.** They were never merged, and the Agent's comparator from that run never passed on an unchanged tree (Release 14 ruling 10).

**Challenge:** Pending. This plan is cross-repository, touches release rules and is over five days, so the planning skill requires an independent critique. Next: a fresh high-judgment reviewer checks the plan and tasks against the code; its findings go in `evidence/critique.md` and are answered here.

**Proof and limits:** the plan's [Completion](plan.md#completion), with the injected failures in GM-1, GM-3 and GM-5. Hosted runners only. Branch protection is the owner's setting.

**Review rounds:** RS1 at most 1, after phase 1, because phase 2 builds on the gates and the re-measure. R at most 2, because the plan is cross-repository and changes release inputs ([D27](#owner-decisions)).

**Run start:** Pending — no run is authorized. Next: once the owner confirms D12–D27 and names the accountable session (D26), record the date, the phase, that session, what it may do without asking (merge accepted cards into `release/16/plan-39`, merge release branches in, dispatch hosted runs on the plan branches, edit this plan's records), and what needs the owner's go: landing in a release branch, changing an assertion beyond the triage rules, renewing a quarantine entry, and accepting a ceiling entry.

## Owner decisions

D1–D10 are the Release 14 decisions, in [the record](evidence/release-14-record/inputs.md#owner-decisions). Its D3 (the quarantine rule) and D9 (the cap counts node IDs, and the Runtime's 19 may only fall) still bind here. The new decisions start at D11. Each is a recommendation until the owner confirms it in writing on the record; D11 is decided.

| # | Decision | Recommendation |
| --- | --- | --- |
| D11 | Release and base | **Decided (Hannah, 24 November 2026, this plan's session):** Release 16, built on `release/15/main`. `release/16/plan-39` is cut from `release/15/main` in astrid-runtime, astrid-app and astrid-dev. It merges `release/15/main` in whenever that moves, and `release/16/main` once it is cut; it never rebases (the [release skill](../../skills/shared/workstreams/astrid-dev-release/SKILL.md)). The Agent's `release/16/plan-39` row goes: the Agent is Plan 91's. |
| D12 | When a failing test may be deleted (the support line) | Plan 91's [D5](../91-agent-main-green/inputs.md#owner-decisions), applied to the Runtime and the App: with no users yet, only current behaviour, and updating from the previous published release, is supported. A test of anything older is retired, citing the retiring change or this line. Where a user could still reach the old path, a test asserts that it refuses. A redundant test is deleted, naming its covering test. Every deletion is listed and read by an `X` reviewer. |
| D13 | One project or two | Two. Plan 91 is the Agent. Plan 39 is the Runtime, the App, and the pieces shared across repositories: the nightly report, the required-checks lists and the comparator's adapters. They share the support line, the ceiling method, the triage rules and `env/baseline-diff.py`, and coordinate where an Agent bug shows in a Runtime or App test (D21). |
| D14 | The App's four quarantined three-products tests expire on 25 November, and `Tests` goes red on 26 November | Renew them once, to 8 December, with a one-line App pull request into `release/15/main` before 26 November. The owner becomes this plan's accountable session (until named, the owner). Their fixes are AP-15, AP-16 and AP-17, and #251 is Plan 91's (D21). The alternative, letting `Tests` go red, would turn the App's only green workflow red for a known cause. |
| D15 | The quarantine caps | No new entry in either repository; the Runtime's 19 IDs may only fall (the record's D9), and both repositories are at 10 or fewer at completion. The Runtime's nine entries expire on 1 December: renew them once, to 15 December, the same way as D14, unless their cards land first. |
| D16 | The Runtime's Agent pin (`0e1543e0`, 12 November) | GM-0 moves it to the Agent's `release/15/main` head and re-measures, and the plan branch follows the Agent's release branch from then on. An old pin hides Agent fixes and adds drift failures (RN-14). |
| D17 | Do native timelines start with V1 and A1? (astrid-dev [#1507](https://github.com/banodoco/astrid-dev/issues/1507), open) | Rule on #1507 before RT-3. The Runtime ships V1 and A1 today, and Plan 77's round notes rely on them. If that stands, RT-3 updates five expectations. If timelines must start empty, the seed is a product bug and RT-3 becomes one. |
| D18 | The Runtime's publication tests import a pack that moved to poms_packs | Rewrite the tests to call the Runtime's own publish path (RT-4), so Runtime CI needs no poms_packs pin; the pack is tested in its own repository (Plan 91's D10). The alternative is to pin poms_packs and install three packs in two jobs. |
| D19 | Should clip type `image` resolve like `media` in the Agent's `timeline_address.py`? | Yes, like the Agent's own clip and appearance code. It is an Agent change, so it goes to Plan 91 (D21), and RT-5 bumps the pin. |
| D20 | 18 tests need a real `pidfd`, which the sandbox job denies on purpose | In the sandbox job, the tests assert the refusal the sandbox gives; they run for real in `unit`. A deselect marker would hide them, which the triage rules forbid. |
| D21 | Agent bugs found by Runtime and App tests | They go to Plan 91 as Agent cards: #251 (TASK-SWAP), D19, and the Release 14 Agent rows no Plan 91 card owns, listed in the [row map](evidence/release-15-measure/row-map.md). This plan keeps the Runtime or App test that shows each, on its ceiling with the Plan 91 card's link, and bumps the pin when the fix lands. |
| D22 | The release rule (Release 14's K4 and K5) and the release record's scope and freeze sections (SF4, SF5) | [Plan 31](../31-releases-from-astrid-dev/plan.md) owns them, as it owns `release-contract` (its RL-1b and RL-1d). This plan supplies their inputs, the required-checks lists (GM-7) and green runs, and drops the rows. |
| D23 | viewing-parity needs pinned Chromium and Chrome binaries and a lock holder | Provision them in one E2E job (AP-12). If the pinned binaries can't be fetched with their recorded hashes, the owner chooses between a self-hosted runner and a dispatched lane outside the required checks. |
| D24 | The Runtime's pack routes are outside its HTTP contract | Now: list them in the fake with citations, under AP-2's coverage check (AP-1, AP-3). Later: a Runtime issue adds them to `workspace-v1.yaml`, a contract change for its own card. The empty-pack answer is the E2E baseline. |
| D25 | The retirements that need a ruling: legacy certification M1 captures (20 Nightly IDs), the R0 rollback (3), the v28 spec and v31 migration (3), `test_wc10_installed_launcher.py` (1) | Retire them all under D12, because they test formats and boundaries older than the previous published release. The legacy timeline write route keeps a test that it refuses. GM-P1 does it. |
| D26 | Who runs it | An orchestrator session (accountable, Claude) and a manager driving ChatGPT packet sessions, as Plan 91 runs. Release 16 has no release manager yet: the owner names a Release 16 Lead, or this plan's orchestrator reports to the owner directly. Cap: five packets in Running or Review, as for Plan 91. |
| D27 | Review rounds | RS1 at most 1, R at most 2 (see Review rounds above). |

## Source identities

- **Measured heads:**
  - Runtime `release/15/main` `24e2c929`;
  - App `release/15/main` `3f5da385`, the last head that ran, and `d53685f3`, a pin move whose runs were all cancelled;
  - Agent `release/15/main` `514499de`;
  - the Runtime's Agent pin `0e1543e0da2215db9cb3320cfd1083174c3c62a9`.
- **Destination:** `release/16/plan-39` in astrid-runtime, astrid-app and astrid-dev, cut from `release/15/main` at GM-0 (D11). No `release/16/*` branch exists yet in any repository.
- **Base choice per overlapping plan** (from [base-overlaps.md](evidence/release-15-measure/base-overlaps.md); re-check at GM-0):
  - **Plan 77** (Runtime `release/15/plan-77` and `plan-77-r7`, App `release/15/plan-77` and `plan-77-r7`) conflicts textually. It touches the Runtime's `timeline_commit_store.py`, `service.py` and `store.py`, and the App's pins and save path. Plan 77 is Release 15's and lands first. This plan builds on `release/15/main` and merges it in when Plan 77 lands. No card here changes those product files, except the RT-14, RT-15 and RN-4 diagnoses, which start after it lands.
  - **Plan 89** (Runtime `release/15/plan-89`) merges cleanly but changes three test files that hold 54 of this plan's IDs. The cards in those files wait for it (RT-6, RT-15).
  - **Plan 38** (Release 16) replaces the Runtime's `darwin-native` job with `host-spawn`, and edits `tests/astrid-agent.pin` and `tests/lanes.py`. GM-2 and GM-3 leave `darwin-native`'s test lines to Plan 38 beyond the reporting flags. The pin moves are ordered: GM-0 first, then whichever plan merges second merges the first.
  - **Plans 63, 76, 75 and 18** (Release 16) touch the timeline commit code and tests. They have no branches yet; check again when they are cut.
  - **Plan 91** shares `env/baseline-diff.py`: GM-1 lands after AG-1. It shares the required-checks format: GM-7 follows AG-2.
  - **Plan 31** owns `release-contract` (D22).
- **Issues** (the 38 labelled `plan:39`, all open):
  - 29 are the Agent's, for Plan 91;
  - Runtime #805, #806, #807, #809 and #910;
  - #984 is GM-1 and GM-3 to GM-5, and #971 is GM-6;
  - #578 is Plan 50's;
  - #925 is VibeComfy's, outside this plan.

  The full map is in the [row map](evidence/release-15-measure/row-map.md).

## References

- [evidence/release-15-measure/README.md](evidence/release-15-measure/README.md): what each evidence file holds.
- [Plan 91](../91-agent-main-green/plan.md), its [triage rules](../91-agent-main-green/tasks.md#triage-rules) and its [decisions](../91-agent-main-green/inputs.md#owner-decisions).
- [The green skill](../../skills/shared/workstreams/astrid-dev-green/SKILL.md), mode B.
