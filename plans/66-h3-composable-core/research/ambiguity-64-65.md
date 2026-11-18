# Ambiguity pass: Plans 64 and 65

Read-only review of the task cards against `origin/release/14/main` (`9f614dff7707a493f29a548583f86c4791b957d2`), Plan 66 and the cached H3 motion-node schema. Citations are `path:line` in that source revision. The cards are implementation specifications, but several contracts conflict with the later job model or leave boundary behavior open. The replacements below are ready-to-paste card text.

## Genuine owner decisions

- **Rectangle edge ties (DS-3):** Code has no scaled-mask precedent. Options: retain `ceil(edge - 0.5)` (ties down; recommended because it is already specified in the card) or switch to `floor(edge + 0.5)` (ties up). Record the choice in the DS-3 fixture oracle. This is a small contract decision; no other owner decision remains open.

Plan 66 inputs record D5 as decided: continuation receives size/reference capacity through CC-7 and captured workflows are removed. No live quality, GPU, or machine claim is made here.

## Plan 64 — speaker references

### SR-1 — identity and occurrence record

**Could misread:** “occurrence identity” versus asset identity; where occurrence IDs originate; identity and derived tags; legacy receipt/build handling. The normalizer currently stores a media list in order and its digest is request-derived (`request_v2.py:127-147`, normalization below this section); records must distinguish repeated uses of one asset. Plan 66 says paths/generated files are outside identity and `placed` records retain occurrence and span.

**Replace SR-1 detail’s identity bullets with:** “Assign each media-list item a stable occurrence key from its authored list position (not asset ID); repeated assets and repeated trims remain separate. Include author-authored modality, role, trim/range, placement, edit/use intent, model and sampling settings in normalized identity. Do not put derived prompt tags, resolved paths, measured metadata, or generated files in identity. Derive tags from final effective node-input order. Reject v1 as stated. Sealed old receipts remain readable by their stored bytes; an old in-flight build that cannot be normalized under the new contract fails with `rebuild this request`.”

Also replace “paired-soundtrack choice” with: “A video reference contributes its soundtrack only when the node input binding includes it; record that as one video occurrence with its video and optional soundtrack effective inputs, not as a second authored audio occurrence.” This removes uncertainty about counting/binding. Plan 66 CC-1 should own the definitive `job` type; do not add a second parallel record definition.

### SR-2 — limits and preflight

**Could misread:** “clips” could mean request range, measured file duration, or each model input; whether video soundtrack consumes a file slot; “valid but sum past” needs per-modality definitions; “12 files” conflicts with video plus soundtrack; schema/model-card bounds are not the same as lowering limits. Existing `prepare_request` resolves assets and validates before compile (`prepare.py:427-478`); source checks are currently route gated (`prepare.py:164-165,275-285`).

**Replace the table notes with:** “Key limits by input type and name the source for each row. Count image, video and standalone-audio effective inputs separately against 9/3/3 slots. A video occurrence consumes one file; if its soundtrack is enabled, count its measured audio duration against audio time, but do not count the same file twice. Count standalone audio files toward the conditioning-file limit; state explicitly whether that limit includes video files. For duration, measure the selected trimmed interval after probing the file; reject an unreadable stream or a trim whose end exceeds measured stream duration. Sum selected durations by effective modality. Fixed placed replacement audio is excluded from *conditioning* limits. Put model/node facts and Astrid lowering restrictions in separate table sections; every refusal names the row and remedy. Do not call 124–362 frames a universal 2–15 s rule: state the actual accepted tick range and route exceptions in the row.”

Resolve “12 conditioning files” from a product rule (not node schema) in Plan 66’s capabilities table; until evidence in the model card/source establishes which file categories count, retain the exact intended list in the card. Do not silently infer “conditioning files” means all files.

### SR-3 — compile record and tags

