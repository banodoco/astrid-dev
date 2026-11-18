> Historical research, not instructions. Where this differs from the current plan, inputs or tasks files, those win.

# Plans 64–66 neutral-executor handoff review

**Read-only review, 18 November 2026.** Source plan worktree: `/home/user/work/recast/plans6465`, branch `claude/vibrant-noether-us2vx6`. Code baseline checked: `astrid-agent` `origin/release/14/main` at `9f614dff7707a493f29a548583f86c4791b957d2`; pinned node source: ComfyUI `6bfaacc`. No tests run and no repository files changed. The report cites the plan worktree and the pinned code snapshot; node citations refer to `Comfy-Org/ComfyUI@6bfaacc`, `comfy_extras/nodes_minimax_h3.py`.

## 1. Intended end state and rationale

**Yes, the intended end state is recoverable from Plan 66 itself.** The clearest explanation is 66 plan.md:21-34 (`recast/plans6465/plans/66-h3-composable-core/plan.md:21`): one job consists of canvas, exact placed items, soft conditioning, grants, prompt/model/sampling; “Placed material is kept. Time nothing covers is generated. A grant opens placed material for change.” Continue, start image, inpaint, redub and Character Swap are data in that shape rather than route/preset code. The reason is repeated in 66 inputs.md:24-29 (`recast/plans6465/plans/66-h3-composable-core/inputs.md:24`): v2 already expresses the model's timeline/reference/edit structure, while route-specific compilers make old product paths restrictive; presets or a new language would encode routes again.

The requested conceptual package reads as follows:

- **Three families:** Output (exact placement/edit), Context (soft reference/guide/prompt), Process (soft LoRA/control/settings). The motivation and taxonomy are in 66 inputs.md:67-70 (`recast/plans6465/plans/66-h3-composable-core/inputs.md:67`), with the deeper definitions/examples in research/levers.md. The main plan describes exact versus soft but does not itself name the families.
- **Three rules:** placed material is kept; uncovered time is generated; grants open placed material for change (66 plan.md:28 (`recast/plans6465/plans/66-h3-composable-core/plan.md:28`)).
- **Place/guide/reference ladder:** a timeline item is exact placement; `role: guide` is soft timed conditioning; a reference is untimed conditioning. Plan 66 makes guide explicit because `hard: false` already means exact timeline placement (66 tasks.md:89-100 (`recast/plans6465/plans/66-h3-composable-core/tasks.md:89`)). This ladder is spread across tasks/research, not summarized in the outcome.
- **One compiler:** normalize author intent, prepare measured bindings and one resolved job, call `compile_job(job, bindings, out_dir)`, compose exact ownership. Lowerings add features in a fixed order (66 tasks.md:37-61 (`recast/plans6465/plans/66-h3-composable-core/tasks.md:37`)).
- **Capability table:** keyed by lever kind and used for admission, named conflicts, refusals and `describe`; each row has a verifiable source (66 tasks.md:22 (`recast/plans6465/plans/66-h3-composable-core/tasks.md:22`)).
- **Templates and thin skills:** request files with named typed holes fill to ordinary v2 requests; a general H3 skill teaches the core, while Recast retains editorial judgment and points to recipes (66 tasks.md:114-155 (`recast/plans6465/plans/66-h3-composable-core/tasks.md:114`)).

**Why is partly buried.** The three families’ “exact vs soft” axis and shared fields are explained fully only in `66/research/levers.md`; proof that a small model can use the compressed presentation is in `haiku-tests.md`, and the candidate skill text is `skill-draft.md`. The plan says “capabilities as lever kinds” but does not explain why those families are useful or show their hierarchy. The place/guide/reference distinction is recoverable from CC-4 and the schema discussion, but absent as a short statement in plan.md. The continuation mechanism and why the port is needed live mainly in `inputs.md` and `research/continuation.md`/`ambiguity-cc7.md`. The rationale for exact still chunk holds is mainly CC-8 and research. A newcomer can derive the intent, but has to assemble it from multiple cards and research.

## 2. Sequencing and dependencies

