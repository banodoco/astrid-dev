> Historical research, not instructions. Where this differs from the current plan, inputs or tasks files, those win.

# H3 jobs: one shape, three families of levers

An H3 job makes a short video with sound, at 24 fps. Set its length with `duration:` (seconds) at the top of the request. You steer it with **levers**, in three families:

| Family | What it sets | Exact? |
| --- | --- | --- |
| **Output** | what's in the video, and what may change | Yes. Placed material comes back exactly. |
| **Context** | what the model looks at: references, guides, the prompt | No, it only influences. |
| **Process** | how the model runs: LoRAs, ControlNet, settings | No, it only influences. |

## Three rules for Output

1. **Placed material is kept.** A placed item covers the output from `at` for the length of its `range`; a still covers one frame. A video brings both its picture and its sound.
2. **Time nothing covers is generated,** picture and sound.
3. **An `edit` opens placed material for change** in a time span, optionally in a region. If you change a mouth, also edit the audio for that span, or the lips and the sound won't match.

## One ladder for any asset

- `role: timeline`: **place** it; kept exactly.
- `role: guide`: shown to the model **at a moment**, softly ("around here, look like this").
- `role: reference`: shown to the model **for the whole clip**, softly ("this is who they are, how they sound"). Refer to references in the prompt as `<Picture 1>`, `<Video 1>`, `<Audio 1>`, numbered per type in listing order. Only references get tags; placed items and guides don't. One asset can be both placed and a reference. `stream: audio` on a video uses only its soundtrack.

## Time

- **Clip time:** `at` is a point and `during` is a span, both in seconds of the output. Negative numbers count back from the end, and `end` means the end: `at: -2` means 2 s before the end; `at: end` means the last frame; `during: [-2, end]` means the last 2 s.
- **Source time:** `range` picks part of the file, in seconds. `range: [-2, end]` means the file's last 2 s.
- **The model's clock:** `phase: [from, to]`, from 0 (start of denoising, composition) to 1 (end, fine detail). Process levers only. Early is about `[0, 0.5]`; late is about `[0.6, 1]`.

## Shared fields

The same names on every lever. Each kind uses only the ones that make sense:

`asset`, `at`, `during`, `range`, `stream` (`video`, `audio`; default both), `mask` (an image covers the same pixels every frame; a video can follow movement; white = may change), `strength` (0 to 1; default 1), `phase`.

A kind can also have its own settings under `params:`. `astrid generate describe --entry h3` lists every kind with its fields, params, defaults and limits.

## The kinds

| Kind | Family | Written as |
| --- | --- | --- |
| place | Output | `media[]` with `role: timeline` |
| edit | Output | `edit[]` inside a placed item. Overlapping edits: the higher strength wins. |
| guide | Context | `media[]` with `role: guide` |
| reference | Context | `media[]` with `role: reference` |
| prompt | Context | `prompt:`, either one string or a list of `{during, text}` for what happens when |
| LoRA | Process | `settings.loras[]`: `{file, strength, phase}` |
| control | Process | `media[]` with `role: control`, `during`, `strength`, `phase`, and its own `params`, e.g. `params: {type: soft_edge, soft_edge: 0.4}`. A control carries another clip's structure or motion without its look, and is off outside its `phase`. |
| settings | Process | `settings: {size: [1024, 576], seed, steps}` |

**Tools make inputs; they aren't levers:**
- `astrid media mask clip.mp4 --select "his mouth" -o mouth.png` makes a mask; add `--track` (and `-o mouth.mp4`) for one that follows something moving;
- `astrid media control --as pose|depth|canny|soft_edge clip.mp4 -o out.mp4` makes a control video, converted to 24 fps and the job's size.

## Write, dry-run, submit

`astrid generate video --entry h3 --request job.yaml --dry-run` prints each lever and what's kept or generated. It also shows where H3 snapped your times: it works in small chunks of frames, so edges can move slightly, but kept material is still delivered exactly. Fix any refusal it names, then run it again without `--dry-run`.

Templates are requests with `${holes}`. See `astrid generate templates list`. A filled template is just a request.

### Example: redub template

```yaml
name: redub
holes: {source: video, mouth_mask: mask, line_span: range, voice: audio, line: text}
request:
  version: 2
  prompt: 'He says "${line}" in the voice of <Audio 1>.'
  media:
    - id: shot
      asset: ${source}
      role: timeline
      at: 0
      edit:
        - {stream: video, during: ${line_span}, mask: ${mouth_mask}}
        - {stream: audio, during: ${line_span}}
    - {asset: ${voice}, role: reference, stream: audio}
```
