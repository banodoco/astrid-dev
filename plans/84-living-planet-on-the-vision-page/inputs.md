# Inputs — A living planet on the vision page

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — The owner asked for this plan on 22 November 2026 in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), pointing at [banodoco/planet](https://github.com/banodoco/planet): "I basically want to add like a project for both building this and adding it to ... the vision page, you know, so it should be in the top, the right corner, replacing it"; "there should be like a new ... container ... that captures both the principles and the pillars ... and that basically the planet then goes behind, and it should be behind that but transparent"; "we have basically built this out already, but obviously the plan should encapsulate building it"; "make sure that it kind of like works really nicely, make sure that it performs well ... looks nice on all the different devices, has like a nice kind of intro animation, and a few other like little details"; "this should be part of release 15 as well".

**Prior art:** Two read-only studies on 22 November 2026: [the mock-up](evidence/research-planet-mock-up.txt), read at banodoco/planet [`037293dedf932cd12eb7ef2568017b9196b76c32`](https://github.com/banodoco/planet/tree/037293dedf932cd12eb7ef2568017b9196b76c32), and [the page and the way of working](evidence/research-vision-page-and-manager-route.txt), read at astrid-app `release/15/main`. The closest earlier work is [Plan 21](../21-astrid-website/plan.md), the website.

- **The mock-up** ([research-planet-mock-up.txt](evidence/research-planet-mock-up.txt), read at banodoco/planet [`037293de`](https://github.com/banodoco/planet/tree/037293dedf932cd12eb7ef2568017b9196b76c32) and built once): one engine function in one 8,996-line file; one three.js scene with 22 named places, four reached by the story cards; 979 kB of JavaScript, 266 kB compressed; resolution capped at twice the screen's, 2,048-pixel shadows; the drawing loop keeps scheduling when the tab is hidden and does not stop off screen; unmounting does not release the scene's geometry, materials and textures; reduced motion slows it, does not stop it; touch on the planet blocks scrolling; a placeholder fades out on the first frame and there is no authored entrance; if WebGL fails the placeholder stays; five of its dependencies are never imported.
- **The page and the way of working** ([research-vision-page-and-manager-route.txt](evidence/research-vision-page-and-manager-route.txt), read at astrid-app `release/15/main`): the page is `src/pages/Home/PublicAstridVision.tsx` at `/vision`, React and Vite; its text comes from astrid-dev's published feed, its layout is the App's; the hero's illustration is `<Juggler />`; below 760 px the hero is one column and the illustration is hidden; the `vision-content` checks include pictures of the hero, Pillars and Principles; three.js is already an App dependency; no size, speed or frame-rate check guards the page today.

**Approach:** Where the engine lives.

| Option | For | Against |
| --- | --- | --- |
| In astrid-app, beside the page, loaded on demand (chosen) | One repository, one release, the page's own tests cover it; three.js already there | An 8,996-line file arrives in the App unless PL-10 splits it |
| Its own package, published from banodoco/planet | The engine can be reused elsewhere | A second release to coordinate for one consumer; the Release 15 branch table does not admit that repository |
| An embedded frame pointing at a separately hosted planet | No App change to the engine | A transparent planet behind the page's own content cannot be done across a frame |

**Challenge:** Reviewed — the owner asked on 22 November 2026 for "Astra to sense check this plan ... in accordance with the ... planning skill". An independent Codex critic (`gpt-6.2-astra`, high effort, read-only, no part in the draft) was commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) the same day, briefed as the [planning skill](../../skills/roles/astrid-dev-plan/SKILL.md) asks: to build as little as possible and to check the plan against the code. Its report is [critique.txt](evidence/critique.txt). It did not measure real devices or production transfer. The owner has asked that such critiques be weighed, not adopted wholesale; what the planner did with each finding:

- **Accepted — a pillar card already does something.** Choosing one opens its goals, gaps and projects (`PublicAstridVision.tsx` near 605–607); the mock-up's click turns the planet and scrolls away. The draft's "cards move the world" is removed: a click keeps its meaning, and a turn on hover is a taste detail in PL-7.
- **Partly accepted — the name.** Both headings and both links stay, and a test pins the links, so the panel gets no navigation entry. The owner then asked the Lead to choose its name; it is Foundations (see Owner decisions).
- **Accepted — one three.js, its own canvas.** The App has 0.185.1 and the mock-up targets 0.187; the engine is ported to the App's, and kept apart from the editor's canvas. The engine must pass the App's type and lint checks.
- **Overruled by the owner — the split.** The critic would cut it: the App's large-file list is advisory and Plan 13's guard covers the Agent's execution code only. Shown the plan, the owner said: "I think we should break up the planet as well." It is PL-9. The critic's point about its proof stands and is taken: pictures in a fixed pose compared within a tolerance, not pixel for pixel.
- **Accepted — loading on demand has to be proved on a production build:** that the Home page and a still-only visit fetch none of the planet's code, and that first paint, largest paint and layout shift are no worse. The mock-up's 266 kB is the whole demo, not the planet's share.
- **Accepted — there are no screenshot baselines.** The capture test writes pictures and compares them with nothing, and the workflow does not run when only the planet changes. PL-6 now extends the path filter and pins the capture settings; no baseline is "approved".
- **Accepted — the owner looks last, at the final commit.** The draft put her preview before the taste rounds. It is now PL-8, after them, on her own phone and laptop.
- **Accepted — merge and reuse.** Layout, panel and devices are one task and the still planet and the intro are one; the sky's 1.8-second reveal, the 760-pixel point, the reduced-motion rules and the loading text are reused; the three existing tests the layout touches are named. Building is routed `N` or `X` and only refinement `T`.
- **Accepted — proofs that would not have worked.** Pixel-identical pictures (the mink use randomness and the clock, and software drawing changes shadows), "zero graphics memory" from the renderer's counters, and frame rates in a headless browser are replaced by a fixed pose with a tolerance, released resources and stable counts, a fake scheduler for the off-screen stop, and named hardware. Quality stepping is built only if measurement asks for it.
- **Accepted — provenance.** The mock-up has no licence and was made in a generating tool. D1 now asks the owner to say it is hers to publish.
- **Accepted — the page's address, social preview and a failed download** of the planet's code are covered (PL-4, PL-6).
- **Partly accepted — a pre-rendered loop instead of a live planet.** The critic proposed comparing a transparent video of the planet with live drawing before bringing the engine in. The owner built a live planet and asked for it to perform well, so the live planet stays the default; the trial in PL-0 decides what a phone gets, which may be the still or a lighter planet.
- **The estimate:** the critic called 12 days optimistic for the proofs and high for a narrower backdrop. With the tasks merged and the split kept it comes to 14.5, and PL-0 re-states it.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: taste is judged by the manager and the owner, and is recorded as pictures and a written verdict, not as a number; frame rates in a headless browser stand in for real devices.

**Review rounds:** Recommended: up to three taste rounds by the manager (PL-7), the owner's look at the finished page (PL-8), and one independent review round of the code, tests and measurements at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go. **Recommended to whoever starts it:** manager duties on the taste route `T`, as the [Orchestrate role](../../skills/roles/astrid-dev-orchestrate/SKILL.md) lets a run choose; the owner asked for "a very taste-based executor who's farming stuff out and then ... iterating on it ... acting as the tastemaker and judge". Workers on `N` for building and for taking pictures, `X` where a card says so. The final reviewer is independent of the manager.

## Owner decisions

- **Taste is delegated, with the owner's look at the end.** By her instruction above, the manager decides how it looks and feels: what a phone shows, which of the mock-up's controls ship, the timing of the intro, the tint of the panel. She sees the finished page in PL-8 and may overrule any of it. These are not listed as separate decisions.
- **The engine is split in this plan.** Decided 22 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "I think we should break up the planet as well." It is PL-9.
- **The combined panel is called Foundations.** She asked the Lead to choose: "you can figure out the name for the combined thing." Pillars are what is being built and principles are how; both are what the rest stands on. The name is used in the code, in this plan and as the panel's label for screen readers; it adds no navigation entry and changes neither section's heading. Whether it is also shown on the page is the manager's call, and she may change the name at her look in PL-8.
- **D1 — the mock-up is hers to publish.** banodoco/planet has no licence file and was made with a generating tool. Before its code and art land in astrid-app and go on a public page, the owner states that they are hers to publish there. Recommendation: one line from her, recorded here. Needed before landing, not before the trial or the build. Pending.

## Source identities

No code work has started. Read on 22 November 2026: banodoco/planet at `037293dedf932cd12eb7ef2568017b9196b76c32` (the mock-up; nothing lands there); astrid-app `release/15/main` at `c5ba8cd92d8cf83b5f641bbffb61add42a5dad1b`. At run start record the plan branch `release/15/plan-84` in astrid-app and the commit it was cut at.

## References

- [banodoco/planet](https://github.com/banodoco/planet): the mock-up.
- [Plan 21](../21-astrid-website/plan.md): the website, the closest precedent for work judged by pictures.
- [Plan 53](../53-vision-aspirations/plan.md): changes the vision's text and feed in the same release; no shared files.
- [Routing and bindings](../../skills/shared/run-contract.md#routing-and-bindings): the taste route.
