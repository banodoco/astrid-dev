# P73-INT — Absorb a landed Plan 71 or Plan 72 into the Plan 73 branch

**Source tasks:** [`tasks.md`](../tasks.md#completion-run-owner-go-24-november-2026) — MSC-9
**Route:** X (ChatGPT mode: Extra High; [run contract](../../../agent/shared/run-contract.md#chatgpt-session-modes)). One fresh session per absorption round: it runs Part A, stops, and runs Part B only after the orchestrator's DECISION.
**Estimate:** about 1–2 hours a round
**Outcome:** After Plan 71 or Plan 72 lands on `main`, the Plan 73 branch carries it in the new layout: every edit that landed under `skills/` is re-applied under `agent/`, every Markdown link a landed change added into `skills/` points at its new home, and nothing else changes.
**Dependencies:** a REQUEST from `p71-73-orchestrator` on the board naming the round, the `main` SHA that contains the landed project, the Plan 73 head, and the orchestrator's evidence: the exact output of `git log <last ported SHA>..origin/main -- skills/` and of `git grep -n -E "\]\([^)]*skills/" -- ':!skills' ':!plans/*/evidence'` on the merged head. **You cannot run git or search other branches; work from that evidence and the compare view.**
**May touch (Part B only):** the `agent/**` file that ports each `skills/**` file the delta names (for Plan 71: `agent/shared/workstreams/gap.md`); `plans/73-markdown-first-agent-skills/evidence/cutover-map.md` (one row per file the delta names); Markdown link targets that the orchestrator's `git grep` output lists. Nothing else.
**Must not touch:** `skills/**`, `sync.sh`, `scripts/**`, any generated file (`docs/checks.md`, views), any test, `tasks.md`, any file the delta and the `git grep` do not name.
**Proof:** the orchestrator's: both repository checks, the full unit suite, `git log <last ported SHA>..origin/main -- skills/` prints nothing unported, two identical skill builds, and `git grep` for links into `skills/` is empty outside history. You cannot verify link anchors; the orchestrator's `markdown-links` and `link-anchors` checks do. Selectors for READY-PROOF: `scripts/test_checks.py scripts/test_skill_builder.py scripts/test_agent_documents.py`.
**PR destination:** astrid-dev `p73/int-<round>` → `project/73-markdown-first-agent-skills`
**Authority:** [run board](../run.md#authority)

One packet starts **one fresh ChatGPT session**. The session opens task PRs and ends with `READY-PROOF`, **never merging or editing `tasks.md`**. The orchestrator runs the proof and reviews; the orchestrator integrates.

## Part A — Fact-find (read-only; post before any edit)

From the evidence in the REQUEST, post one STATUS with a table: each `skills/**` file the delta names; its ported home in `agent/**` (from `evidence/cutover-map.md`); what changed upstream (the lines); the exact edit you will make at the new path; and every relative link in that change, with its new target. Relative depth changes (`skills/shared/workstreams/x/SKILL.md` links four levels up; `agent/shared/workstreams/x.md` links three) and generated-skill name rules (`astrid-dev-<stem>`) are the usual traps. Name any file with no ported home as a question. Then stop: the orchestrator answers within 45 minutes.

## Part B — Port (after the DECISION)

Make exactly the edits the DECISION approves, on `p73/int-<round>` from the Plan 73 head the REQUEST names. Keep the landed wording byte-for-byte except link targets and heading names the new path requires. Open the draft PR, post the early STATUS, then `READY-PROOF`.

## Contract

- No new rule and no reworded sentence: this carries a landed change to its new path, nothing more.
- No second copy: the `skills/` file is not edited (the cutover deletes it).
- If the delta names a file the cutover map does not cover, post BLOCKED; do not invent a home.
