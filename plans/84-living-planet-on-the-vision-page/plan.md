# A living planet on the vision page

**Project:** A living planet on the vision page

**Goal:** The public vision page opens on a convincing, fully spherical, inhabited Astrid planet, with small expressive 3D pixel-identity minks and discoverable stories; it replaces the hero's juggling mink, continues behind the Foundations panel, and arrives with an authored intro, accessible fallbacks and measured performance on every device.

**Status:** active

**Owner:** the AI Studio run's manager, a Codex session the owner starts with the start message in [ai-studio-run.md](ai-studio-run.md#manager-start-message); the session is named on that board

**Estimate:** About 27 engineering days from 23 November 2026: about 23 one-day packets in AI Studio (the engine split, what the page needs from the engine, then the page itself), plus 4 days to import it into astrid-app and prove it there, with reflection and the owner's daily looks alongside. It is re-stated at the run's RF-0 and RF-A rows from what the first packets actually take.

**Waiting on:** the owner to send the manager start message; the first packet is EX-00. The work now runs in Google AI Studio in the planet lab (banodoco/planet) and is imported into astrid-app at the end; the queue, roles and authority are in [ai-studio-run.md](ai-studio-run.md). Run 1 (PL-0, PL-1 and most of PL-2) is in [tasks.md](tasks.md#run-1-stopped--22-november-2026).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-003 — Our vision and execution aren't yet fully connected](../../vision/gaps/CA-003-vision-experiments-progress.md) (primary): the vision page is where a newcomer first meets what Astrid is for, and the planet shows the pillars as places they can visit, not a list to read. CA-003's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

The vision page today (astrid-app `src/pages/Home/PublicAstridVision.tsx`, served at `/vision`) has a hero with a pixel-art mink juggling at the right, then a Pillars section of cards ("What we're building"), then a Principles section. The owner built the [banodoco/planet](https://github.com/banodoco/planet) mock-up as the **engineering baseline**. Its engine and overall hero composition are reused, but its appearance is not the approved art target: the owner-selected [production brief](art-direction.md) and [assets](assets/README.md) now govern the look and inhabitants. Pillar cards retain their existing click behavior.

**What a visitor gets:**

- **The planet in the hero,** top right, where the juggling mink is now.
- **One translucent panel, Foundations,** below the hero that holds both the Pillars and the Principles, with the planet visible behind it. The text stays comfortably readable over a moving background.
- **One time of day, and spinning the planet changes it.** The public pages already have a sky that follows the visitor's real time and can play through a day. The planet joins it: it arrives lit for the hour the sky shows, and when a visitor spins it the hour moves with it, so the sky behind and the page's colours change as the planet turns.
- **An intro:** the page's words appear at once; the planet then arrives in an authored entrance, with no empty box, flash or jump in the layout.
- **The same care on a phone, a tablet, a laptop and a wide screen,** by touch, mouse or keyboard.
- **A still planet, never a hole,** for a visitor who asks for reduced motion or whose device cannot draw it.

**How it is judged.** This is taste work with engineering under it. The manager is the tastemaker and judge: it farms small tasks out to workers, looks at what comes back in screenshots and short recordings at fixed sizes, and sends it back until it is right. The owner looks at a preview before it lands; her look is the final judgment.

**Not included:** changing what the vision, pillars or principles say (that text comes from astrid-dev's `vision/` folder and is not touched); changing what a pillar card does when chosen (it opens its goals, gaps and projects, as now; the mock-up's cards turn the planet instead, and whether the planet also turns toward a pillar on hover or focus is a taste detail, not a requirement); a new navigation entry for the panel (it is named Foundations, but both section headings and both links stay as they are); the Home page; sound; any use of the mock-up's unused AI-studio scaffolding.

## Art direction — owner replacement, 24 November 2026

The [complete production brief](art-direction.md) **replaces the original mock-up as the visual target**, while this existing plan, Release 15 routing, accepted technical decisions, task history and AI Studio run remain authoritative for delivery. See [locally checked-in visual references](assets/README.md). The art direction is not a request to build a new plan or publish code from the lab.

- **A planet, not a flat-topped island:** preserve a complete spherical silhouette; geometry, terrain, water, paths, props and characters follow its curvature and the far side is actually inhabited. Use a three-quarter resting pose with no mandatory automatic spin.
- **A tactile diorama at planetary scale:** sculpted low-poly/softly rounded surface, warm key light plus fill, anchored contact shadows and mild material texture. Vary prop sizes with just a few large landmarks, clustered scenes and broad quieter areas. Reject overpopulated front-facing fantasy villages and giant props.
- **Pixel mink and 3D mink are one character:** a volumetric elongated orange body, slender neck, small ears, short legs, simple face, cream underside and dark tail tip; rigged and recognizable from all directions. Apply selective authored pixel markings, not a whole-frame downsample or realistic fur.
- **Living stories with continuity:** the tea pair, running trio, solitary rose keeper, mystery-box investigator and telescope note-taker are five required scenes. Give them calm intervals, prop ownership, varied pace and coherent interrupted/resumed behavior. Roughly 12–16 residents on the *whole globe* is an initial composition, not a quota.
- **Subtle cultural references:** a collaborative maker area, a meditating elder and a cozy node-based creator desk can be discovered as small vignettes, but must not displace required scenes or visually reproduce proprietary character designs.
- **The site remains Astrid:** cream/peach page, pixel clouds, orange iconography, serif headline, clean HTML text and legible Foundations overlay. Pixel elements can drift in front of the globe, but do not render the whole sphere as voxels.

The same world must pass a gray-material 3D inspection and clean-render vs pixel-styled comparisons **before** detailed decor is approved. The [15 acceptance criteria in the production brief](art-direction.md#acceptance-criteria) add to the existing performance, accessibility and release gates. Visual acceptance requires fixed-setup desktop/phone captures, character front/side/back/elevated renders, full-globe inspection, a 30-second behavior recording and explicit owner judgment; generated concept art is not proof.

## Existing work and decision

- **The mock-up is an engineering baseline and donor of the engine, not the final visual target:** banodoco/planet at `037293de`. One function, `initPlanetEngine(canvas, callbacks)`, in one 8,996-line file, drives a single three.js scene with 22 named places; four story cards turn the planet to four of them. It builds to 979 kB of JavaScript (266 kB compressed). What it does and does not yet do is in [evidence/research-planet-mock-up.txt](evidence/research-planet-mock-up.txt).
- **The page already has a home, tests and a way of working:** the App's `vision-content` checks include screenshot captures of the hero, the Pillars and the Principles, mobile layout checks and a reduced-motion path; three.js is already one of the App's dependencies. See [evidence/research-vision-page-and-manager-route.txt](evidence/research-vision-page-and-manager-route.txt).
- **Decision (23 November 2026): the rest is built in the planet lab and imported.** banodoco/planet becomes the lab, no longer read only; see [inputs.md](inputs.md#owner-decisions). The engine still lands in the App as decided below; nothing is published from the lab.
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

**How the rest runs (from 23 November 2026):** the owner moved the remaining work to Google AI Studio. Every planet and page change is made in the planet lab, banodoco/planet, which holds astrid-app's Vision page files at their own paths and the engine from PL-1; packets of about a day are run in AI Studio by a Codex manager, each reviewed by an Astra subagent, with the owner looking once a day; the lab is then imported into astrid-app in four integration packets. The same outcome and completion cases apply; the PL tasks map onto the packets as listed in [ai-studio-run.md](ai-studio-run.md#plan-84-tasks-and-the-packets-that-deliver-them). The engine split (PL-9) now comes first, proved by a scene fingerprint test because AI Studio cannot take screenshots.

**Unresolved:** none; D1 was decided on 22 November 2026. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the mock-up's engine, the [owner production brief](art-direction.md), the [visual assets](assets/README.md), and the page's existing content feed, unchanged. **Produces:** one planet component in astrid-app that a page mounts into a container; the reworked hero and the combined panel; a still poster image of the planet; tests and budgets that hold the result. **Compatibility:** no change to the content feed, to astrid-dev's `vision/` folder or to any other page; the page's address and its navigation stay as they are.

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
