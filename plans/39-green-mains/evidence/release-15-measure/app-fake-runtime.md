# App E2E fake Runtime vs the Runtime contract (Plan 39, read-only)

Scope: `astrid-app` `tests/e2e/fake-runtime/server.ts`, checked against the App client and the Runtime at `release/15/main`.
Sources read at: App `d53685f3` (2026-11-24, `FETCH_HEAD`); Runtime `24e2c929` (2026-11-23 21:25 +0100, the pin in App `runtime.lock.json`). Nothing was run: no `node_modules`, no E2E, no writes. "V" = verified by reading code or logs; "L" = inferred from log text or from static reading only.

Working files (all in this directory): `app-client-routes.tsv` (138 generated client operations), `runtime-openapi-routes.tsv` (139 OpenAPI operations), `runtime-door-entries.txt` (browser door table), `runtime-openapi.yaml`, `client_vs_fake.json`, `diff_routes.py`, `door_refused_usage.txt`.

## 1. Routes the fake implements

Dispatch is in `tests/e2e/fake-runtime/server.ts:165-323`. Three layers:

| Layer | Route | Source |
|---|---|---|
| direct | `GET /runtime-config/v1/workspace.json` (no auth) | server.ts:171 |
| direct | `POST /__test/reset` | server.ts:193 |
| direct | `PUT /v1/projects/selection` | server.ts:228 |
| fixture | `GET /v1/health`, `/v1/handshake`, `/v1/realm` | server.ts:247; fixture fakeWorkspaceRuntime.ts:222-228 |
| direct | `GET /v1/projects/{p}/timelines` (list, aggregated across instances) | server.ts:251 |
| direct | `GET /v1/projects/{p}/documents` (always empty) | server.ts:270 |
| fixture | `GET`/`PATCH /v1/projects/{p}/timelines/{t}` | server.ts:280; fixture :530, :270 |
| fixture | `POST /v1/projects/{p}/timelines/{t}/inspect` | fixture :413 |
| fixture | `GET .../composition-revisions`, `GET .../composition-revisions/{rev}`, `POST .../composition-revisions/{rev}/restore` | fixture :445-491 |
| fixture | `POST .../composition-revisions` and `POST .../replace-parent-media` return 410 `retired_route` | fixture :191 |
| fixture | `POST /v1/projects/{p}/media-imports`, `POST /v1/projects/{p}/objects`, `GET /v1/projects/{p}/objects/{id}/location` | server.ts:293-300; fixture :276, :308, :364 |
| fixture | `GET`/`HEAD /v1/objects/{id}` | server.ts:301; fixture :387 |
| router | `GET|PUT /v1/app-state/user/{key}` | fakeRuntimeRouter.ts:785 |
| router | `GET /v1/capabilities` | router:808 |
| router | `GET /v1/projects`, `GET /v1/projects/{selector}` | router:827, :833 |
| router | `GET /v1/events` | router:842 |
| router | `POST /v1/tasks`, `GET /v1/tasks/{id}`, `POST /v1/tasks/{id}/cancel`, `GET /v1/projects/{p}/tasks` | router:846-857, :861 |
| router | `GET /v1/projects/{p}/generations`, `GET /v1/generations/{id}`, `GET /v1/generations/{id}/variants` | router:884-900 |
| router | `GET /v1/projects/{p}/objects` (list) | router:16-32 |
| acp | non-`/v1` ACP chat/agent routes | tests/e2e/fake-runtime/acp.ts:83-186 (not Runtime `/v1`; not assessed) |

Anything else returns `404 not_found "No fake route for <pathname>"` (server.ts:213-225). Any thrown error in the fixture becomes a 500 (`unexpected METHOD path`, fakeWorkspaceRuntime.ts:553; server.ts:154-156).

