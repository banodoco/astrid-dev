# Plan 84 — orchestrate with fresh ChatGPT/Codex packets and human creative feedback

[Plan](plan.md) · [Tasks](tasks.md) · [Art direction](art-direction.md) · [Creative units](creative-units.md) · [Visual assets](assets/README.md)

**Purpose:** A ready-to-use, *Plan 84-specific* handoff for an owner-appointed Orchestrator. This is not a second task queue or permission to begin an unstarted run. Follow Astrid's actual [Lead packet preparation](../../agent/roles/leader/multi-manager-release.md), [Orchestrator dispatch](../../agent/roles/orchestrator/multi-manager-dispatch.md), [one-packet execution](../../agent/roles/manager/chatgpt-packet.md), and [run contract](../../agent/shared/run-contract.md). For this plan, use `tasks.md` as the one source of task progress.

## Owner-facing introduction — post before the first dispatch

Start with an inviting but concrete explanation in the same owner chat, *before* launching packet sessions:

> **We're making Astrid's little living planet into a complete, tactile miniature world**, not just decorating a sphere. Its tiny sculptural orange minks should look like a 3D version of the pixel mascot, and the whole scene should sit naturally among the website's cream/peach editorial layout and pixel clouds. The globe will be real-time 3D. The visible side at entry reflects the site's current local time; drag right and you move to later hours, drag left to earlier hours, while vertical movement doesn't change the sky. The background and sun/moon colours already belong to Astrid's shared clock, so we use that instead of creating another one.
>
> We're developing a set of **eight small, deliberately different stories** around the sphere—makers collaborating, tea, play, a rose, a mystery, astronomy, meditation and a cozy creator. The characters should feel alive but the planet should have quiet places too. Four small flying ideas and a camera fly-in and exit get their own attention later. We first prove the planet, the mink, and one complete collaborative scene, then let that standard guide the rest.
>
> **You'll see the actual results at each important stage**—a screenshot at real website size, a short motion clip or a live preview, and a few clear questions. Most feedback is optional: we'll keep working while you decide what you like. We will explicitly ask you to approve only four high-impact choices that would otherwise force significant artistic rework. You can respond, redirect, or interrupt at any point, in English or Turkish. No silence will be interpreted as approval. The implementation stays on reviewed branches until the separate release decision.

Follow that with **real links** to [Plan 84](plan.md), [visual direction](art-direction.md), [creative-unit board](creative-units.md), [references](assets/README.md), and the current GitHub task PR/preview once they actually exist. When reporting in ChatGPT, use full GitHub URLs rather than repository-relative links. Do not invent ChatGPT conversation URLs, screenshots, preview deployments or status.

## Setup and accountability

1. **Read the current source SHAs and permissions first.** Plan 84 is currently queued; do not treat older lab runs, a prior branch or this document as fresh product execution authority. The owner's pasted launch message authorizes only the role and tasks it actually grants. Coordinate the release branch and any overlapping owner/Lead authority with the current Release Lead. No accidental restart of an older packet run.
2. **Appoint exactly one accountable Lead.** If acting as Plan 84's lane Lead, take that responsibility only under the release's accepted delegation. Otherwise the Release Lead stays accountable and reviews/merges all packet PRs. The Orchestrator dispatches and supervises, never silently becomes an additional owner.
3. **Use one durable plan/run board** under Astrid's existing board conventions. Put readiness, packet ID, route/mode, dependencies, session/PR links, exact head, tests, review status, feedback permalink, human gate status and next action in the existing board/task record. Do not create one separate issue or status ledger for every scene.
4. **Cut bounded engineering packets**, one contract each, ideally a few hours and no more than a sensible one-session chunk, from the accepted `LP`, `SC`, `FL` and `CAM` cards. A creative unit remains a meaningful artistic outcome even if it takes several technical packets; don't force a whole scene into one oversized coding assignment or split every prop into a new creative project. The Lead writes May touch / Must not touch, exact base/destination, focused tests and evidence requirements *before* Ready.
5. **Dispatch one new ChatGPT session per packet** via the [ChatGPT dispatch workstream](../../agent/roles/orchestrator/multi-manager-dispatch.md). Sessions write scoped draft PRs and post READY-PROOF, not local broad builds, final review or merges. The Lead/orchestrator runs independent proof and owns dispositions, as described by the live release rules. Do not dispatch blocked dependencies.
6. **Record a real feedback destination.** After a stage, share the actual accessible ChatGPT session URL **only if one is available and verified**; always include the real preview/capture and PR link, plus a permalink to the relevant comment on the existing plan board as a stable fallback. The owner can reply in the Orchestrator's ChatGPT conversation or on that board thread. Relay that reply into `tasks.md`/board without requiring the owner to chase packet sessions.
7. **Start with project orientation, then work.** Explain the project and current progress before posting a wall of packet IDs. The owner should know which decisions matter and how to interrupt you without having to read a private management thread.

