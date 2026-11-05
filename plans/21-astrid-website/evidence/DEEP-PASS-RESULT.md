The sandbox blocked writing `DEEP-PASS-RESULT.md`. The full result follows.

# Deep pass result — 20 October 2026

Audited checkout: `17e46de99b7cef52fe494de1703a9865a8d4be24`. Read the guide, brief and both full-page mockups. Three parallel Luna agents gathered evidence; I checked the consequential findings against source. No app, build or tests were run.

**The journey is buildable, but “only their order changes” is wrong.** Round 4 changes the snapshot dependencies, plate assets, conversation continuity and transition choreography. Several prerequisite fixes have already landed.

Citation prefixes below expand relative to the root of the astrid-app checkout at `17e46de99`:

- `H/` = `src/pages/Home/`
- `V/` = `src/tools/video-editor/`
- `C/` = `src/shared/components/conversation/`

“Absent” means proposed work has not landed, rather than an existing implementation having been deleted. `F1`–`F19` refer to the guide’s §1 rows in their original order.

## A. Is the guide still true?

### W1 — scrolling and page structure

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F3:** `Shell.css:29,33`: `100vh`, `overflow: clip` | **Still present; diagnosis overstated.** Both declarations remain. The page also contains only the hero grid; changing overflow alone does not create a journey. Add real section height and scope clipping deliberately. `H/PublicAstridShell.css:28`, `H/PublicAstridShell.tsx:721`. |
| **F4:** sticky works and no ancestor breaks it | **Unverified for the proposed structure.** There is no journey sticky stage to inspect. Audit the actual resulting ancestors, including body overflow and the retained-page wrapper. `src/index.css:345`, `src/index.css:350`, `H/PublicAstridSite.css:14`. |
| Showcase row at CSS `:298` | **Still true:** `clamp(520px, calc(100svh - 40px), 680px)`. Its 520 px minimum needs an override in short viewports and the phone stage. `H/PublicAstridShell.css:295`. |
| Move the grid’s View Transition name | **Still needed.** The snapshot name remains on `.astrid-landing-grid`. Do not let it encompass the entire new scrolling journey. `H/PublicAstridSite.css:42`. |
| Callout scroll listeners `:915–916`; mount `Shell:890` | **Line drift; behavior remains.** Window/capture scroll and transition listeners are now around `H/PublicAstridCallouts.tsx:908`; mount remains gated by editor reveal and `visualActive`, not journey section. `H/PublicAstridShell.tsx:890`. |
| Quiet-field geometry and raster work | **Still relevant, but painting is already coalesced.** Geometry observes scroll; raster invalidation schedules rAF rather than painting synchronously on every event. No hero-section gate exists. `H/publicAstridSkyGeometry.ts:166`, `H/PublicAstridSky.tsx:78`, `H/PublicAstridSky.tsx:95`. |
| Layout-glide selectors `:9–16` | **Still hero-specific.** They target the landing grid/showcase and must be scoped when those wrappers change. `H/usePublicAstridLayoutGlide.ts:3`, `H/PublicAstridShell.tsx:265`. |
| Drift saturates at 1400 px | **Still true.** Keep parallax drift separate from the new time-of-day progression. `H/publicAstridSkySession.ts:35`, `H/publicAstridSkySession.ts:168`. |
| Vision round-trip test `:179–208` | **Existing coverage, not journey proof.** Site saves/restores scroll; the lifecycle test checks a mocked 427 px position and retained editor identity. `H/PublicAstridSite.tsx:39`, `H/PublicAstridSite.tsx:59`, `H/PublicAstridSite.lifecycle.test.tsx:176`. |

### W2 — arrangements

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F2:** four absolute surfaces, 720 ms App/Agent move | **Still true.** Geometry/transition declarations remain at `H/PublicAstridShell.css:415`; timing is 720 ms at `H/publicAstridMotion.ts:43`. |
| Add `data-journey` at shell `:680` and stage `:781` | **Absent/proposed.** Current attributes describe audience, theme, lifecycle and readiness. `H/PublicAstridShell.tsx:672`, `H/PublicAstridShell.tsx:770`. |
| Audience cascade, tilt and stagger pointers | **Still applicable.** Audience geometry remains around CSS `:863`, `:883`, `:1079`; assembly transforms around `:891`, `:1106`; stagger variables at `:993`. Pointer tilt is now written at `H/PublicAstridCallouts.tsx:458`. |
| `sameExperience`, `routeMotionTiming` | **Still audience-only.** Same-audience routes stop the existing motion clock. Either add an explicit journey pose to the motion contract or give journey motion its own controller. `H/PublicAstridShell.tsx:154`, `H/publicAstridMotion.ts:5`, `H/publicAstridMotion.ts:35`. |
| `useInactiveSurface` calls | **Still audience-based.** The helper manages `inert`; calls must incorporate journey visibility. `H/PublicAstridShell.tsx:108`, `H/PublicAstridShell.tsx:282`. Also update surface `aria-hidden`, currently audience-based in `H/PublicAstridMountedEditor.tsx:120`, `:150`. |
| Conversation loading at MountedEditor `:94–95` | **Guide incomplete.** It starts requested for Agent and is retained once requested; App also preloads after editor reveal. `H/PublicAstridMountedEditor.tsx:94`, `H/PublicAstridShell.tsx:810`. Journey still needs explicit presentation/visibility control. |
| Reduced-motion blocks | **Still present, only covering existing arrangements.** `H/PublicAstridShell.css:1715`, `:1757`, `:1793`. |
| W2 done condition: hero → editing | **Wrong for round 4.** Replace with hero → extend; editing is now the last live-editor arrangement. |

### W3 — activation and director

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| Vision IO pattern `:265–283` | **Still usable for reveal, not sufficient by itself for arbitrary scroll jumps.** `H/PublicAstridVision.tsx:261`. The journey needs an explicit section-position reconciliation on initial load, hash navigation and large jumps. |
| **F14:** `scriptedReplayReducer` | **Still available, but strongly fixture-specific.** Duration/cues are constants; actions and generation checking exist; integer-only ticks remain. `H/replay/scriptedReplay.ts:1`, `:47`, `:83`, `:106`. No section or finish action exists. |
| Extend the reducer | **Reasonable pattern, not a requirement to reuse its types.** Its presentation type hardcodes cue IDs and unavailable-result semantics. A small journey reducer avoids contaminating the hero fixture. `H/replay/scriptedReplay.ts:17`, `:56`, `:124`. |
| `visualActive`, stale callback generations | **Still valid seams.** `H/PublicAstridShell.tsx:166`, `H/publicAstridSkySession.ts:379`. Navigation also invalidates stale transitions: `H/publicAstridNavigation.ts:27`. |
| New director/section files | **Absent/proposed.** The existing mount remains Site → Shell → MountedEditor. `H/PublicAstridSite.tsx:110`, `H/PublicAstridShell.tsx:810`. |