Reachability notes (V): several handlers exist in the fixture or router but are unreachable because `server.ts` routes first: fixture `POST /v1/projects/{p}/timelines` (fixture:246), `PATCH /v1/projects/{p}` (fixture:235), `POST /v1/projects/{p}/documents` with timeline (fixture:210), router `GET /v1/health` and `GET /v1/objects/{id}`. Those are dead code for the E2E path.

No `packs` route exists anywhere in `tests/e2e/fake-runtime` (V, grep). No `POST .../timelines/{t}/commit` handler exists (V; fixture:553 throws).

## 2. Routes the App calls

Generated client: `src/integrations/runtime/generated.ts` (314 lines, header "Generated from contract/openapi/workspace-v1.yaml"; `PROTOCOL` workspace.v1). 138 operations extracted (`app-client-routes.tsv`). The client prefixes `/v1/...` and the browser reaches it through `/api/runtime`.

Hand-written calls to Runtime paths (V, grep of non-test `src/`):

| Route | Call site |
|---|---|
| `GET /packs/inventory` | `src/tools/video-editor/runtime/extensionLoader.ts:89`, `useRuntimePackExtensions.ts:42` (a 404 here is treated as "packs absent", :44-50; extensionLoader throws on non-ok, :90) |
| `GET /packs/project-elements?project=<id>` | `src/tools/video-editor/runtime/admittedElementLoader.ts:111-115` |
| `GET /packs/project-elements/{p}/{digest}.js` | `admittedElementLoader.ts:53` |
| `GET /v1/projects/{p}/timelines/{t}/verified-head` | `src/integrations/runtime/client.ts:1011` |
| `GET /v1/update/status`, `POST /v1/update` | `client.ts:823`, `:838` |
| `GET /v1/diagnostics` | `src/shared/components/RuntimeConnection/diagnosticsDownload.ts:36` |
| `GET /v1/health`, `/v1/realm`, `/v1/handshake`, `/v1/objects/{id}`, `POST /v1/projects/{p}/objects`, `/v1/tasks`, `/v1/events`, `/v1/capabilities`, `/v1/projects`, `/v1/projects/{p}`, `/v1/projects/{p}/timelines`, `/v1/projects/{p}/generations`, `/v1/generations/...`, `/v1/projects/{p}/tasks`, `PUT /v1/projects/selection` | `src/integrations/astrid/*Routes.ts`, `src/integrations/runtime/*`, `localWorkspaceProjectSelection.ts:12` |
| `POST /v1/projects/{p}/timelines/{t}/commit` | `src/tools/video-editor/commands/commitSession.ts:227`, `localSaveSession.ts:356`, `bootstrapInitialization.ts:179`, `commitOutbox.ts:561` |
| `GET /v1/projects/{p}/timelines/{t}/commits?limit=50` | `generated.ts:212` (`listTimelineCommits`), called from `bootstrapInitialization.ts:91` and `dataProvider.ts:521-539` |

## 3. Runtime routes (the real surface)

Three tables, all at Runtime `24e2c929`:

- **OpenAPI contract** `contract/openapi/workspace-v1.yaml`: 139 operations (`runtime-openapi-routes.tsv`). The App's 138 generated operations are all present in it (V: 0 generated routes missing from OpenAPI). `TimelineCommitPage` = `HistoryPage` (`contract/schemas/timeline-commit.json`), required `items`, `next_cursor`, `head{revision_id, publication_id}`, `additionalProperties:false` (V).
- **Browser door** `runtime_protocol/door.py:185-260`: 69 entries including ACP. It serves 54 of the App's 138 generated operations. It adds `GET /v1/projects/:/timelines/:/verified-head`, `GET /v1/diagnostics`, `POST /v1/update`, `GET /v1/update/status` (all absent from OpenAPI). `GET /v1/capabilities` is in `ASTRID_ONLY_ROUTES` (door.py:242). Pack routes are classified at door.py:334.
- **Pack routes** `runtime_protocol/server.py:31-64` (`pack_http_route`), dispatched at server.py:774-790, implemented in `service.py:6135` (`pack_inventory`) and `service.py:6150-6240` (`project_pack_elements`). They are **not in the contract**: `git grep packs` over `contract/` and `conformance/` returns nothing (V).

