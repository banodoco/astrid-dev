# RS1 brief: review stop after WS-7b and LE-2b (Plan 56)

**Reviewer:** Codex Astra (the newest Astra ID the login accepts), via `codex exec`, read-only (`-s read-only`), at most one round. Commissioned by Plan 56's accountable agent (mailbox r15-lead, astrid-dev #1757).

**When:** as soon as Agent #599 (LE-2b) merges into astrid-agent `release/15/plan-56`. The Lead posts the exact heads in the commissioning message.

**Read (exact heads given at commissioning):** astrid-agent `release/15/plan-56` and VibeComfy `release/15/plan-56`. Plan: `plans/56-workflow-setup/plan.md`, `tasks.md` and `inputs.md` (decisions D1–D12) in astrid-dev.

**Question:** this is the point where unapproved node code is first refused at the target. Is the refusal sound? Review only these:
1. **Approval record and recipe shapes:** VibeComfy `vibecomfy/node_recipes.py` (canonical recipe, `recipe_sha256`) and `vibecomfy/node_approvals.py` (identity, `approval_sha256`, placement class, `_CONTEXT`); the Agent's use of them in `astrid/core/generation/node_approvals.py` (storage and `authorize_nodes`) and `comfyui_engine.py` (`extra.nodes`).
2. **Consent token:** the 12-hex token, `--consent code=<token>` checking (bound to what was shown; bare or stale returns `needs_consent` with the warning again), and the consent fix (`who: human`, `instruction` that shows the warning).
3. **Refusal at the target:** VibeComfy `node_packs/_install.py` (`validate_restore_approvals`, `restore_pack`, `_batch_restore_entry`, `_install_required_packs_impl`) and `commands/nodes.py` (`_cmd_nodes_restore`). Is anything cloned, fetched, checked out or pip-installed for an unapproved ref, on any path? Is a reviewed shipped-lock ref at its pinned commit the only thing that passes without a record? Are a changed commit, recipe or placement refused? Is any refusal silent?
4. **The controlled install path (WS-7b):** dry-run first, the protected-package check before and after each step, `requirements_txt` confined to the pack folder, `install.py` never executed.
5. **The tests:** do `test_install_script_never_executed`, `test_apply_refuses_unapproved_code` (or its equivalent), `tests/test_node_restore_approval.py` and `tests/core/generation/test_code_consent.py` exercise the real code path, or do they patch it out?

**Out of scope:** wording (LE-11), lookup (LE-4/5), the live SAM run (WS-L), the Plan 90 items.

**Output:** findings as rows `RS1.<n>` with severity (BLOCKING: wrong result, install of unapproved code, data or install damage, security hole; FOLLOW-UP; NOTE), file:line evidence, and a one-line proposed fix. End with PASS (no BLOCKING) or FAIL. Evidence, not a rewrite; no code changes.

**Gates:** RS1 gates LE-13 (P56-10), LE-17 (in P56-09) and WS-L.
