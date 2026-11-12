# Release 13 machines manager (own session) — brief

**You:** the Release 13 machines manager, Opus, in your own cloud session, so your workers get this session's CPUs and disk. You **manage**: you dispatch Codex workers and sub-agents, judge their results, commit, and hand branches over. You do little hands-on work yourself.
**You take over from:** the machines manager that ran inside the orchestrator's session until now. Its handover note will be at `releases/13/briefs/machines-handover.md` on this branch. The orchestrator publishes it once it's written. **Read it before dispatching anything.**
**You report to:** the Release 13 manager (orchestrator), session `session_011EzfW2L4ou5fDudzKLrc9d`, by `send_message`. Hannah, the owner, reaches you through the orchestrator unless she writes in your session herself.
**Written:** 12 Nov 2026, about 18:30 UTC, at Hannah's request.

## Your goal
Land the machines redesign in the Release 13 candidate. It's on the critical path. The owner's decisions are O1–O8 in astrid-dev `plans/40-machine-lifetime-controls/inputs.md` D14 on `main`:
- declare once;
- claim separate from generate;
- no automatic claim;
- no consent flag;
- named machines;
- jobs queue on their machine;
- no hard datacenter pin;
- you can see what a machine is doing;
- the idle timer is the only lifetime mode.

The live proof is **claim, then `generate --machine`**, on the composed candidate.

## Order (ruled by the orchestrator at 18:22, after an independent advisor review)
1. **K1** (the keep-warm checkpoint fix for edit): merge first, as soon as its Astra review passes.
2. **M1** (part d closes three custody gaps), after its Astra re-check.
3. **M2:** delete the generate-time paid controls, the allocation shims and the preferences plumbing, so the state space shrinks.
4. **LT: one lease transition table.** One module, an enum of states and events, and a table (state × event) → next state plus billing action. Every writer of `record.state`, `lease.state` and `preparation_state` goes through it.
   - A test enumerates every state × {restart, paid expiry, idle expiry, job failure, recipe or model change, cancel}, and each must end released or kept with a deadline.
   - The custody gaps found today are required rows.
   - Astra reviews it once.
   - The draft brief is in the handover.
5. **M4,** with card 5's fixes: the deadline interrupts post-create provider calls, and no thread waits under `lease_owner.lock`. Merge LT into it; never rebase.
6. **M3.** M5–M10 come after the first live claim-path pass.

## Gates on every card (`machines-gates.md` in the handover)
- **mypy:** net zero per file over R12, from `releases/13/evidence/tests/mypy/new-findings.tsv`. The machines lane owns 117.
- **Boundary ratchet:** `scripts/check_core_pack_boundary.py --check`, never `--write-baseline`. Per the owner (18:25), don't build new generalising interfaces for a second provider that doesn't exist. Any real RunPod crossings left over are handled by a one-time, owner-ruled baseline update, which the orchestrator lands.
- **Ruff and mypy are moving to per-(file, code) ratchets,** run by the test lane. Don't raise BLE001 or F821 in your files.
- **Money and custody work:** Sol at high effort, plus an Astra (high) review before merge.

## Read
- The handover note, first.
- `releases/13/decisions.md`: the NOW block, and the entries mentioning machines, M1, M4, K1 or LT.
- `releases/13/briefs/machines-design.md`, `machines-plan.md`, `machines-manager.md`.
- The skills on astrid-dev `main`: `astrid-dev-manage`, `astrid-dev-iterate`, the `astrid-dev-shared/run-contract.md`, and `astrid-dev-orchestrate/codex-in-claude-cloud/README.md`.

## Setup, in this order
1. **Attach** `banodoco/astrid-agent` (push), `banodoco/VibeComfy` (read), `banodoco/astrid-runtime` (read) and `banodoco/astrid-dev` (push) with `add_repo`.
2. **Codex:** make sure `codex` is installed. If it isn't signed in, start the sign-in and **send Hannah the sign-in link or code in your session's reply**; she'll complete it. Then confirm `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high -s danger-full-access` runs and the log header shows the effort.
3. Fetch the lane's branches (`r13/machines`, `r13/machines-m1`, `r13/machines-m4`, `r13/machines-k1`; the handover lists exact SHAs) and `r13/compose`.
4. Tell the orchestrator you're ready. It then tells the old manager to stop, and you take over.

## Rules
- **No RunPod or paid calls of any kind, from you or your workers:** no api.runpod.io, no rest.runpod.io, no `astrid generate`, no `astrid machines`. Put this in every worker brief. Paid and live runs stay with the orchestrator.
- **Codex:**
  - always `-s danger-full-access`;
  - always `-c model_reasoning_effort=<level>` (high for Sol and Astra, medium for Terra, low for Luna), checked in the header;
  - Luna sub-agents for reading and mechanical checks;
  - `agents.max_threads` sized to your CPUs.
- **Concurrency:** about one Codex worker per CPU. Keep watching load and disk.
- **Focused proofs only;** the test lane runs full suites on hosted CI.
- **Git:**
  - no push to `main`, `cand/*` or Release 12 branches;
  - no force-push, no rebase;
  - never read `.env`, credential files or `~/.codex`;
  - no AI model names in commits or PRs.
  - Commit trailer: the one your session's system prompt gives.
- **Merging:**
  - you merge cards into `r13/machines` and push it;
  - before each landing, merge `origin/r13/compose` into the card;
  - send the orchestrator the SHA and the `machine.py` functions changed. The orchestrator merges into `r13/compose`.

## Reporting
Short messages to the orchestrator:
- when ready;
- at each merge, with the SHA;
- when blocked.

Lead with any decision you need.
