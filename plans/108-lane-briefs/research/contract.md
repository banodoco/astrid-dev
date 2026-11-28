# Lane briefs — the contract (L-2, 28 Nov 2026)

[Plan](../plan.md) · [Tasks](../tasks.md) · [Findings and design](design.md)

This note settles the lane-brief contract that L-3 to L-9 (and H-1) apply. It starts from [design.md](design.md), uses the name "lane", not "batch" (the owner decided D1 = lane, recorded in inputs.md via PR #2072), and adopts owner decision D2 (the Lead divides each release into lanes *with* the owner). Where this note and design.md differ, this note wins. The owner widened L-2 to cover the brief ladder (§1), one board per lane and no separate manager briefs (§3), and to note task L-9 (§3). Each later task applies its rows here and makes no new design choice; a gap goes to the Plan 108 manager as a question. The manager adds the L-9 card (path `agent/shared/workstreams/start-session.md`, Depends on L-2), makes L-4 and L-5 depend on L-9 or land with it, and extends L-R to L-3 to L-9.

## 1. What a lane is, and where its brief lives

**A lane is the set of plans one orchestrator session runs and answers for, possibly across releases.** This is the one definition. It goes in `agent/shared/glossary.md`, and every other file links to it.

- **One brief per lane,** at `releases/<N>/briefs/<lane>.md`, where `<N>` is the first release the lane runs in and `<lane>` is a lowercase slug (`[a-z0-9-]+`).
- **A later release adds nothing to the brief's folder.** It lists the lane's plans for that release in its own `## Included plans`, and links the same brief from its run board's Lanes table. Nothing is copied.
- **Every plan in a release belongs to exactly one lane.** Small independent plans may share a lane (leader.md's existing grouping rules stand). A **standing lane** is an ordinary lane whose Plans table grows during the release. A plan outside any release (astrid-dev-only) may run without a lane, under its own `Run start` line. A release plan may run under direct release leadership without a lane while the Lead and owner have not laned it; `release status` prompts for it.
- **Lane brief or not:** a file in `releases/*/briefs/` is a lane brief exactly when it has a header line starting `**Lane:**`. Other files there (reviewer briefs, the standby Lead's brief, fixed messages, and older manager briefs from before §3, except the h3 ones H-1 supersedes) are unaffected.

### The brief ladder

Four rungs, each linking the rungs next to it:

1. **Release brief** (`releases/<N>.md`, with its run board `releases/<N>/run.md`): what the release ships, its Included plans, landing order, qualification and publication, the lanes it uses, and release-wide rulings.
2. **Lane brief** (`releases/<N>/briefs/<lane>.md`): which plans one orchestrator runs and in what order, how they run, who may do what, the owner's go and limits, and the lane's rulings.
3. **Plan** (`plans/<PP>-<slug>/plan.md` with its `inputs.md`): one plan's scope, end state, decisions and evidence; in a lane, its `Run start` is a pointer to the lane brief.
4. **Task card** (a row of the plan's `tasks.md`): one unit's outcome, route, dependencies, May touch, focused proof and progress.

Each rung has one template, one writer and one ready-to-start check:

| Rung | Template | Writer | Ready-to-start check |
| --- | --- | --- | --- |
| Release brief | [releases/TEMPLATE.md](../../../releases/TEMPLATE.md), with its run board from [templates/release/run.md](../../../templates/release/run.md) | The Lead (whoever starts the release) | `python3 scripts/astrid_dev.py check` passes, and the owner's go is recorded (each plan joins by a PR the owner approves) |
| Lane brief | [templates/release/lane.md](../../../templates/release/lane.md) | The Lead, with the owner | The L-7 `lane-briefs` check passes; State `prepared` until the go; `**Go:**` recorded and State `running` before the launch is sent |
| Plan | [templates/project/plan.md](../../../templates/project/plan.md) and [inputs.md](../../../templates/project/inputs.md) | The plan's author | The plan and inputs checks in `astrid_dev.py check` pass, and `inputs.md` has its `Run start` line (in a lane, the pointer to the brief) |
| Task card | A row of the execution-units table in [templates/project/tasks.md](../../../templates/project/tasks.md) | The plan's manager (in a lane, the orchestrator) | Its dependencies are merged and its card fields are complete: one bounded outcome, route, dependencies, scope and focused proof |

**The principle: very minimal and elegant.** The role skill says how, the brief says what, and the launch line only connects them. Anything that should survive a session replacement belongs in the brief. Authority lives in the brief on `main`; the launch line only points to it. **L-9's start-session workstream runs the ready-to-start check of the session's rung before starting any session** (§3).

**Each fact has one home on this ladder, at the rung it belongs to, and is never copied down.** A lower rung links the rung above for anything it needs from it (a lane brief links the release's Included plans; a card links its plan's decisions), and a higher rung links down rather than restating (a lane brief's Queue links `tasks.md`; it never copies a card).

## 2. The brief's fields

L-3 writes `templates/release/lane.md` with exactly these fields, in this order. **Required for L-7** means the check fails without it.

### Header (before the first `## `), one `**Key:** value` line each

| Field | Value | Required for L-7 |
| --- | --- | --- |
| `**Lane:**` | The slug; equals the file name without `.md` | Yes (the marker) |
| `**Releases:**` | One or more release numbers, first one first (for example `16, continuing in 17`). The first equals `<N>` in the path | Yes |
| `**State:**` | Starts with one of `prepared`, `running`, `paused` or `done`; free text may follow | Yes |
| `**Go:**` | `Pending` while prepared; otherwise the owner's go: date, the owner, and a link to where the owner gave it | Yes. It may start `Pending` only when State is `prepared` |
| `**Orchestrator:**` | Route (`X` or `S`, chosen by [leader.md](../../../agent/roles/leader.md#divide-the-release-into-lanes)) and the session id once started | Yes |
| `**Reviewer:**` | The high-judgment binding and its brief | Yes |
| `**Board:**` | The board issue title, `board: lane <lane>` (§3), and its link once opened | Yes |

### Sections, each a `## ` heading with exactly this text, non-empty

| Section | Holds | Required for L-7 |
| --- | --- | --- |
| `## Outcome` | The end state, in a few sentences | Yes |
| `## Plans and order` | A table with columns exactly `Plan \| Release \| Starts when \| Branches`. Plan links `plans/<PP>-<slug>/plan.md`; Release is one of the header's Releases; Starts when holds the joins (the units that must merge first); Branches names repository, branch and base | Yes, with the table checks in §5 |
| `## Queue` | Links to each plan's execution-units table in `tasks.md`; never a copied table | Yes: at least one `tasks.md` link and no table rows |
| `## How it runs` | `**Option:** hosted` or `**Option:** packets` (§4), then six labelled bullets: `**Start.**` (startup checks), `**Dispatch.**` (cap, first unit alone), `**Proof.**`, `**Reviews.**`, `**Merges.**` (including the release gate), `**Check-ins.**` | Yes: the Option line and the six labels present; their text is not checked |
| `## Roles` | Orchestrator, its manager or packet sessions, reviewer, advisor, owner; and what the orchestrator **may do without asking** | Yes |
| `## Standing rulings` | Dated, append-only; the one home for this lane's rulings (§3) | Yes (may say "None yet") |
| `## Context` | Decisions and their reasons, with links | Yes |
| `## Cut line and coordination` | What slips first; other lanes touching the same code or fixture; CI sharing | Yes |
| `## Owner only` | What the orchestrator must bring to the owner | Yes |
| `## Launch` | The owner's one-line launch, in one fenced `text` block, carrying only the three parts below | Yes: exactly one fenced block |
| `## Status` | A pointer to `release status <N>` and the board; never a copy | Yes |

**The fixed launch line** has exactly three parts, and the template's Launch block carries only these:

1. **The skill:** the role's skill to follow, and how to install the skills.
2. **The brief:** the path of its brief, in that role's fixed place (for a lane orchestrator, `releases/<N>/briefs/<lane>.md` on banodoco/astrid-dev `main`).
3. **The creator:** the session that created this one, and its sign-off name, so the new session knows whom it answers to.

```text
Follow the astrid-dev-orchestrator skill (install the skills with python3 scripts/astrid_dev.py skills install from a banodoco/astrid-dev checkout). Your brief is releases/<N>/briefs/<lane>.md on banodoco/astrid-dev main. Created by session <creator session id>, signing <creator sign-off>.
```

**Anything that should survive a session replacement belongs in the brief, never in the launch line.** So the orchestrator's own sign-off name (`<lane>-orchestrator`) goes in the brief's Roles, and "open the board first, then post one STATUS" goes in How it runs `**Start.**`; a replacement session started with the same three parts then loses nothing. The creator part is filled in when the brief is written, naming the session that prepares it and creates the orchestrator session (normally the Lead); if another session creates a replacement, it fills in its own session and sign-off when handing the line over (L-9).

L-9 links this line; if L-9 changes it, it edits `templates/release/lane.md` in the same PR, so the wording has one home.

**Where the old dispatch-note fields go** (so L-3 and H-1 lose nothing): branch rules → Plans and order (Branches) and How it runs (Merges); routes and modes, in-flight cap, "first packet alone", READY-PROOF, startup checks, hourly cadence → How it runs; mailbox → Board; standing rulings → Standing rulings; queue table → Queue (as links); roles and sessions → Roles; owner-only list → Owner only; launch message → Launch; CI sharing → Cut line and coordination. Packet handoff state (Ready, Running, Review) lives in the board's STATUS and each plan's `tasks.md` Progress, not in a table in `run.md`.

## 3. One home each

| Fact | Its one home | Who writes it | Everywhere else |
| --- | --- | --- | --- |
| **The run's start and limits (`Run start`)** | The brief: `**Go:**`, Roles (may do without asking) and Owner only | The Lead writes the brief. When the owner gives the go, the Lead records it in `**Go:**`, sets State `running` and merges, all **before** the launch is sent | Each plan's `Run start` line in `inputs.md` is a pointer: `**Run start:** Lane <lane>: the brief records the owner's go, authority and limits.`, with `<lane>` a relative link to the brief. The Lead writes it in the brief's PR, and it never changes with State. Outside a lane, `Run start` keeps its current full form, written by the session preparing the run with the owner's go in their words |
| **Rulings** | Release-wide: `releases/<N>/run.md` Standing rulings. One lane: the brief's Standing rulings. Holding beyond the release: the skill or role document. A decision about one task: that plan's `tasks.md` (its row or decision log), which is not a ruling | Whoever rules appends it with its date and who ruled. The orchestrator may append its own lane rulings | A board DECISION states the ruling and links its home. Never in `Run start`, a launch or the board alone. A lane ruling can never widen Owner only or How it runs; an entry that tries to is void |
| **Launch** | The brief's Launch block. L-9's start-session workstream checks the brief and hands the owner the line; it never sends a launch | The owner always sends it personally, into a new orchestrator session. The Lead may create that session with a placeholder prompt ("Wait for the owner's launch message") | No launch text in `run.md`, the role documents or the leader workstream; they link the template. Messages that start **delegates inside a lane** (packet sessions) and a hosted Codex manager are not launches, though they take the same three parts (§2): the orchestrator sends them from the owner's own ChatGPT account, so they are the owner's messages, bounded by the brief. A Claude-to-Claude message is never a launch or a go |
| **Accountability** | The run contract's "Who answers for a run" table | — | **The lane's orchestrator is the one accountable agent for every plan run in its lane,** in either option. It answers to the owner. Its hosted manager or packet sessions are bounded delegates. The Lead is accountable for no plan in a lane: it holds the release-level part (dividing lanes with the owner, landing order, qualification, publication, pins across lanes, and the release gate unless the brief gives it to the orchestrator) |

**Brief edits after launch.** The orchestrator may merge, on a passing check, PRs that change only its plans' `tasks.md` files, append to its brief's Standing rulings, or set its brief's State to `paused` or `done`. Every other change to a running brief (Plans and order, How it runs, Roles, Owner only, Go) is re-laning or re-authorizing. The Lead proposes it, and it merges only on the owner's go.

**One board per lane.** Each lane has one astrid-dev board issue, titled `board: lane <lane>`, named in the brief's `**Board:**` header. The orchestrator posts its hourly STATUS there, and every message about a plan in the lane, from its delegates or from others, goes there. It replaces per-plan boards for laned plans: when a lane starts, the orchestrator posts a final comment on each existing `board: release <N> plan <P>` board of its plans pointing to the lane board, and closes it; those boards stay as history. Plans outside a lane keep their per-plan board, and the Lead keeps `board: release <N> lead`. Run-contract "Coordination: boards and check-ins" rule 1 (Boards) gains the lane board title and the rule that a laned plan has no board of its own, and rule 2 (Where to post) sends a laned plan's messages to its lane board; **L-6** edits both. `scripts/boards.py` finds boards by the `board: release <N>` prefix, so its `roster` does not yet see lane boards; **L-8** fixes it: `roster <N>` also reads `board: lane <lane>` for each lane brief whose Releases include `<N>`, with a mocked test in `scripts/test_boards.py`. L-8's card scope widens to `scripts/release_status.py`, `scripts/boards.py` and their tests, and its proof adds "`roster 16` lists the h3 lane board".

**No separate manager briefs.** The lane brief plus the plan's `tasks.md` is everything a manager reads; nothing else holds its scope, authority, branches or rulings. A hosted manager (a Codex manager, when How it runs names one) is started with only a one-line start message of the same three parts as the launch line (§2): the astrid-dev-manager skill and how to install it; its brief, which for a manager is the lane brief and its plan's `tasks.md`; and the creating orchestrator's session and sign-off name. The Codex guide's start-up mechanics apply as before; nothing in the message restates the brief, and anything that should survive a replacement manager is in the brief. `agent/guides/codex-in-claude-cloud/manager-brief.md` stops being a per-run brief to copy and fill in: it keeps only what is the same for every Codex manager (workspace layout, route-to-model lines, the rules that differ under Codex, what to report), and the project-specific parts it used to carry come from the lane brief and `tasks.md`. Because Codex takes its authority only from its starting prompt, that start message names the brief whose Roles and Merges grant it.

**L-9, a shared start-session workstream** (a new task), is the one procedure for starting any session from a brief: validate that the new session's brief is on `main`, passes its check (for a lane brief, `lane-briefs`) and carries the owner's authority (for a lane brief, a `**Go:**` that is not `Pending` and State `running`), then give the three-part line (§2) pointing at it to whoever sends it: the owner, for a lane orchestrator (or any session the owner launches); the orchestrator, for a delegate it starts under its brief (§3, Launch row). **The Launch row above and the file moves below defer to L-9:** where L-9 settles how a session's start is checked and sent, its text wins over this note's, except that it cannot change who sends a launch or what counts as the owner's go, which stay as the Launch and Run start rows say; and L-3, L-4 and L-5 link L-9 rather than restating start steps.

**The advisor** (blocking questions) follows the chain and is named once, in the brief's Roles. A delegate asks the orchestrator. The orchestrator asks the Lead for release-level questions, and the reviewer binding, a fresh high-judgment session, for technical judgment beyond its own route. A lane orchestrator is never anyone's advisor except its own delegates'.

## 4. How it runs: two options

Each brief picks one, on its `**Option:**` line. A lane that needs both is two lanes.

| | `hosted`: Claude orchestrator running Codex workers by `codex exec` (Claude workers as fallback) | `packets`: fresh ChatGPT packets, pasted by the owner or started by the orchestrator only where an owner-signed-in route exists |
| --- | --- | --- |
| **Session** | One Claude cloud session is the orchestrator and holds the manager role for each running plan itself (at most two plans running at once; a third needs its own lane, per leader.md). Only when How it runs names a Codex manager is the manager a separate Codex process (the owner pastes that launch on their own computer; a cloud session cannot create or wake a signed-in Codex desktop manager) | One orchestrator session. A fresh normal ChatGPT session per unit, in its route's mode (N High, X Extra High, S Pro), pasted by the owner or started by the orchestrator only where an owner-signed-in route exists |
| **The manager** | By default the orchestrator manages each plan itself, dispatching each card to a **Codex worker** by its route (Claude subagents on the same routes if Codex is unavailable). This is the one statement in [codex-in-claude-cloud.md](../../../agent/roles/orchestrator/codex-in-claude-cloud.md#use-codex-from-claude-cloud). A **Codex manager** only when How it runs says so, with a one-line reason; it reads the lane brief and `tasks.md` and is started with a one-line start message pointing at them (§3) | None. The orchestrator writes each unit's packet at dispatch from its cards ([packet template](../../../templates/release/packet.md)); no packets are prepared ahead. Fixes are packet work: Claude sessions diagnose, review, prove and merge, but never write the fix |
| **Proof** | The card's focused proof in the session, and hosted CI as the final check | The author runs the focused proof and opens a PR into the plan branch. Green CI plus the shown proof is the evidence, and the orchestrator answers each READY-PROOF |
| **Merges** | Same in both: the orchestrator merges its own progress PRs and into its plan branches on green. Into `release/<N>/main`: the release gate the brief's Merges names, either `Lead` (the default) or `orchestrator, after any overlapping merge`, which the owner grants by their go on the brief | (same) |
| **Mechanics** | [orchestrator/lane-orchestrator.md](../../../agent/roles/orchestrator/lane-orchestrator.md) | [orchestrator/multi-manager-dispatch.md](../../../agent/roles/orchestrator/multi-manager-dispatch.md), its packet start message and proof turnaround |
| **Use when** | Any unit needs what a ChatGPT session cannot reach: an installed stack, a live machine or fixture, GPU or local measurement, a loop or taste plan worked in rounds; or the lane is astrid-dev-only | Every unit is self-contained: a card with outcome, May touch and focused proof that runs in the packet session or on hosted CI. The usual choice for wide, independent product-repository units |

## 5. What CI checks

**L-7 adds one check, `lane-briefs`,** in `scripts/records.py` (parsing) and `scripts/checks.py` (the check, `always`), over every lane brief (§1). It fails when:

1. **A field is missing:** any header field or section in §2 marked Required is missing or empty, or a header value, a Plans and order cell or the Launch block still holds a template placeholder (`<…>`); section prose is not scanned for placeholders. The same applies when the Option line or one of the six How it runs labels is absent, when Launch has no fenced block or more than one, or when Queue has no `tasks.md` link or holds a table row.
2. **A header value is malformed:** `Lane` differs from the file name; the first `Releases` number differs from the path's `<N>`; State does not start with one of the four values; Go starts `Pending` while State is not `prepared`; or another lane brief anywhere under `releases/*/briefs/` has the same Lane.
3. **A plan is unknown:** a Plans and order row's link does not resolve to an existing `plans/<PP>-*/plan.md`, or its Release is not in the header's Releases.
4. **A plan is not in the named release:** the plan is missing from that release's `releases/<R>.md` `## Included plans` (read with `records.release_brief`), or `releases/<R>.md` does not exist.
5. **A plan is in two active lanes:** across all briefs, a plan appears in more than one brief whose State is `prepared`, `running` or `paused`.
6. **A started lane's plan has no pointer:** for a brief whose State is `running` or `paused`, a listed plan's `inputs.md` `**Run start:**` line does not link that brief's path.

Each of the six failures gets one injected-failure test. Checks 2 (including the duplicate-Lane test) and 6 extend the L-7 card; the manager records this as a tasks.md ruling when L-7 is dispatched.

**L-7 also relaxes the astrid-dev-only `Run start` check.** `_active_plans_in_releases` in `scripts/checks.py` (lines 113-120) requires an active astrid-dev-only plan's `inputs.md` `**Run start:**` line to contain `owner-authorized`. L-7 lets it accept instead a `Run start` pointer to a lane brief whose State is `running`.

**L-8: `release status <N>`** shows a Lane column for each Included plan: the lane whose brief lists the plan with Release `<N>`, or `—`. For each Included plan with no lane, it prints one prompt line: `Plan <PP> has no lane: the Lead proposes lanes with the owner (agent/roles/leader.md#divide-the-release-into-lanes).` This is a prompt, not a failure: the exit code is unchanged.

**CI does not check:**
- the text of rulings, Context, Outcome, Owner only, Cut line or How it runs beyond the labels;
- the launch line's wording;
- whether Starts when joins name real units, or form a cycle;
- whether branches or SHAs exist;
- board, issue or session existence;
- whether a plan's units are done, or State is true;
- who edited which section of a brief;
- the Lanes table in `run.md`;
- briefs without the `**Lane:**` marker.

## 6. The eleven contradictions

Each row has one resolution and the task that applies it. "Link" means the other files replace their text with a link to the one home.

| # | Contradiction | Resolution | Applied by |
| --- | --- | --- | --- |
| 1 | **Lane** is defined three ways (glossary; leader; release workstream) | One definition (§1): the set of plans one orchestrator runs and answers for, possibly across releases, with one brief at `releases/<N>/briefs/<lane>.md`. The glossary holds it. In leader.md, "Divide the release into lanes" links it. In release.md, "Give each lane its own session, with a manager and its brief" becomes a link. The standing-lane entry says it is an ordinary lane | L-6 (glossary, release.md); L-4 (leader.md) |
| 2 | **Accountability:** the lane orchestrator "answers for it finishing", against the run contract's manager accountable and orchestrator advisor | In a lane, the orchestrator is the one accountable agent for every plan run, in either option; managers and packet sessions are bounded delegates (§3). The run contract gets a row "A plan in a lane" and drops the Lead-accountable fresh-packet row. "A manager in its own session" stays, for runs outside lanes. manager.md gets one line: "In a lane, the orchestrator answers for the run; you deliver your plan for it, under the brief. The lane brief and your plan's `tasks.md` are all you read; there is no separate manager brief." (§3) | L-6 (run contract, manager.md); L-5 (orchestrator.md "One exception" paragraph). L-6 also rewrites for lanes (in a lane: the orchestrator, under the brief) these run-contract sentences: the "Cheapest model first" paragraph ("In the fresh-session dispatch workstream, the Lead is the accountable agent…", which links the deleted multi-manager-release.md); the review-boundaries clause "…or under fresh-packet dispatch, takes it to the owner"; and the test-exception line "…the orchestrator, who may approve under the Lead's delegation" |
| 3 | **The Lead's part:** a lane orchestrator may take the Lead's part for its plan, against the Lead as the single accountable agent | Split by level, with no "taking a part". Plan level (packets, reviews, plan-branch merges, proofs) is always the orchestrator's; release level (lanes with the owner, landing order, qualification, publication, cross-lane pins, and the release gate unless the brief grants it) is always the Lead's. Delete "A lane can be the Lead for its own plan". Leader responsibility 2 names the lane's orchestrator, or the plan manager outside a lane | L-4 |
| 4 | **Default manager type:** Codex manager by default, against Codex workers by default | Codex workers are the default; a hosted Codex manager only by the brief's stated choice (§4). codex-in-claude-cloud.md stays the one statement. Remove "Host one Codex manager on Terra…" from the leader lane launch text, which goes with the launch move. L-4 notes that a hosted orchestrator holding the manager role takes the higher of the orchestrator and manager routes. A hosted Codex manager gets no separate brief: `manager-brief.md` keeps only the Codex mechanics, and the manager starts from a one-line start message pointing at the lane brief and `tasks.md` (§3); codex-in-claude-cloud.md's "Brief a manager as a manager" and the guide's start steps change to match | L-4 (leader text); L-5 (`orchestrator/codex-in-claude-cloud.md`, `agent/guides/codex-in-claude-cloud/manager-brief.md` and README); L-6 (`manager/whole-project.md` "Managing under Codex") |
| 5 | **Who writes `Run start`:** orchestrator, Lead (twice), owner | In a lane, the Lead writes the brief and each plan's pointer `Run start` line in one PR, and records the owner's go in `**Go:**` before the launch (§3). The orchestrator never writes `Run start`. Outside a lane, the session preparing the run writes it with the owner's go. The rule's one home is the run contract's "Who answers for a run", with the field list in `templates/project/inputs.md`, which gains the pointer form | L-6 (run contract, `templates/project/inputs.md`); L-4, L-5 (link) |
| 6 | **Who sends the launch:** the owner must paste it, against the orchestrator sending start messages from the owner's account | The owner always sends a lane's launch personally. Delegate start messages inside a lane (packet sessions) are sent by the orchestrator from the owner's ChatGPT account, bounded by the brief, and are not launches (§3). The run contract's authority paragraph states both, once. How a start is checked and handed over is L-9's start-session workstream; the owner still sends every launch, which this row defers to (§3) | L-6 (run contract); L-4, L-5 (link); L-9 (start-session workstream) |
| 7 | **Where rulings live:** one home in the run board, against answers in `tasks.md` or `Run start` | Four homes by reach (§3): release (`run.md`), lane (brief), beyond the release (skill), one task (`tasks.md`, a decision and not a ruling). Never `Run start`. Run-contract coordination rule 4 states this; lane-orchestrator.md's "written into `tasks.md` or the `Run start` line" becomes "the brief's Standing rulings" | L-6 (run contract); L-5 (lane-orchestrator.md); L-4 (leader "Rulings" paragraph) |
| 8 | **The advisor:** the orchestrator, a fresh high-judgment session, or a lane orchestrator on route X | The advisor follows the chain and is named once in the brief's Roles. Delegates ask the orchestrator; the orchestrator asks the Lead (release level) or the reviewer binding (technical judgment). A lane orchestrator advises only its own delegates (§3). Glossary "advisor" and lane-orchestrator.md's "with the Release Lead as advisor" opening change to match | L-6 (glossary); L-5 (lane-orchestrator.md "When to use") |
| 9 | **Merge rights** of a lane orchestrator against the run contract's auto-merge rules | One rule in the run contract. The accountable agent (the orchestrator in a lane) merges its plans' `tasks.md`-only PRs, its brief's ruling and State edits, and into its plan branches, on a passing check or green CI. Into `release/<N>/main`, the release gate named in the brief's Merges (Lead by default). Every other merge into `main` needs the owner's go | L-6 (run contract); L-5 (lane-orchestrator.md "Merge your own records" links it) |
| 10 | **Duplicated rules:** `Run start` in four places, launch messages in four, the parallelism pass in two | `Run start`: the run contract plus `templates/project/inputs.md`, with the rest linked. The brief ladder (§1): one rung per fact, in the release.md records table. Manager briefs: none per run; the lane brief and `tasks.md` hold it all, and `manager-brief.md` keeps only Codex mechanics (§3). Boards: one per lane, in run-contract rule 1 (§3). The start steps for any session live only in L-9's workstream. The lane launch lives in the lane template's Launch; the "Orchestrator launch message" section leaves `templates/release/run.md`, and orchestrator.md "The start message" is kept only for runs outside lanes. The packet start message stays only in multi-manager-dispatch.md. The parallelism pass lives in lane-orchestrator.md; the Lead's hourly pass keeps only cross-lane conflicts and links it | L-3 (`templates/release/run.md`); L-4 (leader lane procedure); L-5 (orchestrator.md, lane-orchestrator.md, `manager-brief.md`); L-6 (run contract, boards rules 1 and 2, the ladder in release.md); L-9 (start steps) |
| 11 | **Dangling references:** "dispatch notes in tasks.md"; `releases/<N>/lead/` | The orchestrator.md start message reads "start from the lane brief" for lanes, and "the Run start line in inputs.md" outside them. The standby Lead's brief goes in `releases/<N>/briefs/`, not `releases/<N>/lead/` | L-5 (orchestrator.md); L-4 (standby Lead text) |

### File moves that go with these rows

These defer to L-9 (§3): any start or launch step a file below would carry links L-9's workstream instead.

- **L-4** merges `agent/roles/leader/multi-manager-release.md` into `agent/roles/leader/lane-orchestrators.md`, retitled "Lanes, divided with the owner", and deletes `multi-manager-release.md`. Every inbound link is repointed to the merged file, including those in historical plan folders; an anchor that no longer exists becomes a plain file link. The link check proves it. Kept from the deleted file: fixes are packet work, rule conditionally, the pin rules and the standby Lead. Not kept: the Lead as accountable plan agent, and the Lead-prepared packet queue.
- **L-5** keeps `orchestrator/lane-orchestrator.md` as the orchestrator's one lane procedure (read only your brief; decide within it; come to the Lead or owner only at the brief's listed points). `orchestrator/multi-manager-dispatch.md` becomes the `packets` option's mechanics. Its "Lead-prepared queue" and "may not merge" lines give way to §4.
- **L-4** updates the frontmatter `description` of leader.md and the merged lane file; **L-5** updates orchestrator.md's and multi-manager-dispatch.md's, so the generated indexes lose the old wording.
- **L-7 and H-1 land together:** H-1's conformed h3.md is in L-7's PR (or merges into the project branch first), so `check` stays green at every merge. So in tasks.md, H-1's Depends on becomes "L-3" and L-7's becomes "L-3, H-1"; the manager makes that tasks.md edit.
- **L-6** adds the brief ladder (§1) to the records table in `agent/shared/workstreams/release.md`, and leader.md and orchestrator.md link it.
- **H-1** folds anything `releases/16/briefs/manager-P66.md`, `manager-P67.md`, `manager-P68.md`, `manager-P70.md` and `orchestrator-h3.md` hold that h3.md lacks into h3.md (the section map shows it), and gives each a first line `Superseded by h3.md; not a brief.`, with `h3.md` written as a relative link to [h3.md](../../../releases/16/briefs/h3.md)
- **L-6** updates the records table in `agent/shared/workstreams/release.md`: `run.md` has a Lanes table linking briefs and holds no launch or dispatch queue for lanes, and `briefs/` holds lane briefs.

## Limits

This contract gives lanes one shape and one home per fact. It cannot make a brief's prose good, or keep State honest. It does not rewrite historical dispatch sections (Releases 13–16), and it adds no scheduler.
