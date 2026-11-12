# Machines lane: handover 2 (12 Nov 2026, 23:15 UTC)

From the machines manager session (Opus) to the same session after the switch to Sonnet. The rules are unchanged: `machines-session-brief.md`. Briefs, logs and reviews live in `/home/user/wt/briefs/wave3/`. Workers are in `/home/user/wt/c-*`, with run logs in `/home/user/wt/runs/*/codex.log`.

## Branches (banodoco/astrid-agent)
- **`r13/machines` `265a074d7`:** M1 merged. Nothing else is on it yet.
- **In `r13/compose` `e24853a88` (all merged by the orchestrator):** ble `4a9fb1e5f`, setupmsg `6536b50b3`, claimwait `53bb6406d`, claimbound `ee0508d9b`, ctrlc `10cef0670`, podwatch `1ef005ed3`, pwsoft `d3d20257e`.
- **K1 `r13/machines-k1`:** origin is `e2f616723`. Locally in `c-k1`, `8ba5c195a` holds round 2 plus compose merged in, not pushed. A Claude sub-agent is reconciling it (one reason vocabulary, compose's `PlacementReasonError`/`Reason`), uncommitted in `c-k1`. Its landing proof is the seven files in `machines-k1-reconcile.md`.
- **M2:**
  - M2a is `r13/machines-m2` `889312e1f`.
  - M2b is `r13/machines-m2b` `0b2398a1f`, which contains M2a. M2 lands as M2b.
  - Open: `tests/sdk/test_generation_target.py`. Compose fails 27 of it; Release 12 passes 38 of 38. Group 1 (8 failures, "preferences incomplete (missing budget_cap_usd)") is ours. **Ruling:** job admission must not require claim-time preferences; fix it in the product, not the fixtures.
  - My M2a-vs-M2b id comparison of that file is still running (scratchpad `gt-m2*.txt`).
  - On merging compose: take M2a's side in `cli.py` and `test_mcp_generation_parity.py`; I own the parity fixes there (project in `required`).
- **LT:**
  - The design is `r13/machines-lt` `58a7241c8` (`transitions.py` in core, `lease_states.py` in the pack, 571 table tests).
  - The wiring is **running** (detached Codex Sol) in `c-ltw`, local branch `r13/machines-lt-wiring`. Its step 0 merges are done (`d9e53adcf` = design + M2b + compose + M4 card 5). ETA about 04:00.
  - Brief: `machines-lt-a-wiring-run.md`. Log: `/home/user/wt/runs/lt-wiring/codex.log`; the `exit` file appears when it finishes.
  - Then one wiring review: Astra, or an independent Opus if Codex is down.
- **M4:** `r13/machines-m4` `354b3d1c8` (card 5). Card 6/6b, parked red, is `d900965e8`; its row moved into LT. M4 lands with LT.
- **REST v2:** **running** (detached Codex Sol), started 23:05, ETA about 01:00. Brief: `machines-restv2.md`. Log: `/home/user/wt/runs/restv2/codex.log`.
  - Astrid side: `c-v2`, local branch `r13/machines-restv2` on compose `1feb10a6b`.
  - runpod-lifecycle side: `/home/user/wt/c-lc`, local branch `r13/rest-v2` from `f2948817`; the worker commits locally there.

## Next actions, in order (orchestrator: v2, K1, M2b, LT, M4)
1. **v2,** when done:
   - Push runpod-lifecycle `r13/rest-v2`. Hannah authorised this in-session (that branch only; never main, no force-push, no rebase). The repo is attached; its clone is `/home/user/runpod-lifecycle`, with the worktree in `/home/user/banodoco/runpod-lifecycle`.
   - Check `grep rest.runpod.io` is empty, and that `rest.runpod.io` is dropped from both `pack.yaml` allowlists.
   - Commit the Astrid side, merge compose in, and push `r13/machines-restv2`.
   - Run one Astra pass, then send the SHAs to the orchestrator (it runs a live claim, a job and a release on v2). Send the lifecycle SHA to cells, so they can re-vendor VibeComfy's wheel.
2. **K1:** when the sub-agent reports green, commit, re-run the landing proof, merge into `r13/machines` with `--no-ff`, push, and send the SHA (machine.py functions: `_checkpoint_installed` and failure release).
3. **M2:** fix group 1, run the per-id comparison against compose, merge compose in, land, and send the SHA.
4. **LT wiring:** prove it, review it, merge K1 and v2 in, and land it with M4.
5. After that, LT issues are #617 and #616; M3; M5–M7 if time allows.

## Rulings in force
- **LT guarantees only:**
  - b1–b5;
  - b6, durable deadlines released on host start;
  - b7, release annotation inside the retry boundary;
  - b8, cancel_requested in startup recovery;
  - b10+b13, the lock held for transitions only, and a late create journalled (T5);
  - b12, never waiting behind an abandoned observation.
- **LT test rule:** the encoding reproduces today's field values. Tests may change only for owner-removed behaviour or for raw acquire→settle setups.
- **Deferred to Plan 39:**
  - b9 cede write-ahead (#617), b11 zero-POST (#616), the publication latch LT-b (#611), the binding fence (#618);
  - the lifecycle deadline hook (#619), the legacy `runpod.provision`/`session` actions (#627, excluded from LT by name);
  - the watchdog limits (#628), and the opaque setup 409 (#631).
- **Decision 1:** no provider observation under the owner file lock; one bounded observer per post-create call, with a deadline no later than paid expiry; an abandoned read-only thread is allowed only if it holds no lock and never mutates.
- **Pod watchdog:**
  - It terminates through the shared exact-release URL.
  - PW-soft: denied or unknown authorisation means host custody plus a warning.
  - The probe premise was wrong, since v1 GET has no `actions` field. The v2 card adds `probe_status`, and the orchestrator verifies it live.
- **Claim:** waits for capacity by default, bounded by `--capacity-timeout`, which defaults to `--for`. The timeout refuses in one line.
- **Lint gate:** only ruff BLE001 and F821, and mypy attr-defined, name-defined and call-arg. Clear them in the files a card touches. `worker_owner.py`'s BLE001 (6→8) and attr-defined (5→7) are in LT.
- **Reviews:** Astra (or an independent Opus) reviews money and custody changes once. Another round only if it finds a money bug.

## Cut and waits
- **Cut decision: Fri 10:00 UTC.** K1, M1 and M2 must be in compose and green. M1 is in.
- **Hannah:** nothing open; Codex credits and lifecycle push are both resolved.
- **Orchestrator:** live verification of v2 and of the watchdog probe; the cells re-vendor.
