# Timing route sandbox probes and source metadata

Stack: release-14-plan-69. Sandbox project `23d9b5a570b2498d878edced4f3d4942`, timeline `r6-occurrence-swap-probe` at head `authoring-parent-revision-bc0c42e5585e6ab65c38a028f5b8a71477178ddb828784b4242b43936c35fdf3`. All attempted commits below were `dry_run:true`; no publication occurred.

## Fixed-time internal clip timing preview succeeds

A one-field guarded `doc.patch` changed only existing fixed-time `r6-occurrence-swap-probe-clip.hold` from 2.0 to 1.966667 seconds on the existing shot occurrence. The SDK session call was `t.session.commit_many([cmd], label="sandbox one-clip hold preview", merge="atomic", dry_run=True, base=t.head)`. Runtime returned `ok:true`, `data.status="preview"`; the canonical candidate carries only that hold change. Exact request with command and expected base: `tighten/sandbox/fixed-855c9f50143b4f0db0acda575d0a6203.request.json`; exact response: corresponding `.response.json`.

A separate attempt through high-level `Timeline.commit(lambda x: x.clip(...).hold_for("59f"), dry_run=True)` obtained a Runtime preview but then failed in local post-preview diff with `KeyError: '_runtime_document'`. Source: installed `astrid/sdk/timeline/commit_session.py:1003,1017`, `emitter.py:185`, `commit.py:308`. It left no pending change or active flight. The supported session-level `commit_many` route above avoids that local diff path. Two deliberately invalid exploratory nudges were rejected by Runtime because the test clip was at the occurrence start or exceeded its end; they do not indicate a timing-binding limitation.

## New shot-owned word declaration is refused by Runtime

On a fresh outbox and unchanged sandbox head, a one-field patch added `app.astrid.on = '"up" in N12'` to that existing shot-owned internal clip; request used `before: {state: absent}`. SDK emitted/captured the command and sent it via `commit_many(... dry_run=True ...)`. Runtime returned `CommitRefused`, `validation_error / invalid_document`, exact message:

```text
candidate.timing: missing exact word binding for ('r6-occurrence-swap-probe-occ', 'r6-occurrence-swap-probe-shot', 'r6-occurrence-swap-probe-clip').on
```

Base and current revision are the same; no conflicts. Exact request: `tighten/sandbox/word-faa799e4156d4eedb0901ca1ee1ffd23.request.json`; exact refusal response: matching `.response.json`.

## Detached document check does not prove a publish bypass

A fresh detached document checkout at the same sandbox head succeeded to `tighten/sandbox/word-doc-retry.json`. Setting the same clip's new `app.astrid.on` field and running:

```text
bash edits/stackpy.sh -m astrid.packs.rendering.docs.scripts.timeline_document check --file tighten/sandbox/word-doc-retry.json
```

returns `validation.valid: true` and shows one changed path, `shots.r6-occurrence-swap-probe-shot.internal_timeline.clips.r6-occurrence-swap-probe-clip.app`. The generated local check artifact is `tighten/sandbox/word-doc-retry.check.json`.

The CLI's `check` validates/diffs locally; its `commit`/`publish` branch has no dry-run argument. Installed `astrid/packs/rendering/docs/scripts/timeline_document.py:246-306` builds document publish commands and sends them through `session.commit_many(... merge="atomic", base=...)`, where Runtime timing validation still applies. I did not run publish. The direct SDK Runtime dry-run on the identical app-field change is the evidence that the local “valid” check cannot bypass Runtime's missing-binding guard. Source guard is additionally at `astrid/sdk/timeline/_commit_timing_validation.py:126-133`; exact word-anchor capture requires a parent clip target in `astrid/sdk/timeline/native_word_anchor.py` (the internal target fails ownership/capture constraints).

## Music source tags and current handling

Read-only stack-Python `ffprobe` inspection of the Runtime CAS object with requested SHA-256 `fece12c84484802f5caa6e8c4565bbc65b23b3639170d46443b163f569bee642` confirmed the full hash. It is 39,301,584 bytes, WAV, PCM signed 16-bit little-endian, stereo, 48 kHz, 204.695521 s. Both container `tags` and stream `tags` are null. No audio copy or external processing was made.

Current authored parent timeline rows in `edits/current-bundle.json` use the source on the music track at unity volume: `music-song` at 0, source from 0, hold 8.6667s, fades 0.5/0.25s; and `music-song:b` at 8.4s, source from 7.808333s, hold 188.1667s, fades 0.25/1.5s, marked `app.split_from=music-song`. Neither row has `app.astrid.duck` nor an automated duck instruction. `sfx/mix.py:1-45` and `freeze/mix.py:1-42` show the nearby manual audition/production scripts: they decode the music asset, place it at unity, sum voice/SFX and music, and encode audition files. They do not sidechain/compress/duck music; the script's explicit level calculations apply to the new SFX candidates. Thus the source WAV's internal mix provenance cannot be recovered from its metadata tags, and these nearby scripts do not show automated ducking.

