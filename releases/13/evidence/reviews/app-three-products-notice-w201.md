**The immediate cause of both publish-ref failures was an App update notice intercepting clicks.** The log supports an App UI obstruction; it does not show an Agent or Runtime error causing either timeout. Why the notice appeared in this run, and whether the R13 pin influenced its appearance, remain unknown.

The publish-ref workflow has since started **attempt 2**, with its `three-products` job in progress when checked. I did not start it. A pass on that attempt would establish pass/fail variation on the same App SHA and pins; either result alone would not establish why the notice appeared.

### Failure context

In [attempt 1, job 132825193964](https://github.com/banodoco/astrid-app/actions/runs/43718524654/job/132825193964):

- **`:417`** reached the recovered-draft alert after the Agent had published, the App had displayed the first conflict, and the test had kept the draft and reloaded. At [line 570](https://github.com/banodoco/astrid-app/blob/200e664717a016141ee41f9289982f26a88a68d2/tests/e2e/local/three-products.spec.ts#L570), Playwright resolved **Save them** and repeatedly found it visible, enabled and stable. A **button inside** `div[role="status"][data-testid="quiet-update-notice"]` intercepted pointer events. The test exceeded 300,000 ms; the subsequent reported click error said the page, context or browser had closed.
- **`:2904`** reached [line 2964](https://github.com/banodoco/astrid-app/blob/200e664717a016141ee41f9289982f26a88a68d2/tests/e2e/local/three-products.spec.ts#L2964) on both the first attempt and retry #1. **Undo** resolved and was visible, enabled and stable, but a **paragraph inside the same fixed update notice** intercepted pointer events. Its text began “This update is required: This update fixes proble…”. Both attempts hit the 300,000 ms timeout and then reported the closed-page click error.

The notice is a fixed, bottom-left status notice with a high stacking order. These are documented hit-test obstructions, rather than a missing locator or an animation inferred from the timeout.

The requested error-term search found no printed console exception, `BootManifest`, `restamp`, `HostError`, `PackHostBootstrapError`, connection, or disk-space error near the failures. The outcome-check errors follow the test failures and skipped cases. The job’s source tuple records App `200e6647`, Agent `8e0006f5`, and Runtime `6855dfa8`, with matching reported schema digests and Runtime lock values.

### Run history

The table lists the **25 latest completed runs** returned by the requested workflow query. The publish-ref run is shown separately because its second attempt was in progress when the completed-run sample was taken. Times are UTC; `D` means workflow dispatch, `S` schedule, and `P` push. P/F refer to the matching **test title**, even where its line moved between revisions. `—` means no result was logged. The final column lists distinct `✘` test lines from the job, including failures marked expected by the suite; it does not treat absent or skipped tests as passes.

| Run; date/time; event | Branch; App SHA | :417 | :2904 | `✘` lines |
|---|---|---:|---:|---|
| [43718524654, attempt 1](https://github.com/banodoco/astrid-app/actions/runs/43718524654); Nov 15 13:20; D | `r13/app-repin-8e0006f5`; `200e6647` | F | F; retry F | 417, 2904 |
| [43713841856](https://github.com/banodoco/astrid-app/actions/runs/43713841856); Nov 15 12:26; D | `int/r13-app-repin-34fee0cf`; `b22b6dc2` | P | P | 1917, 2098, 2437, 3200 |
| [43710544433](https://github.com/banodoco/astrid-app/actions/runs/43710544433); Nov 15 11:46; D | `int/r13-app-repin-f709407c`; `cf2f9535` | F | P | 417 |
| [43707235824](https://github.com/banodoco/astrid-app/actions/runs/43707235824); Nov 15 11:05; S | `main`; `ae4da5d7` | P | P | 1917, 2098, 2437, 3200, 3674 |
| [43586058785](https://github.com/banodoco/astrid-app/actions/runs/43586058785); Nov 14 10:36; S | `main`; `d6ee9af2` | P | P | 1917, 2098, 2437, 3200, 3674 |
| [43414687440](https://github.com/banodoco/astrid-app/actions/runs/43414687440); Nov 13 11:08; S | `main`; `237b28be` | P | P | 1917, 2098, 2437, 3200 |
| [43209065892](https://github.com/banodoco/astrid-app/actions/runs/43209065892); Nov 12 11:25; S | `main`; `237b28be` | P | P | 1917, 2098, 2437, 3200 |
| [43134521115](https://github.com/banodoco/astrid-app/actions/runs/43134521115); Nov 12 01:26; D | `scratch/r12-app-int`; `237b28be` | P | P | 1917, 2098, 2437, 3200 |
| [43129231012](https://github.com/banodoco/astrid-app/actions/runs/43129231012); Nov 12 00:42; D | `scratch/r12-drop-side`; `63ebc10d` | P | P | 1917, 2098, 2439, 3202, 3503 |
| [43129183431](https://github.com/banodoco/astrid-app/actions/runs/43129183431); Nov 12 00:42; D | `scratch/r12-app-int`; `824439ff` | P | P | 1917, 2098, 2437, 3200, 3674 |
| [43126783920](https://github.com/banodoco/astrid-app/actions/runs/43126783920); Nov 12 00:22; D | `scratch/r12-drop-side`; `3622b91a` | P | P | 1917, 2098, 2439, 3202, 3503 |
| [43126378875](https://github.com/banodoco/astrid-app/actions/runs/43126378875); Nov 12 00:18; D | `scratch/r12-drop-side`; `e4df8e0d` | — | — | None logged; cancelled |
| [43126122053](https://github.com/banodoco/astrid-app/actions/runs/43126122053); Nov 12 00:16; D | `scratch/r12-app-int`; `d9e2798d` | F | P | 417 |
| [43125309433](https://github.com/banodoco/astrid-app/actions/runs/43125309433); Nov 12 00:10; D | `scratch/r12-drop-side`; `05ac65ca` | F | P | 417 |
| [43123933078](https://github.com/banodoco/astrid-app/actions/runs/43123933078); Nov 11 23:59; D | `scratch/r12-app-int`; `7a971cea` | P | P | 1917, 2098, 2437, 2629 |
| [43123578817](https://github.com/banodoco/astrid-app/actions/runs/43123578817); Nov 11 23:56; D | `scratch/r12-iso`; `516f21bd` | — | — | 2607, 3367 |
| [43120357069](https://github.com/banodoco/astrid-app/actions/runs/43120357069); Nov 11 23:30; D | `scratch/r12-app-int`; `48ec9bb7` | P | P | 1917, 2098, 2522 |
| [43119630799](https://github.com/banodoco/astrid-app/actions/runs/43119630799); Nov 11 23:24; D | `scratch/r12-app-int`; `9afd4aaa` | — | — | None logged; cancelled |
| [43118115615](https://github.com/banodoco/astrid-app/actions/runs/43118115615); Nov 11 23:13; D | `scratch/r12-app-int`; `e2d48f42` | P | P | 1915, 2096 |
| [43115743810](https://github.com/banodoco/astrid-app/actions/runs/43115743810); Nov 11 22:55; D | `scratch/r12-app-int`; `2dc109bc` | P | P | 1689 |
| [43110857559](https://github.com/banodoco/astrid-app/actions/runs/43110857559); Nov 11 22:19; D | `scratch/r12-app-int`; `726655c5` | P | P | 1689 |
| [43104742119](https://github.com/banodoco/astrid-app/actions/runs/43104742119); Nov 11 21:37; D | `scratch/r12-app-int`; `61b064a9` | P | P | 1541 |
| [43099497728](https://github.com/banodoco/astrid-app/actions/runs/43099497728); Nov 11 21:01; D | `scratch/r12-t4-all`; `2172ba66` | P | P | 1489, 1602, 1818, 1989, 2221, 2404, 2467, 2649, 3184, 3483 |
| [43094106211](https://github.com/banodoco/astrid-app/actions/runs/43094106211); Nov 11 20:11; P | `scratch/r12-t4-conv`; `9c6715cf` | P | P | 1462; job cancelled |
| [43092415166](https://github.com/banodoco/astrid-app/actions/runs/43092415166); Nov 11 20:00; P | `scratch/r12-t4-all`; `2172ba66` | P | P | 610, 1489, 1602, 1818, 1989, 2221, 2404, 2467, 2649, 3184, 3483 |
| [43092408466](https://github.com/banodoco/astrid-app/actions/runs/43092408466); Nov 11 20:00; P | `scratch/r12-settings-persist`; `4551b814` | P | P | 610 |

Counting one result per run, excluding cancelled jobs and runs without a logged result, and **including publish-ref attempt 1**:

| Sample | :417 failures / observed | :2904 failures / observed |
|---|---:|---:|
| Main | 0/4 | 0/4 |
| Other branches | 4/18 ≈ 22% | 1/18 ≈ 6% |

These are small, heterogeneous samples across App revisions and pins, so they are observed failure proportions, not reliable probabilities for the publish ref. Counting :2904’s failed retry as another independent run would overstate the sample. The earlier R12 `:417` failures at `d9e2798d` and `05ac65ca` were at the later conflict-dialog visibility assertion, rather than this run’s intercepted click.

No completed sampled run shows either target passing on the **same App SHA as a target failure**. Attempt 2 of the publish-ref run is the pending same-SHA comparison.

### What the tests exercise

`:417` is a three-product integration journey. It holds an App save acknowledgement after the Runtime commits it, calls the Agent to checkout, edit and publish, then checks conflict handling and durable App draft recovery. In this failure, the Agent publication and the earlier conflict checks had already succeeded; the stuck operation was the App’s **Save them** click.

`:2904` clears a transition through the App, checks the Runtime’s accepted document and retained request, deliberately loses an acknowledgement, restarts the Runtime, reloads the App, and verifies an exact recovery retry. The stuck operation was the App’s **Undo** click after those checks; the assertions following Undo were not reached.

The most useful single rerun is therefore the **already-running attempt 2 of the same publish-ref workflow and pins**. A pass would demonstrate intermittent results on that exact SHA. If it fails, its click-interception and notice evidence should be compared with attempt 1; a repeat failure would still not by itself prove an R13 Agent regression.

GitHub access for this investigation was read-only. No workflow was dispatched or rerun by me, and no comments, pushes, provider calls, or tracked-file edits were made.