### W4 — timeline data and editing

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F1:** real editor and Remotion preview | **Still true.** Provider mounts `EditorRuntimeProvider`; parts render `RemotionPreview` and `TimelineEditorCoreBody`. `H/PublicAstridEditorProvider.tsx:39`, `H/PublicAstridEditorParts.tsx:61`, `:80`. |
| **F7 / W4.1:** read-only guard awaiting branch merge | **Changed: present on main.** Home supplies denied editability and the public element host; runtime forwards both. `H/PublicAstridEditorProvider.tsx:13`, `:39`; `V/contexts/EditorRuntimeProvider.tsx:448`; `V/hooks/useTimelineState.ts:759`. |
| Three `enable*Services` flags unimplemented | **Changed: implemented and disabled by Home.** Extensions, process/command services, live services and export are gated. `H/PublicAstridEditorProvider.tsx:50`; `V/contexts/EditorRuntimeProvider.tsx:230`, `:260`, `:448`. Regression specifications remain at `V/contexts/EditorRuntimeProvider.test.tsx:2661`, `:2763`. |
| Browser provider drops effects/services; assembly hardcodes public hooks | **Changed: forwarding exists.** Browser passes effects and installed timeline services; runtime forwards them; assembly’s public hooks are a default. `V/browser/BrowserVideoEditorProvider.tsx:68`, `:228`; `V/contexts/EditorRuntimeProvider.tsx:531`; `V/contexts/editorRuntimeAssembly.tsx:605`. |
| `VideoEditorProvider` missing `astridElementHost` | **Changed: field is present.** `V/contexts/VideoEditorProvider.tsx:1084`. This is source verification, not a fresh typecheck. |
| **F6:** immutable provider and poll adoption | **Still true.** Provider returns cloned fixed data/version 1; poll sync still adopts with `save:false`, `skipHistory:true`. `H/publicAstridExample.tsx:127`; `V/hooks/useTimelineQueries.ts:42`; `V/hooks/usePollSync.ts:354`. |
| W4.2 publisher and QueryClient | **Publisher absent; QueryClient present.** Its owner is `H/PublicAstridEditorProvider.tsx:23`, `:37`. Timeline and registry keys are `V/hooks/useTimeline.ts:12`; optional identity suffixes are added at `V/hooks/useTimelineQueries.ts:49`. Prefix invalidation still matches suffixed keys unless `exact:true` is used. |
| Version rejection and asset allowlist | **Still true, with more adoption gates.** Stale versions, active interactions, unsaved work and canonical drafts can block adoption. The public URL allowlist is captured at construction. `V/hooks/usePollSync.ts:66`, `:112`, `:299`; `H/publicAstridExample.tsx:133`, `:153`. |
| No IndexedDB writes | **Not established by `persistenceEnabled:false`.** Normal saved mutations schedule a local draft before checking that flag. Poll adoption avoids `scheduleSave` because it uses `save:false`. `V/hooks/useTimelineCommit.ts:337`, `:398`; `V/hooks/useTimelinePersistence.ts:973`, `:1028`, `:1040`; `V/data/timelineDraftIndexedDb.ts:13`. |
| **F8 / W4.3:** only three pure commands; editing only store-bound | **Narrow claim true; broad claim wrong.** `MEDIA_COMMAND_DESCRIPTORS` still has add/swap/place. However, pure `compileTimelinePatch` supports move and update; split/slice are reserved and skipped. This compiler already existed at the guide’s baseline. `V/commands/media.ts:737`; `V/lib/timeline-patch.ts:994`, `:1208`, `:1309`. |
| Facade move/trim/split/update; test-local move command | **Still present.** Facade operations are mounted-state/editability-dependent. The test-local descriptor remains test-only. `V/hooks/useTimelineCommandsService.ts:157`, `:604`, `:658`, `:720`, `:794`; `V/lib/timeline-save-utils.test.ts:89`, `:151`. |
| **F9:** speed and crossfade | **Still supported, with actual timing semantics to respect.** Playback rate: `V/compositions/VisualClip.tsx:307`; transition resolution: `:557`; incoming pre-roll: `:640`; opacity renderer: `V/effects/transitions.ts:6`. Built-ins remain available despite Home’s empty effect catalog: `V/transitions/catalog.ts:183`. |
| **F11 / W4.4:** stable clip keys and geometry transitions | **Still true for media clip actions.** Positioned wrappers use stable IDs and numeric left/width. `V/components/TimelineEditor/TrackListRenderer.tsx:294`; inner clip attributes: `V/components/TimelineEditor/ClipAction.tsx:555`; selectors: `V/lib/timeline-dom.ts:17`, `:140`. |
| Playback-rate remount / pause preview | **Still relevant.** Video key includes playback rate. Current public playback coordinator pauses only when inactive. `V/compositions/ReadinessVideo.tsx:15`; `H/PublicAstridEditorParts.tsx:102`. |

### W5 — conversation spine

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F15:** shared conversation presentation | **Still true.** Hero uses it at `H/PublicAstridScriptedConversation.tsx:106`. Items, pending state, scroll refs and bottom anchor remain available at `C/ConversationPresentation.tsx:14`. |
| `column-reverse` | **Still host CSS, not a shared-component requirement.** `H/PublicAstridShell.css:732`; shared content layout is at `C/ConversationPresentation.tsx:85`. Use normal chronological flow for the journey. |
| Duplicate assistant messages | **Still suppressed when the preceding item is a matching message.** Tool groups interrupt that adjacency. `C/contracts.ts:58`, `:68`. Do not loosen global deduplication just for this page. |
| Tool/result cards need a new item kind | **Overstated.** `tool_group` already exists and is rendered. A compact journey presentation is still needed to place chips directly under replies. `C/contracts.ts:31`; `C/ConversationPresentation.tsx:86`. |
| Pending and entrance animation | **Available primitives, new composition required.** `hasPendingWork` renders Thinking; `astrid-rise` remains. `C/ConversationPresentation.tsx:103`; `H/PublicAstridShell.css:1898`. |
| Carry hero’s first request forward | **Copy needs updating against the actual fixture.** The real request is longer than the guide’s shortened quotation, and the response differs. Preserve it or deliberately write a new journey handoff. `H/content/light-study-v1/authored-script.ts:7`. |

