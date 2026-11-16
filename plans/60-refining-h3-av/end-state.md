# H3_AV: where it should end up

Written 16 November 2026 from the Release 14 code, four focused explorations and the live pilot notes, and revised the same day after an independent critique. Nothing here has been proven on a GPU yet; the items that depend on the pilot are marked **open**.

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
2. **Know the words.** Today: listen, and pick a cut point at a pause. Once transcription exists: transcribe that media once and read the words and times.
3. **Ask for the edit.** One request: continue this media from this range, he says the new line, total length. The source is named by handle and range; H3 cuts and conforms it itself.
4. **Run it.** `astrid generate video --entry h3` on the rented GPU. The take comes back as stored media.
5. **Check it.** Pull clean frames at the cut point and listen against the written line. Later, transcribe the take and compare.
6. **Place it.** Add the take as its own clip above the shot with the existing timeline commands, showing only the newly generated part, at normal speed, with the temporary voiceover silent over it. The original stays untouched underneath.

A mask works the same way later: a mask workflow's output handle goes into the request where a mask file goes today.

## Continuing a clip and continuing a voice

They are the same operation. There is no separate voice route.

- The model hears the **last 39 frames (about 1.6 seconds)** of sound before the cut point. That is the only voice sample it gets. A longer starting clip does not lengthen it.
- So "continue the voice" means: choose a start of at least 39 frames whose last 1.6 seconds are that person speaking clearly, and allow sound to be generated after it. The graph needs that many; the "two options" source clip, at about 1.5 seconds, is too short as it stands. The kept start still contains his original words, so on the timeline you use only the newly generated part.
- Continuation takes no voice or video reference. One of the two request formats lets you write one, and the code then rejects it.
- **Open:** whether 1.6 seconds holds Morpheus's voice across a full line, and whether the long target line fits in the 6.75 seconds generated for it. The graph's context is fixed at 39 frames today. A longer window would be a change to the graph, to be considered only if the pilot shows the need.

**One limit to know before you choose a shot.** Continuation regenerates the whole picture after the cut point. Changing the words while keeping the exact picture (same pose, same camera, only the mouth and voice change) is **not supported today**: the masked edit keeps the original sound. The plan records this as a follow-up and does not pretend continuation covers it.

There were two versions of the same thing in three places: two request formats that compile to the same graphs, two commands, and old guides naming a "Seitanism extension workflow" that is in fact the packaged continuation graph.

## LanPaint: remove it

Your understanding is right. A commit on 28 October replaced it for masked picture edits with H3's own masking nodes. Since then no request can reach it, the skill says so, and tests fail if a masked edit uses LanPaint nodes. What remains is an unreachable helper, a packaged workflow that was never run on a GPU, and a test of that helper.

One honest cost: LanPaint was the only graph that could regenerate **sound** inside existing footage. It never ran on a GPU, so removing it removes no working route, but nothing replaces the idea today. For new dialogue the route is continuation. If you later need to change words while keeping the exact picture, that should be built on the native nodes, not revived from LanPaint.

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
| Checking the spoken words | Skill: listening against the written line now, transcription when it exists |
| Giving H3 real footage (any frame rate, size, range) | Small tool: H3 prepares its own source, with Fill or Fit stated |
| Passing one workflow's result to H3 | Connect: H3 accepts the handles Astrid already has |
| Finding the H3 entry when VibeComfy is not set up | Small fix: say what is missing instead of "unknown entry" |
| Placing a take on the timeline | Already exists (add and trim on the timeline); skill only. Your choice: a stored alternate (recommended) or a local review draft |
| Where words live | Already exists (a transcript attached to the media); connect |
| Producing words from any clip | Small tool, general to Astrid, not H3's |
| Producing a mask from a description | Small tool, general to Astrid, not H3's; only when a shot needs it |
| Longer voice context | **Open** until the pilot |
| Changing words while keeping the exact picture | Not supported today; recorded as a follow-up |
| LanPaint route, the `astrid h3` command, "audio only", the unused reference-audio setting, dead links, the old speech guide | Delete |
| The second request format | One format is documented for the three operations. The character swap keeps the second format, documented separately as experimental. The rest of the second format works but duplicates the first: your decision whether to retire it now (recommended) or leave it undocumented |

## Order to build in

1. **H3 accepts real footage by handle and range.** This is what blocks the Morpheus pilot today. A short independent review of this change comes before any paid run builds on it.
2. **The Morpheus pilot on a GPU**, and you hear it and accept or reject it. It settles the voice question. A rejected take is an unfinished result, not a finished step.
3. **Remove what is not the product.**
4. **Write the skills**, first from the code, then again from what the Morpheus shot taught.
5. **Someone else's similar shot:** a fresh, weaker agent with only the skills, on a different clip.

Nothing here waits for transcription or automatic masks. Until the Minkhole work provides them, words are checked by listening and masks are supplied by hand; when they arrive, this path uses them.
