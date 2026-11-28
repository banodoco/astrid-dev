# Lane briefs — the contract (L-2, 28 Nov 2026)

[Plan](../plan.md) · [Tasks](../tasks.md) · [Findings and design](design.md)

This note settles the lane-brief contract that L-3 to L-8 apply. It starts from [design.md](design.md), and adopts ruling D1 ("lane"; no "batch") and owner decision D2 (the Lead divides each release into lanes *with* the owner). Where this note and design.md differ, this note wins. Each later task applies its rows here and makes no new design choice; a gap goes to the Plan 108 manager as a question.

## 1. What a lane is, and where its brief lives

**A lane is the set of plans one orchestrator session runs and answers for, possibly across releases.** This is the one definition. It goes in `agent/shared/glossary.md`, and every other file links to it.

- **One brief per lane,** at `releases/<N>/briefs/<lane>.md`, where `<N>` is the first release the lane runs in and `<lane>` is a lowercase slug (`[a-z0-9-]+`).
- **A later release adds nothing to the brief's folder.** It lists the lane's plans for that release in its own `## Included plans`, and links the same brief from its run board's Lanes table. Nothing is copied.
- **Every plan in a release belongs to exactly one lane.** Small independent plans may share a lane (leader.md's existing grouping rules stand). A **standing lane** is an ordinary lane whose Plans table grows during the release. A plan outside any release (astrid-dev-only) may run without a lane, under its own `Run start` line.
- **Lane brief or not:** a file in `releases/*/briefs/` is a lane brief exactly when it has a header line starting `**Lane:**`. Other files there (manager briefs, reviewer briefs, fixed messages) are unaffected.

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
| `**Board:**` | The board issue title, and its link once opened | Yes |

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
| `## Launch` | The owner's one-line launch, in one fenced `text` block | Yes: exactly one fenced block |
| `## Status` | A pointer to `release status <N>` and the board; never a copy | Yes |

**The fixed launch line,** filled in from the header:

```text
You are the <lane> lane orchestrator; sign comments <lane>-orchestrator. Follow the astrid-dev-orchestrator skill. Your whole job is the lane brief releases/<N>/briefs/<lane>.md on banodoco/astrid-dev main; open its board first, then post one STATUS.
```

**Where the old dispatch-note fields go** (so L-3 and H-1 lose nothing): branch rules → Plans and order (Branches) and How it runs (Merges); routes and modes, in-flight cap, "first packet alone", READY-PROOF, startup checks, hourly cadence → How it runs; mailbox → Board; standing rulings → Standing rulings; queue table → Queue (as links); roles and sessions → Roles; owner-only list → Owner only; launch message → Launch; CI sharing → Cut line and coordination. Packet handoff state (Ready, Running, Review) lives in the board's STATUS and each plan's `tasks.md` Progress, not in a table in `run.md`.

## 3. One home each

| Fact | Its one home | Who writes it | Everywhere else |
| --- | --- | --- | --- |
| **The run's start and limits (`Run start`)** | The brief: `**Go:**`, Roles (may do without asking) and Owner only | The Lead writes the brief. When the owner gives the go, the Lead records it in `**Go:**`, sets State `running` and merges, all **before** the launch is sent | Each plan's `Run start` line in `inputs.md` is a pointer: `**Run start:** Lane <lane>: the brief records the owner's go, authority and limits.`, with `<lane>` a relative link to the brief The Lead writes it in the brief's PR, and it never changes with State. Outside a lane, `Run start` keeps its current full form, written by the session preparing the run with the owner's go in their words |
| **Rulings** | Release-wide: `releases/<N>/run.md` Standing rulings. One lane: the brief's Standing rulings. Holding beyond the release: the skill or role document. A decision about one task: that plan's `tasks.md` (its row or decision log), which is not a ruling | Whoever rules appends it with its date and who ruled. The orchestrator may append its own lane rulings | A board DECISION states the ruling and links its home. Never in `Run start`, a launch or the board alone. A lane ruling can never widen Owner only or How it runs; an entry that tries to is void |
| **Launch** | The brief's Launch block | The owner always sends it personally, into a new orchestrator session. The Lead may create that session with a placeholder prompt ("Wait for the owner's launch message") | No launch text in `run.md`, the role documents or the leader workstream; they link the template. Messages that start **delegates inside a lane** (packet sessions) are not launches: the orchestrator sends them from the owner's own ChatGPT account, so they are the owner's messages, bounded by the brief. A Claude-to-Claude message is never a launch or a go |
| **Accountability** | The run contract's "Who answers for a run" table | — | **The lane's orchestrator is the one accountable agent for every plan run in its lane,** in either option. It answers to the owner. Its hosted manager or packet sessions are bounded delegates. The Lead is accountable for no plan in a lane: it holds the release-level part (dividing lanes with the owner, landing order, qualification, publication, pins across lanes, and the release gate unless the brief gives it to the orchestrator) |

**Brief edits after launch.** The orchestrator may merge, on a passing check, PRs that change only its plans' `tasks.md` files, append to its brief's Standing rulings, or set its brief's State to `paused` or `done`. Every other change to a running brief (Plans and order, How it runs, Roles, Owner only, Go) is re-laning or re-authorizing. The Lead proposes it, and it merges only on the owner's go.

**The advisor** (blocking questions) follows the chain and is named once, in the brief's Roles. A delegate asks the orchestrator. The orchestrator asks the Lead for release-level questions, and the reviewer binding, a fresh high-judgment session, for technical judgment beyond its own route. A lane orchestrator is never anyone's advisor except its own delegates'.

## 4. How it runs: two options

Each brief picks one, on its `**Option:**` line. A lane that needs both is two lanes.

| | `hosted`: Claude-hosted orchestrator with a manager | `packets`: fresh ChatGPT packets |
| --- | --- | --- |
| **Session** | One Claude cloud session is the orchestrator. The manager role is hosted inside it, one per running plan, at most two at once | One orchestrator session. A fresh normal ChatGPT session per unit, in its route's mode (N High, X Extra High, S Pro) |
| **The manager** | By default the orchestrator manages each plan itself, dispatching each card to a **Codex worker** by its route (Claude subagents on the same routes if Codex is unavailable). This is the one statement in [codex-in-claude-cloud.md](../../../agent/roles/orchestrator/codex-in-claude-cloud.md#use-codex-from-claude-cloud). A hosted **Codex manager** only when How it runs says so, with a one-line reason | None. The orchestrator writes each unit's packet at dispatch from its cards ([packet template](../../../templates/release/packet.md)); no packets are prepared ahead. Fixes are packet work: Claude sessions diagnose, review, prove and merge, but never write the fix |
| **Proof** | The card's focused proof in the session, and hosted CI as the final check | The author runs the focused proof and opens a PR into the plan branch. Green CI plus the shown proof is the evidence, and the orchestrator answers each READY-PROOF |
| **Merges** | Same in both: the orchestrator merges its own progress PRs and into its plan branches on green. Into `release/<N>/main`: the release gate the brief's Merges names, either `Lead` (the default) or `orchestrator, after any overlapping merge`, which the owner grants by their go on the brief | (same) |
| **Mechanics** | [orchestrator/lane-orchestrator.md](../../../agent/roles/orchestrator/lane-orchestrator.md) | [orchestrator/multi-manager-dispatch.md](../../../agent/roles/orchestrator/multi-manager-dispatch.md), its packet start message and proof turnaround |
| **Use when** | Any unit needs what a ChatGPT session cannot reach: an installed stack, a live machine or fixture, GPU or local measurement, a loop or taste plan worked in rounds; or the lane is astrid-dev-only | Every unit is self-contained: a card with outcome, May touch and focused proof that runs in the packet session or on hosted CI. The usual choice for wide, independent product-repository units |

## 5. What CI checks

**L-7 adds one check, `lane-briefs`,** in `scripts/records.py` (parsing) and `scripts/checks.py` (the check, `always`), over every lane brief (§1). It fails when:

1. **A field is missing:** any header field or section in §2 marked Required is missing or empty, or a field holds a template placeholder (`<…>`). The same applies when the Option line or one of the six How it runs labels is absent, when Launch has no fenced block or more than one, or when Queue has no `tasks.md` link or holds a table row.
2. **A header value is malformed:** `Lane` differs from the file name; the first `Releases` number differs from the path's `<N>`; State does not start with one of the four values; or Go starts `Pending` while State is not `prepared`.
3. **A plan is unknown:** a Plans and order row's link does not resolve to an existing `plans/<PP>-*/plan.md`, or its Release is not in the header's Releases.
4. **A plan is not in the named release:** the plan is missing from that release's `releases/<R>.md` `## Included plans` (read with `records.release_brief`), or `releases/<R>.md` does not exist.
5. **A plan is in two active lanes:** across all briefs, a plan appears in more than one brief whose State is `prepared`, `running` or `paused`.
6. **A started lane's plan has no pointer:** for a brief whose State is `running` or `paused`, a listed plan's `inputs.md` `**Run start:**` line does not link that brief's path.

Each of 1, 3, 4 and 5 gets an injected-failure test (the Completion list), and 2 and 6 get one each.

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
| 2 | **Accountability:** the lane orchestrator "answers for it finishing", against the run contract's manager accountable and orchestrator advisor | In a lane, the orchestrator is the one accountable agent for every plan run, in either option; managers and packet sessions are bounded delegates (§3). The run contract gets a row "A plan in a lane" and drops the Lead-accountable fresh-packet row. "A manager in its own session" stays, for runs outside lanes. manager.md gets one line: "In a lane, the orchestrator answers for the run; you deliver your plan for it, under the brief." | L-6 (run contract, manager.md); L-5 (orchestrator.md "One exception" paragraph) |
| 3 | **The Lead's part:** a lane orchestrator may take the Lead's part for its plan, against the Lead as the single accountable agent | Split by level, with no "taking a part". Plan level (packets, reviews, plan-branch merges, proofs) is always the orchestrator's; release level (lanes with the owner, landing order, qualification, publication, cross-lane pins, and the release gate unless the brief grants it) is always the Lead's. Delete "A lane can be the Lead for its own plan". Leader responsibility 2 names the lane's orchestrator, or the plan manager outside a lane | L-4 |
| 4 | **Default manager type:** Codex manager by default, against Codex workers by default | Codex workers are the default; a hosted Codex manager only by the brief's stated choice (§4). codex-in-claude-cloud.md stays the one statement. Remove "Host one Codex manager on Terra…" from the leader lane launch text, which goes with the launch move | L-4 |
| 5 | **Who writes `Run start`:** orchestrator, Lead (twice), owner | In a lane, the Lead writes the brief and each plan's pointer `Run start` line in one PR, and records the owner's go in `**Go:**` before the launch (§3). The orchestrator never writes `Run start`. Outside a lane, the session preparing the run writes it with the owner's go. The rule's one home is the run contract's "Who answers for a run", with the field list in `templates/project/inputs.md`, which gains the pointer form | L-6 (run contract, `templates/project/inputs.md`); L-4, L-5 (link) |
| 6 | **Who sends the launch:** the owner must paste it, against the orchestrator sending start messages from the owner's account | The owner always sends a lane's launch personally. Delegate start messages inside a lane (packet sessions) are sent by the orchestrator from the owner's ChatGPT account, bounded by the brief, and are not launches (§3). The run contract's authority paragraph states both, once | L-6 (run contract); L-4, L-5 (link) |
| 7 | **Where rulings live:** one home in the run board, against answers in `tasks.md` or `Run start` | Four homes by reach (§3): release (`run.md`), lane (brief), beyond the release (skill), one task (`tasks.md`, a decision and not a ruling). Never `Run start`. Run-contract coordination rule 4 states this; lane-orchestrator.md's "written into `tasks.md` or the `Run start` line" becomes "the brief's Standing rulings" | L-6 (run contract); L-5 (lane-orchestrator.md); L-4 (leader "Rulings" paragraph) |
| 8 | **The advisor:** the orchestrator, a fresh high-judgment session, or a lane orchestrator on route X | The advisor follows the chain and is named once in the brief's Roles. Delegates ask the orchestrator; the orchestrator asks the Lead (release level) or the reviewer binding (technical judgment). A lane orchestrator advises only its own delegates (§3). Glossary "advisor" and the leader-side "Release Lead as advisor" wording change to match | L-6 (glossary); L-5 (lane-orchestrator.md "When to use") |
| 9 | **Merge rights** of a lane orchestrator against the run contract's auto-merge rules | One rule in the run contract. The accountable agent (the orchestrator in a lane) merges its plans' `tasks.md`-only PRs, its brief's ruling and State edits, and into its plan branches, on a passing check or green CI. Into `release/<N>/main`, the release gate named in the brief's Merges (Lead by default). Every other merge into `main` needs the owner's go | L-6 (run contract); L-5 (lane-orchestrator.md "Merge your own records" links it) |
| 10 | **Duplicated rules:** `Run start` in four places, launch messages in four, the parallelism pass in two | `Run start`: the run contract plus `templates/project/inputs.md`, with the rest linked. The lane launch lives in the lane template's Launch; the "Orchestrator launch message" section leaves `templates/release/run.md`, and orchestrator.md "The start message" is kept only for runs outside lanes. The packet start message stays only in multi-manager-dispatch.md. The parallelism pass lives in lane-orchestrator.md; the Lead's hourly pass keeps only cross-lane conflicts and links it | L-3 (`templates/release/run.md`); L-4 (leader lane procedure); L-5 (orchestrator.md, lane-orchestrator.md); L-6 (run contract) |
| 11 | **Dangling references:** "dispatch notes in tasks.md"; `releases/<N>/lead/` | The orchestrator.md start message reads "start from the lane brief" for lanes, and "the Run start line in inputs.md" outside them. The standby Lead's brief goes in `releases/<N>/briefs/`, not `releases/<N>/lead/` | L-5 (orchestrator.md); L-4 (standby Lead text) |

### File moves that go with these rows

- **L-4** merges `agent/roles/leader/multi-manager-release.md` into `agent/roles/leader/lane-orchestrators.md`, retitled "Lanes, divided with the owner", and deletes `multi-manager-release.md`. Every inbound link is repointed to the merged file, including those in historical plan folders; an anchor that no longer exists becomes a plain file link. The link check proves it. Kept from the deleted file: fixes are packet work, rule conditionally, the pin rules and the standby Lead. Not kept: the Lead as accountable plan agent, and the Lead-prepared packet queue.
- **L-5** keeps `orchestrator/lane-orchestrator.md` as the orchestrator's one lane procedure (read only your brief; decide within it; come to the Lead or owner only at the brief's listed points). `orchestrator/multi-manager-dispatch.md` becomes the `packets` option's mechanics. Its "Lead-prepared queue" and "may not merge" lines give way to §4.
- **L-6** updates the records table in `agent/shared/workstreams/release.md`: `run.md` has a Lanes table linking briefs and holds no launch or dispatch queue for lanes, and `briefs/` holds lane briefs.

## Limits

This contract gives lanes one shape and one home per fact. It cannot make a brief's prose good, or keep State honest. It does not rewrite historical dispatch sections (Releases 13–16), and it adds no scheduler.
