# Plan 39 status audit (Runtime, App, cross-repo scope), 24 Nov 2026

Read-only. Sources, all at `origin/main` of astrid-dev unless stated: `plans/39-green-mains/{plan,tasks,inputs,handover}.md`, `releases/{14,15,16}.md`, `releases/14/run.md`, `plans/91-agent-main-green/{inputs,tasks}.md`, `plans/index.md`. Code: astrid-runtime `release/15/main` = `24e2c929` (23 Nov), astrid-app `release/15/main` = `d53685f3` (24 Nov), both via FETCH_HEAD.

Citation style: `tasks.md:N` is the line in `plans/39-green-mains/tasks.md` (the table rows are at lines 38-154). `plan.md:N` and `inputs.md:N` likewise.

Caveat on method: none of the Release 14 plan-branch commit SHAs that tasks.md cites (for example Runtime `5f64eabe`, `19cd1e35`, `97321788`, App `e5f00690`, `549e335d`, `0700e981`) exist in the Runtime or App clones. Only `8e8711fd` (Runtime #70) and `16d5734a` (Runtime #53) are ancestors of release/15/main. So "DONE (verified)" below means the content was read on release/15/main, not that the cited SHA was checked. Statuses for phase 2 rows are "OPEN" where tasks.md says `[ ]` and nothing on release/15/main contradicts it. I did not run CI, so I cannot say whether the underlying tests now pass.

## 1. Task table (rows that are not Agent-only)

Counts: 56 rows. DONE 11, OPEN 39, STALE 2, UNCLEAR 4. Rows that are Agent-only are listed after the table and excluded.

Legend: P = phase, W = wave in the Release 14 plan (`tasks.md:193-199`). Repo: D = astrid-dev, R = Runtime, A = App, X = cross-repo.

| Id | Title (short) | Repo | P/W | tasks.md claims | What release/15/main shows | Verdict |
|---|---|---|---|---|---|---|
| G0 | Worker smoke for Runtime and App | D,R,A | 1 / w0 | [x] 16 Nov (`tasks.md:38`) | astrid-dev `env/` holds `runtime-pytest.sh`, `app-test.sh`, `runtime-fixture-preflight.py`, `agent-setup.sh`. The Runtime and App copies were not compared. | DONE |
| G1 | Baseline on `release/14/main` heads | X | 1 / w0 | [ ] open, "folded into G2" (`tasks.md:39`) | The `release/14/main` heads are no longer the base (Release 15 is). G2 superseded it. | STALE |
| G2 | Re-measure after phase 1 | X | 1 / stop | [x] 19 Nov (`tasks.md:59`) | A record, taken on Release 14 heads. Numbers are not a Release 15 baseline. | DONE (record only) |
| RS1 | Review stop | X | 1 / stop | [x] 19 Nov, findings (`tasks.md:60`) | A record. | DONE (record only) |
| RE1 | Runtime jobs install the Agent at the pin, set `ASTRID_CHECKOUT` | R | 1 / w1 | [x] (`tasks.md:43`) | `ci.yml:96-147` (unit), `:261-306` (boundary), `:320-356` (sandbox), `:395-447` (portability) read `tests/astrid-agent.pin` and set `ASTRID_CHECKOUT`. Pin is `0e1543e0` (see section 4). | DONE |
| RE2 | No scratchpad fallback for the Agent source | R | 1 / w1 | [x] (`tasks.md:44`) | `git grep scratchpad` finds nothing in `tests/test_timeline_clip_replacement.py` or `tests/astrid_checkout.py`. | DONE |
| RE3 | `git archive` tests have their commits | R | 1 / w1 | [x] for unit; Nightly lane = RT9 (`tasks.md:45`) | `unit` and `sandbox` use `fetch-depth: 0` (`ci.yml:107`, `:329`). `nightly.yml:52-67` adds a "Check historical Agent archive input" step that only warns if `321cef4b` is not served. | DONE for unit; Nightly part is RT9 |
| RE4 | `tsc` available to `unit` | R | 1 / w1 | [x] for unit (`tasks.md:46`) | `setup-node@v4` node 22 plus locked `tsc` on PATH in `unit` (`ci.yml:147-153`) and Nightly (`nightly.yml:85`). `sandbox-process-control` has no setup-node step; the handover said four of its tests lacked `tsc` (`handover.md:25`). | UNCLEAR |
| PE1 | App Lanes use the App's pins, not `main` | A | 1 / w1 | [x] (`tasks.md:47`) | `lanes.yml:31-48` and `:132-151` read Runtime and Agent SHAs from `public/install-manifest.json`. Inputs D7's check that `vendor.lock.json` and the manifest name the same Agent commit was not looked for. | DONE |
| K1b | Runtime quarantine guard | R | 1 / w1 | [x] (`tasks.md:50`) | `tests/lanes.py:106-292`: `DECLARED_XFAILS` entries are `strict=True` with issue URL, owner, expiry, `MAX_XFAIL_DAYS = 14`; guard errors on a missing field, an expired entry, an expiry over 14 days out. | DONE |
| K1b-cap | (derived) Runtime quarantine at most 10 | R | 2 | tasks.md:50 says "wave 2 lowers the ceiling to 10" | `tests/lanes.py:244` `MAX_DECLARED_XFAIL_TESTS = 20`. 19 node IDs are declared. All seven entries have owner "R14 Lead" and expiry 2026-12-01 (7 days from today). plan.md:97 and inputs.md:145 say 10. | OPEN |
| K1b.1 | Runtime guard under xdist | R | 1 / w1 | [x] (`tasks.md:55`) | `tests/lanes.py` contains xdist handling (grep hit). Not exercised. | DONE (static) |
| K1c | App quarantine guard; vitest on PRs | A | 1 / w1 | [x] (`tasks.md:51`) | `scripts/quality/check-known-failures.mjs:9-18`: `MAX_QUARANTINE_ENTRIES = 10`, `MAX_EXPIRY_DAYS = 14`, required fields id/file/title/issue/owner/expiry. `test.yml:193-195`: vitest runs on PRs into release branches. Entries in `config/testing/direct-journey-expected-failures.json` (4, issues #249-#252) have owner "Plan 39 manager" and expiry **2026-11-25, tomorrow**. `config/testing/skipRegistry.mjs` itself has no strict/owner/expiry (it is the skip registry, not the quarantine list). | DONE |
| K1c.1 | App guard cannot be fooled (run-time expected-fail set equals the registry) | A | 1 / w1 | [x] (`tasks.md:56`) | `check-known-failures.test.mjs:103-121` tests the registry rules. The run-time equality check from the card was not found by grep. | UNCLEAR |
| SF3a | Every `main`/`int` run stores per-test results | R,A | 4 / w0 | [x] (`tasks.md:144`) | Runtime: `-rA --junitxml` plus upload `test-results-*` in `unit` (`ci.yml:165-193`), `sandbox-process-control` (`:361-390`), `portability-lifecycle` (`:451-497`) and Nightly (`nightly.yml:93-121`). Not in `windows-realm-publication`, `darwin-native`, `boundary` (`pytest -q`). App: no JUnit or per-test upload in `test.yml`, `lanes.yml` or `e2e.yml`; e2e uploads only `test-results` directories. vitest reporter is the skip guard only (`vitest.config.ts:66`). | OPEN (Runtime done, App missing) |
| K2 | Trusted per-ID comparison on each product PR | R,A (+Agent) | 3 | [x] (`tasks.md:132`) | No comparator, inventory or sealed-list file in Runtime or App `release/15/main` workflows or scripts. `releases/14/run.md:114` says K2/K3 "is not on `release/14/main`; it moves to Release 15"; issue #984 (activation) is open. | OPEN (claim is about the plan branch only) |
| K3 | Same comparator nightly on release-tier jobs | R,A (+Agent) | 3 | [x] (`tasks.md:133`) | Same as K2. | OPEN |
| RT1 | Verify migrated-realm readiness | R | 2 / D | [ ] (`tasks.md:108`) | `releases/14/run.md:169` marks R14-P39-15 "Release 15", restart pending. `6846891f` not on release/15/main. | OPEN |
| RT2 | Fresh provider registration on migrated-realm restart | R | 2 / D | [ ] (`tasks.md:109`) | Same. | OPEN |
| RT3 | v28 fixtures match C28 | R | 2 | [ ] (`tasks.md:110`) | Nothing to contradict. | OPEN |
| RT4 | No test drives the retired timeline writer | R | 2 | [ ] | Nothing to contradict. | OPEN |
| RT5 | Stubs match real interfaces | R | 2 | [ ] | Nothing to contradict. | OPEN |
| RT6 | Runtime long tail (about 207 distinct IDs outside the cut, `tasks.md:184`) | R | 2 | [ ] (`tasks.md:113`) | Nothing to contradict. | OPEN |
| RT6.1 | macOS watchdog failure | R | 2 | [ ] | Same test as RT11. | OPEN |
| RT6.53 | Refuse visual fields on audio tracks (10 Nightly IDs) | R | 2 / D | [ ] | Nothing to contradict. | OPEN |
| RT6.58 | Refuse mutation after ancestor/history checks (22 Nightly IDs) | R | 2 / D | [ ] | Nothing to contradict. | OPEN |
| RT7 | Installed lifecycle and update (8 IDs) | R | 2 / D | [ ] | Nothing to contradict. | OPEN |
| RT8 | windows-realm-publication | R | 2 | [ ] | Job exists (`ci.yml:22`). | OPEN |
| RT9 | Snapshot certification input (Agent `321cef4b` not served) | R | 2 | [ ] (`tasks.md:119`) | Nightly now warns instead of failing (`nightly.yml:52-67`), and the two `test_snapshot_legacy_certification` xfails are still declared (`lanes.py:169-176`, issue #806). | UNCLEAR |
| RT10 | `SKIP_REGISTRY` names removed Windows legs | R | 2 | [ ] (`tasks.md:120`) | `tests/lanes.py:106` `SKIP_REGISTRY = {}` is now empty, so the stale names are gone. Whether `test_skip_registry.py` passes was not run. | UNCLEAR (likely stale) |
| RT11 | macOS watchdog fails once | R | 2 | [ ] | Nothing to contradict. | OPEN |
| RT12 | Delayed cleanup ACK test fails at random | R | 2 | [ ] | Nothing to contradict. | OPEN |
| RT13 | Custody spawn xfail hit a 120 s timeout | R | 2 | [ ] | Nothing to contradict. | OPEN |
| PT1 | App vitest (16 files) | A | 2 | [ ] (`tasks.md:124`) | Nothing to contradict. Triage guess P-a (`inputs.md:85`) is unverified. | OPEN |
| PT2 | Shared E2E setup, seven mechanisms | A | 2 / D | [ ] (`tasks.md:125`) | Nothing to contradict. All six `e2e.yml` jobs still exist. | OPEN |
| PT3 | Add-to-timeline (5) and extension reload (3) | A | 2 | [ ] | Nothing to contradict. | OPEN |
| PT4 | Visual baseline | A | 2 | [ ] | Nothing to contradict. | OPEN |
| PT5 | Conflict shown, draft kept after lost ACK | A | 2 / D | [ ] | Nothing to contradict. | OPEN |
| PT6 | Source tuple preserved across Quick Journey | A | 2 / D | [ ] | Nothing to contradict. | OPEN |
| PT12 | Browser-rendered film download | A | 2 / D | [ ] | Nothing to contradict. | OPEN |
| FIX-11 | Cleanup ACK fences activation (#905) | A+R | 2 / C | [ ] (`tasks.md:105`) | Not found landed. | OPEN |
| FIX-12 | Owner retry with durable logs settles (#926) | R+Agent | 2 / C | [x] (`tasks.md:106`) | Runtime #70 `8e8711fd` is an ancestor of release/15/main. Agent #439 not checked. | DONE (Runtime half) |
| AT21 | Time and fix the 26 Agent-and-Runtime CPU journey cases (#578) | X | 2 | [ ] depends on Plan 50 RB-1 (`tasks.md:97`) | Tests are in the Agent; not in Plan 91's "Taken from Plan 39" table. | OPEN (owner unclear) |
| K4 | `release-contract`: every release-tier check green on each pinned commit | D | 3 | [ ] (`tasks.md:134`) | astrid-dev `.github/workflows/docs.yml` jobs are documentation, refresh-generated, vision-consumer-contract, publish-vision. No `release-contract` job, no `scripts/release_record.py`, no `ci/required-checks.json`. Plan 31 RL-1b is `[ ]` (`plans/31.../tasks.md:22`). | OPEN |
| K5 | Release skill rule text | D | 3 | [ ] (`tasks.md:135`) | Depends on K4, SF4, SF5. | OPEN |
| Owner | Turn on merge-tier required checks; `release-freeze` ruleset | owner | 3 | [ ] (`tasks.md:136`) | `releases/14/evidence/nightly-qualification.md` (21 Nov): none of nine product refs had an effective branch rule. | OPEN |
| R | Final review (at most 3 rounds) | X | 3 | [ ] "all retained Release 14 tasks" (`tasks.md:137`) | Scope wording refers to Release 14. | STALE |
| SF1a | Three-products tests own their seed | A | 4 | [ ] (`tasks.md:139`) | `tests/e2e/local/three-products.spec.ts:54-61` worker-scoped `seed3`; `:83` `mode: 'serial'`. | OPEN |
| SF1b | Journey runs parallel and shuffled | A | 4 | [ ] | Same file still serial. | OPEN |
| SF2a | Expected failure names step and error | A | 4 | [ ] (`tasks.md:141`) | `direct-journey-expected-failures.json` entries have no `step` or `error` field. | OPEN |
| SF2b | Unmarked test: Runtime refuses wrong media selection | A | 4 | [ ] | Not found. | OPEN |
| SF2c | VIDEO-DROP on the commit-time path | A | 4 | [ ] | `P39-R12-VIDEO-DROP` is still a registry entry (issue App #252, expiry 2026-11-25). | OPEN |
| SF3b | Compare candidate with published `main` from stored results | D | 4 | [ ] (`tasks.md:145`) | `env/baseline-diff.py` exists; `env/ci-results.sh` does not. | OPEN |
| SF4 | Candidate is `main` plus a listed set of fixes | D | 4 | [ ] (`tasks.md:147`) | Needs K4 and Release skill owner's agreement; `inputs.md:128` says no advisor review yet. | OPEN |
| SF5 | Freeze product `main`s during a release | D | 4 | [ ] (`tasks.md:148`) | Same. | OPEN |
| Nightly report | `scripts/ci_red_report.py` plus nightly workflow (no task row) | D | 3 | Listed only in plan.md:126, plan.md:98, plan.md:111 | astrid-dev `.github/workflows/` has only auto-merge, claim-project, docs, issue-intake, review-intake. No `ci_red_report.py`. Rolling issue #971 exists and is open. | OPEN |

Excluded as Agent-only (in Plan 91's table or Agent code): GL, GL.1-GL.3, AE1, AE2, K0, K1a, K1a.1, SF3a.1, SF3c, AT1.x, AT1.9, AT1.54, AT2-AT20, AT22-AT27, LS-7, #869, SF6a-e, SF7, and the Release 12 follow-up paragraphs (`tasks.md:5-13`).

Orphan check: Plan 91's "Taken from Plan 39" table (`plans/91.../tasks.md:131-150`) names only SF3a, GL*, K0, K1a, K2/K3 (Agent), SF6d, AT1.1, AT1.2, AT1.3, AT1.5, AT1.10, AT1.34, AT1.50, AT1.21, AT1.111, AT1.113, AT1.233, AT4, AT9, AT11, AT12, AT12.1, AT27, LS-7, AT1.14/.15/.38/.96, R15-1, R15-2. These Agent rows are not named there: AT1.6, AT1.7, AT3, AT5-AT8, AT10, AT13-AT20, AT22-AT26, #869, K1a.1, SF6a-c, SF6e, SF7, SF3c, AT21. They may be covered by Plan 91's own cards (Wave C is "by file"), or may be dropped; this needs confirming with Plan 91's manager. They are not in this table.

## 2. Stale text in plan.md and tasks.md

Release 14 / int branch / branch names
- plan.md:9 owner "Release 14 Lead (`session_011EzfW3Zy19ncNecpQnKb7D`), by packet dispatch". Release 14 is closing; same string in `plans/index.md` and `inputs.md:9` ("Run start"). Release 16 names no manager (`releases/16.md:5`).
- plan.md:44-86 whole "Release 14 scope" section, including `release/14/plan-39` and `release/14/main` as landing place (plan.md:50), "replaces `int/39-green-mains`", the "Done for Release 14" three-nights rule (plan.md:52), and the waves table (plan.md:78-84). `releases/16.md:79-82` now lists `release/16/plan-39` in astrid-dev, Agent, Runtime and App.
- tasks.md:23 "Where work lands: by PR to `release/14/plan-39`"; tasks.md:189-199 "Release 14 waves"; tasks.md:191 refers to "Release 15" for the SF/K4 rows; tasks.md:164-187 "Release 15 ceiling" heading and table (R15-1..R15-5 owner rows).
- inputs.md:143 D1 "int/39-green-mains" (already marked replaced at plan.md:50, but D1 is not).
- inputs.md:9 "Run start" and tasks.md:207 "dispatch queue" point at `releases/14/run.md`.
- plan.md:48 and `releases/14.md:75`: Release 14 brief says K2/K3, the ceiling, required checks, gate hardening and evidence trees "move to Release 15" and that `release/14/plan-39` "is not merged whole". tasks.md still shows them `[x]` as if landed (K1a-K1c, K2, K3, SF3a). Only the Release 14 picks reached release/15/main; see section 1.

16 Nov measurements
- plan.md:56-66 "Measured on 16 November" table (Runtime 77 failed/1,010 errors, Agent 250/160, App six E2E jobs failing); plan.md:58 "G1 replaces this table".
- plan.md:66 "R-a, R-b, R-c, R-f, A-c and A-i are still present on `release/14/main`": R-a, R-b, R-c, R-f are now fixed in Runtime (RE1-RE4); A-c and A-i are Agent.
- inputs.md:46-92 triage counts from 9 Nov; inputs.md:157-162 source identities (Agent `a105de3a`, Runtime `4f5477cb`, App `57e200b4`).
- handover.md (written 16 Nov, 21:00 UTC): whole file is a dated snapshot of branches that have since moved; its "first step" (bring tasks.md up to date) is done. Its 547 errors are explained by the pin it asks to change.

Owner and "three mains" wording
- plan.md:1 title "All three mains green"; plan.md:3 project name; plan.md:23 "astrid-agent, astrid-runtime and astrid-app"; plan.md:25, 134 "three repositories"; plan.md:29-34 Included list still names the Agent's four workflows with a "moved" note; plan.md:76, 80, 83, 110 ("three repositories in parallel"); tasks.md:1 title; tasks.md:205 "Agent, Runtime and App can work in parallel". plan.md:21 itself says "Where the text below says three repositories, read the Runtime and the App".
- plan.md:7 Status `active` and `plans/index.md` row show `active`, while Release 16 is Draft with no release manager.

Estimate and Waiting on
- plan.md:11 estimate "22-31 (8-11 elapsed): phase 1 6.5, phase 2 13-21, phase 3 3.5" disagrees with tasks.md:234 "30-60 engineering days ... parallel across the three repositories". Neither has had the Agent's share removed (Plan 91 now carries 55-72 days for it, `plans/91.../tasks.md:154`). The index row repeats "22-31".
- plan.md:13 Waiting on: "a manager; G1 redone on `release/14/main`; Plan 38 for the custody tests; Plan 31 RL-1b for K4, which is Release 15's; Release 16 for the rest of phase 4, K4 and K5". G1 is superseded; "K4, which is Release 15's" contradicts "Release 16 for ... K4". Plan 31 itself is in Release 16 (`releases/16.md:31`).
- plan.md:48 "K4 and K5, which wait for Plan 31, are Release 15's".

Wording that now belongs to Plan 91
- plan.md:23, 30, 95-100 (Agent registry and `tests/test_skip_policy.py`), 108 (Agent Ruff import-sort and Windows custody), 112, 118-120, 134 (Agent workflows green three nights); plan.md:127 Agent mypy/Ruff baselines; inputs.md:66-79 whole Agent triage table; inputs.md:95-105, 112 (Agent items); inputs.md:150-152 D8, D10 (Agent).
- tasks.md:5-13 Release 12 follow-up paragraphs; tasks.md:38-258 every AT*, AE*, GL*, K0, K1a*, SF3a.1, SF3c, SF6*, SF7 row; tasks.md:172-183 Agent rows of the "Release 15 ceiling" table; tasks.md:215-217 and 225 Agent required checks; tasks.md:246-257 Agent K2/K3 follow-through paragraphs. Plan 91 D3 (`plans/91.../inputs.md:83`) also puts Plan 38 custody tests outside Plan 39's cap.
- Release docs: `releases/16.md:36` summarises Plan 39 as "the structural fixes from Release 12, and the release rule ..." and omits the Runtime and App green work; `releases/16.md:80` lists `release/16/plan-39` in astrid-agent; `releases/15.md:116-169` still lists all plan:39 issues as Release 15 issues ("Pulled from GitHub on 2026-11-15"), while `releases/16.md` has none.

Facts that moved
- plan.md:101 (quarantine) says "ten per repository"; Runtime is at 19 IDs with ceiling 20 (D9 at inputs.md:151).
- plan.md:26 / tasks.md:209-230 Required checks list `ci/required-checks.json` as written by K2; the file does not exist.
- tasks.md:222 App `release-guard` "excluded because Plan 31 deletes it": still present at `test.yml:147`.

## 3. Issues labelled plan:39 (38 found by the API, all open)

| # | Title (short) | Scope |
|---|---|---|
| 1313 | test_fail_closed_g28 settlement case fails on release/15/main | Agent (Plan 91); also plan:13 |
| 1307 | three timeline tests fail, 37 error, on Release 15 forward base | Agent (Plan 91); also plan:81 |
| 1291 | five tests fail on untouched release/15/main in Agent | Agent (Plan 91) |
| 1290 | giant-file check cannot stop growth, failing today | Agent (Plan 91); also plan:13 |
| 1158 | Trace two call failures from grouped Undo and endpoint fixtures | Agent (Plan 91) |
| 1141 | Decide expected clip position, 1 s move at 30000/1001 fps | Agent test expectation; owner decision |
| 1130 | Missing five-second child-discovery signal in two D18 cases | Agent (Plan 91) |
| 1127 | Two retained-source rendering cases lack the Remotion project dir | Agent (Plan 91) |
| 1011 | Child-bridge and device-ambient receipt outcomes | Agent (Plan 91) |
| 1007 | Remaining S01 call failures | Agent (Plan 91) |
| 1006 | Retained media selection digests after H31 upgrade | Agent (Plan 91) |
| 1002 | Undo of shared video unplace refused after restart | Agent (Plan 91) |
| 984 | K2/K3: activating the failure-ceiling comparator | Cross-repo (Agent, Runtime, App) |
| 971 | Nightly new-red report (D4, rolling) | Cross-repo (astrid-dev) |
| 964 | `astrid/_tls_policy.py` adds structure finding over GL.2 ceiling | Agent (Plan 91) |
| 925 | VibeComfy `release/14/main` CI cannot qualify anything | Outside all three repos; needs scope decision |
| 910 | Windows receipt temp files at 261-262 UTF-16 units | Cross-repo (Runtime writer, Agent review) |
| 809 | Top-level timeline text hook remains quarantined | Runtime |
| 807 | Historical audio trim held by Runtime strict quarantine | Runtime |
| 806 | Legacy capture recertification quarantined in Runtime | Runtime |
| 805 | Runtime quarantine retains 14 tests of retired writers | Runtime |
| 785 | H3 end-to-end test fails intermittently | Agent (Plan 91) |
| 733 | Readiness tests fail on busy machine (2 s probe) | Agent (Plan 91) |
| 647 | Structure baseline stale (59 vs 13) | Agent (Plan 91) |
| 639 | `TestPackDeclaredBackendIds` fails on R12 and R13 | Agent (Plan 91) |
| 637 | 133 SDK timeline tests assert a hard-coded Runtime commit | Agent (Plan 91) |
| 636 | `test_shared_redo_rechecks_source_archive_at_acceptance` order-dependent | Agent (Plan 91) |
| 633 | Parked mypy type-only fixes | Agent (Plan 91) |
| 626 | Foley selection test fails | Agent (Plan 91) |
| 621 | Pinokio adapter readiness flake | Agent (Plan 91) |
| 615 | Stale or environment-dependent Agent fixtures | Agent (Plan 91) |
| 614 | Unit shards 1 and 5 never finish | Agent (Plan 91) |
| 613 | Release 13 ruff/mypy additions | Agent (Plan 91) |
| 612 | Release 13 engine-lane items deferred | Agent (Plan 91) |
| 611 | Terminal publication replay unbounded | Agent `generic_host.py` (Plan 91 or Plan 13) |
| 606 | Agent skills test never runs in CI | Agent (Plan 91) |
| 585 | Agent integration lane dependencies not provisioned | Agent, also plan:50 |
| 578 | CPU journey takes 57 min for 26 tests | Cross-repo (Agent plus Runtime), also plan:50 |

Totals: Runtime 4 (#805, #806, #807, #809); App 0; cross-repo or astrid-dev 5 (#984, #971, #910, #578, and #925 as outside scope); Agent 29 (including #1141, #611, #585). Plan 39's remaining issue set for Runtime and App is thin: no open issue is labelled for any App row (PT*, SF1-SF2). Release 16 lists none of these; Release 15 lists them as Release 15 issues.

Note: #805 says "14 tests", the registry now holds 19 IDs in the code, so the issue count is itself stale.

## 4. Open owner decisions and questions that still apply to Runtime and App

From `inputs.md:139-152` and the handover:
1. **D2 required checks**: two tiers, merge tier into branch protection (Hannah). Not done; no effective rule on the nine product refs as of 21 Nov (`releases/14/evidence/nightly-qualification.md`). `ci/required-checks.json` not written.
2. **D3 / D9 quarantine ceiling**: plan says 10; Runtime is at 19 IDs with `MAX_DECLARED_XFAIL_TESTS = 20` (`tests/lanes.py:244`). D9 says wave 2 brings each repo to 10 or fewer before Release 14 ships. That did not happen. Decision needed: re-affirm ceiling, retire entries, or raise the cap. All Runtime entries expire 2026-12-01 and name "R14 Lead" as owner; all four App entries expire 2026-11-25 and name "Plan 39 manager". Both owner names are stale.
3. **D4 nightly report output** (job summary plus one rolling issue): still a "Recommendation", never marked decided, though #971 exists.
4. **D7 App pin skew**: PE1 makes Lanes read the manifest; the same-commit check or recorded reason was not found.
5. **D6 review rounds** (RS1 one, final R three): R still covers "Release 14 tasks".
6. **SF4 and SF5** need the Release skill owner's agreement and an advisor review (`inputs.md:128`, `tasks.md:147-148`); neither is recorded.
7. **Handover ruling 1, Agent pin in Runtime tests**: `tests/astrid-agent.pin` is now `0e1543e0`. Issue #615 calls `0e1543e0` "R12 main", i.e. an old Agent commit, not the head of `release/14/main` or `release/15/main` the handover recommended. Handover (`handover.md:38`) said the older pin caused 547 errors because it lacked `astrid.sdk.timeline.commit`. Whether the current pin is intended was not checked (no Agent clone). Worth confirming.
8. **Handover ruling 4**: Agent `321cef4b` not served by the public remote. Nightly now warns (`nightly.yml:52-67`); the ruling is unresolved.
9. **VibeComfy scope** (`inputs.md:124`, issue #925): owner and scope decision requested, not answered.
10. **#984 K2/K3 activation**: the comparator exists only on the Release 14 plan branches; owner must decide whether it lands in Release 16 for Runtime and App, and in what form (Plan 91 reuses `env/baseline-diff.py` for the Agent, per `plans/91.../tasks.md:137`).
11. **#1141** (clip position at 30000/1001 fps): asks for authorisation to change one expectation; Agent-side but a Plan 39 issue.
12. Release 16 has no release manager (`releases/16.md:5`), and Plan 39's owner is a Release 14 session.

## 5. Overlaps with other plans touching Runtime/App CI

- **Plan 31** (Release 16): K4/K5 are rules in Plan 31's `release-contract` (RL-1b). RL-1b is still `[ ]` and astrid-dev has no `release-contract` job or `scripts/release_record.py`. Plan 39's K4 cannot start before it. Plan 31 RL-0 (App worker setup) is `[ ]` while G0 here is marked done and delivered "whichever is not merged" (`tasks.md:38`); the two plans disagree about who owns `env/app-setup.sh`. The `release-guard` job in App `test.yml:147` is deleted by Plan 31 but is still there.
- **Plan 38** (Release 16): custody and host-spawn tests are excluded from Plan 39's count. Plan 38 E1 replaces Runtime `darwin-native` with a `host-spawn` matrix (`plans/38.../tasks.md:36`); Plan 39's required-check list for the Runtime names `host-spawn` "once it lands". RT10 and RT13 and #808 (declared xfail) depend on Plan 38. W0 (`env/runtime-setup.sh`) is shared with G0.
- **Plan 91**: owns the Agent half of SF3a, K2/K3, K1a and the comparator; reuses `env/baseline-diff.py`. Its D3 puts Plan 38's custody tests outside the cap of ten. Plan 39's remaining Runtime/App K2/K3 must reuse the same comparator to avoid two implementations.
- **Plan 55** (paused, Release 15): Plan 39 leaves alone tests in Plan 55's inventory (`plan.md:54`) and LS-7 is a Plan 55 load proof (`tasks.md:207`). Plan 55 is Agent-heavy; limited Runtime/App overlap. Not verified further.
- **Plan 50** (Release 16): RB-1 runs the CPU journey in the lane; AT21/#578 and #585 depend on it (`tasks.md:97`). Cross-repo (Agent plus Runtime).
- **Plan 13** (Release 16): labels on #1313 and #1290 (`plan:13`); the giant-file guard on `generic_host.py`. Agent only.
- **Plan 81 / 77 / 75 / 63 / 76**: #1307 carries `plan:81`; Runtime #109 (Plan 77 save) is the head of release/15/main and its gate evidence sits in `releases/15/evidence/plan-77-agent-gate-*`. Plans 63 and 76 are in Release 16 and change App behaviour covered by PT5 and the three-products spec; I did not verify how they would collide with SF1a/SF2a. Plan 61 App workflows (`p61-*.yml`, `plan61-real-macos` in `test.yml:24`) also touch the same files.
