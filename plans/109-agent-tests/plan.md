# Agent tests

**Project:** Agent tests

**Goal:** Every role, workstream, start message and brief is proved the way code is: declared cases give a fresh session only what that role receives, and check it takes the golden path.

**Status:** active

**Owner:** The planning session `session_011EzfW1gtAhRQwk8pgJMzhG` (Claude Opus), at the owner's request on 28 November 2026

**Estimate:** 3–4 days (units of at most 1 day; planning figures)

**Waiting on:** —

**Run route:** astrid-dev-only

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — the release process itself. Runs stall when instructions a session follows are missing, contradictory or untested; agent tests find that before a launch, not during it.

## Outcome and scope

- **Cases** in `agent-tests/cases/`, one file each, declaring the documents they cover, the brief they run under, the host, the exact starting message, and Expect and Must not lines.
- **A golden path** (`agent-tests/golden-path.md`): what each role should do, each line resting on a document or on one of four parent rules (authority, hand-off, clock, host).
- **A runner** (`astrid_dev.py agent-test`): list, status, coverage, the actor's prompt (never the expectations), the judge's prompt, an actor checkout that withholds the answers, and status from the newest run sheet.
- **A structure check** (`agent-tests`), and a home in the existing meta workstream: [improve](../../agent/shared/workstreams/improve.md#agent-tests) runs, synthesizes and records agent tests. Principle 11 in the [design principles](../../docs/contribution-design-principles.md).
- **First cases:** the H3 lane chain (orchestrator, Codex manager, ChatGPT chat, Claude worker, reviewer) and six general paths (Lead dividing lanes, plan manager, manager to worker, a refused start, a contributor, an improve change).

**Deferred:** mocked-act runs through `claude plugin eval` for Claude hosts; CI running models.

## Existing work and decision

Builds on the 17 November fresh-context dry runs ([ledger](../../docs/ledger/2026-11-17-fresh-context-dry-runs.md)) and the 28 November H3 dry runs ([ledger](../../docs/ledger/2026-11-28-agent-path-dry-runs.md)), and on improve's existing Audit. See [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

[tasks.md](tasks.md). The parent-rule document fixes (AT-6) wait for the owner's answers to the golden path's three questions.

## Interfaces and handoff

Consumes the role and workstream documents as merged with Plan 108. Produces cases, results and the golden path that any later change to an agent document runs through improve.

## Completion

- `python3 scripts/astrid_dev.py check` passes, and `scripts/test_agent_tests.py` passes.
- Every case in `agent-tests/cases/` appears on a run sheet; the H3 chain passes, or its remaining misses are owner questions.
- The four parent rules are written at their homes and the cases that found them re-run.
