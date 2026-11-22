# Inputs — A living planet on the vision page

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — The owner asked for this plan on 22 November 2026 in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), pointing at [banodoco/planet](https://github.com/banodoco/planet): "I basically want to add like a project for both building this and adding it to ... the vision page, you know, so it should be in the top, the right corner, replacing it"; "there should be like a new ... container ... that captures both the principles and the pillars ... and that basically the planet then goes behind, and it should be behind that but transparent"; "we have basically built this out already, but obviously the plan should encapsulate building it"; "make sure that it kind of like works really nicely, make sure that it performs well ... looks nice on all the different devices, has like a nice kind of intro animation, and a few other like little details"; "this should be part of release 15 as well".

**Prior art:** Two read-only studies on 22 November 2026, kept in [evidence/](evidence/).

- **The mock-up** ([research-planet-mock-up.txt](evidence/research-planet-mock-up.txt), read at banodoco/planet [`037293de`](https://github.com/banodoco/planet/tree/037293dedf932cd12eb7ef2568017b9196b76c32) and built once): one engine function in one 8,996-line file; one three.js scene with 22 named places, four reached by the story cards; 979 kB of JavaScript, 266 kB compressed; resolution capped at twice the screen's, 2,048-pixel shadows; the drawing loop keeps scheduling when the tab is hidden and does not stop off screen; unmounting does not release the scene's geometry, materials and textures; reduced motion slows it, does not stop it; touch on the planet blocks scrolling; a placeholder fades out on the first frame and there is no authored entrance; if WebGL fails the placeholder stays; five of its dependencies are never imported.
- **The page and the way of working** ([research-vision-page-and-manager-route.txt](evidence/research-vision-page-and-manager-route.txt), read at astrid-app `release/15/main`): the page is `src/pages/Home/PublicAstridVision.tsx` at `/vision`, React and Vite; its text comes from astrid-dev's published feed, its layout is the App's; the hero's illustration is `<Juggler />`; below 760 px the hero is one column and the illustration is hidden; the `vision-content` checks include pictures of the hero, Pillars and Principles; three.js is already an App dependency; no size, speed or frame-rate check guards the page today.

**Approach:** Where the engine lives.

| Option | For | Against |
| --- | --- | --- |
| In astrid-app, beside the page, loaded on demand (chosen) | One repository, one release, the page's own tests cover it; three.js already there | An 8,996-line file arrives in the App unless PL-10 splits it |
| Its own package, published from banodoco/planet | The engine can be reused elsewhere | A second release to coordinate for one consumer; the Release 15 branch table does not admit that repository |
| An embedded frame pointing at a separately hosted planet | No App change to the engine | A transparent planet behind the page's own content cannot be done across a frame |

**Challenge:** Pending — an independent critique of this plan is commissioned from the Release 15 Lead session and its result is added here before a run starts. Next: the critic's report, and what the planner did with each finding.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: taste is judged by the manager and the owner, and is recorded as pictures and a written verdict, not as a number; frame rates in a headless browser stand in for real devices.

**Review rounds:** Recommended: up to three taste rounds by the manager (PL-9), the owner's look at a preview (PL-8), and one independent review round of the code, tests and budgets at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go. **Recommended to whoever starts it:** manager duties on the taste route `T`, as the [Orchestrate role](../../skills/roles/astrid-dev-orchestrate/SKILL.md) lets a run choose; the owner asked for "a very taste-based executor who's farming stuff out and then ... iterating on it ... acting as the tastemaker and judge". Workers on `N` for building and for taking pictures, `X` where a card says so. The final reviewer is independent of the manager.

## Owner decisions

- **Taste is delegated, with the owner's look at the end.** By her instruction above, the manager decides how it looks and feels: what a phone shows, which of the mock-up's controls ship, the timing of the intro, the tint of the panel. She sees a preview in PL-8 and may overrule any of it. These are not listed as separate decisions.
- **D1 — what the combined panel is called.** It holds the Pillars and the Principles. (a) No new name: one panel, the two existing headings and navigation entries kept. (b) A new name over both, which also changes the navigation. Recommendation: (a), because the navigation and the content feed stay as they are. Pending.
- **D2 — the engine in modules, now or later.** The engine is one 8,996-line file. (a) Split it in this plan (PL-10, about 2 days), proved by identical pictures. (b) Bring it in whole and split it in a later plan. Recommendation: (a): Release 15 is spending Plan 13 on a file that grew this way, and the split is cheapest while the pictures that prove it are fresh. Pending.

## Source identities

No code work has started. Read on 22 November 2026: banodoco/planet at `037293dedf932cd12eb7ef2568017b9196b76c32` (the mock-up; nothing lands there); astrid-app `release/15/main` at `c5ba8cd92d8cf83b5f641bbffb61add42a5dad1b`. At run start record the plan branch `release/15/plan-84` in astrid-app and the commit it was cut at.

## References

- [banodoco/planet](https://github.com/banodoco/planet): the mock-up.
- [Plan 21](../21-astrid-website/plan.md): the website, the closest precedent for work judged by pictures.
- [Plan 53](../53-vision-aspirations/plan.md): changes the vision's text and feed in the same release; no shared files.
- [Routing and bindings](../../skills/shared/run-contract.md#routing-and-bindings): the taste route.
