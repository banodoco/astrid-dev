# Inputs — Agent main green

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah asked on 23 November 2026, in session https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV, for a project focused only on getting the Agent to green, broken off from Plan 39 (All three mains green). On 24 November, in the same session, Hannah asked for it to be:
- built on `release/15/main`;
- given a strategy for the long tail that holds up;
- aligned with the planning skill's routes;
- run with up to five workers at a time;
- made ready to run, then pushed to astrid-dev;
- cleaned aggressively: "we can probably aggressively clean tbh … theres likely a lot of cruft … be thoughtful but bold", with no users yet ("we have no users rn").

The end state is Plan 39's, for one repository: every Agent workflow green and kept green. Where it lands and when it starts are D1 and the owner's go.

**Prior art:**
- [Plan 39](../39-green-mains/plan.md), its [triage](../39-green-mains/inputs.md#agent-ci-lanes-windows-task-host-journey), its [handover](../39-green-mains/handover.md) and its [Release 15 ceiling](../39-green-mains/tasks.md#release-15-ceiling). Each Agent row's cause and kind were traced from Plan 39's tasks, evidence and the Release 14 packets; the map is in [tasks](tasks.md#taken-from-plan-39).
- The [Release 14 run board](../../releases/14/run.md): rulings 6a, 10 and 13. K2/K3 never passed on an unchanged tree (ruling 10). `release/14/plan-39` (head `2ef74155` on 24 November) was not merged. The [Release 14 brief](../../releases/14.md): Release 14 published on "no new red against Release 13", and its committed inherited-red list (`releases/14/evidence/inherited-red.json`) is empty.
- The [Release 15 hosted baseline](../../releases/15/evidence/agent-ci-baseline-8807f820/README.md): the unit and macOS failing IDs at `8807f820`, compared by hand with every Release 15 lane, and the groups that move between runs of unchanged code. It does not cover the integration or opt-in lanes, so their failures are compared with nothing: 36 integration IDs are new on `release/15/main` since Release 14.
- **The workflows as they are** (`release/15/main` at `a09ea669`):
  - **CI on a pull request** runs only fast checks, unit shard 1 and boundary (`ci.yml:9-13`, `:248`).
  - **Lanes** has no pull-request trigger (`lanes.yml:6-16`), and pushes to plan branches start nothing.
  - **The unit shards** install the Runtime non-editable through `scripts/ci_install_runtime.py` (`ci.yml:341-342`); `darwin native` installs it editable from its checkout (`:473-474`).
  - **The timeline config schema** is vendored from the Runtime and checked by `boundary` (`runtime.lock.json:3-5`, `ci.yml:594-622`).
  - **`env/baseline-diff.py`** already sorts `-rA` logs into regression, preexisting, fixed and missing.
- **This plan's measurement** ([evidence](evidence/README.md)):
  - **Runs read:** the full logs of [CI 45183456598](https://github.com/banodoco/astrid-agent/actions/runs/45183456598) and [Lanes 45183456544](https://github.com/banodoco/astrid-agent/actions/runs/45183456544) at `b324d7c1`, the latest `release/15/main` head with both runs complete. For comparison, Agent `main` at `c0ad6b54` ([CI 45028846987](https://github.com/banodoco/astrid-agent/actions/runs/45028846987), [Lanes 45028847122](https://github.com/banodoco/astrid-agent/actions/runs/45028847122)).
  - **Grouping:** `evidence/cluster_failures.py` groups every failing ID by the frame that raised it. CI has 1,087 distinct (job, id) pairs in 437 clusters, and Lanes has 787 in 104. 1,070 of the CI IDs fail on both branches.
- **The triage:** seven read-only agents (Claude Haiku), one per batch of clusters, each read the traceback, the test and the code, and gave a kind, a cause, a size and the clusters that share it:
  - **The largest integration refusal** (282 IDs) is the commit-time reader check added in `86031e92` ("Check every timeline commit with the readers' eyes", 17 November). It is tripped by fixtures that leave out `output.resolution` and by clip-level namespaced data. Verified here: `86031e92` is in both branches, and `tests/editing_conformance/test_occurrence_hold_current_runtime.py:166` writes a clip-level `opaque`.
  - **The next 90 integration IDs** are the same check refusing a rational `fps` (`{numerator, denominator}`). The commit bundle allows it; the vendored config schema doesn't.
  - **The middle clusters** (about 230 IDs in 68 clusters) hold about 40 distinct causes. Over everything triaged, the kinds were about: env 30%, stale test 25%, unknown 30%, product bug 10%, retired 5%.
  - **One-test clusters:** in a random sample of 40 of the 343, 22% were a known cause, 58% shared a cause with others in their file, and 20% were unique. By extrapolation those 343 hold about 80–110 causes, mostly under half a day each.
  - In all, about **150 distinct causes**, not the 30 the first estimate assumed.
- **Negative findings:**
  - `git log -S` and per-file history mostly return three squash merges (`fb730f78`, `998ca937`, `6564b580`), each touching about 4,000 files. So a stale-test card quotes a stated source instead ([rule 3](tasks.md#triage-rules)).
  - 21 of the last 28 CI and Lanes runs on `release/15/main` were cancelled after starting, though the workflows don't cancel runs on that branch. The cause is not yet known (AG-0).
  - The worker environment can't reproduce the env causes: Python 3.13, shallow fetches, and none of Node, Remotion, Pinokio or ComfyUI.

**Approach:** Plan 39's approach, for one repository, with the triage made explicit and the gate built on what exists:
- Seal what is red, keyed by job and test ID.
- Compare every merged batch with it, using `env/baseline-diff.py` and hosted card runs.
- Fix by cause under one set of rules, and keep it green.
- Phase it so the first one and a half weeks carry most of the value: the gate, and the ten cards that hold about 1,000 IDs.
- Generate the long tail's cards from the evidence, so a re-measure re-cards it without hand work.

Splitting it off from Plan 39 lets the Agent reach green without the Runtime's and the App's work. It also gives the Agent one manager, which Plan 39's handover found Release 14 lacked.

Rejected:
- **Leaving the Agent in Plan 39.** That plan is in no Release 15 lane and has no owner.
- **Porting Release 14's K2/K3 comparator.** It never passed on an unchanged tree, and the existing diff script does the job.
- **A gate on pull requests only.** Pull requests don't run the jobs that fail.
- **A "known failures" baseline that never falls.** It keeps red as normal.
- **Quarantining the long tail.** The cap is ten (Plan 39's D9), and the tail is hundreds.
- **One card per test ID, or per cluster.** Most one-test clusters share a cause with their neighbours, so cards go per file, batched by area.
- **Landing outside a release.** Product work lands through `release/15/main` ([project format](../../docs/project-format.md)).

**Challenge:** Reviewed — an independent critique by a fresh high-judgment agent with no stake in the draft, and two ambiguity passes, all on 24 November 2026 in session https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV, checking claims against `release/15/main` at `a09ea669`. Five must-fix findings changed the gate, the cancellation diagnosis, the frame-rate contract, the reader-check card and the safety-net source. The findings and what changed are in [critique.md](evidence/critique.md).

**Proof and limits:**
- **Proof:** each workflow named in [plan.md](plan.md#outcome-and-scope) is green in three dispatched full runs on one frozen plan head on three nights, and once on `release/15/main` after landing. The comparison fails a batch that adds one red test or loses one ID. The quarantine guard fails on an expired entry or a strict xfail that passes.
- **Limits:**
  - one run per workflow, so a difference of a few IDs can't be told from flakiness. AG-0 re-measures on the head it cuts from;
  - the kinds and causes are an agent triage from logs and code, without running tests. Rule 1 (reproduce first) and rule 2 (name the kind with evidence) confirm each one on the card;
  - the Wave C estimate rests on a 40-test sample (about ±20%), and RS1 re-estimates it;
  - GitHub-hosted runners only; branch protection is the owner's setting.

**Review rounds:** RS1, at most 1 round, on the gate (AG-1), the clip-data decision (AG-A8) and the frame-rate contract (AG-A9). Every later card relies on these: a late finding in the gate would mean re-proving every landed card, and one in either contract would mean redoing the fixtures. Final R, at most 2 rounds. Both are done by the high-judgment review role. The owner confirms.

**Run start:** 24 November 2026. Authorized by Hannah in this run's launch message, in session https://claude.ai/code/session_011EzfW1yUojAfWkGcaZNRph, which confirms D1 and D3–D15 as recommended (D12 was already decided). The run covers every task in [tasks.md](tasks.md): AG-0 to AG-2, AG-P1, AG-P2, Wave A, RS1, Wave B, Wave C, AG-10 and R.
- **Accountable agent:** that session, the Plan 91 orchestrator (mailbox name `r15-p91-orchestrator`), reporting to the Release 15 Lead (`r15-release-lead`, `session_011EzfW1gtAhRQwk8pgJMzhG`). It works as the [Plans 87 and 89 dispatch](../../releases/15/run.md#plans-87-and-89-dispatch) section of the run board describes: it writes the packets (`releases/15/packets/R15-P91-<nn>.md`), reviews them, merges them, and runs every proof that needs `github.com` or hosted CI. A Plan 91 manager starts one fresh ChatGPT session per packet. There is no separate plan manager.
- **In the orchestrator's own lane:** AG-0, AG-1 (the gate, the `workflow_dispatch` inputs and the comparison), AG-2, every hosted card run and batch run, the ceiling ratchet, RS1, R and AG-10. Packet sandboxes cannot reach `github.com`, so packets post `READY-PROOF` and the orchestrator runs the proof.
- **Cap:** five packets in Running or Review at once (the owner's choice for this plan). Agent CI is release-wide: at most two Agent CI runs at once across all lanes, so the orchestrator checks the running `ci.yml` and `lanes.yml` runs before dispatching and names the slot in its hourly report.
- **The orchestrator may, without asking:** merge accepted packet PRs into `release/15/plan-91`; merge `release/15/main` into it; edit this plan's records; dispatch hosted runs on the plan branch; ratchet the ceiling down.
- **The owner's go is needed for:** changing an existing assertion beyond what the [triage rules](tasks.md#triage-rules) allow; any Runtime PR or release (D8); accepting a D6 ceiling entry (and a D3 one, as D3 says); quarantine entries beyond Plan 39's D9 cap; turning on the required checks. Landing into `release/15/main` needs the Release 15 Lead's written gate confirmation.
- **Mailbox:** [astrid-dev #1826](https://github.com/banodoco/astrid-dev/issues/1826), run `r15-p91-dispatch`.
- **Reports:** hourly on the Plan 91 mailbox: done, in progress, IDs cleared from the ceiling, decisions taken, the CI slot in use, and the one thing the orchestrator is least sure of.

## Owner decisions

On 24 November 2026, in this plan's session, Hannah answered D12 and agreed in conversation with the other recommendations below. On the same day, in the run's launch message (session https://claude.ai/code/session_011EzfW1yUojAfWkGcaZNRph), she confirmed D1 and D3–D15 as recommended, so every row below is decided. D2 and D12 were decided earlier.

| # | Decision | Recommendation |
| --- | --- | --- |
| D1 | Which release the plan lands in | **Decided (Hannah, 24 November 2026, launch message):** as recommended. Release 15, as its own lane: one manager and five worker slots. Phase 1 lands in `release/15/main` after RS1, so Release 15 publishes with the gate and the large causes even if Phases 2 and 3 run on. |
| D2 | Whether Plan 39 is narrowed to the Runtime and the App | **Decided (Hannah, 23 November 2026, this plan's session):** yes. The Agent rows of Plan 39 move here; Plan 39 keeps the Runtime, the App and the cross-repository pieces. |
| D3 | The custody and host-spawn tests Plan 38 owns | **Decided (Hannah, 24 November 2026, launch message):** as recommended. AG-A1 makes them run. Any that still fail stay on the ceiling with Plan 38 as owner, outside Plan 39's D9 cap of ten, because Plan 38 is unowned and in the draft Release 16. The owner accepts each entry when it is filed. |
| D4 | The Agent's required checks | **Decided (Hannah, 24 November 2026, launch message):** as recommended. **On pull requests** into `release/15/main`: `fast checks`, `unit` and `boundary`, the only jobs that run there; a skipped job counts as passing, so requiring the others protects nothing. **For the release:** the full comparison of CI and Lanes against the ceiling, on the batch runs and on the release head, plus `Chat service`, `Windows task host journey` and `Windows runtime retention`. Turn them on once AG-1's comparison passes on an unchanged tree. |
| D5 | When a failing test may be deleted rather than fixed | **Decided (Hannah, 24 November 2026, launch message):** as recommended. **The support line:** with no users yet, only current behaviour, and updating from the previous published release, is supported. A test of anything older is **retired**: older formats, the R0 and R1 install boundaries, tests that rebuild a historical commit's state, moved packs. It is deleted, citing the retiring change or this line. Where a user could still reach the old path today (an API route, a command, a file the App opens), a test asserts that it refuses, as with `410 retired_route`. A **redundant** test is deleted, naming the passing test that covers the same behaviour. A test of something users do today is never deleted for being hard to fix. Every deletion is listed in its PR and read by an `X` reviewer. AG-P1 and AG-P2 apply this first, to the [prune candidates](evidence/release-15-b324d7c1/prune-candidates.md), and every card applies it to what they missed. |
| D6 | Product bugs too large for this plan | **Decided (Hannah, 24 November 2026, launch message):** as recommended. A fix of a day or less is a card here. A larger one needs an `X` check that the test shows a real defect, an issue, and the owner's acceptance when it is filed. It then stays visibly red on the ceiling rather than being quarantined, which keeps Plan 39's D9 cap for real quarantines. |
| D7 | When the comparison starts protecting other lanes | **Decided (Hannah, 24 November 2026, launch message):** as recommended. From AG-1. Every batch run and every completed `release/15/main` run is compared, so other Release 15 lanes see new red within one full run. It doesn't run on each pull request, because pull requests don't run the failing jobs. |
| D8 | Whether a timeline's `fps` may be rational, `{numerator, denominator}` | **Decided (Hannah, 24 November 2026, launch message):** as recommended. AG-A9 (route S) first finds whether any production writer emits one. **If none does:** the fixtures write a number. **If one does:** the Runtime's contract schema accepts it, by a Runtime PR and release. The Agent's vendored copy follows by a pin bump, after Plan 77's pin moves. That needs the owner's go, because it moves a Runtime release. |
| D9 | Whether the Release 15 Lead compares integration and opt-in results by ID before this plan starts | **Decided (Hannah, 24 November 2026, launch message):** as recommended. Yes. [lanes-failing-ids.tsv](evidence/release-15-b324d7c1/lanes-failing-ids.tsv) is the integration counterpart of the existing unit baseline. Using it now stops more new integration red landing unnoticed (36 IDs already have). |
| D10 | The first-party packs the tests expect that moved to poms_packs (iteration, youtube, and the executors `understanding.audio_understand`, `video_editing.hype`, `editorial.transcribe`, `editorial.arrange`) | **Decided (Hannah, 24 November 2026, launch message):** as recommended. Retire those tests in the Agent (drop them from `PORTFOLIO_PACK_IDS` and the discovery fixtures), under D5, citing `config/astrid-beta-capabilities.json`, which records the move. The packs are tested in their own repository. AG-P1 and AG-P2 do it. |
| D11 | Which timeline-composition package the rendering tests pin | **Decided (Hannah, 24 November 2026, launch message):** as recommended. The test reads the chunk from the package `remotion/package.json` pins (0.0.19), not a hard-coded chunk name from another build. Pin a different build only if that is the one that ships. |
| D12 | The authentic legacy archive (44 integration IDs) | **Decided (Hannah, 24 November 2026, this plan's session):** restoring projects from before Release 12 is not needed ("we have no users rn"), so the tests are retired under D5. AG-P2 deletes them, citing this decision; the old AG-A4 card is gone. |
| D13 | Clip-level namespaced data and the reader check | **Decided (Hannah, 24 November 2026, launch message):** as recommended. Keep the data. `test_commit_runtime_opaque_items.py` promises that unknown namespaced values survive a commit, so the reader check is too strict, and AG-A8 (route S) fixes it unless it finds a recorded decision retiring that data. RS1 reviews the fix. |
| D14 | Product deadlines the moving tests depend on: the 2-second readiness probe and the macOS render reconciliation budget of about 1.2 seconds | **Decided (Hannah, 24 November 2026, launch message):** as recommended. Fix the tests' own fakes first (the Release 15 baseline shows the readiness fake takes 1.7–1.9 s to answer). Change a product deadline only with the owner's go, and with a measurement showing the deadline, not the fake, is wrong. |
| D15 | How the end is proved, given that `release/15/main` keeps moving and its runs get cancelled | **Decided (Hannah, 24 November 2026, launch message):** as recommended. Three green dispatched runs on one frozen head of `release/15/plan-91` (merged up with `release/15/main`) on three nights. Then one green run on `release/15/main` after landing. No freeze of `release/15/main` itself. |

## Source identities

- astrid-agent `release/15/main` at `b324d7c1`: measured above. The head on 24 November is `a09ea669`, and the critique and ambiguity passes read it; its runs were cancelled. AG-0 cuts from the head of the day and re-measures.
- astrid-agent `main` at `c0ad6b54aadd21630d98bb5039613e37efe92a8f` (the published Release 14): measured for comparison.
- astrid-agent `release/14/plan-39` at `2ef74155a1a984101408b19b4e1e4fd274f3178e`: reference only; nothing is ported.
- **Base choice.** The base is `release/15/main`, and the plan branch is `release/15/plan-91`. The other Release 15 plan branches were compared on 24 November by the files each changes against `release/15/main`:
  - **Landed:** Plans 13, 40, 69, 78, 81 and 89. There is nothing to choose.
  - **Disjoint:** Plans 56 and 87 change none of the failing test files and no shared CI file. Build on the release branch.
  - **Plan 77** (`release/15/plan-77` at `fda01977`) changes `.github/workflows/ci.yml`, both `runtime.lock.json` files and eight failing test files:
    - `tests/core/generation/backends/test_qwen_21_turbo.py`
    - `tests/core/generation/test_engine_custody.py`
    - `tests/core/generation/test_runpod_engine_selection.py`
    - `tests/editing_conformance/test_native_batch_ingress.py`
    - `tests/integrations/test_managed_host_preparation.py`
    - `tests/integrations/test_pinned_source_cpu.py`
    - `tests/integrations/test_r14_builtin_transitions.py`
    - `tests/test_installer_backup.py`

    **Stack, per file:** a card whose scope includes one of these files merges `release/15/plan-77` into its topic branch before its proof, and lands after Plan 77. Those cards are AG-A5, AG-A10, AG-B19, AG-B22 and their Wave C rows. Every other card builds on the release branch. AG-A1, AG-A2 and AG-A9 re-read the pins at dispatch, because Plan 77 moves them.
  - **Plan 88** (`release/15/plan-88` at `50125423`) changes two failing test files, `tests/sdk/test_timeline_checkout.py` and `tests/timeline/test_authoring_media.py`. AG-A7 and the Wave C rows that touch them stack the same way.
  - **Plans added to Release 15 later** get the same check at dispatch: `git merge-tree --write-tree --name-only release/15/main release/15/plan-<PP>`, against the card's files.
- astrid-dev: this plan's records land on `main`. AG-1 changes `env/baseline-diff.py` and AG-A1 changes `env/agent-setup.sh` here.

## References

- [Plan 39](../39-green-mains/plan.md), its [handover](../39-green-mains/handover.md) and its [owner decisions](../39-green-mains/inputs.md#owner-decisions) D3, D9 and D10, which this plan keeps.
- [Release 14 run board](../../releases/14/run.md) rulings 6a, 10 and 13; [Release 15 run board](../../releases/15/run.md).
- [Evidence](evidence/README.md): the measurement, the clusters, the card ownership, the Wave C cards and the [critique](evidence/critique.md).