**Could misread:** “one route” still requires how input rows map back to request occurrences, and “prompt tag no row has” may reject literal prompt prose. Existing builder is keyword-only and currently has image refs plus video refs as separate parameters (`generation.py:205-211`); masked compile rejects adapters (`compile.py:489-493`); row order needs to follow actual node inputs, not source media order. Plan 66 CC-1 supersedes field shape and requires feature-selected lowerings.

**Replace SR-3 detail with:** “Build one resolved job from normalized author intent and measured bindings; the compiler takes only that job plus bindings/output directory. Keep each effective reference row as `{occurrence, modality, trim, input_binding, tag}`. Construct rows in the exact order passed to node slots, preserving request order within each modality; apply any node-specific cross-modality ordering explicitly (video soundtrack before standalone audio only if that is the emitted node order). Verify prompt tags only where they are generated reference labels; do not scan/reject arbitrary prompt text that happens to contain angle-bracket text. Adapter and mask combinations are capability-table decisions, not unconditional compiler refusals.”

### SR-4 — exact stills

**Could misread:** “source frame 0” as model input versus compositor overwrite; source audio needed despite absent audio; duration/gap semantics; Plan 66 adds arbitrary-frame still placement. Existing compositor treats source as timeline baseline and uses it for kept portions (`compose.py:820-860`); current source preflight demands fixed dimensions (`prepare.py:238-242`).

**Replace SR-4 detail with:** “This is a special case of a placed exact still, implemented through the job’s placed-item and grant rules. For Plan 64 compatibility, prove a still at frame 0: preparation creates a full-duration held-frame video source and silent audio baseline; generation is permitted from frame 1 onward; composition pastes the still exactly at frame 0 and uses generated audio where the audio grant covers it. Do not add a separate frame-0-only compiler path. Plan 66 CC-8 owns exact stills at other frames and their chunk holds; keep this frame-0 case as a compatibility fixture there.”

### SR-5 — generated and supplied audio

**Could misread:** whether the audio mask gates latent noise or controls delivered sample ownership; whether fixed audio is a grant or placed item; mask shape/channel and application order are unspecified. The current masked node exposes clip-wide `audio_strength` (`ComfyUI-H3-Motion-Context-MultiRef@cpu-runtime.json:26-62`), while the pinned motion pack also provides `MiniMaxH3SetAVNoiseMask` with optional `audio_mask: MASK` (`...json:2989-3027`). The schema establishes the socket type, but not the mask raster shape/time alignment. Composition separately selects generated/source intervals (`compose.py:847-860,955-958`). Plan 66 explicitly separates grant influence from delivered ownership.

**Replace SR-5 with:** “Keep three separate concepts in the job and dry run: requested audio grants, the node’s effective audio conditioning/noise control, and delivered audio ownership intervals. Do not claim a per-window audio-noise mask is supported by the current node: its cached contract exposes clip-wide `audio_strength`, not a time-mask input. If per-window generation requires `MiniMaxH3SetAVNoiseMask`, implement that node only after confirming its pinned schema’s input type/shape and graph insertion point; otherwise refuse mixed generated windows before claim and retain source audio outside a single generated interval in composition. Fixed supplied audio is a placed exact item and wins on its own interval. A generated audio span uses candidate samples; uncovered spans keep source samples. Record exact sample intervals and one-sample tolerance.”

**Plan 66 conflict:** CC-1 currently says `audio_strength 1 when any audio is generated`, which may destroy source/supplied context unless the audio mask is bound at the latent. Amend CC-1 to name the pinned `MiniMaxH3SetAVNoiseMask.audio_mask` socket, define a time-indexed two-stream mask fixture from the pinned implementation, and make unsupported combinations capability refusals. The socket exists; its temporal layout and alignment still need implementation evidence.

### SR-6 — dry run/result

**Could misread:** “same rows” does not specify which fields persist after scratch cleanup; Plan 66 CC-3 replaces this narrower view. Current `_sealed_plan` retains compilation digest, output contract, intent, workflow-member hashes and input hash only (`stages.py:68-82`).

