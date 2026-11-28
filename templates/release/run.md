# Release NN — run board

The live state of the Release NN run. It's rewritten at every check-in. The brief (`releases/NN.md`) holds intent and approach; `decisions.md` holds dated rulings (append-only); `tests.md` holds the test gate.

## Now (HH:MM UTC, day DD Mon)

One or two sentences: where the release stands, and the next thing that matters.

### Boards

Every project's board is the astrid-dev issue titled `board: release NN ...` ([rules](../../agent/shared/run-contract.md#coordination-boards-and-check-ins)); [list them](https://github.com/banodoco/astrid-dev/issues?q=is%3Aissue+is%3Aopen+in%3Atitle+%22board%3A+release+NN%22).

### Timeline to publish: <day DD Mon, HH:MM UTC>

| When (UTC) | Milestone | Owner | Status |
|---|---|---|---|
| <when> | <what lands, and its proof> | <lane or session> | <state> |
| **<when>** | **Cut line:** <what must be done>. If it isn't, ship without <what> | release manager | — |
| **<when>** | **Freeze** the candidate; final frozen CI head | release manager | — |
| **<when>** | **Publish**, with the owner's go | release manager | — |

### Qualification

The Qualifier's bar and coverage map are `releases/NN/qualification.md` ([workstream](../../agent/shared/release-qualification.md)).

### Issue list

- Brief: `releases/NN.md` → Issues; last pulled: <date or not yet>.

### Lanes

| Lane | Session | Brief | State |
|---|---|---|---|
| <lane> | <session id> | `briefs/<lane>.md` | <one line> |

Each lane's launch is in its brief ([lane template](lane.md#launch)); packet handoff state lives on the lane board and in each plan's `tasks.md`.

### Waiting on the owner

- <decision, with the recommendation>; or "nothing".

## Standing rulings

Rulings the Lead has made that recur, each with the decision that set it. Read before acting. A ruling not listed here was a one-off and binds no other packet.
