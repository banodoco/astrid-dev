> Historical research, not instructions. Where this differs from the current plan, inputs or tasks files, those win.

# Handoff check: Plans 64, 65 and 66

Read-only, 18 Nov 2026. Nothing run. Plans read at `cb6621d6` in `/home/user/work/recast/plans6465` (the coordinator says this matches main at `f893151d`). I read every plan and task file for the three plans and checked the two Luna reports against them and against the pinned node source.

## 1. Verdict

**The detail would survive a handoff. The reasoning would not, and one stretch of the sequence is wrong.**

- **Detail: strong.** The task cards are unusually precise: named functions, node wiring, test cases with frame numbers, refusals with wording. A neutral executor could build each card as written.
- **High level: buried.** `plan.md` for Plan 66 still describes the model in the earlier vocabulary (canvas, placed items, conditioning, grants). The three families, the place → guide → reference ladder and the six mechanisms appear only in `research/levers.md` and in one paragraph of `inputs.md`. The tasks then speak of "lever kinds" without the plan ever defining them. An executor would implement the cards and miss the invariants that should decide the cases the cards do not cover.
- **Thirteen research files carry advice that has since been reversed,** including two of mine. Nothing marks which statements still hold.
- **Sequencing: mostly right, with three problems.** Templates and the skill are written before the continuation, bridge and insert work, so bridges and inserts end with no recipe and no line in the skill. Phase 2 waits on the skill for no technical reason. And there are 18 working days across the three plans before a single render.
- **Is this the right way to reach the end state?** Yes for the order 64 → 65 → 66: Plan 64 delivers what the film in Plan 59 needs first, and its record and table are named so Plan 66 extends them. The risk is not the order. It is that everything is proven by compiling only.

### The Lunas' claims, checked

| Claim (hand-1) | Verdict |
| --- | --- |
| Source-free image rule contradicts itself | **Confirmed.** Plan 64 `plan.md` says "Generation needs no image"; `inputs.md` still says "Retain the image prerequisite on source-free generation". |
| Paired soundtrack capacity is missing and could admit unbindable requests | **Overstated.** Soundtracks pair one-to-one with videos, so three videos bound them. The only real gap is whether soundtrack time and standalone audio time share the 15-second audio total. One sentence fixes it. |
| CC-1.3's combined-request proof cannot pass before CC-2 | **Mostly wrong.** That combination (placed clip, region grant, audio grant, three images, speaker clip) is all Plan 64 work and should already compile. Keep the proof: it is the guard against routes returning. Only its escape clause needs rewording. |
| CC-2 claims to be the whole table before later kinds exist | **Confirmed, minor.** Also true: it lists `control` and `phase` though neither is built. |
| Completion line says every still holds 4 frames | **Confirmed.** CC-8 is correct (1 or 4); the completion line is stale. |
| Plan 64 SR-4 points at the wrong Plan 66 task | **Already fixed** in the current text. |
| Task-id line omits CC-9 | **Confirmed.** |
| CC-7a depends on CC-6 needlessly | **Confirmed.** |
| Skill draft contradicts the cards | **Confirmed, and more serious than rated.** The draft uses `settings.loras`, `role: control`, `phase` and `${hole}` in YAML. The cards use `settings.adapters`, no control, and JSON files with `{"$hole": …}` markers. The page that the small-model test validated is not the syntax that will ship. |

Two more that neither report caught:

- **The `continuation` flag is decided both ways.** CC-1's lowering table says "From CC-1.2 the `continuation` flag is accepted but selects nothing". `inputs.md` lists as *not taken* "the suggestion to make the `continuation` flag do nothing in CC-1".
- **Plan 64 SR-4 still says "audio is generated (strength 1, per SR-5)".** SR-5 now binds strength 0 and uses a time mask, and says a clip-wide 1 is wrong.

**hand-2 holds up.** I checked its ControlNet row against the node: `MiniMaxH3FunControlNetApply` takes `strength`, `start_percent`, `end_percent`, an optional control video and a mask, and returns a patched model. Its description says it applies "to a text-to-video model", so use with the Ref2VA weights is unverified. The node file has no negative prompt or guidance-scale input, as the report says. Its conclusion is right: all ten fit the six mechanisms, and the only thing outside is multi-pass work, which is a sequence of jobs.

## 2. Fixes, in priority order

**[S]** marks a change to sequencing.

### Must fix before dispatch