### W6 — overlays and mink

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F13:** extract measuring loop | **Still useful, but extract narrowly.** Target resolution now starts at `H/PublicAstridCallouts.tsx:349`; read/write queue at `:414`; animation detection at `:830`; observers at `:875`; transition listeners at `:908`. |
| Separate callout layout helper | **Still present.** Preserve existing geometry/choreography utilities rather than moving the entire callout system. `H/PublicAstridCalloutLayout.tsx:3`. |
| Clip anchoring | **Still supported.** Scope the inner `.clip-action[data-clip-id]` selector to the timeline; use outer action slots for geometry. `V/lib/timeline-dom.ts:17`, `:140`; `V/components/TimelineEditor/TrackListRenderer.tsx:294`. |
| **F16:** mink PNG/steps pattern | **Partly true.** Home swaps static poses and has a psychic sprite overlay; Vision uses a sprite strip with `step-end`. The four quoted hex colors are an artwork requirement, not a validated sprite contract. `H/PublicAstridShell.tsx:223`; `H/PublicAstridSky.css:111`; `H/PublicAstridVision.css:73`. |
| Reduced-motion static mink | **Needs deliberate implementation.** Current psychic animation is hidden, not converted to a static frame. `H/PublicAstridSky.css:117`. |
| Beat overlay host | **Still exists and is gated.** `V/components/TimelineEditor/TimelineExtensionOverlayHost.tsx:176`; mount gate at `V/components/TimelineEditor/TimelineCanvas.tsx:1469`; Home disables it at `H/PublicAstridEditorProvider.tsx:53`. A small journey-owned layer is simpler. |

### W7 — editing, now §4

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F12:** `setScaleWidth` is a no-op | **Wrong for the mounted public editor.** The initial fallback is still a no-op, but real state wires the preference setter. `V/hooks/timelineStore.ts:404`; `V/hooks/useTimelineState.ts:575`, `:583`, `:770`, `:1263`; `V/hooks/useEditorPreferences.ts:88`. |
| Scale formula and fit | **Formula valid; blanket fallback unnecessary.** Scale is 5, default width 160, yielding 32 px/s. `V/hooks/useEditorPreferences.ts:30`, `:85`; `V/lib/timeline-scale.ts:87`. Fit must measure the real gutter: desktop 144 px, touch 56 px. `V/lib/coordinate-utils.ts:6`. |
| Fit side effects | **Additional concern.** Preference changes write localStorage after a debounce. UI zoom clamps 40–1000, but the direct setter does not. Save/restore hero zoom and check narrow layouts. `V/settings/useEditorSettings.ts:17`; `V/lib/timeline-scale.ts:13`; `V/hooks/useEditorPreferences.ts:88`. |
| **F10:** audio tracks and browser waveform decoding | **Still true.** `V/types/index.ts:57`; `V/hooks/useWaveformData.ts:29`, `:106`. Music must now exist in §2, not first appear in §4. |
| History and beat-list components | **Still proposed.** Keep these journey presentation data, separate from editor undo history: poll replacement explicitly bypasses normal history. `V/hooks/usePollSync.ts:369`; `V/hooks/useTimelineCommit.ts:357`. |

### W8 — generation, still §3

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| Tray, GPU detector, five-card landing sequence | **Absent/proposed.** Existing Home lazy boundaries cover editor, inspector and conversation. `H/PublicAstridShell.tsx:42`; `H/PublicAstridEditorParts.tsx:18`; `H/PublicAstridMountedEditor.tsx:96`. |
| Media convention | **Still valid.** Existing media declares public URLs, hashes and durations; registry uses `origin:'immutable-public'`. `H/content/light-study-v1/media.ts:9`; `H/content/light-study-v1/timeline.ts:14`. |
| Public-media byte hashing | **Still missing for the proposed journey assets.** Bundle validation checks metadata/hash consistency, not these future files’ bytes. Add a journey-specific digest check. `H/publicAstridExample.tsx:251`. |
| Existing content can supply real generation evidence | **False.** The fixture explicitly forbids claiming live generation/named tool invocation; provider binding is unbound and verified output unavailable. `H/content/light-study-v1/authored-script.ts:9`; `provider-binding.ts:5`; `verified-result.ts:5`; `provenance.ts:28`. |
| Readouts based on a real run | **Still required.** Add a separate journey provenance contract; do not relabel the existing placeholder fixture as generated evidence. |

### W9 — extendable suite, now §2

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F17:** Three.js is not a dependency | **Changed: already installed.** `three`, `@react-three/fiber` and `@remotion/three` are listed at `package.json:162`. No package addition is needed. |
| Surfaces flatten/risk live 3D | **Still a valid architectural concern.** Existing surfaces combine overflow clipping and 3D transforms. Use separate plates rather than nesting the real editor into the exploded stack. `H/PublicAstridShell.css:415`. |
| Add `vendor-three` branch at policy `:21` | **Not implemented; optional.** Existing manual chunk policy has no Three branch. Lazy import is required; a dedicated vendor chunk should depend on measured output, not be automatic. `config/vite/policy.ts:19`. |
| Plates and Three scene use §3’s end state | **Wrong after reorder.** Use hero light studies, then the §2 music addition. Canonical hero data is `H/content/light-study-v1/timeline.ts:4`. Lake media must not appear yet. |
| Beat-sync reuses §2 beat list | **Dependency moves earlier.** Music and beat data must be inputs to the extend section and later reused by editing. |
| Backend blocks and tabs | **New journey presentation.** Do not enable installed extension/mutation services merely to show these examples; Home intentionally disables them. `H/PublicAstridEditorProvider.tsx:50`. |

### W10 — sky and finale

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| **F5:** fixed sky and manual hours | **Still true.** Fixed positioning: `H/PublicAstridSky.css:1`; manual hours stop replay/review and patch settings: `H/publicAstridSkySession.ts:511`. |
| Every sky animation rerenders the shell | **Too broad.** Raster, parallax and control subscriptions are separate. However, changed settings/palette still notify controls, so using `setManualHours` for scroll remains wrong. `H/publicAstridSkySession.ts:324`, `:340`, `:580`; `H/PublicAstridSky.tsx:57`. |
| Proposed scroll-hours fast path | **Absent.** Effective hours currently select manual or zoned clock time plus replay offset. Session API has no journey claim/progress method. `H/publicAstridSkySession.ts:192`, `:576`. |
| Palette writing / stale React inline tokens | **Still relevant.** Imperative writes coexist with Shell’s inline palette properties. Keep the controls snapshot consistent with the held palette. `H/publicAstridSkySession.ts:246`; `H/PublicAstridShell.tsx:695`. |
| Formatter caching | **Still applicable, narrowly.** `utcOffsetHours` constructs `Intl.DateTimeFormat`; `zonedHours` depends on it. `H/publicAstridLocation.ts:52`, `:66`. Cache the formatter by zone, not a permanently fixed UTC offset. |
| Solar-noon / solar-midnight target | **Matches ordinary-latitude renderer geometry.** `sunTimes` and `skyState` remain at `H/publicAstridSkyRender.ts:322`, `:366`. Moon twilight constant remains private at `:45`. Polar-day/night branches exist at `:336`; they cannot guarantee a visible opposite body. |
| Dusk and whole-palette holding | **Still relevant.** Threshold/ink logic: `H/publicAstridSkyRender.ts:75`, `:120`. Freeze the readable UI palette, not the sky raster, during a section. |
| Claim/release and Vision ownership | **New journey work around an existing single palette target.** `H/publicAstridSkySession.ts:567`; Vision registers its target at `H/PublicAstridVision.tsx:339`. Preserve the captured journey window across temporary inactivity. |
| Moon phase / silhouette | **Still true.** Session computes date-based phase; renderer draws it. `H/publicAstridSkySession.ts:232`; `H/publicAstridSkyRender.ts:536`. |
| Reveal, link and horizon layer | **Reveal/link reusable; horizon new.** `H/PublicAstridVision.tsx:261`; `H/publicAstridLinks.ts:11`; Home link example `H/PublicAstridShell.tsx:741`. Renderer already has layer caching: `H/publicAstridSkyRenderer.ts:18`. |

