# Release 16 — run board

The live state of the Release 16 run, rewritten at each check-in by the release manager. The [brief](../16.md) holds intent, included plans, branches and issues; each plan's `tasks.md` holds its progress.

## Scope change — 25 November 2026

The owner now places the full Plan 91 green programme in [Release 17](../17.md), not Release 16. The existing plan branch, packet names, mailbox, evidence and active authority below are preserved; nothing is deleted, renamed, force-pushed or merged by this scoping change. **Do not land Plan 91 into release/16/main.** Before another target-dependent dispatch or landing, the existing Lead and Plan 91 orchestrator must record a coordinated handoff, confirm in-flight work, and rebind destination, branch and proof on the Release 17 base. Until then use the existing lane only for already-authorized bounded work on its retained branch; do not start a competing lane or treat the historical launch message below as fresh authorization. The Release 17 brief is the intended destination, and the older dispatch section remains the record of the original run.

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
Follow agent/roles/orchestrator/multi-manager-dispatch.md in banodoco/astrid-dev, with the orchestrator as "the Lead".
Read releases/16/run.md on main, section "Plan 91 dispatch", then again at every hourly check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1826, format in its first post.
First do the manager startup checks (Release 15's "Manager startup checks" for Plans 87 and 89, run against #1826, for astrid-agent and astrid-dev) and post one STATUS with each result. Dispatch nothing until the orchestrator's DECISION answers it.
Then give each Ready packet a FRESH ChatGPT session in the mode its packet's Route sets (N High, X Extra High, S Pro), with the workstream's packet start message, naming the session r16-P91-<nn>-<n>. Dispatch R16-P91-01 alone first.
Every hour: read the mailbox to the last page, check every open packet, run the parallelism pass (start every Ready packet with no unmet dependency and no file conflict with a Running one, up to five in Running or Review), resume or replace stalled sessions, pass submissions and READY-PROOF posts to the orchestrator, and post one STATUS.
You may start, resume, stop and replace packet sessions and comment on the mailbox. You may not merge, edit the repository, approve anything or dispatch hosted CI. Send anything reserved to the owner to the orchestrator.
If a check fails, say which manual step the owner must do instead of promising automation.
```
