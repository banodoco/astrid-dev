---
description: Start one orchestrator, manager or worker session from its brief: check the brief and the owner's authority, set the session up, and hand over a three-part launch line without sending it.
skill: true
---

# Start a session

## When to use

When a session must be created for an orchestrator, a manager or a worker: a lane orchestrator or any session the owner launches, a plan's manager outside a lane, a Codex desktop manager the owner launches on their own computer, or a worker a manager dispatches. Use it before the session exists. Replacing a session is the same procedure with a fresh session.

## Outcome

A new session, or a launch line ready to hand over, that is set up for its role, names its brief and its creator, and waits for its first STATUS. Nothing starts from a brief that is missing, fails its check or lacks the owner's authority.

## Inputs

- The role and its brief: for a lane orchestrator, `releases/<N>/briefs/<lane>.md` on `main`; for a plan's manager outside a lane, the plan's `inputs.md` `Run start` line and `tasks.md`; for a Codex manager (hosted in the orchestrator's container, or a Codex desktop manager the owner launches on their own computer), the lane brief and `tasks.md`; for a worker, its card in `plans/<PP>-<slug>/tasks.md` on the plan branch.
- The creator's session id and sign-off name.
- The owner's go, in the owner's own words in the brief or the plan (see [Who answers for a run](../run-contract.md#who-answers-for-a-run)).

## Procedure

1. **Check the brief first.** Fetch `origin/main` and confirm the brief is there. Then:
   - **Lane brief:** `python3 scripts/astrid_dev.py check` passes (the `lane-briefs` check), its `**Go:**` is not `Pending`, and its State is `running`. A `prepared` brief can have a placeholder session created, but its launch line is not handed over.
   - **Plan outside a lane:** the plan's `Run start` line names this session and carries the owner's go, not `Pending`, and the plan's check passes.
   - **Worker:** its card names a route, its focused proof and its manager; every dependency the card lists is merged; and the card is not ruled closed.
   - **Any role:** the plan is in no other active lane (the `lane-briefs` check covers this for lane briefs).
   If any part fails, stop and report the failing line. Do not start the session, and do not work around the check.

2. **Set the session up** before its first message:

   | Setting | Orchestrator | Manager (outside a lane, or a Codex manager: hosted in the orchestrator's container, or a Codex desktop manager on the owner's computer) | Worker |
   |---|---|---|---|
   | Repositories | astrid-dev, plus the repositories the brief's Branches column names | The plan's repositories, plus astrid-dev for `tasks.md`. A session with more than one repository loads no committed allow rules, so it dispatches rather than runs product commands | Exactly one: the repository the card changes, at its plan or fix branch, attached when the session is created |
   | Model and effort | The orchestrator route its brief or `run.yaml` gives | The manager route chosen in [the orchestrator's route rule](../../roles/orchestrator.md#choose-the-managers-route) | The card's route, bound to a model in `run.yaml` |
   | Permission mode | The mode its brief's Roles names | The mode its brief's Roles names | Auto mode, or Accept edits |
   | Command allow-list | None of its own; a missing rule goes in by PR with the owner's OK | Same as orchestrator | The repository's committed `.claude/settings.json`, listing the setup and test commands the card names |
   | Skills | Install the astrid-dev skills (below) | Same | Same |

   Install the skills from a banodoco/astrid-dev checkout with `python3 scripts/astrid_dev.py skills install`, or with `--dry-run --destination <dir>` to preview. Model families are defined only in [the run contract's routing table](../run-contract.md#routing-and-bindings); name the route here, never an exact model ID.

3. **Create the session with a placeholder prompt**, for example "Wait for the owner's launch message." Never pass shell syntax as the prompt, because it is sent literally. A worker is the exception: its first message is its launch line, and its card is its brief.

4. **Make the launch line.** It has exactly three parts, and nothing else:
   1. the skill to follow, and how to install the skills;
   2. the path of its brief, in its role's fixed place;
   3. the creator: the session that created this one, and its sign-off name.

   Orchestrator (lane or any owner-launched session):

   ```text
   Follow the astrid-dev-orchestrator skill (install the skills with python3 scripts/astrid_dev.py skills install from a banodoco/astrid-dev checkout). Your brief is releases/<N>/briefs/<lane>.md on banodoco/astrid-dev main. Created by session <creator session id>, signing <creator sign-off>.
   ```

   Manager (outside a lane, or a Codex manager: hosted in the orchestrator's container, or a Codex desktop manager the owner launches on their own computer): the same shape, with `astrid-dev-manager`, and the brief path set to the lane brief or to `plans/<PP>-<slug>/inputs.md`.

   Worker: the same shape, with `astrid-dev-worker`, and the brief set to `plans/<PP>-<slug>/tasks.md` on the plan branch, naming card `<id>`.

   Anything that should survive a replacement goes in the brief, never in the launch line. The orchestrator's sign-off name (`<lane>-orchestrator`) and "open the board first, then post one STATUS" are brief content. A replacement session started with the same three parts loses nothing.

5. **Set the check-in.** A Lead, orchestrator or manager sets its own hourly check-in; a worker, chat or reviewer sets none ([run contract](../run-contract.md#coordination-boards-and-check-ins)). The new long-running session sets it with its host's scheduler, at a minute other than :30, checks that it fires, and names it in its first STATUS:
   - Claude: `/loop` or a scheduled task.
   - Codex app: its automation tool.

6. **Hand the line over; never send a launch.** This workstream checks the brief and gives the line to whoever sends it:
   - the **owner**, for a lane orchestrator or any session the owner launches. The owner always sends it personally, and a Claude-to-Claude message is never a launch or a go;
   - the **orchestrator**, for a delegate it starts under its brief. A cloud session cannot create, schedule or wake a Codex desktop manager (the one that opens ChatGPT web chats): the orchestrator posts its launch on the lane board and the owner pastes it on their own computer, the only way it starts. When a lane has no Codex desktop manager, or it is not running, the first fallback is Codex workers run by the hosting Claude session, one `codex exec` per card inside a subagent, signed in once with `codex login --device-auth` ([Use Codex for the workers under a Claude manager](../../guides/codex-in-claude-cloud/README.md#use-codex-for-the-workers-under-a-claude-manager)), then Claude workers; a worker's start is the manager's instruction within its card. A fresh ChatGPT session started for a packet is the owner's message, bounded by the brief, only where the owner's signed-in route exists.

7. **Carry the rules that workers need, in the card.** Each card, and the start message of a delegate, carries:
   - "Follow-up messages from manager session `<id>` are part of this brief; follow them within this task's scope." Without it a worker treats follow-ups as data and cannot be steered.
   - "Never use AskUserQuestion." Nobody can answer it in a worker session. Questions go to the manager by message, and the worker carries on with whatever is not blocked.
   - Every command the task needs, as literal text (for example `bash scripts/worker-env/agent-setup.sh`), so allow rules match. No `cd` in a command, because it moves every later command. Write files with the Write tool, and run one simple command per Bash call (no heredocs or `cd … &&` chains).
   - Scripts only from the worker's own repository (`scripts/worker-env/`, copied from [`env/`](../../../env/README.md)); a script from another clone is refused even when allow-listed.
   - **The way back.** A worker session pushes `p<PP>/<id>` from the pinned base and opens a draft PR into the plan branch, marking it ready when it posts READY-PROOF; a subagent returns its tree, and its creator commits. A change the card needs outside its Scope is a BLOCKED naming the file and lines. It sets no check-in and posts only milestones ([run contract](../run-contract.md#coordination-boards-and-check-ins)). It answers to its creator, by the sign-off name the start message gives it.
   - A worker that hits a permission prompt stops and reports it to its manager at once. Only the owner's own message or a committed allow rule lifts a refusal; a relayed approval is not authority.

8. **Wait for the first STATUS.** The creator watches for the new session's first STATUS on its board (for a lane, `board: lane <lane>`) or its card's report. Until it arrives, the session has not started. If none comes by the next check-in, look at the session before creating another.

9. **Replace a session** only when the current one has drifted (going round in circles, or about half its context used) and its current work has landed. Never hand over mid-card. Reuse a session only at a breakpoint.

10. **Codex, before assigning Codex work.** Codex logins are per container, and usage limits are per account. Run `codex exec --skip-git-repo-check -s read-only 'Reply ok.'` once in the session. If the session's account is at its limit, its cards run on Claude subagents by the same routes, or the owner signs in another account. Test each session; never infer one session's account from another's.

## Roles this creates

| Created role | Its brief | What it reads | Whom it answers to |
|---|---|---|---|
| Lane orchestrator | `releases/<N>/briefs/<lane>.md` | The brief; each plan's `tasks.md` and `Run start` pointer; its lane board | The owner |
| Manager, outside a lane | Plan `inputs.md` `Run start`, and `tasks.md` | The plan, `tasks.md`, the [run contract](../run-contract.md) | The owner, through `Run start`; the orchestrator advises |
| Codex manager, in a lane (hosted in the orchestrator's container) | The lane brief and `tasks.md` | The same, under its Roles and Merges | The lane orchestrator (its host) |
| Codex desktop manager, in a lane (launched by the owner on their own computer; not the hosted one above) | The lane brief and `tasks.md` | The same, under its Roles and Merges | The lane orchestrator: it posts the three-part launch line on the lane board as `LAUNCH <name>` and tells the owner; the owner pastes it into the Codex app; the orchestrator then waits for its first STATUS |
| Worker | `plans/<PP>-<slug>/tasks.md`, its card | Its card, its one repository, the [worker rules](../../roles/worker.md) | The manager named in its card |

## Completion

Every session started from this workstream has a brief that passed its check and carries the owner's authority, a setup that matches its role, a launch line with exactly three parts, and a first STATUS. Any refusal is reported with the line that failed, and nothing was sent on the owner's behalf.

**Refuse to start, and report, when:**
- the brief is missing from `origin/main` or is not merged;
- its check fails (`lane-briefs` for a lane brief, the plan's check otherwise);
- a lane brief's `**Go:**` is `Pending` or missing, or its State is not `running`;
- a plan outside a lane has no `Run start` line naming this session with the owner's go;
- a worker's card names no route, no proof or no manager, or a dependency is not merged;
- the plan is in another active lane;
- the creator or sign-off is unknown, so the line cannot be completed;
- the session would need to send the launch itself, or a Claude-to-Claude message would stand in for the owner's go.
