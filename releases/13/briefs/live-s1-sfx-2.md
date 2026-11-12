# Fix, pass 2: SFX enum type and offline schema identity, solved structurally

You are a Codex worker with full access. Deploy Luna sub-agents at low effort for all reading, searching and mechanical checks. You judge and write the fix.

## Where pass 1 got to (in your working tree; saved at `/home/user/wt/briefs/wave3/live-s1-sfx-v1.patch`)
Pass 1 made the live SFX failure go away, but as two patches. The owner wants the structural fix:
1. **It added `COMBO` to one alias set,** in `vibecomfy/workflow.py:_types_match`. The enum socket type is spelled three ways in this repository, and about ten modules each keep their own alias set or spelling: `ingest/normalize.py:1563` (`CHOICE`), `porting/object_info/consume.py:43,1043` (`ENUM`), `porting/authoring_surface.py`, `porting/edit/editable_surface.py:234`, `porting/widgets/settings_contract.py:108`, `porting/wrappers/codegen.py:238`, `porting/wrappers/discovery.py:438`, `porting/emit/*` (`COMBO`). That's one fact with many owners, so the next comparator to be written gets it wrong again.
2. **It hand-added `pack_slug` and `git_commit` to one cached schema file** (`porting/cache/object_info/ComfyUI-HunyuanVideo_Foley@source-b94f7ac.json`). Nearly every one of the 49 cache files lacks `git_commit` on every entry, although each entry already carries the commit as `pack_version`. So the offline identity lookup almost always fails, and VibeComfy falls back to the live schema: **for nearly every template, the offline type checks never run on CPU.** That's why this mismatch reached a rented GPU.

## Outcome
1. **One owner for the socket-type vocabulary.**
   - One module defines the canonical type names and the only alias table, with one function that canonicalizes a socket type.
   - Every comparator and consumer calls it, and the local alias sets are deleted.
   - Comparisons become equality on canonical names.
   - Choose the canonical spelling of the enum type with evidence. ComfyUI's own `COMBO` is the default choice unless something stored and digest-bearing makes that costly.
   - **Don't change stored or digest-bearing values in templates, companions or caches** unless there's no other way. If you must, stop and report first; that would change semantic digests that Astrid admits.
   - Add a ratchet test: outside the vocabulary module, no module names an enum alias as a socket type.
2. **One field for a pack's commit in the object-info cache, and the offline lookup resolves for every cached pack.**
   - Find the identity lookup that printed `offline object-info identity did not resolve`. Find what it reads, why old cache files fail it, and which field is canonical: `pack_version` or `git_commit`.
   - Don't keep the same commit in two fields. Either the lookup reads the canonical field the files already have, or every cache file is migrated by the repository's own generator or migration code, never by hand.
   - Revert pass 1's hand edit of the Foley file if it's no longer needed.
3. **A CPU check that runs offline for every ready template:**
   - every node a ready template uses resolves its offline schema by identity;
   - every public input type-checks against that schema through the canonical vocabulary.

   It must fail on `a8a7be7c` (Foley at least) and pass after. Report how many ready templates resolved offline before and after, and any template the check catches that wasn't known.

## Proof
- The new checks fail before and pass after. The ratchet fails if an alias set is reintroduced; show it.
- These pass with no new failures against `a8a7be7c`: `tests/test_ready_templates.py`, `tests/test_workflow_core.py`, `tests/test_porting_object_info.py`, `tests/test_workflow_bundle.py`, and the test files of each module you change (name them). Known base failures: `test_native_wan_animate_template_declares_frame_count_binding`, the 3 `test_derived_template_live_identity_requires_package_lock_and_checkout[...]`, `test_v2_companion_keeps_generated_python_small_and_round_trippable`, `test_v2_source_contract_rejects_whole_file_integrity_mutations`, `test_porting_emitter.py::test_ideogram_fixture_native_boundary_is_materialized`, `test_ready_template_helpers.py::test_ready_template_root_supports_packaged_install`. Pass 1 saw two 60-second schema-hashing timeouts on the base; record them by id.
- `python -m tools.refresh_template_index --check` and `git diff --check` pass. No template semantic digest changes, or every change is listed and explained.

## Rules
- Do not commit or push. Leave the change in the working tree.
- Never weaken, skip or delete a test. If an existing test pins an alias spelling on purpose, stop and report it.
- **No RunPod or paid services of any kind:** no calls to api.runpod.io, rest.runpod.io or any RunPod endpoint, no `astrid generate`, no `astrid machines`. The proxy injects a real key, so a call spends real money. Package registries, GitHub and Hugging Face reads are allowed.
- No `.env`, credential files or `~/.codex`.
- **No full suites,** only the files named. The machine has 4 CPUs shared with other workers, and about 3 GB of disk is free. Use `TMPDIR=$PWD/.tmp-tests` and `--basetemp=$PWD/.tmp-tests/pt`, and delete them at the end.
- Python: `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH=$PWD`.
- No AI model or product names in code or comments. Stop after three failed attempts at the same thing, and report.

## Return
For each of outcomes 1 and 2: the cause in two sentences and the design you chose, with its one owner. Also the diff summary, before and after test ids, the offline-resolution counts before and after, and any digest changes.
