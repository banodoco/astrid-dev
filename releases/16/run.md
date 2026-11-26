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

How Release 16 runs unattended for days. **All judgment happens once, in Setup, before anyone is left running.** After that, each role repeats one short loop. This section is each role's whole job for this run: where it differs from a skill, this section wins. Don't open the skills to look for more work.

**Where each role runs:**
- the Lead and the orchestrators: Codex (or Claude cloud) sessions with network access;
- each manager: a Codex session, which opens each packet as a new ChatGPT chat;
- packets: those ChatGPT chats.

### The six rules

1. **The queue is fixed.** Setup writes every packet, in order. Nobody running the release adds, splits, re-scopes or reorders work; the only exception is a [fix packet](#fixed-messages). A plan is **finished** when every packet in it is Done or Parked.
2. **Proof is one command.** Every packet names its own **Proof:** command. The orchestrator runs it once, in its own session, on the head named in `READY-PROOF`. The result is one of three:
   - **PASS:** the command passes;
   - **FAIL:** the command ran and failed;
   - **COULDN'T RUN:** a cancellation, a timeout, a broken environment, or not finished by the next check.
   Nothing else counts as proof, and nothing more is collected.
3. **Every loop has a cap.** At the cap, mark the item **Parked**, post one line saying why, and move on. Parked work waits for the owner, and everything else keeps moving.
4. **Park, don't ask.** A question this section doesn't answer is parked, never debated. Nobody waits for an answer.
5. **Replace once, then park.** A session that is stuck, looping or confused is replaced by a fresh one with the fixed message, at most once each:
   - each packet's session, after one resume;
   - each manager, after one nudge;
   - each orchestrator, after one nudge.
   A second need parks that packet, plan or lane for the owner. The state is on GitHub, not in the chat.
6. **A missed check isn't made up.** If your scheduled check didn't fire, run the loop once now; don't backfill.

### Never, at any level

- Write evidence files, receipts, audits, readbacks, summaries or re-verifications. A one-line board comment is the whole record.
- Re-run a proof that passed, or run tests the packet doesn't name.
- Edit plans, skills, this section or `releases/16.md`. The orchestrator edits only `tasks.md` Progress ticks and fix packets.
- Start a new plan, investigation, review or document.
- Rebase, force-push, or create a branch outside the table below.
- Spend money, or use the owner's machine or media. Hosted CI on GitHub is not spend.

### Branches

| Branch | Who creates it | Who merges into it |
|---|---|---|
| `release/16/main` | Setup, once | the Lead, at a gate |
| `release/16/plan-<PP>` | Setup, once | the orchestrator, on PASS |
| `p<PP>/<packet-id>` | the packet session, from its plan branch's head | nobody: it is the PR's head |

Merge, never rebase. A PR always targets its plan branch. Before `READY-PROOF`, the packet merges its plan branch's head in. A PR that then won't merge cleanly counts as FAIL.

### Packet states

| State | Set by | When |
|---|---|---|
| Queued | Setup, or the orchestrator for a fix packet | written, waiting its turn |
| Running | the manager | its session has started |
| Proof | the packet session | it posted `READY-PROOF` |
| Rework 1, Rework 2 | the orchestrator | its proof FAILED |
| Done | the orchestrator | PASS, and merged into the plan branch |
| Parked | whoever hits a cap, or the orchestrator for a BLOCKED | it frees its slot, and the orchestrator parks each packet that depends on it; everything else continues |

Rework 1 and Rework 2 count as Running, for slots and for silence.

**Every park is one comment on the plan's board:** `PARKED <packet, plan <PP> or lane <n>>: <reason>`. A parked plan gets no new packets. A parked lane's managers stop once their slots are full.

The live state is the newest STATUS on each board, and each role's own last STATUS is its memory: it carries what was nudged, resumed and replaced. Nobody keeps a second copy.

### Setup (once, before leaving it running)

The owner does this with a planning session she chooses, such as the one that wrote this section; no running role does it. Running Setup again is the only way to change the run.
1. Choose the plans for this run. Take only plans whose owner decisions are answered and that need no real hardware. A plan without a written queue is not in this run.
2. For each plan, write every packet under `releases/16/packets/R16-P<PP>-<nn>.md`. Each packet has:
   - one contract, about three hours;
   - **Route** and **Depends** (earlier packets of the same plan only);
   - **May touch** and **Must not touch**;
   - the ids that already fail;
   - one **Proof:** command, which runs in under 30 minutes.
   Packets that touch the same file get a Depends link, so they never run at once. Review stops (RS, R) are packets too.
3. Write each plan's queue table below, in dispatch order.
4. Cut the branches, open the boards, record each plan's Run start naming its orchestrator, and fill in the Lanes table.
5. Start the Lead. The earlier Release 16 Lead (`session_011EzfW1C63rxLXsL6TkHHVV`) stands down.

### Lanes

| Lane | Plans in this run | Orchestrator | Board |
|---|---|---|---|
| 1 Install, update and release | chosen in Setup from 31, 10, 09, 29, 30, 38 | — | — |
| 2 Environment and generation | chosen in Setup from 93, 94, 90 (with Plan 56's residual), 35, 52, 53 | — | — |
| 3 Editing, media and render | chosen in Setup from 63 (with Plan 04), 87 (the Release 15 handoff, #1938), 79, 85 | — | — |

### Queues

One table per plan, written in Setup: Packet, Route, Depends, Proof. None is written yet.

### The Lead — every 3 hours

**Job:** keep the orchestrators alive and moving, and open the gates. Nothing else.

1. **Read** your own last STATUS, the newest STATUS on each lane's board, and new comments on your own board.
2. **Check each lane:**
   - **Moving:** its STATUS is under 2 hours old, and its Done plus Parked count rose within the last 6 hours. Do nothing; a lane that moves is no longer nudged.
   - **Not moving, not yet nudged:** send the nudge.
   - **Not moving, nudged, never replaced:** replace the orchestrator.
   - **Not moving after a replacement:** park the lane for the owner.
3. **Gates:** for each `GATE` request:
   - it shows `new failing ids: 0` → merge the plan branch into `release/16/main` and reply DONE;
   - it shows any new ids → reply "fix packet";
   - it says COULDN'T RUN → park the plan.
4. **Parked:** copy any new Parked lines into your STATUS, under "for the owner". Don't solve them.
5. **Post** one STATUS, then stop until the next check:

   ```text
   STATUS r16-lead | lane 1: <moving|nudged|replaced|parked> done+parked <n> (last rise <time>) | lane 2: … | lane 3: … | gates: <merged ids or none> | for the owner: <parked lines or none>
   ```

**Never:** read code, run tests, write or reorder packets, answer technical questions, or change a plan.

### The orchestrator — every hour

**Job:** turn `READY-PROOF` into Done or Rework, keep each plan's manager alive, and request the gate when a plan is finished.

1. **Read** your own last STATUS, then new comments on your lane board and your plans' boards, after your cursor.
2. **Each `READY-PROOF`:**
   - Check the PR's changed files. Any file outside the packet's May touch, or inside Must not touch, means FAIL.
   - Otherwise, run the packet's Proof command once, on that head, side by side with other proofs.
   - **PASS:** merge the PR into the plan branch, tick the packet's `tasks.md` Progress, and post `DONE <packet> <merge sha>`.
   - **FAIL:** post the rework message with the failing ids or files. After Rework 2, a third FAIL means Parked.
   - **COULDN'T RUN:** run it once more at the next check. If it still can't run, it is Parked. This doesn't count as a Rework.
3. **Each BLOCKED or other park:** post `PARKED <packet>` with its question or reason, then `PARKED` for each packet that depends on it.
4. **Each plan's manager:** if its last STATUS is over 2 hours old, nudge it. If it is still silent after the nudge, replace it, once. If the replacement is silent too, post `PARKED plan <PP>`.
5. **A finished plan:**
   - merge `release/16/main` into the plan branch;
   - run the repository's hosted CI on that head; if it is cancelled or times out, run it once more, and if that fails too, post `GATE plan <PP> | head <sha> | COULDN'T RUN`;
   - compare its failing test ids with `release/16/main`'s latest run, using `python3 env/baseline-diff.py --strict`;
   - post on the Lead's board: `GATE plan <PP> | head <sha> | new failing ids: <n> <ids>`.
   After "fix packet", write and queue one fix packet for those ids. A second gate with new ids parks the plan.
6. **Post** one STATUS, then stop until the next check:

   ```text
   STATUS r16-lane<n>-orchestrator | plan <PP>: queued <n> running <n> proof <n> done <n> parked <n> manager <ok|nudged|replaced> | … | acted on: <ids> | queued now: <fix packet ids or none> | parked: <lines or none> | cursor: <id>
   ```

**Never:** write a fix yourself, write any packet but a fix packet, judge a PR beyond the May touch check and the Proof command, run other tests, or ask the Lead anything but a gate.

### The manager — every hour

**Job:** start the next packet. You are a dispatcher, not a reviewer.

1. **Read** your own last STATUS, then new comments on your plan's board, after your cursor. Drop each packet posted as `PARKED` from your Running list. If the plan itself is parked, post a final STATUS and stop.
2. **Each Running packet** with no commit and no post for 3 hours:
   - send the resume message;
   - if it was already resumed, replace the session, once;
   - if a replacement goes silent too, post `PARKED <packet>: silent after replacement`.
3. **Free slots:** at most three packets per plan in Running or Proof. Fill them with Queued packets, in queue order, whose Depends are all Done. Fix packets the orchestrator posts as `QUEUED` come first. Each packet gets a NEW ChatGPT chat in its Route's mode (N High, X Extra High, S Pro), with the packet start message, named `r16-P<PP>-<nn>-<n>`.
4. **Each Rework** the orchestrator posted: send it to that packet's chat. If that chat won't load, use a new chat at the PR's head.
5. **Post** one STATUS, then stop until the next check:

   ```text
   STATUS r16-p<PP>-manager | running: <ids> | proof: <ids> | next: <id> | started: <ids or none> | resumed ever: <ids> | replaced ever: <ids> | cursor: <id>
   ```

**Never:** edit the repository, merge, judge code, answer a packet's question (its BLOCKED is the orchestrator's, on the same board), or start packets out of order.

### Fixed messages

Fill the `<…>`. Never write a different one.

- **Nudge:** `Check-in missed. Run your loop in releases/16/run.md "Delivery" now and post STATUS.`
- **Rework (orchestrator to packet):** `REWORK <n> of 2 for <packet>: FAIL on <head>. Failing: <ids or files>. Fix only these, inside May touch, merge the plan branch's head in, and post READY-PROOF again.`
- **Resume (manager to packet):** `Resume <packet>. Your branch is p<PP>/<id> at <head>. Read the board for messages to you, continue, and end with READY-PROOF.`
- **Fix packet (orchestrator, after "fix packet"):** write `releases/16/packets/R16-P<PP>-FIX.md`:
  - **Route:** X;
  - **Outcome:** make these test ids pass: `<ids>`;
  - **May touch:** the files the plan's packets touched;
  - **Must not touch:** the test files that hold those ids;
  - **Proof:** those ids, run directly with pytest.
  Then post `QUEUED R16-P<PP>-FIX` on the plan's board. One per plan.
- **Replace (any parent):** start a fresh session with that role's start message below, adding: `You replace <old session>. The state is on <board>, from comment <cursor>. Don't redo Done work.`

### Lead start message

The owner pastes this once, after Setup.

```text
You are the Lead for Release 16 of Astrid (mailbox r16-lead). Your whole job is the Lead loop in releases/16/run.md, section "Delivery: Lead, lanes and managers", on astrid-dev main. Run it every 3 hours with your own scheduled task, at a minute other than :00 or :30, and never do anything that section doesn't list.
Start the lane orchestrators named in its Lanes table now: create each session in my Codex account and send it the orchestrator start message. If a session won't take it as my message, post the text on your board for me to paste.
You may, without asking me:
- create, nudge and replace orchestrator sessions as the section says;
- merge plan branches into release/16/main on a GATE showing 0 new failing ids.
Everything else is parked for me.
```

### Orchestrator start message

```text
You are the orchestrator for Release 16 lane <n> (mailbox r16-lane<n>-orchestrator, board <issue URL>); the Lead is r16-lead. Your whole job is the orchestrator loop in releases/16/run.md, section "Delivery: Lead, lanes and managers", on astrid-dev main, for the plans the Lanes table gives your lane. Run it every hour with your own scheduled task, at a minute other than :00 or :30, and never do anything that section doesn't list.
Now start one manager per plan: create each session in the owner's Codex account and send it the manager start message for that plan.
You may, without asking:
- run each packet's Proof command, and merge PASSing PRs into your plan branches;
- tick tasks.md Progress;
- write and queue fix packets;
- run hosted CI once per gate;
- create, nudge and replace manager sessions as the section says.
Everything else is parked.
```

### Manager start message

```text
You are the manager for Release 16 Plan <PP> (mailbox r16-p<PP>-manager). Your orchestrator is r16-lane<n>-orchestrator, and your board is <issue URL>. Your whole job is the manager loop in releases/16/run.md, section "Delivery: Lead, lanes and managers", on astrid-dev main, over the Plan <PP> queue in that section and any fix packet posted as QUEUED. Run it every hour with your own scheduled task, at a minute other than :00 or :30, and never do anything that section doesn't list.
Start each packet in a new ChatGPT chat with this message, filled in:
"You are implementing ONE packet for Release 16: releases/16/packets/<id>.md on astrid-dev main. Follow agent/roles/manager/chatgpt-packet.md, except that you edit only files in the packet's May touch. Board: <issue URL>; you are r16-<id>-<n>. Branch p<PP>/<id> from release/16/plan-<PP>'s head, and write the code and tests only; never clone, build or run tests. Post an early STATUS once your draft PR is open. Merge the plan branch's head in, end with READY-PROOF <repo> <PR> <head>, and stop. If the packet can't be done inside May touch, post BLOCKED once with the reason and stop. Do not merge or start another packet."
You may start, resume and replace packet chats as the section says, and comment on the board. Nothing else.
```

### The owner's check-ins

Whenever you like, read the newest STATUS on `board: release 16 lead`. "For the owner" lists everything parked. Answer there, or run Setup again to change the run.

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
