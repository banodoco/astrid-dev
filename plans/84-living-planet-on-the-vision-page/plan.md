# A living planet on the vision page

**Project:** A living planet on the vision page

**Goal:** The public vision page opens on a living 3D planet in place of the hero's pixel-art mink; the planet continues behind one translucent panel, Foundations, that holds the Pillars and the Principles; and it arrives with an authored intro, runs smoothly, and looks right on every device.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 16 engineering days, including one shared time of day and splitting the engine into modules: the planet is already built as a mock-up, so this is integration, performance, devices, the intro and polish. It is re-stated after the device trial (PL-0), which decides how much has to be drawn live on a phone.

**Waiting on:** a manager on the taste route. The owner's one decision, D1 in [inputs.md](inputs.md#owner-decisions), is needed before landing, not before starting.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-003 — Our vision and execution aren't yet fully connected](../../vision/gaps/CA-003-vision-experiments-progress.md) (primary): the vision page is where a newcomer first meets what Astrid is for, and the planet shows the pillars as places they can visit, not a list to read. CA-003's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

The vision page today (astrid-app `src/pages/Home/PublicAstridVision.tsx`, served at `/vision`) has a hero with a pixel-art mink juggling at the right, then a Pillars section of cards ("What we're building"), then a Principles section. The owner has built a mock-up, [banodoco/planet](https://github.com/banodoco/planet), in which a low-poly planet with articulated orange mink sits at the top right of the hero and runs on behind the section below, and the pillar cards turn the planet to the place each one stands for.

**What a visitor gets:**

- **The planet in the hero,** top right, where the juggling mink is now.
- **One translucent panel, Foundations,** below the hero that holds both the Pillars and the Principles, with the planet visible behind it. The text stays comfortably readable over a moving background.
- **One time of day, and spinning the planet changes it.** The public pages already have a sky that follows the visitor's real time and can play through a day. The planet joins it: it arrives lit for the hour the sky shows, and when a visitor spins it the hour moves with it, so the sky behind and the page's colours change as the planet turns.
- **An intro:** the page's words appear at once; the planet then arrives in an authored entrance, with no empty box, flash or jump in the layout.
- **The same care on a phone, a tablet, a laptop and a wide screen,** by touch, mouse or keyboard.
- **A still planet, never a hole,** for a visitor who asks for reduced motion or whose device cannot draw it.

**How it is judged.** This is taste work with engineering under it. The manager is the tastemaker and judge: it farms small tasks out to workers, looks at what comes back in screenshots and short recordings at fixed sizes, and sends it back until it is right. The owner looks at a preview before it lands; her look is the final judgment.

**Not included:** changing what the vision, pillars or principles say (that text comes from astrid-dev's `vision/` folder and is not touched); changing what a pillar card does when chosen (it opens its goals, gaps and projects, as now; the mock-up's cards turn the planet instead, and whether the planet also turns toward a pillar on hover or focus is a taste detail, not a requirement); a new navigation entry for the panel (it is named Foundations, but both section headings and both links stay as they are); the Home page; new scenes, creatures or places on the planet beyond what the mock-up has; sound; any use of the mock-up's unused AI-studio scaffolding.

## Existing work and decision

- **The mock-up is the design reference and the donor of the engine:** banodoco/planet at `037293de`. One function, `initPlanetEngine(canvas, callbacks)`, in one 8,996-line file, drives a single three.js scene with 22 named places; four story cards turn the planet to four of them. It builds to 979 kB of JavaScript (266 kB compressed). What it does and does not yet do is in [evidence/research-planet-mock-up.txt](evidence/research-planet-mock-up.txt).
- **The page already has a home, tests and a way of working:** the App's `vision-content` checks include screenshot captures of the hero, the Pillars and the Principles, mobile layout checks and a reduced-motion path; three.js is already one of the App's dependencies. See [evidence/research-vision-page-and-manager-route.txt](evidence/research-vision-page-and-manager-route.txt).
- **Decision: the engine moves into the App.** It is brought into astrid-app beside the page and loaded only when the page needs it, on the App's own version of three.js (0.185.1; the mock-up targets 0.187) and in its own canvas, apart from the editor's. banodoco/planet stays as the mock-up it is; nothing is published from it. A separate package would add a release to coordinate for one consumer.
- **What the page already has is reused, not rebuilt:** the sky's 1.8-second reveal, the 760-pixel point below which the hero's illustration is hidden, the reduced-motion rules and the stable loading text.
- **An independent critique changed this plan** before it was accepted; what it found and what was done with each point is in [inputs.md](inputs.md#planning-evidence).
- **Precedent for the way of working:** [Plan 21](../21-astrid-website/plan.md), the website, ran on screenshots, visual criteria and delegated capture and edit tasks.

## Sequence and readiness

1. **PL-0,** a short trial of the mock-up as it is, on a real phone and laptop, and the record of where its code and art came from.
2. **PL-1,** the engine in the App behind a clean boundary, loaded on demand, with a fixed pose so pictures of it can be compared.
3. **PL-2, PL-3 and PL-10,** the page's layout, the planet's framing at each size, and the planet and the sky sharing one time of day. From here the page looks like the mock-up, and every later task is judged by eye.
4. **PL-4 and PL-5,** side by side: the still planet and the intro, and speed.
5. **PL-6,** the page's pictures and tests brought up to the new look.
6. **PL-7,** the taste rounds.
7. **PL-8,** the owner's look at the finished page on her own phone and laptop.
8. **PL-9,** the engine split into modules, once the pictures that prove nothing changed exist.
9. **R,** one review round.

**Real dependencies:** none on other plans. It changes astrid-app only. [Plan 53](../53-vision-aspirations/plan.md) changes the vision's text and the feed the page reads, not its layout; if both are in flight, this plan takes the feed as it finds it.

**Unresolved:** D1. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the mock-up's engine and look; the page's existing content feed, unchanged. **Produces:** one planet component in astrid-app that a page mounts into a container; the reworked hero and the combined panel; a still poster image of the planet; tests and budgets that hold the result. **Compatibility:** no change to the content feed, to astrid-dev's `vision/` folder or to any other page; the page's address and its navigation stay as they are.

## Completion

- **The look:** at five sizes (a phone upright and on its side, a tablet, a laptop, a wide screen) the page matches the mock-up's composition and the manager's judgment, shown by before-and-after pictures and a short recording of the intro at each size; and the owner has looked at the finished page on her own phone and laptop and approved it.
- **One time of day:** on arrival the planet's light matches the sky's hour; spinning the planet moves the sky, the page's colours and the planet's light together, through a whole day, with one owner of the hour and no flicker or lag between them; and there is a way back to the real time.
- **The intro:** words first, then the planet's entrance, once per visit, with no layout shift and no empty frame.
- **Smooth:** on the named phone and laptop from PL-0 the planet holds a steady frame rate while the page scrolls, and it does no work when it is off screen or the tab is hidden. The numbers are set by measurement, not chosen in advance.
- **No cost before it is wanted:** on a production build, the page's first paint, largest paint and layout shift are no worse than today; the Home page, and a visit that only ever shows the still planet, download none of the planet's code.
- **Everyone gets something good:** with reduced motion, without WebGL, or after the graphics context is lost, the visitor sees the still planet; touch scrolling works over the planet; every control and card works from the keyboard and says what it is and what state it is in.
- **Clean:** nothing of the mock-up's scaffolding is in the App; the engine is in modules, none over 1,200 lines; the engine passes the App's own type and lint checks; everything the planet creates is released when the page is left, and its resource counts are the same after ten visits as after one.
- **Held:** the page's pictures are taken at fixed settings on every change to the page or the planet; its existing checks of the headline, the sky, the phone layout and the two section links pass with their assertions unchanged; the page's address and its social preview are as before.
- **Limits of the proof:** frame rates measured in CI's headless browser stand in for real devices; the owner's own look on her phone and laptop is part of the proof and is recorded. Landing and publishing remain the owner's.
