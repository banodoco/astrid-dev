# Fixes spec — duplicate work inside one `generate`, proven by reading

Read on 22 November 2026 at astrid-agent `315b8b7a9336ec3147b399f6bf6f168011d09b27` (`release/15/plan-81`) and VibeComfy `e65f494` (not the pinned `799d90f6`). Nothing was run. "Counted" below says how each count was established: by call sites, or by the request counts in `plans/81-once-per-command/evidence/2026-11-22-us2-exact-gate.json`. Re-check every line at dispatch.

**Task ids:** `F-1` to `F-5`. **Rules for every card:** no wire, schema or store change; no refusal moves later than it is today; no existing test edited, skipped or weakened; a value worked out once is an argument or an attribute of one command's objects, never module-level state; nothing is kept for a later command. Lazy imports wait for the profile.

## What the code does not support (corrections to the memo)

- **A second `/object_info` fetch on the successful path: not proven, dropped.** `comfy_target.py:748` (`_capture_model_resolution`) is reached only from `backends/vibecomfy.py:525`, the catalog candidate. `entries.py:1189` (`target_schema`) is reached from `sdk/generation.py:1966` and `:1993`, the workflow-entry candidate. One command prepares one candidate at a time, so a successful command makes **one** explicit fetch. `bundle.compile` validates against the captured schema and does not refetch (VibeComfy `workflow_bundle.py:2698-2760`). My memo's "at least two fetches on this route" was wrong.
- **Duplicate emission: already fixed by US-5a.** `emit_bundle` runs once at `sdk/generation.py:2001` and its bytes are reused at `:2133-2134`; the catalog candidate emits once at `:2131`. The approval compile runs once (`:2003` or `:2009`). What remains is that they are untimed (attribution spec, A-3).
- **The launcher connection at 4.6 s on `generate` against 2.1 s on a timeline edit: now explained** (F-1). The memo said the cause was not determined.

## Cards

| Task / outcome | Route | Depends on | Scope | Focused proof | Size |
| --- | --- | --- | --- | --- | --- |
| F-1 `generate workflow` opens one Runtime connection, not two | N | — | astrid-agent `astrid/core/generation/placement.py` (`attached_comfy_url`, 166-179), `astrid/sdk/generation.py:1559` | Below | 3 h |
| F-2 The availability declaration is read once per command | X | — | astrid-agent `astrid/core/generation/availability.py` (105-110, 143-144, 146-173), `astrid/core/generation/entries.py` (`_EntryDiscovery`, 869-), `astrid/sdk/generation.py` (1549, 1590, 1766, 1773, 2233) | Below | 5 h |
| F-3 A catalog candidate uses the command's model registry | N | — | astrid-agent `astrid/core/generation/backends/vibecomfy.py` (`prepare_catalog_workflow`, 500-530), `astrid/sdk/generation.py:887` | Below | 3 h |
| F-4 Placement and generation settings are resolved once per command | N | F-1 | astrid-agent `astrid/sdk/generation.py` (1639-1647, 1718, 1791-1793) | Below | 3 h |
| F-5 The workflow file is snapshotted once on the workflow route. **Held:** do it only if the attribution table shows `workflow snapshot` at 0.2 s or more per occurrence | N | A-6 | astrid-agent `astrid/sdk/generation.py` (1544, 1571, 1973-1980) | Below | 3 h |

### F-1 One Runtime connection

**Today.** `sdk/generation.py:1559` calls `placements.attached_comfy_url(placement)`. That function (`placement.py:166`) calls `resolve_placement(request_from_selector(selector))` with no client (`:174`). `resolve_placement` reads `settings.placement_default(client)` (`:139`), which with `client=None` reaches `settings.current_store(None)` (`settings.py:189`) and then `_launcher_store()` (`settings.py:176-186`): a second `AstridClient.open_from_launcher()` with the pack host, kept in the module-level `_opened` and closed at exit. The command's own client, opened at `cli.py:544`, is in scope as `client` at `generation.py:1559` and is not passed.