### Plan 64, in listed execution order

| Order | Card | Declared dependency | Neutral executor finding |
|---|---|---|---|
| 1 | SR-1 typed reference occurrences | owner scope | Valid prerequisite: current `normalize_v2` assigns tags at normalization and hashes derived tags into identity (`request_v2.py:333-455`); Plan 64 proposes occurrence identity and compiler-derived effective tags, which must precede admission/compiler work. |
| 2 | SR-2 limits/admission | SR-1 | Valid: needs normalized occurrences/use and `prepare.py` measurements. The node has 9 image, 3 video, 3 standalone audio and 3 paired video-audio ports (`nodes_minimax_h3.py:263-283`); soundtracks are index-paired (`:313-318`). |
| 3 | SR-3 single `GenerationInputs` lowering | SR-2 | Valid in broad order; depends on stable rows, limits and preparation. Existing builder currently has a large route-shaped signature (`generation.py:205-223`), not the record described by SR-3. |
| 4 | SR-5 masked audio | SR-3 | Declared parallel with SR-6; actual dependency is on record/builder and compose interfaces. It should precede SR-4 because SR-4’s generated audio strength 1 differs from the SR-5 baseline 0 and needs explicit generalized grant semantics. Current builder only supports masked video through `masked_edit` (`generation.py:214-219`), so SR-5 has a real new node-path dependency. |
| 5 | SR-6 dry-run/result rows | SR-3 | Can run parallel to SR-5 only if it persists requested/effective references independently of graph audio-mask details. It explicitly extends Plan 66 CC-3; risk of doing the view twice is acknowledged. |
| 6 | SR-4 frame-0 timeline still | SR-3, SR-5 | Sensible after audio path, but it implicitly requires the resolved placement/grant model and composition generalized enough to represent a synthetic full-length source and generated audio. This overlaps CC-8 substantially. |
| 7 | SR-7 recipes/request examples | SR-3, SR-4, SR-5 | Valid. Note Plan 66 CC-5 later turns these examples into recipes, so they are deliberately temporary fixtures/prose. |
| 8 | R | SR-1…SR-7 | Valid. |

### Plan 65

| Order | Card | Declared dependency | Neutral executor finding |
|---|---|---|---|
| 1 | DS-1 size normalization/resolved canvas | Plan 64 SR-3 | Valid. Must be after SR-3 because it extends `GenerationInputs.canvas`; current normalizer does not admit `output.size` (`request_v2.py:333-455`) and `prepare_request` independently defaults width/height to 1024×576 (`prepare.py:427-433`). |
| 2a | DS-2 source conform | DS-1 | Valid. Code currently hard-codes 1024×576 and rejects other dimensions (`prepare.py:159,241-242`). |
| 2b | DS-3 static masks | DS-1 | Valid, can parallel DS-2 only if both settle on the same effective canvas and artifact contract. DS-3 is a prerequisite of DS-4. |
| 3 | DS-4 bind size at generation entries | DS-2, DS-3 | Correct; all paths need conform plus mask handoff. This also changes Plan 64's builder contract and is a reason Plan 66 cannot start until Plan 65 lands. |
| 4 | DS-5 docs/examples | DS-4 | Valid. |
| 5 | R | DS-1…DS-5 | Valid. |

### Plan 66

Declared order is 66 plan.md:63-65 (`recast/plans6465/plans/66-h3-composable-core/plan.md:63`). Task-level dependencies in 66 tasks.md:17-33 (`recast/plans6465/plans/66-h3-composable-core/tasks.md:17`) mostly enforce it. The substantive hidden dependencies are:

