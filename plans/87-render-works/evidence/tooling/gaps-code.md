# Agent-tooling gaps: code findings (read-only)

Root: `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/a/` (abbrev. `a/`).
Paths below are relative to `a/astrid/` unless noted. Nothing was executed; repro lines are not run.

Evidence labels: **code** = read in source; **doc** = a docs/comment statement; **inferred** = my reading, not confirmed at runtime. The Runtime (the server side of `open_composition`) is not in this tree, so anything that depends on what the Runtime returns is marked as such.

---

## Gap 1: no standalone audio excerpt

**Surface.** `a/cli-surface.json`, family `timelines`, has no audio verb (verbs: apply, archive, assets, check, checkout, commit, create, diff, discard, duplicate, edit, elements, export, find, history, import, inspect, lines, lint, list, log, pending, place-element, recover, redo, rename, render, replace-parent-media, restructure, retry, script, shots, show, status, transcripts, undo, update-element, visualize, words). `media` verbs: import, list, open, references, relate, show, thumbnails, verify. `timelines visualize` flags include `--show`, `--render-run`, `--render-every`, `--include-media`, `--mode`, `--format`; no audio-file output flag.

**Where audio appears (all as pictures or numbers, never as samples a human or agent can play).**
- Input-lane waveforms from source files: `packs/rendering/actions/timeline_visualize/filmstrip_cards.py:309-321` (`attach_input_audio_waveforms`: "Only ``verified_original`` files are opened ... analyzed once and its complete bounded analysis is written to a sidecar"). Written to `output_root/source-audio-analysis`.
- Render-audio waveform: `filmstrip_execution.py:1784-1788` sets `status: 'not_analyzed'` and `coverage.reason: 'composed frame capture has no audio render'` when `capture_mode` is true. The analysis (`analyze_audio`, line 1795) runs only on the non-capture branch, i.e. when a rendered video exists.
- Loudness/silences of a render: `packs/rendering/actions/timeline_visualize/render_review.py:100` (`measure_audio`) and `:188`; surfaced by `timelines visualize --render-run RUN --render-every 5` (`~/.claude/skills/astrid-rendering/SKILL.md`, "A contact view of a render ... also prints its loudness and silences").
- `audio_analysis.py:1-8` (module docstring): "Bounded, deterministic audio facts for a verified rendered media file ... PCM is consumed in small chunks and reduced directly into bounded integer-sample bins." It keeps bins, not a playable excerpt.

**Is it deliberate?** Partly documented, no explicit "won't do" for the timeline path:
- doc: `packs/rendering/docs/references/render-inspect-transfer.md:340-347`: "Audio rows are frozen to the render; they never turn missing script into silence or present the rendered mix as an isolated stem."
- doc: same file `:355-357`: "the JSON retains the measured amplitudes." So the numbers are available in JSON.
- doc: `:360-361` "Source audio-track rails are timing signifiers (not per-source loudness measurements)".
- doc: `:371` "`--include-media` separately adds a relative, hash-verified MP4 for offline playback; the attachment does not supply frame pixels." This is the whole render MP4, not an excerpt.
- code, explicit out-of-scope comment, but in a module the CLI does not call: `packs/rendering/actions/timeline_visualize/thumbnails.py:~79-81` `AUDIO_FILMSTRIP_NOTE = "audio filmstrips are not produced yet: spectral and waveform rendering is out of scope"`. No caller of `sample_filmstrip` was found under `packs/`, `sdk/` or `core/` outside the module (only `__all__`, `thumbnails.py:526`), so this is a source-asset sampler note, not the visualize path.
- doc: `packs/rendering/docs/references/placeholder-voiceover.md:66-74`: split PCM "using real speech-boundary timing" and "listen at the cuts when reviewing speech." The guide assumes a human listens.
- doc (worlds only, not timeline): `packs/rendering/docs/references/worlds-authoring.md:528-533` "There is no automatic audio extraction".
- Verdict: **not evident as a deliberate block on excerpts.** No code, comment or test says "no audio excerpt for agents". The gap is consistent with the design (audio = waveform bins + MP4), and the only written "out of scope" is the unused thumbnail note.

**Documented workarounds.**
- `timelines visualize ... --mode inputs --show audio` (inferred from `render-inspect-transfer.md:311` `--show output,inputs,text,audio --every 5`): waveform lanes, numbers in JSON, no playable audio.
- `media open <ref> --materialize` writes "a verified bounded copy to a disposable local path" (`a/astrid/core/cli/domain_media.py:311-331`, `--max-bytes` default 10 MiB at `:327-331`). This is the only route to bytes of a source audio asset. Cutting/decoding is then outside Astrid (ffmpeg, which `placeholder-voiceover.md:~62` already uses).
- Rendered audio: `--include-media` (whole MP4) from `timelines visualize --render-run <RUN> --include-media`.

