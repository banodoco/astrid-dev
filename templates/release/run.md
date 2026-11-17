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

| Packet | Plan tasks | Estimate (human days) | Handoff | Session | Next action / evidence |
|---|---|---:|---|---|---|
| <release-plan-sequence> | <links to tasks.md rows> | <up to 3> | Ready | — | <next action> |

Handoff is Ready / Running / Review / Blocked / Done. This is not another task checklist: plans' `tasks.md` records engineering completion. Delete this section when dispatch is not used. Link the single cross-session mailbox here if one is needed.

### Waiting on the owner

- <decision, with the recommendation>; or "nothing".
