# Astrid Homepage Journey — Tasks

Task progress is tracked in the phase cards linked from this index. The project has 34 tasks: 8 XHARD (route `X`), 13 NORMAL (route `N`), 7 TASTE-HIGH, 2 TASTE-LOW, and 4 ASSET placeholder tasks. Routes `N` and `X` use the shared run contract routing table.

## Task index

The index links each task to its accepted card in the matching phase file.


### Phase 0 (parallel, after Step 0)

| ID | Work |
|---|---|
| [`T0`](tasks/phase-0.md#task-t0) | The Opus sheet |
| [`P1`](tasks/phase-0.md#task-p1) | **The Artifact preview, from today's hero** |
| [`H0`](tasks/phase-0.md#task-h0) | Capture harness |
| [`S1`](tasks/phase-0.md#task-s1) | Snapshot publish and replay spike |
| [`S2`](tasks/phase-0.md#task-s2) | The live stack pose |
| [`S4`](tasks/phase-0.md#task-s4) | Scroll-driven sky with ownership |
| [`A1`](tasks/phase-0.md#task-a1) | Placeholder music + beat list |
| [`A2`](tasks/phase-0.md#task-a2) | Placeholder lake media |
| [`A5a`](tasks/phase-0.md#task-a5a) | Mink placeholder kit |
| [`A9`](tasks/phase-0.md#task-a9) | Pixel icons |

### Phase 1: foundation

| ID | Work |
|---|---|
| [`T1`](tasks/phase-1.md#task-t1) | Scripts, snapshots and registry to T0's numbers |
| [`T2`](tasks/phase-1.md#task-t2) | Session-owned publisher and adoption bridge |
| [`T3`](tasks/phase-1.md#task-t3) | Scroll reader, pure director, projections and clock |
| [`T5`](tasks/phase-1.md#task-t5) | Sticky showcase in the tall grid |
| [`T9`](tasks/phase-1.md#task-t9) | Fit controller and hero zoom restore |
| [`T10`](tasks/phase-1.md#task-t10) | Flat overlay layer with computed positions + `PixelSprite` |
| [`T28`](tasks/phase-1.md#task-t28) | Shared motion primitives reading only tokens |

### Phase 2: §2 and §4 in parallel, the sky, the mink

| ID | Work |
|---|---|
| [`T6`](tasks/phase-2.md#task-t6) | Section layouts |
| [`T8`](tasks/phase-2.md#task-t8) | The pull-apart and its reverse, from App and Agent, at D and P, plus the RM dip |
| [`T11`](tasks/phase-2.md#task-t11) | Section spines with chip slot, pending ellipsis, reserved height |
| [`T12`](tasks/phase-2.md#task-t12) | The look of every primitive |
| [`T13`](tasks/phase-2.md#task-t13) | Three.js structure view |
| [`T14`](tasks/phase-2.md#task-t14) | §2 example states and tabs |
| [`T15`](tasks/phase-2.md#task-t15) | Example panels, **including the 3D view's look** |
| [`T19`](tasks/phase-2.md#task-t19) | §4 mechanics |
| [`T20`](tasks/phase-2.md#task-t20) | The grow and the §4 beats |
| [`T21`](tasks/phase-2.md#task-t21) | Sky in the journey |
| [`M1`](tasks/phase-2.md#task-m1) | Every mink cue and glyph |

### Phase 3: §3

| ID | Work |
|---|---|
| [`T17`](tasks/phase-3.md#task-t17) | Tray mechanics |
| [`T18`](tasks/phase-3.md#task-t18) | The fold and every §3 beat at D and P |

### Phase 4: finale, navigation, accessibility, E2E

| ID | Work |
|---|---|
| [`T22`](tasks/phase-4.md#task-t22) | The finale |
| [`T23`](tasks/phase-4.md#task-t23) | Navigation, lifecycle and hash restore |
| [`T24`](tasks/phase-4.md#task-t24) | Semantics and keyboard |
| [`T26`](tasks/phase-4.md#task-t26) | The journey E2E spec with `page.clock` |

## Review rounds

| ID | Who | What | Done when |
|---|---|---|---|
| R1 | Astra (`gpt-6-astra`, xhigh, legwork to Luna; the coordinator runs the browsers) | **Per section at D and P:** dropped frames and p95 frame time while scrolling (1× and 4× CPU throttle); the longest main-thread task during its demo (adoption commits, three.js init, tray video start, waveform decode); sky raster ms per paint and paints per second; the cost of the ambient cycle at rest (compositor and CSS motion only; no per-frame React; paused off-screen and in hidden tabs); bytes fetched entering it. **Page-level:** hero LCP, TBT and initial JS compared with `main`; peak memory and live video/WebGL counts on an iPhone. **One real-iPhone pass** via Safari Web Inspector on the LAN preview | A short report with numbers against `main`, named regressions and a ranked, tiered fix list |
| R2-D | Opus, **desktop iteration pass** (deploys Haiku subagents for captures and edits) | Iterates on the running page at D and S (1440×700), both audiences and both palettes, from H0 recordings, 2× stills and the live preview. It judges the two priorities first: each section alive at rest (`rest-*`) and every transition really nice (`pull-*`, `fold`, `grow`, `back-*`, `flick`). Then it checks the rest of the journey against [design.md](design.md#10-craft-details-t0s-starting-values-from-the-opus-craft-pass) and the mockups, and that every cut-list item ([design.md](design.md#107-cut-list-r2-confirms-each-is-absent)) is absent. Each loop: judge → fix taste issues directly (Haiku subagents make the edits; Opus checks them) → send mechanism issues to the coordinator as tiered fix tasks → re-capture. Up to 3 loops | Both priorities pass at D and S on a fresh capture; any remaining findings are tiered for R3 |
| R2-P | Opus, **phone iteration pass** (deploys Haiku subagents for captures and edits) | The same loop at P (390×844) and N (320×693), plus reduced motion and "Show the steps". It includes one look on a real iPhone in Safari via the LAN preview (toolbar collapse, sticky stage, sky), with the coordinator driving the device or the user sending notes. Runs in parallel with R2-D on its own port; layout changes that could affect desktop are checked against D before they're kept | Both priorities pass at P and N on a fresh capture and on the real iPhone; remaining findings tiered for R3 |
| R3 | Tiered like everything else; each fixer follows the fan-out rule (Opus/Sonnet → Haiku, Terra/Sol/Astra → Luna) | One fix round over R1's findings and anything R2-D or R2-P couldn't close in its loops | Findings fixed or explicitly dropped; R1's numbers and the R2 priorities still pass on a re-capture |
| R4 | Coordinator, **after asking the user** | (a) May placeholder media ship, or make real assets first ([inputs.md](inputs.md#asset-scope-and-provenance))? (b) Merge `feat/home-journey` into `main` | E2E green, budget green, R3 done, the user has seen the preview, the user said go |

## Phase order

| Phase | Runs in parallel | Notes |
|---|---|---|
| Step 0 | branch · Luna pointer re-check · commit the folder | Coordinator |
| 0 | T0 · P1 · H0 · S1 · S2 (with the T8 Opus agent) · S4 · A1 · A2 · A5a · A9 | One heavy Codex test job at a time; S2 waits only for H0 v0 |
| 1 | T1 → T2 → T3 → T5 · T28 (after T0) · then T9, T10 | A short serial chain |
| 2 | §2: T6, T8, T11, T12, T13, T14, T15 · §4: T19, T20 · T21 · M1 as cue slots land | §4 starts with §2 so the payoff gets the most refinement time |
| 3 | §3: T17, T18 · T20's grow after T18 | |
| 4 | T22 · T23 · T24 · T26 | |
| Review | R1 ∥ R2-D ∥ R2-P → R3 → ask the user → R4 | The only review gates; R2-D and R2-P iterate, they don't just report |

TASTE-HIGH pass 2s run as each moment reaches the preview, before R2-D and R2-P.

## How to run it

### Repo, branches, worktrees
`banodoco/astrid-app`, branch `feat/home-journey` off `main`. One worktree per parallel task: `git worktree add ../hj-<id> -b hj/<id> feat/home-journey`. The coordinator merges `hj/<id>` into `feat/home-journey`, merges `main` in daily, and re-runs S1's adoption test after each merge.

### Agents
- **Codex:** `codex exec -m <model> --skip-git-repo-check -C ../hj-<id> -s workspace-write --add-dir <repo>/.git -o reports/<id>.last.txt "<brief>" < /dev/null`, in the background; Sol adds `-c model_reasoning_effort='"xhigh"'`. No ports, signals or nested sandboxes.
- **Claude:** Agent tool with `model: "opus"` or `"sonnet"`; they deploy Haiku subagents (`model: "haiku"`) for the hands-on work, fixes included.
- **Fan-out:** Terra, Sol and Astra deploy Luna subagents (`spawn_agent`, `model: "gpt-6-luna"`) for the hands-on work, fixes included. Every brief says this explicitly ([tasks.md](#brief-templates)).
- **Preview:** only the coordinator republishes the Artifact (P1's script, then the Artifact publish with the same file path/URL). Fallback: `vite preview --host` from `dist-preview/`, opened at the Mac's LAN address `/home` on the iPhone (or a quick tunnel).

### Dev server, tests, rules
- `npm run dev` serves port 2222 (`config/vite/policy.ts:1`); taste agents use 2223+. Open `/home`. The public path needs no backend; Supabase vars can be placeholders. The build needs the selected or bundled Astrid source and a valid tool catalog (`config/vite/astridSource.ts:67`).
- vitest on Node 20.19.4 (executor brief), `--maxWorkers=2..4`; don't use `vitest.public-host.config.ts`.
- E2E: `npx playwright test --config playwright.config.ts tests/e2e/public-astrid-journey.spec.ts` (boots its own Vite and fake Runtime; `chromium-condensed`/`chromium-mobile` are WebKit).
- `npm run lint` allows zero warnings; `react-hooks/exhaustive-deps` is an error. No `@/integrations/supabase/client` in journey code. Palette tokens (`--astrid-*`), never hard-coded colours. Lint and debt allowlists only shrink. `npm test` rejects placeholder smoke tests. No `ms`/`cubic-bezier` literals in `J/` outside the tokens.

### H0 capture IDs
Recordings `h0/<id>-<D|P>.webm`; stills `h0/<id>-<D|P>-<ms>.png` at 2× DPR. Scroll profiles: **slow** 400 px/s, **flick** 3000 px/s, **back** 600 px/s. Ids: `pull-app`, `pull-agent`, `pull-interrupt` (App→Agent switch, then scroll at 300 ms), `back-2-1`, `fold`, `back-3-2`, `grow`, `back-4-3`, `flick` (hero→§4), `s2-demo`, `s3-demo`, `s4-demo`, `rest-2`, `rest-3`, `rest-4` (20 s resting in each section after its demo, to judge that it feels alive), `finale`, each also `-rm`. Seeded blinks keep reruns identical. Judge at 2× against the named mockup, not from contact sheets.

### Reports
`docs/plans/home-journey/reports/<id>.md`: what changed, decisions made (with one-line reasons), tests run, checks left for the coordinator.

### Brief templates

Fix tasks (hand-offs from R2-D or R2-P, and R3) use the same template for their tier, with the finding and its capture in place of the task row. Every senior fixer follows the fan-out rule: Opus and Sonnet deploy Haiku; Terra, Sol and Astra deploy Luna.

**NORMAL (route `N`: Haiku or Luna)**
> Task `<id>` (NORMAL) for the Astrid homepage journey. Read `docs/plans/home-journey/plan.md` for authority and order, the `<id>` card at `docs/plans/home-journey/tasks/phase-<phase>.md#task-<id>`, the relevant `design.md` sections, and `inputs.md` when source facts or assets matter. Work in `../hj-<id>` on branch `hj/<id>`; touch only `<files>`. Timings and easings come from `J/journeyMotion.ts`; never write `ms` or `cubic-bezier` literals. For any legwork that splits, including fixes, spawn parallel subagents of your own model. Run vitest on Node 20 (`export PATH=<path to Node 20.19.4>/bin:$PATH`, `--maxWorkers=2`). You can't run a dev server or Playwright: list the visual and E2E checks the coordinator should run. Done when: `<row>`. Commit to `hj/<id>` and write `reports/<id>.md`.

**XHARD (route `X`: Sonnet or Terra)**
> Task `<id>` (XHARD) … *(as NORMAL, plus:)* You own the mechanism and its correctness. Write the tests that pin the behaviour rules first. Deploy parallel `N` subagents in your family (Haiku via `model: "haiku"`, Luna via `spawn_agent`) for the hands-on work (reading, searching, edits, running unit tests), including when you're fixing; keep the design decisions yourself and check what they return. You're bound by the experience, not the suggested implementation: prefer the simplest mechanism that meets the done-when, and record any deviation and anything you chose not to build.

**TASTE-HIGH (Opus)**
> You own the feel of `<moment>` (task `<id>`, TASTE-HIGH). Read the task card at `tasks/phase-<phase>.md#task-<id>`, the relevant [design.md sections](design.md), [inputs.md](inputs.md#starting-code-facts) when source facts matter, and `notes/opus-craft.md`. Run your own dev server on port `<2223+>` and H0 for `<ids>`; judge at 2× against `mockups/<frames>`. Decide the tuning of tokens, CSS custom properties and choreography yourself. Deploy parallel Haiku subagents (`model: "haiku"`) to make the edits, run captures and read code, and check every result before keeping it. If the mechanism needs changing, write a note for the coordinator rather than rebuilding it. You're bound by the experience (the executor brief), not the suggested implementation. Two passes: pass 2 once it's on the preview, folding in any user notes. Done when: you sign off `<named stills/recordings>`. Append your decisions to `notes/opus-craft.md` and write `reports/<id>.md`.

**TASTE-LOW (Sonnet)**
> You own the look of `<components>` (task `<id>`, TASTE-LOW). Read the task card at `tasks/phase-<phase>.md#task-<id>` and the relevant [design.md sections](design.md); consult [inputs.md](inputs.md#starting-code-facts) for source facts. Use your own dev server (`<port>`) and H0 for `<ids>`; judge at 2× against `mockups/<frames>` in both palettes at D and P. Change only styling and token use in `<files>`; mechanism changes go back as a note. Deploy parallel Haiku subagents (`model: "haiku"`) for the edits, captures and legwork, and check their results. Done when: `<row>`. Write `reports/<id>.md`.

**ASSET (placeholder)**
> Make placeholder `<asset>` (task `<id>`): `<spec from [inputs.md](inputs.md#6-assets)>`. Use `<Codex image generation | FFmpeg | the Astrid chiptune pack | existing art>`. Write files to `P/…` at the given dimensions and durations, compute sha256 and duration, and register them in `L/journey-media.ts` in the light-study format. Placeholders claim nothing real. Done when: `<row>`. Write `reports/<id>.md` with the commands used, so the real asset can replace it as data later.