### W11 — phone, accessibility and navigation

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| Phone breakpoint 640 px; skip audience View Transitions | **Still true.** `H/publicAstridLifecycle.ts:12`; `H/publicAstridNavigation.ts:63`. |
| 45svh journey stage, flat stack, two-turn spine | **Absent/proposed.** Treat 45svh as a starting layout constraint, not enough room for five full plates. Show compact layers plus the selected example. |
| Inert surfaces and accessibility tests | **Existing primitives; journey coverage absent.** Inert helper: `H/PublicAstridShell.tsx:108`; current accessibility suite: `H/PublicAstridShell.accessibility.test.tsx:107`; audience buttons already have `aria-pressed`: `H/PublicAstridShell.tsx:750`. |
| Same-page hash interaction | **Still needs handling.** Site popstate dispatches by pathname; standalone Shell also synchronizes experience on popstate. Avoid treating a section hash as a room transition. `H/PublicAstridSite.tsx:68`; `H/PublicAstridShell.tsx:608`. |
| Vision URL/hash restoration | **Existing foundation.** Opening Vision saves the complete Home URL; back uses browser history or the stored URL. `H/PublicAstridSite.tsx:78`, `:85`. |
| **F18:** `/art` is public | **Still false.** It is in app routing; unauthenticated behavior depends on the app-entry preference. Keep it out of the finale. `src/app/routes.tsx:174`; `src/app/Layout.tsx:98`; `src/app/entryClassification.ts:9`. |

### W12 — tests, performance and build

| Guide claim or pointer | Verdict and current pointer |
|---|---|
| Unit scaffolds | **Still usable.** Manual rAF: `H/PublicAstridCallouts.scheduling.test.tsx:59`; fake timers: `H/PublicAstridSite.lifecycle.test.tsx:98`; motion listener fixture: `H/PublicAstridShell.accessibility.test.tsx:79`. |
| jsdom and inert IO setup | **Still true.** `config/testing/vitest.config.ts:86`; `src/test/setup.ts:10`. Journey tests must drive their own IO/scroll model. |
| Existing integrated E2E / new journey spec | **Existing spec useful; journey spec absent.** Reduced-motion examples: `tests/e2e/public-astrid-integrated.spec.ts:152`. Default matching will collect a new journey spec: `playwright.config.ts:92`. |
| Desktop/iPad/iPhone coverage | **Still configured.** `playwright.config.ts:159`. These are Chromium device projects, not proof of Safari behavior. Add a WebKit check for the plate handoff/sticky layout. |
| Test server setup | **More involved now.** Playwright owns both Vite and a fake Runtime server; it does not reuse an existing server. `playwright.config.ts:114`, `:147`. |
| **F19:** dynamic imports excluded from budget | **Still true.** Budget walks static `chunk.imports`, not dynamic imports. That is not a license for unlimited deferred downloads. `config/vite/bundleBudget.ts:39`, `:62`. |
| Vite/build pointers | **Files remain, but prerequisites matter.** Build requires selected or bundled Astrid source and a valid tool catalog. `config/vite/vite.config.ts:62`; `config/vite/astridSource.ts:67`, `:132`. Budget plugin/manual chunks remain wired at `config/vite/vite.config.ts:167`, `:208`. |
| CI runs the new default E2E spec | **Supported by current wiring.** Workflow invokes `make slot-first-audit`, which reaches default Playwright. `.github/workflows/slot-first-quality.yml:27`; `Makefile:99`; `package.json:55`. |
| Bundle size, 60 fps, preview availability | **Unverified.** No build/profile/deployment was performed. Railway serving scripts exist, but source alone does not establish current branch deployment policy or available preview environments. `package.json:29`. |

### Appendix coverage not otherwise called out

All production files named in the appendix still exist; no wholesale path migration is required for this work.

| Appendix area | Current pointer / qualification |
|---|---|
| Editor readiness | `H/publicAstridReadiness.ts:1`: attempt-safe loading/presentation state machine. Reuse readiness for the plate-to-live handoff. |
| Sample package assembly | `H/content/light-study-v1/public-example.ts:11`, `:36`: maps authored script and assembles immutable bundle. |
| Sample timeline/media | `H/content/light-study-v1/timeline.ts:4`, `:14`; `media.ts:11`: three clips, 28 seconds, immutable assets. |
| Share and links | `H/publicAstridShare.ts:19`; `H/publicAstridLinks.ts:3`: current repository link is `banodoco/astrid-app`. |
| Public bootstrap | `src/app/publicBootstrap.tsx:6`; classification at `src/app/entryClassification.ts:25`. Public entry mounts Site directly. |
| Build port | `config/vite/policy.ts:1`: default remains 2222. |
| New journey files in guide §2.4 | Proposed, not renamed or deleted implementations. Preserve this separation from the large Shell/Callouts files. |

## B. Guide §7 open items

| Item | Status on today’s main |
|---|---|
| Read-only guard | **Implemented in source.** Host and editability are forwarded. The vanished branch is irrelevant to implementation status. Browser drag/trim behavior was not rerun. See W4. |
| Browse-only flags | **Implemented.** Home disables all three. This does not mean “no local state or storage activity anywhere”: editor preferences still use localStorage. `V/settings/useEditorSettings.ts:17`. |
| Installed browser effects/services/host | **Forwarding is present.** The old missing-field issue is no longer visible in source. Fresh typecheck remains unperformed. |
| Public editor store and zoom | **Normal mounted store with working preference setter.** The fallback no-op is not the active path. Use measured touch/desktop gutters; preserve hero zoom. |
| Publish + invalidate | **Mechanism remains viable; publisher absent; runtime proof outstanding.** Do the spike before relying on it. |
| Pure move/trim/split/update | **Move/update available through the pure patch compiler.** Trim can be represented as timing-field updates; there is no equivalent dedicated pure trim command in the media registry. Split/slice are reserved no-ops in the patch compiler. |
| Sky raster cost | **Unknown.** Existing dirty-layer/rAF machinery helps, but no profile establishes the cost of the proposed progression. |
| Bundle budget | **Unknown actual size.** Current gate exists; no build was run. |
| Tall-page Vision restoration | **Not proven.** Existing lifecycle coverage is useful but insufficient for the new document height and transition snapshots. |

