# Agent main green

**Project:** Agent main green

**Goal:** Every CI workflow on astrid-agent `main` is green and stays green, so a red Agent check means a new regression, and anyone changing the Agent knows within one run whether they broke something.

**Status:** active

**Owner:** Orchestrator session `session_011EzfW1yUojAfWkGcaZNRph` (`r15-p91-orchestrator`), with one manager for its packets

**Estimate:** 55–72 (about 4–5 weeks elapsed with five workers): Phase 1 (the gate, the prune pass and the large causes) 23–27, Phase 2 (the middle) 17–22, Phase 3 (the long tail) 12–20, Phase 4 (green runs and review) 3–5

**Waiting on:** AG-1 (the gate) and the first packets; the Release 16 Lead's gate for landing in `release/16/main`, which is not yet cut (until then the plan branch merges `release/15/main` forward)

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). A red check on Agent `main` should mean a new regression. Today it means nothing: the CI and Lanes workflows have been red on every push to `main` since at least Release 12.

## Outcome and scope

The Agent's share of [Plan 39](../39-green-mains/plan.md), split off as its own project on 23 November 2026 so that one repository can reach green without waiting on the other two ([why](inputs.md#planning-evidence)). Plan 39 keeps the Runtime, the App and the shared cross-repository pieces.

Every Agent workflow is green on `release/16/main`, and on `main` once Release 16 is published, and it stays green (the owner moved the plan to Release 16 on 24 November 2026; until `release/16/main` is cut, the plan branch builds on `release/15/main` and merges it forward):
- **Cannot get worse, first.** Before any fix lands, the Agent's current failing tests are sealed as a ceiling that may only fall, keyed by job and test ID, the integration and opt-in lanes included. Every batch the plan merges, and every completed `release/15/main` run, is compared with it. New, lost or reintroduced red fails the comparison.
- **Prune boldly, then fix.** With no users yet, only current behaviour, and updating from the previous published release, is supported. A test of anything older, or one another passing test already covers, is deleted with its citation rather than repaired (D5). A test of something users do today is never deleted for being hard to fix.
- **Green by cause.** Each remaining failing test is fixed at its root cause, under one set of [triage rules](tasks.md#triage-rules): name the kind (env, stale test, retired, redundant, product bug, flaky, unknown), fix it the way that kind allows, prove it by ID on hosted CI. Never a loosened assertion, a stub input, a widened deadline, a skip or a growing baseline. Plan 39's anti-hiding rules ([inputs](../39-green-mains/evidence/release-14-record/inputs.md#where-changing-a-test-would-hide-a-bug)) apply unchanged.
- **Kept green.** The owner turns on the Agent's required checks: on pull requests, the jobs that run there; for the release, the full comparison. The quarantine rule (strict xfail with an issue, an owner and an expiry, at most ten; Plan 39's D3 and D9) is the only way a known failure may be tolerated. Product bugs too large for this plan stay visibly red on the ceiling, each with an issue and the owner's acceptance (D6).

**Measured on `release/15/main` at `b324d7c1`**, the latest head with a complete CI and Lanes run (23 November 2026; [evidence](evidence/README.md)):

| Workflow | State | Failing (distinct job and test ID) |
| --- | --- | --- |
| `Chat service`, `Windows task host journey`, `Windows runtime retention` | green | — |
| `CI` | red | All eight `unit` shards and `darwin native`: 1,087, in 274 files, of about 33,000 tests. `fast checks`, `boundary`, `windows-native-and-installer` and both release wheels are green. |
| `Lanes` | red | The four `integration` shards and `opt-in`: 787, in 129 files. `installed wheel` is green. |

