# Triage: media / element / pack defects (friction r6), against release/14/main

Source: `origin/release/14/main` = commit 9f614dff7 (same commit as the checked-out `release/14/fix-1238-stale-registry-asset` HEAD). No local branch named release/14/main exists. Files read with `git show`, not from the dirty working tree. Snapshot copies: r6/tooling/src14/. Line numbers below are current; "was" = the friction log's citation.

## Search status
28 org-wide queries (banodoco) on verbatim strings and phrasings. No hit contained the verbatim error strings. Closest, unverified relevance:
- astrid-agent#394 closed: "Prove legacy timing exemptions in one pass" (M1 area)
- astrid-app#251 open: "Agent cannot commit a timeline swap to a task-output handle" (M3 area)
- astrid-agent#474 closed / astrid-runtime#98 closed: "verified descriptor-backed Runtime" (M6 area)
- astrid-dev#1234 open: "skill points at an old client; error suggests a reinstall" (friction minor 1)
- astrid-dev#1240 open: media list paging (not a listed defect)
Rate limit (30/min) forced retries; the search was not exhaustive.

## M1 asset swap on word-anchored occurrence clip
(a) No issue found. #394 closed is adjacent.
(b) sdk/timeline/_timing_evaluators.py:422 `raise TimingCompileError(f"missing exact word binding for {owner}.{field}")` (was 422, same).
    sdk/timeline/_commit_timing_validation.py:387-401 `_legacy_exemptions` ("Return unchanged declarations the base already failed to resolve"), was 402-416.
    :832 `raise TimingCompileError("word anchors require parent ownership")`; :843-846 exemption skip + `legacy_binding(...)`. Bindings loop was 840-866, now 825-850.
(c) Small fix: no. Inference: the exemption is keyed on unchanged declarations, so an asset-only change to an occurrence clip is not exempted. Host test: the commit-timing validation tests (not located).

## M2 capture_mismatch on doc.patch + media.admit
(a) None found.
(b) sdk/timeline/_commit_patch.py:592 `if all(self.calls[i]['op'] == 'doc.patch' ...)` (pure-patch branch, was 592-603); :606 `raise CommandError('semantic step assertion differs from execution', kind='capture_mismatch')` (was 604-606).
(c) No. Inference: the mixed step compares field claims on the old ref against an after-closure keyed by a new internal-revision ref.

## M3 media outside Runtime-verified inputs / handles
(a) astrid-app#251 open, adjacent.
(b) sdk/timeline/_doc_patch.py:356 `raise CommandError('patch references media outside Runtime-verified inputs', kind='dependency_changed', ref=ref)` (same line). Allowed set built at :350-355 from verified_media only.
    sdk/timeline/commit_session.py:255 `def _register_asset(...)`: only local file paths are verified.
(c) No. Two rules conflict (handle refused by patch; local path refused by replace_asset), per friction. Media import output lacks ids (minor 3): not traced to source.

## M4 legacy registry entries without generation/variant pins
(a) None found.
(b) sdk/timeline_media_replacement.py:47-66 `_target_pin` (was 47-65); :59-60 reads generationId/variantId with no fallback error.
    sdk/timeline/native_occurrence_media_commands.py:146-147 `elif (... entry.get('type') != kind ...)` (was 143-149); :149-151 `raise CommandError('unsupported old registry identity codec', kind='unsupported_media')`.
    packs/rendering/docs/scripts/timeline_document.py:61 `lacks an exact generation/variant pin; ...` (resolve_media_rebinds at :38).
(c) No. Needs a legacy-pin path or a re-pin step.