**Recommended publisher contract**

Create one journey session per mounted public editor, not a mutable module-global singleton.

- Preserve the immutable hero example and its evidence metadata.
- Give the journey provider a fixed registry containing all approved journey asset URLs. Adding metadata early need not mean fetching all media early.
- Keep one stable provider and QueryClient. Publish a copied config with a strictly increasing version.
- Invalidate through the timeline key helper; expose an acknowledgment when that version is adopted.
- Give replayed older content a **new higher version**. Never restore its old version number.
- Coalesce skipped steps to the final required snapshot; invalidate stale callbacks and outstanding handoffs.

This avoids changing the captured asset allowlist and racing separate registry updates. The loader reads config and registry together; adoption then rechecks state before its deferred commit. `V/lib/timeline-data.ts:585`; `V/hooks/usePollSync.ts:332`.

The spike must publish three visibly different snapshots, then replay the first with a higher version. Assert adoption, unchanged editor instance, no history entries, zero `saveTimeline` calls and zero writes to `astrid.timeline-drafts`. The distinction matters because ordinary saves write the draft before checking persistence enablement. `V/hooks/useTimelinePersistence.ts:973`, `:1028`.

## C. Engineering consequences of round 4

The mockups establish composition and tone. They do not establish consistent timeline content: notably, the day §2 stack already shows lake imagery. Rebuild those plates from the actual hero data.

### State lineage

Use explicit section projections:

| Projection | Timeline and presentation state |
|---|---|
| Hero | Existing three light studies on `V1`; existing hero contract. |
| §2 end | Hero light studies + music on `A1`; beat-sync artifact and model-setup demonstration completed. No lake clips. |
| §3 end | §2 state + five lake clips on `V2`, “Lake at dawn”. |
| §4 end | §3 state with edits to `V1` and music level; lake source clips preserved unchanged. |
| Finale | Same completed data retained; editor presentation inactive. |

The current `V1` IDs and source bounds are concrete: 8/12/8 seconds. `H/content/light-study-v1/timeline.ts:4`.

### Hero → §2: one continuous live-to-plate move

Recommended sequence:

1. Freeze pointer tilt and pause preview playback; retain the hero’s transport/zoom state.
2. Measure visible surfaces in one read phase.
3. Place matching plate wrappers over those surfaces, copying their transform hierarchy and transform origins.
4. Crossfade live surfaces to plates **before** separating them.
5. Animate plates into the exploded stack; introduce the backend plate and inactive layers.
6. Reveal the example panel and agent tag after the stack settles.

A transformed `getBoundingClientRect()` is only an axis-aligned bounding box. Using it alone to recreate tilted panels will produce a jump. The spike must demonstrate matching corner positions, not just matching bounding boxes. Current transforms span stage, assembly and pointer-tilt wrappers. `H/PublicAstridShell.css:302`, `:408`; `H/PublicAstridCallouts.tsx:458`.

Build-time screenshots cannot exactly match an arbitrary live preview frame. Make the content crossfade intentional, short and geometrically aligned; do not promise an instantaneous pixel-identical substitution.

**Plate contents:** light-study preview poster, actual inspector/panels, light-study timeline, current hero conversation, and backend capabilities. Add music while the plate representation covers the live editor. Use separate light/dark captures where baked UI colors require them.

**Simpler:** no generation-result continuity is needed in the first stack.

**Harder:** this is now the first major transition, so it must work from App, Agent, interrupted audience motion and incomplete editor readiness.

### §2’s demonstrations

- The Three.js view derives from the hero timeline plus the §2 music addition. Use light-study thumbnails and a waveform representation for audio.
- Display the actual scene source module in the code panel; avoid a decorative snippet unrelated to the rendered view.
- Beat-sync’s card uses the same music digest and beat list later used by §4.
- Model setup ends with the LTX-ready exchange required by the brief.
- Keep tab selection separate from completion state. Selecting the 3D tab must not erase the completed beat-sync setup.

Three is already installed. Lazy-load the scene, render only while active, cap pixel ratio and dispose resources. `package.json:162`.

### §2 → §3: plates return to live surfaces

Flatten/converge the timeline plate onto the real generation-strip rectangle. Behind it:

- adopt the §2-end snapshot;
- set the generation arrangement and fit;
- wait for editor readiness/adoption;
- crossfade the plate to the live timeline;
- reveal the generation tray.

Do not unmount/remount the editor to accomplish this. Its provider currently owns the QueryClient and mounted parts together. `H/PublicAstridMountedEditor.tsx:115`.

The backend plate can fade into the setup readouts. The retained spine ends with:

> Run LTX-Video locally on my GPU.  
> LTX-Video is ready on your GPU.

No editing/retime carry-over belongs here.

### §3: generated media and honest readouts

Preserve the still → vertical → animation → landing progression. Animate explicit card dimensions, then transfer each card to its live timeline target.

Publish each landing only after its asset is available in the approved registry. A skipped section can publish the complete five-clip endpoint once.

Separate:

- **visitor capability:** optional local GPU description;
- **recorded run facts:** actual runner, model, tool and elapsed time;
- **scripted presentation:** compressed demonstration timing.

A visitor GPU heading above checkmarked recorded timings is otherwise easy to misread as execution on that visitor’s hardware. Keep a small “Recorded example” label and identify the actual run machine beside the measured facts.

### §3 → §4: grow the live timeline

This transition becomes simpler: the timeline is already live. Expand its container, refit it, reveal History and switch the spine into editing.

**Recommended edit scope: the three light studies and music only.** It preserves the brief’s “3 clips” and “3 downbeats” copy and reuses existing assets. Editing all five lake clips as well adds choreography and contradicts the stated counts.

Retain `V2` as a clearly labeled source track. Current schema supports `role:'source'`; the renderer excludes source tracks from output while retaining authored state. `V/types/index.ts:77`; `V/data/timelineOutputProjection.ts:115`; `V/compositions/TimelineRenderer.tsx:1580`.

This also prevents lake imagery from obscuring the light-study retiming demonstration. Every §4 snapshot should assert unchanged lake clip IDs, timings and assets.

**Retiming needs authored arithmetic.** For example, starting from the 8/12/8 cut:

- middle at 8, source `0…8.4`, speed `0.6` → 14 seconds;
- final at 22, source `2…8` → 6 seconds;
- total remains 28 seconds.

