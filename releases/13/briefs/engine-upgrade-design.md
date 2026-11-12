# Engine upgrade in place (Fable reframe, 12 Nov) — accepted with the model layout

## Owner decisions (12 Nov)
- The model layout and the in-place upgrade both ship in the Release 13 candidate. No shims: no symlinks shipped.
- On Fable's four questions, the manager's recommendation is yes to all (REVIEW, the owner may overrule):
  1. U1–U5 ship in Release 13 with the layout.
  2. The one-time rename of an old `<root>/models` into `ComfyUI/models` (M2) is acceptable.
  3. No rollback on a failed upgrade; re-running resumes it.
  4. Tracked edits in a managed checkout are saved as a patch and discarded.

## Why the clean-root reinstall goes
It fires on any helper-bytes mismatch (`engine_runner.py` about 597-618; `helper_manifest` about 78-88 and 282-309 hash about ten code files plus the recipe and locks), so almost any release strands every install. A recipe change gives a generic `integrity_failed` (590-596, 925-927). It arrived in `ad9694518` (2 Nov, empty message). The real need is narrow: never rebuild a venv under a live engine, and never orphan a GPU process from older code. Stop-then-rebuild under the install lock covers both.

## Design
- **One verb.** `astrid engines install` on an existing root converges it to the current recipe. The local endpoint calls it automatically when a root is stale (`engine_local_endpoint.py` about 198-205).
- **The receipt is a cache, not an authority.** A recipe mismatch means stale, and the existing steps (already verify, skip or repair) run.
- **Helper identity stays a live check only** (`helper("identity")`, about 833-835). Drop `helper_sha256` from the persisted environment receipt, `lock.json` and the session marker.
- **Stop first.** Under the install lock, stop the supervisor whatever helper bytes started it, and wait for `owner.lock` to free. If a job is running, refuse with `engine_busy` and say so.
- **Sources.** Save the tracked diff to `.astrid-engine/discarded/<time>.patch`, then `git checkout --force --detach <pin>` and apply the patches. Never `git clean` (ComfyUI's `.gitignore` covers `/models/`, `/user/`, `/output/` and `/custom_nodes/`).
- **Environments.** If inputs changed, delete the venv, replace the lock and sync. The wheels cache in `runtime/uv-cache`, so unchanged wheels aren't downloaded again.
- **Models.** The default is `<root>/runtime/ComfyUI/models`, via `--models-directory`. The receipt's `models_root` (null means the default) is the only declaration; `effective_models_root` is the only resolver. Re-running install with `--models-root X` rebinds; Astrid never moves or deletes the old directory. Explicit roots stay outside the engine tree. RunPod is unchanged.

## Delete
- `EngineReinstallRequired`, `for_install`, `clean_root`, `install_command` (`engine_contracts.py:78-103`).
- Their raise and mapping sites: `engine_runner.py:443-447,597-598,606-618`; `engine_runner_target.py:157-168`; `engine_custody.py:257-263`; `engine_local_endpoint.py:198-205`; `engine_cli.py:172-179,204-216`; `failure_diagnostics.py:28`; `_STATUS_ERROR_CODES`.
- `check_environment_identities` and `_check_install_identity`.
- The clean-root tests (`test_engine_runner.py` about 680-1160) and the stale-identity test (about 1634).
- All of the model layout's A3: the symlinks, the `models-config*` operations, `{models_config}`.
- The leftover `<root>/models` readers.

## Migration
Once, inside the first converge, with the engine stopped: if `models_root` is null and `<root>/models` is a real directory, remove exact-match legacy links, rename its children into `<root>/runtime/ComfyUI/models/` (same filesystem: no copy, no download), and remove the empty directory.

## Tasks (combined with model-layout-design.md A1–A3)
| id | outcome | size |
|---|---|---|
| U1 | Install converges a stale root in place (`engine_runner.py:environment_state, environment, install_engine, _parse_receipt`; `engine_runner_target.py:_validate_lock_identity`); proof: real-uv CPU fixture, a recipe change, the same root, a model file's inode unchanged | S |
| U2 | Converge stops an older supervisor; a busy engine gives `engine_busy` (`engine_custody.py`) | S |
| U3 | Tracked edits saved, then forced checkout (`_Runner.source`) | X |
| U4 | `engine_reinstall_required` and `-clean` removed everywhere | X |
| U5 | The local endpoint converges automatically, with visible progress | X |
| M1' | One default and one resolver; stragglers gone (`effective_models_root` plus the leftover readers) | X |
| M2' | Legacy `<root>/models` renamed into place once | X |
| M3' | Re-install with `--models-root` rebinds | N |
| A1 | Align uses `subdir/name` (partly done in `c-layout`) | N |
| A2 | `--models-directory` launch (partly done in `c-layout`) | X |
| A3 | Symlinks and their checks deleted (partly done in `c-layout`) | S |

Live proof (G1) stays with the Release 13 manager.

**Not verified:** whether the new client can deliver `stop` to an older supervisor without a protocol change (the SIGTERM handler is at `engine_custody.py:1136-1140`; where the supervisor pid is recorded wasn't traced).

## Astra design review (12 Nov, `review-engine-upgrade-2.log`): SOUND WITH CHANGES, all accepted by the manager
1. **U2: busy admission before stop.** Today stop cancels and drains unconditionally (`engine_custody.py:1063`); the queue check exists only in release (`:1047`); generation submits over HTTP outside the supervisor's operation lock (`comfy_target.py` about 263). Coordinate managed prompt admission with the existing installation lock. Check running and pending work while admission is excluded, and return `engine_busy` before sending stop. Keep the exclusion through convergence. No new locking system.
2. **U2: stopping an older supervisor.** Keep the full ephemeral session identity for addressing its live owner (the private marker `engine_custody.py:310`, the socket, the inherited `owner.lock`); remove it only as an environment-cache veto. A stop-only client validates the marker and sends the OLD identity in the existing envelope (the old supervisor accepts stop at `:1075`; today's client rejects the mismatch before connecting, `:253`). Existing `stop_owned()` waits for the marker to be removed; add the owner-lock barrier. If the old supervisor is unreachable, refuse with an understandable custody error; never erase the marker or kill a remembered PID. Stop comes before even the helper identity call.
3. **M2': a recursive merge by rename.** Rename an entry when its destination is absent; recurse when both are real directories; refuse other collisions, showing both paths; remove emptied source directories. Resumes naturally; no journal. Legacy-link removal is part of the same step and runs for explicit bindings too, judged against the PREVIOUS receipt's binding before a rebind, inspecting existing immediate links rather than only the current lock categories. Only the default binding moves old model files.
4. **U3: checkout safety.** Keep untracked files that don't collide; refuse an obstructing path before a destructive checkout, with the path in the error. Save staged and unstaged tracked changes, including binary ones, with a collision-free name identifying the source. Re-apply only the declared recipe patches. Fetch the pin before checkout when it's missing; a fetch failure leaves the checkout unchanged.
5. **U1: old receipts.** Read an old receipt structurally, keep its installation binding and unresolved-custody information, and treat recipe-dependent evidence as disposable (parser `engine_runner.py:925`, `:965`, `:997`, `:1013`). Accept and ignore the old helper field. Apply current-recipe checks only when deciding an install is current.
   - **Environments:** invalidate completion evidence BEFORE deleting the venv (today any environment receipt triggers a probe, `:636`). Reset stale lock metadata consistently (`engine_runner_target.py:383`). Recreate and sync whenever completion evidence is absent; publish completion only after verification.
6. **U5: one shared "ensure current installation and server" path,** called before readiness-dependent preparation. The production run path calls `ensure_local_engine_server()` before `local_engine_endpoint()` (`run.py:765`; `engine_local_server.py:53`). Acquire the lock, reread state, converge only if still needed. Keep the stored model binding when no override is given (`engine_cli.py:125`). Bridge installer steps into product progress: waiting, the current step, an actionable failure.
7. **U4: the deletion inventory gains** `engine_cli.py:23,150`, `engine_local_server.py:58`, `managed_preparation.py:361`, plus tests `test_engine_local_endpoint.py:83`, `test_engine_bootstrap.py:195`, `test_engine_custody.py:1409` and `test_managed_host_preparation`.
8. **M1': resolver consolidation sites** (all use `effective_models_root`):
   - `engine_runner.py:514` (and `:511`, `:759` in the partial work), `engine_platforms.py:104-105`, `managed_preparation.py:535`, `engine_custody.py:943` (publish the resolved binding), `run.py:716,895`.
   - Old-root spelling only inside the legacy migration (`engine_runner_target.py:35`).
   - Old receipt paths are read as old evidence (`engine_runner.py:972`).
   - RunPod's explicit volume (`generation.py:138`) and the H3 release-builder layout (`h3_release_remote.py:102,247,276`) are separate; leave them alone.

Interrupted convergence resumes at every boundary with these changes. Move stop and migration inside the install-lock scope (`engine_runner.py:829`). No rollback machinery, migration journal or second implementation.

## Manager ruling on U2 after its review (REWORK, 16:12Z)
Managed preparation already holds the exclusive install lock through execution and cleanup, so jobs and installs exclude each other through that one lock. The ruling:
- **No shared admission mode.** One lock.
- **Contention fails fast,** with the receipt read only on contention:
  - an install that finds a job holding the lock refuses with `engine_busy`, naming the queue;
  - a job that finds an install holding the lock (receipt says `installing`) refuses with `engine_busy`;
  - a job that finds another job waits, so local jobs still queue;
  - an install that finds another install waits.
- **The queue is read directly** with a loopback `GET /queue` from the install process, not through an embedded program.
- **Stop-only client:** an explicit stop-only constructor loads the live identity from the marker.

## U1 review (Astra, high effort, 16:24Z): ACCEPT WITH FIXES
The six focused failures all reproduce on `593749c4` (model-layout test fallout); none comes from U1. Two fixes are required and now running (`engine-u1-fixes.md`):
- **Old custody handles:** keep and validate recovery handles on legacy model steps.
- **Freshness:** one shared check that a receipt is current, at every admission boundary (endpoint, startup, status, local server).

**Integration note for the U1 + U2 combination:** in the converted custody test, add `assert sent == []` right after the refused probe and before stop.

## U2 re-review (Astra, 17:02Z): REWORK again; round-2 ruling
Four fixes are required: restore the local-run progress phases; keep failure receipts when preparation fails; exclusion survives an uncertain cleanup unwinding; and holder classification must cover the whole lock-held interval.
**Ruling:** the holder writes its kind (`install` or `job`) into the lock file right after acquiring the lock. A contender reads it only on contention, and an empty or unreadable kind counts as a job (wait). The receipt is no longer consulted.
U2 ships as a second merge, after A1–A3 and U1.

## Integration (17:38Z)
- **r13/engine-layout 31253d5a6** is merged into **r13/compose** as 913c6b8f.
- **Before landing,** U2 and r13/engine-fresh merge in origin/r13/compose. Its VibeComfy pin is a8a7be7c, and its digests are regenerated by scripts/vibecomfy_pin.py.
- **test_engine_recipe.py:88:** the recipe's two-element form (`--models-directory`, then `{models_root}`) is the intended one. The test now asserts the flag is immediately followed by the placeholder. The fix rides with engine-fresh.
