# Direction review: is the H3 work heading toward an elegant agent toolset?

Read-only review, 18 Nov 2026. No tests, runs or edits. Sources: Plans 64 and 65 on astrid-dev main; `astrid-agent` `origin/release/14/main` (`9f614dff`) for the H3 pack; `origin/release/14/plan-59` for the Recast skill, which is not on release main yet; the two Plan 66 research notes, `continuation.md` and `nekodificador.md`, as completed at 15:20.

## 1. Verdict

**The direction is right and the plans do not get there by themselves.** The proposed core (canvas, timeline, references, permissions, prompt) is close to correct, and most of it already exists in the request. What is missing is behind the request: one resolved job and one compiler. Plans 64 and 65 each move a step toward that, and each also adds new route-shaped structure that Plan 66 would have to undo.

**The request is already the proposed model.** `request.v2.json` is a media list: each item is `role: timeline` (with `at`, `range` and `edit[]` permissions carrying stream, interval, mask, strength, seed and guides) or `role: reference`. It even has `hard` and `latent_pin` fields on timeline items that nothing uses yet. So Plan 66 is not a new request design. It is the removal of what stands between that request and the model:

- **Four representations.** Request v1 (`operation: edit | continue | generate`, a route named in the request), request v2, `H3Spec` in `spec.py`, and Plan 64's new `GenerationInputs`.
- **A narrow waist that discards the model.** `spec.py` `_from_v2` accepts one bounded video source at frame 0, image references only, no `hard`, no `latent_pin`, and fails anything else as "outside SPEC-MIN".
- **Route dispatch.** `request_v2.branch_for` returns `source_free | audio_only | extension_context | source_backed_v2v`; `compile.py` has one compiler per route (`_compile_native`, `_compile_lanpaint`, `_compile_native_masked_edit`, `_compile_character_swap_v2`, `_compile_generation`) and roughly sixty hand-written refusals.
- **A route flag in the request.** `continuation: true` selects the captured workflows. In the core model a continuation is simply a clip placed at 0 with a longer duration.

**Where the plans drift.**

| Drift | Where | Why it matters |
| --- | --- | --- |
| Route rows in the limits table | Plan 64 SR-2: "Character Swap images/videos 1/1", "Continuation images/videos 2/0" beside the model's 9/3/3 | Model facts and "what this lowering can't do yet" are different things. Mixed, the table becomes the route list again. |
| Route-shaped job record | Plan 64 SR-3: `GenerationInputs` has `source_edit` and `adapter` optional blocks | It is the one resolved job in all but name. Named by route, it will be reshaped in Plan 66. |
| Exact start image as a one-route special case | Plan 64 SR-4: "source-free route only", "generation runs as it does today", then paste the still over frame 0 | The model never sees the still as frame 0, so frame 1 can jump. `inputs.md` says the opposite (lower to the frozen-frame mechanism). The two files disagree. See section 4. |
| Fixed audio kept as an edit binding | Plan 64 non-goals; the `use: conditioning | replacement` classification | Fixed replacement audio is a placed audio item. Classifying it at normalization is a workaround for not saying so. |
| Soft guides excluded outright | Plan 64 non-goals: no `MiniMaxH3AddGuide`, no timeline image off frame 0 | Per the Nekodificador note, AddGuide is exactly where the community capability attaches (section 2). |
| Investment in the workflows to be retired | Plan 65 D1 and DS-4: size bindings plus a nine-case matrix on both captured continuation workflows, with new recorded digests | Half a day of work and new fixtures pinning the thing Plan 66 removes. |
| Digest preservation as a design constraint | Both plans: `model_tags` kept "only so digests don't change", `use` kept out of identity bytes | The pack is `status: experimental`, version 0.1.0. Each plan pays a compatibility tax that one deliberate break would end. |
| Hand-written messages | SR-4: `timeline images are only supported at frame 0`; compile errors naming "LanPaint", "SPEC-MIN", "native KSamplerSelect contract" | An agent cannot act on internal names. `spec.py` `_fail(code, message, path, fix)` is the right pattern and is used in one file only. |

**Agent-unfriendly surfaces today.** The general H3 skill is 357 lines, and about two thirds is machinery an agent never chooses (resume journals, worker attestation, receipt states, LoRA checksums). Its request section teaches v1 first. Limits are restated in prose per route. `generate describe --entry h3` returns the entry's plain inputs, not what a request may contain.