That visibly lengthens the middle while preserving the final source ending. Treat this as a feasible example, then validate against the selected beat sequence. Duration applies speed once; the incoming transition already adds pre-roll, so do not also manually subtract 1.5 seconds from `at`. `V/lib/config-utils.ts:98`; `V/compositions/VisualClip.tsx:640`.

### Repeated agent-action UI

Use one shared visual vocabulary, with separate semantic variants:

| Section | Exact additions |
|---|---|
| §2 | “built by your agent” on Three/beat-sync; preserve “installed by your agent” for model setup. Highlight **Panels**, **Agent**, or **Runtime** with text and a filled dot. |
| §3 | “set up by your agent” below both applicable readout titles. |
| §4 | `arrange · 3 clips`; `beat-sync · 3 downbeats`; `retime · crossfade`. Beat-sync gets the stronger fill. Earlier reply/chip pairs fade together. |

Keep these as DOM text. Existing tool groups can supply structure, but their current renderer does not provide the requested compact reply attachment directly. `C/ConversationPresentation.tsx:86`.

Use the brief’s exact headline/subtitle pairs:

- **A creative suite your agent can extend.**  
  Any view, tool or model, from the canvas down to the runtime.
- **Open models, without the setup pain.**  
  Your agent installs and runs them, on your machine or in the cloud.
- **A creative partner with deep tools.**  
  It edits beside you, with tools you build and workflows the community shares.

### Director and sky consequences

Order must be explicit: `hero → extend → generate → edit → vision`; never infer it from old section numbering.

- First entry plays; completed upward entry shows that section’s endpoint.
- Backtracking must restore the section’s own projection: §2 must not retain visible lake clips from §3.
- Replay resets only the active section’s presentation and publishes its base with a new version.
- Adjacent early departure may compress presentation into the handoff; the next demo starts only after the required endpoint is adopted.
- A large jump commits skipped endpoints logically in order but can coalesce rendering to the final destination.
- Hidden-tab time must not accumulate into a giant tick on resume.
- Reduced motion shows endpoints immediately; manual tabs remain usable.

The sky still runs from the first post-hero section to the finale. Reordering changes the progress anchors, not the astronomical target. Capture the window once per journey visit; preserve it through Vision and tab hiding.

Use the same ownership mechanism for continuous desktop progression and stepped phone/reduced-motion progression. “Do not claim on phones, but step through the same claimed API” is internally inconsistent.

Keep manual sky controls authoritative. Hold the UI palette per section, and handle twilight and polar cases explicitly. The renderer has genuine polar branches where the opposite body may never appear. `H/publicAstridSkyRender.ts:336`.

## D. Ranked risks and spikes

| Rank | Risk / why difficult | First spike | Pass condition |
|---|---|---|---|
| 1 | Snapshot adoption, replay and draft side effects | Three snapshots plus replay through the real public provider | All versions adopted in order; same editor instance; no persistence/draft/history writes; stale publication cannot win. |
| 2 | Hero → plates → live continuity | One player and timeline transfer from both audiences | No corner jump, blank frame or double surface at desktop/phone; interruption reverses cleanly; WebKit checked. |
| 3 | Mobile live timeline fit and usable stage | Real `V1+A1+V2` at 390 and 320 px | Whole authored range visible; readable key labels/chips; overlay alignment correct; no document horizontal overflow. Touch gutter is 56 px, not 144. `V/lib/coordinate-utils.ts:6`. |
| 4 | Sky ownership and palette consistency | Scrub through dusk, open Vision, return | No React commit per scroll frame; no stale inline palette; same captured window restored; contrast survives boundaries. |
| 5 | First-section Three load cost | Lazy scene using three hero clips | No Three request at initial hero load; usable fallback; resource count does not grow across repeated entry; phone frame rate acceptable. |
| 6 | Generation evidence becomes a schedule blocker | Produce one complete Flux → vertical → Wan sample early | Original outputs, prompts, model/tool versions, hardware and timing receipts correspond to displayed facts. |
| 7 | Fixture/evidence contracts accidentally falsified | Introduce separate journey content bundle | Hero remains labeled according to its existing provenance; new readouts reference actual journey receipts. Existing restrictions: `H/content/light-study-v1/authored-script.ts:9`. |
| 8 | Build prerequisites and source provenance | Validate selected Astrid source/catalog in a writable build environment | Production build and default public E2E boot from a fresh checkout without undocumented local paths. `config/vite/vite.config.ts:62`. |

The guide is wrong or over-built where it asks to reimplement landed guards, add an installed dependency, assumes zoom cannot work, excludes existing pure patch operations, or treats the reorder as CSS alone.

## E. Task breakdown

Each row is intended for one agent session. New paths are proposals.

Additional prefixes:

- `J/` = `src/pages/Home/journey/`
- `L/` = `src/pages/Home/content/light-study-v1/`
- `P/` = `public/astrid/journey/`
- `E2E` = `tests/e2e/public-astrid-journey.spec.ts`

Visual checks:

- **D:** 1586×992, light and dark.
- **P:** 390×844, light and dark.
- **N:** 320×693.
- **S:** 1440×700.
- **RM:** reduced motion at D and P.

Tiers follow the requested assignment: NORMAL/Luna; XHARD/Sol xhigh; TASTE-HIGH/Opus; TASTE-LOW/Sonnet; ASSET/generation or capture.

### Spikes first

| ID / tier | Goal and files | Dependencies | Done when |
|---|---|---|---|
| S1 — XHARD | Prove publication/adoption without writes. `J/publication-spike.*`, provider test, E2E fixture. | — | Three states and higher-version replay adopted; no saves/drafts/history; instance stable. |
| S2 — XHARD | Prove transformed live/plate transfer. `J/SurfaceTransferSpike.*`, temporary captured plates. | — | App/Agent forward, reverse and interrupted handoffs pass corner-alignment checks at D/P and WebKit. |
| S3 — XHARD | Prove real timeline fit and retime. `J/TimelineFitSpike.*`, snapshot fixture. | S1 | `V1+A1+V2` fits D/P/N/S; crossfade frames correct; no doubled overlap; zoom restored. |
| S4 — XHARD | Prove sky progression/ownership. Session spike and unit test. | — | D/P/RM, midnight, twilight and Vision return pass; controls notifications occur only at intended boundaries. |
| S5 — XHARD | Prove lazy Three scene and cleanup. `J/structure-view-spike.*`. | — | D/P fallback works; no initial hero load; repeated entry leaves no growing canvas/resource count. |

### Assets and content

