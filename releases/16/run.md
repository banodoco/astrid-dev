# Release 16 — run board

The live state of the Release 16 run, rewritten at each check-in by the release manager. The [brief](../16.md) holds intent, included plans, branches and issues; each plan's `tasks.md` holds its progress.

## Scope change — 25 November 2026

The owner now places the full Plan 91 green programme in [Release 17](../17.md), not Release 16. The existing plan branch, packet names, mailbox, evidence and active authority below are preserved; nothing is deleted, renamed, force-pushed or merged by this scoping change. **Do not land Plan 91 into release/16/main.** Before another target-dependent dispatch or landing, the existing Lead and Plan 91 orchestrator must record a coordinated handoff, confirm in-flight work, and rebind destination, branch and proof on the Release 17 base. Until then use the existing lane only for already-authorized bounded work on its retained branch; do not start a competing lane or treat the historical launch message below as fresh authorization. The Release 17 brief is the intended destination, and the older dispatch section remains the record of the original run.

The Plan 91 mailbox records the owner-directed [STOP](https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7129888302) and [manager confirmation](https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7130215692): no packet was started and monitoring stopped. The older bounded-authority text does not override that STOP; only a later owner or orchestrator decision can resume it. Preserve its actual Agent branch and records.

## Proposed R16 readiness — pending scope agreement and dispatch

The brief holds strategy; each plan's tasks hold work and progress. This section records current readiness, branch/function reservations, scarce proof slots and source/pin deltas. It does not start a run. Reconfirm the existing Lead and each carried custodian before dispatch; preserve R15 priority, the P91 R17 handoff and held P82 authority.

1. Establish the current served/predecessor/candidate register and actual old origins. Confirm narrow owner decisions: qualification mode, retained P89 gate, Windows route, P38 role scope, grant restore/revoke policy and P52/P53 closure boundary. Independent inventory, fixtures, native feasibility and bounded implementation preparation proceed together once authorized.
2. Fill every ready nonconflicting work package: records/protection; native update/Pinokio/systemd; provider/closure; state/grants; existing and managed environments/exact plan; save model/corpus/capture; streaming media; pack/output/recovery; bounded paid safety; evidence; carried P52/P53 residuals. For each, link canonical task IDs, current branch/function holder, exact predecessor, next landing contract and proof venue. A different function in the same file is not a blanket conflict.
3. Hold only real joins: provider/schema review before dependent consumer landing; exact authorization before privileged apply; verified migration before retirement; individual inverse feasibility before batching; actual native engine authority before lifecycle proof. Start fixtures, adapters and venue discovery before those joins where useful.
4. Record two interim vertical checkpoints independently: existing-environment first creation with decline/consent; substantial import/edit/recovery/undo/reopen/short-render/next-render. Record exact tuples and limits. These are internal integration evidence, not shipment or automatic final acceptance.
5. Converge all retained outcomes, P56 residuals and bounded adjunct product changes through one pin integrator. Rehearse changed-schema lived-in update/rollback, grant/state recovery, native custody and generated publication. Resolve unknown causes; preserve original task history. Name current resource reservations and actual waits, not a new task list.
6. Freeze exact product/Runtime/client/schema/pack/bootstrap/launcher/engine identities after required landings and code/interface reviews. Qualify the retained support/negative matrix, actual served origins, heavy and native journeys; require complete comparable inventories and effective required checks. Then complete RL-R and final qualification reviews on that evidence before the owner's go. Rerun only affected evidence when inputs move, with explicit impact rationale; do not silently carry old passes.
7. Owner approves one exact tuple and ledger. P31 performs one protected Final transition and coherent generated sync/deploy, then verifies complete served bytes and live identity. Plans do not publish separately. Retain named post-live owner observations/administrative closure without pretending they happened before publication.

**Conditional critical path (proposal):** reviewed producer/identity/schema/grant contracts → slowest retained native custody, managed/exact workflow, save/inverse/migration, media/output or install/update consumer → coherent pin convergence → exact-tuple changed-schema/native/support/negative/heavy proof → RL-R and required final reviews → owner go → one protected Final/deploy and served readback. This is conditional on measured work and venue availability, not a committed duration.

**Shared-function reservations:** the existing Lead records the actual holder, branch/function, next landing contract and proof venue when each lane is authorized and ready. Reserve the P38 Runtime lock, P90/P56 workflow command and schema, readiness/error case table, P63 outcome/queue mutation, shared media add/placement, pack/schema generator, and release pins/publication writer individually. No holder, branch, date or capacity is assigned by this proposed section. Independent fixtures and venue discovery can start before these joins once authorized.