**Minimal repro (not run):**
`timelines visualize <timeline> --project <project> --mode inputs --show audio --range 5..10 --json`
then, for bytes: `media open <asset-ref> --project <project> --materialize --json`

---

## Gap 2: visualize window caps

**Presets.** `a/astrid/packs/rendering/actions/timeline_visualize/motion/window.py:28-39`:
- scan: `"every_s": 0.5 ... "max_window_s": 30.0, "budget": 64` (line 29-30)
- motion: `"every_frames": 2 ... "max_window_s": 3.0, "budget": 60` (31-32)
- beat: `"strategy": "onsets" ... "max_window_s": 20.0, "budget": 48` (33-34)
- frame: `"max_window_s": 1.0, "budget": 1` (35-36)
- cut: `"max_window_s": None, "budget": 60` (37-38)
- `MAX_COLUMNS = 16`, `MAX_PAGE_HEIGHT = 2600`, `MAX_PAGE_WIDTH = 2600` (`:42-43`, `:154`).
- Table in the module docstring (`:9-15`) matches these numbers.

**Enforcement and messages.**
- Window length: `window.py:84-88`: `raise ValueError(f"preset {preset} shows at most {limit:g} s (asked {end - start:.2f} s); " f"narrow --range, or use --preset {other} for this window")`.
- Frame count: `window.py:147-150`: `raise ValueError(f"{len(frames)} frames is over the {window['preset']} budget of {budget}; try {hint} (or --frame-budget up to 120)")`. Note: "--frame-budget up to 120" is the only override, and it changes only the frame count, not the seconds.
- `--frame-budget` range: `a/astrid/packs/rendering/actions/timeline_visualize/filmstrip_options.py:54-55` (`MOTION_FRAME_BUDGET = 60`, `MOTION_FRAME_BUDGET_MAX = 120`) and `:276-281` (`frame_budget must be an integer between 1 and 120`). `run.py:256-257` help: "motion view: maximum captured frames (default 60)".
- Where it runs: the same `resolve_window` is called in plan mode from the CLI (`a/astrid/packs/timeline/cli_visualize.py:519-523`, `:544`) and in the capture path (`filmstrip_cards.py:869-870`, `:1910-1911`). I did not trace whether the capture path runs in the CLI process or in the Runtime. Since the error is a plain `ValueError`, the agent sees it as the command's error text.
- Client-side only for addresses: `cli_visualize.py:31-38` (`_preset_max`, used only for a hint) and `:187-191`: with `--at <layer>` the CLI widens to the layer's whole span only if `end - start <= limit`; otherwise it falls back to one moment (`:193-194`).

**Paging / continuation.**
- No cursor or page token exists on `timelines visualize`. Surface flags with "page" or "cursor": only `--page-size` (no `--page`, no `--cursor`). The `--window` flag (`run.py:259`) is the window *width* around `--at`, not a page.
- Continuation is by re-running with a new window. `window.py:174-191` `navigation()` returns `earlier`, `later`, `zoom_in`, `zoom_out`, `busiest`; `cli_visualize.py:485-512` prints these as `next:` commands ("the CLI's next: block"). Cited in the output as `next:` lines, so an agent can copy them.
- Filmstrip pages (non-motion): `filmstrip_cards.py:1131-1133` and `filmstrip_execution.py:983-985`, `:1236-1238` `page_size` default 50 cards per PNG page; the page files are listed in `outputs.pages` (`filmstrip_execution.py:339`). This is the only real multi-page output; `--page-size` (surface) changes the count per page.
- Contact view never paginates by design: `window.py:154-171` `fit_columns`: "Tiles shrink and rows widen before anything paginates."

**Sweep.** `a/astrid/packs/rendering/actions/timeline_visualize/sweep.py:13` `SWEEP_MAX_FRAMES = 90` (no comment). Used by `a/astrid/sdk/timeline/check.py:548` (`sweep_mod.sweep(...)` with default `max_frames`) for `check --sweep` / the after-edit sweep (`packs/timeline/cli_sweep.py:21-27`). Overflow is not an error: `sweep.py:107-135` `_budget` marks extra cuts `render=False`, `kind="unchecked"`, `verdict="inputs changed; not captured (sampled out)"`. The `max_frames` is not exposed as a flag on `visualize` or `check`.