1. CC-1.1 resolved-job schema must include a stable contract for placed-item source/span/offset, grants, canvas, measured ranges, generated/sampled/delivered counts, conditioning rows and persisted serialization before CC-1.2 can adapt every old compiler. The allowed “extend only fields below” list omits some later-required fields (e.g. output duration/counts, effective mask artifacts, reference use/tag derivation, fixed audio binding, guide positions). CC-1.1 is therefore not independently ready as written.
2. CC-1.2 claims only compiler entry point while CC-1.3 public hook migrates to v2; CC-1.2 says adapters at compiler boundary but does not name how prepared job and raw hook inputs coexist. The public path must remain working across merges, yet `compile_job` requires a prepared job. Define a temporary adapter boundary and its removal point explicitly.
3. CC-1.3's “combined request … placed clip with region grant and an audio grant” claims composability before CC-2 capability table and before CC-9/CC-4/CC-8. It is achievable only if CC-1.3 implements those combinations itself or returns explicit refusals. Current text allows refusal but calls the request a positive compile case. Contradictory proof requirement; split the positive supported combination from pair-refusal cases.
4. CC-2 capability rows require final lever schemas/fields, guide and prompt constructs, adapter contracts, and all actual conflict pairs. CC-2 runs before CC-9, CC-4, CC-8, while the table is said to be the sole admission truth. It can define extensible rows first, but cannot have a complete authoritative table until later features land. Require every later feature card to extend the table and its `describe` proof, or move a final reconciliation card after CC-8.
5. CC-3 dry-run view is ordered before CC-9/CC-4/CC-8 and is then extended by each. This is okay only if it specifies a stable versioned view and later cards own extensions. CC-3 currently calls its serializer “the single view” but does not state versioning/compatibility strategy; SR-6/DS-4 already persisted partial views.
6. CC-4 is correctly after CC-9; CC-8 after CC-4 is not technically required by node wiring, but ensures the soft-guide/exact-placement distinction is resolved before exact still composition. CC-5 must follow CC-8 because recipes depend on those features.
7. CC-7a follows CC-6 in the task table (although prefix continuation is product work, not documentation-dependent). That creates an unnecessary dependency on skills/templates. It also occurs after capability table and resolved-job work, which is real. CC-7b and CC-7c depend on CC-7a because they share its context helper; this is stronger than the earlier research recommendation to parallelize, but internally coherent.
8. CC-7b/c call for capability behavior and composition contracts produced in CC-1/CC-2/CC-3; their task rows only name CC-7a. Add CC-3 (view) and CC-2 (capability) as explicit predecessors if these reports/refusals must use the finalized interfaces. CC-7b/c also use CC-6 only indirectly for user-facing affordances; not a code dependency.
9. CC-7d correctly follows all three ports and removes flag only after a caller search, but D3 authorizes deletion without quality comparison. The CPU proof can show wiring and exact prefix paste, not model-output quality parity; the plan acknowledges this limitation. The user decision is explicit, so this is a risk statement, not an executor blocker.

**Work that is built then reshaped.** Plan 64 SR-1 to SR-3 creates typed-reference rows, a limits table, a `GenerationInputs` record and per-route compiler integration. Plan 65 extends that record and every builder entry point with canvas size and changes mask handoff. Plan 66 CC-1.1 then expands the same record into the definitive job; CC-1.2/1.3 adapt then remove route compilers; CC-2 expands SR-2’s limits table into lever-kind capabilities; CC-3 replaces/extends SR-6 and DS-4 reporting; CC-8 re-generalizes SR-4’s frame-0 path into all exact stills. These are acknowledged in prose, but scope/order lacks a merge strategy to keep Plan 64/65 code from being throwaway. The plans should either define Plan 64/65 as intentional enabling increments with explicit compatibility adapters and point to the exact CC task that consumes each interface, or move work whose only purpose is immediately superseded into Plan 66.

**Code cross-check summary.** Current `branch_for` chooses source-free/audio-only/extension/source-backed routes (`request_v2.py:472-479`); source-free rejects non-image references and continuation has two image slots (`compile.py:868-934`). Character Swap is strictly one typed image plus one video (`request_v2.py:306-308`). Builder accepts lists of images/videos, but no standalone audio list, and a route-oriented scalar/control signature (`generation.py:205-223,234-239`). Composition currently derives masks itself and can rescale them (`compose.py:425-505,910-945`); preparation and source verification hard-code 1024×576. This confirms the direction but means “compile one arbitrary job” is a substantial rewrite, not an interface-only refactor.

