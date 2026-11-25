# Inputs — Runtime and App main green

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — in part, by the owner in this plan's session (https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV):
- **The split.** On 23 November 2026 the owner asked for the Agent's share to become its own project ([Plan 91](../91-agent-main-green/plan.md), its D2).
- **The release and base.** On 24 November, in this plan's session (https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV), she set both: "This should be for release 16, but we should build on top of release 15, obviously. And we should be mindful about rebasing that" ([D11](#owner-decisions)). The same day she moved Plan 91 to Release 16.
- **The Lead.** Also on 24 November, she named this session Lead for Plans 91 and 39 until a Release 16 Lead is named.
- **Still open.** She asked whether this should be one project or two. The recommendation, two, is [D13](#owner-decisions).

**Prior art:** the [Release 14 record](./evidence/release-14-record/plan.md) and its [audit](./evidence/release-15-measure/audit.md):
- **The Release 14 record.** Its plan, tasks, inputs and handover are in [evidence/release-14-record](evidence/release-14-record/plan.md), unchanged except their relative links.
- **The audit.** [audit.md](evidence/release-15-measure/audit.md) checks every Runtime and App row against the code on `release/15/main`. Of 56 rows, 11 are done, 39 open, 2 stale and 4 unclear.
- **What the record gets wrong.** K2 and K3 are ticked, but no comparator exists in either repository. The App has no per-test results. The Runtime's quarantine cap is 20, against the plan's 10. The Release 14 plan-branch commits were never merged.
- **Reused:** Plan 91's approach, triage rules and comparator.

**Measurement (23–24 November):** ten read-only helpers wrote the measurements and card drafts in [evidence/release-15-measure](evidence/release-15-measure/README.md):
- the Runtime's CI and Nightly logs, clustered;
- the App's E2E, Lanes and Direct Journey logs;
- the fake Runtime against the real routes;
- the gate's design;
- the base and overlap analysis;
- a map of every old row and issue.

Two ambiguity passes then checked every row against the code. No test was run.

**Negative findings:**
- **The Runtime's largest cause isn't a product bug.** The 1 November v33 fence (`v33_lifecycle.py:297-300`) is correct, and the App always registers a provider. 358 tests are stale ([rt-c1c2.md](evidence/release-15-measure/rt-c1c2.md)).
- **Two of the Release 14 environment causes are gone:** R-a (no Agent checkout) and R-c (a shallow checkout). R-b, the hard-coded path, is down to two IDs.
- **The App's Vitest suite is green.**
- **No App test is retired or redundant.**
- **Pin drift explains no App failure.**
- **The cancelled runs:** manual cancels through the shared account, and the Runtime's pull-request concurrency by design (Plan 91's AG-0, and App `d53685f3`'s check annotation).
- **`env/baseline-diff.py` on `main`** blocked only on regressions and cut IDs with spaces. Plan 91 fixes both in astrid-dev #1833, with `--strict` and a reading of every pytest run in a log.

**Approach:** Plan 91's, per repository:
1. a sealed baseline (inventory and ceiling) from two runs;
2. the prune pass;
3. green by cause;
4. kept green.

The comparison runs in the orchestrator's lane through one gate tool, with no gate job inside product CI.

**Rejected alternatives:**
- **One project with Plan 91** ([D13](#owner-decisions)).
- **Quarantining the old red** in place of a ceiling: the cap is 10 per repository, against about 660 failing Runtime IDs.
- **A gate job inside each workflow:** it needs astrid-dev's comparator inside product CI. One tool in the orchestrator's lane does the same for every repository ([critique 2.2](evidence/critique.md)).
- **Per-test Vitest results:** Vitest is green, and a job result with its test count catches a new failure and a lost test.
- **An astrid-dev plan branch:** tools there would not reach workers or the gate.
- **A local Playwright worker script:** packets have no network.
- **Vendoring the Runtime's OpenAPI** into the App's `runtime.lock.json`, which Plan 77 is changing.
- **Porting `release/14/plan-39`'s ceiling scripts:** they were never merged.

**Challenge:** Reviewed — an independent high-judgment critic checked the plan and tasks against the code ([critique.md](./evidence/critique.md)), and two ambiguity passes checked every row. All of the critique's findings were accepted, except one:
- **1.1, deleted tests:** the baseline now stores the passing inventory as well as the failures.
- **1.10, the 19 quarantined Runtime IDs:** GM-Q owns them, and the prune rules apply.
- **1.2, App pull requests:** the workflows they start are listed, and Direct Journey is a proof route.
- **1.3:** Nightly is re-measured on the plan branch.
- **1.4:** GM-2's Nightly change is reduced to the log.
- **1.5, Plan 89:** its overlap is counted by distinct ID, and RN-4, RN-5, RN-8, RT-6, RT-11 and RT-15 wait for it.
- **1.6:** D17 is recorded as decided.
- **1.7, the pidfd tests:** D20 now uses the existing `needs_real_pidfd` marker.
- **1.8:** RT-9 adds no App pin.
- **1.9:** D14 and D15 are reworded, and split out as needed now.
- **1.11:** D22 waits for Plan 31's acceptance.
- **1.12:** GM-7 writes into the one astrid-dev file.
- **1.13:** the Lead is named, and proofs run in the orchestrator's lane.
- **1.14:** the cancellations are recorded as answered.
- **2.1–2.8:** the comparator change stays Plan 91's. GM-8, AP-5 and AP-20 are gone, and AP-3 is folded into AP-2. The three-products structure is deferred. The astrid-dev plan branch is dropped.
- **2.9:** Nightly stays in scope, after Plan 89 and a check with Plan 75.
- **3.1:** phase 2 no longer waits for RS1.
- **3.2:** the missing dependencies are added.
- **3.3:** each baseline is sealed from two runs.
- **6:** the `S` rows get per-card checks, and every deletion goes on one list.
- **Not accepted, 4 (D13):** the critic would keep the Runtime and the App in one plan, with separate landings, and so does this plan. The owner's question was about Plan 91, so D13 stays.

**Proof and limits:** the plan's [Completion](plan.md#completion), with the injected failures in GM-3 and GM-5. Hosted runners only. Branch protection is the owner's setting.

**Review rounds:** RS1 at most 1, on the baselines and the prune list before the first landing. R at most 2, because the plan is cross-repository and feeds the release rule ([D27](#owner-decisions)).

**Run start:** Pending — no run is authorized. Next: once the owner confirms the open decisions, the Release 16 Lead names the orchestrator. Record the date, the phases, that session, and what it may do without asking:
- merge accepted cards into `release/16/plan-39`;
- merge release branches in;
- dispatch hosted runs on the plan branches;
- ratchet the baselines;
- edit this plan's records.

What needs the owner's go: landing in a release branch, changing an assertion beyond the triage rules, renewing a quarantine entry, and accepting a ceiling entry. GM-Q can run before the Run start, once D14 and D15 are decided.

## Owner decisions

D1–D10 are the Release 14 decisions, in [the record](evidence/release-14-record/inputs.md#owner-decisions). Its D3 (the quarantine rule), D4 (the nightly report's output) and D9 (the cap counts node IDs, and the Runtime's 19 may only fall) still bind here. The new decisions start at D11. Each is a recommendation until the owner confirms it in writing on the record; D11 and D17 are decided. **D14 and D15 are needed now.**

| # | Decision | Recommendation |
| --- | --- | --- |
| D11 | Release and base | **Decided (Hannah, 24 November 2026, this plan's session):** Release 16, built on `release/15/main`. `release/16/plan-39` is cut from `release/15/main` in astrid-runtime and astrid-app. It merges `release/15/main` in whenever that moves, and `release/16/main` once it is cut; it never rebases (the [release skill](../../agent/shared/workstreams/release.md)). It lands only in `release/16/main`, because `landing-reference` refuses it into `release/15/main`. astrid-dev changes go to `main` by ordinary pull requests. |
| D12 | When a failing test may be deleted (the support line) | Plan 91's [D5](../91-agent-main-green/inputs.md#owner-decisions), applied to the Runtime and the App: with no users yet, only current behaviour, and updating from the previous published release, is supported. A test of anything older is retired, citing the retiring change or this line. Where a user could still reach the old path, a test asserts that it refuses. A redundant test is deleted, naming its covering test. Every deletion is listed and read by an `X` reviewer. |
| D13 | One project or two | Two. Plan 91 is the Agent. Plan 39 is the Runtime, the App, and the pieces they share with the Agent: the gate tool, the nightly report and the required-checks entries. They share the support line, the baseline method, the triage rules and `env/baseline-diff.py`. The Runtime and the App stay together in Plan 39, each with its own baseline and landing. |
| D14 | **Now:** the App's four quarantined three-products tests (#249–#252) expire on 25 November, in both `release/15/main` and `main`. From 26 November `npm run test:app` stops at its guard, so the App reports no Vitest results at all | Renew the four entries once, to 8 December, in both branches, before 26 November. The owner is "Plan 39 orchestrator". This is a four-entry change through the Release 15 Lead, who holds `release/15/main`. Their fixes are AP-15, AP-16 and AP-17; #251 is Plan 91's (D21). Once the App baseline is sealed, an entry that expires again comes off and its test goes on the ceiling. |
| D15 | **By 30 November:** the Runtime's nine entries (19 IDs, #805–#809) expire on 1 December, in both branches | GM-Q sorts them under D12 first: most test retired writers that return `410`, and are retired. Any entry still needed is renewed to at most 14 days after the day the change merges, which the guard checks (`tests/lanes.py:298`). `MAX_DECLARED_XFAIL_TESTS` falls to what is left. It goes through the Release 15 Lead, as D14. |
| D16 | The Runtime's Agent pin (`0e1543e0`, 12 November) | GM-0 moves it to the Agent's `release/15/main` head, together with `windows-realm-publication`'s hard-coded Agent SHA; `darwin-native`'s is Plan 38's. Later moves follow the Agent's release branch, never an unlanded plan-branch commit. Each move is a load-bearing moment: compare with the baseline. |
| D17 | Do native timelines start with V1 and A1? | **Decided (owner, 23 November 2026, on [#1507](https://github.com/banodoco/astrid-dev/issues/1507)):** keep the Runtime's starter tracks, and the App accepts exactly the V1/A1 shape. RT-3 updates its tests' expectations. |
| D18 | The Runtime's publication tests import a pack that moved to poms_packs | Rewrite them to call the Runtime's own publish path (RT-4), so Runtime CI needs no poms_packs pin. The pack is tested in its own repository (Plan 91's D10). |
| D19 | Should clip type `image` resolve like `media` in the Agent's `timeline_address.py`? | Yes, like the Agent's own clip and appearance code. It is an Agent change for Plan 91 (D21); RT-5 moves the pin once it lands. |
| D20 | Tests that need a real `pidfd`, which the sandbox job denies on purpose (17 IDs) | Use the Runtime's existing `needs_real_pidfd` marker. The sandbox job deselects it by design (`tests/seccomp/README.md:20`), and the tests run for real in `unit`, so nothing is hidden. Plan 38 uses the same marker. |
| D21 | Agent bugs found by Runtime and App tests | They go to Plan 91 as Agent cards, once its orchestrator and the Release 16 Lead accept them: #251 (TASK-SWAP), D19, and the Release 14 Agent rows no Plan 91 card owns ([row map](evidence/release-15-measure/row-map.md), section 2). This plan keeps the Runtime or App test that shows each one on its ceiling, with the Plan 91 card's link. |
| D22 | The release rule (Release 14's K4, K5) and the release record's scope and freeze sections (SF4, SF5) | Offer them to [Plan 31](../31-releases-from-astrid-dev/plan.md), which owns `release-contract`, as new rows. Its RL-1b reads no required-checks list today. Until Plan 31 accepts, they wait, under Waiting on. This plan supplies the required-checks entries (GM-7) and the green runs. |
| D23 | viewing-parity needs pinned Chromium and Chrome binaries and a lock holder | Provision them in one E2E job (AP-12). If the pinned binaries can't be fetched with their recorded hashes, choose between a self-hosted runner and a dispatched lane outside the required checks. |
| D24 | The Runtime's pack routes are outside its HTTP contract | Now: the fake serves them from a cited hand list, under AP-2's coverage check, with the empty-pack answer as the E2E baseline. Later: a Runtime issue adds them to `workspace-v1.yaml`. |
| D25 | Retirements that need a ruling: the legacy certification M1 captures (20 Nightly IDs), the R0 rollback (3), the v28 spec and v31 migration (3), `test_wc10_installed_launcher.py` (1), the legacy word anchor (Nightly, as the Agent refuses it) | Retire them under D12: they test formats and boundaries older than the previous published release. The legacy timeline write route keeps a test that it refuses. GM-P1 does it. |
| D26 | Who runs it | The Release 16 Lead (this session, until one is named) names an orchestrator session, and a manager that drives ChatGPT packet sessions, as for Plan 91 in [releases/16/run.md](../../releases/16/run.md). Packets have no network, so the orchestrator runs every hosted and networked proof. Cap: five packets in Running or Review. The Lead sets the runner budget across Plans 91 and 39. |
| D27 | Review rounds | RS1 at most 1, R at most 2. |
| D28 | The App's vision specs read the live public feed today, and AP-8 replaces it with a fixture | Keep one live-feed check as a scheduled or dispatched job outside the required checks, so the feed is still watched without making E2E depend on the network. |
| D29 | The three-products extension batch test drove an extension that no longer exists (#250) | Drive a current first-party extension that does the same batch move, chosen by AP-16; if none fits, retire the test under D12 with a refusal or coverage note. |
| D30 | The dropped-video data loss (#252, AP-17) touches the App save path that Plan 77 is changing and Plan 63 (dependable saving) owns next | Keep it here, landing after Plan 77, because its test is in this plan's ceiling and quarantine. Hand it to Plan 63 instead only if that plan starts first. |
| D31 | Is Direct Journey's `three-products` project part of the App gate? | Yes, once the four quarantined tests are fixed or on the ceiling. It is the only end-to-end test of the three products together. |
| D32 | A native clip swap after a disjoint edit: "rebases" (the test) or "merged" (the product)? (RN-9) | Ask Plan 89's lane which is the contract. Until it answers, the ID stays on the ceiling. |

## Source identities

- **Measured heads:**
  - Runtime `release/15/main` `24e2c929`, and Runtime `main` `5120462` for Nightly;
  - App `release/15/main` `3f5da385`, the last head that ran, and `d53685f3`, a pin move whose runs were cancelled by hand;
  - Agent `release/15/main` `514499de`;
  - the Runtime's Agent pin `0e1543e0da2215db9cb3320cfd1083174c3c62a9`.
- **Destination:** `release/16/plan-39` in astrid-runtime and astrid-app, cut from `release/15/main` at GM-0 (D11), landing in `release/16/main`. No `release/16/*` branch exists yet in either repository.
- **Base choice per overlapping plan** (from [base-overlaps.md](evidence/release-15-measure/base-overlaps.md) and [critique.md](evidence/critique.md); re-check at GM-0):
  - **Plan 89** (Runtime `release/15/plan-89`, still active) **— wait.** It changes:
    - test files holding 18 distinct CI IDs and 37 Nightly IDs of this plan's: the sequential verifier, acceptance, recorder ABI, history assembly, commit integration and projection occupancy files;
    - the product's history guards, commit authorization and execution, `store.py`, `server.py` and `v33_manifest.py`.

    RT-6, RT-11, RT-15, RN-4, RN-5, RN-8 and GM-P1's acceptance-file deletions wait for it to land. RT-1 and RT-2 re-check once its `v33_manifest.py` change lands.
  - **Plan 77** (Runtime and App `release/15/plan-77` and `plan-77-r7`) **— wait.** It changes:
    - the Runtime's `timeline_commit_store.py`, `service.py` and `store.py`;
    - the App's pins and save path (`localSaveSession.ts`, `commitOutbox.ts`, `bootstrapInitialization.ts`).

    AP-14 and AP-17 touch the same App code, so they wait for it. Everything else builds on `release/15/main` and merges it in when Plan 77 lands.
  - **Plan 38** (Release 16) **— stack per card.** It replaces the Runtime's `darwin-native` job, and edits `tests/astrid-agent.pin`, `tests/lanes.py` and the bootstrap tests:
    - GM-2 leaves `darwin-native`'s test lines alone beyond the reporting flags;
    - RT-12's `StaleOwnerTests` and four of RT-8's IDs follow Plan 38;
    - the pin moves are ordered: GM-0 first, and whichever plan merges second merges the first.
  - **Plan 75** (Release 16) **— check before acting.** Its effect-list rework rewrites the Runtime's history re-checks. Ask its lane before RN-4 and RN-5.
  - **Plans 63, 76 and 18** (Release 16) touch the timeline commit code and tests. They have no branches yet; check again when they are cut.
  - **Plan 91** owns the comparator change (#1833) and astrid-dev's `ci/required-checks.json` (AG-2). GM-3 and GM-7 follow them.
  - **Plan 31** owns `release-contract` (D22).
- **Issues** (the 38 labelled `plan:39`, all open):
  - 29 are the Agent's, for Plan 91;
  - Runtime #805, #806, #807 and #809 are GM-Q's, and #910 (Windows receipt temp names past 260 UTF-16 units) is RT-18;
  - #984 is GM-3 to GM-5, and #971 is GM-6;
  - #578 is Plan 50's;
  - #925 is VibeComfy's, outside this plan.

  The full map is in the [row map](evidence/release-15-measure/row-map.md).

## References

- [evidence/release-15-measure/README.md](evidence/release-15-measure/README.md): what each evidence file holds.
- [critique.md](evidence/critique.md): the independent critique this plan answers.
- [Plan 91](../91-agent-main-green/plan.md), its [triage rules](../91-agent-main-green/tasks.md#triage-rules) and its [decisions](../91-agent-main-green/inputs.md#owner-decisions).
- [The green skill](../../agent/shared/workstreams/green.md), mode B.