At every check-in: read all current mailbox messages; reconcile predecessor moves, task receipts, exact writer conflicts and proof availability; start ready work within actual authorized capacity; report blocked contracts/resources with owner and next action. Agent CI remains subject to existing shared authority and the current Release Lead's priority and capacity decisions. P91's historical launch text is not new R16 authorization. No new permanent scheduler, strategy file or tracker is introduced.

## Delivery: Lead, lanes and managers

The Lead's worksheet for running Release 16 once the owner agrees its scope. It holds who runs what, the hourly checks and the launch messages; the rules behind them live in the skills it links, and each plan's `tasks.md` holds its progress. The Lead rewrites the tables at each check-in.

### How it runs

- **One Lead** (`r16-lead`): owns the release. Every hour it confirms that each orchestrator is alive and its lane moved, unblocks what didn't, answers gates, and confirms every landing into `release/16/main` ([Leader](https://github.com/banodoco/astrid-dev/blob/main/agent/roles/leader.md), [lane orchestrators](https://github.com/banodoco/astrid-dev/blob/main/agent/roles/leader/lane-orchestrators.md)).
- **Up to three lane orchestrators** (`r16-lane<n>-orchestrator`): each answers for its lane's plans. It cards each plan into packets, starts one manager per plan, runs every proof, reviews, and merges into the plan branches ([lane orchestrator](https://github.com/banodoco/astrid-dev/blob/main/agent/roles/orchestrator/lane-orchestrator.md); as the Lead for its own plans, [fresh-packet dispatch](https://github.com/banodoco/astrid-dev/blob/main/agent/roles/leader/multi-manager-release.md)).
- **One manager per plan** (`r16-p<PP>-manager`, a Codex session as for Plans 87, 89 and 91): it starts each Ready packet in a fresh ChatGPT session in its Route's mode, keeps sessions moving, and passes `READY-PROOF` to its orchestrator. It never merges or edits the repository ([dispatch](https://github.com/banodoco/astrid-dev/blob/main/agent/roles/orchestrator/multi-manager-dispatch.md)).
- **One fresh ChatGPT session per packet** (`r16-P<PP>-<nn>-<n>`): writes one packet's code and tests, ends with `READY-PROOF`, then stops ([packet](https://github.com/banodoco/astrid-dev/blob/main/agent/roles/manager/chatgpt-packet.md)).