Retired routes (V): `POST .../timelines/{t}/composition-revisions` returns 410 `retired_route`, via `server.py:980-984` calling `reject_retired_timeline_writer()` (`service.py:450-456`). The matching fixture is `conformance/responses/retired_route_410.json` (commit f232693, 2026-10-27), vendored into App at `src/integrations/runtime/fixtures/responses/retired_route_410.json` (App `runtime.lock.json` sha256 e3b43083...). `PATCH /v1/timelines/{t}`, shot and reference writes, `publish-timeline-render` and `timeline-document` writes also return 410 or are refused (`service.py:545`, `:4654-4665`; `server.py:1120`).

## 4. Diff

### 4a. Missing or wrong in the fake, for routes the E2E actually calls

| # | Route | Fake today | Runtime (real) | Evidence (logs and code) |
|---|---|---|---|---|
| M1 | `GET /api/runtime/packs/inventory` | 404 "no fake route" (server.ts:223-224) | 200 `{version:1, revision:int>=0, packs:[...]}` (service.py:6135-6148) | V: 308 fake log lines in the 6 E2E logs; App guard `timeline/support.ts:576` throws on any 404 |
| M2 | `GET /api/runtime/packs/project-elements?project=<id>` | 404 | 200 `{version:1, projectId, realmId, selectionDigest, projects[], legacy[], elements[]}` (service.py:6150-6240) | V: 472 log lines; App parser `admittedElementLoader.ts:76-82` requires `projectId === requested`, non-empty `realmId`, a sha256 `selectionDigest`, and arrays for `projects`, `legacy` and `elements` |
| M3 | `GET /v1/projects/{p}/timelines/{t}/commits?limit=50` | 500 `unexpected GET ...` (fixture:553 via server.ts:154) | 200 `HistoryPage` (openapi `listTimelineCommits`, :362) | V: 357 log lines; the App's unit tests already use the shape `{items:[], next_cursor:null, head:{revision_id, publication_id}}` (`timelineCommit.test.ts:34`) |
| M4 | `GET /v1/projects/{p}/timelines/{t}/verified-head` | 500 (not served) | 200 (door.py:206) | L: not seen in the 6 logs; needed by `client.ts:1011` |
| M5 | `POST /v1/projects/{p}/timelines/{t}/commit` | 500 (no handler) | commit (openapi :347) | L: no `unexpected POST` line in these logs; the save path is not exercised by the failing specs. Any spec that saves will hit this |
| M6 | `POST /v1/projects/{p}/timelines` | unreachable (server routes only GET) → 404 | create timeline | V (code), not observed in logs |

Retired-route item (stale on the App side, not a fake gap):

| # | Route | Fake today | Real Runtime | Evidence |
|---|---|---|---|---|
| R1 | `POST /v1/projects/{p}/timelines/{t}/composition-revisions` (test helper) | 410 retired_route (fixture:191) | 410 retired_route (server.py:980-984, service.py:450) | V: caller `tests/e2e/timeline/support.ts:275` (`publishFakeRuntimeComposition`, 264-286); the App's own local harness already moved away (`tests/e2e/local/support/harness.ts:1287` comment) |

### 4b. Shape drift

- Packs: App parser requirements above (M1, M2) against `service.py` shapes match field-for-field on the keys the App reads (V). Drift risk is only in keys the App does not check, e.g. `artifactManifest` detail (`extensionLoader.ts:82-100`).
- `HistoryPage`: fake's planned shape matches the contract (V). The `publication_id` value to use is `publication-current`, which the fixture already emits (`fakeWorkspaceRuntime.ts:234`, `:546`) (L: not checked against a live read).
- The fake's 410 for `POST .../replace-parent-media` (fixture:191) is not evidenced in Runtime code. OpenAPI still lists the operation (openapi:430) and the door does not serve it (door.py has no entry). Whether the real Runtime returns 410 or 404 is unverified.

