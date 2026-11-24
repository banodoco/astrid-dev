# Release 15 — qualification bar

**Proposed by** the Release 15 Lead (`session_011EzfW1gtAhRQwk8pgJMzhG`) and **agreed with the owner on 24 November 2026.** Run by the Release 15 Qualifier (mailbox `r15-qualifier`, `session_011EzfW1Lc24EARJQsmbgNfo`) on [astrid-dev #1834](https://github.com/banodoco/astrid-dev/issues/1834). The [run board](run.md) holds the lanes and the freeze (about 26 November); this file holds what has to be true before the owner is asked to publish.

The Qualifier finds, measures, records and reports. **It never decides that a failure is acceptable:** acceptance is the Lead's recommendation and the owner's call. The owner reserves publishing, paid runs, her machine, install and media, and changes to existing test assertions.

## The bar

### Tier 1 — blocks shipping

1. **No new failures against Release 14.** Compare every test id on the frozen head in all three product repositories against Release 14's published heads, **whole run to whole run (never one shard against one shard)**, from full job logs (`gh api repos/<repo>/actions/jobs/<id>/logs`, never the 5,000-line tail). Each new failure gets a fix or the owner's explicit acceptance, written down.
2. **Each Release 15 promise works on a real installed build of the frozen candidate:**
   - **Heavy timeline:** open a 300-clip project, edit, save, reload byte-identical; twice.
   - **Render:** a long render (more than 5 minutes) and Plan 87's film-shaped render, with output that decodes and is correct.
   - **Generate:** one real `astrid generate` on a GPU (the owner's machine or RunPod), run only with her go and her budget.
   - **Update:** a real Release 14 install updated to the Release 15 candidate and then rolled back, with no project data lost.
3. **Nothing harmful:** no lost work, no broken install or update, no wrong output on a real path.
4. **The owner's go names exact SHAs** for every repository; she checks the result on her own long-lived install afterwards.

### Tier 2 — should pass, or ship with the owner's OK as a known issue

- App **Direct Journey** (`direct-journey.yml`), Agent **`journey.yml`** (the update matrix) and Agent **`windows-journey.yml`** are green on the candidate.
- A Windows tester session, if a tester is available.
- The speed targets are reported as **measured against target** (generate about 3 s; heavy save about 3 s). They do not block.

### Tier 3 — not a Release 15 bar

Fully green suites ([Plan 39](../../plans/39-green-mains/plan.md) and [Plan 91](../../plans/91-failures-caught-on-every-pull-request/plan.md), Release 16).

## Release 14 reference (what "new failure" is measured against)

Release 14's published heads are in [releases/14.md](../14.md#publication). The frozen head is compared with these, by test id, whole run:

| Repository | Release 14 head | Reference set | State |
| --- | --- | --- | --- |
| astrid-agent | `c0ad6b54aadd21630d98bb5039613e37efe92a8f` | [evidence/agent-ci-baseline-8807f820](evidence/agent-ci-baseline-8807f820/README.md) (run 45010433010) | exists |
| astrid-runtime | `5120462d67479dc4719406d0d34440edb616ace1` | `evidence/ci-baseline-r14/` (run 44996701468) | Phase 0b |
| astrid-app | `e0da794ac9d26a808ab4082b29f60408b66b3a4c` | `evidence/ci-baseline-r14/` (runs 45028860223 on `main`, 45023090092 on `release/14/main`; both green) | Phase 0b |
| VibeComfy | `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` | VibeComfy's hosted `ci` runs no unit tests ([#1768](https://github.com/banodoco/astrid-dev/issues/1768)); the Lead's local fast suite compared by id stands in (baseline `c0e910ca`: 758 passed, 9 failed, 9 skipped) | per Plan 56 ruling 7 |

Where a repository's test jobs cannot be compared test by test, the gap is stated here and the extraction script that closes it is under `scripts/` ([App](evidence/ci-baseline-r14/README.md)).

## Checklist

"Needs" says who or what must be available. A row is closed only by evidence in `evidence/qualification-<sha8>/` (Phase 1), where `<sha8>` is the first eight characters of the frozen Agent head.

| # | Item | Tier | How it is proved | Needs | Evidence file |
| --- | --- | --- | --- | --- | --- |
| 1a | Agent: no new failures vs Release 14 | 1 | `ci.yml` and `lanes.yml` whole-run, full logs, `env/baseline-diff.py --strict` against the Agent reference | Lead's Agent CI slot (max two at once across Releases 15 and 16) | `agent-ci-diff.md` |
| 1b | Runtime: no new failures vs Release 14 | 1 | `ci.yml` whole run, full logs, same tool | none (Runtime runs are reported to the Lead) | `runtime-ci-diff.md` |
| 1c | App: no new failures vs Release 14 | 1 | `test.yml` whole run; vitest per-file counts and failing ids by script | none | `app-ci-diff.md` |
| 1d | VibeComfy: no new failures vs Release 14 | 1 | Lead's local fast suite by id | Lead (suite) | `vibecomfy-diff.md` |
| 2a | Heavy timeline: 300 clips, edit, save, reload byte-identical, twice | 1 | `scripts/qualification/heavy_timeline.sh` on an installed stack, fixture from Plan 89 | an installed candidate on a Linux or macOS machine; Plan 89's 300-clip fixture | `heavy-timeline-run{1,2}/` |
| 2b | Render: more than 5 minutes, decodes, correct | 1 | long-render recipe from Plan 88's handover; `ffprobe` and a frame and audio check | installed candidate; Plan 87's core on `release/15/main`; a machine with ffmpeg | `render-long/` |
| 2c | Render: Plan 87's film-shaped render (621 clips by default) | 1 | `build-fixture.mjs --variant film-shaped`, then the render, output decoded and spot-checked | as 2b; the film-shaped fixture (astrid-app `scripts/save-loop/`) | `render-film/` |
| 2d | Generate: one real `astrid generate` on a GPU | 1 | the command and RunPod recipe in `scripts/qualification/generate_runpod.md`, teardown confirmed | **the owner's go and budget**; a RunPod key or her GPU | `generate/` |
| 2e | Update from a real Release 14 install to the candidate, then roll back, no project data lost | 1 | Release 14's journey scripts (`scripts/journey_*.py`) plus `scripts/qualification/update_rollback.sh`; realm-ID list before and after, project bytes hashed before and after | a Release 14 install (fresh container or VM); the candidate's installer | `update-rollback/` |
| 3 | Nothing harmful | 1 | read across 1 and 2: every failure and every anomaly in the logs gets a harm judgement (the Qualifier records evidence; the Lead and owner judge) | Lead | `verdict.md` |
| 4 | The owner's go names exact SHAs; her own long-lived install checked afterwards | 1 | `verdict.md` lists the four SHAs; the owner checks | the owner | `verdict.md` |
| T2a | App Direct Journey green on the candidate | 2 | `direct-journey.yml` by `workflow_dispatch` on the candidate head | none (told to the Lead) | `tier2.md` |
| T2b | Agent `journey.yml` (update matrix) green | 2 | `workflow_dispatch` with `branch` set to the release branch | Lead's Agent CI slot | `tier2.md` |
| T2c | Agent `windows-journey.yml` green | 2 | runs on every push to `release/*/main`; read the run on the candidate | none | `tier2.md` |
| T2d | Windows tester session | 2 | a tester runs update, generate, edit, save, reopen on a real Windows install | a tester (owner) | `tier2.md` |
| T2e | Speed targets reported as measured against target | 2 | generate about 3 s; heavy save about 3 s; installed measurement on the exact head | installed candidate | `speed.md` |

## Phase 0 (until the freeze, about 26 November)

- **a.** This file, by astrid-dev pull request, merged by the Lead.
- **b.** Release 14 reference sets for the Runtime and the App, committed beside the Agent's.
- **c.** Tier 2 workflows that do not trigger on release branches (App `direct-journey.yml`, Agent `journey.yml`) dispatched on today's `release/15/main` heads, so failures surface early.
- **d.** Tier 1 installed journeys scripted so each reruns with one command, and dry-run on `release/15/main`.
- **e.** Each journey re-run when a plan lands in `release/15/main`; one line to `r15-release-lead` on #1834 (pass, fail, or the new failure ids). A new failure in a landed plan's code also goes straight to that plan's orchestrator.

## Phase 1 (on the frozen candidate)

Everything above is run on the frozen heads; timing-sensitive Tier 1 journeys run twice. The Qualifier writes `releases/15/evidence/qualification-<sha8>/` with a result for each row, and gives the Lead a one-page verdict: what passed, each new failure with evidence of harm or of no harm, and what needs the owner.

## Rules the Qualifier works under

- It does not push to or merge into `release/15/main` or any plan branch, does not cancel any `release/*/main` run, does not publish and does not spend. Fixes it commissions go through `p15q/<packet>` → `release/15/q-<topic>` → `release/15/main`, the last step through the Lead's gate.
- A failure in a plan's own code goes to that plan's orchestrator, not to a packet.
- Packets (issue packets in [packets/](packets/), sessions `r15-Q-NN-<n>`) cover only failures with a failing test id or an exact repro that a sandbox with no network can target, a fix of about three hours or less, one contract and no owning lane. Anything that needs an installed build, a GPU, a render, a real timing or hosted CI to reproduce stays with the Qualifier.
- Every comparison uses whole runs and full job logs. A missing id counts as red until explained.
