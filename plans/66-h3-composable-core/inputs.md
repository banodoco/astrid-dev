# Inputs — H3 composable core

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — Owner agreed on 27 November 2026 in ChatGPT to make 66 provider-ready and 67 a full default-companion and composable-pack proof, with NKD as the first real provider; both are allocated to Release 16 in the proposed brief. Earlier one-compiler and CPU-only decisions remain. Next: independent critique of the amended interface and release-base readiness; record the accepted scope/run start with the Lead.

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
  - exact start with a guided end. The owner then asked for exact stills at any frame, added as CC-8 (one frame at multiples of 17, otherwise a 4-frame hold);
  - deleting the LanPaint row;
  - a lifecycle of intent, then measured inputs, then one resolved job;
  - grants keeping strength, seed, occurrence and references together, with the polarity stated;
  - the source-labelled capability table added to `describe`;
  - three separate dry-run fields and the 1, 4, 4, 4, 4 token widths;
  - the fill contract;
  - keeping the #863 workaround until a recipe reproduces it;
  - installed recipe files in the example test;
  - a review stop after the CC-1 cards;
  - continuation as its own phase, a one-block limit, and the two-phase estimate.
- **Also accepted:** the Plan 64 SR-2, SR-4 and SR-5 corrections.
- **Rejected:**
  - the scan of every refusal string (dropped, as the critique also advised);
  - the prescribed tuple of steps (dropped);
  - keeping the captured workflows as fallback fixtures, and preserving Plan 65 D1. Both were overruled by the owner in D3 and D5.
- **Cut, as the critique advised:** shot-plan schema changes and automatic take recording.

**Lever abstraction and small-model tests.** Fable's levers note ([research/levers.md](research/levers.md)) groups every control into three families: Output (exact: place and edit), Context (soft: references, guides, prompt) and Process (soft: LoRAs, control, settings). The families share field names, and the denoising clock is a second time axis (`phase`). A one-page lever document was then tested on five creative asks with a small model in two rounds ([research/haiku-tests.md](research/haiku-tests.md)). In round 2 all five structures were correct. Accepted as a result:
- the capability table keyed by lever kind (CC-2);
- end-relative time in phase 1 (CC-9). Timed prompts were briefly here and moved to Plan 67 on 18 Nov, when the owner asked that Plans 64–66 cover only the existing tools;
- the tested page as the CC-6 skill draft ([research/skill-draft.md](research/skill-draft.md)).