| ID / tier | Goal and files | Dependencies | Done when |
|---|---|---|---|
| A1 — ASSET | Produce 28-second music, beat list and receipt. `P/music.*`, `L/journey-audio.json`. | — | Digest, duration and beat positions verified; waveform legible at P. |
| A2 — ASSET | Generate five Flux landscape stills with run evidence. `P/lake-*-16x9.webp`, evidence manifest. | — | Five actual outputs and complete receipts; contact sheet passes D/P review. |
| A3 — ASSET | Produce five vertical variants with provenance. `P/lake-*-9x16.webp`, manifest. | A2 | Composition retained; no stretched crops; D/P card crops approved. |
| A4 — ASSET | Generate five Wan clips and posters. `P/lake-*.mp4`, posters, evidence manifest. | A3 | Durations/codecs/digests verified; phone playback and poster fallback checked at P. |
| A5 — ASSET | Produce needed mink strips and source grids. `public/astrid-journey/`. | — | Palette/density/alpha/frame bounds verified; clear at intended D/P sizes; static RM frames selected. |
| T1 — NORMAL | Define scripts, copy, endpoint snapshots and evidence references. `L/journey-script.ts`, `journey-snapshots.ts`, `journey-media.ts`. | A1–A4, S1 | Every snapshot validates; endpoints follow new order; §4 preserves all lake clips; no invented run facts. |
| A6 — ASSET | Capture real hero/§2 plates and Three fallback. `P/plates/`, capture fixture/script. | T1, S2, S5 | Light/dark plates contain no lake media; geometry/crops approved at D/P. |
| A7 — ASSET | Produce quiet horizon strip if selected. `P/horizon.*`. | — | No visible seam at D/P/N; acceptable in both palettes. |

### Runtime foundation

| ID / tier | Goal and files | Dependencies | Done when |
|---|---|---|---|
| T2 — XHARD | Implement session-owned publisher and adoption bridge. `J/publicAstridJourneyData.ts`, `H/PublicAstridEditorProvider.tsx`, `H/PublicAstridMountedEditor.tsx`. | S1, T1 | Publication/replay/race tests pass; one provider instance; hero bundle stays immutable. |
| T3 — XHARD | Implement pure director, completion projections and clock. `J/publicAstridDirector.ts`, `usePublicAstridDirector.ts`, tests. | T1, T2 | Enter/leave/skip/up/replay/hidden/RM rules pass; no stale callback changes the current section. |
| T4 — XHARD | Add section activation and deep-jump reconciliation. `J/publicAstridJourneySections.ts`, tests. | T3 | Initial `#edit`, fast scrollbar jumps and boundary oscillation select the correct section without flicker. |
| T5 — XHARD | Mount one sticky stage alongside flow sections. `J/PublicAstridJourney.tsx`, `H/PublicAstridSite.tsx`, Shell mount points, Site CSS. | S2, T4 | One editor; no doubled scroll height; sticky ends before finale; D/P/N/S geometry assertions pass. |
| T6 — TASTE-HIGH | Compose section layouts and exact headline typography. `J/PublicAstridJourney.css`, section wrappers. | T5 | Named “section composition” review passes D/P/N/S; no title/spine collision; P stage remains usable. |
| T7 — XHARD | Implement measured plate handoff and cancellation. `J/useSurfaceTransfer.ts`, transfer tests. | S2, T5, A6 | Both audience routes and resize/interruption checks pass at D/P; hidden surfaces are inert. |
| T8 — TASTE-HIGH | Choreograph hero → exploded stack. `J/PublicAstridExplodedStack.tsx`, transfer CSS. | T6, T7 | Named “first pull-apart” review passes D/P/RM; no disconnected fade-to-new-scene feeling. |
| T9 — XHARD | Add fit controller and restore hero zoom. `J/useJourneyTimelineFit.ts`, narrow editor seam if S3 requires it. | S3, T2, T5 | D/P/N fits use actual gutter; resize stable; no CSS lane scaling; hero zoom restored. |
| T10 — XHARD | Extract minimal anchored overlay scheduler. `J/useAnchoredOverlay.ts`, targeted Callouts extraction. | S2, T5 | Clip/cursor targets stay within 2 px during movement at D/P; loop idles when inactive. |

### Section implementations

| ID / tier | Goal and files | Dependencies | Done when |
|---|---|---|---|
| T11 — NORMAL | Implement chronological spine and compact call attachments. `J/PublicAstridJourneySpine.tsx`, narrow shared render slot if needed. | T1, T3 | Carry-over text exact; pending state/chip association correct; replay creates no duplicate turns. |
| T12 — TASTE-LOW | Style action tags, chips, highlights and fading. `J/JourneyAgentAction.*`, spine CSS. | T11, T6 | Named “agent-action device” review passes D/P/N; readable contrast and text-plus-dot state. |
| T13 — NORMAL | Implement functional Three scene from snapshot data. `J/structure-view.ts`, `PublicAstridStructureView.tsx`. | S5, T1, T8 | Plane IDs/timing match snapshot; displayed source is actual module; cleanup/fallback tests; D/P/RM inspection. |
| T14 — NORMAL | Implement beat-sync/model example states and tab behavior. `J/extendExamples.ts`, `PublicAstridExtendExamples.tsx`. | T3, T8, A1, T12 | Tab selection independent of completion; leave produces canonical LTX-ready handoff; keyboard/RM tests pass. |
| T15 — TASTE-LOW | Compose §2 example cards and flat phone layers. Extend components/CSS. | T13, T14 | Named “extend examples” review passes D/P/N; selected layer and agent tag remain legible. |
| T16 — NORMAL | Implement GPU capability parser and factual readout model. `J/detectVisitorGpu.ts`, `journeyReadouts.ts`, tests. | T1 | Fixture tests cover unavailable/sanitized hardware; no visitor VRAM; recorded and visitor facts separated; no logging/network telemetry. |
| T17 — NORMAL | Implement generation tray states/media lifecycle. `J/PublicAstridGenerationTray.tsx`, media controller. | T1, T3, T16, A2–A4 | Five cards follow script; offscreen videos stop; failed video keeps poster; landing IDs match snapshots. |
| T18 — TASTE-HIGH | Choreograph plates → generation and card landings. Transfer/tray CSS. | T7, T9, T15, T17 | Named “reassembly and landing” review passes D/P/RM; no duplicate/missing landing clip. |
| T19 — NORMAL | Implement edit cues, display History and mink/cursor states. `J/PublicAstridJourneyHistory.tsx`, `PublicAstridJourneyMink.tsx`, edit cues. | T1, T3, T10–T12, A5 | Each History entry corresponds to its snapshot; beat chip uses A1 artifact; lake data unchanged. |
| T20 — TASTE-HIGH | Choreograph generation → editing and three edit beats. Editing CSS/cue timings. | T9, T18, T19 | Named “editing payoff” review passes D/P/N/RM; trim/gap/beat/retime changes are visually understandable. |

### Sky, navigation and delivery

