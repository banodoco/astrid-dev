# H3_AV: where it should end up

Written 16 November 2026 from the Release 14 code, the node packs' own source and the live pilot notes, and revised after two independent critiques and your decisions. Nothing here has run on a GPU yet; what only a GPU run can settle is marked **open**.

## How we get there: one skill per kind of task, proven by an agent

For each kind of edit the Minkhole film needs there is one skill document. It takes an agent from "this clip, this intended result" to a reviewed take on the timeline: find the shot, know the words, choose the cut point, write the request, rent the GPU through Astrid, run, check, place, release the GPU.

Each skill is proven the same way. A fresh agent on the normal-task model gets the skill, the clip and the intended result, and nothing else. It rents a machine and does the edit end to end. Every place it stalls, guesses or needs help is recorded, and the tool or the skill is fixed at that place. Then another fresh agent tries, until one finishes unaided, and you review the take. Before any trial that rents a GPU, a fresh agent first passes a rehearsal that rents nothing: find the skill, write the request, get a ready dry run, and practise checking and placing with media that already exists. Tool work happens only when a skill needs it.

The speed-up is one named setting: the Pika Labs 8-step Ref2VA file, without an A/B test. LightX2V remains an option only where its variant matches the base; CFG other than 1 is refused by name until a real CFG graph exists. Paid trials should examine the community leads on reference voice, Ref2VA joins and LightX2V loading as leads, not facts. A check against the publishers' documentation found the reference base is the right one for every route; the documented way to carry a voice (a reference audio clip, or a reference video with its sound) is exposed only on character swap, which is the gap the voice skill has to close. No rental begins until the creation-time deadline is independently reviewed; every machine must carry that deadline and the existing pod watchdog.

The task skills, in order:

1. **A character says a new line by continuing the shot.** The three Morpheus clips: shot 02c (the long "You keep running tools..." line), shot 01 ("You have two options."), and the cut back to Morpheus in shot 04 ("who knows how to do everything...").
2. **A character says new words and the picture is kept.** One Morpheus line first; then any of the three where you prefer the exact picture.
3. **Something inside the picture changes** (the pill, a reflection). Outlined now, run when the edit reaches its first picture change on real footage.
4. **A still becomes a moving shot.** Outlined now; the two Neo reaction stills are the first candidates.

You expected about three clips. Three clips have Morpheus speaking on screen, and the first skill covers all three. Three other lines ("You take the blue pill.", the creature line, "And see just how deep the minkhole goes.") are narration over pictures and stay as voiceover. Only the first two skills must be proven for this plan to be done. The rest of the film is a different kind of work: six of the nine shots are stills.

## What H3_AV is, and is not

**It is** the pack that turns one edit request into one run of the H3 model. It does three things:

- **Continue** a clip: keep the start, generate what happens next, picture and sound.
- **Change part of a clip** and keep the rest: a region of the picture today, and after this work a span of the sound.
- **Generate** a new clip from reference images (including the character swap).

It prepares the inputs, runs on a rented GPU, puts the protected parts of the original back, and checks that it did.

**It is not** a transcriber, a mask maker, a timeline editor or a judge of whether the line sounds right. Those are separate things it uses.

## Three problems in the pack today

1. **It rejects real footage.** The Morpheus pilot was refused before renting anything: the Matrix clip is 23.976 fps and 1920×800, and H3 accepted only exactly 24 fps and 1024×576. Its error told the agent to run an ffmpeg command by hand, and that command would stretch the picture. Automatic source conform now exists on Plan 59 task branch `p59/h3-conform`; its reviewed integration remains part of RH-1.
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

You asked whether the node packs can regenerate sound inside existing footage. **The nodes we already pin support it. We still have to build the route, put its result back together and prove it; none of that exists today.** It needs no LanPaint and no pull request to anyone's node pack.

- H3 keeps the picture and the sound as two separate streams, each with its own mask, and its sampler honours each mask separately.
- The node pack behind our continuation graph has a node that sets a separate sound mask. Its own example regenerates all of a clip's sound with the picture protected; a chosen span is something we construct.
- Our masked edit already uses that pack and simply sets "regenerate sound" to zero. Nobody recorded why.

What we build, precisely:

- **The request** is the existing edit request with a sound change over a time span. The new line goes in the prompt; no new field.
- **The sound mask** is built on the sound's own grid, 40 steps a second, so nothing is approximated from the 24-a-second picture. A span edge that falls between steps moves inward by less than 25 ms, and the dry run says so.
- **"Picture kept"** means the decoded picture of the result equals the picture we started from. The model decodes and re-encodes on the way, so we take the picture from the original when nothing in it may change, and the existing check compares the decoded frames. It does not mean the original file's bytes.
- **The join** is a 20 ms fade at each end, entirely inside the span you allowed. Sound outside the span is untouched, and the check enforces exactly that.

