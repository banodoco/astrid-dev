# A living planet on the vision page

**Project:** A living planet on the vision page

**Goal:** The public vision page opens on a living 3D planet in place of the hero's pixel-art mink; the planet continues behind one translucent panel that holds the Pillars and the Principles; and it arrives with an authored intro, runs smoothly, and looks right on every device.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 12 engineering days: the planet is already built as a mock-up, so this is integration, performance, devices, the intro and polish. About 14 if the engine is also split into modules in this plan (D2).

**Waiting on:** a manager on the taste route; the owner's decisions D1 and D2 in [inputs.md](inputs.md#owner-decisions).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-003 — Our vision and execution aren't yet fully connected](../../vision/gaps/CA-003-vision-experiments-progress.md) (primary): the vision page is where a newcomer first meets what Astrid is for, and the planet shows the pillars as places they can visit, not a list to read. CA-003's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

The vision page today (astrid-app `src/pages/Home/PublicAstridVision.tsx`, served at `/vision`) has a hero with a pixel-art mink juggling at the right, then a Pillars section of cards ("What we're building"), then a Principles section. The owner has built a mock-up, [banodoco/planet](https://github.com/banodoco/planet), in which a low-poly planet with articulated orange mink sits at the top right of the hero and runs on behind the section below, and the pillar cards turn the planet to the place each one stands for.

**What a visitor gets:**

- **The planet in the hero,** top right, where the juggling mink is now.
- **One translucent panel** below the hero that holds both the Pillars and the Principles, with the planet visible behind it. The text stays comfortably readable over a moving background.
- **An intro:** the page's words appear at once; the planet then arrives in an authored entrance, with no empty box, flash or jump in the layout.
- **Cards that move the world:** choosing a pillar turns the planet to its place, as in the mock-up.
- **The same care on a phone, a tablet, a laptop and a wide screen,** by touch, mouse or keyboard.
- **A still planet, never a hole,** for a visitor who asks for reduced motion or whose device cannot draw it.

**How it is judged.** This is taste work with engineering under it. The manager is the tastemaker and judge: it farms small tasks out to workers, looks at what comes back in screenshots and short recordings at fixed sizes, and sends it back until it is right. The owner looks at a preview before it lands; her look is the final judgment.

**Not included:** changing what the vision, pillars or principles say (that text comes from astrid-dev's `vision/` folder and is not touched); the Home page; new scenes, creatures or places on the planet beyond what the mock-up has; sound; any use of the mock-up's unused AI-studio scaffolding.

## Existing work and decision

- **The mock-up is the design reference and the donor of the engine:** banodoco/planet at `037293de`. One function, `initPlanetEngine(canvas, callbacks)`, in one 8,996-line file, drives a single three.js scene with 22 named places; four story cards turn the planet to four of them. It builds to 979 kB of JavaScript (266 kB compressed). What it does and does not yet do is in [evidence/research-planet-mock-up.txt](evidence/research-planet-mock-up.txt).
- **The page already has a home, tests and a way of working:** the App's `vision-content` checks include screenshot captures of the hero, the Pillars and the Principles, mobile layout checks and a reduced-motion path; three.js is already one of the App's dependencies. See [evidence/research-vision-page-and-manager-route.txt](evidence/research-vision-page-and-manager-route.txt).
- **Decision: the engine moves into the App.** It is brought into astrid-app beside the page and loaded only when the page needs it. banodoco/planet stays as the mock-up it is; nothing is published from it. A separate package would add a release to coordinate for one consumer.
- **Precedent for the way of working:** [Plan 21](../21-astrid-website/plan.md), the website, ran on screenshots, visual criteria and delegated capture and edit tasks.

## Sequence and readiness

1. **PL-1,** the engine in the App behind a clean boundary, loaded on demand, with a frozen-time mode so pictures of it can be compared.
2. **PL-2 and PL-3,** the planet in the hero and the translucent panel over it. From here the page looks like the mock-up, and every later task is judged by eye.
3. **PL-4, PL-5, PL-6, PL-7,** side by side: the intro, speed, devices, and the still planet for reduced motion and failure.
4. **PL-8,** the page's own tests brought up to the new look, with the owner's look at a preview as the approval of the new pictures.
5. **PL-9,** the taste rounds.
6. **PL-10,** the engine in modules, if D2 says it is in this plan.
7. **R,** one review round.

**Real dependencies:** none on other plans. It changes astrid-app only. [Plan 53](../53-vision-aspirations/plan.md) changes the vision's text and the feed the page reads, not its layout; if both are in flight, this plan takes the feed as it finds it.

**Unresolved:** D1 and D2. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the mock-up's engine and look; the page's existing content feed, unchanged. **Produces:** one planet component in astrid-app that a page mounts into a container; the reworked hero and the combined panel; a still poster image of the planet; tests and budgets that hold the result. **Compatibility:** no change to the content feed, to astrid-dev's `vision/` folder or to any other page; the page's address and its navigation stay as they are.

## Completion

- **The look:** at five sizes (a phone upright and on its side, a tablet, a laptop, a wide screen) the page matches the mock-up's composition and the manager's and owner's judgment, shown by before-and-after pictures and a short recording of the intro at each size.
- **The intro:** words first, then the planet's entrance, once per visit, with no layout shift and no empty frame.
- **Smooth:** on a mid-range phone and on a laptop with built-in graphics the planet holds a steady frame rate while the page scrolls, steps its own quality down when it cannot, and does no work when it is off screen or the tab is hidden. The numbers are set by measurement in PL-5 and then held by a test.
- **No cost before it is wanted:** the page's words and layout load as fast as today; the planet's code arrives separately.
- **Everyone gets something good:** with reduced motion, without WebGL, or after the graphics context is lost, the visitor sees the still planet; touch scrolling works over the planet; every control and card works from the keyboard and says what it is and what state it is in.
- **Clean:** nothing of the mock-up's scaffolding is in the App; mounting and unmounting the page ten times leaves no graphics memory behind.
- **Held:** the page's screenshot tests show the new look, approved by the owner; the existing sky and content checks still pass.
- **Limits of the proof:** frame rates measured in CI's headless browser stand in for real devices; the owner's own look on her phone and laptop is part of the proof and is recorded. Landing and publishing remain the owner's.