## 3. Contradictions and stale text

### Must resolve before dispatch

1. **Source-free image requirement conflicts across Plan 64 and 66.** Plan 64 says source-free animates a still and says “Generation needs no image” (64 plan.md:21-26 (`recast/plans6465/plans/64-h3-speaker-references/plan.md:21`)); its planning-evidence paragraph then says “Retain the image prerequisite on source-free generation” (64 inputs.md:34 (`recast/plans6465/plans/64-h3-speaker-references/inputs.md:34`)); Plan 66 restrictions accepted “no image required” (66 inputs.md:72-74 (`recast/plans6465/plans/66-h3-composable-core/inputs.md:72`)). Current compile rejects source-free without 1–9 image references and rejects video/audio modalities (`compile.py:881-885`), while builder itself requires an image unless masked (`generation.py:234-239`). Decide the intended contract and update SR-3/CC-1 acceptance. As written, text-only and audio/video-only use are simultaneously allowed and forbidden.
2. **Paired soundtrack capacity is missing from SR-2's table/counts.** Pinned node has `ref_video_audios` capacity 3 and `ref_audios` capacity 3 separately ([ComfyUI nodes_minimax_h3.py:272-283](/tmp/comfy-h3-source.py:272)); each soundtrack pairs by video slot and receives its own Audio tag before the Video tag ([same:313-339](/tmp/comfy-h3-source.py:313)). SR-2 lists 9/3/3 as images/videos/standalone audio and says soundtrack counts audio time but not a second file (64 tasks.md:47-67 (`recast/plans6465/plans/64-h3-speaker-references/tasks.md:47`)). It never states whether paired tracks count toward the standalone slot count, the 3 paired ports, total per-modality 15 seconds, or 12-file cap. In addition, SR-2 says duration per modality but defines effective audio inconsistently. This can admit requests the node cannot bind or reject valid ones. Split paired soundtrack port count, standalone-audio port count, audio-time total and file count into explicit rows with sources.
3. **CC-1.3 proof fights the accepted ambiguity correction.** Current card demands a specific formerly unsupported combined request compile (66 tasks.md:19 (`recast/plans6465/plans/66-h3-composable-core/tasks.md:19`)); accepted ambiguity report says add mixed case only when required fields already exist and “defer new combinations until capability rows can admit them” (research/ambiguity-cc1-3.md:16 (`recast/plans6465/plans/66-h3-composable-core/research/ambiguity-cc1-3.md:16`)). CC-2 is after CC-1.3. Make CC-1.3 prove only current supported combinations and named transitional refusals; place the new combination positive proof after CC-2 and the relevant feature lowerings.
4. **Capability table completeness versus order.** CC-2 is before CC-9, CC-4 and CC-8, yet is described as the sole capability/admission truth. Those later features (timed prompt, guide, placed still) must add rows/conflicts and `describe` tests. State that CC-2 establishes the table contract and each later card extends it, or add a final table reconciliation task. It also lists `control` as a lever kind even though ControlNet is “not in plan” and no control implementation exists; mark the row `unavailable` with an Astrid source or omit it until a later plan.
5. **Exact-still completion says every hold is four frames.** Plan 66 completion says each still’s dry run shows “its 4-frame hold” (66 plan.md:94 (`recast/plans6465/plans/66-h3-composable-core/plan.md:94`)). CC-8 correctly says multiples of 17 (including 0 and 51) are single-frame chunks, other frames hold four; research/restrictions also documents the correction. This completion sentence is stale and invalidates its own 0/51 cases.
6. **Plan 64 SR-4 says Plan 66 lifts exact stills at nonzero frames.** Plan 64 limit table says nonzero timeline images are refused “Plan 66 adds soft guides … and exact stills” [64 tasks.md:91-95]. The table entry can be mistaken for a promise that guide support lifts exact-placement refusal; guide and exact still are different. Plan 66 CC-8 does implement exact stills at any frame, so point directly to CC-8, not CC-4.
7. **60-frame bridge survives in archived research.** Final Plan 66 inputs and tasks correctly replace it with 39 + 63 + 39 = 141 frames ([66 inputs.md:96] and [66 tasks.md:30]); `research/restrictions.md:128` still proposes “A, 60-frame gap, B”, while `ambiguity-cc7.md:22,35` correctly calls it invalid. Mark old recommendations superseded prominently or correct the stale line so an executor/search doesn't copy it.
8. **CC-7 deletion evidence wording overclaims parity.** CC-7a CPU proves graph wiring and exact composition, while task's captured graph compare is structural. CC-7d deletes captured workflows before owner live test (explicit D3). “CPU parity list” in inputs.md:117 can imply behavioral parity, although plan completion says output quality is untested. Rename this “CPU graph/interface comparison”; state the port is structurally compared, not quality-equivalent.

