# Agent main green

**Project:** Agent main green

**Goal:** Every CI workflow on astrid-agent `main` is green and stays green, so a red Agent check means a new regression, and anyone changing the Agent knows within one run whether they broke something.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 13–25 (about 2–3 weeks elapsed): the safety net and measurement 2–3, CI wiring 1–3, known behaviour changes 2–4, the long tail 8–15 after RS1 re-estimates it, then three green nights

**Waiting on:** the owner's go and a release (D1, recommended: Release 15); a manager

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). A red check on Agent `main` should mean a new regression. Today it means nothing: the CI and Lanes workflows have been red on every push to `main` since at least Release 12.

## Outcome and scope

The Agent's share of [Plan 39](../39-green-mains/plan.md), split off as its own project on 23 November 2026 so that one repository can reach green without waiting on the other two ([why](inputs.md#planning-evidence)). Plan 39 keeps the Runtime, the App and the shared cross-repository pieces.

Every Agent workflow that runs on a push to `main` is green and stays green:
- **Green.** Each failing test is fixed at its root cause, never by loosening an assertion to match a bug. A test changes only when the behaviour it checks changed on purpose, and the task card names the commit or contract that changed it. Plan 39's anti-hiding rules ([inputs](../39-green-mains/inputs.md#where-changing-a-test-would-hide-a-bug)) apply unchanged.
- **Cannot get worse first.** Before any burn-down, the Agent's current failing IDs are sealed as a ceiling that may only fall, and every pull request into the release branch is compared with it by test ID. New, lost or reintroduced red fails the pull request.
- **Kept green.** The owner turns on the Agent's merge-tier required checks. The Agent's existing quarantine rule (strict xfail with an issue, an owner and an expiry, at most ten per repository; Plan 39's D3 and D9) is the only way a known failure may be tolerated.

**Measured on 22 November 2026** (Agent `main` at `c0ad6b54`, the published Release 14; runs listed in [inputs](inputs.md#planning-evidence)):

| Workflow | State | Failing |
| --- | --- | --- |
| `Chat service` | green | — |
| `Windows task host journey` | green | — |
| `Windows runtime retention` | green | — |
| `CI` | red | All eight `unit` shards: 786 failed and 328 errors, in about 1,081 test IDs across 321 files, of about 32,000 tests. `darwin native` was cancelled, so its state is unknown. `fast checks`, `boundary`, `windows-native-and-installer` and both release wheels are green. |
| `Lanes` | red | All four `integration` shards: 345 failed and 435 errors. `opt-in`: 12 failed. `installed wheel` is green. |

Eight causes account for 453 of the unit failures; one refusal accounts for 249 of the integration failures ([clusters](inputs.md#failure-clusters-22-november-2026)).

**Included:** the Agent workflows on push to `main` and to `release/<NN>/main`:
- `CI`: `fast checks`, the eight `unit` shards and the aggregate `unit`, `darwin native`, `windows-native-and-installer`, `release` (3.11, 3.12), `boundary`;
- `Lanes`: `integration` 1–4, `opt-in`, `installed wheel`;
- `Chat service`, `Windows task host journey` and `Windows runtime retention`, which are green today and must stay green.

It also includes the Agent side of Plan 39's per-ID ceiling (K2/K3), gates and stored results, carried from `release/14/plan-39`, and the Agent rows of Plan 39's [Release 15 ceiling](../39-green-mains/tasks.md#release-15-ceiling).

**Not included:**
- the Runtime and the App, which stay in Plan 39;
- the cross-repository pieces that stay in Plan 39: the nightly report (`scripts/ci_red_report.py`), the release rule in Plan 31's `release-contract` (K4, K5) and the release-record sections from phase 4. This plan consumes them if they exist and does not need them to finish;
- the behaviour of the custody and host-spawn tests [Plan 38](../38-one-process-identity/plan.md) owns. This plan repairs their imports so they run, and their residual failures follow [D3](inputs.md#owner-decisions);
- the Agent's `journey.yml` release receipts, GPU and live lanes ([Plan 34](../34-real-gpu-proof/plan.md));
- product features. A real product bug found here gets its own fix task; a large one goes to an issue and is quarantined under the rule.

## Existing work and decision

The approach, the anti-hiding rules and most of the machinery come from Plan 39, which was reviewed on 9 November and ran in Release 14. Release 14 built the Agent's safety net on `release/14/plan-39`: per-test stored results (SF3a), gates that fail only when findings rise (GL, K0), a structure ceiling that may only fall (GL.2), the skip-policy guard (K1a) and the per-ID comparator (K2/K3, Agent [#433](https://github.com/banodoco/astrid-agent/pull/433)). That branch was not merged whole, and the comparator stayed advisory until it passes once on an unchanged tree ([Release 14 ruling 10](../../releases/14/run.md)). This plan lands that net first, then fixes by cause. Measurements, alternatives and the split decision are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

1. **Measure and seal** (AG-0, AG-1, AG-2). Re-measure on the head of `release/<NN>/main` when the plan branch is cut; land the safety net; seal the ceiling; turn on the merge-tier required checks. From here the Agent cannot get worse, which protects every other plan in the same release.
2. **CI wiring** (AG-3, AG-4, AG-5). The inputs the tests ask for and CI never provides. About 320 unit IDs, and possibly the 249 integration refusals.
3. **Known behaviour changes** (AG-6, AG-7, AG-8). The copy-only upgrade boundary, the custody imports and the timeline fork binding schema, each with an existing Plan 39 row or packet.
4. **Review stop RS1.** Re-measure, cluster what is left, and re-estimate the long tail. If more than 60 distinct causes remain, the manager splits AG-9 into cards before going on.
5. **The long tail** (AG-9), one worker per cause, in parallel.
6. **Three green nights** (AG-10), then the final review R.

**Constraints:**
- CI time, not workers, sets the pace: unit shards take 27–96 minutes and integration shards 13–98, and jobs queue. Prove each card with its focused tests and the stored results, merge in batches, and run the full workflows once per batch ([Release 14 ruling 13](../../releases/14/run.md)).
- Other plans change the Agent in the same release (in Release 15: Plans 40, 69, 77, 78, 81). The ceiling from AG-1 is what stops them adding red while this plan burns it down, which is why it comes first.
- Recording this plan does not authorize implementation. Details are in [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:**
  - Agent `release/<NN>/main` at the head recorded in AG-0, and the Runtime, VibeComfy, RunPod lifecycle and ComfyUI pins that commit names;
  - the Agent commits on `release/14/plan-39` (`ab95803ce28fa51eec937b4074f5ec0f0439b98a`) that carry the safety net, picked by row, not merged whole;
  - Plan 39's sealed-ceiling format and `ci/required-checks.json` schema, so the two plans write one file.
- **Produces:**
  - green Agent workflows on `release/<NN>/main`, and on `main` once that release is published;
  - the Agent's sealed per-ID ceiling, falling to zero, and its entries in `ci/required-checks.json`;
  - the Agent merge-tier check list for the owner's branch protection;
  - per-cause fix PRs in astrid-agent, each linked from its task row.

## Completion

- Every workflow listed in [Outcome and scope](#outcome-and-scope) has a green run on the final head of `release/<NN>/main` on three consecutive nights, with any quarantine entries listed and within age, and the merge-tier required checks are on.
- The ceiling is empty, or holds only entries the owner accepted under D3, each with an issue, an owner and an expiry.
- **Negative cases:**
  - a pull request that turns one passing Agent test red fails the per-ID comparison;
  - an expired quarantine entry, or a strict xfail that starts passing, turns the Agent red;
  - a shard that is cancelled or truncated turns the run red rather than counting as passing.
- **Limits:** GitHub-hosted runners only. GPU, live and Pinokio lanes are out of scope. Branch protection is the owner's setting; the plan can only list and check it. `main` turns green when its release is published, because work lands through the release branch.
