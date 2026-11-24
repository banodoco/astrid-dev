# Handover — Plan 89 (heavy saves in seconds)

**State on 24 November 2026.** Plan 77's save run landed the commit-store work in Runtime `release/15/main` (`24e2c929`, #109) and the Agent capture fix in Agent `release/15/main` (`a09ea669`, #571); App is re-pinned (`d53685f3`, #384). Plan 89 carries the loop: measure installed, fund the largest residual, repeat, until the median is at most 2 s to "Saved" with none over 4 s.

**Read first.** [`tasks.md`](tasks.md); Plan 77's save profile (Plan 77 `evidence/2026-11-23-sv3-profile`, not yet on main); [Plan 88's history-growth lines](evidence/2026-11-24-p88-history-growth/README.md): on stock `24e2c929` a fixed-size commit still grows steadily with accepted history (provider_commit 1.6 s to 32 s over about 30 batches, one 248 s outlier). So the work that remains is history scaling, not a single hot spot.

**Branches.** `release/15/plan-89` exists in astrid-runtime (`c9e535bd`: SV-L1 stage spans), astrid-agent and astrid-app. Open drafts that are not packets: Runtime SV-L6 `covers` index (#113, head `485f82b0`, installed measurement pending). Packet branches are `p89/<task id>` into `release/15/plan-89`.

**Not for packets.** Installed save measurements (SV-L4 and the loop), every real render, and anything that needs the heavy fixture stay in the orchestrator's lane. Post `READY-PROOF` for the proof you cannot run.

**Open threads.** SV-L7 (burst coalescing) is sized at 4 to 6 App days, if the existing step receipt and undo semantics suffice; no implementation is authorized until the Release 15 Lead's go. SV-L8 is investigation first.