The chain is Lead → orchestrator → manager → packet. Each role posts on its own board ([rules](https://github.com/banodoco/astrid-dev/blob/main/agent/shared/run-contract.md#coordination-boards-and-check-ins)):
- the Lead on `board: release 16 lead`;
- each orchestrator on `board: release 16 lane <n>`;
- each manager and its packets on `board: release 16 plan <PP>`.

A plan gets its manager only when it has Ready packets, so not every plan has one at once.

### Before any lane starts

1. **Take the role.** The new Lead:
   - posts on its board;
   - records itself as release manager in [releases/16.md](../16.md);
   - takes over from the earlier Release 16 Lead (`session_011EzfW1C63rxLXsL6TkHHVV`), which then stands down.
2. **Scope agreement.** Bring the owner, in one message, [PR #1964](https://github.com/banodoco/astrid-dev/pull/1964) and the decisions in its [scoping handoff](evidence/scoping/README.md#scoping-handoff--pending-owner-scope-decision), each with a recommendation. Nothing is implemented until she agrees. Then merge it.
3. **Branches and Run start.** Cut `release/16/main` in each repository from the `release/15/main` heads she names (merge forward, never rebase). Record each plan's Run start, naming its lane orchestrator as the accountable agent.
4. **Lanes.** Start the lanes with the launch message below, one session each.

### Lanes

Plans are carded in this order and run side by side once carded. One writer per function, schema or pin, as the Approach in [releases/16.md](../16.md) reserves them.

| Lane | Plans, in carding order | Orchestrator | Board | State |
|---|---|---|---|---|
| 1 Install, update and release | 31, 10, 09, 29, 30, 38 | — | — | not started |
| 2 Environment and generation | 93, 94, 90 (with Plan 56's residual), 35, then the Plan 52 and 53 residuals | — | — | not started |
| 3 Editing, media and render | 63 (with Plan 04), 87 (the Release 15 handoff, #1938), 79, 85 | — | — | not started |

### Plans

| Plan | Lane | Manager | Board | Packets ready / running / review | Next |
|---|---|---|---|---|---|
| 31 | 1 | — | — | 0 / 0 / 0 | card after scope agreement |
| 10 | 1 | — | — | 0 / 0 / 0 | card; native Stop/Quit first |
| 09 | 1 | — | — | 0 / 0 / 0 | card; IU-0 freezes the sources |
| 29 | 1 | — | — | 0 / 0 / 0 | reconcile the Release 12 rows, then card |
| 30 | 1 | — | — | 0 / 0 / 0 | after Plan 29's UR-1 and UR-9 to UR-11 |
| 38 | 1 | — | — | 0 / 0 / 0 | card |
| 93 | 2 | — | — | 0 / 0 / 0 | card CD-0 and CD-1 |
| 94 | 2 | — | — | 0 / 0 / 0 | card ER-0 and ER-1 |
| 90 | 2 | — | — | 0 / 0 / 0 | after Plan 56's residual is reconciled |
| 35 | 2 | — | — | 0 / 0 / 0 | card from scratch |
| 52, 53 | 2 | — | — | 0 / 0 / 0 | confirm the existing custodians |
| 63, 04 | 3 | — | — | 0 / 0 / 0 | card; inverse and batching first |
| 87 | 3 | — | — | 0 / 0 / 0 | take over the Release 15 handoff |
| 79 | 3 | — | — | 0 / 0 / 0 | card |
| 85 | 3 | — | — | 0 / 0 / 0 | card |

**Cap:** at most five packets in Running or Review per lane. The release total stays within the number of ChatGPT sessions the account can run at once, which the first manager's startup checks measure.

### Hourly checks

**Lead**, about ten minutes:
1. Check liveness: `python3 scripts/boards.py roster 16`. Nudge any orchestrator or manager with no post for 2 hours. At 3 hours, replace the session or tell the owner.
2. Check movement: each lane should have a commit, PR, packet move or `tasks.md` tick since the last check. If not, say whether the work or the environment is the cause, and fix it where it lives.
3. Answer every gate and REQUEST on your board, once, with the condition and next step attached.
4. Reconcile release status: `python3 scripts/astrid_dev.py release status 16 --refresh`, then `--check`.
5. Rewrite the Lanes and Plans tables, post one STATUS, and add any rulings to the decisions log for the owner.

**Orchestrator:**
1. Read your board and your plans' boards by cursor.
2. Answer each `READY-PROOF` within 45 minutes, running proofs in parallel.
3. Keep every carded plan with a live manager and its next packets written before the current ones finish.
4. Run the parallelism pass, then post one STATUS.

**Manager:** every 20 minutes while a packet is Running or in Review, hourly otherwise, as its launch message says.

### Standing rulings

These hold for every lane, on top of the skills:
1. **Fixes are packet work.** Orchestrators and the Lead diagnose, prove, review and merge; they don't write the fix.
2. **Only harm blocks.** Harm means lost work, a broken install, update or rollback, wrong output on a real path, or a broken promise of this release. File everything else as an issue and move on.
3. **Plan 91 is Release 17's.** Its branch, board (#1826) and packets above are not this release's work.
4. **Nothing paid.** Nothing runs on rented machines, the owner's machine or her media without her go. Real-hardware rounds go through user test requests such as [#1952](https://github.com/banodoco/astrid-dev/issues/1952).

### Waiting on the owner

- Paste the Lead start message below into the Lead's session.
- The scope agreement, which the Lead brings her.
- A Codex device sign-in in any session whose login check fails.
- A resume nudge when a session's window ends and the Lead can't resume it.

### Lead start message

The owner pastes this into the Lead's own session.

```text
You are the Lead (release manager) for Release 16 of Astrid, "Make Astrid dependable" (0.1.0), and you answer for it shipping. Your mailbox name is r16-lead.
Follow the astrid-dev Leader role (agent/roles/leader.md) and its lane-orchestrators and multi-manager-release workstreams, in banodoco/astrid-dev.
Your worksheet is releases/16/run.md, section "Delivery: Lead, lanes and managers"; the brief is releases/16.md. Read both on PR #1964's branch until it merges, then on main.
First do "Before any lane starts": post on board: release 16 lead, and bring me the scope agreement in one message, with your recommendation on each decision. Nothing is implemented until I agree.
Then run the release through up to three lane orchestrators, as the worksheet lays out. Each answers for its lane's plans, and each plan has one manager that hands its packets to fresh ChatGPT sessions. Create the orchestrator sessions and send each one the worksheet's orchestrator message from my account; if a session won't take it as my message, give me the text to paste.
Every hour: run the worksheet's Lead check, post one STATUS on your board, and keep a decisions log I can read each morning.
You may, without asking me:
- create, resume and replace orchestrator and manager sessions in my Codex account;
- attach any banodoco repo;
- cut release/16/* branches from the release/15/main heads I agree (merge forward, never rebase);
- edit and merge Release 16's astrid-dev records: the worksheet, packets, tasks.md progress, and the Run start lines for the scope I agreed;
- confirm gates and merge plan branches into release/16/main on your by-id comparison;
- dispatch hosted CI within the shared slots.
Come to me for:
- the scope agreement and the decisions it lists;
- changing an existing test assertion beyond a plan's rules;
- anything paid, rented machines, or my machine or media;
- publishing a release.
```

### Orchestrator launch message

The Lead fills each `<…>` and sends it, one session per lane.

```text
You are the orchestrator for Release 16 lane <n>, <lane name>: Plans <list>. You answer for those plans finishing. Your mailbox name is r16-lane<n>-orchestrator, and the Lead is r16-lead.
Follow the astrid-dev Orchestrator role and its lane-orchestrator workstream in banodoco/astrid-dev. For your own plans, also take the Lead's part in agent/roles/leader/multi-manager-release.md ("A lane can be the Lead for its own plan").
Your worksheet is releases/16/run.md, section "Delivery: Lead, lanes and managers", on astrid-dev main. Your plans' Run start lines name you.
For each plan, in the worksheet's order:
- Card it into packets under releases/16/packets/R16-P<PP>-<nn>.md: one contract each, about three hours, with May touch, Must not touch, the focused selectors and the ids that already fail.
- Open its board, board: release 16 plan <PP>.
- Start one manager for it in a Codex session, with the worksheet's manager message.
- Keep the next packets written before the current ones finish.
Packets have no network, so you run every proof. You also review, merge into release/16/plan-<PP>, and commission each plan's review stops. Then ask the Lead for the gate into release/16/main, with your by-id comparison.
Every hour: run the worksheet's orchestrator check and post one STATUS on board: release 16 lane <n>.
You may, without asking:
- run Codex, or Claude subagents if Codex refuses;
- attach any banodoco repo;
- cut release/16/plan-<PP> from release/16/main;
- create, resume and replace manager sessions in the owner's Codex account;
- write and merge your plans' packets, tasks.md progress and evidence in astrid-dev;
- merge into your plan branches on green.
The Lead decides direction; bring anything else to the Lead.
```

### Manager launch message

The orchestrator fills each `<…>` and sends it, one session per plan.

```text
You are the manager for Release 16 Plan <PP> (<title>). Your mailbox name is r16-p<PP>-manager, and you report to r16-lane<n>-orchestrator (session <id>).
Follow agent/roles/orchestrator/multi-manager-dispatch.md in banodoco/astrid-dev, with your orchestrator as "the Lead".
Board: <issue URL> (board: release 16 plan <PP>); its format is in its first post. Your packets are releases/16/packets/R16-P<PP>-*.md on main, and the queue is the plan's row in releases/16/run.md. Re-read both at every check.
First do the startup checks and post one STATUS with each result:
- the board works both ways;
- you can start a fresh ChatGPT session in each Route's mode, and resume one;
- your hourly reminder fires;
- a packet session can push, open a draft PR and comment in each repository the packets name;
- how many ChatGPT sessions the account can run at once.
Dispatch nothing until the orchestrator's DECISION answers it.
Then give each Ready packet a FRESH ChatGPT session in its Route's mode (N High, X Extra High, S Pro), with the workstream's packet start message, named r16-P<PP>-<nn>-<n>. The first packet goes alone.
Every 20 minutes while a packet is Running or in Review (hourly otherwise):
- read the board by cursor;
- check every open packet;
- start every Ready packet that has no unmet dependency and no function conflict with a running one, within your lane's cap;
- resume or replace stalled sessions;
- pass READY-PROOF to the orchestrator.
Post one STATUS an hour.
You may start, resume, stop and replace packet sessions and comment on the board. You may not merge, edit the repository, approve anything or dispatch CI. If a check fails, say which step the owner must do.
```

## Now (11:20 UTC, Tue 24 Nov; historical before the scope change)

Release 16 is a draft. Plan 91 (Agent main green) runs now as its own lane, moved here from Release 15 by the owner on 24 November 2026; its section is below. The Release 16 Lead is `session_011EzfW1C63rxLXsL6TkHHVV`.

## Plan 91 dispatch

Added 24 November 2026. The owner started [Plan 91](../../plans/91-agent-main-green/plan.md) in its orchestrator's session and confirmed its D1 and D3–D15. The same day, in the Release 15 Lead's session, she moved it to Release 16 (D1, "Move Plan 91 to Release 16"): it runs now, at the same pace, and targets `release/16/main` from the start. It works like Release 15's [Plans 87 and 89 dispatch](../15/run.md#plans-87-and-89-dispatch), with the same roles, standing rulings, manager startup checks and cadence, and with the names and differences below. The [Run start](../../plans/91-agent-main-green/inputs.md#planning-evidence) holds the owner's authority.

| Plan | Mailbox | Run | Orchestrator | Manager |
|---|---|---|---|---|
| 91 | [astrid-dev #1826](https://github.com/banodoco/astrid-dev/issues/1826) | `r15-p91-dispatch` | `r15-p91-orchestrator`, Claude session `session_011EzfW1yUojAfWkGcaZNRph` | `r15-p91-manager-1` |

The mailbox names keep their `r15-` prefix, as they were opened before the move. Packet sessions are `r16-P91-<nn>-<n>`.

- **Lead:** the Release 16 Lead (`session_011EzfW1C63rxLXsL6TkHHVV`). Its DECISIONs bind the orchestrator, the manager and packet sessions within this section and the Run start. Its gate covers only the landing into `release/16/main`.
- **Plan branch:** astrid-agent `release/16/plan-91`, cut by the orchestrator at `514499de` (the `release/15/main` head of 24 November). `release/16/main` is not yet cut, so the orchestrator merges `release/15/main` forward into the plan branch as it moves, and `release/16/main` once it exists. `release/15/plan-91`, cut first at the same commit, is superseded and unused. The manager's check 6 covers astrid-agent, and astrid-dev for R16-P91-06's `env/` change.
- **In the orchestrator's own lane:** AG-0 (done), AG-1 (the gate, the `workflow_dispatch` inputs and the comparison), AG-2, every hosted card run and batch run, the ceiling ratchet, RS1, R and AG-10. Packet sandboxes cannot reach `github.com`: packets post `READY-PROOF astrid-agent <PR> <head> <selectors>` and the orchestrator runs the proof.
- **Needs the owner:** changing an existing assertion beyond what Plan 91's [triage rules](../../plans/91-agent-main-green/tasks.md#triage-rules) allow; any Runtime PR or release (D8); accepting a D6 or D3 ceiling entry; turning on required checks.

### Standing rulings (Plan 91)

1. Release 15's Plans 87 and 89 rulings 1–3, 5 and 6 apply as written.
2. Release 15's [rulings for Plan 82](../15/run.md#rulings-for-plan-82-from-the-first-three-dispatches) apply to Plan 91, from the Release 15 Lead's review of the first twelve merged packets:
   - packets have no network and run no hosted test, so each packet's list of already-failing IDs and its focused selectors come from AG-0's [card lists](../../plans/91-agent-main-green/evidence/release-15-514499de/cards/);
   - one contract per PR, aimed at about three hours; a larger card is delivered as consecutive PRs at its seams;
   - every packet lists what must pass unchanged, and an existing assertion changes only as the triage rules allow; a packet that finds this untrue posts `BLOCKED` once with the exact list;
   - measurement stays in the lane;
   - sweeps carry their count;
   - the orchestrator answers each `READY-PROOF` within 45 minutes, independent proofs in parallel, and reads the mailbox to the last page at every check.
3. **Comparisons are whole-run by id,** keyed by job family (`unit`, `integration`, `darwin native`, `opt-in`, and single jobs by name), never per shard: tests move between shards across runs ([AG-0](../../plans/91-agent-main-green/evidence/release-15-514499de/README.md#two-findings-for-ag-1)).
4. **Cap:** at most **five** packets in Running or Review at once (the owner's choice for this plan). The first packet goes alone, until its early STATUS shows a session can push, open a draft PR and comment.
5. **Agent CI is shared with Release 15** while it is unpublished: at most two Agent CI runs at once across both releases, and Release 15's landing gates take a slot first. The orchestrator checks the running `ci.yml` and `lanes.yml` runs before it dispatches, names its slot in each hourly report, and asks the Release 15 Lead for any slot that competes with a Release 15 gate.
6. Packets never edit `ci/agent-ceiling.tsv`. Only the orchestrator ratchets it, and only down, after a hosted batch run.

### Dispatch queue (Plan 91)

The order is tasks.md's [dispatch order](../../plans/91-agent-main-green/tasks.md#dispatch-order). Wave C packets are written after RS1 regenerates its list. Each packet names its own dependencies.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| [R16-P91-01](packets/R16-P91-01.md) | AG-P1 (X): the prune pass, CI | Ready (first, alone) | — | One PR per area; posts kept IDs early |
| [R16-P91-02](packets/R16-P91-02.md) | AG-P2 (X): the prune pass, Lanes | Ready (after R16-P91-01's early STATUS) | — | D12's legacy archive tests retire |
| [R16-P91-03](packets/R16-P91-03.md) | AG-A8 (S): clip-level namespaced data and the reader check | Ready (design note first) | — | D13; RS1 reviews |
| [R16-P91-04](packets/R16-P91-04.md) | AG-A9 (S): rational frame rates | Ready (investigation note first) | — | D8; a Runtime PR needs the owner's go |
| [R16-P91-05](packets/R16-P91-05.md) | AG-A7 (N): fixtures write `output.resolution` | Ready | — | The largest single refusal |
| [R16-P91-06](packets/R16-P91-06.md) | AG-A1 (N): the unit shards install the Runtime editable | Ready (merges after AG-1) | — | astrid-agent, and astrid-dev `env/` |
| [R16-P91-07](packets/R16-P91-07.md) | AG-A2 (N): CI provides the tests' inputs | Blocked on R16-P91-06 merging | — | Same `ci.yml` steps |
| [R16-P91-08](packets/R16-P91-08.md) | AG-A10 (N): the fake client takes `**kwargs` | Ready | — | 0.25 days |
| [R16-P91-09](packets/R16-P91-09.md) | AG-A6 (N): the ABI-1 binding fixture | Ready | — | — |
| [R16-P91-10](packets/R16-P91-10.md) | AG-A3 (N): fixtures and resources | Ready | — | D10, D11 |
| [R16-P91-11](packets/R16-P91-11.md) | AG-A5 (X): the kept installer tests | Blocked on R16-P91-01's verdict | — | — |
| [R16-P91-12](packets/R16-P91-12.md) to [R16-P91-30](packets/R16-P91-30.md) | AG-B1 to AG-B22 (Wave B, in index order) | Ready as slots free, each after its own dependency | — | Listed in [tasks](../../plans/91-agent-main-green/tasks.md#run-decisions) |

### Manager launch message

The owner pastes this into the manager's own session (a Codex session, as for Plans 87 and 89).

```text
You are the manager for Release 16 Plan 91 (Agent main green), mailbox name r15-p91-manager-1, reporting to the Plan 91 orchestrator (mailbox name r15-p91-orchestrator, Claude session session_011EzfW1yUojAfWkGcaZNRph).
Follow skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md in banodoco/astrid-dev, with the orchestrator as "the Lead".
Read releases/16/run.md on main, section "Plan 91 dispatch", then again at every hourly check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1826, format in its first post.
First do the manager startup checks (Release 15's "Manager startup checks" for Plans 87 and 89, run against #1826, for astrid-agent and astrid-dev) and post one STATUS with each result. Dispatch nothing until the orchestrator's DECISION answers it.
Then give each Ready packet a FRESH ChatGPT session in the mode its packet's Route sets (N High, X Extra High, S Pro), with the workstream's packet start message, naming the session r16-P91-<nn>-<n>. Dispatch R16-P91-01 alone first.
Every hour: read the mailbox to the last page, check every open packet, run the parallelism pass (start every Ready packet with no unmet dependency and no file conflict with a Running one, up to five in Running or Review), resume or replace stalled sessions, pass submissions and READY-PROOF posts to the orchestrator, and post one STATUS.
You may start, resume, stop and replace packet sessions and comment on the mailbox. You may not merge, edit the repository, approve anything or dispatch hosted CI. Send anything reserved to the owner to the orchestrator.
If a check fails, say which manual step the owner must do instead of promising automation.
```