What LanPaint added on top is a special sampler that refines the edges of a regenerated span. Its graph is kept, only as a worked example of edge handling, until the second skill's takes show our route is usable; then it is deleted.

The second skill makes two takes: sound only with the picture fully kept, and sound plus a small mouth region. The first proves the mechanics; unchanged lips may not suit the line. The skill is done when you accept one of the two.

**Open:** whether the new words are intelligible, in his voice, and clean at both ends of the span; and whether the lips need the mouth region regenerated to match.

## Any size

- **In:** footage of any size, shape and frame rate is accepted and conformed, with Fill or Fit stated and never a stretch.
- **Out:** the canvas is no longer fixed at 1024×576. The request states the shape it wants, usually the shape of where the take is going. The model's own nodes take any width and height in steps of 32, so one rule picks the size: the nearest shape whose sides are both multiples of 32, within the pixel budget we use today. The dry run reports the size it chose. 16:9 still gives 1024×576, and the Morpheus pilot asks for 16:9 explicitly.
- **Fixed, because the model fixes them:** 24 frames a second, and frame counts on the model's own grid.
- **Open:** how well the model does on shapes other than 16:9. Nothing we could read says, and it stays unproven unless money remains for a run on one.

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

It had not been checked; the first draft was built around one Morpheus line. The plan now carries a table of the film's needs (each on-screen line, the narration, each picture change, the joins, the stills, and the handover brief's five techniques) against every step a task needs from the tooling.

The table is an inventory of methods and gaps. It is not a share of the film delivered. Of its 119 cells, 53 work today, 53 are fixed by this plan, 5 belong to tasks in the Minkhole plan, and **8 are covered by nothing**. 16 can only be settled by a GPU run, and none has had one.

Said plainly: this plan qualifies the three speaking-face clips. **The still-heavy majority of the cut remains unqualified**: six of the nine shots are stills, and three of those are sequences of several images (four in the opening, three for the red pill, six in the close). A reference image guides a generated shot; it is not guaranteed to be its first frame.

What nothing covers:

- **Motion from one still to another** (the opening, the hand reveal, the reflection change, the pickup, the run, the logo). The largest gap: no H3 request expresses it. You decided to try one still first and decide this afterwards; until then those shots stay as stills. An older stand-alone end-frame workflow exists and is where that work would start.
- **Word timings**, for cut points such as "who knows". By ear for now.
- **Two regions changed differently in one request.** The film does not need it: the glasses shot changes the left reflection and protects the right one, which is one edit.
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
| Placing a take on the timeline | The commands exist (add, then trim); the full method, including silencing the old voiceover over just that span, is rehearsed at no GPU cost before the first paid trial |
| Where words live | Already exists (a transcript attached to the media) |
| Word timings; masks from a description | General to Astrid, under the Minkhole plan; not H3's |
| Longer voice context; a separate voice reference | **Open** until the first takes |
| The `astrid h3` command, "audio only", the unused reference-audio setting, dead links, the old guides | Delete (the guides only after their Minkhole script and shot notes are saved in the Minkhole plan) |
| The LanPaint graph | Delete after the second skill's takes |
| The second request format | One format is documented. The character swap keeps the second, as experimental. The rest of it duplicates the first and is retired, as you decided |

## What you decided, and the money

You decided on 16 November: the `astrid h3` command goes; any size in, with Fill by default; transcription is a skill reference; the duplicate parts of the second request format are retired; this is in Release 14 with one short review after the footage change and one at the end; a take is placed as a stored alternate above the shot, with a local draft only as fallback; and the stills are tried with one still first.

**Money.** $25 is the hard total for everything, including the Minkhole plan's own fresh-agent trial on a different film. The pilot remains at $0 of its $3 allocation.

- I no longer promise a number of trials. My earlier "12 trials at $1.50" assumed a trial fits in about an hour, and fetching the models alone (about 53.5 GB) could take that long on a fresh machine.
- The pilot, funded at $3, measures what a cold start really costs: setting up, fetching the models, the worker becoming ready, and one generation. The cap per trial and the number of trials are set from those numbers and the dollars left.
- Every paid trial is preceded by a free rehearsal, so a rented hour is not spent discovering something a dry run would have shown. A failed trial still spends, and one ledger records every rental and release receipt.
- Whether trials can start warm (reusing a machine, or models kept on storage) is not yet known. The account already shows about $0.03 an hour with nothing rented, which may be existing storage; that is being checked. Until it is known, assume every trial starts cold.
- Money is spent in this order: the three Morpheus clips; the two takes with the picture kept; the cross-film trial; and the picture skills only from what remains.
- A failed trial still spends. One ledger records every rental, failure and release.
