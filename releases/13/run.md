# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (18:00 UTC Sat 14 Nov): read this first

**No fixed freeze time; freeze when proven. R13 scope is CLOSED (17:52). Review gate: an Astra finding blocks only for a user-hittable money, custody or generate-path failure in R13. The checklist after the freeze: evidence/live/final-live-checklist.md.**
- **Compose head 941fca2a4.** Proving now, one worker per branch:
  - **batch A**, lanes 87b8a5850 → comfy-source 2451d9ca6 → timeout c0da1b2d0 → W2 ec264e87b (W89). Then **W2 is measured live** (verify_models seconds), and that decides W3.
  - **phase 4**: the manager's next SHA (3cf6da2e + R4.L + R4.M + the recommended P4.7.1 wording). App via the P4.8 worker; Pinokio's sentence via me.
- **Last rounds:**
  - hostwedge round 4 (cells, kept as built);
  - httpj round 4 (machines, saved-cap recheck only; about 19:00);
  - W3 round 4 (opt-in; the omitted projection becomes False);
  - W4 round 2 (cells, the idle-release race; deferred to the next plan if not through both reads at the freeze).
- **Live:** 0 pods; $84.22.
- **Waiting on Hannah:** the W3 default (best decided after the W2 number), the PR banodoco/astrid-dev#648 merge, and optionally the P4.7 wording (the recommendations ship meanwhile) and the review gate.

### Timeline
No fixed clock (Hannah, 14:05 Sat): freeze when every item is proven, then the CI comparison, the live repeat (evidence/live/final-live-checklist.md), and publish only on her go. The earlier timeline and stream tables were removed at 17:55 Sat as stale; the history is in decisions.md.

### Rules in force
- **Tests:** no worse than R12 `main`, test by test, on hosted `int/r13` CI. No local full suites. Managers run focused proofs only.
- **Codex:** always pass `-c model_reasoning_effort=…` (`high` for Sol and Astra, `medium` for Terra, `low` for Luna). Until 16:13 every worker ran at `none`.
- **Codex safety:** every brief forbids RunPod calls and `astrid generate` or `machines`. Paid steps stay with me.
- **Reviews:** Astra for rigour and robustness; Opus for structure, taste and feel.
- **Disk:** prune old install homes and data dirs before every live round (I deleted `home-b3`, the Stage 1 uv cache, at 14:20 Sat to free space for W1; the next install re-downloads packages). A VibeComfy clone mirror is at `/home/user/wt/vc.git`.
- **Review gate (17:52 Sat):** an Astra finding blocks only if it names a money, custody or generate-path failure a user can hit in R13; everything else is a deferred.md row.

### Group B (after the candidate)
T7 (the wait reason reaching the CLI), T8 (Runtime blocker list), T10 and T11 (now IN R13: warm models and the default project via Plan 20 phase 4), T13 (CPU journey), T14 (catalog dry-run corpus), Astrid `models.lock.json` to the same model record, the Plan 50 revision.