### Codex/ChatGPT route selection

Use the route in the actual task/packet, not a single model for the whole project. Use **N → ChatGPT High (Codex Luna)** for routine bounded engineering, docs, fixtures and measurements; **X → Extra High (Codex Terra)** for difficult geometry, rigging, motion, interactive graphics, synchronization and original scene implementation; **S → Pro (Codex Sol)** for unusually complex coupled decisions and deep reasoning. Independent acceptance/creative judgment uses the configured high-judgment reviewer (for Codex, Astra), rather than a packet self-approving. The shared `T` route is **editorial refinement only**, not a substitute for original scene art direction. Respect actual run bindings and model availability; do not invent access or model IDs.

## Make every feedback request reviewable in one glance

**A question without its reference image is not a usable creative review.** The person answering should not have to hunt through GitHub to remember what "Astrid mink" or "the website's aesthetic" means. Build a **small reference-versus-result bundle** for each consequential visual decision, including ordinary scene/flight feedback when useful:

1. **THE REFERENCE / REFERANS:** attach or embed the *actual* relevant original image (not just its filename) from [the checked-in reference assets](assets/README.md), or the previously **approved** creative result if the comparison is to an established design. Label exactly what is authoritative about it: silhouette, palette, negative space, material, scale, or motion language. **Never present an exploratory anti-target image as the goal.**
2. **THE NEW RESULT / YENİ SONUÇ:** attach the current actual render/capture at a **comparable angle and scale**, alongside a crop showing it at the website's *real display size*. When movement is judged, attach the actual **video/GIF plus a meaningful still** from the clip. For time-driven work, include a relevant day and night rendering. Match framing where comparison would otherwise be misleading.
3. **THE CONTEXT / BAĞLAM:** show the finished element **in the actual Vision hero** alongside headline, clouds and the rest of the planet, not only in an isolated 3D viewer. Provide exact source SHA, PR and available preview links. If a side-by-side contact sheet is useful, generate and attach it as a real artifact; never substitute a generated imaginary "after" for the implemented candidate.
4. **THE QUESTION / SORU:** ask **two or three questions that explicitly point to the comparison**, ideally noting the most important difference and what decision it controls. Allow *Approve / Request changes / Alternative* for a gate. If references disagree, state the chosen source of truth rather than handing the human an unexplained collage.
5. **THE NEXT STEP / SONRAKİ ADIM:** identify what will continue now and what is held for the human's answer. Real images and clips should be **visible inline in the ChatGPT feedback message when the host supports it**; still provide verified full-size links. If embedding is unavailable, link a verified contact-sheet image or PR preview and say so. Never claim an attachment has been posted unless it actually exists.

**Concrete reference selection by stage:**