**Thumbnails.** `packs/rendering/actions/timeline_visualize/thumbnails.py:70-71`: `MAX_FRAMES_PER_PAGE = 12` with comment "HARD per-page filmstrip budget (R13): no page may carry more than 12 frames." Also `:122-136` `per_page_frame_budget`. This module's `sample_filmstrip` (`:331`) is the source-asset sampler; I found no caller in the visualize CLI path. Not an agent-visible limit on `timelines visualize`.

**Deliberate?** Yes for the window caps: the table and the messages are explicit (`window.py:1-16`, error texts above), and `MAX_PAGE_HEIGHT` is commented "ONE page" (`window.py:158-161`). The reason is stated as "every motion-style view is some frames of one time window, on one page" (`window.py:1-2`). No comment explains why 3 s or 30 s specifically. The `--frame-budget` ceiling of 120 is uncommented.

**Workarounds documented.**
- Narrow `--range`, or use the named preset: "use --preset scan for this window" (`window.py:88`).
- `--frame-budget N` up to 120 for the frame count (`window.py:150`).
- Follow the `next:` lines for the next window (`cli_visualize.py:485-512`).
- Filmstrip paging: `--page-size` (surface; `filmstrip_options.py` path).

**Minimal repro (not run):**
`timelines visualize <timeline> --project <project> --preset motion --range 0..10 --json`  (expect `ValueError` "preset motion shows at most 3 s ...")
`timelines visualize <timeline> --project <project> --range 0..30 --preset beat --json`  (expect "frames is over the beat budget of 48 ...")

---

## Gap 3: `timelines show --json` returns 50 per page

**Parser.** `a/astrid/core/cli/domain_timelines.py` (`_configure_show`, starts `:938`):
- `:965` `--page`: "Cut table page N (1-based); with no --page-size, 20 cuts a page."
- `:966` `--page-size`: "Cuts per page (default: all cuts)."
- `:997` `--limit`: default `50`, "Maximum bounded inspection rows (1–100)."
- `:998` `--cursor`: "Continue a bounded inspection page from its cursor."

**Routing: `--json` always takes the 50-row inspection path.** `a/astrid/packs/timeline/cli.py:1063-1080`:
- `inspection_view = bool(parsed.json or ...)` (`:1063-1065`). So `--json` never reaches the cut-table printer.
- `values` (`:1067`) forwards `clip, occurrence, shot, track, asset, range, detail, limit, cursor, revision_id`. It does not forward `page` or `page_size`. So `show --json --page 2` is **silently ignored** (inferred from the dict literal; the human path is the only consumer, `cli_show.py:361`).
- `:1098-1104` `opener(..., limit=values.get("limit") or 50, cursor=values.get("cursor"), ...)`.
- `a/astrid/sdk/remote.py:925-937` `open_composition(..., limit=50, cursor=None, ...)` (default 50, matching the CLI default).

**What the JSON contains (the agent can see paging).** `a/astrid/sdk/remote.py:1316-1331`:
- `"pagination": {"next_cursor": data.get("next_cursor"), "limit": selectors.get("limit")}` (`:1318`). `next_cursor` is the flag to page.
- Top-level `page`, `bounds`, `omission_metadata` copied through if the Runtime sends them (`:1325-1327`).
- Human text prints `page: returned X of Y selected clips; Z remain` and `page: more results available (cursor ...)` (`a/astrid/packs/timeline/cli.py:990-1006`). That line is read from `data["page"]`, so the same fields exist in JSON, **but a total count appears only if the Runtime supplies `page.total_selected_clips`**. The Runtime source is not in this tree, so this is not verified.
- No truncation boolean was found; the signal is `pagination.next_cursor` being non-null.

**Paging flag.** `--cursor <next_cursor>` with the same query (`domain_timelines.py:998`; cli.py `values` includes `cursor`). `--limit` 1–100 is only documented in help text; I found no clamp in `cli.py` or `remote.py` for the inspection path (`cli.py:1181` clamps to 100 only in the `--as cuts` presentation path).

**Dead-code note.** `a/astrid/packs/timeline/cli_show.py:256-272` has a `--json` branch built by `cut_table_payload` (`a/astrid/sdk/timeline_cuts.py`, which sets `"complete": True` and returns all rows and words). It is **not reachable** through `timelines show --json` because `cli.py:1063` routes JSON to the inspection path. The `complete: true` payload is therefore not emitted by the CLI.

**The 50-row inspection is not the same as the cut table.** The default human `show` (no flags) prints all cuts (`sdk/timeline_cuts.py:131-137`: `if page is None and page_size is None: return list(rows), None`). The `--page` / `--page-size` flags (`cli_show.py:361`) and their "--page must be between 1 and N" error (`sdk/timeline_cuts.py:138-147`) work only on the human path.

