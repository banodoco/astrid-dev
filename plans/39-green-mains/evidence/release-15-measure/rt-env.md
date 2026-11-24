# Runtime release/15/main: environment and small-cluster cards (Plan 39, read-only)

Measured run: CI 45259255785 (24e2c929, 23 Nov 2026), jobs unit ubuntu, unit macos, sandbox-process-control, portability ubuntu/macos.
Runtime release/15/main = 24e2c929. Agent pin `tests/astrid-agent.pin` = 0e1543e0 (ancestor of Agent release/15/main 514499de). Poms_packs main = 2379ab54 (checked via GitHub API).
Counts: "distinct IDs" come from `runtime-green/failing-ids.tsv` (rows are id x job; clusters.md counts rows, so its numbers are about 3x).
Paths below are relative to repo roots: Runtime = `astrid-runtime`, Agent = `astrid-agent`, App = `astrid-app`.

Summary of cards (one per cause; RT-E4 and RT-E6 touch different files, so none are merged):

| card | cluster | distinct ids | kind | route | size (days) |
| --- | --- | ---: | --- | --- | ---: |
| RT-E1 | C4 `video_editing` pack absent | 20 | env | N (X if the test is rewritten instead) | 1 |
| RT-E2 | C5 element `image` not installable | 12 | product-bug (suspected, Agent) or stale-test; unknown until ruled | X | 1 |
| RT-E3 | C6 "created identity is occupied" | 10 | unknown (2 h cap) | X | 1 |
| RT-E4 | portability `No module named 'astrid'` | 8 | env | N | 0.5-1 |
| RT-E5 | sandbox pidfd custody | 18 | env (by design) plus marker gap, needs owner rule | X | 2 |
| RT-E6 | R-b hard-coded paths | 2 (1 ID in p2 test, 1 in wc10) | env (p2) and retired-or-env (wc10) | N | 0.5 |

---

## RT-E1: `astrid.packs.video_editing` is not in the Agent pin, and CI installs no packs

- **Repo:** astrid-runtime (test); astrid-runtime `.github/workflows/ci.yml` (unit and sandbox env steps); new pin file.
- **Cluster and IDs:** C4, 20 distinct IDs, all in `tests/test_timeline_render_publication.py` (3 IDs) and `tests/test_timeline_render_publication_authority.py` (17 IDs, per REPORT). Each fails in unit ubuntu, unit macos and sandbox. Example: `tests/test_timeline_render_publication.py::test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence`.
- **Kind: env.** Evidence:
  - `tests/test_timeline_render_publication.py:187` does `from astrid.packs.video_editing.shared.runtime_orchestration import publish_stitched_render`.
  - Agent at the pin (`git ls-tree -r 0e1543e0`) and Agent release/15/main (514499de) have no `astrid/packs/video_editing` path. `git log --all -- astrid/packs/video_editing` is empty, so the pack never lived in the Agent.
  - The pack is in banodoco/poms_packs at `video_editing/` (84 files; `video_editing/shared/runtime_orchestration.py` exists; `pack.yaml` depends on packs `editorial` and `iteration`).
  - `config/astrid-beta-capabilities.json` (identical to `astrid/resources/astrid-beta-capabilities.json`) records the move: `video_editing.sync_draft_voiceover` and `video_editing.human_notes` are "Moved to poms_packs; install with `astrid packs add video_editing`".
  - No CI job installs any pack ("No packs are installed in any job", REPORT).
