# Release NN — run board

The live state of the Release NN run. It's rewritten at every check-in. The brief (`releases/NN.md`) holds intent and approach; `decisions.md` holds dated rulings (append-only); `tests.md` holds the test gate.

## Now (HH:MM UTC, day DD Mon)

One or two sentences: where the release stands, and the next thing that matters.

### Timeline to publish: <day DD Mon, HH:MM UTC>

| When (UTC) | Milestone | Owner | Status |
|---|---|---|---|
| <when> | <what lands, and its proof> | <lane or session> | <state> |
| **<when>** | **Cut line:** <what must be done>. If it isn't, ship without <what> | release manager | — |
| **<when>** | **Freeze** the candidate; final frozen CI head | release manager | — |
| **<when>** | **Publish**, with the owner's go | release manager | — |

### Issue list

- Brief: `releases/NN.md` → Issues; last pulled: <date or not yet>.

### Lanes

| Lane | Session | Brief | State |
|---|---|---|---|
| <lane> | <session id> | `briefs/<lane>.md` | <one line> |

### Dispatch queue (only when using the Lead's multi-manager workstream)

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| `packets/RNN-PXX-01.md` (link when created) | <tasks.md IDs> | Ready | — | <next action> |

Each packet is a short, stable Markdown assignment at `releases/NN/packets/<packet-id>.md`, implemented in **one fresh ChatGPT session**, including its source tasks, up-to-3-day estimate, outcome, dependencies, inherited proof/permissions and handoff recipient ([format](packet.md)). The table tracks Ready / Running / Review / Blocked / Done **handoffs**, not engineering completion; the plan's `tasks.md` remains authoritative. Delete this section when dispatch is not used. Link an existing cross-session mailbox issue here when needed, rather than creating another.

### Waiting on the owner

- <decision, with the recommendation>; or "nothing".

## Standing rulings

Rulings the Lead has made that recur, each with the decision that set it. Read before acting. A ruling not listed here was a one-off and binds no other packet.

## Orchestrator launch message

Only when dispatching packets. The owner pastes it into the Orchestrator's own session; fill each `<…>`.

```text
You are the Orchestrator for Release <N>, reporting to the Lead (mailbox name <lead name>).
Follow skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md in banodoco/astrid-dev.
Read releases/<N>/run.md at <SHA>, then on main at every hourly check. Ready rows link the packets.
Mailbox: <issue URL>, format in its first post. Your mailbox name: <name>.
First do the board's startup checks and post one STATUS with each result; dispatch nothing until
the Lead's DECISION answers it. Then give each Ready packet a FRESH ChatGPT session in the mode its packet's Route sets (N High, X Extra High, S Pro),
with the workstream's packet start message. Every hour: read the mailbox, check every open packet,
resume or replace stalled sessions, pass submissions to the Lead, and post one STATUS.
You may start, resume and replace packet sessions and comment on the mailbox. You may not merge,
edit the repository or approve anything. Send anything reserved to the owner to the Lead.
If a check fails, say which manual step the owner must do instead of promising automation.
```