## 2. The right core abstraction

**One sentence:** a job says what is placed on the output, what the model may look at, and where the model may change things; everything placed and not opened for change is returned exactly.

Stated minimally:

- **Canvas:** size, duration (frames at 24 fps, audio at 48 kHz).
- **Placed items (exact):** video, still or audio at a time. They own their span of the output.
- **Conditioning (soft):** anything the model looks at. Untimed: references (image, video with soundtrack, audio). Timed: guides (image, clip or audio at a frame) and, if a node supports it, timed prompt segments.
- **Change grants:** stream, interval, optional region, strength. Uncovered time is generated by default; covered time is kept by default.
- **Prompt, model (base, adapter, turbo), sampling (seed, steps).**

**Critique of the proposed five nouns.**

1. **The exact/soft split is the real axis, and "timeline" hides it.** The first-frame research found precisely this: composition gives pixel exactness, AddGuide gives time-positioned influence and no guarantee. A "soft timeline item" and a "reference" are the same kind of thing (conditioning), differing only in whether they have a time. The existing `hard` boolean on timeline items is the natural spelling: `hard: true` is placed, otherwise it is a guide. I would not add a third top-level list.
2. **Permissions need one default rule, not a separate section.** "Placed is kept; uncovered is generated; a grant opens placed material" makes continue, start image, start plus end, inpaint and redub fall out with no preset code at all. v2's per-item `edit[]` already expresses grants. Keep it.
3. **The internal object is an ownership map.** For every output frame, pixel and audio sample: kept from item X, or generated. The compiler resolves the request into that map plus an ordered conditioning list, then lowers. That is the one record (`GenerationInputs` renamed and reshaped), and it is what a dry run should print.
4. **Audio must be a stream with its own intervals.** The V2V node has one `audio_strength` scalar for the whole clip. The compiler should hide that: any audio grant sets the scalar to 1 and composition restores kept samples. Plan 64 SR-5 already does this; it should be stated as the general rule, not a masked-edit case.
5. **Leave out of the core:** multiple outputs and variations (the agent submits N jobs with N seeds), multi-pass chains (`sampling_passes` in `spec.py` is orchestration; it belongs above the job), size presets, a second model. Model choice stays a setting; Character Swap is an adapter plus a recipe, not a route.

**Lowerings, and how a community capability plugs in.** The compiler is one builder with a short ordered list of lowering steps. Each consumes one feature of the resolved job and adds nodes:

| Job feature | Mechanism |
| --- | --- |
| References | `MiniMaxH3ReferenceToVideo` slots and prompt tags |
| Placed video or still, with grants | Source latent plus `H3V2VGranularFractionalDenoise` noise mask; composition paste-back |
| Audio grants | `audio_strength` 0 or 1; composition splices kept samples |
| Guides | `MiniMaxH3AddGuide`, chained per guide (negative index gives an end frame) |
| Generated time after a placed clip (continuation) | Motion-context stage: `MiniMaxH3StartMaskedContext` plus chained `MiniMaxH3GeneratedAVMaskedContext` blocks (39-frame context, 8-tick audio feather), then stream mux |
| Adapter | LoRA loader in the model chain |

Each step declares what it accepts. The union of those declarations, plus model facts read from the pinned node schema, is the capability table. Refusals are generated from it. A new capability is then: one new item kind or field, one lowering step, one row in the table, one skill recipe. No route is touched because there are none.

**The Nekodificador capability is not timed text prompts.** `nekodificador.md` identifies it as NKD Event Curve (GPL-3.0, released 15 Nov, no independent quality evidence): a curve of events is synthesised into an audio waveform and attached with `MiniMaxH3AddGuide` at a frame. His MiniMax Guides nodes are a convenience layer over the same stock node. For Astrid that is an audio guide item whose asset was produced by a curve tool. It needs the guide lowering and nothing else in the core. This makes the guide lowering the highest-value missing mechanism: it also yields first and last keyframes, mid-shot keyframes and audio-driven picture. Timed text exists only as community workflow strategies (one structured prompt with timed clauses, or conditioning chosen per sampling window); the note found no evidence that H3 isolates text to frames. Do not add a timed prompt field before choosing one of those mechanisms. Two of his other controls (audio shift curve, ControlNet ranges) run along sampling progress, not clip time; they are sampling settings and must not be drawn on the timeline.