## M5 clip.delete refused whenever parent declares app.astrid.slots
(a) None found.
(b) sdk/timeline/_delete_commands.py:17-23 `_unrelated`, raise at :22 (same). :41-50 `_unreferenced`; slots checked at :48 for every clip removal.
(c) No. The guard is timeline-wide (the friction's point). Fix means checking slot use by the removed clip (inference). Host test: not located.

## M6 ElementPackNotInstalled for project-pack element; packs list --project
(a) None found.
(b) sdk/timeline_address.py:460-465 `ElementPackNotInstalled ... "no installed pack declares this element"` (friction cited none; this is the raise site).
    core/pack/cli_parser.py:136-138 `subparsers.add_parser("list", ...)`: no --project argument.
(c) No. Needs project-pack listing in pack CLI.

## M7 timelines elements / update-element / place-element
(a) None found.
(b) core/element/project_packs.py:741-744 `configured_realm()`; raise `'Pass --realm or configure ASTRID_WORKSPACE_DISCOVERY'` at :744 (was 843-848).
    :755 `for clip in parent.get('clips') or []:` parent-only listing (was 855-857).
    sdk/timeline_elements.py:30 `target = f'parent/clip:{clip_id}'`; :147-153 `_clip` raises 'Expected one existing parent effect clip' (was 161-168, 30).
    sdk/timeline_elements.py:398-400 `place_element(... *, realm, target, element, expected_head, ...)`: no params argument.
(c) Realm: probably small (use active realm from discovery, inference). Occurrence listing and params on place-element: not small.

## M8 project-pack CLI not reachable; default root ignores runtime data root
(a) None found.
(b) core/element/project_packs.py:33 `ROOT_ENV = "ASTRID_PROJECT_PACKS_ROOT"`; :56-57 `authoring_root()` defaults to XDG_DATA_HOME/astrid/project-packs (was 55-56). The file has no ASTRID_RUNTIME_DATA_ROOT reference.
    packs/timeline/ and core/pack/ CLI routing not traced for the project-pack command.
(c) Yes, small (inference): derive the default from the runtime data root or name the folder in the error; host test: tests for core/element/project_packs (not located).

## M9 pack validate passes what admit rejects
(a) None found.
(b) core/contracts/capability_schema.py:23 `DESCRIPTION_MAX_LEN = 500`; :162-166 raises `"{manifest_id}: description is {n} chars; max is {MAX}"` (was 163).
    core/element/schema.py:299-304 calls `validate_capability_text(..., error_cls=ElementValidationError)` (admit path only).
    core/pack/validate.py:1374 `validate_pack`: no call to validate_capability_text (grep: only element, execution and orchestrator schemas call it).
(c) Yes, small (inference): call the element description/keyword check from the validate path. Host test: tests for core/pack/validate (not located). Traceback-vs-one-line in admit: not traced.

## M10 "An older Astrid is still running" (SDK identity)
(a) None found.
(b) The refusal string is not in this repo (runtime repo file, not in this checkout). Agent side: sdk/host_bootstrap.py:1135 reads ASTRID_INSTALL_RELEASE only to choose an execution profile (`default = ("installed" if "ASTRID_INSTALL_RELEASE" in os.environ ...`). Friction's startup_identity.py:30 is not checked.
(c) Not determined from this checkout. Needs the Runtime repo.

## M11 timelines assets --json; timelines history --json head
(a) None found.
(b) packs/timeline/cli.py:3224 `_cmd_assets` (no --json handling in the function); `--json` wiring for assets not located.
    packs/timeline/cli_history.py:50-52 `if parsed.json: print(json.dumps({"ok": True, "data": data, ...}))`: the history envelope has no head field in the friction's reading (data shape not traced).
(c) Yes, small (inference): add --json to assets. Test host: not located.

## Friction citations that moved
Current lines differ from the logs for: capability_schema (163 -> 162), project_packs (843-848 -> 741-744; 855-857 -> 755; 55-56 -> 56-57), timing validation (402-416 -> 387-401; 840-866 -> 825-850), native_occurrence (143-149 -> 146-151), _timing_evaluators (422 same), _doc_patch (356 same), _delete_commands (22 same), timeline_elements (161-168 -> 147-153).
