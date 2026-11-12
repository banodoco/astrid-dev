# Inputs — All three mains green

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah asked for this plan on 9 Nov 2026 in session https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9. It starts right after release 12 is published. The end state: every CI workflow on Agent, Runtime and App `main` is green and kept green, and the release rule changes from "no new red" to "everything green".

**Prior art:** the main runs measured on 9 Nov, the code at those SHAs, and the [Plan 38 test inventory](../38-one-process-identity/tasks.md#test-inventory). The runs:
- Agent CI 42553788480, Lanes 42553788553 and Windows task host journey 42553788523, at `a105de3a4852cb61b9647dfe2c920118bd29f272`;
- Runtime CI 42553816749 at `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f`;
- App Tests 42553827565, Lanes 42553826381 and E2E 42553826369, at `57e200b4`.

The orchestrator extracted those logs ([session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9)), because this planning session's proxy refuses the Actions API for unattached repositories. The release-12 candidate's Runtime unit job is 129056194610. Code was read at those SHAs by seven read-only helpers, and every line this plan relies on was re-read by the planner. Prior plans: [Plan 29](../29-update-and-release/inputs.md#planning-evidence) decision 6 deferred full CI health, and its UR-0 stopped unfinished; [Plan 38](../38-one-process-identity/tasks.md#test-inventory) owns the custody tests; [Plan 31](../31-releases-from-astrid-dev/tasks.md) owns `release-contract` and RL-0. The [triage below](#root-cause-triage) has the details.

**Approach:** fix by root cause in three phases.
1. CI environment and wiring first, since one cause in each repository hides most of the rest.
2. Then the stale tests and real bugs, one cause per small task, with the repositories in parallel.
3. Then keep it green with what already exists:
   - each repository's skip and xfail registry, extended with an issue, an owner and an expiry;
   - one required-checks file in astrid-dev, read by the nightly report and by Plan 31's `release-contract`;
   - Hannah's branch protection.

Rejected:
- a fresh "known failures" baseline per repository. It keeps red as normal, which is the problem being fixed;
- skipping the cross-repository tests. They are the only proof that the pinned pair works;
- a second release gate beside Plan 31's;
- re-baselining mypy upward.

**Challenge:** Reviewed — advisor review, 9 Nov 2026, in the [orchestrator session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9), before merge. Findings: (1) G1 must re-measure on the published release-12 heads, not cand/29-r12 ff40f2c6: release 12's fixes for the Agent ESBUILD collection error, Windows custody, the wheel smoke and Ruff live on fix/r12-autostart and reach main only when release 12 publishes, so A-a and the Windows rows may already be green; drop the tasks G1 shows are fixed. (2) The anti-hiding rules are right and are acceptance criteria, not guidance: the v33 and migrated-realm fences reach ready only through provider_ready(), with a negative case, and a test is never re-expected to pass. (3) The strategy row moves from 'a release rule plus a one-off batch, not a plan' to this plan because the owner asked for the project on 9 Nov; the owner sees that change in this PR. (4) AT1 is the dominant unknown; keep the stated split rule (over 60 Agent failures re-plans it) as a hard trigger.

**Proof and limits:**
- **Proof:** each workflow named in [plan.md](plan.md#outcome-and-scope) passes on the final `main` head of its repository on three consecutive nights. The quarantine guard fails on an expired entry, or on a strict xfail that starts passing. `release-contract` refuses a record whose pinned commit has a failed required check.
- **Limits:**
  - the counts are from one run per workflow, and G1 re-measures them on the release-12 heads;
  - the Agent's true failure count is unknown, because every unit and integration shard aborts at collection on `main`;
  - GitHub-hosted runners only;
  - branch protection is Hannah's setting.

## Root-cause triage

The counts were measured on 9 Nov from the main runs. "E" means a pytest error at setup or collection, and "F" a test failure. Classes: **env** (CI environment or tooling), **xrepo** (a cross-repository import or checkout), **stale** (a test or fixture against behaviour that changed on purpose), **bug** (a real product bug), **flaky**, and **38** (owned by Plan 38). "Verify" marks a stale guess that could hide a real bug, and its task must rule that out first.

### Runtime `CI` (unit ubuntu: 77 F, 8352 passed, 1010 E; macOS about the same; sandbox-process-control: 135 F, 1014 E, same clusters)

| # | Cause | Count (unit ubuntu) | Class | Evidence | Task |
|---|---|---|---|---|---|
| R-a | `unit` and `sandbox-process-control` install no Agent and set no `ASTRID_CHECKOUT`. The fallback `../astrid` never exists | 457 E "Astrid checkout is unavailable", and 10 E + 9 F + 8 BootstrapError "No module named 'astrid'" | xrepo | `tests/astrid_checkout.py:19-24`; `ci.yml:89-114` has no Agent step; 39 test files import `astrid`, 4 of them at module scope | RE1 |
| R-b | A test falls back to a hard-coded agent scratchpad path | 92 E "frozen ordinary Agent source is unavailable" | stale (env-shaped) | `tests/test_timeline_clip_replacement.py:96-106` | RE2 |
| R-c | `git archive <sha>` on depth-1 checkouts | 159 E CalledProcessError | env | `tests/test_snapshot_legacy_certification.py:20-32`, `tests/test_v33_protected_acceptance.py:32-45` | RE3 |
| R-d | v33 activation fence: fixtures restart a migrated realm without provider verification | 168 E + 12 F | stale, **verify** | `runtime_protocol/v33_lifecycle.py:297-300`, called per mutation at `service.py:874` | RT1 |
| R-e | A migrated realm starts without a Timeline provider (neutral profile) | 124 E | stale, **verify** | `runtime_protocol/daemon.py:317-320`; neutral by design (`timeline_commit_provider.py:72-78`) | RT2 |
| R-f | `tsc` is not on PATH in `unit` | 6 | env | `ci.yml:89-114` has no setup-node; bare `tsc` at `tests/test_timeline_bundle2_contract.py:93` and `tests/test_timeline_commit_contract.py:765` | RE4 |
| R-g | Hand-built v28 layouts vs the C28 fingerprint | ≤2 files | stale, **verify** | `runtime_protocol/v33_manifest.py:109-111`; `tests/test_realm_admission_hardening.py:993`, `tests/test_spec_reference.py:263` | RT3 |
| R-h | Tests still driving the retired legacy timeline writer | a few, in the tail | stale. A 200 where 410 is expected would be a bug | `service.py:450-458`; 19 files reference it | RT4 |
| R-i | `SimpleNamespace` stubs missing attributes the code now reads | a few, in the tail | stale | e.g. `tests/test_platform.py:165` patches `sys` with `platform` only, but `platform.py:1142`, `:1256` read more | RT5 |
| R-j | Long tail, 1–4 each: realm integrity, settlement `effect_type`, CommitOutcomeUnknown, KeyError `windows-worker-handoff`, diagnostics "Last update result" text, DID NOT RAISE, PermissionError, FileExistsError | about 20 | **unclassified**. DID NOT RAISE and realm integrity are candidate bugs | orchestrator digest | RT6 |
| R-k | portability-lifecycle: "foreground Runtime exited 1", selection-or-inputs-invalid, no `astrid` | 7 F ubuntu, 8 F macOS | xrepo + unclassified | `ci.yml:211-283` | RT7 |
| R-l | windows-realm-publication | 1 F | unclassified | — | RT8 |
| R-m | process identity, DuplicateOwner, StaleOwner, seccomp pidfd, darwin-native custody | ~15 + darwin 1 | 38 | Plan 38 inventory | Plan 38 (F1, L1, E1) |

Drift that comes with it: `ci.yml:31` and `:143` hard-code Agent SHAs `e425903f`, `4866090e`, which differ from `tests/astrid-agent.pin` (`b05ac03a`). Plan 38 E1 replaces those two lines. RE1 uses the pin in the other jobs.

### Agent `CI`, `Lanes`, `Windows task host journey`

| # | Cause | Count | Class | Evidence | Task |
|---|---|---|---|---|---|
| A-a | Module-level `os.environ['ASTRID_BUILD_TEST_ESBUILD']` aborts collection in every unit shard, `darwin-native` and every Lanes integration shard. No workflow sets it | every shard, so 0 tests run (e.g. "24531 deselected, 3 errors") | env | `tests/pack_builder/test_pack_build.py:13`. Still unchanged at `cand/29-r12` `ff40f2c684fc7ce22e42a5cacda5c63a0c8800a9` | AE1 |
| A-b | Failures hidden behind A-a. Measured on release 12 against Release 10: 398 regressions in 15 causes, all from commits in served release 11 (`a105de3a`); about 306 are stale tests or test-infra and belong here, the product regressions are release 12's ([evidence](evidence/release-12-r10-diff.md), D8) | 398 vs Release 10 (plus Release 10's own 1010) | mostly stale tests; 4 product causes fixed by release 12 | [release-12-r10-diff.md](evidence/release-12-r10-diff.md) | AT1, AT1.1–AT1.7 |
| A-c | Lanes integration: the Runtime checkout lacks `d9e2a71e` (depth 1; not in the historical-objects fetch list) | all integration shards | env | `tests/editing_conformance/test_authenticated_legacy_restore.py:24`, `tests/sdk/test_timeline_checkout_history_runtime.py:25`, `tests/helpers/runtime.py:84`, `lanes.yml:76-80` | AE2 |
| A-d | mypy is over its exact-match baseline: 2345 in CI at the release 12 candidate ("regressed by 153"; 2350 locally at Release 10, which never ran Mypy because Ruff failed first). Blame: 150 from `edaa8e7c10` and 29 from `c61acfd93b` (5 Nov ports), none from release 12's commits ([evidence](evidence/release-12-r10-diff.md#mypy)). Release 12 fixes only its own additions (D8) | about 153 findings | bug (real type findings) | `scripts/reshape/baselines/mypy_astrid.json`; `scripts/reshape/count_baseline.py:19-30` | AT2 |
| A-e | Ruff: about 89 import-sort findings | ~89 | stale. Release 12 sorts them (I001 only); G1 confirms | `scripts/reshape/baselines/ruff_astrid.json` (2128) | G1 |
| A-f | windows-native-and-installer: 12× "Group custody requires a supported POSIX filesystem", 1 remotion FileNotFoundError | 13 F | bug. The orchestrator reports it fixed on release 12, though the refusal string is still at `transaction.py:210` on `ff40f2c6`; G1 confirms | `astrid/core/pack/transaction.py:210` | G1, then AT3 if still red |
| A-g | `release` wheel smoke on 3.11 and 3.12: `entries.py` ImportError | 2 jobs | bug. Reported fixed on release 12; `entries.py` is identical at `ff40f2c6`; G1 confirms | `astrid/core/generation/entries.py` | G1, then AT3 |
| A-h | Windows task host journey, pwsh and powershell: exit 1 | 2 jobs | unclassified | `windows-journey.yml:94-118` | AT4 |
| A-i | Lanes clones `peteromallet/VibeComfy` while CI clones `banodoco/VibeComfy` | latent | env | `lanes.yml:169`, `:280` vs `ci.yml:175-190` | AE2 |
| A-j | The aggregate `unit` job only echoes. A skipped shard would count as passing on a required check | latent | env | `ci.yml:227` | K1a |

### App `Tests`, `Lanes`, `E2E`

| # | Cause | Count | Class | Evidence | Task |
|---|---|---|---|---|---|
| P-a | vitest: 16 files fail. Suspected: the Plan 33 merge `698bfbd` deleted `scripts/installer/release-check.mjs`, `update-manifest.mjs` and `config/qualification/*`, which tests may still import | 16 files | stale, **verify** (inference) | `git show --stat 698bfbd` | PT1 |
| P-b | playwright-timeline (36 F across 18 specs) and chrome-export (3 F): one shared boot path, `openEditor` with the Vite dev server and the fake Runtime | 39 | unclassified (one cause likely) | `playwright.config.ts:121-150`, `tests/e2e/timeline/support.ts` | PT2 |
| P-c | Editor-with-extensions specs: `production-widget-scope.spec.ts:64`, `extension-accessibility.spec.ts:114`, `extension-cross-browser.spec.ts:76` | 3 | unclassified. A focus or a11y regression would be a **bug** | those lines | PT3 |
| P-d | extension-visual: one screenshot differs from `tests/e2e/visual-snapshots/` | 1 | stale if the UI change was intended, otherwise bug | `playwright.extension-visual.config.ts:44` | PT4 |
| P-e | Lanes `checkout-lanes` (1 of 5 files) and `quick-journey` check out Agent and Runtime at **`main`**, not the App's pins, so they inherit the other mains' red | 2 jobs | xrepo | `lanes.yml:27-38`, `:113-127` | PE1 |
| P-f | Pin skew: `config/astrid-cli-surface/vendor.lock.json` pins Agent `5dec5dc6` while `public/install-manifest.json` pins `a105de3a` | latent | xrepo | `vendor.lock.json:35`, commit `57e200b4` | PE1 |
| P-g | `vitest` runs on push only; `release-guard` on PR only. Plan 31 deletes `release-guard` | latent | env | `test.yml:19-56` | K1c |

### Ranked by tests cleared (measured)

1. **Agent A-a, the ESBUILD collection abort:** about 24,500 tests can run again. That is the biggest unlock, and the cause clears none of their own failures.
2. **Runtime R-a, no Agent in `unit` or sandbox:** about 485 per job (457 + 27 + module-scope collection), times 3 jobs.
3. **Runtime R-d, the v33 fence fixtures:** 180.
4. **Runtime R-c, git archive depth:** 159.
5. **Agent A-d, mypy:** 158 findings, 1 gate.
6. **Runtime R-e, the migrated-realm provider:** 124.
7. **Runtime R-b, the frozen source path:** 92.
8. **App P-b, the timeline boot:** 39.
9. **App P-a, vitest:** 16 files.
10. **Agent A-f, Windows custody:** 13 (likely already done by release 12).
11. Then the long tails: R-j about 20, R-k 15, and the rest under 10 each.

### Where changing a test would hide a bug

- **R-d and R-e** are deliberate fail-closed fences. A fixture must reach "ready" the way a user's Runtime does (provider registration, then `provider_ready()` at `service.py:3066`), never by writing `.v33-activation.json` as ready or by patching `require_ready`. If no production path makes a migrated neutral realm ready, that is a user-facing bug: an upgraded realm that never becomes ready. It gets an S card, not a fixture change.
- **R-h:** a test that gets 200 where it expects 410 means the retired route is live. That is a bug.
- **R-g:** the fingerprint table is the approved schema contract. The fix is the fixture, and the table changes only by its own reviewed decision.
- **A-d:** the 158 are real type findings. Each is fixed or carries a narrow `type: ignore[code]` with a reason, and the baseline only goes down.
- **P-c and P-d:** a lost focus or a changed screenshot is a bug unless a named commit changed it on purpose. Hannah sees before and after for any re-baseline.
- **R-j and A-b** are unclassified. Each row gets its class recorded in run state before its fix.

## Challenge record

The planner's own challenge, and the changes it made:
- **The release-12 claims.** The orchestrator reported that release 12 fixes the Agent's Windows custody refusal, the wheel smoke and Ruff. At `cand/29-r12` `ff40f2c6`, the ESBUILD line, the Windows refusal string and `entries.py` are unchanged. So none of these is assumed fixed: G1 measures them on the published release-12 heads, and AT3 exists in case they are still red.
- **Duplicate setup work.** Plan 38 W0 (`env/runtime-setup.sh`, `smoke.sh runtime`) and Plan 31 RL-0 (`env/app-setup.sh`, `smoke.sh app`) already specify the worker setup. G0 delivers whichever is not merged yet, to those plans' own specs. Both plans then reuse it, and nothing is built twice.
- **One gate.** The "everything green" release rule is one more `release-contract` rule (Plan 31 RL-1b), reading the same `ci/required-checks.json` as the nightly report and the branch-protection list. It adds no workflow.
- **Rejected:** a permanent per-repository baseline of known failures. That is the "no new red" rule under another name.

Release 12 also recorded [VibeComfy CI first-failure comparisons](evidence/release-12-vibecomfy-ci.md). VibeComfy's own workflows are outside this plan's stated three-repository scope; the record requests an owner and scope decision and does not establish later checks passed.

## Release 12 structural evidence

**Request:** on 12 Nov 2026 the owner asked to add work that removes the structural causes Release 12 exposed, not only their symptoms (session https://claude.ai/code/session_011EzfVzCLu2vv52JWNRiDJM). That is phase 4 in [tasks](tasks.md). SF4 and SF5 change release rules and have had no advisor review yet; one is due before they start.

Evidence, 11–12 Nov:
- **Order-dependent journey (SF1a, SF1b):** App `tests/e2e/local/three-products.spec.ts` runs `test.describe.configure({ mode: 'serial' })` with a worker-scoped `seed3` and one shared Runtime project. Four leaks, each patched in the test: a transition published by `:417` broke gate 5's seed baseline; earlier undos broke mixed editing's "no `undo_of`" check; the bootstrap test's new project became the editor's default through `src/tools/video-editor/pages/VideoEditorPage.tsx`'s `mostRecentlyCreatedProject` fallback, since a fresh browser context has no last-opened project; and gate 5 needed a 5→0 position reset. Patches: App `e2d48f428`, `d9e2798d4`, `7a971cea5`, plus the gate 5 reset. One failure skipped every later serial test, repeatedly.
- **Expected-failure markers (SF2a–SF2c):** mid-test `test.fail(true, …)`, registered in `config/testing/direct-journey-expected-failures.json` and enforced by `scripts/quality/check-known-failures.mjs` and `config/testing/direct-journey-outcome.jq`, took four review rounds to place for VIDEO-DROP, and the outcome check compares titles only. VIDEO-DROP waits for a verified-selection read the product stopped making in App `7b33f8f50`; restating it waits on App #253.
- **No stored per-test baselines (SF3a–SF3c):** Agent CI fails 1,000+ tests on R10, R11 and the R12 candidate alike. Shard 5 hit the 2-hour job limit, and R11's shards 1 and 5 were cancelled twice, so shard 1 had no baseline. Comparing by test ID needed scratch `-rA` commits (Agent `20326aa4`; Runtime `scratch/r12-rt-base` `3e59cf6b`, `scratch/r12-rt-cand` `5cdedc01`), baseline reruns and a local rebuild. Agent `ci.yml` `unit-shard` runs `pytest -q` and keeps only `test-durations` artifacts, for 3 days.
- **Release size (SF4):** the R12 Agent candidate is 207 commits and +24k lines over R11 (`a105de3a..c5370a86`). Its own regressions surfaced late: the `text` alias refused, `add_text` needing an optional pack, a broken printed recovery command, and the core boundary ratchet growing.
- **Main moved during the freeze (SF5):** App `main` gained `acfe70e7b` and `3e53462f4` (onboarding tour, another session) after the R12 cut-off `6545f130`, so the candidate re-merged twice; publication is fast-forward only. The mains report `protected: false` with no required checks.
- **Agent code (SF6a–SF6e):** clip-type alias copies in `astrid/core/rendering/_effect_registry.py` (~`:319`) and `astrid/core/rendering/storage.py` (~`:231`) beside the shared `astrid/core/element/clip_types.py`; the parsed-corpus cache in `astrid/core/element/registry.py` (~`:197-219`), keyed by neither `ASTRID_PACKS_PATH`, HOME/XDG nor the active sources; `astrid/resources/moved-elements.json`, never run against the real CLI; 45 tests importing `tests.test_verified_host_launch`, which no release has, from `tests/core/execution/test_runtime_source_custody_d40.py`, `test_runtime_orchestrator_custody_d40.py` and `tests/helpers/external_orchestrator_owner.py`; monkeypatches leaking into teardown, fixed one by one in `r12/fix-round` `3e2a254e5`, `4601e8859`.
- **Journey harness (SF7):** `scripts/journey_version_jumps.py` (~`:1716-1739`) records a macOS autostart-off capture failure as `unverified` and passes the row; harness commits `d92ea0ee6`, `fbd7e7e71` simulate a newer served release inline.

## Owner decisions

| # | Decision | Recommendation |
|---|---|---|
| D1 | Where the work lands | Each task goes by PR to `int/39-green-mains` in its repository. The Release skill promotes to `main` twice: after RS1 (environment fixes), so `main` shows real failures early, and after R. |
| D2 | Required checks: per PR, or per release | Two tiers in `ci/required-checks.json`. **Merge** checks (fast, run on every PR) go into branch protection. **Release** checks (Lanes, E2E, journeys, Nightly) must be green on the pinned commit, checked by `release-contract` and the nightly report. Requiring the slow lanes on every PR would make each PR an hour or more. |
| D3 | The quarantine ceiling | Each entry is strict xfail with an issue, an owner and an expiry at most 14 days out, with at most 10 per repository. Expiry fails CI. |
| D4 | The nightly report's output | A job summary, plus one rolling issue in astrid-dev (one comment per night with new red). No Slack. |
| D5 | Plan 29's UR-0 and the strategy row "Green mains (proposed)" | Mark UR-0 superseded by Plan 39, and point the strategy row at Plan 39 (done in this PR for the strategy row). |
| D6 | Review rounds | RS1 at most 1 round. Final R at most 3 (cross-repository and release). |
| D7 | App pin skew (`vendor.lock.json` Agent `5dec5dc6` vs the install manifest `a105de3a`) | PE1 makes Lanes read the install manifest, and adds a check that both pins name the same Agent commit, or records why they differ. |
| D8 | **Decided (Hannah, 10 Nov 2026).** Release 12's Agent CI comparison with Release 10 | Release 12 fixes every *product* regression against Release 10 (fail-open `element_schema`, the 15 unregistered `local` effects, the lost `comfy_wrap` GPU mapping, the VibeComfy COMBO/CHOICE binding) and the one CI setting (`ASTRID_TEST_LIFECYCLE_CHECKOUT`). The stale-test and test-infra causes (about 306 tests) and the Mypy debt are Plan 39's AT1.1–AT1.7 and AT2. For those, release 12's no-regression judgement is against served release 11 and `main`. |

## Source identities

Planning revisions:
- Agent `a105de3a4852cb61b9647dfe2c920118bd29f272` (`main`) and `ff40f2c684fc7ce22e42a5cacda5c63a0c8800a9` (`cand/29-r12`);
- Runtime `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f` (`main`);
- App `57e200b4` (`main`);
- astrid-dev `666cd8d`.

G1 records the published release-12 heads. Every task starts from those heads, not from these.

## References

- The orchestrator's CI digest and the mypy and Ruff note: [session](https://claude.ai/code/session_011EzfVzreGCJJQnTuXpbib9), 9 Nov 2026.
- Plan 38's [test inventory](../38-one-process-identity/tasks.md#test-inventory), W0 and E1.
- Plan 31's [RL-0 and RL-1b](../31-releases-from-astrid-dev/tasks.md).
- The [Release skill](../../skills/astrid-dev-release/SKILL.md) line "A publish never turns a passing check red", which K4 replaces.
- [Release 12 pre-existing test failures, bucket A (323 ids)](evidence/release-12-preexisting.md).