**Risks in the proposal I would not wave through.**

- **Continuation is not a time-masked V2V edit.** `continuation.md` traced both captured graphs: they hand a 39-frame context from the source into a starter and six chained audio-video blocks, with joint audio. The shared builder's V2V branch has no such context, rejects a source shorter than the target and holds audio at strength 0. So continuation is expressible as placement in the request, but its lowering is a motion-context stage that has to be rebuilt inside the shared builder. "Retire the captured workflows" therefore means porting that stage, not deleting it. Equivalence to today's output is unproven until a live comparison; keep the captured bundles selectable until then.
- **Latent granularity leaks.** H3 tokens span 1, 4, 4, 4, 4 frames, and a grant touching any frame of a token opens the whole token. Composition restores exactness, but the dry run must show the effective generation boundary, or agents will be surprised by seams.
- **Duration rules leak too** (frame counts of 17k+5, trained around 124 to 362 frames, trim after sampling). The canvas should accept seconds and report the sampled and delivered frame counts.

## 3. The agent surface, by the owner's four layers

### Layer 1: tools

**Exists and is sound:** one request document; `astrid generate video --entry h3` with `--dry-run`; `generate describe`; `media mask` with `--preview-on`; `media trim`, `media crop --remove-bars`; `timelines visualize`, `timelines transcripts`, `timelines shots plan`; `tasks show/cancel`.

**Missing or weak, in priority order:**