### 4c. Missing in fake, not hit by the E2E logs

About 98 of the App's 138 generated operations have no fake handler (V, `client_vs_fake.json`). Mostly shots, references, shot-text-bindings, runs, managed-output adopt/lifecycle, attempts/worker, realm lifecycle, `GET /v1/preferences/{scope}` and `PUT` on it, and `GET /v1/projects/{p}/timelines/{t}/revisions/{rev}`. None appears in the six E2E logs. Only the `commits` route is seen failing.

### 4d. Routes the App calls that the Runtime's browser door refuses

84 of the generated operations exist in OpenAPI but have no browser-door entry (`door_refused_usage.txt`). Examples the App code does call (V for the call, L for "runs in production"): `GET /v1/capabilities` (`src/tools/video-editor/lib/timeline-transfer.ts:68`, `operationHost.ts:275`), which door.py lists as Astrid-only (door.py:242); `POST /v1/projects/{p}/timelines/{t}/views`; `POST .../replace-parent-media`; `POST /v1/managed-outputs/{id}/adopt`; `GET /v1/projects/{p}/timelines/{t}/revisions/{rev}`. Either these reach a different door, or they are a product-level route mismatch. Not resolved here.

### 4e. Retired or redundant

- `POST .../composition-revisions` (R1): retired on the Runtime. The test helper is the stale part.
- `POST .../replace-parent-media`: OpenAPI-listed, not in door. Status unclear (see 4b).
- Fixture dead branches (section 1) are redundant, not wrong.

## 5. Failing E2E tests mapped to the route they need

Source: `app-green/logs/45231479752_*` (latest completed run with logs, `3f5da385`). Attribution is per failing test block in the log. Route-naming error text is V (the failure message itself names the URL). Otherwise L.

