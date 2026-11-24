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

Fully green suites ([Plan 39](../../plans/39-green-mains/plan.md) and [Plan 91](../../plans/91-agent-main-green/plan.md), Release 16).

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

| # | Item | Tier | How it is proved | Needs | Evidence file | Covered by | Gap | Work |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1a | Agent: no new failures vs Release 14 | 1 | `ci.yml` and `lanes.yml` whole-run, full logs, `env/baseline-diff.py --strict` against the Agent reference | Lead's Agent CI slot (max two at once across Releases 15 and 16) | `agent-ci-diff.md` | [Plan 88 gate `551c190e`](evidence/agent-plan-88-gate-551c190e/README.md) and [Plan 89 gate `d10817a7`](evidence/agent-plan-89-gate-d10817a7/RESULT.md): whole-run by id, but against `release/15/main`, not Release 14. Plan 56, 82, 87: per-PR proofs only. | No whole-run comparison against the Release 14 baseline on the frozen head; Plan 56 head still has 2 new failures (A#599). | **re-run** `baseline-diff.py --strict` on the frozen head |
| 1b | Runtime: no new failures vs Release 14 | 1 | `ci.yml` whole run, full logs, same tool | none (Runtime runs are reported to the Lead) | `runtime-ci-diff.md` | [Runtime #109 gate `bda91409`](evidence/runtime-109-gate-bda91409/README.md) (Plan 77 save). | No gate record for Runtime #108, #113, #115, #118 or Plan 87's Runtime changes; nothing against [the Release 14 set](evidence/ci-baseline-r14/README.md). | **re-run** on the frozen head |
| 1c | App: no new failures vs Release 14 | 1 | `test.yml` whole run; vitest per-file counts and failing ids by script | none | `app-ci-diff.md` | none; Plan 77 and 89 App PRs ran hosted `test.yml` green. | No test-id comparison is possible from the log; [per-file extractor](evidence/ci-baseline-r14/README.md) built. | **new**, tool built; run at freeze |
| 1d | VibeComfy: no new failures vs Release 14 | 1 | Lead's local fast suite by id | Lead (suite) | `vibecomfy-diff.md` | Lead's local fast suite (baseline `c0e910ca`); Plan 56 per-PR local proofs. | No frozen-head VibeComfy comparison. | **re-run** (Lead's suite) |
| 2a | Heavy timeline: 300 clips, edit, save, reload byte-identical, twice | 1 | `scripts/qualification/heavy_timeline.sh` on an installed stack, fixture from Plan 89 | an installed candidate on a Linux or macOS machine; Plan 89's 300-clip fixture | `heavy-timeline-run{1,2}/` | Plan 89 [SV-L2 installed marks](../../plans/89-heavy-saves-in-seconds/handover.md) (PR #1685): gesture-to-Saved warm median **6.15 s**, 19 drags, one repetition, on a restored 300-clip archive; Plan 77 save profiles; save-loop sweep (`scripts/save-loop`) compares the Runtime `content_digest` after reload. | No frozen integrated build; no two-run reload comparison; **no 300-clip generator in any repository** (the archive lives on one container); the standard builder fails its size gate (575,879 of 2,600,000 bytes, run on `d53685f3`); Plan 89's save work is not on `release/15/main`. | **re-run** Plan 89's method on the candidate + **new** 300-clip generator (packet R15-Q-02 once its shape is settled) |
| 2b | Render: more than 5 minutes, decodes, correct | 1 | long-render recipe from Plan 88's handover; `ffprobe` and a frame and audio check | installed candidate; Plan 87's core on `release/15/main`; a machine with ffmpeg | `render-long/` | Plan 87 RN-15 (`4d0abe71`, claimed: 5 of 5 and 2 of 2 renders of 5 to 7 minutes succeed after the fix; 8 of 10 failed before); raw results not in the repository. | Not on `release/15/main`; no output decode recorded; no render longer than 20 minutes; a 5,897-frame render failed at about 20 min with an uncaptured child process (cause undetermined). | **re-run** Plan 87's acceptance on the candidate; [`render_verify.py`](../../scripts/qualification/README.md) wraps the decode check |
| 2c | Render: Plan 87's film-shaped render (621 clips by default) | 1 | `build-fixture.mjs --variant film-shaped`, then the render, output decoded and spot-checked | as 2b; the film-shaped fixture (astrid-app `scripts/save-loop/`) | `render-film/` | Plan 87 RN-6 (small command renders only); Plan 88 film-shaped builder (App `release/15/plan-88`, `0c6bda563`, 621 clips). | RN-10, RN-12 and RN-13 open; builder not on `release/15/main`; no film-shaped render on any build; Plan 88 has zero render proof. | **re-run** RN-12/13 when Plan 87 lands |
| 2d | Generate: one real `astrid generate` on a GPU | 1 | the command and RunPod recipe in `scripts/qualification/generate_runpod.md`, teardown confirmed | **the owner's go and budget**; a RunPod key or her GPU | `generate/` | none (Plan 56's WS-L is the analogue: not started; Plan 82 measured `generate image` at a median 5.36 s on a build that predates its code). | Needs the owner's go and budget; CPU stand-ins only so far. | **new**, prepared ([recipe](../../scripts/qualification/generate_runpod.md)); owner |
| 2e | Update from a real Release 14 install to the candidate, then roll back, no project data lost | 1 | Release 14's journey scripts (`scripts/journey_*.py`) plus `scripts/qualification/update_rollback.sh`; realm-ID list before and after, project bytes hashed before and after | a Release 14 install (fresh container or VM); the candidate's installer | `update-rollback/` | Plan 89 P89-06 / Agent #609 rollback hook: fake-backend tests only; the lane's run against Runtimes `789d3e2c` and `5120462d` has no evidence in the repository. `journey.yml` update rows use a synthetic "release+1" stand-in. | No real Release 14 to candidate update, no forced rollback on real SHAs, no data check; `journey.yml` cannot go green on `release/15/main` (verifier requires a name the installer no longer produces; Release 14's `fix17-r13-update-matrix` harness never merged); #609 is not on `release/15/main`. | **new**: leg on `release/15/q-update-rollback` (built, unproven) + verifier fix; reuse Plan 89's #609 proof |
| 3 | Nothing harmful | 1 | read across 1 and 2: every failure and every anomaly in the logs gets a harm judgement (the Qualifier records evidence; the Lead and owner judge) | Lead | `verdict.md` | Plan 87 and 88 anomaly notes (below). | Judgement across all rows; unexplained: Plan 87 20-minute failure; Plan 88 edit drift up to 0.000333667 s; RN-14 (motion pack on a fresh install) moved to Release 16. | **new** (judgement; mine) |
| 4 | The owner's go names exact SHAs; her own long-lived install checked afterwards | 1 | `verdict.md` lists the four SHAs; the owner checks | the owner | `verdict.md` | none. | The owner's go and her own install. | **N/A** to the Qualifier (owner) |
| 5 | Agent timeline writes open in the editor | 1 | run each Agent timeline-writing command (occurrence create, move, trim, transcripts refresh, word anchors, media add, others in `astrid/packs/timeline` and `astrid/sdk/timeline`) on a fixture and pass every saved bundle through the App's real `parseTimelineBundle` and timeline loader, offline | the Agent and App checkouts; no network | `agent-writes-open/` | Plan 88 PR #624 adds a transcript-references check on the Agent side; its PR body says "Not verified: a real editor open of an Agent-written project"; no other plan covers it. | Nothing runs the Agent's writes through the App's `parseTimelineBundle` and loader; twice on 24 November the Agent wrote data the editor rejects (transcript references, #1849; fractional `start_ms`, #1776). | **new**: packet R15-Q-01 ([brief](packets/R15-Q-01.md)) |
| T2a | App Direct Journey green on the candidate | 2 | `direct-journey.yml` by `workflow_dispatch` on the candidate head | none (told to the Lead) | `tier2.md` | App `direct-journey.yml` green on `d53685f3` (run 45387669347). | Re-run on the frozen candidate. | **re-run** |
| T2b | Agent `journey.yml` (update matrix) green | 2 | `workflow_dispatch` with `branch` set to the release branch | Lead's Agent CI slot | `tier2.md` | none: run 45397909312 failed on `release/15/main`. | Harness verifier defect (see 2e); R0-handoff rows unclassified. | **new** (harness fix) then **re-run** |
| T2c | Agent `windows-journey.yml` green | 2 | runs on every push to `release/*/main`; read the run on the candidate | none | `tier2.md` | Agent `windows-journey.yml` green on `514499de` (run 45351510737). | Re-read on the frozen candidate. | **re-run** |
| T2d | Windows tester session | 2 | a tester runs update, generate, edit, save, reopen on a real Windows install | a tester (owner) | `tier2.md` | none. | A tester, if available. | **N/A** to the Qualifier (owner) |
| T2e | Speed targets reported as measured against target | 2 | generate about 3 s; heavy save about 3 s; installed measurement on the exact head | installed candidate | `speed.md` | Plan 89 6.15 s (heavy save) and Plan 82's estimate 2.8 to 3.4 s (generate, *estimated*, measured 5.36 s on a build without its caches). | Nothing measured against target on a candidate with the plans' changes; save number must use Plan 89's method (SV-L2 marks). | **re-run** the plans' methods on the candidate |

## Backlog: the new work, in order (user harm first, then freeze risk)

Every "re-run" row is the plan's own tool run by the Qualifier on the frozen, integrated candidate (r15-lead-qual-0005); nothing is written for it. Only "new" rows are built. Updated 24 November 2026 from the coverage map above.

| # | Row | New work | Why this order | Who | State |
| --- | --- | --- | --- | --- | --- |
| N1 | 5 | Contract harness: every Agent timeline write, through the App parser and loader, offline | an unopenable project is lost work for the user, and it has happened twice in one day | ChatGPT packets [R15-Q-01](packets/R15-Q-01.md) (the parser) and [R15-Q-03](packets/R15-Q-03.md) (every `_ms` field a whole number; Plan 87 fixed one instance on `release/15/plan-87`) | packet written |
| N2 | 2e, T2b | Real Release 14 install, update to the candidate, forced rollback, five steps, data fingerprint; plus the harness verifier fix that stops `journey.yml` failing on every candidate | a failed update or rollback can lose a project; deadline 26 Nov 12:00 UTC | Qualifier (hosted runs) with Sonnet helpers; branch `release/15/q-update-rollback` | built, unproven; verifier fix in progress |
| N3 | 2a | A 300-clip fixture generator in a repository (the archive lives on one container), and the two-run reload comparison, using Plan 89's SV-L2 method for the save number | the heavy timeline is the release's headline; the only fixture can disappear | Qualifier; generator as packet R15-Q-02 once Plan 89 confirms the shape | open |
| N4 | 3 | Harm judgements for the open anomalies: Plan 87's 20-minute failure with an uncaptured child process; Plan 88's drift of up to 0.000333667 s on a 250-clip edit; RN-14 moved to Release 16 (no motion pack on a fresh install) | wrong output on a real path blocks shipping | Qualifier, with the Lead | open |
| N8 | 2a, 2e, 3 | Add a **Runtime restart on the heavy project** to the heavy-timeline and update journeys: Plan 87 found that after the 616-clip build the Runtime refuses to start at the default admission budget (about 1.8 s; with 900 s the start blocks about 439 s), which would fail the Release 14 to Release 15 update and any rollback on a heavy project | a project that cannot start after an update or restart is lost work for the user; routed by the Lead to Plan 89 (#1777, SV-L9a) | Qualifier (installed); verdict item | open: Plan 89 to confirm on its Runtime |
| N5 | 2b, 2c | Nothing new to write: re-run Plan 87's RN-15, RN-10, RN-12, RN-13 acceptance when Plan 87 lands, then [`render_verify.py`](../../scripts/qualification/README.md) on each output | long renders were failing; Plan 87 is the long pole | Qualifier | waits for Plan 87 |
| N6 | 1a to 1d | Whole-run comparisons at the freeze with the references in [ci-baseline-r14](evidence/ci-baseline-r14/README.md) | a new failure is a Tier 1 block | Qualifier | at the freeze |
| N7 | 2d, T2e | The owner's go for one real generate; speed numbers by Plan 82's and Plan 89's methods | needs the owner | owner and Qualifier | prepared |

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