### Stale/research-only and smaller inconsistencies

- `tasks.md:5` omits **CC-9** from Task ids even though critical path and row include it. Add CC-9.
- Plan 66 task rows CC-7b and CC-7c depend only on CC-7a, while the earlier accepted `ambiguity-cc7.md:22-26` has them depend on CC-3 and CC-6 and says they may parallelize if contracts are distinct. The phase order puts them after CC-6 anyway, but CC-3's job view and CC-2's admission/conflict rows are real code contracts. Add those explicit dependencies; avoid making CC-6 a code prerequisite unless recipe/skill artifacts are genuinely consumed.
- `research/fable-final.md:5-39` is an earlier “final” report and names resolved leftovers (CC-3 mistaken guide reference, DS-1 digest, wrong SR-4 pointer, duplicate reporting, recipe conversion). Current plan has fixed several; it is not wholly reconciled with the latest text (CC-1 combined-request issue remains). Mark it as a dated historical review superseded by the named ambiguity pass, and retain only unresolved findings in a current checklist.
- `research/levers.md:229-243` says “Nothing here adds a task,” places timed prompt and other functionality later, and suggests adding shared table fields; current Plan 66 has CC-9 in Phase 1 and includes timed prompts, while control/phase/event-curve remain out of scope. Since this file is cited as conceptual basis, mark these as superseded recommendations and distinguish the adopted abstraction from deferred feature proposals. Its claim that every control maps to one kind is useful; its old timeline is not.
- `research/ambiguity-cc7.md:46` recommends waiting for live comparison before deletion, but owner D3 explicitly chooses CPU-only deletion in `inputs.md:117`. It is labeled a recommendation, but flag it as rejected by D3 in the file or add a supersession note.
- `research/ambiguity-64-65.md:45-47` asserts the audio time mask was not established, while current 64 inputs explicitly say a time-mask input was confirmed and reject that claim (64 inputs.md:48 (`recast/plans6465/plans/64-h3-speaker-references/inputs.md:48`)); Plan 64 tasks specify exact pinned wiring and Plan 66 inputs accepts it ([66 inputs.md:95]). Mark those portions superseded; otherwise the same research pack directs implementers to refuse a feature the task requires.
- `64 inputs.md:34` says source-free image prerequisite while 66 restrictions say no image required (above). This appears to be an unedited accepted/rejected decision summary, not merely historical text.
- Estimate arithmetic: Plan 66's headline 13.5 = 8 + 5.5 correctly, but there is no card-level allocation or explanation of whether this is effort or elapsed time ([66 plan.md:11]). The earlier critique says the full scope exceeded a previous 7-day estimate ([66 research/critique.md:60-71]); current estimate is larger but no reconciliation states which added work it covers. Plans 64/65 add 4.5 days ahead of 66, giving 18 project-days total before any live owner test; not surfaced as a combined estimate. Add one compact phase/task estimate table, define person-days vs elapsed, and say predecessor work excluded/included.
- Plan 64 is titled “speaker references” but includes exact frame-zero placement, generalized interval audio generation and limits. These are intended prerequisites, but the estimates don't identify the cost of SR-4/SR-5 separately and the handoff order is fragile. Add per-card effort or adjust scope estimate based on explicit total.
- 64 SR-2 says source-free generation needs no image, but task's mixed source-free + masked fixture only checks references; no explicit text-only positive fixture. Completion should say whether text-only is admitted even though outside documented Ref2VA use, and include it in admission if yes.
- `skill-draft.md:27,46-48,58-76` contains reserved/unbuilt `phase`, `control`, `role: control`, `settings.loras`, `${holes}` template syntax and schema names that do not match the final CC-2 (`settings.adapters`), CC-5 (`{"$hole":"name"}` JSON files), or scope. CC-6 says start from this draft and keep about its length. It must be a conceptual copy source, not a literal implementation draft; list exact sections to replace and prohibit importing unsupported fields/examples. `skill-draft.md:13` also says a still covers one frame, while CC-8 default is chunk-hold (1 or 4 frames).
- Research-only Plan 64 `research/misc.md:27` still recommends a GPU spike for AddGuide compatibility; current owner D2 and Plan 66 D1 prohibit in-plan GPU/live runs. It is explicitly old research, but tag it “superseded by CPU-only owner decision; no task.”
- Plan 64 reference/source identities point at Plan 59 donor snapshot, while Plan 66 names `release/14/main` and earlier plans say actual release base is pending. This is not a code contradiction if dispatch rechecks it, but a “neutral executor” cannot dispatch until one integrated release SHA plus Plan 59/64/65 merge SHAs are recorded. The instructions' “Plans 64-66 to intended end state” don't themselves supply greenlight or run authorization; each plan says pending. Scope is understandable, but execution authorization is not present in these artifacts.

