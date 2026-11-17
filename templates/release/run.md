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
| [RNN-PXX-01](packets/RNN-PXX-01.md) | <tasks.md IDs> | Ready | — | <next action> |

Each packet is a short, stable Markdown assignment at `releases/NN/packets/<packet-id>.md`, including its source tasks, up-to-3-day estimate, outcome, dependencies, inherited proof/permissions and handoff recipient ([format](../../skills/astrid-dev-lead/workstreams/multi-manager-release.md#packet-format)). The table tracks Ready / Running / Review / Blocked / Done **handoffs**, not engineering completion; the plan's `tasks.md` remains authoritative. Delete this section when dispatch is not used. Link an existing cross-session mailbox issue here when needed, rather than creating another.

### Waiting on the owner

- <decision, with the recommendation>; or "nothing".
