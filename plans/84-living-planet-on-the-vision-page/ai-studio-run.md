# Plan 84 — the AI Studio run board

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · Lab: [banodoco/planet](https://github.com/banodoco/planet)

This is the working document for running Plan 84's remaining work in Google AI Studio. Every planet and page change is made in the **planet lab**, `banodoco/planet`: the real Vision page's files from astrid-app, at the same paths, with the planet engine beside them. When the queue is done, the lab's changes are imported into astrid-app in a few integration packets. The owner chose this on 23 November 2026 ([inputs.md](inputs.md#owner-decisions)).

**State:** set up; starts when the owner sends the [manager start message](#manager-start-message). The lab's `main` has passed `npm run check` and `npm run build`, and the fidelity check against the App.

## Who does what

| Role | Who | Does | Workstream |
| --- | --- | --- | --- |
| **Manager** | One Codex session, started by the owner with the [start message](#manager-start-message), with browser control of the owner's AI Studio account | Runs the queue: drives each packet through AI Studio as its operator, commissions a reflection for each one, merges accepted packets into the lab's `main`, posts the daily look, keeps this board current | [Run one packet in AI Studio](../../skills/roles/astrid-dev-manage/workstreams/ai-studio-packet.md) for each packet |
| **Executor** | A fresh Google AI Studio Build session per packet | Changes the lab, runs its tests and build, writes a result note, pushes `lab/<id>` | The lab's [`LAB_RULES.md`](https://github.com/banodoco/planet/blob/main/LAB_RULES.md) and the packet brief |
| **Reflection** | A fresh Astra subagent (the high-judgment role) that did none of the work, commissioned by the manager for every gate and RF row | Gates every packet (accept, rework, split), replans at RF rows, drafts the daily look | [Reflect on AI Studio lab packets](../../skills/roles/astrid-dev-manage/workstreams/astra-reflection.md) |
| **Owner** | The owner | Looks at the lab once a day and replies with notes; final say on the look; gives the go for integration | — |
| **Integrator** | An Astrid agent in astrid-app (IN rows only), commissioned by the manager after the owner's go | Imports the lab into astrid-app and proves it there | [Manage](../../skills/roles/astrid-dev-manage/SKILL.md) |

The manager does not write lab code itself and does not overrule a reflection verdict; it may ask a second Astra reviewer when it disagrees, and takes the disagreement to the owner if they still differ.

## The loop

1. The board marks a packet **Ready** (its dependencies are Accepted).
2. The manager runs it in a fresh AI Studio session and pushes `lab/<id>` → **Gate**.
3. A fresh Astra subagent reruns the checks and reads the diff → **Accepted** (the manager merges it into lab `main` with a merge commit), **Rework** (at most twice) or **Split**.
4. Once a day the manager gives the owner the **daily look** in its own chat; the owner opens the lab's `main` in AI Studio's preview at the listed sizes and settings and replies there with notes. Notes become rework, new packets or rulings below.
5. At each **RF** row an Astra subagent re-estimates and rewrites the briefs ahead; the manager merges the brief changes into the lab's `main` and updates this board.

One packet runs at a time until RF-A; after that, packets with no shared files may run in parallel, two at most.

**Talking to the owner:** the manager reports straight to the owner in its own chat: a short status after each packet and verdict, anything blocked, and the daily look. There is no mailbox issue. Astra reviewers report their verdicts back to the manager as subagents. Anything that must outlive the chat (each verdict and commit, the owner's rulings on the look) goes on this board.

**Board updates:** the manager updates this file on astrid-dev `main` through a pull request at least once a day and at every RF row (the repository requires pull requests and passing checks; merge each one once its checks pass).

## Authority

The owner's go (sending the start message) starts the run. Within it, the manager may open AI Studio sessions on the owner's account, push `lab/*` branches, commission Astra subagents, merge a `lab/*` branch into the lab's `main` on an Astra accept verdict, merge Astra's brief rewrites into `packets/`, and update this board and Plan 84's progress through pull requests to astrid-dev `main`. **Comes to the owner:** anything paid (for example a hosted AI Studio deployment), changing `LAB_RULES.md`'s engine invariants or any existing test, changing `upstream.json`'s base, and the start of integration (IN-01). Landing in astrid-app follows the Release 15 rules in [inputs.md](inputs.md).

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

## Plan 84 tasks and the packets that deliver them

The accepted outcome and completion cases in [plan.md](plan.md) are unchanged; this is how the remaining PL tasks map onto the lab's packets.

| Plan task | Delivered by |
| --- | --- |
| PL-0, PL-1 | Done in run 1 (the lab starts from PL-1's port) |
| PL-2 The page's layout | The lab's base (`plan-84/pl-2`), finished by EX-20 |
| PL-3 Framing for each size | EX-18, EX-19 |
| PL-10 One time of day | EX-12, EX-13 |
| PL-4 The still planet and the way in | EX-16, EX-21, EX-22 |
| PL-5 Speed | EX-14, EX-15; measured on a production build at IN-03 |
| PL-6 Pictures and tests | EX-01 (the lab's scene fingerprint), IN-02 (the App's captures and workflow) |
| PL-7 Taste rounds | RF-D and the owner's daily looks |
| PL-8 The owner's look | IN-04 |
| PL-9 Engine in modules | EX-01 to EX-11, EX-17 |
| R Review | Astra gates throughout; one independent review of the integrated App candidate at IN-04 |

## Manager start message

The owner sends this, as the first message, to a new Codex session that can control a browser signed in to the owner's Google AI Studio account and that has GitHub access to banodoco/planet and banodoco/astrid-dev.

```text
You are the manager of Plan 84's AI Studio run: you farm the planet lab's packets out to Google AI Studio, one at a time, and have each one reviewed by an Astra subagent before the next starts.

Read, in this order, on banodoco/astrid-dev main:
1. plans/84-living-planet-on-the-vision-page/ai-studio-run.md (this board: your role, the loop, your authority, the queue)
2. skills/roles/astrid-dev-manage/workstreams/ai-studio-packet.md (how you run each packet in AI Studio)
3. skills/roles/astrid-dev-manage/workstreams/astra-reflection.md (what each Astra reviewer you commission does)
Then on banodoco/planet main: LAB_RULES.md and packets/README.md.

Your authority is the board's Authority section; anything it does not list comes to me. You do not write lab code yourself.

Start now:
1. Run EX-00 in a fresh AI Studio Build session connected to banodoco/planet main, using the start prompt in ai-studio-packet.md.
2. Commission a fresh Astra subagent for the EX-00 gate and then RF-0, and act on their verdicts.
3. Tell me here, in a few lines, after each packet and verdict, then continue down the queue. Record each verdict on the board.

Report to me directly in this chat; there is no mailbox. Each day, give me the daily look here: what was accepted, the lab main commit, and exactly what to open and look at. My replies here are binding on how it looks; record my rulings on the board.

If you cannot drive AI Studio from your browser, tell me, and give me the ready-to-paste start prompt for each packet instead; I will paste it and tell you when it has pushed.
Never push to the lab's main except by merging an accepted packet, never change LAB_RULES.md, an existing test or upstream.json, and never touch banodoco/astrid-app before I give the go for IN-01.
```

## Standing rulings

- The lab's engine invariants and file limits are in `LAB_RULES.md`; this board does not repeat them.
- Proposal [astrid-dev#1631](https://github.com/banodoco/astrid-dev/pull/1631) is the source of the packet split; this board supersedes its satellite-lab and transfer-receipt mechanics.