1. **One compiler behind the request** (section 2). Until then every tool answer is "depends on the route".
2. **A dry run that returns the resolved job.** Canvas, sampled and delivered frames, per-stream kept and generated intervals after token rounding, effective reference rows with their prompt tags, which mechanisms were used, warnings. Plan 64 SR-6 and Plan 65 DS-4 each add a slice of this; it should be one printed record.
3. **Introspection from the same table the compiler uses.** `generate describe --entry h3 --json` should return model limits, accepted item kinds and which features are available. Today limits live in prose in the skill.
4. **Uniform errors:** code, request path, the limit broken, a fix. No internal names.
5. **Preparation gaps the Recast skill works around with FFmpeg:** still to silent 24 fps clip (astrid-dev#863), browser copy of a lossless take (#864). The first disappears once a placed still is a real item.
6. **Take inspection as a single step:** transcript plus strip of a returned take. Today it is three commands the skill chains by hand.

What makes this elegant for an agent rather than a human: one shape to learn; every rule checkable before spending (dry run costs nothing); refusals that say what to change; and an answer to "what can I do" that cannot drift from what the compiler does.

### Layer 2: the general H3 skill

**It exists as a file and does not yet do this job.** `astrid/packs/h3_av/docs/SKILL.md` documents the pipeline and its evidence chain, teaches v1 with a route field, and lists per-route limits. It does not teach composition: there is no statement of the placed/conditioning/grant model, no "these five recipes are the same request with different items".

**What it should be (about a page and a half):** the model in three rules; the item kinds; how to dry-run and read the result; how to ask the tool for limits; five to seven recipes as tested request examples (continue, start image, start plus end, regional inpaint, redub with fixed audio, speaker reference, character swap). `test_skill_examples_admitted.py` already keeps examples honest; presets can live here as examples rather than as a code layer. Runtime, resume and attestation material moves to a reference page.

### Layer 3: problem skills (Recast)

**Recast is a real problem guide, and a good one.** It plans in the cut first, makes voice before picture, picks the least invasive method per shot, records plans on shots, and names pitfalls with evidence (window length and filler words, last syllable clipped, wrong voice slice).

**It leaks tool detail in three places,** each a symptom of a layer 1 or 2 gap:

- Its method table maps to routes ("Continuation", "Lower-face mask with fixed replacement audio"). With one request these become recipe names from the general skill.
- It carries tool workarounds: the FFmpeg still loop, 24 fps range snapping, lossless viewing copies, lead-in handling.
- It restates request mechanics (`"1/6"` seconds, mask and guide fields) that belong in the general skill.

Minimal fix: after Plan 66, Recast keeps method choice, order of work, checks and pitfalls, and links to recipes by name. No rewrite before then.

### Layer 4: other problem skills, e.g. endless continuation

Nothing exists. What it needs from the tools, and what is planned:

| Need | Planned? |
| --- | --- |
| Continue from a returned take without re-encoding loss or manual trimming | No. Today the skill says to `media trim` when stream durations block reuse. |
| A stated, machine-readable context window: how much tail the model reads, the usable range of each take | Partly. `h3/take.json` has a usable `range`; lead-in is continuation-only. |
| The same references and voice across every segment, declared once | No. This is a chain concern above the job; a small shared "cast" block in a chain file, or just the agent reusing ids. |
| Seam handling: overlap, and audio continuity at joins | No. |
| Drift checks per segment (identity, voice, transcript) in one step | No (see layer 1, item 6). |
| A chain record: which take continues which, placed on the timeline in order | Partly. Shot plans record takes; nothing records lineage. |
| Start plus end bridging to land on a target frame | Needs the guide lowering. |
| More than six context blocks per job, or a clean hand-off between jobs | No. The captured graph fixes six blocks; the ported stage should take the count from the canvas. |
| Budget and stop conditions across N jobs | Machine spend caps exist; nothing per chain. |

The first two are tool work worth doing; the rest belongs in the skill itself or in later issues. I would not build a chain orchestrator: an agent looping over one well-behaved job is the design.

## 4. Briefs and templates

**A brief belongs in the core, and it mostly exists already: it is the shot plan.** On the Plan 59 branch, `timelines shots plan set/show/list` stores per shot a method, intent, check, `inputs.references`, `inputs.masks`, `inputs.voice` (media and range), takes with what each covers, and a status; `plan list` reports unplanned, invalid and not-approved shots. That is a structured brief. It lives at the timeline layer, which is the right place: a brief describes a shot, and H3 is one way to make it. I read this from the Recast skill text; I did not inspect the shot-plan code.

**The request alone is not enough, and the brief must not become a second request.** The request describes one job. A shot often needs several jobs (voice, then mouth, then a lens) plus checks and approvals, and that state has to live somewhere other than the agent's memory. But if the brief starts carrying intervals, masks geometry and strengths, it becomes a fifth representation. The split:

| | Brief (shot plan) | Request |
| --- | --- | --- |
| Says | What the shot is, who speaks which line, which references, what is kept and what is made, how to judge it | Exactly one job |
| Read by | Agent, owner, `plan list`, `visualize --shot-plans` | The compiler |
| Holds | Named inputs, ordered steps (each a template name), takes, status | Placed items, conditioning, grants |

**Minimal brief shape** (existing fields, plus the two marked new):

- `intent`, `on_screen`, `line` (text stays in the voiceover binding);
- `keep` / `make`: one plain sentence each (new, optional; today this is implied by the method letters);
- `inputs`: references, masks, voice slice, source range;
- `steps`: ordered template names (new; replaces the `method=LM,R` letters, which only Recast understands);
- `check`, `takes`, `status`.

**Templates.**

- **What:** a v2 request with named holes, for example `${source}`, `${source_range}`, `${mouth_mask}`, `${voice}`, `${line}`. Filling is plain substitution of brief inputs. No conditionals, no template language; a variant is another file.
- **Where:** core recipes (continue, start image, inpaint, redub, speaker reference, character swap) in the H3 pack beside the general skill. A problem skill ships its own in its skill folder: a brief template (the fields to fill per shot) and any request templates specific to its steps.
- **How they are validated:** the existing `test_skill_examples_admitted.py` pattern, extended: every shipped template is filled with fixture values and must normalize and dry-run compile. The normalizer already rejects unresolved placeholders, so a half-filled template cannot be submitted.
- **The one tool:** `generate video --entry h3 --template NAME --from-shot SHOT --dry-run` fills the template from the shot's brief and prints the request and resolved job. The same command without `--dry-run` runs it and records the take on the shot. Missing inputs are reported by name.

This makes problem skills thin as the owner wants: Recast becomes the order of work, the judgment calls and pitfalls, a brief template, and step names. Its seven-row method table turns into a choice among templates.

**What I would not build:** a brief-to-request planner that decides the method, a workflow engine over steps, or brief validation beyond "the template's holes are filled". The agent chooses; the tools check.

**What this means for the plans.**

- **Plan 66:** add templates and the fill command (small, once the single compiler exists), add `steps` to the shot plan, and ship the core recipes as template files. Essential, but after items 1, 2 and 5 below; templates over routes would just encode the routes.
- **Plan 64 SR-7 and Plan 65 DS-5:** write the new recipes as request files with holes that the admission test fills, not as prose examples. No other change.

## 5. Recommendations

### Plan 66 (essential now)

1. **One resolved job record and one compiler.** Request v2 normalizes into the record (canvas, placed, conditioning, ownership map, prompt, model, sampling). `branch_for`, the per-route compilers and `H3Spec`'s single-source waist go. Refusals come from the capability table.
2. **Capability table = model facts plus per-lowering declarations.** Model facts are read from, or tested against, the pinned node schema. It feeds admission, `describe` and error text.
3. **Guide lowering (`MiniMaxH3AddGuide`)** for image, clip and audio at a frame. This is the plug point for Event Curve, end frames and keyframes. CPU proof is wiring only; adherence is a live question.
4. **Continuation by placement.** Drop the `continuation` flag from the documented request; a clip shorter than the canvas means "generate the rest". Port the motion-context stage into the shared builder as a lowering (this lifts the two-image-slot and fixed-size limits for free). Keep the captured bundles until a live comparison passes, then delete them and migrate the fixtures `continuation.md` lists. This is the largest item in the plan; size it honestly.
5. **Dry run prints the resolved job;** `describe` prints the table; errors use code, path, limit, fix everywhere.
6. **Rewrite the general H3 skill** around the three rules; v2 only. Ship the recipes as template files, add the fill-from-shot command and `steps` on the shot plan (section 4). Trim Recast to a thin guide plus its brief template.
7. **One deliberate request-identity break,** recorded once, instead of preserving digests through each plan. v1 is accepted by translation only, or dropped.

### Later issues (not Plan 66)

- Timed text prompt segments, once a verified node exists.
- Event Curve asset tool, after its license and schema are checked.
- Endless continuation skill, plus "continue from a take" and take lineage.
- One-step take inspection.
- Normalized mask coordinates (see below).
- Captured continuation deletion, after the A/B.

### Changes to Plan 64

1. **SR-3: name the record by the core model, not by route.** Fields for canvas, placed items, keep map (video mask artifact, audio kept intervals), conditioning rows, prompt, model, sampling, in place of `source_edit` and `adapter` blocks. Same work, no later reshape.
2. **SR-2: split the table.** Model limits in one block; the Character Swap and continuation rows marked as lowering limits that Plan 66 removes.
3. **SR-4: resolve the contradiction between `inputs.md` and `tasks.md`, and define the rule generally.** A placed still is exact at its frame. The paste-only version guarantees frame 0 and nothing about frame 1; if that is accepted for now, say so in the skill and in the dry run. The refusal for other frames should come from the table ("no lowering for a placed still at frame N yet"), not a fixed sentence.
4. **SR-5: state the audio rule generally** (any audio grant regenerates the stream; composition restores kept samples), and treat fixed replacement audio as a placed audio item in the record, even if the request spelling stays as is.
5. **Do not extend `spec.py` in both directions** more than SR-1 strictly needs; it is the layer Plan 66 removes.

### Changes to Plan 65

1. **DS-4: bind size on the captured continuation workflows and stop there.** Drop the nine-case matrix and new recorded digests, or defer small-size continuation to Plan 66's lowering. This reverses part of D1, so it is the owner's call.
2. **Call it the canvas in the record** (`size` and `frames` together), so Plan 66 does not rename it.
3. **`mask.canvas`:** workable, but normalized 0 to 1 coordinates would make a mask independent of size and are simpler for an agent. Not worth blocking Plan 65; file it.

### Order

Plan 64 SR-1 to SR-3 (with the record renamed), then Plan 65, then Plan 66. If only one thing changes in the existing plans, make it the SR-3 field names.

## What I could not establish

- Whether a motion-context stage rebuilt in the shared builder matches the captured workflows' output. Wiring can be compared on CPU; quality cannot.
- Whether Event Curve, or AddGuide adherence generally, works well with the Ref2VA weights Astrid uses.
- Whether an exact end frame is achievable: the last latent token spans four frames, so only composition can guarantee it.
- Anything about output quality: nothing here was run.
