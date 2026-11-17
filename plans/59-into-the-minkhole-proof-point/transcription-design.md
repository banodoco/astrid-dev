# Word-level transcription: how it works today and the standard we want

Investigation, 17 November 2026 (read-only; Agent `release/14/plan-59` at 55df77b20, VibeComfy 79143f24, Runtime e6106ac). Orchestrator spot-checked: `astrid/core/generation/cli.py:23` (audio modes are only music/tts/sfx), `astrid/sdk/whisper_transcript.py:156-161` (re-import returns "unchanged" without comparing), `astrid/packs/rendering/actions/timeline_visualize/contact_sheet.py:173` ("—" when clips carry no words). Status: design for the owner; nothing built.

## Short answer

Astrid already has the right store: one Runtime `media.transcript/v1` document per media file, times in seconds of that file, carried in `.astrid` archives. The Whisper workflow writes it. But every editing and review reader (`timelines words`/`lines`, visualize word tiles, contact sheet, review captions, narrated editing) reads a second store, words on clips (`app.words`, clip-local time), through at least six separate projections. So a real transcript, once made, would not show anywhere except `timelines transcripts show`. This is astrid-dev#773.

## Pieces today

- **Workflow:** entry `transcription` (audio, mode transcribe, input `audio_ref`): LoadAudio -> Apply Whisper (ComfyUI-Whisper 006a7098, patched to load only the provisioned, hash-checked `large-v3-turbo.pt`, `word_timestamps=True`) -> `VibeComfySaveTranscript` (JSON). Language hard-coded `auto`, no prompt/script hint, whole file decoded at once. Reachable only through `astrid timelines transcripts run <media>`; `astrid generate audio --mode transcribe` is refused by the CLI and the entry's own example is wrong.
- **Stores of words:** (A) media transcript document, intended source of truth; (B) clip `app.astrid.words`, the actual authority for readers; (C) shot `voiceover_script` text = the script, not timings, keep; (D) shot `transcript` text, untimed, nothing writes or reads it; (E) `config.app.transcript` file attachment for visualize/render; (F) render speech inputs; (G) word anchors pinning A, correct design; (H) derived index; (I) TTS `speech-words.json`, reaches B only by hand.
- **Projections:** eight separate pieces of code map words to the timeline; only the `transcripts show` path and word anchors handle trim, speed, nesting and repeated placements correctly. The B readers ignore speed and put a repeated shot's words at its first placement only.

## What happens when something changes

| Change | Today |
|---|---|
| Media replaced | No transcript for the new media; nothing transcribes or warns (refused if the clip has words) |
| Clip trimmed | B shifted; at publish the "whole-media" narration transcript is cut down to the clip |
| Speed changed | B readers silently stale; next publish writes wrong source times into A |
| Shot placed twice | Words appear at the first placement only |
| New take generated | Nothing; no transcription step, the shot plan's takes have no words |
| Voice track swapped | Manual, needs a words file |
| Re-transcribe same media | Silently "unchanged"; with --replace every word id changes and pinned anchors fail |
| Export/import | Correct (A and references carried) |

Live state on the repaired install (project `minkhole`): no transcripts, no words anywhere. `blue.wav` is split across four VO clips in four shots, which a media-keyed store handles and the clip-word model does not.

## The standard (reuse, do not add)

1. **One stored copy:** the media transcript document (A), per media digest and source, in that media's seconds. Producers write only A: Whisper via ComfyUI, TTS words (source `astrid.tts`), hand imports, and legacy clip words converted once (source `astrid.narration`).
2. **One projection every reader uses** (`project_words(bundle, transcripts, scope)`), built from the correct existing paths: keep words with `from <= t < to`, map `timeline = owner_start + clip.at + (t - from)/speed`. Scope `shot:<id>` gives the sub-timeline view (owner_start 0); scope `parent` repeats per placement and clips to its length. Child and parent always agree. Rows carry A's stable word ids, so anchors keep working. Readers that switch to it: `timelines words`/`lines`/moments/lint, `transcripts show`, visualize filmstrip/motion/contact sheet, review captions, render speech inputs, and the editor.
3. **Which transcript a timeline uses:** default source order (Whisper, then TTS, import, narration), overridable per media through the existing `transcriptReferences` block (already exported and validated).
4. **One refresh command:** `astrid timelines transcripts refresh <timeline> [--shot S] [--run-missing --placement runpod] [--convert] [--dry-run]`: lists every audio-bearing media in the parent and child timelines with its transcript status, runs the ComfyUI workflow for missing ones, records the choice, reports anchors pinned to old versions and cuts that split a word. Trim, move, speed and repeated placements need no refresh because projection happens on read. GPU work stays explicit.
5. **Existing data:** clip words converted once into A then removed (line identity and script text stay); the `transcript` shot text becomes a derived view; `voiceover_script` stays as the script ("meant" vs "said"); the publish-time narration sync goes once B is gone.
6. **Takes and the shot plan:** a take's words are A(its media digest), shown wherever it is placed. The plan's `inputs.voice = {media, range}` states range in seconds of that media; it references words, never copies them.

## Builds, smallest first

- **B0:** allow `transcribe` in `astrid generate audio` with an audio input, fix the entry example; make re-import compare content and say "differs; use --replace".
- **B1:** the shared projection; `timelines words`/`lines` and `transcripts show` use it (A first, fall back to B). Tests: child shot, repeated placement, speed 0.5/2, one media across four shots.
- **B2:** visualize, contact sheet, motion and review captions read it (fixes the "—").
- **B3:** `transcripts refresh` (status, --run-missing, --convert, stale anchors, references); `sync` becomes an alias.
- **B4:** producers write A: narrated line/take replacement, TTS words, an optional `--transcribe` on generate; shot plan clock wording.
- **B5:** retire clip words for converted timelines, the publish narration sync and the separate visualize/render word readers.
- **B6:** Runtime schema: optional `clock` and `producer`; optional language and prompt inputs on the entry.

Skills that change: timeline `transcripts`, `narrated`, `shots`; H3 `recast-scene` (stages 1, 4, 5) and the main H3 skill; how-to-look if it mentions word tiles.

## First real GPU run: what it must prove

Model present at 1,617,941,637 bytes with its hash (no download by the node); both nodes registered on the worker; WAV and MP4-with-audio both decode; the single JSON output collected; import guards pass (no ambiguous segment membership, no word past the duration, no empty segment text); one document per media, re-run gives "unchanged"; word starts within about 0.1 s on five checked boundaries; the `blue.wav` cut points (1.55, 3.967, 8.258 s) fall between words; `transcripts show --clip blue-voiceover-part-3` lands within 12.17-16.46 s. Expected and not a failure until B1: `timelines words` still shows nothing. Order: `choice.wav`, then `blue.wav`, then the Matrix source.

## Unknowns

What the editor's `adaptTranscript.ts` does (astrid-app not inspected); whether the editor writes `transcriptReferences`; Whisper's real timing error and behaviour on music-heavy audio; whether RunPod provisioning pre-fetches the Whisper model; memory for the full Matrix file decoded at once.