1. **Put the design on one page in Plan 66 `plan.md`.** Replace the "One model" bullets with:

   > **Levers.** Every control on a job is a lever of one of three families. *Output* levers (placed items and edits) decide what is in the result, and are the only ones that can be exact. *Context* levers (references, guides, the prompt) are what the model looks at. *Process* levers (adapters and settings) change how the model runs. Context and Process only influence.
   >
   > **One ladder for any asset:** place it (`role: timeline`, kept exactly), show it at a moment (`role: guide`, soft), or show it for the whole clip (`role: reference`, soft).
   >
   > **Three rules for Output.** Placed material is kept. Time nothing covers is generated. An edit opens placed material for change.
   >
   > **Six mechanisms.** The compiler merges levers into: the latent and its ownership mask; timed rows; untimed rows; the prompt text; the model chain; the sampler. Composition then restores every kept pixel and sample. A new lever adds a kind to the table and a function that feeds one mechanism. It never adds a request structure or a compiler branch.
   >
   > **Invariants.** No code names or classifies a kind of job. Only composition promises exactness. Astrid never silently moves what was asked for: a snap is shown in the dry run, and a mismatch is refused. Every limit an agent meets comes from the capability table, with its source.

2. **[S] Move templates and skills to the end.** New order for Plan 66: CC-1.1 to CC-1.4, RS1, CC-2, CC-3, CC-9, CC-4, CC-8, **CC-7a, CC-7b and CC-7c, CC-7d**, then **CC-5, CC-6**, then R. Change CC-7a's dependency from CC-6 to CC-3, and CC-5's from "CC-8, Plan 59" to "CC-7d, Plan 59". Add to CC-5: "Ship recipes for continue, bridge and insert alongside the others." The skill is then written once, against the finished system, and its cold-read test covers everything. If the owner prefers skills earlier, the smaller alternative is to keep the order and add "ship its recipe and its line in the skill" to CC-7a, CC-7b and CC-7c.

3. **Decide the `continuation` flag once.** Keep the task text and delete the "Not taken" bullet in `inputs.md`, replacing it with: "From CC-1.2 a continuation is chosen by the arrangement of placed items; the `continuation` flag is accepted and ignored until CC-7d removes it."

4. **Make the skill draft a source of structure only.** Replace the first sentence of CC-6's scope with:

   > `docs/SKILL.md` takes its structure and length from research/skill-draft.md (families, ladder, time, shared fields, kinds). Rewrite every field name and example to match the shipped schema: `settings.adapters`, no `role: control`, no `phase`, recipes as JSON files with `{"$hole": …}` markers, and stills holding one or four frames. Do not copy an unsupported field into the skill.

   The cold read in CC-6 already re-runs the five asks, which re-validates the page in its shipped syntax.

5. **Mark unbuilt kinds honestly, and add status.** In CC-2, after the list of kinds, add:

   > `control` and the `phase` field are listed as `unavailable`: a request using either is refused from the table. Every kind carries a status: `compiles` by default, `live-tested` only with a run reference and date, `unavailable` if no lowering exists. Each later card that adds a kind, field, limit or pair adds its rows and its `describe` fixture in that card.

6. **Remove the three stale lines.**
   - Plan 66 `plan.md` completion: replace "each come out pixel-exact, and the dry run shows each one's 4-frame hold" with "each come out pixel-exact (frame 0 and frame 51 hold one frame; frame 61 and the last frame hold their four-frame chunk, clipped at the end), and the dry run shows each requested frame, chunk and hold".
   - Plan 64 `inputs.md`: replace "Retain the image prerequisite on source-free generation and the existing adapter and continuation contracts." with "Generation needs no image (superseding the earlier decision to keep that prerequisite); the continuation contract is kept until Plan 66."
   - Plan 64 `tasks.md` SR-4: replace "audio is generated (strength 1, per SR-5)" with "audio is generated: the SR-5 audio mask is 1 over the whole clip, with V2V `audio_strength` 0".

7. **Mark research as history.** Add at the top of every file under `66-h3-composable-core/research/` and `64-h3-speaker-references/research/`:

   > Historical research, not instructions. Where this differs from the current plan, inputs or tasks files, those win.

### Should fix

8. **Keep CC-1.3's combined proof, reword its exit.** Replace "If a pair can't be combined yet, it gets a named capability refusal rather than a claim of composition." with "Every part of this request is Plan 64 behaviour, so it compiles. `compile_job` chooses lowerings from the features present, never from a classified shape."

