# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (19:00 UTC Sat 14 Nov): read this first

**No fixed freeze; freeze when proven. Scope closed except Hannah's calls (W4 is a must; h3first is pending her). Review gate in force. Two proof lanes:** the main test lane, and test lane 2 (session_011EzfW4KtCLNFrD7ct3Cu95, all new SHAs).
- **Compose a921b7dce** (plus auto-placement-timeout).
- **Ready:** W3 622ba8938 (Astra APPROVE).
- **Proving:**
  - batch A (lanes → comfy-source → timeout → W2 7e553baf7);
  - hostwedge round 4 (Astra APPROVE);
  - httpj round 5 3f67b3553 (Astra APPROVE);
  - phase 4 cf49d415, plus a docs commit coming (cancel command; honest i2v line);
  - W4 2ca1a8de1 (APPROVE), with warmrel5 fidelity fixes about 20:00.
- **Merge order:** batch A → W3 → hostwedge → httpj → phase 4 → W4. Then the W2 live measurement, then the freeze.
- **h3:** our i2v is a reference, not a first frame. Cells dry-runs the mask requests and builds h3first on a branch (ships if Hannah says so). The final checklist gains T1–T5.
- **Windows tester run (Hannah, tomorrow afternoon):** prep answers Q1–Q6 are in with the advisor; manifest `release: 13`; the SHA is checked via the doctor bundle.
- **Live:** 0 pods; $84.22.

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