**Count, and how counted.** Two connections per `generate workflow` command. By call sites as above, and by the gate's request counts for that command: `POST /v1/handshake` 2 and `GET /v1/health` 2 against 1 and 1 for a timeline edit; `GET /v1/app-state/user/{key}` 4, which is exactly the four settings reads at `generation.py:1559`, `:1641`, `:1718` and `:1791`. The second connection runs the launcher `connect` subprocess and the pack-host attachment again; the calibration shows `Runtime launcher connection` at 4.6 s for `generate` against 2.1 s for a timeline edit. `generate image` does not call `attached_comfy_url`, so this is the workflow route only (and `cli.py:464`, the `--as-entry` form, which is left as it is).

**Change.** `attached_comfy_url(selector, *, client=None, repo=None)` passes both to `resolve_placement`. `generation.py:1559` becomes `placements.attached_comfy_url(placement, client=client, repo=project_root)`. No other caller changes. `settings._opened` is not touched.

**Why nothing moves or is kept.** The same settings document is read, through the connection the command already holds, at the same point. `attached_comfy_url` still swallows the same errors and returns `''`. With `client=None` (a dry run) the behaviour is today's. `repo` only matters when the selector is `auto`, where it makes this read agree with the two that follow.

**Proof.** New test in `tests/sdk/`, in the style of `tests/core/generation/test_command_local_registry.py`: `AstridClient.open_from_launcher` is monkeypatched to count and fail; `GenerationFacade().workflow(workflow=<a ready template>, placement="http://127.0.0.1:1", client=<fake with get_user_app_state>, inputs={...})` with `_generate_on_target` stubbed reaches the stub with zero opens and one `get_user_app_state` call before it; two commands in one process with two fake clients each read their own client. A dry run with `client=None` still consults the store factory, as today. In the gate (A-5): `POST /v1/handshake` 1, `Runtime launcher connection` count 1, `GET /v1/app-state/user/{key}` 3 on the workflow groups.

### F-2 The availability declaration once per command

**Today.** `require_model_available` (`availability.py:105`) and `require_entry_available` (`:143`) call `model_availability` / `entry_availability` with no declaration, so each call runs `availability_declaration()` (`:21`), which runs `discover_packs_ordered()` (`:36`), a full `discover_pack_metadata`. `require_template_available` (`:109`), reached from `require_bundled_workflow_available` (`:146`), does the same. Inside one command the pack scan is reused (`pack_discovery_scope`, entered by `_generation_boundary`, `generation.py:594`), but each reuse re-verifies the managed sources and hashes every file under every pack root to prove the reuse (`discovery.py:508-516`, `_tree_fingerprint`, `:78`), then deep-copies the result.

**Count, and how counted.** By call sites: in the qualification loop one call per candidate (`generation.py:1766` for a catalog candidate, `:1773` for a workflow entry), over **every** candidate before any is prepared (`:1759-1778`). So plain `generate image "prompt"` runs it once per catalog model and ready template offered for that kind and mode; the number is the size of that list and was not counted here. On the workflow route: once at `:1549` and once at `:1773`, two. With `--entry`: once more at `:2233`. Research G's stack samples of `generate image` at 5 s and at 10 s were both in this hashing (`discovery.py:102` at that commit). The seconds per call are not measured; the tree hash alone took 0.07 s for `astrid/packs` in this container.

**Change.** `_EntryDiscovery` (one per command) gains `availability()`, which calls `availability_declaration()` on first use and keeps the result on the instance. `require_model_available`, `require_entry_available`, `require_template_available` and `require_bundled_workflow_available` gain a keyword `declaration=None` passed through to the functions that already accept it (`model_availability`, `entry_availability`, `template_availability`). `_generate_on_target_impl` reads `declaration = discovery.availability()` once before the loop and passes it at `:1766` and `:1773`; `_resolve_public_entry` passes `discovery.availability()` at `:2233`. `GenerationFacade.workflow` has no discovery object at `:1549`, so it creates the command's `_EntryDiscovery` there (as `_generate_on_target_impl` does at `:1716`), uses it at `:1549`, and passes it as `_discovery` at `:1571` so the loop reuses it. Callers that pass nothing behave as today.

**Why nothing moves or is kept.** The same declaration decides the same refusals at the same lines; it is read at the first use instead of at every use. It lives on a per-command object. A pack manifest edited between two candidates of one command is no longer noticed inside that command, which is the same within-command snapshot US-4 already takes for entries and registries; the next command reads it afresh.

