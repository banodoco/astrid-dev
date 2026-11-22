# Inputs — One place to measure

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — The owner asked on 22 November 2026 in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "do you think we should have like a general, subfolder inside ... astrid-dev, that does this profiling across the various parts of the app?", and then: "Could you create like a plan for this in astrid-dev? ... we should basically create like a work stream for this ... a shared work stream ... and then basically just kind of like the central place to manage that, like the tooling for it, and then the stuff inside the repo. We should make sure all the existing stuff is saved, but we mention it in this project so that it can be ... organize[d] ... appropriately." She has not chosen its release.

**Prior art:** What exists today is listed [below](#what-exists-today), read on astrid-dev `main` at [`3db0fc91`](https://github.com/banodoco/astrid-dev/tree/3db0fc91) and astrid-app `release/15/main`. The lessons the method is built from, each seen on 22 November 2026:

- **A development build is not what a person runs.** An empty timeline opened in 19.9 s on the development build and 1.6 s compiled; Plan 77's earlier figures were on the development build ([Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md)).
- **A source checkout is not an install.** Plan 81 was scoped from source timings; on an installed build a timeline edit already took about 1.1 s, and its 4.2 s gate was a source figure ([Plan 81](../81-once-per-command/plan.md)).
- **A shared machine is noise.** Control runs an hour apart differed by a second with load from 1.1 to 3.7; Plan 81 moved to alternated pairs under a load gate.
- **A project rebuilt every run costs hours.** Plan 77's standard project took over three hours to build and had never completed; it is now built once and restored ([ledger](../../docs/ledger/2026-11-22-separate-measurement-session.md)).
- **Old code gives old answers.** Plan 77's build predated Release 14's save fixes, and a bug it reported was not on the current branch ([astrid-dev #1427](https://github.com/banodoco/astrid-dev/issues/1427)).
- **One number hides the cause.** "About 60% unexplained" became a ranked table only when a profile of the installed command was taken.
- **A result one machine produced is not yet a result.** Plan 81's reviewer re-runs its script before the figure is quoted.

**Approach:** Where the machinery lives.

| Option | For | Against |
| --- | --- | --- |
| Method, runner and record in astrid-dev; drivers with their products (chosen) | One method and one record across repositories and releases; a driver changes with what it drives | Two places to look, joined by the catalogue |
| Everything in astrid-dev | One place | A browser harness for the editor would drift from the App it drives, and the App's CI could not run it |
| Each product keeps its own, with a shared page of advice | No moving | This is today: two shapes, numbers that cannot be compared, lessons learned twice |

**Challenge:** Reviewed — an independent Codex critic (on the high-judgment role, high effort, read-only, no part in the draft) was commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 22 November 2026 and read this plan and Plan 86 against the repositories; its report is [critique.txt](evidence/critique.txt). It ran no benchmarks. The owner has asked that such critiques be weighed, not adopted wholesale; what the planner did with each finding on this plan:

- **Accepted — the draft built too much.** A common schema for result files, a generated table and a check, with two users, is a framework before its second use. The plan now delivers the workstream, a short index, one portable runner and a list of results; the rest is named as later work with where it would live. The estimate falls from about 7 days to about 4.
- **Accepted — the inventory was incomplete.** It missed the App's editor benchmark (`npm run perf:editor`, used on a real 286-clip film in October 2026), Plan 54's phase timings, Plan 55's standing meter and fingerprint benchmark, Plan 81's attribution profiler, the execution host's start-up events, the App's bundle budgets and its extension performance tests. All are now in the table.
- **Accepted — a wrong label.** Plan 81's "after" arm was a local pin-bump on its plan branch; the draft would have listed it as the Release 15 candidate. MS-4 lists each result as it really was.
- **Accepted — two proofs that would not have worked.** "A fresh reader runs a scenario from the workstream alone" is replaced by one pinned scenario from a clean checkout with machine-only paths removed. The draft cited a check on words added to skills; there is no such registered check, and the mention is gone.
- **Accepted — the separate-machine page is linked, not folded in.** It is the orchestrator's guide to custody of a saved project, and stays where it is.
- **Accepted — what may be compared.** Only arms alternated in one session on the same machine, project, build and cache state.
- **Partly accepted — the release comparison.** The critic would drop it: qualifying a release already takes hours. The owner asked for each release to be compared with the last, and the quick command-line scenarios take minutes, so it stays as one paired run at freeze rehearsal, recorded and linked, and is not a gate.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: a stand-in ComfyUI on a CPU container unless a row says otherwise.

**Review rounds:** Recommended: one round at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## What exists today

| What | Where | What it measures | Proposed fate |
| --- | --- | --- | --- |
| Installed before-and-after runner, summary, profiler | astrid-dev `plans/81-once-per-command/evidence/installed-container-baseline/` (`run-installed-baseline.sh`, `run-ab-installed.sh`, `ab_run.py`, `ab_summary.py`, `rebuild_ab_summary.py`, `profile-generate.py`) | `generate` to queued and a timeline edit, on installed builds, two sets of commits alternated | Scripts move to `measure/runner/` (MS-4); results stay |
| Stand-in ComfyUI | the same folder, `standin/standin_comfy.py` | lets the command run without a GPU | Moves with the runner |
| The owner's fifteen-command baseline script | astrid-dev `plans/81-once-per-command/evidence/us0-baseline/` | the same commands on any installed Astrid | Becomes the first scenarios (MS-4) |
| Attribution and hashing evidence | astrid-dev `plans/81-once-per-command/evidence/attribution/`, `2026-11-22-attribution-bundle/` | where a command's time goes | Stays as evidence; its method goes into the workstream |
| Command timings | astrid-agent `astrid/sdk/command_timing.py`, `--timings` (on `release/15/plan-81` until Plan 81 lands) | stages inside one command | Stays in the Agent; listed as a driver |
| Editor harness | astrid-app `scripts/save-loop/` (`build-fixture.mjs`, `sweep.mjs`, `edits.mjs`, `cpu.mjs`, `drops.mjs`, `clash.mjs`, `readiness.mjs`, `run.sh`) | opening, saving, processor time of the Runtime and the browser, on a synthetic project | Stays in the App; listed as a driver; its results read by an adapter (MS-5); its weaknesses are [Plan 86](../86-the-timeline-feels-fast/plan.md)'s first task |
| Edit trace and two-moment drag observer | Plan 77's hosting session; partly recorded in astrid-dev by #1428 | where one edit stops between gesture and save | To be confirmed committed (MS-1) |
| The 616-clip project and its backup | the Release 15 Lead session's machine, built 22 November 2026 | the standard heavy project | Tied to the machine that built it; recorded, not moved |
| Separate measurement machine | astrid-dev `skills/roles/astrid-dev-orchestrate/workstreams/measurement-box/`, `docs/ledger/2026-11-22-separate-measurement-session.md` | how to get a quiet machine | Folded into the workstream (MS-2) |
| Editor benchmark | astrid-app `scripts/perf/measure-editor.mjs`, `scripts/perf/compare-editor-measure.mjs`, `npm run perf:editor`; results in `docs/quality/editor-efficiency-2026-10.md` | idle cost, playback rate and holds, scrub latency, renders, on a real 286-clip film in October 2026 (warm development builds) | Stays in the App; listed as a driver; reused by [Plan 86](../86-the-timeline-feels-fast/plan.md), which first fixes a counting fault in its comparator |
| Preview scrub evidence test | astrid-app `tests/e2e/timeline/preview-scrub-evidence.spec.ts` | that the frame shown after a seek matches a reference, cold and repeated | Stays; reused by Plan 86 |
| Bundle budgets, extension performance tests | astrid-app `config/vite/bundleBudget.ts`, `tests/e2e/timeline/extension-performance-budget.spec.ts` | size of what the App ships; an extension's cost | Stay; listed |
| Attribution profiler | astrid-dev `plans/81-once-per-command/evidence/2026-11-22-attribution-bundle/tools/profile_runner.py` | a ranked profile of one command | Moves with the runner (MS-3) |
| Phase timings, standing meter, fingerprint benchmark | astrid-dev `plans/54-warm-latency/` (tasks near 12), `plans/55-local-speed/` (tasks near 60; `evidence/continuation-20261116/ls12-fingerprint-benchmark.json`) | generation phases on a warm engine; hashing cost | Stay as evidence; listed |
| Start-up events of the execution host | astrid-agent `astrid/core/execution/generic_host.py` (near 125) | where the host's start-up time goes | Stays in the Agent; listed |
| Test baseline comparison | astrid-dev `env/baseline-diff.py` | which tests changed between two commits | Not speed; left alone, named so nobody confuses the two |

## Owner decisions

- **D1 — how much slower is worth her attention.** When the paired run at freeze rehearsal is recorded, a scenario slower by more than a margin is pointed out to her. (a) 10%; (b) 20%; (c) per scenario, set from each one's own run-to-run spread. Recommendation: (c), with 20% until a scenario has enough runs to know its spread. Pending.

## Source identities

No work has started. Read on 22 November 2026: astrid-dev `main` at `3db0fc91`; astrid-app `release/15/main` at `e3dbad64d402724ac5a35fb6447f18e432c64b78`. At run start record the branch and the commits.

## References

- [Plan 81](../81-once-per-command/plan.md) and [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md): where the tools and the lessons came from.
- [Plan 82](../82-reuse-across-commands/plan.md) and [Plan 86](../86-the-timeline-feels-fast/plan.md): the next two users of this.
- [Release workstream](../../skills/shared/workstreams/astrid-dev-release/SKILL.md): where the comparison is added.