| ID / tier | Goal and files | Dependencies | Done when |
|---|---|---|---|
| T21 — XHARD | Implement sky ownership, progress and held palette. Sky session/geometry modules, `J/useJourneySky.ts`. | S4, T4, T5 | Clock/palette/claim tests pass; quiet-field work stops outside hero; phone stepping and Vision return are deterministic. |
| T22 — TASTE-LOW | Build finale and subtle horizon treatment. `J/PublicAstridJourneyFinale.tsx`, CSS. | T6, T21, A7 if used | Named “opposite-peak finale” review passes D/P/RM; one Vision link; no art link. |
| T23 — XHARD | Finish navigation, retained lifecycle and hash restoration. Site/navigation modules, lifecycle tests. | T4, T5, T22 | Repeated Vision/back restores exact scroll/hash/section; hidden work stops; same-page hashes do not launch room transitions. |
| T24 — NORMAL | Complete semantic structure and keyboard behavior. Section/spine/tab components, accessibility tests. | T11, T14, T17, T19, T22, T23 | Heading order, labelled sections, tab keys, Replay focus and hidden-surface inertness verified; P and RM reading order checked. |
| T25 — TASTE-HIGH | Final desktop/phone motion and type review. Journey CSS and cue timings. | T8, T12, T15, T18, T20, T22, T24 | Named “full journey” review passes D/P/N/S/RM, both hero audiences and both palettes. |
| T26 — XHARD | Add integration E2E matrix and race coverage. E2E, focused lifecycle tests. | T25, T23 | Default three projects pass; forward/skip/back/replay/Vision paths deterministic; WebKit handoff check passes. |
| T27 — XHARD | Profile, verify lazy loading and run production checks. Build config only if measured need; performance evidence. | T26 | Budget passes; no Three at initial hero; no inactive video/overlay loops; measured frame-time report at D/P. |
| T28 — NORMAL | Prepare private preview and release gate. Deployment configuration, flag wiring, release evidence. | T27 | Reviewable private URL, rollback path and flag behavior verified; unflagged hero regression check passes D/P. |

Do not make “no test failures” the only done condition for a TASTE task. Keep the named visual reviews as explicit acceptance checks.

## F. Assets and how to obtain them

| Asset | Tool and production route | Required evidence |
|---|---|---|
| Music + beats | Original procedural audio, or licensed music. Use Astrid chiptune only if its sound suits the piece; otherwise procedural synthesis/DAW, then offline beat analysis. | WAV master, delivery MP3, duration, license/original-source record, SHA-256, beat/downbeat JSON tied to that digest. |
| Five landscape lake stills | **Actual Flux run via ComfyUI**, orchestrated with Astrid’s VibeComfy/generation tooling on a real GPU. | Workflow JSON, seeds, model revision, tool revision, prompts, actual GPU, timings and original outputs. |
| Five vertical variants | Crop when sufficient; otherwise a recorded Flux edit/outpaint run. | Source mapping and actual operation. Do not call a crop a new generation. |
| Five animated clips | **Actual Wan run through Wan2GP**, using a cloud GPU host such as RunPod through the corresponding Astrid tools. | Model/version, source image, seed, dimensions, frames, steps, job times, GPU and output hashes. |
| Posters and delivery encodes | FFmpeg from the actual generated clips. | Original-to-delivery mapping; duration/fps/codec probe; hashes of served bytes. |
| Mink poses | Codex image generation for reference-consistent art, then Astrid pixel tooling for extraction and density/outline checks. | Source grids, prompt history, frame dimensions/order, transparent strips, selected static frames. Start with the poses actually used. |
| Stack plates | Playwright screenshots of the real UI at controlled content, time, theme and viewport. | Capture script and fixture version; hero/§2 content only; light/dark variants. |
| Three fallback | Screenshot the implemented scene. | Same snapshot and scene version as the live view. |
| Beat-sync and model setup evidence | Execute the authored beat-sync implementation against the music; record a real LTX install/load/smoke run for displayed setup facts. | Inputs, artifact revision, output and sanitized setup receipt. |
| Horizon | Small procedural/vector pixel strip; image generation only if useful. | Transparent artifact and light/dark visual checks. |

**Get the real generation run early:** provision/select the actual GPU → run Flux five times → produce vertical inputs → run Wan five times in the cloud → retain raw receipts → encode delivery assets → hash delivery bytes → derive readout strings from the manifest.

Print measured facts only after those receipts exist. A model name plus invented duration is not evidence. Current light-study content cannot substitute for this run: its provenance says locally authored silent media, with unbound provider and unavailable verified output. `H/content/light-study-v1/provenance.ts:28`; `provider-binding.ts:5`; `verified-result.ts:5`.

Keep the public presentation clearly labeled as a scripted/recorded example. Do not imply that visiting the page launches generation or installs models.

## G. Over-engineering check

1. **Cut the guard/service implementation work.** Preserve and regression-test the landed behavior; do not reopen it as a homepage prerequisite. `H/PublicAstridEditorProvider.tsx:39`.

2. **Do not add Three again or automatically force a vendor chunk.** Use a lazy import, inspect the output, then decide whether manual chunking helps. `package.json:162`; `config/vite/policy.ts:19`.

3. **Keep one live editor and one plate representation.** Avoid a second editor, runtime DOM screenshot library, or live Remotion surfaces inside the exploded stack.

4. **Use a fixed approved asset registry for this finite demo.** This removes registry-publication races and the need to mutate the provider’s captured URL allowlist. `H/publicAstridExample.tsx:133`.

5. **Author endpoint snapshots; reuse pure patch operations where useful.** Do not build an ACP command registry or a general editing framework for a short homepage script. Do not rely on reserved split operations. `V/lib/timeline-patch.ts:994`.

6. **Avoid CSS-scaled timeline fallbacks.** The real zoom setter works. Use it with actual gutter measurements and restore the hero preference. `V/hooks/useEditorPreferences.ts:88`; `V/lib/coordinate-utils.ts:14`.

7. **Keep §4 edits to three light studies.** Preserve the lake clips as source material; editing both sets would enlarge the script, break the copy counts and burden phones.

8. **Extract a small overlay scheduler, not the entire callout system.** Keep connector/card-FLIP logic where it is. `H/PublicAstridCallouts.tsx:414`; `H/PublicAstridCalloutLayout.tsx:3`.

9. **Do not implement every historical mink pose before choreography is settled.** Produce the poses needed by approved cues; reuse static frames for quieter moments and reduced motion.

10. **Do not animate every skipped publication.** Commit the required endpoint and cancel obsolete cues. Preserve the visible fast-forward for ordinary adjacent departures.

11. **Do not render React state every animation frame.** Commit section/cue changes; use DOM/CSS motion and the sky’s raster channel between them. Existing sky channels already provide the right separation. `H/publicAstridSkySession.ts:580`.

12. **Do not treat the mockup timestamps, baked logs or existing lake-filled stack as specifications.** Preserve the story and visual treatment, but derive displayed content from the implemented timeline and recorded run.