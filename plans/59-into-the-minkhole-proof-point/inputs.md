# Inputs — Into the Minkhole proof point

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — Hannah's direction in the accountable session on 16 November 2026: deliver the video and, more importantly, a reusable workflow a weaker agent can run. Work through Astrid's tools; fix blockers at cause or file useful work that is too large; return creative choices to the owner. The [source brief](https://github.com/peteromallet/minkhole-h3av-handover) is also a source record.

**Prior art:** Existing timeline transfer, rendering and H3 tools are the starting points. In the current findings, Release 14 rejects the rough-cut archive; issue [#346](https://github.com/banodoco/astrid-agent/issues/346) has a fix on a Release 15 branch, being brought into `release/14/plan-59`. Preview/export disagree, fit is track-level, and clip crop is not editable. The composition source is consolidated on `banodoco/timeline-composition` branch `release/14/plan-59`. The owner approved the crop on 16 November after editor preview, composed frame and export agreed on the cut; four independent reviews completed and the fix is merged. The approved Astrid archive is on the working machine, and its permanent home remains an owner decision. Timed-word transcription is now built and merged, with offline proof only; it has not run on a real machine. The first H3 take is composed and structurally verified, but its words and creative quality await the owner. Reassess issues and source heads when each task begins.

**Approach:** Keep this as a live work loop rather than a fixed implementation plan. Start from the next creative result; extend the Astrid capability that owns each blocker; file a durable issue when the fix is too large for this run. The composition package is the shared appearance source; D3 records its current source home.

**Challenge:** Keep the task list intentionally short and mutable: only C1 is detailed; later creative tasks are one line each. A retrospective blocker log captures cause, decision, landing place and proof without maintaining a second backlog.

**Proof and limits:** The ten user-visible outcomes in [plan.md](plan.md#outcome-and-scope) are the acceptance picture. Evidence belongs beside the task and blocker as work proceeds. The plan does not claim completion from CPU fixtures where a real GPU result is required.

**Review rounds:** One owner review stop for the finished creative result; taste choices are brought back as they arise.

**Run start:** Started 16 November 2026 by Hannah in accountable session `session_011EzfW4BJ221kXBNRB4xQcG`. On 16 November, the owner extended this session's authority to update the plan, release brief and records, and to file astrid-dev issues without asking first. The session may dispatch work on the loop, create and push Release 14 plan/task branches, file listed issues after duplicate search, and use RunPod within the stated $25 total ceiling and split. Pull requests, merges into `release/14/main`, creative reviews and spend beyond $25 still require the owner's go. Advisor: none.

## Owner decisions

- **D1 — Release inclusion:** Decided 16 November 2026: yes, include in Release 14 (“add it to the release”). The release manager adds Plan 59 to the Included plans list in `releases/14.md`.
- **D2 — Shared appearance and migration:** Decided 16 November 2026: one placement function owned by the composition package is called by export rendering, editor preview and editing handles; delete their local copies. Fit is authored per clip, falling back to its track. Replace the implicit “geometry or crop means cover” rule by writing the choice explicitly once when an old project is opened.
- **D3 — Shipped composition package source:** Resolved in substance (16 November 2026): exact 0.0.17 source recovered byte for byte at AstridPseudon/timeline-hub commit `14628ad5d`. `banodoco/timeline-composition` branch `release/14/plan-59` at `2c0740a` merges that lineage with staging as 0.0.18, adds a placement oracle against 0.0.17, stamps the source commit into packed `package.json`, and adds CI. The package now builds from its owning repository. Owner decisions remain: whether this branch becomes `main`, the missing license field, and which stray branches and copies to delete. Only the owner deletes those branches/copies.
- **D4 — Budget:** Decided 16 November 2026: at most $2/hour; $3 pilot, $6 experiments, $4 retries, $3 fresh-agent trial, $9 reserve; $25 total. No other paid resource.
- **D5 — Review:** Decided 16 November 2026: one review stop is fine.

**Parallel work:** Automatic source conform is in Plan 60 RH-1. The first GPU take exercised the creation-time deadline and watchdog; the provider accepted the deadline and the watchdog acknowledged it, but provider termination was not observed because the machine was released first. Hivemind fixes are reviewed and merged.

## Source identities

Plan source: astrid-dev branch `release/14/plan-59`, based on Release 14. Product work uses each repository's `release/14/main` and its `release/14/plan-59` branch, with task branches as needed. At each task start, record actual base and dependency SHAs, dirty state and retained changes. Inspected planning snapshots: Agent `ab95803ce28fa51eec937b4074f5ec0f0439b98a`, Runtime `2537fed24385ec1c24f48a812e09af4bb63fb794`, App `0b6ef16152dc3fa11246ccc2007da630c66d1a1a`, VibeComfy `aee8bd825c619cfb516feb63d38f500aa4ddb4d7`, composition source `67b8aa3d0d6831d3e3504a340ff583c3da253707`. These are inspection snapshots, not dispatch pins.

The supplied rough-cut archive SHA-256 is `50e7bf1262f0b89bd95dcce5ee0edebf80eea7d446f6f8234c52f022a4110e2e`; source reference archive SHA-256 is `7a19fb1fc2253d8b6a39d8bd603d8b88bb0a6117d1cc1ac1f38ebf685658f8fb`. Shipped composition artifact SHA-256: `cdd89c78d18b4b437a03efd1fff081f1ce00ee448d644ef8360fc1937df60f0f`.

## References

[Source brief and archive instructions](https://github.com/peteromallet/minkhole-h3av-handover) · [Release 14](../../releases/14.md)