## 4. Prioritized concrete fixes (paste-ready text)

### P0 — make behavior and admission unambiguous

**A. Replace the source-free rule in `64/plan.md:26` and reconcile `64/inputs.md:34` with one decision.** If adopting Plan 66's no-image rule, replace with:

> Source-free generation accepts any reference mix admitted by SR-2, including no image reference. Text-only is admitted as a dry-run/CPU compilation case and is outside documented Ref2VA use; do not claim output quality. A start image is an optional exact placed still at frame 0 (SR-4). This removes the current source-free image prerequisite.

Then change `64/inputs.md:34` sentence “Retain the image prerequisite on source-free generation” to:

> Source-free generation does not require an image; this supersedes the current compiler’s image-only prerequisite. SR-3 proves text-only plus audio/video-only admission where supported by the node contract.

Or, if the owner intended to retain image as product requirement, replace Plan 66's “no image required” decision and capability examples. Don't leave both.

**B. Replace the capacity portion of SR-2 (`64/tasks.md:49-67`) with explicit counters:**

> Node input capacities are separate: 9 `ref_images`, 3 `ref_videos`, 3 `ref_video_audios` (paired one-to-one by video ordinal), and 3 standalone `ref_audios`. Count each enabled paired soundtrack against the paired-audio port capacity and the audio-duration total, but count its video occurrence as one supplied file. Count each standalone audio occurrence against standalone-audio slots, audio-duration total and the file cap. State the file cap's exact included categories in the table; do not count a video soundtrack as a second supplied file. Enforce per-clip selected-trim duration and summed selected-trim duration for effective audio (paired plus standalone) and video separately. Each row names its source and its error names the row.

Add paired-soundtrack over-capacity and mixed paired+standalone audio duration boundary fixtures. Derive the file categories from the referenced model card and state them, rather than “conditioning files.”

**C. Replace CC-1.3 mixed-request proof (`66/tasks.md:19`) with:**

> Trace the public invocation for the four currently supported cases through normalize → prepare → `compile_job` → compose → receipt. Prove only combinations admitted by the current capability table. Until CC-2 and the feature card that adds a combination have merged, assert the named refusal for each unsupported pair. Move the positive case combining a placed clip, region grant, audio grant, three image references and speaker clip to the last of its enabling feature cards; it compiles only after each pair is admitted and its graph inputs and composition intervals are asserted.

**D. Replace Plan 66 completion line (`66/plan.md:94`) with:**

