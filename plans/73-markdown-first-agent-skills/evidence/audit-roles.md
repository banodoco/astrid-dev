# MSC-4 rule-preservation audit — roles (P73-04)

Approved scope and method: [Step 1 decision](https://github.com/banodoco/astrid-dev/issues/1882#issuecomment-7154905027). Source main M: `2761114f93452d7c3110b71a9b55a5d4dc36490d`; INT pair source: `fd8a9a04accc2634e2cd9f7ba4916da3679f0da8`. Candidate base: `090c3f87a0b40cadd6b7587847ff9b57a277407b`. Source/target paths below are repository-relative; line numbers are one-based. Quoted excerpts identify individual consequential obligations; consult the cited full line for its context. Layout-only replacements are superseded, not new execution authority. No proof run by packet session.

## agent/start.md

Source: `skills/astrid-dev/SKILL.md` at M. Destination: `agent/start.md`.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Start here for any Astrid contribution. | 8 | 8 | kept |
| identify the person's goal, then find the existing issue, project and code. | 8 | 8 | kept |
| Bug, small fix, docs or maintenance | 14 | 14 | kept |
| file it, search first | 15 | 15 | kept |
| follow the task card and invoke | 16 | 16 | kept |
| inherit accepted decisions and permissions | 17 | 17 | kept |
| New independent outcome | 18 | 18 | kept |
| A difficult bug still needn't become a project | 18 | 18 | kept |
| read it first for release and version direction | 19 | 19 | kept |
| define or reassess the outcome, write its closure approach and route to closure | 20 | 20 | kept |
| define the accepted scope and tasks | 21 | 21 | kept |
| own the overall outcome; select the | 22 | 22 | kept |
| keep manager runs and handoffs moving, advise and check in | 23 | 23 | kept |
| Running one accepted project | 24 | 24 | kept |
| for a genuine blocker or consequential choice | 24 | 24 | kept |
| a lead critic and a few cheap helpers review it, then merge it, send it back or bring it to the owner | 25 | 25 | kept |
| measure completely, then gate on no new failures or retire old red by cause | 26 | 26 | kept |
| A release is one branch per repository that its plans and fixes merge into, tested as a whole and published on the owner's go | 27 | 27 | kept |
| your pull request goes into a plan or fix branch | 27 | 27 | kept |
| with explicit current authorization | 28 | 28 | kept |
| within the owner's standing budget | 29 | 29 | kept |
| find the rule's one home, change only that, prove it | 30 | 30 | kept |
| define who is accountable; shared workstreams are independently callable procedures; role-specific workstreams are operating variants | 32 | 32 | kept |
| govern every invocation | 32 | 32 | kept |
| Standalone skills retain | 32 | 32 | kept |
| Learn what the contributor wants; consult the | 36 | 36 | kept |
| Trace actual behavior and prior work before changing it. Search issues and projects; confirm source revision, dependencies and relevant proof. | 37 | 37 | kept |
| Agree the smallest complete result and test of success. | 38 | 38 | kept |
| Reuse accepted scope; challenge consequential designs without creating a mandatory second planning ritual. | 38 | 38 | kept |
| protect existing work and respect the current run's constraints. | 39 | 39 | kept |
| Record proof as the | 40 | 40 | kept |
| A green wrapper is not product proof. | 40 | 40 | kept |
| Link issue/project and implementation PRs, merged into the plan branch of the release they ship in | 41 | 41 | kept |
| use ordinary review and | 41 | 41 | kept |
| Start at the first stage | 43 | 43 | kept |
| find the closest issue or existing task first. | 47 | 47 | kept |
| Otherwise offer 2–3 bounded choices | 47 | 47 | kept |
| claim, propose, request a start decision, ask a question, submit multiple product PRs or finish a project | 49 | 49 | kept |
| Claiming is ownership, not authorization. | 49 | 49 | kept |
| No mandatory project conversation hub is created. | 49 | 49 | kept |
| The concise completion PR is an index of real evidence, not another database. | 49 | 49 | kept |
| add an entry file to the add-only | 49 | 49 | kept |
| Follow the | 51 | 51 | kept |
| This skill routes the work; it does not grant execution, integration or release permission. | 51 | 51 | kept |
| Never install skills or change a contributor's machine merely to orient them. | 51 | 51 | kept |

Count: 45 found; 45 kept; 0 restored; 0 moved; 0 superseded.


## agent/README.md

Source: `skills/shared/workstreams.md` at M. Destination: `agent/README.md`. Replacement references are to the scripts/CI on the pinned base; test names without a path belong to `scripts/test_agent_documents.py` or `scripts/test_skill_builder.py` unless specified. Mechanical indexes and old contract fields are not reintroduced. Flags below identify missing analogous enforcement for the orchestrator's ruling; no change to checks is authorized here.

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| is the entrypoint and routes requests. | 3 | 11 | kept |
| defines **who is responsible** | 4 | 12, 47 | kept |
| reusable, independently discoverable **shared workstreams** | 5 | 14, 20 | kept |
| They have a defined result and inherit the invoking role's authority. | 5 | 20, 47 | restored |
| owns shared rules, terms, templates and reusable workstreams | 6 | 15, 47 | kept |
| the shared workstreams have no second authoritative copy. | 6 | 47 | restored |
| they inherit the role and are not separately installed skills. | 7 | 13, 43 (default ordinary document; opt-in is intentional) | kept |
| Every workstream is a procedure with a defined outcome | 11 | 45, 47 | restored |
| Both use the same authored, machine-checked `## Workstream contract` | 11 | 45; scripts/agent_documents.py:93–103; test_roles_workstreams_and_references_share_one_document_format | superseded |
| the **first level-two section** after the title | 11 | 45; scripts/agent_documents.py:89–103; test_missing_or_empty_procedure_is_refused (ordered required headings replace first-section constraint) | superseded |
| An independently verifiable result that this workstream produces. | 16 | 45, 47 | restored |
| The trigger or context in which an authorized agent selects it. | 17 | 45 | kept |
| The assignment, source and permission facts needed before acting. | 18 | 45 | kept |
| A concise route through the actual execution instructions below. | 19 | 45, 47 | kept |
| What evidence or disposition proves the workstream is finished. | 20 | 45 | kept |
| These five labels must occur once, in that order, with substantive single-line values | 23 | 45; scripts/agent_documents.py:94–103 orders nonempty sections; test_missing_or_empty_procedure_is_refused. No new duplicate-heading check; flag to orchestrator (old single-field uniqueness replaced by section contract). | superseded |
| there must be actual execution instructions beyond the summary. | 23 | 45, 47 | kept |
| A second contract field after a blank line is also a duplicate. | 23 | 45; old duplicate field check not applicable to section contract; no analogous duplicate-heading enforcement (scripts/agent_documents.py:94–103). Flag to orchestrator. | superseded |
| it cannot decide whether the instructions are correct, the evidence sufficient, or the actor authorized. | 23 | 47 | restored |
| Keep detailed instructions under their existing headings after the contract summary. | 23 | 45, 47; scripts/agent_documents.py:94–103; test_missing_or_empty_procedure_is_refused (no separate duplicated summary) | superseded |
| Do not replace real steps or proof with placeholder summaries | 23 | 47 | restored |
| do not duplicate shared run policy. | 23 | 47 | restored |
| Standalone skills add `name: astrid-dev-<name>` to frontmatter, use a matching directory | 25 | 34, 43; scripts/agent_documents.py:71–87, 135–143; test_invalid_skill_value_and_manual_name_refused; test_duplicate_skill_stems_fail_without_name_override | superseded |
| may give their H1 a natural title. | 25 | 34; scripts/agent_documents.py:89–92 | kept |
| Role-specific documents use only `description:` in frontmatter and start with `# Workstream: <title>` | 25 | 34, 43, 45; scripts/agent_documents.py:71–82, 89–103; test_roles_workstreams_and_references_share_one_document_format | superseded |
| Both have a one-line description of at most 240 characters, ending in punctuation. | 25 | 34; scripts/agent_documents.py:74–79; test_missing_description_and_invalid_filename_fail (missing description); max length and punctuation directly enforced by parser | kept |
| Supporting guides inside nested workstream directories are not workstreams and do not need this contract. | 25 | 16, 43; scripts/agent_documents.py:42–49; test_roles_workstreams_and_references_share_one_document_format | superseded |
| A shared workstream skill inherits the invoking role's and run's authority; a role-specific document inherits its parent's. | 27 | 13–14, 20, 45 | kept |
| Neither can authorize its own execution, merges, spending or publication. | 27 | 20, 45, 60 | kept |
| parse frontmatter and ordered fields | 29 | 45; scripts/agent_documents.py:71–103; test_missing_or_empty_procedure_is_refused | superseded |
| the existing check registry enforces it as `workstream-structure`. | 29 | 45, 54; scripts/agent_documents.py:154–160; test_real_repository_markdown_catalog; test_staged_dispatch_names_canonical_manager_and_ci_checks_packages | superseded |
| The names-only shared-workstream index and role-specific descriptions are projections of these canonical files. | 29 | 20, 47; human navigation index replaces generated lists; test_staged_roles_use_one_shared_workstream_index. No automated role-summary consistency check; flag to orchestrator. | superseded |
| A shared workstream that an agent can invoke directly lives under `skills/shared/workstreams/astrid-dev-<name>/SKILL.md`. | 33 | 14, 34, 43; scripts/agent_documents.py:42–49, 71–87; test_location_does_not_determine_skill_status | superseded |
| Its folder name must exactly match its frontmatter `name: astrid-dev-<name>` | 33 | 43; scripts/agent_documents.py:71–87, 135–143; test_duplicate_skill_stems_fail_without_name_override | superseded |
| its `description:` is a nonempty single line. | 33 | 34; scripts/agent_documents.py:74–79; test_missing_description_and_invalid_filename_fail | kept |
| installs it as a flat, independently discoverable skill without changing its name. | 33 | 43, 54–57, 60; skills build/check/install; test_generate_canonical_metadata_and_links; test_existing_install_symlink_survives_exchange | superseded |
| A role may invoke it but cannot gain permissions merely by selecting it. | 33 | 20, 45, 60 | kept |
| There is no independently installed `capabilities/` category or standalone Planner role. | 33 | 12, 14, 43; test_real_repository_markdown_catalog (original roles and skills); no categorical denylist by design | superseded |
| Legacy relative symlinks preserve old Markdown links without maintaining duplicate skills | 33 | 7, 60; skills install links generated packages, MSC-6 rewrites old links; test_duplicate_skill_stems_fail_without_name_override; test_generate_canonical_metadata_and_links | superseded |
| `sync.sh` ignores them. | 33 | 54–57; skills build/check/install; scripts/agent_documents.py:109–151 discovers canonical Markdown and refuses source symlinks; test_reject_source_symlink | superseded |
| A role-specific workstream stays beneath its parent role as a `.md` file | 35 | 13, 43; test_orphan_role_workstream_is_refused | kept |
| Each role skill also contains a generated **Shared workstreams** section | 35 | 20; human index; test_staged_roles_use_one_shared_workstream_index | superseded |
| it does not duplicate descriptions or grant permissions. | 35 | 20, 47 (authoritative metadata one home; role navigation summaries are not new authority), 60 | restored |
| Every direct role-specific `workstreams/*.md` file | 39 | 13, 34, 43; scripts/agent_documents.py:42–49, 71–103; test_orphan_role_workstream_is_refused | superseded |
| has its own title and description as defined above. | 39 | 34; scripts/agent_documents.py:74–92 | kept |
| Keep full instructions in its body | 39 | 47 | restored |
| do not repeat its discovery description in the parent skill. | 39 | 47; human navigation summaries allowed, authoritative metadata remains in source; no automated role-summary consistency check, flag to orchestrator | superseded |
| Nested `workstreams/<guide>/` files are supporting documentation, not separately indexed workstreams. | 39 | 16, 43; scripts/agent_documents.py:42–49; test_roles_workstreams_and_references_share_one_document_format | superseded |
| keeps its shared responsibilities, defaults, selection rules and composability guidance as handwritten text. | 41 | 47 | restored |
| Only the list of file-backed workstreams is generated between | 41 | 20; one human navigation index instead; test_staged_roles_use_one_shared_workstream_index | superseded |
| Edit the workstream file, not its parent list. | 41 | 47; canonical document is the instruction/metadata owner; navigation maintained in role, no automatic index-consistency check (flag to orchestrator) | superseded |
| regenerates the parent indexes; the existing documentation workflow refreshes them on `main` | 43 | 20, 54–57; skills build/check/install and one human index; test_staged_dispatch_names_canonical_manager_and_ci_checks_packages; test_staged_roles_use_one_shared_workstream_index | superseded |
| PR CI **always** validate the full common contract and package metadata of every workstream, including new files. | 43 | 54; scripts/agent_documents.py:109–160; .github/workflows/docs.yml:31–32,69; test_staged_dispatch_names_canonical_manager_and_ci_checks_packages; test_valid_workstream_extension_adds_a_skill_without_removing_any | kept |
| The generated shared-workstream lists are validated against the standalone skills and registered as explicit role targets. | 43 | 20; test_staged_roles_use_one_shared_workstream_index; no registry required for new skills (test_valid_workstream_extension_adds_a_skill_without_removing_any) | superseded |
| The CI write-back allowlist remains explicit | 43 | 20; .github/workflows/docs.yml:117–156 still verifies declared generated-view paths; scripts/test_views.py test_target_symlink_inside_repository_is_refused_before_any_write, test_sync_reports_shared_target_once_when_both_regions_are_stale | kept |
| a new parent skill with workstreams must first be registered in `scripts/workstreams.py`'s `PARENT_SKILLS`. | 43 | 20, 43; scripts/agent_documents.py:109–151; test_valid_workstream_extension_adds_a_skill_without_removing_any, test_orphan_role_workstream_is_refused; intentional no manual registry | superseded |
| Every independently discoverable role or shared workstream skill retains its namespaced `name: astrid-dev-*` and matching leaf directory name. | 46 | 43; test_real_repository_markdown_catalog; test_canonical_agent_source_root_and_skill_prefix_are_stable; name now from filename stem, intentional original role renames | superseded |
| installs **flat symlinks** to the canonical packages for Claude/Codex discovery | 46 | 60; skills install; test_existing_install_symlink_survives_exchange; test_generate_canonical_metadata_and_links | superseded |
| the extra grouping directory does not appear in installed skill names. | 46 | 43; test_location_does_not_determine_skill_status | kept |
| Do not duplicate instructions or add folders for workstreams that need no variant. | 46 | 47 | restored |
| Follow the run contract. | 46 | 15, 20, 45, 47 | kept |

Count: 61 found; 22 kept; 11 restored; 0 moved; 28 superseded.

*Draft in progress: remaining 19 document audits follow before READY-PROOF.*
