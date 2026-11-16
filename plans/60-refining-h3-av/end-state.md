# H3_AV: where it should end up

Written 16 November 2026 from the Release 14 code, four focused explorations and the live pilot notes. Nothing here has been proven on a GPU yet; the items that depend on the pilot are marked **open**.

## What H3_AV is, and is not

**It is** the pack that turns one edit request into one run of the H3 model. It does three things:

- **Continue** a clip: keep the start, generate what happens next, picture and sound.
- **Change a region** of the picture inside a mask, keeping everything else and the original sound.
- **Generate** a new clip from reference images (including the character swap).

It prepares the inputs, runs on a rented GPU, puts the protected parts of the original back, and checks that it did.

**It is not** a transcriber, a mask maker, a timeline editor or a judge of whether the line sounds right. Those are separate things it should use, not contain.

## Three problems in the pack today

1. **It rejects real footage.** The Morpheus pilot was refused before renting anything: the Matrix clip is 23.976 fps and 1920×800, and H3 only accepts exactly 24 fps and 1024×576. Its error tells the agent to run an ffmpeg command by hand, and that command would stretch the picture.
2. **It carries things that are not the product.** The LanPaint route cannot be reached by any request. An "audio only" mode is advertised and always errors. A "reference audio" setting is read by nothing. There are two request formats and two commands for the same operations.
3. **Its documentation describes machinery, not choices.** The skill links to pages that do not exist, and the older guides describe the unreachable LanPaint route as the next thing to try.

## How one workflow feeds another

Astrid already has the mechanism: any result is stored media, and a later step can name it with a **handle** (its digest, or "output N of run X") instead of a file path. H3 is the exception: it wants a hand-written map of names to local files. Fixing that is most of the chaining story.

The Morpheus shot, as it should work:

1. **Find the shot.** `timelines show` says the clip uses the Matrix media, source time 81.05–84.30 s.
2. **Know the words** (when transcription exists): transcribe that media once, read the words and times, and pick a cut point at a pause.
3. **Ask for the edit.** One request: continue this media from this range, he says the new line, total length. The source is named by handle and range; H3 cuts and conforms it itself.
4. **Run it.** `astrid generate video --entry h3` on the rented GPU. The take comes back as stored media.
5. **Check it.** Pull clean frames, transcribe the take and compare with the intended line, then you listen.
6. **Place it.** `timelines edit --swap-asset` with the take's handle, trimmed so only the new part shows.

A mask works the same way later: a mask workflow's output handle goes into the request where a mask file goes today.

## Continuing a clip and continuing a voice

They are the same operation. There is no separate voice route.

- The model hears the **last 39 frames (about 1.6 seconds)** of sound before the cut point. That is the only voice sample it gets. A longer starting clip does not lengthen it.
- So "continue the voice" means: choose a start whose last 1.6 seconds are that person speaking clearly, and allow sound to be generated after it. The kept start still contains his original words, so on the timeline you use only the newly generated part.
- Continuation takes no voice or video reference. One of the two request formats lets you write one, and the code then rejects it.
- **Open:** whether 1.6 seconds holds Morpheus's voice across a full line. If it does not, the timing code already allows for longer context (90 or 141 frames). Whether the model graph accepts that is untested, so it is something to try only if the pilot shows the need.

There were two versions of the same thing in three places: two request formats that compile to the same graphs, two commands, and old guides naming a "Seitanism extension workflow" that is in fact the packaged continuation graph.

## LanPaint: remove it

Your understanding is right. A commit on 28 October replaced it for masked picture edits with H3's own masking nodes. Since then no request can reach it, the skill says so, and tests fail if a masked edit uses LanPaint nodes. What remains is an unreachable helper, a packaged workflow that was never run on a GPU, and a test of that helper.

One honest cost: LanPaint was the only graph that could regenerate **sound** inside existing footage. Nothing replaces that today. For new dialogue the route is continuation. If you later need to change words while keeping the exact picture, that should be built on the native nodes, not revived from LanPaint.

## The skills

```
creative work (exists)                  "which pack does this job?"
└─ audiovisual editing (new)            "what does this shot need, and in what order?"
   ├─ H3_AV (rewrite, one screen)       "how do I ask for continue / change a region / generate?"
   │  ├─ requests (reference)           one complete, tested example per operation
   │  └─ techniques (reference)         choosing the start and cut point; voice; masks; what goes wrong
   ├─ timeline (exists)                 placing a take and comparing it with the original
   ├─ rendering (exists)                pulling a clean frame, rendering a range
   └─ RunPod (exists)                   renting the GPU and what it costs
```

Transcription and masking get a paragraph each in "audiovisual editing" until they exist as tools.

## What each need should be

| Need | Answer |
|---|---|
| Choosing continue, region change or generate | Skill |
| Choosing the start clip and the cut point | Skill |
| Judging voice, lips and continuity; when to retry or ask you | Skill |
| Checking the spoken words | Skill, using transcription |
| Giving H3 real footage (any frame rate, size, range) | Small tool: H3 prepares its own source, with Fill or Fit stated |
| Passing one workflow's result to H3 | Connect: H3 accepts the handles Astrid already has |
| Finding the H3 entry when VibeComfy is not set up | Small fix: say what is missing instead of "unknown entry" |
| Placing a take on the timeline | Already exists (`timelines edit`); skill only |
| Where words live | Already exists (a transcript attached to the media); connect |
| Producing words from any clip | Small tool, general to Astrid, not H3's |
| Producing a mask from a description | Small tool, general to Astrid, not H3's; only when a shot needs it |
| Longer voice context | **Open** until the pilot |
| LanPaint route, the `astrid h3` command, "audio only", the unused reference-audio setting, dead links, the old speech guide | Delete |
| The second request format | Keep only what the character swap needs; document one format |

## Order to build in

1. **H3 accepts real footage by handle and range.** This is what blocks the Morpheus pilot today.
2. **The Morpheus pilot on a GPU**, and you hear it. It settles the voice question.
3. **Remove what is not the product.**
4. **Write the skills**, first from the code, then again from what the Morpheus shot taught.
5. **Someone else's similar shot:** a fresh, weaker agent with only the skills, on a different clip.

Transcription comes in alongside step 2 because the Minkhole work needs it to find cut points and check takes. Masks come when the first picture change (the pill, the glasses) needs one.