**Functional review.** An independent functional walk-through of 18 November 2026 ([research/functional-review.md](research/functional-review.md)) traced five requests down to node inputs. The masked recast and the symmetric bridge are feasible as designed. All blocking and high findings are accepted, in [tasks.md](tasks.md#functional-additions):
- one ordered AV mask pair;
- separate permission and strength masks;
- occurrence bindings;
- exact per-channel verification;
- the bridge and prefix assembly contracts;
- clock transforms;
- resource reporting;
- pre-claim refusals for a late LoRA, a mouth edit inside a prefix, and ControlNet.

From the red-team review only these were taken: declared lowering dependencies, per-tag binding reports, refusal of per-grant seed or reference conflicts, and refusal of still collisions inside one chunk. The owner set the rest of that list aside for a later plan. Timed prompts and other community steering moved to [Plan 67](../67-h3-community-steering/plan.md).

**Restrictions review.** On 18 November the owner asked for every restriction to be justified or dropped. Fable's review is in [research/restrictions.md](research/restrictions.md). Its Luna helpers were blocked by the session's permissions, so Fable did the research directly. It found most limits came from Astrid using one node of the already-pinned motion pack. All ten edits are accepted:
- no image required;
- a time-varying audio mask via `MiniMaxH3SetAVNoiseMask`, so the model hears kept audio and several audio windows are allowed;
- regions may differ in interval and strength;
- audio strength anywhere from 0 to 1;
- bridges and inserts (now CC-7b and CC-7c);
- several voices bound by prompt text (no voice-to-face input exists);
- v1 deleted;
- adapters as table rows with declared input contracts;
- the 1, 4, 4, 4, 4 chunk pattern, so frames 0, 17, 34 and so on are single-frame pins;
- a source column on the limits table.

**Ambiguity pass.** Also on 18 November, one reviewer per task group read the final cards against the code, to make them safe for an implementer who knows far less than the planner: [Plans 64 and 65](research/ambiguity-64-65.md), [CC-1 to CC-3](research/ambiguity-cc1-3.md), [CC-4, CC-8, CC-5 and CC-6, plus the Plan 64 SR-5 audio wiring](research/ambiguity-cc4-8.md), and [CC-7](research/ambiguity-cc7.md).

Accepted:
- CC-1 split into CC-1.1 to CC-1.4, each mergeable on its own, with the callers to migrate listed;
- RS1 reviewing the integrated head after all four;
- CC-2's source fields and refusal pairs, and the `describe` JSON shape;
- CC-3's half-open intervals and persisting the view before cleanup;
- CC-4's exact guide wiring, with 1–4 frames using the first frame and `-1` resolved by Astrid;
- CC-8's chunk boundaries, confirmed from the model code;
- CC-5's JSON recipe files with `{"$hole": …}` markers, typed `--set` values and qualified names;
- CC-6's file list;
- Plan 64 SR-5 wired exactly: `MiniMaxH3SetAVNoiseMask` with only an audio mask, after V2V, with V2V `audio_strength` 0;
- CC-7 split into CC-7a to CC-7d. Prefix continuation is `MiniMaxH3ExistingVideoMaskedContext` at `insert_frame` 0; inserts share that node with a different assembler; bridges use their own node family. The 60-frame bridge example was invalid, and is replaced by 39 + 63 + 39 = 141 frames. Inserts must sit on multiples of 51, and a Character Swap adapter case was added to continuation and bridge.

Not taken:
- (resolved) From CC-1.2 a continuation is chosen by the arrangement of placed items; the `continuation` flag is accepted and ignored until CC-7d removes it. The captured bundle keeps continuation working until CC-7a replaces it;
- the suggestion to keep the captured workflows until a live comparison. The owner already decided D3.

Two owner choices raised by the pass were decided the same day: Plan 64 D4 (audio-mask edges) and Plan 65 D3 (rectangle edge ties).

**Split.** On 18 November the owner asked to break this plan into several. An independent review ([research/split-review.md](research/split-review.md)) checked the cut. Accepted:
- this plan keeps the core (CC-1.1 to CC-1.4, RS1, CC-2, CC-3, CC-9) plus composition by occurrence and exact delivery (new CC-10, moved out of CC-8), the template machinery and recipes for existing capabilities, and the base skill rewrite;
- guides and exact stills (CC-4, CC-8) become [Plan 68](../68-h3-guides-and-stills/plan.md);
- continuation, bridges and inserts (CC-7a to CC-7d) become [Plan 70](../70-h3-continuation-bridges-inserts/plan.md), which starts at this plan's contract review (28 Nov 2026);
- four reservations, the design file in the pack, three skill guards, RS1 here, and the programme's integrated review in Plan 67 R (28 Nov 2026);
- card ids unchanged.

**Provider seam readiness (27 Nov 2026; source-only):** Agent main `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` has `GenerationInputs` and `LIMITS` in `astrid/packs/h3_av/shared/generation.py` and H3's existing VibeComfy workflow hooks. The prerequisite integration [Agent #478](https://github.com/banodoco/astrid-agent/pull/478), `f6e629b31e0f7fe74c0cb809061c10b74a79a765`, is its ancestor (compare ahead 821, behind 0). Plan 65's historical task evidence still records red CPU/CI and earlier-head live receipts: completion status is not a current baseline. At dispatch record exact release/dependency identities and scoped baseline failures. Have an independent high-judgment reviewer check the CC-2 registration seam, stable snapshot, six mechanisms, pack-neutral receipt and 67 consumption against current source before freezing the contract. No independent review or tests have run in this planning update. See [67's dependency assessment](../67-h3-community-steering/inputs.md#provider-boundary-and-plan-17-dependency-27-nov-2026).

**Proof and limits:** CPU only (D1). Because of D3, the old workflows are gone before the live test, so the live test compares the port with today's saved takes rather than with a fresh run of the old workflows. Proof covers compiled graphs, refusals, the dry-run record, template admission and a cold read of the skill. Not covered, and left to the owner's live test:
- whether the ported continuation looks and sounds like the captured one;
- guide adherence;
- how well Event Curve audio guides work.

**Review rounds:** Recommend 1. This replaces the pack's compiler and request identity, and it's the base for every future H3 skill. Next: the owner confirms.

**Run start:** Pending — this plan runs in the H3 lane; its run starts when the owner records her go in the lane brief [releases/16/briefs/h3.md](../../releases/16/briefs/h3.md) (its "Owner's go" line). Next: the owner launches the lane.

## Owner decisions

- **D1 — CPU only (decided 18 Nov 2026, owner in the Plan 59 session: "we're not going to do a GPU test. This is just CPU… We'll do a test afterwards").** No task claims a machine or spends money.
- **D2 — finish the model rather than keep routes (decided 18 Nov 2026, owner: "if we're doing something for historical reasons, why don't we just update it to use the current way").**
- **D3 — delete the captured continuation workflows (now in Plan 70) (decided 18 Nov 2026, owner: "delete it ASAP… we already have it saved in GitHub… in the history").** Plan 70 CC-7d deletes them once the port passes its CPU proofs, with no live comparison first. The CPU parity list against their active path is the only check before deletion.
- **D4 — one clean break in request identity, now (decided 18 Nov 2026, owner: "we should make a clean break now… who gives a fuck about keeping things of the past").** The break happens in Plan 64 SR-1, the first task to land. After it, no plan preserves old digests: changed fixtures are regenerated in the same commit, with reasons.
- **D5 — drop Plan 65's continuation work (decided 18 Nov 2026, owner: "let's drop this plan 65 work and the continuations workflow as well").** Continuation gets size, and any reference count, from Plan 70 CC-7a. This reverses Plan 65's earlier D1.

- **D6 — live checks during the work (pending).** The handoff review ([research/handoff-review.md](research/handoff-review.md)) points out that many CPU days pass before any render. After the split into Plans 66, 68 and 70, the recommended points are three short live sessions, each with one render per new mechanism:
  - after Plan 64 (speaker reference, audio time mask, exact start);
  - after Plan 66 (a regression check of the shipped recipes);
  - after Plan 68 (guides, interior stills).

  The options are (a) keep everything CPU-only until all the plans are done (D1 as it stands), or (b) add those sessions, with small GPU spend and a budget set by the owner. Recommendation: (b), because nothing can be marked `live-tested` otherwise. Still pending the owner.

- **D7 — provider-ready core (owner direction, 27 Nov 2026).** H3 keeps semantic ownership and one typed capability/lowering assembly seam. 66 proves it with a separate fixture; 67 owns real installation, default companion selection and chained contributions. In the owner follow-up on 27 Nov, NKD is to ship by default with H3 without becoming H3's hard dependency. The provider seam advertises ordinary preprocessing tools as such, not invented levers; absence of the default provider cannot affect native requests. No new registry, generic API or Plan 17 dependency. Preserve CPU-only scope; the narrow contract is subject to independent review.

## Source identities

Planning snapshot: `astrid-agent` `origin/release/14/main` at `9f614dff` for the H3 pack, and `origin/release/14/plan-59` for the Recast skill and shot plan. The pinned ComfyUI is `6bfaacc`; the H3 motion pack is `361624fb`. At dispatch, record the release, its `release/<NN>/main` SHA, the Plan 64, 65 and 59 merge SHAs, and the `release/<NN>/plan-66` head.

## References

- [Direction review](research/direction.md), [continuation research](research/continuation.md), [community capabilities](research/community.md), [Astra critique](research/critique.md).
- [Plan 64](../64-h3-speaker-references/plan.md), [Plan 65](../65-h3-dynamic-size/plan.md), [#866](https://github.com/banodoco/astrid-dev/issues/866) (build the invocation once; superseded by the CC-1 cards and Plan 70 CC-7a), [#863](https://github.com/banodoco/astrid-dev/issues/863) (still-to-clip preparation; stays open until a recipe reproduces the four-frame silent hold).