> Exact stills at frame 0, a single-frame chunk (for example frame 51), a four-frame chunk (for example frame 61), and the last delivered frame are pixel-exact. The dry run shows each still’s requested frame, snapped chunk and delivered hold (one or four frames, clipped at the output end).

### P1 — align contract sequencing and make references authoritative

**E. Replace `66/tasks.md:5` task-id line with:**

> **Task ids:** `CC-1.1` … `CC-1.4`, `RS1`, `CC-2`, `CC-3`, `CC-9`, `CC-4`, `CC-8`, `CC-5`, `CC-6`, `CC-7a` … `CC-7d`, `R`.

**F. Add to CC-2 scope, and repeat in each later feature card:**

> CC-2 establishes the capability-row schema and initial rows for existing features. Every subsequent card that adds a request kind, parameter, limit or supported combination updates this same table, its admission checks, conflict rows and `describe --json` fixture in that card. `control` remains `unavailable` and refuses requests until a separately scoped lowering is implemented. No future field (including `phase`) is accepted just because it appears in the shared-field vocabulary.

**G. Replace CC-7b/c dependencies:**

> CC-7b depends on CC-2, CC-3, CC-6 and CC-7a. CC-7c depends on CC-2, CC-3, CC-6 and CC-7a. CC-2/CC-3 provide admission and resolved-job contracts; CC-7a establishes the shared context helper. If the recipe/skill files are not consumed by these code changes, remove CC-6 from these dependencies.

**H. Replace CC-8 phrase in Plan 64 SR-4 detail and limit table:**

> A timeline still outside frame 0 is refused by Plan 64 as a temporary lowering limit. Plan 66 CC-4 adds soft guides at other frames; Plan 66 CC-8 adds exact still placement at any frame. A guide does not lift the exact-placement limit.

**I. Add this note at the top of `66/research/` files that contain old recommendations (fable-final, levers, restrictions, ambiguity-cc7, ambiguity-64-65):**

> **Historical research; not execution authority.** Where this note conflicts with current `plan.md`, `inputs.md` or `tasks.md`, the current plan files win. In particular, the 60-frame bridge, live-comparison-before-deletion, source-free image prerequisite, frame-0-only exact still, and “audio mask unsupported” recommendations were superseded by the current task cards/owner decisions.

Also correct `restrictions.md:128` from “60-frame gap” to “63-frame generated middle; total 141 frames” or strike it as superseded. Add a final “adopted / rejected / superseded” index in inputs.md instead of relying on readers to compare every review round.

### P2 — make delivery and effort realistic

**J. Replace CC-6 draft instruction with:**

> Use `research/skill-draft.md` only for the family/ladder teaching structure. Rewrite examples and syntax to match the final schema and CC-5 contract. Do not copy its reserved `phase`, `control`, `role: control`, `settings.loras`, `${holes}` syntax, or any unsupported settings into the skill. Explain still holds using CC-8's one-or-four-frame chunk rule. The skill's commands and examples must be exercised by the CC-5/CC-6 cold-read case.

**K. Add a cost table in `66/plan.md` and define estimate unit:**

> Estimates are person-days of implementation and review, excluding the owner's later live test and predecessor plans. Allocate the 8-day core and 5.5-day continuation phase across task IDs, including CC-8 and CC-9. Plan 64 and Plan 65 estimates are additional 2.5 and 2 person-days; the combined planned effort through Plan 66 is 18 person-days before owner live evaluation. Re-estimate if the card-level allocations exceed the phase totals.

Adjust those figures if task owners' estimates do not support them; current text only makes the phase addition sum to 13.5, not the underlying estimate.

## Executor verdict

A neutral engineer can explain the architecture and can start foundational work after the owner supplies release-base/merge SHAs and scope authorization. They cannot execute Plans 64–66 safely to the intended end state from the files exactly as written: source-free image admission, paired soundtrack limits, CC-1 mixed-case proof, capability-table evolution, and stale research recommendations can produce divergent behavior. Fix P0 items before dispatch; P1 fixes prevent costly rework; P2 improves handoff quality. All checks cited above are planned acceptance criteria only; this review ran no tests.