- **Retired or not:** not retired. The 20 IDs test Runtime publication authority ("a prepared checkpoint cannot publish after cancel or stale fence"), which is current behaviour. D10 (`plans/91-agent-main-green/inputs.md:90`) retires Agent tests of the moved packs' content, not Runtime tests that call one moved helper. Under the triage rules, "tests of what users do today are never deleted for being hard."
- **Fix:** provide the real input in CI. Pin a poms_packs revision (full SHA, new file `tests/poms-packs.pin`) and install `video_editing` with its dependencies `editorial` and `iteration` into the unit and sandbox environments. The install is `astrid packs add https://github.com/banodoco/poms_packs --revision <sha> --pack-id <id> --subpath <id>` for each pack, or `ASTRID_PACKS_PATH` pointing at a checkout of that SHA. Do not copy the `--revision main` form from the `install` string in `astrid/resources/moved-elements.json`, which is unpinned. Also make the test's import fail with a message that names the pack (today it is a bare `ModuleNotFoundError`), so the "input removed" proof has a refusal message to check.
- **Scope:** `tests/test_timeline_render_publication.py:186-190` (import guard only, no skip); `.github/workflows/ci.yml` unit job (env and install steps, around lines 117-162) and sandbox job (around lines 320-361); `tests/seccomp/run-suite.sh` and `tests/seccomp/container-entrypoint.py` (the sandbox container must mount the pack, because it only mounts `/src` and `ASTRID_CHECKOUT`).
- **Focused proof:** `tests/test_timeline_render_publication.py`, `tests/test_timeline_render_publication_authority.py`. Hosted run of unit ubuntu, unit macos and sandbox. Then with the pack removed, the test still refuses with its own message.
- **Route N, 1 day.** Dependencies: an owner-chosen poms_packs SHA (candidate: 2379ab54, the current main head; not pinned yet). Overlaps RT-E5 in the sandbox job steps.
- **Alternative (owner's choice, route X):** rewrite `_publish` (line 186) to call Runtime's own publish path directly. The pack helper only composes that call, so the IDs keep their coverage and no pack is needed.
- **Confidence:** verified in code and config. The chosen pin and whether the sandbox container can take the pack are open.

---

## RT-E2: element `image` is not installable from any pack (C5)

- **Repo:** astrid-agent (product or test-side fix); astrid-runtime `tests/test_timeline_native_asset_union.py` (only if the test changes).
- **Cluster and IDs:** C5, 12 distinct IDs in `tests/test_timeline_native_asset_union.py`, in unit ubuntu, unit macos and sandbox. Raise: `astrid/sdk/timeline_address.py:524` (`raise _unresolved(...)`), reached through `_element_schema_once` (line 481).
- **Answer to "what should CI install?":** nothing that exists today. No pack declares an element with id `image`:
  - no `element.yaml` with id `image` in Agent release/15/main or at the pin (`git grep`);
  - no `*/image/element.yaml` or image element in poms_packs (checked against the full tree of `main`, 2379ab54);
  - `astrid/resources/moved-elements.json` lists only `astrid_motion` (20 elements, none named `image`).
- **Kind: suspected product bug in Agent, or stale test. Unknown until the owner rules.** Evidence:
  - the test writes clips with `"clipType": "image"` (`tests/test_timeline_native_asset_union.py:81`) and `_native_import_media(kind="image")` (line 62);
  - `astrid/sdk/timeline_address.py:494` (also :557, :604) short-circuits only `element == MEDIA_CLIP_TYPE` (`"media"`, line 330). Any other clip type, `image` included, goes to the registry and fails;
  - Agent code elsewhere treats `image` as a media clip type: `astrid/sdk/timeline/_clip_commands.py:24`, `astrid/sdk/timeline/_appearance.py:222`, `astrid/core/timeline/onscreen.py:279`, `astrid/core/timeline/expand_shots.py:193`;
  - Agent's own native media writer sets `clipType='media'` (`astrid/sdk/timeline/native_parent_media_commands.py:210`).
  - The same code is at the pin 0e1543e0 (line 492 there), so a pin bump to 514499de does not change it.
  - Timing: the short-circuit has been there since `fb730f78` (10 Nov, squash merge, which does not count as a source by itself). The test was last changed in `f232693` (27 Oct). So no source postdates the test that says `image` should or should not resolve. Per the rules, that is `unknown`.
- **Fix (owner chooses one):**
  - A. Product (Agent): treat `image` (and `video`, `audio`, if the owner agrees) like `media` in `timeline_address.py:494`, consistent with the sibling code above. Proof: this test file passes.
  - B. Test: change the row at `test_timeline_native_asset_union.py:81` to `clipType: "media"`, as the Agent's writer does. Needs a source that states the new rule; none is found yet.
- **Scope:** A: `astrid/sdk/timeline_address.py` (lines 494, 557, 604 only). B: `tests/test_timeline_native_asset_union.py:62,81`.
- **Focused proof:** `tests/test_timeline_native_asset_union.py`; `tests/sdk/test_timeline_reader_roundtrip.py` for the writer.
- **Route X, 1 day.** Dependencies: Agent decision, then a pin bump (Plan 77 owns the pin).
- **Confidence:** verified in code and at the pin. The kind is inferred. I did not run the test.

---

## RT-E3: "created identity is occupied" in the three-products seed (C6)

- **Repo:** astrid-runtime (test fixture); the Agent checks are cited for context.
- **Cluster and IDs:** C6, 10 distinct IDs, all in `tests/test_timeline_commit_sequential_verifier.py`: `test_public_three_products_seed_preserves_full_raw_assertions_and_history` and nine `test_public_three_products_scope_forgery_refuses_without_write[...]` variants (`ambiguous, duplicate, foreign, missing_batch, missing_step, outside, tampered_source, wrong_ordinal, wrong_phase`). Raise: `astrid/sdk/timeline/_recording.py:175` (`ref` already present).
- **Mechanism (verified):**
  - the seed case has `initialize: True`, so the script calls `capture_initialize` (`tests/fixtures/timeline_three_products_seed.json`, script lines 31-35);
  - Runtime's canonical bootstrap already gives the timeline starter tracks V1 and A1 (`runtime_protocol/timeline_commit_baseline.py:431-432`, added in `f232693`, 27 Oct 2026 12:12Z);
  - the script then creates `parent/track:V1` again (script line 40), and `_recording.py:175` refuses because it exists.
  - The script's own assertion (line 38) expects `[V1]` only in the non-initialize case.
- **Kind: unknown (2 h cap).** Stale fixture or product contract is not settled:
  - the test file was last changed in `2edc444` (27 Oct 15:29Z), after `f232693`, so no source postdates the test. The rule requires that for `stale-test`;
  - the product may also be wrong if `initialize` should accept an existing V1.
- **Diagnosis to run first:** confirm the first refusal in a local run of one ID (`--tb=long`), and check whether the expected 21 commands (test line 78) count the V1 create. If the seed drops V1, the count changes too.
- **Fix after the diagnosis:** if the seed is stale, remove script line 40, update the expected command count, and cite `timeline_commit_baseline.py:431` with `f232693` as the source. If the product is wrong, file it under D6 and keep the IDs red.
- **Scope:** `tests/fixtures/timeline_three_products_seed.json` (script line 40 and the count), `tests/test_timeline_commit_sequential_verifier.py:78` only.
- **Focused proof:** the 10 IDs above.
- **Route X, 1 day (2 h diagnosis cap).** Dependencies: none. Agent is not changed unless the diagnosis says so.
- **Confidence:** the mechanism is verified in code. Which side is wrong is not verified.

---

## RT-E4: `No module named 'astrid'` in the stage venv (portability-lifecycle)

- **Repo:** astrid-runtime `tests/conftest.py` only.
- **Cluster and IDs:** portability lane, 8 distinct IDs (ubuntu 7, macos 8 per REPORT): `tests/test_portable_lifecycle.py` (5 installed-lifecycle tests, plus the C44-C46 messages) and `tests/test_profile_services.py` (installed run/up, and the node-environment test). Message in the logs: `runtime daemon exited during startup: no module named 'astrid'`.
- **Kind: env.** Evidence:
  - the fixture `stage1_runtime_environment` (`tests/conftest.py:146-214`) builds an offline venv from two wheels only, the Runtime and the client (`pip install --no-index --no-deps`, line 212). The Agent is never installed into it;
  - the portability job sets `ASTRID_CHECKOUT` (`ci.yml:397`) and installs the Agent only into the outer venv (`ci.yml:447`). The stage daemon does not inherit that venv;
  - the darwin-native job shows the pattern that works: `pip install --require-hashes -r $ASTRID_CHECKOUT/requirements/runtime.lock`, then the Agent `--no-deps` (`ci.yml:235-239`). The pin has `requirements/runtime.lock` (verified with `git cat-file -e`).
- **Fix:** in the stage fixture only, when `ASTRID_CHECKOUT` is set, make the Agent importable from the stage venv. Preferred: build its wheel offline the way the Runtime wheels are built (`pip wheel --no-index --no-build-isolation --no-deps`) and install it with the Runtime wheels. If the Agent's import needs third-party packages, seed the venv from `runtime.lock` wheels, which changes the offline rule the fixture states; that is a route X question. When `ASTRID_CHECKOUT` is unset, the fixture must refuse with its own message (`tests/astrid_checkout.py:20-24` already does this for other callers).
- **Scope:** `tests/conftest.py:146-214` (fixture `stage1_runtime_environment`). No `ci.yml` change.
- **Focused proof:** the portability job on both OS, `tests/test_portable_lifecycle.py`, `tests/test_profile_services.py`. Then with `ASTRID_CHECKOUT` unset, the fixture refuses with its message.
- **Route N, 0.5-1 day** (X if the dependency set is needed). Dependencies: none.
- **Confidence:** the cause is verified in code and logs. Whether the wheel alone is enough is not verified; I did not build it.

---

## RT-E5: sandbox pidfd custody (18 IDs, sandbox-process-control only)

- **Repo:** astrid-runtime tests (marker or assertions) and `tests/seccomp/`. Product code is not changed.
- **Cluster and IDs:** `tests/test_real_bootstrap.py` (10, including `test_cli_indexed_file_replaced_by_checkout_refuses_live_owner[*]`, `test_linux_loopback_*`), `tests/test_linux_runtime_boundary_native.py` (4, including `test_start_publishes_native_custody_and_term_signals_exact_owner`), `tests/test_linux_listener.py` (2), `tests/test_process_control.py` (2). Log count: 12 raise `astrid_runtime/custody_broker.py:1864` ("Linux pidfd custody is unavailable") in job 137989251348.
- **Kind: env, by design, plus a marker gap that needs an owner ruling.** Evidence:
  - `tests/seccomp/README.md` says the OpenShell-like profile denies `pidfd_open` (ENOSYS), `pidfd_send_signal` (EPERM), and that tests marked `needs_real_pidfd` "exercise the strict pidfd path itself... so this job alone deselects them";
  - `tests/seccomp/container-entrypoint.py:73` deselects only that marker;
  - `tests/test_real_bootstrap.py` has no marker; `tests/test_linux_runtime_boundary_native.py:21-22` uses `requires_linux_tree_custody`, which gates only on `sys_platform` (`tests/lanes.py:341-344`), so it runs in the container;
  - the product refusal at `custody_broker.py:1864` is correct behaviour under this profile.
- **Fix:** the triage rules forbid adding to a deselect list, so adding `needs_real_pidfd` to these files is not an allowed fix without an owner decision. The rule-compliant option is per test: in sandbox mode, assert the product's refusal ("Linux pidfd custody is unavailable", or the `pidfd: enosys` message) and keep the success assertions for the strict job. Owner must choose per file (the test names say which are strict-only).
- **Scope:** `tests/test_real_bootstrap.py` (the 10 IDs), `tests/test_linux_runtime_boundary_native.py` (4), `tests/test_linux_listener.py` (2), `tests/test_process_control.py` (2, one of which already has the marker).
- **Focused proof:** sandbox job (`sh tests/seccomp/run-suite.sh`), and unit ubuntu for the strict assertions.
- **Route X, 2 days.** Dependencies: owner ruling on the marker versus refusal assertion. Overlaps RT-E1 in the sandbox steps only.
- **Confidence:** verified from README, entrypoint and log. Which exact tests are strict-only is inferred from names and not run.

---

## RT-E6: hard-coded paths (R-b)

REPORT said "3 ids"; in `failing-ids.tsv` the p2 test is 1 ID in 3 job rows, plus 1 wc10 ID in nightly.

### RT-E6a: `tests/test_p2_commit_phase_capture.py:62`

- **Cluster:** C22, ID `tests/test_p2_commit_phase_capture.py::test_supported_app_bootstrap_loads_this_pinned_helper_offline` (unit ubuntu, unit macos, sandbox).
- **Kind: env.** Line 62 hard-codes `work/app/scripts/testing/sitecustomize.py` (a developer checkout). `assert bootstrap_path.is_file()` then fails in CI. The file exists in the App at `scripts/testing/sitecustomize.py` (App release/15/main); the Runtime CI never checks out the App.
- **Fix:** provide the real input. Check out astrid-app at a pinned SHA in the unit and sandbox jobs, pass its path via an env var (for example `ASTRID_APP_CHECKOUT`), and have the test refuse with its own message when it is unset. Alternative (owner): move this App-bootstrap test to astrid-app, since it tests App behaviour.
- **Scope:** `tests/test_p2_commit_phase_capture.py:57-66`; `.github/workflows/ci.yml` unit and sandbox steps.
- **Focused proof:** that file, unit ubuntu and sandbox.
- **Route N, 0.5 day.** Dependencies: an App pin (`tests/` has none for the App; owner choice).

### RT-E6b: `tests/test_wc10_installed_launcher.py:21-26`

- **Cluster:** nightly only, 1 ID.
- **Kind: retired (proposed), owner decides.** It builds an installed launcher from a historical Agent commit `6efc8150...` (checked out at `/home/user/work/wt/agt-pin-6efc8150`) and a historical Runtime `8f70a818...`. Both commits exist on GitHub (HTTP 200), but the current pin is `0e1543e0`. "Historical commits... are retired" under D5. Its only other fix would be an env fix (fetch the commit into a temp dir), which keeps testing an old install boundary.
- **Fix if retired:** delete the test, citing D5 and the pin move (`tests/astrid-agent.pin`), and keep any refusal test that users could reach (none found). If kept: fetch `6efc8150` into a temp dir in the test and drop the hard-coded worktree.
- **Scope:** `tests/test_wc10_installed_launcher.py`.
- **Focused proof:** nightly dispatch (the schedule only fires from main).
- **Route N, 0.5 day.** Owner decision on retire versus keep.

---

## Open questions for the owner

1. RT-E1: which poms_packs SHA to pin (2379ab54 is the current main head, unpinned), and whether the sandbox container should get the packs or the test should call the Runtime path directly.
2. RT-E2: is `image` a clip type the Agent should resolve as media (fix A), or should the test write `media` (fix B)?
3. RT-E5: per-test choice between strict-only (marker, owner must approve the deselect growth) and refusal assertion in sandbox mode.
4. RT-E6b: retire the wc10 test under D5?

## What I could not verify

- I did not run any test, build the stage wheel, or dispatch a workflow. All fixes are unproven.
- RT-E3: which side is wrong. The diagnosis is not run.
- RT-E4: whether the Agent's import needs third-party packages in the stage venv.
- RT-E2 and RT-E3 "unknown": I found no source that postdates the test. A PR or plan line might exist elsewhere that I did not read.
- Whether a pin bump to Agent release/15/main (514499de) changes C5 or C6. I checked only that it has no `video_editing` path; I did not check the C5/C6 code on it in full.
- Line numbers are at the fetched heads (Runtime 24e2c929, Agent 0e1543e0 and 514499de, App release/15/main). Re-check at dispatch.
