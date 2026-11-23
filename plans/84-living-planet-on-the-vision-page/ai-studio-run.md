# Plan 84 — the AI Studio run board

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · Lab: [banodoco/planet](https://github.com/banodoco/planet)

This is the working document for running Plan 84's remaining work in Google AI Studio. Every planet and page change is made in the **planet lab**, `banodoco/planet`: the real Vision page's files from astrid-app, at the same paths, with the planet engine beside them. When the queue is done, the lab's changes are imported into astrid-app in a few integration packets. The owner chose this on 23 November 2026 ([inputs.md](inputs.md#owner-decisions)).

**State:** set up; not started. Starts on the owner's go.

## Who does what

| Role | Who | Does | Workstream |
| --- | --- | --- | --- |
| **Executor** | A fresh Google AI Studio Build session per packet | Changes the lab, runs its tests and build, writes a result note, pushes `lab/<id>` | The lab's [`LAB_RULES.md`](https://github.com/banodoco/planet/blob/main/LAB_RULES.md) and the packet brief |
| **Operator** | A Codex agent with browser control of the owner's AI Studio account | Opens the session, pastes the start prompt, keeps it to the packet, pushes, reports | [Run one packet in AI Studio](../../skills/roles/astrid-dev-manage/workstreams/ai-studio-packet.md) |
| **Reflection** | An Astrid agent on the high-judgment role (Astra) | Gates every packet (accept into lab `main`, rework, split), posts the daily look, replans at RF rows | [Reflect on AI Studio lab packets](../../skills/roles/astrid-dev-manage/workstreams/astra-reflection.md) |
| **Owner** | The owner | Looks at the lab once a day and replies with notes; final say on the look; gives the go for integration | — |
| **Integrator** | An Astrid agent in astrid-app (IN rows only) | Imports the lab into astrid-app and proves it there | [Manage](../../skills/roles/astrid-dev-manage/SKILL.md) |

## The loop

1. The board marks a packet **Ready** (its dependencies are Accepted).
2. The operator runs it in a fresh AI Studio session and pushes `lab/<id>` → **Gate**.
3. The reflection reviewer reruns the checks and reads the diff → **Accepted** (merged into lab `main`), **Rework** (at most twice) or **Split**.
4. Once a day the reviewer posts the **daily look**; the owner opens the lab's `main` in AI Studio's preview at the listed sizes and settings and replies with notes. Notes become rework, new packets or rulings below.
5. At each **RF** row the reviewer re-estimates and rewrites the briefs ahead.

One packet runs at a time until RF-A; after that, packets with no shared files may run in parallel, two at most.

**Mailbox:** one issue in banodoco/planet, titled `Planet lab mailbox`, created by the operator before EX-00. STATUS, BLOCKED, verdicts, the daily look and the owner's notes are comments on it. Link it here when it exists.

## Authority

The owner's go starts the run. Within it, the operator may open AI Studio sessions on the owner's account and push `lab/*` branches; the reflection reviewer may merge accepted `lab/*` branches into the lab's `main`, write and rewrite briefs in `packets/`, and update this board. **Comes to the owner:** anything paid (for example a hosted AI Studio deployment), changing `LAB_RULES.md`'s engine invariants or any existing test, changing `upstream.json`'s base, and the start of integration (IN-01). Landing in astrid-app follows the Release 15 rules in [inputs.md](inputs.md).

## Queue

Briefs: [`packets/`](https://github.com/banodoco/planet/tree/main/packets) in the lab; the outcome of each packet is in [its README](https://github.com/banodoco/planet/blob/main/packets/README.md#queue). Each EX is about one engineering day.

| ID | Outcome (short) | Depends on | State | Branch @ commit | Verdict |
| --- | --- | --- | --- | --- | --- |
| EX-00 | Prove the loop: import, test, build, push | — | Ready on go | | |
| RF-0 | Adjust rules and packet size to what AI Studio manages | EX-00 | | | |
| EX-01 | Build the world without WebGL; scene fingerprint test | RF-0 | | | |
| EX-02 | Types, resource owner, world config modules | EX-01 | | | |
| EX-03 | Terrain and terrain meshes | EX-02 | | | |
| EX-04 | Mink visuals | EX-02 | | | |
| EX-05 | MinkAgent and world assets | EX-03, EX-04 | | | |
| RF-A | Calibrate; re-cut scene packets | EX-05 | | | |
| EX-06 | Scenes 1–3 | RF-A | | | |
| EX-07 | Scenes 4–9 | EX-06 | | | |
| EX-08 | Scenes 10–14 | EX-06 | | | |
| EX-09 | Scenes 15–21 | EX-06 | | | |
| EX-10 | Vegetation, agents; balloon house, castle, Little Prince | EX-05 | | | |
| EX-11 | Wright biplane, Banzai Bill, orbit lanes | EX-10 | | | |
| RF-B | World split done; owner looks at every landmark | EX-07 to EX-11 | | | |
| EX-12 | One time of day with the sky session, no echo | RF-B | | | |
| EX-13 | Day replay, Use current time, reduced motion | EX-12 | | | |
| EX-14 | Quality levels and step-down guard | RF-B | | | |
| EX-15 | Off-screen stop; staged construction | EX-14 | | | |
| EX-16 | Still planet in every fallback case; controls | EX-15 | | | |
| EX-17 | Runtime split; no file over 1,200 lines | EX-12 to EX-16 | | | |
| RF-C | Engine contract complete; replan the page | EX-17 | | | |
| EX-18 | Framing at five sizes | RF-C | | | |
| EX-19 | Touch, taps, keyboard | EX-18 | | | |
| EX-20 | Reading comfort over the planet at all hours | EX-18 | | | |
| EX-21 | Arrival with the 1.8-second reveal | EX-16, EX-18 | | | |
| EX-22 | Camera fly-in | EX-21 | | | |
| RF-D | Taste rounds with the owner (at most three) | EX-22 | | | |
| IN-01 | Import into astrid-app; build, typecheck, lint | RF-D, owner's go | | | |
| IN-02 | App tests unchanged; captures; CI path filter | IN-01 | | | |
| IN-03 | Production measurements; no planet code on Home | IN-01 | | | |
| IN-04 | Owner's look on real devices; review; landing | IN-02, IN-03 | | | |

**Estimate:** about 23 execution days plus reflection and the daily looks, and 4 integration days. RF-0 and RF-A restate it from what the first packets actually take.

## How the import stays mechanical

- The lab's `src/pages/Home/`, `src/shared/` and `public/` are astrid-app's own files at the same paths, copied from `plan-84/pl-2` at `0e290681` (recorded in the lab's `upstream.json`). The lab mounts the page exactly as the App's `PublicAstridSite` does, with the real sky session, so time-of-day, layout and palette work is done against the real code.
- The lab's engine is the App's PL-1 port with the mock-up's later commit `a444d14` (Banzai Bill, orbit lanes) merged in.
- `npm run check` in the lab runs the App's own 90 page, sky and planet tests, unchanged, plus lab checks: file sizes, allowed imports in exported files, the pinned three.js, no new randomness or clocks in the engine, and no new TypeScript diagnostics beyond the two the App already has in `publicVisionContent.ts`.
- `scripts/export-to-app.mjs` replays the lab's changes since the base commit onto an astrid-app branch, and refuses paths outside the mirrored folders. A dry run with no lab changes is a no-op apart from the merged engine.
- What the lab cannot prove: screenshots (AI Studio cannot take them, so the owner's daily look stands in, and IN-02 takes the real captures), real-device speed and heat (IN-03, IN-04), and the App's full CI (IN-02).

## Existing App work

- **`release/15/plan-84`** (PL-1 merged) is the base the integration lands on.
- **`plan-84/pl-2`** (`0e290681`, the Foundations panel and stage) is the lab's base, so its layout is already in the lab; it merges into the plan branch at IN-01.
- **[astrid-app#372](https://github.com/banodoco/astrid-app/pull/372)** (entry repair) touches `publicAstridNavigation.ts`, which the lab does not hold. EX-15 rebuilds its fix inside the engine and the wrapper; at IN-01 the integrator keeps whichever is still needed from #372 and closes the rest.

## Standing rulings

- The lab's engine invariants and file limits are in `LAB_RULES.md`; this board does not repeat them.
- Proposal [astrid-dev#1631](https://github.com/banodoco/astrid-dev/pull/1631) is the source of the packet split; this board supersedes its satellite-lab and transfer-receipt mechanics.
