# H3_AV: where it should end up

Written 16 November 2026 from the Release 14 code, the node packs' own source, the live pilot notes and an independent critique. Nothing here has run on a GPU yet; what only a GPU run can settle is marked **open**.

## How we get there: one skill per kind of task, proven by an agent

For each kind of edit the Minkhole film needs there is one skill document. It takes an agent from "this clip, this intended result" to a reviewed take on the timeline: find the shot, know the words, choose the cut point, write the request, rent the GPU through Astrid, run, check, place, release the GPU.

Each skill is proven the same way. A fresh agent on the normal-task model gets the skill, the clip and the intended result, and nothing else. It rents a machine and does the edit end to end. Every place it stalls, guesses or needs help is recorded, and the tool or the skill is fixed at that place. Then another fresh agent tries, until one finishes unaided, and you review the take. Tool work happens only when a skill needs it.

The task skills, in order:

1. **A character says a new line by continuing the shot.** The three Morpheus clips: shot 02c (the long "You keep running tools..." line), shot 01 ("You have two options."), and the cut back to Morpheus in shot 04 ("who knows how to do everything...").
2. **A character says new words and the picture is kept.** One Morpheus line first; then any of the three where you prefer the exact picture.
3. **Something inside the picture changes** (the pill, a reflection). Outlined now, run when the edit reaches its first picture change on real footage.
4. **A still becomes a moving shot.** Outlined now; the two Neo reaction stills are the first candidates.

You expected about three clips. The dialogue work is exactly three clips, all covered by the first skill. The rest of the film is a different kind of work: six of the nine shots are stills.

## What H3_AV is, and is not

**It is** the pack that turns one edit request into one run of the H3 model. It does three things:

- **Continue** a clip: keep the start, generate what happens next, picture and sound.
- **Change part of a clip** and keep the rest: a region of the picture today, and after this work a span of the sound.
- **Generate** a new clip from reference images (including the character swap).

It prepares the inputs, runs on a rented GPU, puts the protected parts of the original back, and checks that it did.

**It is not** a transcriber, a mask maker, a timeline editor or a judge of whether the line sounds right. Those are separate things it uses.

## Three problems in the pack today

1. **It rejects real footage.** The Morpheus pilot was refused before renting anything: the Matrix clip is 23.976 fps and 1920×800, and H3 accepted only exactly 24 fps and 1024×576. Its error told the agent to run an ffmpeg command by hand, and that command would stretch the picture. This is being fixed now, because the first skill cannot run without it.
2. **It carries things that are not the product.** The LanPaint route cannot be reached by any request. An "audio only" mode is advertised and always errors. A "reference audio" setting is read by nothing. There are two request formats and two commands for the same operations.
3. **Its documentation describes machinery, not choices.** The skill links to pages that do not exist, and the older guides describe the unreachable LanPaint route as the next thing to try.

## How one workflow feeds another

Astrid already has the mechanism: any result is stored media, and a later step can name it with a **handle** (its digest, or "output N of run X") instead of a file path. H3 was the exception: it wanted a hand-written map of names to local files.

The Morpheus shot, as it should work:

1. **Find the shot.** `timelines show` says the clip uses the Matrix media, source time 81.05–84.30 s.
2. **Know the words.** Listen, and pick a cut point at a pause.
3. **Ask for the edit.** One request: continue this media from this range, he says the new line, total length. The source is named by handle and range; H3 cuts and conforms it itself, once.
4. **Run it.** `astrid generate video --entry h3` on the rented GPU. The take comes back as stored media.
5. **Check it.** Pull clean frames at the cut point and listen against the written line.
6. **Place it.** Add the take as its own clip above the shot, showing only the newly generated part, at normal speed, with the temporary voiceover silent over it. The original stays untouched underneath.

A mask works the same way: a mask's handle goes into the request where a mask file went.

## Continuing a clip and continuing a voice

They are the same operation. There is no separate voice route.

- The model hears the **last 39 frames (about 1.6 seconds)** of sound before the cut point. That is the only voice sample it gets, and the start must be at least that long. The "two options" clip in the cut is about 1.5 seconds, so its request takes a longer range from the source footage.
- The kept start still contains his original words, so on the timeline you use only the newly generated part.
- Continuation regenerates the whole picture after the cut point.
- **Open:** whether 1.6 seconds holds Morpheus's voice across a full line, and whether the long line fits in the 6.75 seconds generated for it.

## New words on the same picture

You asked whether the node packs can regenerate sound inside existing footage. **They already can, with the nodes we already pin, and without LanPaint.**

- H3 keeps the picture and the sound as two separate streams, each with its own mask, and its sampler honours each mask separately.
- The node pack behind our continuation graph has a node that sets a separate sound mask over time, and its documentation names "regenerate the sound while protecting the picture" as a use.
- Our masked edit already uses that pack and simply sets "regenerate sound" to zero. Nobody recorded why.
- So the change is in our own graph: put a sound mask over the chosen span, and optionally a small picture mask around the mouth over the same span. No pull request to anyone's node pack is needed, and nothing newer upstream changes this.

What LanPaint added on top is a special sampler that refines the edges of a regenerated span, and a blending step. That is why I would keep its graph a little longer, only as a worked example of edge handling, and delete it once the second skill's takes show our route is usable.

**Open:** whether the new words are intelligible, in his voice, and clean at both ends of the span; and whether the lips need the mouth region regenerated to match. The second skill's two takes (picture fully kept; mouth region regenerated) answer that.