**Proof.** New tests beside `tests/core/generation/test_default_command_discovery.py`, which must **not** stub `_generate_on_target` (US-4's count tests do, so they cannot see this loop): `availability.availability_declaration` is wrapped to count; a `generate image` dry run with at least three qualifying candidates calls it once; `generate workflow` calls it once; a second command in the same process calls it again and sees a declaration changed between the two (an unavailable model is refused by the second command only, with the code and wording `tests/` already pin for `generation_route_unqualified`). The existing availability tests pass unchanged.

### F-3 The command's registry for a catalog candidate

**Today.** `_prepare_catalog_target_workflow(registry=registry, ...)` (`generation.py:877`) holds the command's registry and calls `backend.prepare_catalog_workflow(candidate, mode, inputs, resolve_target=...)` (`:887`) without it. With a target client, `prepare_catalog_workflow` calls `ModelRegistry.load_default()` itself (`backends/vibecomfy.py:518`), outside any stage.

**Count, and how counted.** By call sites: one extra full registry load per prepared catalog candidate when a ComfyUI target is selected; none on the workflow route. Research B measured one load at 1.5 to 1.8 s. US-4's "one registry load per command" tests stub `_generate_on_target`, so they do not cover this call.

**Change.** `prepare_catalog_workflow(..., registry=None)`: when given, it is used in place of `load_default()` at `:518`; the lines that rebuild `ModelRegistry([entry, *entries])` are unchanged. `generation.py:887` passes `registry=registry` when the backend's method accepts it, tested with `inspect.signature` as `cli.py:514-515` already does for `replace`, so a substituted backend without the keyword keeps working. `VibeComfyBackend.generate` (`:652`) passes nothing and behaves as today.

**Why nothing moves or is kept.** Same registry contents, same resolution, same refusals; the object is the argument the caller already holds.

**Proof.** New test: `ModelRegistry.load_default` is monkeypatched to count; `_prepare_catalog_target_workflow` is called with a loaded registry, a catalog entry with model roles and a fake target client returning a canned `object_info`; the count stays 0 and the returned plan equals the plan from the same call with `registry` omitted (count 1). A second test drives `GenerationFacade().image(...)` to a stubbed admission without stubbing `_generate_on_target` and asserts one load per command and two for two commands.

### F-4 Placement and settings once per command

**Today.** A live command resolves and validates the placement at `generation.py:1641` and again at `:1791` with the same request, client and repo, and reads the generation settings at `:1718`. Each `resolve_placement` reads the settings document again (`placement.py:139`). With no requested placement and no default kind, each also runs `_discovered_attachment(repo)` (`placement.py:145`, `:196`), which can probe the discovery address.

**Count, and how counted.** Three settings reads per live command after F-1 (four today on the workflow route, matching the gate's count of 4), two placement resolutions, and on `--placement auto` with no default up to two discovery probes. By call sites and the request count. Small: the four reads total about 0.05 s in the gate.

**Change.** `_generate_on_target` passes its `resolved` placement to `_generate_on_target_impl` as a named keyword `_placement`; the impl uses it at `:1791` when given and resolves as today when not (a dry run, or the `:1647` dry pass, which passes it too). `resolve_placement` gains nothing. The settings snapshot at `:1718` stays where it is: it is the one remaining read that is not a placement read.

**Why nothing moves or is kept.** In a live command the placement is already resolved and validated at `:1641`, before qualification, so a placement refusal is already the earlier one; reusing the value changes no order. In a dry run nothing changes.

**Proof.** New test: `placements.resolve_placement` wrapped to count; one live command to a stubbed admission resolves once; a dry run resolves once; two commands resolve twice. In the gate: `GET /v1/app-state/user/{key}` 2 on every generation group. First to cut if time runs short.

### F-5 One snapshot of the workflow file (held)

**Today, by call sites.** On `generate workflow <file.py>` the same source bytes pass through `load_bundle` four times before emission: the snapshot at `generation.py:1544` (`:182`); `describe_workflow` at `:1560` (`entries.py:640`, `production_engine.py:381`); a second snapshot, of the first snapshot, at `:1974`; and `prepare` at `:1976` (`entries.py:1014`). The admission preflight loads the emitted bundle a fifth time (`sdk/remote.py:183`); that one checks the bytes read back from the Runtime and is left alone.

**Why held.** The cost is unknown, and research A measured one ready workflow loading in 2.3 ms. If the attribution table shows `workflow snapshot` at 0.2 s or more: pass the frozen path from `:1544` to the impl as a named keyword `_frozen_workflow`, and at `:1974` use it directly in place of a second `_snapshot_generation_workflow` when it is set; source retention at `:1975-1980` is already skipped there because `retained_source` is set. Sharing one loaded workflow object between `describe_workflow` and `prepare` is **not** proposed: `prepare` binds inputs onto the object, and nothing read here proves `describe_workflow` leaves it unchanged.

**Proof if done.** `_snapshot_generation_workflow` wrapped to count: one per `generate workflow` command, two for two commands; `tests/sdk/test_generation_source_retention.py::test_stale_bundle_rejects_before_target_or_admission` passes unchanged; a file edited after the snapshot does not change the admitted graph.

## The node list inside one command

No card changes when or how often ComfyUI is asked. Each prepared candidate still captures `/object_info` live (`comfy_target.py:748` or `entries.py:1189`), the provider keeps `refresh_object_info=client.object_info` (`entries.py:1258`, `backends/vibecomfy.py:529`), and VibeComfy's reconciliation refreshes before queueing (`runtime/reconciliation.py:158`, read at `e65f494`). A per-command capture kept on `ComfyTargetClient` would save a request only when an automatic default fails and the next candidate is tried; it is not specified, because a successful command would gain nothing. The gate's `/object_info` count (A-5) will show whether that case matters.

## Verified by reading but not specified

- **A saved UI workflow (`generate workflow <file.json> --placement <url>`) fetches `/object_info` three times:** `describe_workflow` (`entries.py:640` to `production_engine.py:298-299`), `prepare` (`entries.py:1014`, same path), and `target_schema` (`entries.py:1189`). The first two go through VibeComfy's own provider and happen before `select_generation_target`; folding them into one capture changes which call first touches the target, and so which refusal an unreachable target gives. That needs the real cost (US-0) and the owner's D6 before a card.
- **A managed local target** re-reads all ready entries, `find_entry` and `ModelRegistry.load_default()` at module level (`engine_local_endpoint.py:274`, `:300-306`) inside `target check`. Whether a live command reaches it was not established (`defer_managed` at `generation.py:1825`), so no card.
- **The admission preflight** re-reads the three objects just written (the gate's nine `GET /v1/objects/{digest}`, 0.16 s) and recompiles the API form (`invocation_preflight.py:469`). It validates the exact bytes the Runtime holds; left alone.
- **A rented-machine command** runs the whole preparation twice, dry then live (`generation.py:1644-1647`). Outside the warm local target.

## Parallel work and shared files

| File | Cards |
| --- | --- |
| `astrid/sdk/generation.py` | F-1 (1559), F-2 (1549, 1571, 1590, 1766, 1773, 2233), F-3 (887), F-4 (1639-1647, 1791), F-5 (1544, 1571, 1974); also A-3 |
| `astrid/core/generation/placement.py` | F-1 only |
| `astrid/core/generation/availability.py`, `entries.py` | F-2; A-3 adds one stage in `availability.py` |
| `astrid/core/generation/backends/vibecomfy.py` | F-3; A-3 adds one stage at 518, which F-3 then makes unreachable on the passed-registry path |

F-1, F-2 and F-3 touch different functions and different lines of `sdk/generation.py` and can be written side by side, each on its own branch; merge in the order F-1, F-3, F-2. F-4 follows F-1 (adjacent lines, and its gate count assumes F-1). F-2 and F-5 both edit line 1571: F-5 after F-2. All of them rebase onto A-3, which wraps the same lines: land A-3 first, or give A-3 and the fixes to one worker. About 14 hours without F-5; one worker in two days, or two in one.

## How we would know

After F-1 to F-4, on the gate's workflow groups: `POST /v1/handshake` 1, `Runtime launcher connection` once, `GET /v1/app-state/user/{key}` 2. On the image groups: `availability declaration` once, `model registry` once. The seconds saved are read from the attribution table before and after; none is promised here, because none of these was timed.
