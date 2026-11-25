# One place to measure

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

**Project:** One place to measure

**Goal:** Anyone working on Astrid can measure how fast a part of it is, the same way every time and on what a person actually runs, and can see how each release compares with the one before.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 4 engineering days. A shared shape for result files and a generated table are left until a second plan has used the home (see Not included).

**Waiting on:** a release; the owner's decision D1 in [inputs.md](inputs.md#owner-decisions).

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary): a speed that is not measured the same way twice cannot be held, and on 22 November 2026 two plans each lost most of a day measuring something users do not run. F-001's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

On 22 November 2026 two lanes built measuring machinery separately. [Plan 81](../81-once-per-command/plan.md) built a repeatable before-and-after run of an installed build and showed `generate` queued in 5.4 s, down from 15.0 s. [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) built a browser harness for the timeline editor. Both learned the same lessons the hard way, and their tools and numbers now sit in different places with different habits. This plan gives measuring one method, one home and one record.

**Included:**

- **A shared workstream,** `astrid-dev-measure`, beside the other shared workstreams: the method on one page.
- **A home in astrid-dev,** `measure/`: a short index of the named scenarios and where each one's driver lives, one runner that works across repositories, and a dated list of results that links to the raw output behind each number.
- **Everything that exists is kept and placed.** Every measuring tool and result built so far is inventoried, saved where it can be found, and either moved to the home, left where it is with a pointer, or marked superseded. Nothing is lost and nothing lives only on a session's machine.
- **The tools that drive a product stay with that product** (the editor's harness and benchmark in the App, the command timings in the Agent) and are listed in the home.
- **A release that claims a speed shows it.** At a release's freeze rehearsal, the quick command-line scenarios are run once, paired, against the release people have now, and the result is linked from the release brief. It is a record, not a gate.

**The method, in short** (each line is a lesson of 22 November 2026, recorded in [inputs.md](inputs.md#planning-evidence)): measure what a person runs, an installed build or the compiled editor, never a development build or a source checkout alone; on a quiet machine; before and after alternated in one session; on a saved project built once and restored, not rebuilt; on the current code, with the exact commits written down; split into stages so one number does not hide where the time is; and repeatable by someone who did not write it.

**Not included:** a common schema for result files, a generated results table and a check on them: these wait until a second plan has used the home, and then belong with the repository's other generated views and checks; a speed comparison as a condition of every release; making anything faster (that is each speed plan's work); new timeline scenarios, which are [Plan 86](../86-the-timeline-feels-fast/plan.md)'s; a hosted dashboard; measuring on a GPU or a paid machine.

## Existing work and decision

The inventory is in [inputs.md](inputs.md#what-exists-today). In short: Plan 81's installed before-and-after runner, stand-in ComfyUI and profiler are in that plan's evidence folder; the App has `scripts/save-loop/` and an older editor benchmark, `npm run perf:editor`, used in October 2026 on a real 286-clip film; the Agent has command timings behind `--timings`; a page and a ledger entry describe a separate measurement machine; and the first numbers are spread over two plans' evidence folders.

**Decision: the method and the record live in astrid-dev; the drivers live with what they drive.** astrid-dev is where work across repositories and releases already lives. A driver has to change with its product, so it stays in that repository and is listed here.

## Sequence and readiness

1. **MS-1,** the inventory, and everything saved.
2. **MS-2,** the workstream and the home's index.
3. **MS-3,** one portable runner, from Plan 81's.
4. **MS-4,** the first results listed, and one scenario run from a clean checkout.
5. **MS-5,** the paired run at a release's freeze rehearsal.
6. **R,** one review round.

**Real dependencies:** Plan 81 landed, so its runner is final. Nothing else. **Unresolved:** D1 and a release. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** Plan 81's runner and results; the App's save-loop harness as it is; Plan 77's measurements. **Produces:** the workstream; `measure/` with its index, one runner and a list of results; a paired run at freeze rehearsal. **Compatibility:** no product behaviour changes. Existing evidence stays where it is; moved scripts leave a pointer behind.

## Completion

- **Nothing lost:** every tool and result in the inventory has a recorded place, and none exists only on a session's machine.
- **One way to measure:** from a clean checkout, with no path that exists only on one machine, one pinned scenario runs from the workstream and the runner alone.
- **The same answer twice:** an independent re-run of Plan 81's before-and-after from the new home reproduces its direction and rough size.
- **Numbers are kept honest:** each listed result names its exact commits, build, project, machine and load, links its raw output, and is compared only with results taken in the same session on the same machine, project, build and cache state.
- **Limits of the proof:** scenarios run on a CPU container with a stand-in ComfyUI unless a row says otherwise; what a real ComfyUI or a GPU adds is outside this plan. Landing remains the owner's.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

one comparable measurement method and index over existing machinery, early enough to guide cuts. Keep common results schema/dashboard/generated table framework deferred. No second benchmark engine.
