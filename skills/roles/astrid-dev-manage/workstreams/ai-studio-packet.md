---
description: Drive one planet-lab packet through a fresh Google AI Studio session, push its branch and report it for the reflection gate.
---

# Workstream: run one packet in AI Studio

## Workstream contract

**Outcome:** One lab packet executed by a fresh AI Studio session and pushed to its own `lab/<id>` branch with a result note, ready for the reflection gate.
**When to use:** When an operator (normally a Codex agent with browser control of the owner's AI Studio account) is given a Ready packet from a lab run board such as Plan 84's.
**Inputs:** The run board, the packet brief and `LAB_RULES.md` at the lab's `main` head, the mailbox issue, the AI Studio workspace linked to the lab repository.
**Procedure:** Check the packet is Ready, open a fresh AI Studio session on `main`, paste the start prompt, supervise to the result note, push `lab/<id>`, then post STATUS.
**Completion:** The branch exists at a recorded commit with `packets/<id>.result.md`, and a STATUS (or BLOCKED) comment on the mailbox names the packet, branch, commit and AI Studio's own check output.

Use for a lab repository built to be developed in Google AI Studio and imported into an Astrid product repository at the end, as in [Plan 84's lab run](../../../../plans/84-living-planet-on-the-vision-page/ai-studio-run.md). **You are the operator, not the engineer.** AI Studio writes the code; you give it the packet, keep it inside the packet, and move its work to GitHub. You do not review it: a fresh Astra reviewer does ([Astra reflection](astra-reflection.md)), and a packet is merged into the lab's `main` only on that reviewer's accept verdict. When you are also the run's manager, you commission that reviewer and do the merge.

## Run one packet

1. **Check.** Read the mailbox for messages to you, on every resume too. On the run board, the packet must be **Ready** and every packet it depends on **Accepted**. Note the lab's `main` head commit.
2. **Open a fresh session.** One packet, one new AI Studio Build session. Bring the lab's `main` into it at that commit (AI Studio's GitHub import or sync). Do not reuse a session from another packet; a rework round may reuse its own packet's session if it is still open.
3. **Start it.** Paste the [start prompt](#start-prompt) with the packet ID and commit filled in. Add nothing else.
4. **Supervise.** Answer AI Studio's questions only from the brief and `LAB_RULES.md`. If it wants to do something the brief does not ask for, the answer is "not in this packet". If it asks something the brief cannot answer, have it write the question in its result note and stop. Make sure it runs `npm run check` and `npm run build` and reports their output. Do not write or edit code yourself.
5. **Push.** When the result note exists and the checks pass, push to the branch `lab/<id>` (never `main`). Confirm on GitHub that the branch head matches, and that the result note is in it.
6. **Report.** Post STATUS on the mailbox: **packet ID; branch and commit; AI Studio's check and build output as reported; time taken; anything it was unsure of**. Mark the packet **Gate** on the board. Stop.
7. **Rework.** If the gate sends rework, paste the gate's rework prompt into the same packet's session (or a fresh one at the branch head), then push and report again. After two rework rounds the gate splits the packet instead.
8. **If blocked** (AI Studio cannot import, run tests, push, or keeps failing the same check after two attempts), post BLOCKED with what happened, a screenshot or copied output, and what you need. Do not work around a rule in `LAB_RULES.md`.

## Start prompt

```text
You are working in the Astrid planet lab (banodoco/planet), at commit <main SHA>.
1. Read LAB_RULES.md and packets/<ID>.md completely before changing anything.
2. Do packet <ID> exactly as written, and nothing in its "Not in this packet" list.
3. Run `npm run check` and `npm run build`, and fix failures within the packet's scope.
4. Write packets/<ID>.result.md as described in packets/README.md.
5. Commit with messages starting "<ID>:" and push to the branch lab/<ID>. Never push to main.
If anything in the brief is unclear or looks wrong, stop and write that in the result note instead of guessing.
```

**Do not merge without an accept verdict, edit briefs yourself, change `LAB_RULES.md`, run two packets in one session or write a verdict:** verdicts and briefs belong to the reflection reviewer, and the look to the owner.
