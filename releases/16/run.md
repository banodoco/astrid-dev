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

## Delivery: Lead and managers

How Release 16 runs unattended for days. **All judgment happens once, in Setup, before anyone is left running.** After that, each role repeats one short loop. This section is each role's whole job for this run: where it differs from a skill, this section wins. Don't open the skills to look for more work.

| Role | Runs in | Every | Job |
|---|---|---|---|
| Lead (`r16-lead`) | Codex | hour | Sends one Luna per active plan to run the plan loop; acts on what comes back; sends Sol for capped fixes; merges finished plans. It reads only one-line results, never code or logs. |
| Manager (`r16-p<PP>-manager`) | Codex, one per active plan | hour | Starts the next packet in a new ChatGPT chat, and resumes or replaces silent chats. |
| Packet (`r16-P<PP>-<nn>-<n>`) | a ChatGPT chat | — | Writes one packet's code and tests, runs its Proof command in the chat, and pushes code and result to its branch after each task. |

### The six rules

1. **The queue is fixed.** Setup writes every packet, in order. Nobody running the release adds, splits, re-scopes or reorders work. A plan is **finished** when every packet in it is Done or Parked.
2. **Proof runs where the code is written, and is pushed with it.** Every packet names one **Proof:** command. The packet runs it in its own ChatGPT chat (Sol in its own sandbox) and pushes to its branch on GitHub after each task. The commit that finishes the packet carries the result as its last line: `Proof: <command> — PASS <summary>`. That pushed line on the head is the proof, and nobody re-runs it. Nothing runs on a machine we set up, and nobody dispatches hosted CI.
3. **Every loop has a cap.** At the cap, mark the item **Parked**, post one line saying why, and move on. Parked work waits for the owner; everything else keeps moving.
4. **Park, don't ask.** A question this section doesn't answer is parked, never debated. Nobody waits for an answer.
5. **Replace once, then park.** A silent packet chat or manager is resumed or nudged once, then replaced once. A second need parks it. The state is on GitHub, not in the chat.
6. **A missed check isn't made up.** If your scheduled check didn't fire, run the loop once now; don't backfill.

### Never, at any level

- Write evidence files, receipts, audits, readbacks, summaries or re-verifications. A one-line board comment is the whole record.
- Clone, build or run tests outside a packet chat, dispatch hosted CI, or collect proof of any other kind.
- Edit plans, skills, this section or `releases/16.md`. A Luna edits only `tasks.md` Progress ticks.
- Start a new plan, investigation, review or document.
- Rebase, force-push, or create a branch outside the table below.
- Spend money, or use the owner's machine or media.

### Branches

| Branch | Who creates it | Who merges into it |
|---|---|---|
| `release/16/main` | Setup, once | the Lead, when a plan is finished |
| `release/16/plan-<PP>` | Setup, once | a Luna on a valid PASS; the Lead, merging `release/16/main` in when the plan is finished |
| `p<PP>/<packet-id>` | the packet chat, from its plan branch's head | nobody: it is the PR's head |

Merge, never rebase. A PR always targets its plan branch. Push after each task. Before posting READY, the packet merges its plan branch's head in, runs the Proof, and pushes.

### Packet states

| State | Set by | When |
|---|---|---|
| Queued | Setup | written, waiting its turn |
| Running | the manager | its chat has started; Rework 1 and 2 count as Running |
| Ready | the packet | it posted READY, and its head commit ends with a PASS line |
| Rework 1, Rework 2 | a Luna | the PASS wasn't valid, or the result was FAIL |
| Sol | the Lead | it failed after Rework 2, or posted BLOCKED; Sol has one try, and the manager leaves it alone |
| Done | a Luna | a valid PASS, merged into the plan branch |
| Parked | whoever hits a cap | it frees its slot, and the Luna parks each packet that depends on it |

**Every park is one comment on the plan's board:** `PARKED <packet or plan <PP>>: <reason>`. A parked plan gets no new packets.

The live state is the newest STATUS on each plan's board. Each role's own last STATUS is its memory: it carries what was nudged, resumed and replaced. Nobody keeps a second copy.

### Setup (once, before leaving it running)

The owner does this with a planning session she chooses, such as the one that wrote this section; no running role does it. Running Setup again is the only way to change the run.
1. Choose the plans for this run. Take only plans whose owner decisions are answered and whose packets can all be proved on CPU inside a chat. Everything needing real hardware, a real install or the network stays out.
2. For each plan, write every packet under `releases/16/packets/R16-P<PP>-<nn>.md`. Each packet has:
   - one contract, about three hours;
   - **Route** and **Depends** (earlier packets of the same plan only);
   - **May touch** and **Must not touch**;
   - **Files to load:** everything the chat needs to run the proof;
   - one **Proof:** command that runs only the narrow tests of the code this packet changes: its own module's tests and the new ones it writes, never a broad suite or an external or integration test. It runs in a chat with no network, on CPU, in under 10 minutes.
   Packets that touch the same file get a Depends link. Plans in one run touch no file in common.
