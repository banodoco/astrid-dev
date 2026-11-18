# Inputs — H3 composable core

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 18 November 2026 in the Plan 59 session, the owner asked for this plan. Their words: "if we're doing something for historical reasons, why don't we just update it to use the current way"; "a generalizable tool on top of MiniMax… really elegant"; tool sets, then a general skill, then problem skills like Recast with templates, applied to other problems such as endless continuation. They asked for it to be "ready to go as another plan". D3 to D5 decided the same day (below). Next: the owner greenlights the scope.

**Prior art:**
- **The request already has the model's shape.** `request.v2.json` holds timeline and reference items, per-item `edit[]` grants, and `hard` and `latent_pin` fields that nothing uses ([direction review §1](research/direction.md)).
- **The compiler is route-shaped.** `request_v2.py` `branch_for` returns one of four routes. `compile.py` has `_compile_native`, `_compile_lanpaint`, `_compile_native_masked_edit`, `_compile_character_swap_v2`, `_compile_native_v2` and `_compile_generation`. `spec.py`'s `_from_v2` accepts one bounded video source at frame 0 and image references only.
- **Continuation is not a time-masked V2V edit.**
  - At defaults the captured graphs run Existing Video mode: a 39-frame motion context taken from the decoded source audio-video feeds one active extension block (six are wired, one is active), with joint audio, then a stream mux ([critique](research/critique.md)).
  - The shared builder's V2V path has no such context. It also rejects a source shorter than the target and holds audio at 0.
  - Porting that stage is the real work ([research/continuation.md](research/continuation.md)).
- **End frames.** H3's last latent token spans four frames, so only composition can guarantee exact pixels. `MiniMaxH3AddGuide` resolves negative indices against the sampled latent, so Astrid resolves "last delivered frame" itself and binds a soft guide there.
- **Community.** Nekodificador's NKD Event Curve synthesises an audio guide and attaches it through `MiniMaxH3AddGuide`. It isn't timed text (GPL-3.0, released 15 November, with no independent quality evidence). His MiniMax Guides nodes are a convenience layer over the stock node. Timed text prompts exist only as community workflow strategies, with no evidence that H3 isolates text to frames ([research/community.md](research/community.md)).
- **Briefs.** The Plan 59 shot plan (`timelines shots plan`) already stores intent, inputs, takes and status per shot ([direction review §4](research/direction.md)).
- **Skills.**
  - The general H3 skill is 357 lines and teaches v1 first.
  - Recast is a good problem guide, but it carries tool workarounds and route names.
  - No endless-continuation skill exists.

**Approach:** finish the model that request v2 already has: one resolved job, one compile call made of ordinary lowering functions, one capability table, and templates over that. Alternatives considered:
- **(a) Presets as a code layer over routes.** Rejected: it encodes the routes again.
- **(b) A new request language.** Rejected: v2 already says it.
- **(c) A planner or workflow engine over briefs.** Rejected: the agent chooses, and the tools check.
- **(d) Keep the captured continuation workflows as the only path.** Rejected: it keeps the two-slot and fixed-size limits.
- **(e) Reuse `hard: false` on timeline items for guides.** Rejected: omitted `hard` already serializes as false on exact placements, so it can't mean soft. A new `role: guide` is used instead.

**Challenge:** Reviewed — Fable's direction review of 18 November 2026 ([research/direction.md](research/direction.md)) read Plans 64 and 65, the H3 pack on `release/14/main` and the Recast skill on `release/14/plan-59`. Accepted:
- the exact/soft split as the core axis;
- the three default rules in place of preset code;
- one record and compiler;
- the capability table;
- the guide lowering as the plug point for community tools;
- continuation as a ported motion-context stage;
- the dry run printing the resolved job;
- templates with named holes and a fill-from-shot command;
- one identity break.

Its changes to Plans 64 and 65 are applied.