**Replace SR-6 with:** “Implement this as Plan 66 CC-3’s resolved-job view, not a parallel `h3.compilation` representation. Persist a self-contained view of requested occurrences, effective reference bindings/tags, effective canvas, grant influence and delivered intervals; it must not depend on scratch asset files. Readback after cleanup reproduces the same view.”

### SR-7 — recipes/docs

**Could misread:** voice-to-face behavior is prompt prose and explicitly untested, while admission tests prove only request acceptance. Plan 66 CC-5/6 replaces manual recipe prose with installable templates and skill rewrite.

**Replace SR-7 with:** “Do not add standalone recipes to the skills. Preserve these two use cases as complete admitted request fixtures and later convert them to Plan 66 CC-5 recipe files. Describe voice-timbre tagging only as an unverified model prompt convention; do not say it binds a voice to a face or imply CPU admission proves that effect. CC-6 owns final skill wording.”

## Plan 65 — dynamic output size

### DS-1 — request size contract

**Could misread:** numbers may be parsed as booleans/floats/strings; whether range applies independently to each dimension; array versus object; “every route except continuation” becomes obsolete under CC-7. Plan 66 has `canvas` on the job and moves continuation into that model.

**Replace DS-1 scope/proof with:** “Normalize optional `output.size` as exactly two JSON integers `[width,height]` (booleans excluded); each dimension independently must be 32..16384 inclusive and divisible by 32. Default once to `[1024,576]`; absent and explicit default normalize identically. Store only the resolved canvas on the job. Until Plan 66 CC-7 lands, a non-default size on the captured continuation is a named capability refusal; after CC-7 it follows the same canvas contract. Remove the continuation exception then.” Keep the listed boundary examples; add `[32,64]` and `[16384,32]` to prove independent bounds.

### DS-2 — conform

**Could misread:** “fill and fit” do not say which mode is selected; source aspect ratio behavior, output dimensions and no-reconform behavior are not fully defined. Current preflight hardcodes 1024×576 and 24fps (`prepare.py:158-160,238-242`); composition uses source dimensions as output authority and scales candidate/mask to them (`compose.py:844-845,939-947`).

**Replace DS-2 proof with:** “Use the requested canvas as the conform target and as the frozen source dimensions. State the existing conform mode used by each route (fill or fit) in the preparation manifest; preserve its crop/pad rule. For same-size frozen sources, reuse bytes without a second conform; if frozen dimensions differ from the resolved canvas, refuse with measured and requested sizes. Composition output dimensions equal the job canvas, including candidate and source segments. Test one fill and one fit source with known landmarks and verify both decoded frame dimensions and manifest.”

### DS-3 — static masks

**Could misread:** rectangle schema has no stated origin convention/unit; edge rounding formula is ambiguous for negative/fractional coordinates; “still-image exact-size refusal becomes decoded-coordinate checks” doesn’t identify threshold semantics; composition currently independently rescales masks (`compose.py:923-928`). Plan 66 consumes Plan 65’s target-sized artifact, so this is retained foundational work.

**Replace DS-3 detail with:** “Coordinates are pixel-edge coordinates on a top-left-origin canvas; `[x,y,width,height]` denotes half-open `[x,x+w) × [y,y+h)`. Validate finite coordinates and positive width/height wholly within declared canvas before scaling. Map each edge with `floor(value + 0.5)` (ties upward), clip only after validation, and rasterize once at target dimensions. For image masks, decode to grayscale, apply the existing explicit threshold if present, then nearest-neighbor resize. The compiler binds that exact raster to H3 and composition; composition must not redraw or resize it. Preserve moving-video mask size/clock/lossless refusals.”

The card’s `ceil(edge - 0.5)` rounds half ties downward; state this explicitly in the fixture oracle. The alternative is `floor(x+.5)`, ties upward. This is a genuine owner choice because current code only supports exact source-sized masks (`static_regions.py:46-80`) and does not define scaled-edge rounding. Recommendation: keep the formula already written in DS-3 (ties down), so the task card itself defines the rule; Plan 66 inherits it. This is a narrow decision to record in the task text/inputs, not a blocker for the feature.

