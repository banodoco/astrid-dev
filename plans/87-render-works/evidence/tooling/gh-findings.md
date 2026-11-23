# GitHub findings (r6 tooling) - read-only, 22 Nov 2026

Raw JSON: ~/tooling/gh/

## Task 1: issues #1238, #748, #1253 (banodoco/astrid-dev)

### #1238 - bug: timelines visualize fails the whole timeline on one stale asset
- State: open. Labels: bug. Author: AstridPseudon. Opened 2026-11-21. Comments: 0.
- Symptom (verified): 615-clip timeline, `canonical registry asset '<id>' contains retired media locator field(s): file`. Also reported, not reproduced: CanonicalizationError 4.79 MB over 4 MB limit; `--mode inputs` returns no frames on a large timeline.
- Fresh-project composed case (verified): same error as #748 (`installed registry discovery refuses explicit import or pack roots`).
- Cause: no file:line cited in the body.
- Fix direction (from body): one stale asset must not block all frames; windowed/range viewing without canonicalising the whole document; error should name the supported repair for a retired locator field.
- Linked PRs/branches: none. Cross-references only to #748, #1253, #1276 (issues).
- Next: no assignee or milestone recorded; no comment asks for action.

### #748 - Composed timeline visualization fails installed registry discovery while inputs mode works
- State: open. Labels: plan:59. Author: peteromallet. Opened 2026-11-16; last update 2026-11-21. Comments: 1 (AstridPseudon, 21 Nov: reproduced on fresh Release 13 macOS install, 6-clip timeline; links to #1238).
- Cause: body says the error comes from the installed-mode guard in `remotion_runtime.py` that rejects nonempty explicit import or pack roots. Body states the source of a `PYTHONPATH`/`ASTRID_PACKS_PATH` value is not established (the pack host env did not have them). No line number given.
- Fix direction (from body): trace env and registry config across the composed visualizer's process boundaries without recording secrets; keep the provenance guard (no blanket allow of arbitrary roots); add tests for composed-under-installed, inputs-mode parity, and rejection of untrusted roots.
- Linked: cross-referenced by #755 (closed PR, "Release 14 is stability and elegance: Plans 59, 39 and 13 join it", merged 2026-11-16), #761, #1238, #1253, #1276. No cross-references from other repos in the timeline.
- Next: no assignee recorded in the body fetch; no PR found that claims to fix it.

### #1253 - bug: every timeline render is refused on an installed release
- State: open. Labels: bug. Author: AstridPseudon. Opened 2026-11-21. Comments: 0.
- Symptom (verified three times): `capability 'rendering.render' exited 1 ... rendering.remotion does not support this render request; reason: runtime validation consumer context differs`. Disk not the cause.
- Cause (traced in code, not tested, per body): `_validated_runtime` in `astrid/core/rendering/remotion_runtime.py` about line 1267 requires the rendering process env to match a variant recorded at Runtime launch. Runtime up three days; a workspace pack in a user packs folder may matter.
- Fix direction: render works; if refused, error names the differing variable (expected and actual) and the supported repair (e.g. restart Runtime); failed runs record the reason in events.
- Linked: cross-referenced by #748 only. No PR/branch.
- Next: no assignee, no comments.

## Task 2: searches (org:banodoco, plus repo-scoped where noted)

Hits per query (number, state, gist):
- "retired media locator" / "retired locator" / "media locator": only #1238 (open, the stale-asset bug).
- "timelines visualize": #1238 (open); #798 (open, release:15, visualize is hard to read: internal IDs, tiny legend, false dead-air alarms, uncopyable next command); #761 (open, release:15, >40 flags in one flat list); #1320 (open, plan:81, "renderer lease channel closed" after ~57 s); #771 (open, release:15, ranged render shows wrong moments: visualize treats clip's first frame as timeline zero); #760 (open, renderer download failure reported only as lease channel closed); #748 (open); #1260, #1276, #799, #758 (open, peripheral).
- "composed": #748, #734 (open, planned, R14 live-scene composed capture fails), #1167 (closed PR, Plan 72 composed review snapshot parity), #95 (closed PR), astrid-agent #355 (open PR, Plan 55 D9 hash observation - not related).
- "audio excerpt": only #1260 (open, idea: cut footage by its transcript; says the proposed cut "is checked against the audio", and that nothing checks cuts against audio today).
- "waveform": only #864 (open, H3_AV deep review), unrelated.
- "timelines words": #773 (open; words stored twice on different clocks; task C3 adds `timelines transcripts import/show`, does not rewire `timelines words`), #1260 (open), #1241 (open, word-level timings from built-in transcribe).
- "words --json": #1260 (open), #798 (open). No issue mentions `timelines words --json`.
- "timelines show": #1261 (open, flat timelines miss the batch route; notes `timelines show --as code` has no write counterpart), #773, #1246 (open, failed commit leaves timeline stuck), astrid-app #338 (closed PR), astrid-dev #352 (closed PR).
- "50 clips": no relevant hit (noise: "50" numbers). "timelines show truncated/silently/limit" : only #796 (coordination issue) and noise.
- "page": #1240 (open, release:15, media list returns 50 rows plus a cursor, CLI has no `--cursor`/`--all`; reported, not reproduced). Other hits are unrelated UI "page" text.
- "motion window", "frame window", "sweep", "visualize window": no issue text about the 3 s / 1 s / 30 s / 12-frame / 90-frame caps. Hits are unrelated (e.g. #1271 frame hold, #761 mentions frame flags only). "MAX_FRAMES_PER_PAGE": zero hits. "12 frames", "90 frames", "3 seconds" + visualize: no relevant hit.

Coverage answer for the four gaps (from search):
- (a) no audio-excerpt command for agents: no issue found. Closest is #1260 (transcript-based cut editing, which mentions audio checking as a proposal, not an excerpt command). Likely a gap (inferred from search, not exhaustive).
- (b) visualize window caps (motion 3 s, frame 1 s, scan 30 s, 12-frame pages, 90-frame sweeps): no issue found that names these caps. Nearest: #761 (flag sprawl, "one clean frame at a time, a review page of a range"), #771 (ranged render wrong moments), #1238 (asks for windowed viewing). Not covered by name.
- (c) `timelines show --json` silently paging at 50 clips: no issue found. #1240 covers the same 50-row-plus-cursor pattern for `media list` only. Gap (inferred).
- (d) `timelines words` with no `--json`: no issue found explicitly. #773 and #1260 discuss `timelines words` but not its output format. Gap (inferred).

## Task 3: open PRs in banodoco/astrid-agent matching visualize|locator|registry|managed_timeline|composed (title or branch)
- Open PRs total: 17 (both pages checked). None match these terms in title or head branch.
- Open PR list for reference: #510 fix31-sdk-reader-compat; #475 easy wins Release 15; #467 p77/sl-3c; #459 fix18; #458 fix17; #455 at1.10; #454; #453; #452; #450 readiness fake HTTP; #408 LS-15; #402 oracle-freeze; #382 K1a; #361 LS-12; #358 release/14/plan-55; #355 D9 hash observer; #353 D9 real CPU floor.
- Note: a closed PR #478 "Release 14: land the Plans 59/64/65 integration (Agent)" matched "visualize window" in search, but it is closed.
