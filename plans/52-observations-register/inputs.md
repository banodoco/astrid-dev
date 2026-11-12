# Inputs — Observations register

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner asked the question on 12 Nov 2026 ("is there a missing piece … a register of smells or tickets that precedes plans and feeds into them? Or should we just have stubs of plans? Or are these actually gaps?") and asked for a proposal; she has not chosen an end state. Next: the owner reads the proposal and decides D1–D6.

**Prior art:** Read on astrid-dev `origin/main` on 12 Nov 2026 (commit not recorded; see Source identities).
- **The process ledger** is the same mechanism for astrid-dev's own friction: one file per entry, four plain header lines, add-only, `Resolved by` as the one editable line ([README](../../docs/ledger/README.md)); checked by `ledger_entry_errors` and `ledger_errors` (`scripts/check_docs.py:114`, `:144`), registered at `scripts/checks.py:465`. It has 38 entries in five days, so agents do write entry files. It excludes product findings by rule. One entry is a product finding anyway (`2026-11-11-gpu-balance-lifecycle-gap`), which shows the pressure.
- **GitHub issues** are the documented home for bugs and small fixes ([contribution workflow](../../docs/contribution-workflow.md), route table; [bug skill](../../skills/astrid-dev-bugfix/SKILL.md)). In practice the repository has three issues, against more than 550 pull requests: a bug, a coordination mailbox and a test (GitHub search, 12 Nov). The bug template asks for reproduction, environment, recovery and an upstream decision, which is an incident record, not a one-line note. No label exists for observations (labels are GitHub's defaults plus `needs-review`).
- **Gaps** hold curated, dated evidence in `Current state`; a gap "names a result that would still matter if today's proposed project were replaced", and gap files feed the generated public vision page. They have no list of observations and are the wrong grain for one.
- **Plans** already take follow-ups as rows: Plan 32 has `F1`–`F4` "(follow-up, …)" (`plans/32-generation-placement-targets/tasks.md:66-69`) and Plan 17 has `C2`, `C3`. So "fold into a plan" has an existing form: a row in that plan's `tasks.md`. What is missing is where a finding waits before a planner places it.
- **Release decision logs** (`releases/13/decisions.md`) hold a run's findings in time order. They are per release and are not read by the next planner.
- **Plan 48** names the record kinds (project, gap, release, ledger entry, review form) and gives one registry for checks and one for generated views ([extending.md](../../docs/extending.md)). A new kind is one reader, one `Check` and one `View`.
- **Negative finding:** Plans 44, 49 and 51 propose no intake or observation mechanism (read of their plan headers and task indexes only; their full text was not read).

**Approach:** Pending — recommended, not chosen. A second entry-file folder, `observations/`, reusing the ledger's shape and parser, with two fields the ledger lacks: `About` (gaps and plans) and `Outcome` (open, folded, fixed, issue, dropped). Next: the owner chooses (D1–D6); the advisor critiques. Alternatives:

| Alternative | Why not |
|---|---|
| GitHub issues with an `observation` label | Lives outside the repository, so a planner reading the pack never meets it and no check can tie it to a gap or a plan. Creating one needs GitHub write access mid-run, which sandboxed workers do not have. Three issues in the repository's life says agents do not work there. |
| Stub plans | A plan is "an independently useful result that merits its own priority, owner, dependencies and completion criteria" ([project format](../../docs/project-format.md)). Twenty stubs would add twenty catalog rows with an owner line and an estimate for things nobody has decided to do, and `pack-shape` would ask each for three files. |
| An observations section in each gap | Many observations bear on no gap or on two. Twenty-two hand-edited public files would conflict in PRs, and a gap would stop reading as an outcome. |
| Widen the process ledger to product findings | Smallest change, but it mixes two readers: Plan 51 and the orchestrator read the ledger to fix astrid-dev; planners would read observations to scope product work. The ledger is also add-only with `fix` entries, where an observation needs a link forward to a plan task. Kept as D2. |
| Do nothing; keep run notes | The 12 Nov findings were in three files outside the repository. That is the failure this plan answers. |

**Challenge:** Pending — Required before greenlight, because the plan changes astrid-dev's own checks ([plan skill](../../skills/astrid-dev-plan/SKILL.md#scale-the-method)). No independent critique has been made. Next: the advisor critiques this draft for what can be removed. The first question to put to it: is the generated page needed, or is `grep "^Outcome: open"` enough until the folder has a hundred files?

**Proof and limits:** Pending — Proposed in [plan.md](plan.md#completion): a fresh agent writes a valid file from the skill alone; the interim files pass unchanged; five negative cases. Verified so far: the 22 interim files and the README, added as `observations/` to a copy of `main`, leave `python3 scripts/astrid_dev.py check` passing (12 Nov, no base supplied, so `pr` checks did not run). Unverified: use. Next: the owner accepts or changes the completion list.

**Review rounds:** Pending — Recommended: none. The project is small and bounded, touches no product repository, release or user data, and ordinary PR review covers it. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, what still needs the owner's go, and the advisor session if there is one.

## Owner decisions

- **D1. Its own plan, or rows in an existing one?** (a) This small plan. (b) Three rows added to [Plan 48](../48-one-record-model/plan.md), which owns record kinds but whose accepted queue is finished and whose remaining tracks are unrelated. (c) Rows in [Plan 51](../51-astrid-dev-clean-up/plan.md), which is active but whose goal is fewer words and script lines. *Recommended: (a).* It has its own decisions and proof, and adding scope to an accepted plan needs a scope review anyway.
- **D2. Name and place.** (a) `observations/` at the repository root, beside `plans/` and `vision/`, because it feeds them. (b) `docs/observations/`, beside the ledger. (c) Call them tickets. *Recommended: (a).* "Ticket" implies an assignee and a workflow; "observation" matches the gap template's "what is observably true today". Also decide here whether the process ledger later moves into the same folder as observations about astrid-dev. *Recommended: not now;* share the parser, keep two folders, revisit when Plan 51 is done.
- **D3. What stops it rotting?** (a) No timer: the generated page lists open observations oldest first, and three existing moments read it (scoping a plan, reassessing a gap, closing a release). (b) Also a check that fails when an observation has been `open` for more than some number of days. (c) Also a completion gate: a plan cannot go `done` while an observation about only that plan is `open`. *Recommended: (a).* A timer would make people write `dropped:` to pass CI. Add (c) only if a release closes with observations nobody read.
- **D4. A command?** (a) None: the file write is the command, as for the ledger. (b) `python3 scripts/astrid_dev.py observe "<text>" --about F-008 --source "<run>"`. *Recommended: (a),* and add (b) only if malformed files show up.
- **D5. Do issues stay the home for bugs?** *Recommended: yes, for incidents:* a failure with a user to recover follows the bug skill and its template. An observation that turns out to be one gets `Outcome: issue: #N`. The route table gains one row so the two are not confused.
- **D6. Are observations shown on the public vision page?** *Recommended: no.* They are unverified by definition. The folder is as public as the repository; the README says to keep credentials, private logs and machine-specific data out.

## Source identities

Pending — The draft was written against a fresh read-only copy of astrid-dev `origin/main` on 12 Nov 2026; its commit was not recorded. Before code work, record the base commit, confirm `scripts/check_docs.py` and `scripts/checks.py` still have the ledger reader and registry at the lines cited above, and record Plan 51's open branches that touch the same files. Destination: astrid-dev `main`, by ordinary PR.

## References

- The owner's question, 12 Nov 2026 (session message, paraphrased in the proposal; not in the repository).
- The inputs it was written from, in the working folder outside the repository: `briefs/wave3/smells.md`, `briefs/wave3/usability-log.md`, `briefs/wave3/failures-catalogue.md`; and the Release 13 decision log, entries of 12 Nov 14:00–14:43 UTC.
- The 22 interim observation files and their README, proposed for `observations/`.
- [Contribution design principles](../../docs/contribution-design-principles.md), principles 2, 4 and 8.