**Astra critique.** The independent Astra critique of 18 November 2026 ([research/critique.md](research/critique.md)) checked the draft against the code with three Luna helpers. Verdict: revise before greenlight.
- **Accepted:**
  - an explicit `role: guide`;
  - porting continuation's active Existing Video path, with differences listed before code;
  - `-1` as the last delivered frame;
  - exact start with a guided end, and exact interior or end stills deferred;
  - deleting the LanPaint row;
  - a lifecycle of intent, then measured inputs, then one resolved job;
  - grants keeping strength, seed, occurrence and references together, with the polarity stated;
  - the source-labelled capability table added to `describe`;
  - three separate dry-run fields and the 1, 4, 4, 4, 4 token widths;
  - the fill contract;
  - keeping the #863 workaround until a recipe reproduces it;
  - installed recipe files in the example test;
  - a review stop after CC-1;
  - continuation as its own phase, a one-block limit, and the two-phase estimate.
- **Also accepted:** the Plan 64 SR-2, SR-4 and SR-5 corrections.
- **Rejected:**
  - the scan of every refusal string (dropped, as the critique also advised);
  - the prescribed tuple of steps (dropped);
  - keeping the captured workflows as fallback fixtures, and preserving Plan 65 D1. Both were overruled by the owner in D3 and D5.
- **Cut, as the critique advised:** shot-plan schema changes and automatic take recording.

**Proof and limits:** CPU only (D1). Because of D3, the old workflows are gone before the live test, so the live test compares the port with today's saved takes rather than with a fresh run of the old workflows. Proof covers compiled graphs, refusals, the dry-run record, template admission and a cold read of the skill. Not covered, and left to the owner's live test:
- whether the ported continuation looks and sounds like the captured one;
- guide adherence;
- how well Event Curve audio guides work.

**Review rounds:** Recommend 1. This replaces the pack's compiler and request identity, and it's the base for every future H3 skill. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: the owner starts a run after Plans 59, 64 and 65.

## Owner decisions

- **D1 — CPU only (decided 18 Nov 2026, owner in the Plan 59 session: "we're not going to do a GPU test. This is just CPU… We'll do a test afterwards").** No task claims a machine or spends money.
- **D2 — finish the model rather than keep routes (decided 18 Nov 2026, owner: "if we're doing something for historical reasons, why don't we just update it to use the current way").**
- **D3 — delete the captured continuation workflows in this plan (decided 18 Nov 2026, owner: "delete it ASAP… we already have it saved in GitHub… in the history").** CC-7 deletes them once the port passes its CPU proofs, with no live comparison first. The CPU parity list against their active path is the only check before deletion.
- **D4 — one clean break in request identity, now (decided 18 Nov 2026, owner: "we should make a clean break now… who gives a fuck about keeping things of the past").** The break happens in Plan 64 SR-1, the first task to land. After it, no plan preserves old digests: changed fixtures are regenerated in the same commit, with reasons.
- **D5 — drop Plan 65's continuation work (decided 18 Nov 2026, owner: "let's drop this plan 65 work and the continuations workflow as well").** Continuation gets size, and any reference count, from CC-7. This reverses Plan 65's earlier D1.

## Source identities

Planning snapshot: `astrid-agent` `origin/release/14/main` at `9f614dff` for the H3 pack, and `origin/release/14/plan-59` for the Recast skill and shot plan. The pinned ComfyUI is `6bfaacc`; the H3 motion pack is `361624fb`. At dispatch, record the release, its `release/<NN>/main` SHA, the Plan 64, 65 and 59 merge SHAs, and the `release/<NN>/plan-66` head.

## References

- [Direction review](research/direction.md), [continuation research](research/continuation.md), [community capabilities](research/community.md), [Astra critique](research/critique.md).
- [Plan 64](../64-h3-speaker-references/plan.md), [Plan 65](../65-h3-dynamic-size/plan.md), [#866](https://github.com/banodoco/astrid-dev/issues/866) (build the invocation once; superseded by CC-1 and CC-7), [#863](https://github.com/banodoco/astrid-dev/issues/863) (still-to-clip preparation; stays open until a recipe reproduces the four-frame silent hold).