### DS-4 — bind all generation paths

**Could misread:** width/height bindings might mean only node fields versus preparation, decode, mux, dry run and retained receipt. Existing `build_generation_workflow` receives `frames` but no canvas size (`generation.py:205-211`); static masked compiler resolves at 1024×576 (`compile.py:506-536`); sealed plan currently has no canvas (`stages.py:68-82`).

**Replace DS-4 with:** “Bind `job.canvas` at every node input that creates, resizes or decodes video/image tensors. Preparation’s source preflight, conform output, mask raster, generated candidate, composition source/candidate/mux and receipt all report the same resolved canvas. Enumerate every emitted width/height input in each graph family and assert it equals the request. Do not count hard-coded workflow constants that are not active graph inputs; remove/parameterize any active fixed-size selector.”

### DS-5 — docs

**Could misread:** “quality is only known at tested sizes” has no tested-size list; recipes are replaced by CC-5 templates; `mask.canvas` authoring support needs schema location and default semantics.

**Replace DS-5 with:** “Before CC-5, add the size examples as admitted request fixtures only; CC-5 converts them into recipe files and CC-6 owns final docs. State only the tested sizes with evidence in the test inventory; for other accepted sizes say quality is uncharacterized. `mask.canvas` applies to rectangle/polygon authored coordinates; omission means the legacy 1024×576 canvas. Still-image masks use their decoded pixel dimensions. Do not promise voice-only quality from issue #885 without a live result.”

## Contradictions with Plan 66; cut/retain

- **Record and compiler:** Plan 64 SR-1/SR-3’s `GenerationInputs` name and per-route construction are transitional. Plan 66 CC-1 explicitly consumes that model but renames it to a resolved `job`, removes `spec.py` as an internal format, and has one `compile_job`. Keep SR-1’s occurrence/identity decisions; cut the competing record/API implementation from 64 and assign its final form to CC-1.
- **Limits:** Plan 64 SR-2 remains useful, but Plan 66 CC-2 owns the final capability table and user-facing refusals. Keep source-labelled limits and pre-claim measurement; cut duplicate “limits table” implementation from 64, make it an input to CC-2.
- **Audio:** Plan 64 SR-5’s interval-level node mask is not established by the node schema. Plan 66 CC-1 repeats an `audio_strength` rule but does not specify a confirmed time-mask input. Resolve before implementation as above; do not silently ship contradictory semantics.
- **Frame-0 still:** retain as CC-8 compatibility case; cut the standalone SR-4 route-specific lowering. CC-8 covers arbitrary placed stills and their exact spans/chunk rules.
- **Dry run/receipt:** cut SR-6 and DS-4’s independent reporting slices; CC-3 replaces both with one resolved-job view.
- **Docs:** cut SR-7 and DS-5 as independent final prose tasks; preserve their fixtures/use cases for CC-5 and hand final wording to CC-6.
- **Size:** DS-1–DS-3 are foundational and should be retained before Plan 66; DS-4 is superseded by CC-3 for reporting and CC-1/CC-7 for graph binding. Keep the graph-binding assertions as CC-1/CC-7 proof, not a separate DS-4 task.
- **Continuation:** DS-1/DS-4 continuation exception is temporary until CC-7. Plan 65 correctly excludes captured-workflow changes; do not implement size in those graphs twice. CC-7 owns the port and then removes the exception.

## Other task-card ambiguities to resolve at dispatch

The `critical path` in Plan 64 lists SR-5 and SR-6 as parallel, then SR-4 after SR-5; that is consistent, but SR-7 depends on SR-3/4/5 and should also include SR-6 only if its dry-run claims reference the final view. Plan 65 says DS-2 and DS-3 parallel; both touch prepared source/canvas assumptions but separate symbols, so state merge order only if they edit a shared function. All three task lists claim pinned worker test commands; this research did not run tests or verify worker availability.