The installed `astrid.packs.music` package remains absent (`find_spec` returned `None`; importing `astrid.packs.music.actions.duck.api` returned `ModuleNotFoundError`). `Clip.tag(duck=<mapping>)` writes metadata via `sdk/timeline/model.py:610-625`; it is not a runnable `duck_timeline` action.

## Film timing refusal (verified against current head)

Command: `bash edits/stackpy.sh -u tighten/preview_anchored_start.py`.
One guarded `doc.patch` changes only `c19-00-am-snap-plate.at`, 6.433667 → 5.833667 seconds in its owning internal timeline; its `on` declaration, hold and params remain unchanged. `dry_run:true`, base=current `943c209e…`, no conflicts.

Verbatim Runtime message:

```
candidate.timing: missing exact word binding for ('occ-77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66-occ', '77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66', 'c19-00-am-snap-plate').on
```

Expected: preserve the exact existing word declaration while translating the clip with its narration. Source: installed `astrid/sdk/timeline/_timing_evaluators.py:413-425` requires the binding; `_commit_timing_validation.py:109-118` includes `at` in the basis for legacy internal word declarations; `native_word_anchor.py:233-257` limits the supported capture route to parent clips. Exact evidence: `anchored-start-command.json`, `anchored-start-error.json`, and the private isolated SDK outbox. Timing publication stopped. Replacing affected word anchors with fixed declarations would change their behavior and was not performed. Smallest product change: authenticate exact word bindings for occurrence-owned clips, including timing-only changes.

The complete arithmetic candidate has 389 rows (`plan.tsv`), unchanged music, and 105 exact field changes (25,960 compact command bytes). Detached `check` accepts its authored schema/diff. `emit_document_publish_commands` does not lower placement changes: it raises `DocumentPatchError: closure membership or provenance changed; use a semantic command` (`sdk/timeline/emitter.py:266-267`). The existing `sdk/timeline/authoring_commit.py:184-253` physical occurrence lowering was used to prepare the guards. Complete previews, with separate commands and with one combined command, both first hit `candidate.shots['77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66'].internal_timeline.clips['c29-06-am-sprite']: timeline interval must fit the occurrence's half-open bounds`. The minimal c19 preview above isolates the decisive word-binding refusal without that intermediate occurrence-bounds issue. No timing preview published.

## Render admission: retired file locator (#1238), not dropped

Command: exact argv in `render-command.json`, invoked foreground by `python3 -u tighten/render_attempt.py` (stack CLI `timelines render` with canonical IDs, `--backend rendering.remotion`, native 1920×1080 / 30 fps / AAC profile, `--wait --json`). Exit 1 after 4.726489 seconds. No task/run was created.

Verbatim message:

```
canonical registry asset 'a09025f7-40ed-4202-ba40-2d4a61d352a9' contains retired media locator field(s): file
```

Details: validator `managed_media_locator`, path `$.assets["a09025f7-40ed-4202-ba40-2d4a61d352a9"]`, reason `live rendering accepts runtime-managed object ids and digests only`. Source: installed `astrid/packs/rendering/actions/render/managed_timeline.py:627-638`. This stack refuses the field before Runtime render admission; the reported drop behavior was not observed.

Both affected registry entries already name managed digest `sha256:4ab84c47567ab892fe2e8620042523c2f9a242d495793c5c590cc448046d625d`, and no remaining clip references either alias. Product `--replace-asset` cannot repair unused aliases: `sdk/timeline/edits.py:608-613` requires a referencing clip and raises `no clips use asset key …`. Guarded SDK document repair therefore removes only each redundant `file` key, preserving both managed media IDs, all pins, all other fields, and every authored clip. Preview accepted; publication result is recorded separately in `registry-repair-summary.json` when completed. This is an authorized render remedy, not a ripple edit.

## Render retry reaches preflight, then loses its execution lease

After the two-field registry repair was published at `authoring-parent-revision-f9237406fdda59eea5c81e30fd6548eb7b42e0a26655058155f6db6da97e5488`, `python3 -u tighten/render_attempt.py` retried the exact native profile (`render-command.json`, 4-hour foreground wait budget). It failed after 47.670378 seconds, exit 1. Task `5327fa0e32eb4c2e84995564486dcf2f`, run `481927383de24bf6ac75ae4fdc43fd96`, attempt `f2eda62c7d224969907769dad23fbd0b`.

