# Lane briefs — findings and design (28 Nov 2026)

[Plan](../plan.md) · [Tasks](../tasks.md)

Gathered by three read-only inventories of astrid-dev on 28 November 2026 (release records; role and workstream instructions with templates; checks and linkage). The owner's direction followed in the same session. Line references are to astrid-dev `main` at `541ced23`.

## Findings

### Dispatch notes are hand-written again and again

Eight dispatch-like sections exist:

| Release | File and section |
| --- | --- |
| 14 | `releases/14/run.md`: the dispatch queue and launch messages, lines 35–302 |
| 15 | `releases/15/run.md`: Plan 56, Plans 87 and 89, Plan 82, qualification |
| 16 | `releases/16/run.md`: H3 lane; Delivery (Lead and managers); Plan 91 |
| 13 | `releases/13/generation.md`: per-manager "START HERE" blocks (the pattern's precursor) |

They share these fields, counted across the eight:

| Field | Count |
| --- | ---: |
| Branch rules | 8 |
| Routes and modes | 8 |
| Mailbox or board | 7 |
| Standing rulings | 7 |
| In-flight cap | 7 |
| Startup checks | 7 |
| Queue table | 6 |
| Roles and sessions | 6 |
| Owner-only list | 6 |
| READY-PROOF protocol | 6 |
| Launch message | 5 |
| "First packet alone" | 5 |
| Hourly cadence | 5 |
| CI-sharing rules | 4 |

Later sections say "works exactly like" an earlier one, and list only the differences.

### Sequencing and spans

- Sequencing across plans has been written three ways:
  - a "Starts after" column (`releases/16/run.md` Plans table);
  - a numbered landing order (`releases/15/run.md`);
  - per-row "blocked on" text.
- Work spanning releases is recorded with "superseded" notes and pointers (Plans 56, 91, 82, 87 and 89), never with one record.

### No templates, no checks

- `templates/release/` has only `run.md` and `packet.md`. There is no lane brief, dispatch note or launch-message template.
- `orchestrator.md` refers to "dispatch notes in tasks.md", which do not exist.
- No check reads `run.md`, `briefs/` or `packets/`.
- Release membership is one-way: the release brief's Included plans, with the back-reference generated.
- No dependency graph is parsed.

### Eleven contradictions in the role documents

1. **Lane** is defined three ways:
   - "a stream of work within a release, with its own session and brief" (glossary);
   - "the plans one orchestrator answers for" (leader);
   - "a session with a manager and its brief" (release workstream).
2. **Accountability:** the lane orchestrator "answers for it finishing" (leader lane workstream), but the run contract makes the manager accountable and the orchestrator an advisor.
3. **The Lead's part:** a lane orchestrator may take the Lead's part for its plan (multi-manager release), against the Lead being the single accountable agent elsewhere.
4. **Default manager type:** a Codex manager by default, against Codex workers by default.
5. **Who writes `Run start`:** the orchestrator, the Lead (twice), and the owner starting the run.
6. **Who sends the launch:** the owner must paste it, since a session's own message is peer data; against the orchestrator sending start messages from the owner's account.
7. **Where rulings live:** "one home per ruling" in the run board, against putting answers into `tasks.md` or `Run start`.
8. **The advisor:** the orchestrator, against a fresh high-judgment session, against a lane orchestrator on route X.
9. **Merge rights** of a lane orchestrator versus the run contract's auto-merge rules.
10. **Duplicated rules:** `Run start` rules in four places, launch-message rules in four, the parallelism pass in two.
11. **Dangling references:** "dispatch notes in tasks.md"; `releases/<N>/lead/`.

## Design

**A lane is the set of plans one orchestrator runs, possibly across releases.** It is described by one lane brief at `releases/<N>/briefs/<lane>.md`, in the release where it starts. A later release links the same brief from its run board and lists its plans in its own Included plans. Nothing is copied.

### Lane brief fields

| Field | Holds |
| --- | --- |
| Header | `Lane`, `Releases`, `State` (prepared, running, paused or done), `Orchestrator`, `Reviewer`, `Board` |
| Outcome | The end state in a few sentences |
| Plans and order | Plan, Release, Starts when (the joins), Branches |
| Queue | Links to each plan's execution-units table, never copied |
| How it runs | One of two options: a Claude-hosted orchestrator with a manager, or fresh ChatGPT packets. Each states dispatch, cap, proof, reviews, merges and check-ins |
| Roles | Orchestrator, reviewer, owner |
| Standing rulings | Dated and append-only; the one home for this lane's rulings. Release-wide rulings stay in `run.md` |
| Context | Decisions and their reasons, with links |
| Cut line and coordination | What slips first, and which other lanes touch the same code |
| Owner only | What the orchestrator must bring to the owner |
| Launch | The owner's one line |
| Status | A pointer to `release status` and the board; never a second copy |

### One home each

- **`Run start`:** each plan's line points to its lane brief, and the owner's go is recorded once, on the brief.
- **Accountability:** the orchestrator answers for its lane.
- **Launch:** the owner always sends it.

### The Lead, with the owner

1. The Lead proposes two or three ways to group the release's plans into lanes. For each option it gives the plans together and their order, which plans run alone and why, the orchestrator route, the cut line, cross-lane coordination and the attention cost.
2. It recommends one.
3. The owner chooses.
4. The Lead records the agreed split on the run board.
5. The Lead writes the briefs.
6. The owner gives the go on each brief and sends its launch.

Re-laning happens only with the owner, at real changes: a plan finishes, a lane stalls, or scope moves.

### The orchestrator and the manager

- **Orchestrator:** reads only its brief, decides within it, and comes to the Lead or owner only at the brief's listed points.
- **Manager:** unchanged apart from taking its authority and rulings from the brief.

### What CI checks

**Checks:**
- the brief's fields are present;
- each listed plan exists and is in the named release's Included plans;
- a plan belongs to at most one active lane.

`release status` gains a lane column, and prompts when a released plan has no lane.

**Does not check:** rulings, context or how-to-run text.

### Not added

- a new "batch" noun or folder;
- a scheduler;
- generated status inside briefs;
- rewriting historical dispatch sections.

## Worked example

[releases/16/briefs/h3.md](../../../releases/16/briefs/h3.md) was written on 28 November 2026, before this template existed. It is the H3 programme's lane: Plans 66, 68, 70 and 67 in Release 16, then Plan 107 in Release 17.
