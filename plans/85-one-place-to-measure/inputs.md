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

**Challenge:** Pending — an independent critique is commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) and its result is recorded here before a run starts. Next: the critic's report and what the planner did with each finding.

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
| Test baseline comparison | astrid-dev `env/baseline-diff.py` | which tests changed between two commits | Not speed; left alone, named so nobody confuses the two |

## Owner decisions

- **D1 — how much slower counts.** When a release is compared with the last, a scenario slower by more than a margin is listed for her. (a) 10%; (b) 20%; (c) per scenario, set from each one's own run-to-run spread. Recommendation: (c), with 20% until a scenario has enough runs to know its spread. Pending.

## Source identities

No work has started. Read on 22 November 2026: astrid-dev `main` at `3db0fc91`; astrid-app `release/15/main` at `e3dbad64d402724ac5a35fb6447f18e432c64b78`. At run start record the branch and the commits.

## References

- [Plan 81](../81-once-per-command/plan.md) and [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md): where the tools and the lessons came from.
- [Plan 82](../82-reuse-across-commands/plan.md) and [Plan 86](../86-the-timeline-feels-fast/plan.md): the next two users of this.
- [Release workstream](../../skills/shared/workstreams/astrid-dev-release/SKILL.md): where the comparison is added.