3. Write each plan's queue table below, in dispatch order, and order the Plans table.
4. Cut the branches, open one board per plan (`board: release 16 plan <PP>`) and the Lead's board, and record each plan's Run start naming the Lead.
5. Start the Lead. The earlier Release 16 Lead (`session_011EzfW1C63rxLXsL6TkHHVV`) stands down.

### Plans

**Active at once:** at most four plans. The first manager's startup check measures how many ChatGPT chats the account runs at once; four plans need about twelve, so if it's fewer, run as many plans as that number divided by three allows. When a plan finishes or is parked, the Lead starts the next one in this table.

| Order | Plan | Board | Manager | State |
|---|---|---|---|---|
| — | chosen in Setup | — | — | — |

### Queues

One table per plan, written in Setup: Packet, Route, Depends, Proof. None is written yet.

### The Lead — every hour

**Job:** run the plan loops through Lunas, act on their flags, and merge finished plans. Nothing else.

1. **Read** your own last STATUS, and new comments on your board.
2. **Send one Luna per active plan,** all at once, each with the plan loop brief below and that plan's last result line. Wait for each one's single result line. A Luna that returns nothing in 30 minutes leaves that plan's line as it was, with `no-result` raised by one; at `no-result 2`, park the plan. A result resets it to 0.
3. **Act on each flag** in the results:
   - `SOL <packet>` → post `SOL <packet>` on the plan's board, then send one Sol with the Sol brief below;
   - `REPLACE manager <PP>` → replace that manager, once, and add `manager replaced` to its line; if it was already replaced, park the plan;
   - `FINISHED <PP>` → merge `release/16/main` into the plan branch, then the plan branch into `release/16/main`. If either won't merge cleanly, park the plan. Then start the next plan in the Plans table, with the manager start message.
4. **Parked:** copy any new Parked lines into your STATUS, under "for the owner". Don't solve them.
5. **Post** one STATUS on your board, then stop until the next check:

   ```text
   STATUS r16-lead | <each active plan's last result line, with no-result <n> and manager replaced if so> | … | sol: <packet and time sent, or none> | merged to release/16/main: <plans or none> | for the owner: <parked lines or none>
   ```

**Never:** read code, diffs or logs yourself, run tests, write or reorder packets, answer technical questions, or change a plan.

### Plan loop (the brief each Luna gets)

```text
You are running one check of the Release 16 plan loop for Plan <PP>, on board <issue URL>. Follow releases/16/run.md, section "Delivery", "Plan loop" on astrid-dev main. Do only these steps, then return one line.
1. Your last result line was: <the Lead pastes it, or "none">. Read the board's comments after its cursor, or the whole board if there is none.
2. For each READY <repo> <PR> <head>:
   - every file the PR changes is in the packet's May touch and none in Must not touch;
   - the head commit's last line is `Proof: <the packet's own Proof command> — PASS …`;
   - the PR merges cleanly into release/16/plan-<PP>.
   All three hold: merge it, tick the packet's tasks.md Progress, and post DONE <packet> <merge sha>.
   Otherwise post on the board: REWORK <n> of 2 for <packet>: <which check failed, in one line>.
   Count that packet's REWORK and SOL posts on the board: after Rework 2, flag SOL <packet> instead; after a SOL post, post PARKED <packet> instead.
