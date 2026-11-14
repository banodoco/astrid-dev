# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (17:00 UTC Sat 14 Nov): read this first

**No fixed freeze time. Freeze when every item is proven. Then: the frozen head's CI comparison; the live repeat (all five cells plus three h3 modes, more steps for edit and v2v, one FRESH download through fetch-models --apply, warm reuse timing with `models.trust_unchanged` on); then Hannah's go.**
- **Compose head 941fca2a4.** Ready, in test lane proof:
  - **batch 1:** lanes round 5 (with the file_fact passthrough) → comfy-source 2451d9ca6 → W3 round 3 (opt-in `models.trust_unchanged`, per error-model.md:90);
  - **hostwedge** 1505a379c (machines OK; Astra W84 and paired W85 running);
  - custody-helpers d89e9fc5b;
  - **phase 4** bea57349 (delta W82). Then R4.J (MCP census: audio and failure on MCP, distinct tool names) and R4.K (seed_used=0, the receipt bug) on its branch.
- **Still building:** machines httpj round 4 (pacing recheck; cold release for old journals), W2 (phase timings), W3 round 3; cells W4 (local idle release).
- **Live:** 0 pods; $84.22. W1 baseline: same-pod t2i 4m35s.
- **Waiting on Hannah:** the P4.7 wording list; W3 default (off, per the contract, unless she rewrites the clause); merging PR banodoco/astrid-dev#648.

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