| Job | Failing | Route needed | Basis |
|---|---|---|---|
| extension-accessibility | 9 (chromium, firefox, webkit x 3 tests) | M1, M2, M3 | V: each issues list names `packs/inventory`, `project-elements`, and `commits?limit=50` 500 (extension-accessibility.spec.ts:148, :163) |
| extension-cross-browser | 6 (chrome-stable, firefox, webkit; spec :76, :97) | M1, M2, M3 | L (same pattern in log block) |
| playwright-timeline | 25 route-attributed (of 36) | M1, M2, M3 | V for `packs` 404s named in `timeline/support.ts:576` message. Per spec: layout-geometry:261 x5, toolbar-reachable:27 x2 and :89 x3, shell-responsive-overflow:42 x3, tablet-gestures:41 x2, desktop-interaction:19, phone-gestures:32, seeded-preview-samples:21, data-lane-viewport:16, extension-performance-budget:67. Report-listed but not in my parse: editor-tour:232/323/357/375 (x4, probable), command-outbox:48 (conflicts with report's browser-path env cause; needs re-run) |
| playwright-timeline | 1 | none (ASSERT) | audio-reactive-colour-export:229, toEqual; report lists it under cause 1 (unverified) |
| playwright-timeline | 10 | none (env) | viewing-parity/cases.ts:240,257,278,288,328 (x2 projects). Needs `VIEWING_BROWSER_FLOCK_HELD`, not routes |
| playwright-timeline-chrome-export | 2 | M1, M2, M3 | L: audio-reactive-colour-export:304, :412 |
| playwright-timeline-chrome-export | 1 | R1 (stale helper) | V: preview-scrub-evidence:231 via `timeline/support.ts:275` POST composition-revisions (410) |
| playwright-default | 1 | M1, M2 (L) | extension-harness.spec.ts:273 desktop (PACKS,COMMITS). Its condensed and mobile variants show toHaveAttribute failures |
| playwright-default | 1 | M1, M2 (L) | video-editor-instance-lifecycle.spec.ts:6 |
| playwright-default | 3 | unclear | public-astrid-integrated:124 (live feed, report cause 4), public-astrid-vision-sigils-nav:352 (CSS). Route text in block is probably noise |
| extension-visual | 1 | none | screenshot size (report cause 4 / cause 1 unverified) |

Count check: route-attributed (V or L) 9 + 6 + 25 + 2 + 1 + 1 = 44, inside the report's 38 confirmed to ~46. The 4 editor-tour tests and command-outbox are the difference between the two counts.

## 6. Proposed cards

**P39-APP-FR-01. Serve packs inventory and project-elements from the fake.** Kind: env (fake fidelity). Repo: astrid-app. Cluster: fake-runtime 404s. Tests: about 44 (list in section 5). Fix: before the non-/v1 branch in server.ts, match the full prefixed pathname (`/api/runtime/packs/...`, the form the fake logs, and the form the Runtime's door matches at door.py:334). Return `{version:1, revision:0, packs:[]}` for inventory. For `project-elements`, return `{version:1, projectId:DEMO_PROJECT_ID, realmId:FAKE_RUNTIME_REALM_ID, selectionDigest:'sha256:'+'0'*64, projects:[], legacy:[], elements:[]}` when `project` is canonical, else 404 `project ... was not found`. Scope: `tests/e2e/fake-runtime/server.ts` (dispatch, insert near :213). Proof: `node --import tsx --test tests/e2e/fake-runtime/server.contract.test.mjs`, then E2E `playwright-timeline` and `extension-accessibility`. Route N. Size 0.5-1 day. Deps: none. Confidence: V for shapes and paths. Open: whether `admittedElementLoader` tests need a non-empty fixture (`src/tools/video-editor/runtime/__fixtures__/project-elements-list.json` exists) for the accessibility specs.

**P39-APP-FR-02. Serve `GET .../timelines/{t}/commits` (HistoryPage).** Kind: env. Tests: about 40 (same families; the commits 500 is in all of them). Fix: in the timeline branch (server.ts:280-289), answer GET `/commits` with `{items:[], next_cursor:null, head:{revision_id: instance.fixture.read().headRevisionId, publication_id:'publication-current'}}`. Scope: server.ts:280 (path:symbol `dispatch`). Proof: server.contract.test.mjs plus `src/integrations/runtime/timelineCommit.test.ts`, `bootstrapInitialization.test.ts`. Route N. 0.5 day. Deps: FR-01 for the same runs. Confidence: V shape; L on bootstrap behaviour with an empty history (watch `bootstrapInitialization.ts:91-120` and `dataProvider.test.ts:1120`). Open: whether empty history changes which bootstrap branch runs; an E2E run decides.

**P39-APP-FR-03. Route-coverage check (fails when the App calls a route the fake lacks).** Kind: env (test infrastructure). Scope: new check in `tests/e2e/fake-runtime/server.contract.test.mjs`, reading `src/integrations/runtime/generated.ts` and the hand-written `/v1/` and `/packs/` literals in non-test `src/`. Fail on any (method, path) not in the fake route table and not in an explicit `NOT_FAKED` list with a reason. Seed the list from section 4c and 4d. Proof: `node --import tsx --test tests/e2e/fake-runtime/server.contract.test.mjs`. Route X (needs a careful parser for template literals and `encodeURIComponent` placeholders, and the hand-written calls). Size 1-1.5 days. Deps: FR-01, FR-02. Confidence: V for the approach, L on parser reliability. Open: do we want M4-M6 added or listed as NOT_FAKED.

**P39-APP-FR-04. Move the publish helper off the retired route.** Kind: stale-test. Evidence: Runtime 410 at `server.py:980-984` via `service.py:450`; conformance fixture `conformance/responses/retired_route_410.json` (f232693, 2026-10-27, App-vendored); App harness already seeds through commit (`tests/e2e/local/support/harness.ts:1287`). The "postdates the test's last change" rule is not cleanly met: the 410 fixture (2026-10-27) predates the helper's file last change (4e51347, 2026-11-11), so the helper was written against a route already retired. Owner should accept the verdict as "broken helper, not stale behaviour". Fix: rewrite `publishFakeRuntimeComposition` (support.ts:264-286) to submit an EditCommand batch through commit (`commitTimeline`), or drop the helper where unused. Scope: `tests/e2e/timeline/support.ts:264-286`; callers `preview-scrub-evidence.spec.ts:231`. Proof: `tests/e2e/timeline/preview-scrub-evidence.spec.ts` on the chrome-export job. Route X (the commit body must be built). Size 0.5-1 day. Deps: FR-05 if the fake must accept commit (M5). Confidence: V for the 410; L for the rewrite cost.

**P39-APP-FR-05. Vendor the Runtime contract into the App check.** Kind: env (drift control). The App does not vendor `contract/openapi/workspace-v1.yaml`. `config/astrid-cli-surface/vendor.lock.json` covers the CLI surface and public-boundary schemas (not Runtime HTTP), and `runtime.lock.json` covers generated.ts, generated-contract-metadata.ts, the conformance responses and the timeline schema (V). Proposed: add the OpenAPI file and `contract/artifacts.json` to the runtime lock's `files`, then have FR-03 read the vendored file rather than the generated client. Also check `OPERATIONS` in `generated-contract-metadata.ts` (already vendored, 0.2.15, schema digest 2c6a76e1...) against the OpenAPI operationIds. Scope: `runtime.lock.json`, `src/integrations/runtime/` (vendored files), FR-03's test. Route N. 1 day. Deps: FR-03. Confidence: V for what is vendored today. Open: owner to approve adding a file to the pinned set.

**P39-APP-FR-06. Packs routes are outside the Runtime contract.** Kind: unknown (contract gap, cross-repo). Evidence: `git grep packs` over Runtime `contract/` and `conformance/` is empty (V); the routes live in `server.py:31-64, 774-790` and `service.py:120, 6135-6240`. Consequence: a contract-driven fake cannot generate these two routes. Options: (a) Runtime adds the pack routes to `workspace-v1.yaml`; (b) the App keeps a hand-written `PACK_ROUTES` list in the fake with citations. Route S (contract change that affects the protocol boundary) if (a); N if (b). Size 0.5 day for (b), 1-2 days for (a). Open: owner decision.

**P39-APP-FR-07. Door-refused generated routes that the App calls.** Kind: unknown (possible product-bug). Evidence: `door.py:185-260` has no entry for, e.g., `GET /v1/capabilities` (listed Astrid-only at :242, while App calls it at `timeline-transfer.ts:68`), `POST .../timelines/{t}/views`, `POST .../replace-parent-media`, `POST /v1/managed-outputs/{id}/adopt`, and 80 more. Whether the App reaches them through another door was not traced. Route X (cross-repo reasoning). Size 1-2 days. Deps: none. Confidence: inferred. Open: which door serves each of these in the shipped product.

## 7. What is verified and what is not

Verified (V): the fake's route table (section 1); the App's 138 generated operations and their pins; the Runtime OpenAPI and door tables; the packs shapes; the 410 path; the log counts (308 inventory, 472 project-elements, 357 commits lines); the test-to-route mapping for accessibility and cross-browser (named in the failure text).

Not verified: I did not run the fake, the fixture, the E2E suites, or `server.contract.test.mjs`. The per-test mapping for timeline and default jobs is from log block text (L). I did not trace which door serves the 84 door-refused routes, nor the exact status the real Runtime returns for `replace-parent-media`. The App's `publication-current` value is taken from the fixture, not from a live read. `support.ts` line numbers are from `d53685f3` (the report's 276-286 has moved to 264-286).

Open questions for the owner: (1) approve the empty-pack response as the E2E baseline; (2) decide whether pack routes go into the Runtime contract (FR-06); (3) decide whether the stale helper is rewritten or deleted (FR-04).