3. Each BLOCKED: flag SOL <packet>, unless the board has a SOL post for it, in which case post PARKED <packet> with its question. A SOL post over 2 hours old with no READY after it: post PARKED <packet>: Sol didn't finish.
4. Each PARKED packet: post PARKED for every packet whose Depends includes it.
5. The manager's last STATUS is over 2 hours old: post the nudge on the board, unless your last result line says manager nudged, in which case flag REPLACE manager <PP>.
6. Every packet is Done or Parked: flag FINISHED <PP>.
Return exactly: plan <PP>: queued <n> running <n> ready <n> done <n> parked <n> manager <ok|nudged> | flags: <SOL …, REPLACE …, FINISHED …, or none> | cursor: <last comment id>.
Never run tests, read beyond these steps, or write anything else.
```

### Sol brief (one try per packet)

```text
You get one try at Release 16 packet <packet> (releases/16/packets/<id>.md on astrid-dev main), on branch p<PP>/<id>, PR <PR>, board <issue URL>.
Reason: <failed after Rework 2: the last REWORK line | BLOCKED: the question>.
Make the packet's Proof command pass, editing only files in its May touch. Merge release/16/plan-<PP>'s head in, run the Proof command once in your own sandbox, and push a commit whose last line is `Proof: <command> — PASS <summary>`.
Then post READY <repo> <PR> <head>. If you can't do it inside May touch, post PARKED <packet>: <one-line reason>.
Don't do anything else.
```

### The manager — every hour

**Job:** start the next packet. You are a dispatcher, not a reviewer.

1. **Read** your own last STATUS, then new comments on your plan's board, after your cursor. Drop each packet posted as `PARKED`, `DONE` or `SOL` from your Running list: a SOL packet is Sol's, not yours. If the plan itself is parked, post a final STATUS and stop.
2. **Each REWORK** on the board: send it to that packet's chat. If that chat won't load, use a new chat at the PR's head.
3. **Each Running packet** with no commit and no post for 3 hours:
   - send the resume message;
   - if it was already resumed, replace the chat, once;
   - if the replacement goes silent too, post `PARKED <packet>: silent after replacement`.
4. **Free slots:** at most three packets per plan Running. A replaced chat counts as closed; if the account refuses a new chat, wait for the next check. Fill them with Queued packets, in queue order, whose Depends are all Done. Each packet gets a NEW ChatGPT chat in its Route's mode (N High, X Extra High, S Pro), with the packet start message, named `r16-P<PP>-<nn>-<n>`. Your first packet goes alone, until it posts its first STATUS.
5. **Post** one STATUS, then stop until the next check:

   ```text
   STATUS r16-p<PP>-manager | running: <ids> | next: <id> | started: <ids or none> | resumed ever: <ids> | replaced ever: <ids> | cursor: <id>
   ```

**Never:** edit the repository, merge, judge code, answer a packet's question, or start packets out of order.

### Fixed messages

Fill the `<…>`. Never write a different one.

- **Nudge:** `Check-in missed. Run your loop in releases/16/run.md "Delivery" now and post STATUS.`
- **Resume (manager to packet):** `Resume <packet>. Your branch is p<PP>/<id> at <head>. Read the board for messages to you, continue, and end with READY.`
- **Replace (Lead to manager, or manager to packet):** start a fresh session with that role's start message, adding: `You replace <old session>. The state is on <board>, from comment <cursor>. Don't redo Done work.`

### Lead start message

The owner pastes this after Setup, or into a fresh session to replace a stopped Lead.

```text
You are the Lead for Release 16 of Astrid (mailbox r16-lead). Your whole job is the Lead loop in releases/16/run.md, section "Delivery: Lead and managers", on astrid-dev main. Run it every hour with your own scheduled task, at a minute other than :00 or :30, and never do anything that section doesn't list.
Now start the manager for the first plan in its Plans table: create the session in my Codex account and send it the manager start message. When its startup STATUS gives the chat limit, start the next plans' managers, up to the number active at once. If you replace an earlier Lead, start no managers: continue from its last STATUS. If a session won't take it as my message, post the text on your board for me to paste.
You may, without asking me:
- send Luna helpers with the plan loop brief, and Sol helpers with the Sol brief;
- create, nudge and replace manager sessions as the section says;
- merge finished plans into release/16/main as the section says.
Everything else is parked for me.
```

### Manager start message

```text
You are the manager for Release 16 Plan <PP> (mailbox r16-p<PP>-manager). Your board is <issue URL>, and the Lead is r16-lead. Your whole job is the manager loop in releases/16/run.md, section "Delivery: Lead and managers", on astrid-dev main, over the Plan <PP> queue in that section. Run it every hour with your own scheduled task, at a minute other than :00 or :30, and never do anything that section doesn't list.
Startup: post one STATUS saying how many ChatGPT chats the account can run at once, and whether High, Extra High and Pro are offered.
Start each packet in a new ChatGPT chat with this message, filled in:
"You are implementing ONE packet for Release 16: releases/16/packets/<id>.md on astrid-dev main. Board: <issue URL>; you are r16-<id>-<n>. Load the packet's Files to load. Branch p<PP>/<id> from release/16/plan-<PP>'s head, or continue on it and its draft PR from their head if they already exist, and edit only files in the packet's May touch. Push to the branch after each task. Open a draft PR into release/16/plan-<PP> and post an early STATUS once it's open. Run the packet's Proof command here in this chat: only the narrow tests of the code you changed, never a broad suite. When it passes, merge the plan branch's head in, run it again, push a commit whose last line is `Proof: <command> — PASS <summary>`, post READY <repo> <PR> <head>, and stop. If you can't run the Proof here, or can't do the packet inside May touch, post BLOCKED once with the reason and stop. Do not merge or start another packet."
You may start, resume and replace packet chats as the section says, and comment on the board. Nothing else.
```

### The owner's check-ins

Once a day, read the newest STATUS on `board: release 16 lead`. "For the owner" lists everything parked. If that STATUS is over 2 hours old, the Lead has stopped: paste the Lead start message into a fresh session, adding the Replace line; it starts no new managers. Answer parked items there, or run Setup again to change the run.

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