Verbatim CLI message:

```
task 5327fa0e32eb4c2e84995564486dcf2f, attempt f2eda62c7d224969907769dad23fbd0b: lease expired with unresolved custody; reconciliation required. Recover with: astrid tasks cancel 5327fa0e32eb4c2e84995564486dcf2f
```

Verbatim task failure: `execution lease lost: lease_fenced`; diagnostic category `heartbeat_exception`, runtime code `lease_fenced`, retryable `false`. Last successful heartbeat 17:16:41.931304 UTC, expiry 17:17:11.925 UTC; task failed at 17:17:16.294 UTC. Successful Remotion validation phases `complete_inputs` (9,770ms) and `owned_probe` (180ms) precede the host's Runtime transport timeout. This attempt does not reproduce #748's explicit-root refusal; assigning it to that issue would be speculation. The actual underlying cause of Runtime transport stalls is unproved by available logs.

Supported recovery command executed: `bash astrid-stack.sh tasks cancel 5327fa0e32eb4c2e84995564486dcf2f --project 801a01b3a87941a1ab25958c488afdbf --json`. Response `ok:true`, task remains terminal `failed`, same lease-loss result. No additional render started. SDK source for the reconciliation instruction: `astrid/sdk/invocation.py:3600-3635`; host handling of heartbeat exceptions at `astrid/core/execution/generic_host.py:12097,12277,12991,13534`. Exact source trace and host log line references are in `render-failure-trace.md`. Smallest product repair indicated by the evidence: keep the admitted pack host's lease renewable during Runtime requests and provide a working custody reconciliation/retry path. Which transport/lock operation needs correction remains inferred, not localized by the logs.

No MP4, ffprobe output, rendered-file stills, or Desktop delivery exists. No screen recording substituted. Only before-editor stills are valid; their retry and contact sheet are in `verify/before/`. `published-assertions.json` verifies from a fresh unique-outbox Runtime read that all389 clips and all7 placements are unchanged; only two unused registry `file` fields were removed.

Disk: 6.3GiB initially, 8,949,526,528 bytes free before the second admission, 8,929,689,600 after failure. Product estimate: scratch6,490,478,241 + output406,741,131 bytes; subtracting both from admission free would leave2,052,307,156 bytes (1.91GiB), below requested2GiB. This estimate is a separate limit for another attempt; no actual disk-floor breach was observed. Recheck and secure the full reserve before any future render retry, including any output materialization/copy. The task failed on lease loss, not a recorded disk-full error.

## Audio verification and measurement limits

`audio-tail-metrics.json`: the removable N10 tail48.166667–48.207700 is0.041033s at−52.78dBFS, compared with−21.43dBFS for “two million”; removed room tone0.558967s is−69.46dBFS. Transcript last-word end48.0277 and next-word start48.8777 give0.8500s. RMS thresholding in10ms windows instead gives0.725s current acoustic gap at−45dBFS, ranging0.715–0.775s for−50…−35dBFS. Thus an18-frame proposal implies0.125s acoustic gap at−45dBFS (0.115–0.175 range), while14 whole frames imply0.258333s. This is threshold-dependent, not an exact phonetic boundary. Timing publication was refused, so no measured edited-after gap exists; `gap-before.m4a` is the actual current46–51s mix. `voice-sync-check.json` distinguishes three proposed−0.6s deltas from published0s deltas.

Primary per-line music measurements are now `music-levels.tsv/json`, with reproducible `measure_music_levels.py`. Source windows use exact clip timing and gain, voice mono is converted to stereo with FFmpeg's energy-preserving `aformat=channel_layouts=stereo`, stereo music is preserved, then integrated EBU R128 loudness is measured. This matches the channel conversion used by `sfx/mix.py`'s FFmpeg `-ac2`; it is a source-window model, not a successful product-render mix.26 lines: music averages8.24LU below voice currently (7.5–11.5),8.29LU in hypothetical18-frame-shift windows (7.0–13.5). Root independently reproduced N11: voice−19.7LUFS; music−27.5 current /−27.8 proposed; differences7.8/8.1LU. Earlier channel-average figures collapsed stereo phase and were unsuitable for the requested stereo comparison; retained only as explicitly labeled diagnostic files. No music was externally processed or replaced.

Optional extra orange-sweep frames at150.9/157.2s did not produce verified output before the final stop. The extra capture worker was stopped; no extra stills are claimed. The original20-frame baseline contact sheet remains valid. This does not change the blocked status: no after timing publication exists to compare.