**Deliberate?** The 50 default is stated in the parser help (`domain_timelines.py:997`, "default 50" in `--limit`). No comment explains the number. The cursor design is explicit ("Opaque cursor from this bundle and identical query", `:998`). The `--page` silently dropped on JSON is not documented; I count it as an unflagged gap.

**Minimal repro (not run):**
`timelines show <timeline> --project <project> --json --limit 100`
then `timelines show <timeline> --project <project> --json --limit 100 --cursor <pagination.next_cursor>`
Human-path alternative: `timelines show <timeline> --project <project> --page 2 --page-size 20`

---

## Gap 4: `timelines words` has no `--json`

**Surface.** `a/cli-surface.json`, `timelines.verbs.words`: flags `--beats --draft --file --find --project --published --range`; positionals `ref, word`. No `--json`. (`show`, `visualize`, `inspect` all list `--json`.)

**Parser.** `a/astrid/packs/timeline/cli_working.py:535-545` `_configure_words`: calls `_timeline_args` (`:369-377`, adds `ref`, `--project`, `--draft` only) then `word`, `--beats`, `--file`, `--published`, `--find`, `--range`. No `--json` added.

**Implementation.** `cli_working.py:440-470` `_cmd_words` (`@guard(2)`, `cli_common.py:22-`):
- Never reads `parsed.json`. Prints one line per word (`:465`): `print(f"  {w.start:.3f}–{w.end:.3f}  {w.text}  [{w.id}]  {cut}")`, then a `next:` line (`:466-467`).
- Single-word form `cli_working.py:483-533` `_print_word`: prints `describe_target(...)` text (`:487`), `anchored to it: ...` (`:~511`), and `--beats` beat list (`:523-531`). All plain text.

**Output formats supported:** plain text only (word lines, or one word's record with optional beats). No JSON, no table/CSV switch.

**JSON alternatives that do exist (inferred from routing; not run):**
- `timelines show <tl> --as script --json`: presentation path, `cli.py:1040-1059` with `print_result(result, as_json=parsed.json, ...)`. Script view = words in time order with cuts. Note `cli.py:1046-1047`: `script/code` without `--json` take the text path; with `--json` they fall through to the presentation JSON.
- `timelines show <tl> --json` includes words only in the dead `cut_table_payload` (`cli_show.py:~256-272`, `sdk/timeline_cuts.py`), so do not rely on it.
- The `words` text output has a stable id per word (`[{w.id}]`), usable with `timelines show <tl> '"<word>" in <cut>'` (address form; `cli_working.py:483-487`).

**Deliberate?** No comment or doc says "words is text-only". The `words` module docstring (`cli_working.py:1-3`) only describes the verbs. Unflagged gap.

**Minimal repro (not run):**
`timelines words <timeline> --project <project> --find <text> --range 5..10 --json`   (today: argparse rejects `--json`, since it is not registered)
Workaround: `timelines show <timeline> --project <project> --as script --json`

---

## Surface entries (a/cli-surface.json)

| verb | flags of note |
|---|---|
| `timelines visualize` | `--preset` (choices beat, compare, cut, frame, motion, overview, scan), `--frame-budget`, `--window`, `--every`, `--every-frames`, `--page-size`, `--render-run`, `--render-every`, `--include-media`, `--show`, `--mode` (auto, composed, inputs), `--format`, `--json`, `--plan`. No `--page`, no `--cursor`. |
| `timelines show` | `--json`, `--limit`, `--cursor`, `--page`, `--page-size`, `--as` (cuts, script, code, sheet), `--range`, `--at`, `--detail`, `--layers`. |
| `timelines words` | `--beats --draft --file --find --range --published` (no `--json`). |
| `timelines inspect` | `--json --limit --cursor --frame --range` (the manifest route; `domain_timelines.py:~680-686`, 1–50 rows, default 10). |
| `timelines check` | `--sweep` / `--no-sweep` (`cli_sweep.py:21-27`); no max-frames flag. |
| `media open` | `--materialize --max-bytes --preview-bytes --cache-root --json`. |

## Docs read
- `~/.claude/skills/astrid-rendering/SKILL.md` (lines 133-160, 258-290, 504-520): visualize presets, "Source decoding, waveforms, and filmstrips are private implementation details" (`:265-268`).
- `a/astrid/packs/rendering/docs/SKILL.md` (18 lines, no audio or cap content).
- `a/astrid/packs/rendering/docs/references/render-inspect-transfer.md` (`:264-275`, `:298-372`, `:406`).
- `a/astrid/packs/rendering/docs/references/placeholder-voiceover.md` (`:62-76`).
- `a/astrid/packs/rendering/docs/references/worlds-authoring.md` (`:528-535`, worlds only).