9. **State the one place where arrangement matters.** Output currently has four preparations: a full-canvas source through the V2V node (edits and stills), and three motion-pack nodes (prefix, insert, bridge). The research in `mc-2.md` says these are the same latent-and-mask mechanism prepared differently. Add to CC-7a, under "Before writing code":

   > Check whether prefix, insert and bridge can be prepared by CC-8's full-canvas source with the V2V node and the audio mask, instead of the three context nodes. If the latent and masks are equivalent, use that one preparation and drop CC-7b and CC-7c as separate lowerings. If not, record why, keep all preparation choices in one function, and add table rows for each pair that cannot share a job (for example a continuation with an exact end still).

   This is unverified. It could remove most of phase 2, or it could confirm the current split. Either way it stops four quiet routes forming inside Output.

10. **One sentence on audio totals** in Plan 64 SR-2: "A video's enabled soundtrack and standalone audio clips share the 15-second audio total; soundtracks need no slot limit of their own, because each belongs to one of at most three videos."

11. **Fix the small text errors:** the Plan 66 task-id line (add CC-9); Plan 64 `plan.md` "Character Swap keeps its contract: one image and one video" (SR-2 now says at least one of each, more allowed); an estimate line saying the three plans total 18 working days of CPU work before any render.

12. **Keep the seams model-neutral.** In CC-2 and CC-5 add: "The `describe` capability format and the template commands contain nothing specific to H3." In CC-8 add: "Composition reads the ownership map and media files and imports nothing else from the pack."

### Owner's call

13. **[S] Two short live sessions.** One after Plan 64 (speaker reference, audio time mask, exact start) and one after phase 1's mechanisms (guides, interior stills), a render per new mechanism. The owner chose CPU-only plans; this places "afterwards" after each plan, not after all three. Without it, statement 9 below stays a label and nothing more.

14. **Arbitrary LoRA files.** The tested page lets an agent name any LoRA file. The plan allows only adapters declared in the table. The plan's choice is the safer one (pinned, checksummed, with a declared contract). If the owner wants undeclared files, that is a later row with status `compiles`, not a Plan 66 change.

## 3. Ten statements about the end state

Each is true of the plans once the fixes above are made, and each is meant to be arguable.

1. **There are no modes.** Continue, inpaint, redub, bridge and swap are words in templates and nowhere in code. The compiler never decides what kind of job it has. Exactly one function looks at how placed items are arranged, and it only prepares the latent.

2. **The model never keeps anything; composition does.** A mask protects the latent, which is not the same as returning your pixels. Exactness is a promise made after sampling by putting the original pixels and samples back. So every lever outside Output is soft, permanently, and no future node changes that.

3. **Six mechanisms are the whole compiler, and there will not be a seventh.** Latent and mask, timed rows, untimed rows, text, model chain, sampler. ControlNet, camera control, negative prompts, in-context LoRAs and audio-driven video all land in one of the six. Anything that does not is several jobs in a row, which is a skill.

4. **A new capability is one table row, one function and one template.** It changes no request structure, no other lever and no line of the compiler's core. If adding ControlNet needs more than a new `role`, a row and a function feeding the model chain, the abstraction has failed.

5. **Levers never know about each other.** Each one adds to its mechanism and reads nothing else. Every interaction between two levers is a row in the table that a person wrote down. There is no clever conflict resolution anywhere.

6. **The table cannot disagree with the compiler, because it is the compiler's input.** Admission, refusals, `describe` and the dry run all read the same rows. A lever that exists in the vocabulary but is not built says `unavailable`; it is never silently absent, and never silently accepted.

7. **There are two clocks and no field touches both.** `at` and `during` are time in the clip. `phase` is progress through denoising. Any future control over "when" is one or the other.

8. **An agent never learns H3.** It learns one page and reads `describe`. A small model must get from a described shot to a valid request using that page alone, and that is a standing test. If the page has to grow to explain a feature, the feature is the wrong shape.

9. **Allowed is not tested, and Astrid says which is which.** Every valid combination compiles. Only shipped templates are tested combinations. A kind is `live-tested` only when it cites a render. Until the first live session, every new mechanism is honestly a compile-only claim.

10. **None of this is H3's except the table and the lowering functions.** The vocabulary, the `describe` format, templates and composition are model-neutral, and a job's Output family is a small timeline. A second model is a new table and new functions. A take comes back as a clip on the span it was asked for.

## Not established

- Whether the full-canvas preparation can replace the three context nodes (fix 9).
- Whether ControlNet works with the Ref2VA weights.
- Output quality of any new mechanism.