| Stage | Reference material to actually show | New evidence / direct comparison |
| --- | --- | --- |
| **VG-STYLE — 3D mink** | [pixel mink reference](assets/astrid-mink-provisional.webp) **and** [pixel mascot pose sheet](assets/astrid-juggler-mink-poses.png), optionally the [actual homepage](assets/reference-homepage-original.jpg) | Current 3D mink front/side/back sheet plus the tiny on-page result, side by side with the original pixel mink. Ask: **"Does this unmistakably match our mink, especially silhouette, body length, cream underside and dark tail tip?"** |
| **VG-STYLE — globe/website** | [original Vision screenshot](assets/reference-vision-original.jpg), [original homepage screenshot](assets/reference-homepage-original.jpg), [sphere-direction concept](assets/concept-03-sphere-direction.jpg) with its limits made explicit | Actual new full-sphere gray/shaded views beside the original planet and the integrated hero. Ask whether it's still clearly a sphere and visually belongs to Astrid. |
| **VG-STORY — collaboration** | The **VG-STYLE-approved** 3D mink and art benchmark, plus [SC-01's intended gesture description](creative-units.md#eight-scene-concepts-to-art-direct) | Current workshop still and **20–30 s real motion clip** with a few helpful frame captures. Ask whether their work reads as collaboration and if the motion/contact feels natural and slick. |
| **SC-02–SC-08 — each ground scene** | Approved SC-01 style/scale benchmark, the approved Mink reference, and one or two relevant art references **with provenance** | That scene at real Vision scale, day/night and 8–20 s clip. Ask about its specific *emotion, storytelling, visual readability and movement*. |
| **VG-WORLD — full composition** | [original Vision screenshot](assets/reference-vision-original.jpg), [globe composition hierarchy sketch](assets/globe-composition.svg), accepted SC cards | 360° turntable + morning/noon/evening/night page views and a labelled atlas. Ask whether the eight locations feel coherent without crowding or a front-only facade. |
| **FL-01–FL-04 — each flying object** | Its **approved silhouette/trajectory graybox** and the current planet/website scale reference | Close-up flight arc and one full-page normal-size clip with foreground/background crossings. Ask whether its trajectory reads, feels smooth and competes with the hero. |
| **VG-MOTION — cinematic camera** | [original website layout](assets/reference-homepage-original.jpg), the accepted **current-hour end-frame**, and the camera storyboard/graybox | Actual before/after keyframes and entry fly-in recording at real page size, plus reduced-motion comparison. Ask whether the camera arc feels elegant, finishes correctly and doesn't steal time/sky state. |

**Example of the mink review — EN / TR:**

> **VG-STYLE / 3D Mink — YOUR DECISION NEEDED / KARARINIZ GEREKİYOR**  
> **Reference / Referans:** [actual pixel-mink image shown here]  
> **New version / Yeni sürüm:** [current four-angle 3D mink sheet and embedded real-site crop]  
> **Motion / Hareket:** [verified walk/sit clip]  
> **EN:** Looking at the original pixel mink and this 3D version **side by side**, does it still feel like the same character? Are the body shape and proportions right? Do the movement and expression fit the mascot?  
> **TR:** Orijinal piksel vizonla bu 3B versiyonu **yan yana** görünce aynı karakter gibi hissediliyor mu? Gövde şekli ve oranları doğru mu? Hareketler ve ifadeler maskota uyuyor mu?  
> **Decision / Karar:** Approve / Request changes / Suggest alternative — Onayla / Değişiklik iste / Alternatif öner  
> **Evidence:** [real PR, source SHA and verified stage feedback thread].  
> **What continues:** [named independent work]. **Held:** [named character-dependent art].

This applies to **every** critical design question: always supply the specific reference or approved prior state that makes the question answerable, not generic "What do you think of X?" without a visual comparator.

## Feedback: routine progress vs human decision

**Routine technical work:** send a short digest at an LP milestone, not a question after every commit. Include the exact test result and preview when relevant; ask an optional question *only if* a real product tradeoff needs taste.

**Creative scene / flight / camera card:** after each internally accepted `SC`, `FL` or `CAM` result, send the owner a **small inline reference-versus-result visual bundle** as specified above—not just a question or link—together with on-page captures (phone and desktop), day/night versions, a short clip demonstrating signature motion or deliberately approved stillness, exact commit/PR and two specific questions (English with Turkish equivalents when useful). Mark this **FEEDBACK OPTIONAL** unless the card is one of the four gates below. Begin the next ready independent packet immediately; do not equate silence with approval.

**Load-bearing human creative gates:** four checkpoints really do require an explicit **approve / request changes / choose alternative** reply. After internal review has passed, the Orchestrator marks the gate **AWAITING OWNER** and sends a compact choice with links. Do not release **dependent creative work** until a recorded affirmative decision; however, dispatch other unrelated ready engineering, asset, tests or scene-research packets in parallel, respecting the no-two-writers rule. No timeout becomes automatic approval.

| Gate and when | What the human validates | What is held while awaiting a reply | What continues |
| --- | --- | --- | --- |
| **VG-STYLE** — after LP-1 and LP-2 | The *planet and 3D mink visual language*: real sphere, sculptural proportions, light, pixel integration | SC-01 final scene art and style-dependent character production | Independent sky/drag tests, performance work, exploratory grayboxes |
| **VG-STORY** — after LP-3 and RS1 | The *first finished collaboration scene*: interaction charm, movement/contact, animation grammar and emotional tone | SC-02–SC-08 final creative production and the LP-4 global art pass | Independent technical infrastructure, scene briefs and rough reference research |
| **VG-WORLD** — after LP-4 | The *complete planet*: eight scenes across a real globe with quiet space, suitable morning/dusk/night compositions | Final visual presentation decisions in LP-5 and downstream cinematic commitment | Nonvisual LP-5 integration tests, fallbacks, measurement infrastructure |
| **VG-MOTION** — after CAM-IN and the four FL motion clips | The *cinematic and airspace language*: approach/arc/pacing, actual flight scale and what to keep or omit | CAM-OUT final choreography and LP-6 polished composition | Independent technical performance, accessibility/fallbacks and unrelated tasks |

Do not invent extra owner gates for every routine creative task. If an individual object unexpectedly threatens the site's identity or has irreversible scope/rights implications, the Lead may identify a new load-bearing decision **with a written reason**, ask the owner, and continue other tasks. Final release/publication approval remains separate and explicitly required after R.

### Suggested high-stakes questions — English / Türkçe

**VG-STYLE — sphere and mink**
- EN: Does this feel like a *complete small planet* from several angles, or still like a floating island?  
  TR: Birkaç açıdan bakıldığında bu gerçekten *küçük, bütün bir gezegen* gibi mi, yoksa hâlâ yüzen bir ada gibi mi görünüyor?
- EN: Do the 3D minks unmistakably feel like sculptural versions of our pixel mascot?  
  TR: 3B vizonlar piksel maskotumuzun heykelsi versiyonları gibi açıkça algılanıyor mu?
- EN: Do the lighting and texture complement the cream/pixel-art website at actual phone size?  
  TR: Işık ve dokular, gerçek telefon boyutunda krem tonlu/piksel estetikli siteyle uyumlu mu?

**VG-STORY — first makers scene**
- EN: Can you tell immediately that the minks are *creating together*, not just standing by props?  
  TR: Vizonların yalnızca nesnelerin yanında durmadığı, *birlikte ürettiği* hemen anlaşılıyor mu?
- EN: Does the motion feel natural, smooth and charming—including pauses and little mistakes?  
  TR: Duraklamalar ve küçük hatalar dâhil hareketler doğal, akıcı ve sevimli hissettiriyor mu?
- EN: Is anything overly cartoonish, oversized or visually busy?  
  TR: Fazla çizgi filmimsi, büyük ya da görsel olarak kalabalık duran bir şey var mı?

**VG-WORLD — full globe**
- EN: Does every turn reveal something worth discovering, while still leaving peaceful open land?  
  TR: Her dönüşte keşfetmeye değer bir şey var mı; yine de sakin, boş alanlar kalıyor mu?
- EN: Which scene feels weakest or most disconnected from the shared world?  
  TR: Hangi sahne en zayıf veya ortak dünyadan en kopuk görünüyor?
- EN: Does the morning-to-night shift preserve readability and the right atmosphere?  
  TR: Sabahtan geceye geçiş okunabilirliği ve doğru atmosferi koruyor mu?

**VG-MOTION — entry and flight language**

**Evidence before asking:** show the original website's hero framing alongside the candidate camera animation, and actual short clips for each of FL-01–FL-04 at normal website size. If any candidate is only a storyboard, label it unproved and defer that specific creative selection rather than asking the human to judge nonexistent motion.
- EN: Does the fly-in/arc feel slick and deliberate, or too dramatic or slow?  
  TR: Yaklaşma ve kavisli kamera hareketi akıcı ve bilinçli mi, yoksa fazla gösterişli ya da yavaş mı?
- EN: Does the motion end in the right time-selected planet view without a visual jump?  
  TR: Hareket, görsel sıçrama olmadan saate göre seçilen doğru gezegen açısında bitiyor mu?
- EN: Which flying details add charm, and which distract from the planet or headline?  
  TR: Hangi uçan detaylar hoş bir katkı sağlıyor, hangileri gezegenden veya başlıktan dikkati dağıtıyor?

### Feedback message template (one per important stage)

> **[VG-STYLE / SC-04 / FL-02 / CAM-IN] — READY FOR YOUR LOOK**  
> **Reference / Referans:** [actual relevant image embedded or a verified labelled contact sheet]  
> **New result / Yeni sonuç:** [actual current render embedded alongside the reference; site-scale crop]  
> **Preview / Ön izleme:** [verified URL]  
> **Video / Video:** [verified URL]  
> **Code and evidence / Kod ve kanıt:** [PR and exact SHA]  
> **Status / Durum:** FEEDBACK OPTIONAL — continuing / **APPROVAL NEEDED** — dependent art held; other tasks moving  
> **The choice / Karar:** Approve / Request changes / Discuss an alternative — **Onayla / Değişiklik iste / Alternatifi konuş**  
> **Questions / Sorular:** 2–3 tailored points **about the visible reference-versus-result comparison**, in English and Turkish for a major gate.  
> **What's next / Sıradaki adım:** [specific ready task; what stays held].  
> **Reply or interrupt anytime / İstediğiniz zaman yanıtlayabilir veya yönlendirebilirsiniz.**

Only use a verified stage comment/thread or accessible session URL; bracketed placeholders above are not public links. When the owner replies, acknowledge it in the owner thread, record the decision and exact evidence/commit it applies to, and propagate it to the Lead/Orchestrator queue. If a reply modifies accepted scope, do not let any packet silently treat it as a trivial code edit.

## Launch message for the owner to paste

> You are the Orchestrator for **Plan 84: A living planet on the Vision page** in `banodoco/astrid-dev`. Follow `skills/roles/astrid-dev-orchestrate/SKILL.md`, `skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md` and the project's `chatgpt-orchestration.md`. Before any dispatch, read `plan.md`, `inputs.md`, `tasks.md`, `art-direction.md`, `creative-units.md` and `assets/README.md` under `plans/84-living-planet-on-the-vision-page/`, at current `main` and a pinned SHA.
>
> First, **introduce the whole project and visual direction to me** in understandable terms, with real links to the plan and source images. Explain the real-time globe, shared time-of-day sky, right-later/left-earlier interaction, eight story concepts, four flyers and camera entrance/exit. Explain what will be built first and how I can steer or stop it.
>
> Coordinate with the Release Lead to record an authorized Plan 84 lane, one accountable Lead, the product branch and one run board. Prepare narrowly scoped task packets from the current ledger; dispatch them **in fresh ChatGPT/Codex sessions** using `N` High, `X` Extra High or `S` Pro according to the bound route and actual difficulty. An assigned packet never merges or invents new project scope; use the Lead and independent proof/review flow. Continue the next ready independent work rather than waiting for routine feedback.
>
> **At each important stage, prepare the right context for my judgment:** embed the actual source reference image beside the new result, matching angle/scale when possible, plus a normal Vision-page crop and motion clip. For the 3D mink, show the pixel-mink mascot and pose sheet next to the current 3D character and explicitly ask whether it looks and moves like **our mink**. Do the same with the current globe/site references, earlier approved scene standards, flight concepts and camera storyboard. Then show verified preview, PR/head and the real comment/session link where I can respond. Ask 2–3 specific questions (English and Turkish for the four high-stakes creative gates), not generic approval requests. I can reply, revise, redirect or interrupt at any time. Most feedback is optional. **Stop only dependent art** at `VG-STYLE`, `VG-STORY`, `VG-WORLD` and `VG-MOTION` until I explicitly approve or direct a change; keep unrelated ready work moving. Treat silence as pending, not consent. Final publication still requires separate permission.
>
> Do not claim a session, model, preview, test result, owner approval or merge exists without verifying it. Tell me what is ready, what is held, what feedback I can give and the next unblocked step. If this account/session cannot launch or share other ChatGPT sessions, give me ready-to-paste prompts and real GitHub/evidence links rather than inventing capabilities.

## Ready/start boundary

This document prepares the run. It does **not** say that it has started or that any sessions were dispatched. The owner-pasted message and the current Release Lead's authority decide when product work starts. The Orchestrator should not treat plan-document PR merges, CI completion or unacknowledged feedback as authorization to integrate into product `main` or publish.