The triage puts the 1,874 in about 150 distinct causes ([how](inputs.md#planning-evidence)). About 20% point at removed, retired, moved or legacy code, and a prune pass (AG-P1, AG-P2) sorts those before anything is fixed. Nine Wave A cards hold about 960 IDs; 19 Wave B cards hold about 400; Wave C holds the rest, 393 in 232 files.

**Included:** the Agent workflows on push to `main` and to `release/16/main`:
- `CI`: `fast checks`, the eight `unit` shards and the aggregate `unit`, `darwin native`, `windows-native-and-installer`, `release wheel` (3.11, 3.12), `boundary`;
- `Lanes`: `integration` 1–4, `opt-in`, `installed wheel`;
- `Chat service`, `Windows task host journey` and `Windows runtime retention`, which are green and must stay green.

It also includes:
- the comparison and the hosted card runs that make the gate work (AG-1);
- the Agent rows of Plan 39's [Release 15 ceiling](../39-green-mains/evidence/release-14-record/tasks.md#release-15-ceiling);
- the worker environment's Runtime install, so workers can reproduce what CI runs;
- the small product fixes the triage finds, where each takes a day or less.

**Not included:**
- the Runtime and the App, which stay in Plan 39. The Runtime changes this plan may need (the frame-rate schema under D8, and refusals raised in the Runtime) go as Runtime pull requests named on their card;
- the cross-repository pieces that stay in Plan 39: the nightly report (`scripts/ci_red_report.py`), the release rule in Plan 31's `release-contract` (K4, K5) and the release-record sections;
- porting Plan 39's K2/K3 comparator, which never passed on an unchanged tree. AG-1 reuses `env/baseline-diff.py` instead;
- the behaviour of the custody and host-spawn tests [Plan 38](../38-one-process-identity/plan.md) owns. AG-A1 makes them run, and their residual failures follow [D3](inputs.md#owner-decisions);
- the Agent's `journey.yml` release receipts, GPU and live lanes ([Plan 34](../34-real-gpu-proof/plan.md));
- product bugs that take more than a day, which go to issues under D6, and product features.

## Existing work and decision

The approach and the anti-hiding rules come from Plan 39, which was reviewed on 9 November and ran in Release 14. Release 15 already compares each lane's unit results with a [hosted baseline](../../releases/15/evidence/agent-ci-baseline-8807f820/README.md), by hand, and names the groups that move between runs. This plan builds on both:
- it extends that baseline to the integration and opt-in lanes;
- it makes the comparison a check, using the existing `env/baseline-diff.py`;
- it adds hosted card runs, so a card proves itself in minutes;
- it burns the baseline down by cause, with the long tail carded from the evidence by script.

The measurement, the triage, the alternatives and the independent critique are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Four phases; Phase 1 carries most of the value. Up to **five worker sessions run at once**, kept full from one [dispatch queue](tasks.md#dispatch-order).

1. **The gate, the prune pass and the large causes** (AG-0 to AG-2, AG-P1, Wave A, RS1).
   - AG-0 cuts the plan branch, re-measures, and finds what cancels runs on `release/15/main`.
   - AG-1 adds the hosted card runs and the comparison.
   - AG-P1 (CI) and AG-P2 (Lanes) sort the 370 prune candidates into retire, redundant or keep, and delete the first two with citations, so no card fixes a test that should go.
   - Nine cards fix the causes that hold about 960 IDs. They start the moment the branch is cut, beside the gate, and land once it works.
   - RS1 reviews the gate, the clip-data decision (D13) and the frame-rate contract (D8), then regenerates Wave C and re-estimates.
2. **The middle** (Wave B): 19 cards, one per cause, each with a kind, scope and proof.
3. **The long tail** (Wave C): one card per test file, generated from the evidence by `make_wave_c.py` and regenerated at RS1, batched by area.
4. **Green and kept green** (AG-10, R): three green dispatched runs on one frozen plan head on three nights, one on `release/16/main` after landing, then at most two review rounds.

**Constraints:**
- **Proof needs hosted CI.** A pull request into a `release/*/main` branch runs only fast checks, unit shard 1 and boundary; pushes to plan branches start nothing; Lanes has no pull-request trigger; and the worker environment differs from CI (Python 3.13, shallow fetches, no Node, Remotion, Pinokio or ComfyUI). So env cards prove on hosted card runs, and the gate runs on the manager's dispatched batch runs ([How work is proved](tasks.md#how-work-is-proved)).
- **CI time sets the pace,** not workers: a full run takes up to about 2.5 hours. The manager merges up to five cards per batch.
- **Most `release/15/main` heads have no complete run:** 21 of the last 28 CI and Lanes runs there were cancelled after starting. The workflows don't cancel runs on that branch, so something else does. AG-0 finds out, and AG-10 doesn't depend on that branch's push runs.
- **Overlapping plans.** Plan 77 edits failing test files, the Runtime pins and `ci.yml`; Plan 88 edits two failing test files. Those cards follow the [base choice](inputs.md#source-identities). The frame-rate schema is vendored from the Runtime, so D8's schema option needs a Runtime PR and a pin bump after Plan 77's.
- Recording this plan does not authorize implementation. Details are in [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:**
  - Agent `release/15/main` at the head AG-0 records, and the Runtime, VibeComfy, RunPod lifecycle and ComfyUI pins that commit names;
  - the Release 15 hosted baseline (`releases/15/evidence/agent-ci-baseline-8807f820/`) and its rule for groups that move between runs;
  - astrid-dev `env/baseline-diff.py` and the [shared worker environment](../../env/README.md), through astrid-agent's copies in `scripts/worker-env/`;
  - for reference only, `release/14/plan-39` at `2ef74155a1a984101408b19b4e1e4fd274f3178e` (its head on 24 November), where Release 14's gate work lives.
- **Produces:**
  - green Agent workflows on `release/16/main`, and on `main` once Release 16 is published;
  - `ci/agent-ceiling.tsv` in astrid-agent, keyed by job and test ID and falling to empty, and the comparison that enforces it;
  - `workflow_dispatch` inputs (`tests`, `repeat`) on `ci.yml` and `lanes.yml`, which any plan can use to prove a change on hosted runners in minutes;
  - astrid-dev `ci/required-checks.json`, with the Agent's entries, in a schema Plan 39 can extend;
  - a re-runnable measurement (`evidence/cluster_failures.py`, `evidence/make_wave_c.py`) that turns a run's logs into causes and cards;
  - per-cause fix PRs in astrid-agent, each linked from its task row; issues for the product bugs left on the ceiling.

## Completion

- Every workflow listed in [Outcome and scope](#outcome-and-scope) is green in three full runs on one frozen head of `release/16/plan-91`, on three different nights, and in one run on `release/16/main` after the plan branch lands. Any quarantine entries are listed and within age, and the required checks are on.
- The ceiling is empty, or holds only entries the owner accepted under D3 and D6, each with an issue and an owner.
- **Negative cases:**
  - a batch that turns one passing Agent test red, in any job, fails the comparison;
  - a batch that loses a test ID fails it;
  - an expired quarantine entry, or a strict xfail that starts passing, turns the Agent red;
  - a shard that is cancelled or truncated fails the comparison rather than counting as passing.
- **Limits:**
  - GitHub-hosted runners only; GPU, live and Pinokio-machine lanes are out of scope;
  - jobs that don't run on pull requests can only be required at the release tier;
  - branch protection is the owner's setting, and the plan can only list and check it;
  - `main` turns green when Release 16 is published, because work lands through the release branch.