## Any size

- **In:** footage of any size, shape and frame rate is accepted and conformed, with Fill or Fit stated and never a stretch.
- **Out:** the canvas is no longer fixed at 1024×576. The request states the shape it wants, usually the shape of where the take is going, and the pack picks the nearest size the model accepts. The model's own nodes take any width and height in steps of 32, so the canvas sides are multiples of 32, within the pixel budget we use today.
- **Fixed, because the model fixes them:** 24 frames a second, and frame counts on the model's own grid.
- **Open:** how well the model does on shapes other than 16:9. Nothing we could read says.

## Knowing the words, and asking Hivemind

Transcription is a reference page in the skills, as you decided. Today the honest version is: listen. One Whisper node is already pinned and returns plain text; if it runs on the worker it becomes a small included workflow for checking that a take said its line. No pinned node gives word timings, so cut points are chosen by ear for now.

Hivemind is Astrid's searchable record of what the Banodoco community actually does: Discord messages, shared workflows and curated answers. Anyone can search it with `astrid hivemind search`; login is only for contributing. For this work it had no report of word-level transcription in ComfyUI, shared H3 masking workflows but no report of clean speech replacement, mixed reports on reference sound (one of voice timbre carrying over, one of the reference being copied word for word), and single-user reports on automatic masks. The skills will tell an agent to search it before building or choosing an unfamiliar workflow, and to treat hits as leads.

## The skills

```
creative work (exists)                        "which pack does this job?"
└─ audiovisual editing (new)                  "what does this shot need?"
   ├─ a new line by continuing the shot       task skill 1
   ├─ new words, same picture                 task skill 2
   ├─ a change inside the picture             task skill 3
   ├─ a still becomes a moving shot           task skill 4
   ├─ knowing the words (reference)           listening; a transcript; the text check
   ├─ placing a take (reference)              the generated part, speed, the old voiceover
   ├─ H3_AV (rewrite, one screen)             "how do I ask H3?"
   │  ├─ requests (reference)                 one complete, tested example per operation
   │  └─ techniques (reference)               start clip, cut point, canvas, what goes wrong
   ├─ timeline, rendering, RunPod (exist)     placing, clean frames, renting the GPU
   └─ Hivemind (exists)                       what the community already does
```

Each topic has one home; the task skills link to the shared pages instead of repeating them.

## Does this cover the whole Minkhole edit?

It had not been checked; the first draft was built around one Morpheus line. The plan now carries a table of every need (each line, each picture change, each join, each still, and the handover brief's five techniques) against every step a task needs from the tooling.

Of 118 step-needs: 37 work today, 52 are fixed by this plan, 20 are being done under the Minkhole plan, and **9 are covered by nothing**. 30 can only be settled by a GPU run.

What nothing covers:

- **Motion from one still to another** (the opening, the hand reveal, the pickup). This is the largest gap: no H3 request expresses it. It is a decision for you before anything is built.
- **Word timings**, for cut points such as "who knows".
- **Two regions changed differently in one request** (the two glasses reflections). Two passes, one after the other, is the route the skill will teach.
- **A voice or video reference separate from the start clip.** Only worth building if the first takes show the voice does not hold.
- **Comparing takes side by side.** Listening and pulled frames for now.

A caution on how complete this is: the live work found six gaps on the first clip before any GPU run, and none of them was in the first draft. Expect a similar handful each time a skill first exercises something new.

## What each need should be

| Need | Answer |
|---|---|
| Choosing the task skill, the start clip, the cut point, the canvas | Skill |
| Judging voice, lips and continuity; when to retry or ask you | Skill |
| Checking the spoken words | Skill: listening now; a small text-transcription workflow if the pinned node runs |
| Giving H3 real footage of any size, frame rate and range | Small tool: H3 prepares its own source, once |
| Passing one workflow's result to H3 | Connect: H3 accepts the handles Astrid already has |
| New sound inside existing footage | Small tool: a sound mask in our own graph, on nodes already pinned |
| Finding the H3 entry when VibeComfy is not set up | Small fix: say what is missing instead of "unknown entry" |
| Placing a take on the timeline | Already exists (add and trim on the timeline); skill only |
| Where words live | Already exists (a transcript attached to the media) |
| Word timings; masks from a description | General to Astrid, under the Minkhole plan; not H3's |
| Longer voice context; a separate voice reference | **Open** until the first takes |
| The `astrid h3` command, "audio only", the unused reference-audio setting, dead links, the old guides | Delete (the guides only after their Minkhole script and shot notes are saved in the Minkhole plan) |
| The LanPaint graph | Delete after the second skill's takes |
| The second request format | One format is documented. The character swap keeps the second, as experimental. The rest of it duplicates the first: your decision whether to retire it now (recommended) |

## Decisions still with you

1. **Retire the duplicate parts of the second request format** now, or leave them undocumented. I recommend retiring them.
2. **Release 14 and reviews:** include this beside the Minkhole plan, with one short review after the footage change and one at the end. I recommend yes.
3. **How a take is placed for your review:** a stored alternate above the shot (recommended), or a local draft.
4. **Money for the trials:** inside your $25, a ceiling of $1.50 per agent trial (about an hour of the GPU that quotes $1.39 an hour), which buys 12 trials after the $3 pilot, with $4 in reserve. The ceiling is reset once the first run shows what a trial really costs.
5. **The stills:** use H3 only where one still is enough and decide the rest after the first try (recommended); build start-to-end motion into H3; or leave the stills as they are.
