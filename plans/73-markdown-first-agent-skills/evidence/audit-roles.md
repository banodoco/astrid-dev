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


## agent/roles/leader.md

Source: `skills/roles/astrid-dev-lead/SKILL.md` at M. Destination: `agent/roles/leader.md`. Legacy generated skill navigation lists are layout, covered in the README table; the role's permission rule and canonical navigation link are retained.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Enter through astrid-dev. | 8 | 24 | kept |
| The Lead is the release manager named in releases/&lt;N&gt;.md | 8 | 24 | kept |
| an incumbent remains in charge until the owner records a handoff. | 8 | 24 | kept |
| Own the release outcome. | 12 | 28 | kept |
| Choose priorities, resolve cross-plan questions and keep the next work ready, within accepted scope. | 12 | 28 | kept |
| Keep responsibility clear. | 13 | 29 | kept |
| Each plan run names one accountable agent: a plan manager or, under fresh-packet dispatch, you, with each ChatGPT session owning only its packet. | 13 | 29 | kept |
| Judge results. | 14 | 30 | kept |
| Accept a submission or name its rework | 14 | 30 | kept |
| landed work shows in tasks.md, not a second checklist. | 14 | 30 | kept |
| Keep progress legible. | 15 | 31 | kept |
| Maintain the existing release brief, run board and decisions, and use the run contract's boards and check-ins with every role | 15 | 31 | kept |
| tell the owner what moved, what is blocked and which decisions need them. | 15 | 31 | kept |
| Own release integration. | 16 | 32 | kept |
| Follow Release for landing order, branch health, qualification and a separate owner's go to publish. | 16 | 32 | kept |
| Tell an environment block from slow work. | 17 | 33 | kept |
| At each check-in, compare every plan and packet with the last. | 17 | 33 | kept |
| Work that has not moved is blocked by the work or by the environment: a session that cannot push, start, resume or be woken | 17 | 33 | kept |
| a missing tool, credential or permission | 17 | 33 | kept |
| CI capacity. | 17 | 33 | kept |
| Fix an environment cause where it lives (the setup, the access, the skill) or bring the owner the exact step. | 17 | 33 | kept |
| Never dispatch into the same wall again. | 17 | 33 | kept |
| They apply in every workstream. | 19 | 35 | kept |
| A lane is the plans one orchestrator session answers for. | 23 | 39 | kept |
| You choose the lanes and each orchestrator's route, and keep both on the run board. | 23 | 39 | kept |
| Same lane when plans: | 25 | 41 | kept |
| edit the same files, or one builds on another: the lane runs them in order and owns the merges between them; | 26 | 42 | kept |
| need the same fixture, machine or live setup; | 27 | 43 | kept |
| are small and independent, so a session each would cost more in setup and in the owner's attention than it saves. | 28 | 44 | kept |
| They run side by side, one manager each. | 28 | 44 | kept |
| Its own lane when a plan: | 30 | 46 | kept |
| is a loop or taste plan, worked in rounds until it is right: it absorbs its orchestrator, and a plan sharing the lane starves; | 31 | 47 | kept |
| needs a quiet machine: measure in a separate session; | 32 | 48 | kept |
| would put a third manager on one machine at once. | 33 | 49 | kept |
| Start a fresh session at a landing once a lane's session has used about half its context | 35 | 51 | kept |
| a long session loses its early decisions. | 35 | 51 | kept |
| Never hand over mid-plan. | 35 | 51 | kept |
| Count lanes by the owner's attention. | 37 | 53 | kept |
| Each is a conversation she follows and answers. | 37 | 53 | kept |
| Lanes share CI runners, so stagger their release-branch runs. | 37 | 53 | kept |
| The orchestrator's route is judged like the manager's, by what the orchestrator itself must do: | 39 | 55 | kept |
| \| X \| The default. Its plans are complete: it starts and resumes managers, tells a stalled manager from a slow one, settles routine questions, | 43 | 59 | kept |
| \| S \| It chooses direction from evidence each round (a loop plan), or holds release-level correctness itself: landing order, pins, data or a migration. | 44 | 60 | kept |
| Never N: a hosting orchestrator answers for its runs. | 46 | 62 | kept |
| A taste lane's judgment is its T manager's | 46 | 62 | kept |
| its orchestrator is X. | 46 | 62 | kept |
| A workstream adds situation-specific steps under this role, not another role or approval system. | 50 | 66 | kept |
| Direct release leadership is the default when a separate dispatcher is unnecessary: use Release and work directly with the relevant managers. | 52 | 68 | kept |
| For fresh-session dispatch, choose the workstream below. | 52 | 68 | kept |
| Lane orchestrators in Claude cloud — Launch and steer one Claude-hosted orchestrator per lane, each running a Codex manager through a carded plan, with the | 56 | 71 | kept |
| Fresh-session ChatGPT packet dispatch — Prepare and lead fresh-session packet delivery across accepted release work without delegating the Lead's review or integration authority. | 57 | 72 | kept |
| Follow the run contract and existing owner permissions throughout. | 60 | 75 | kept |
| Use these independent skills as needed within your existing role and authority | 64 | 79 | kept |
| selecting a skill does not grant new permissions. | 64 | 79 | kept |

Count: 54 found; 54 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/orchestrator.md

Source: `skills/roles/astrid-dev-orchestrate/SKILL.md` at M. Destination: `agent/roles/orchestrator.md`. Legacy generated skill navigation lists are layout, covered in the README table; the role's permission rule and canonical navigation link are retained.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Your job: get authorized work into manager sessions and keep it moving. | 8 | 24 | kept |
| The default is a continuing project manager | 8 | 24 | kept |
| the fresh-packet workstream uses a new ChatGPT manager session for each packet, with the Lead owning plan-level integration. | 8 | 24 | kept |
| Deploy: brief managers from accepted project tasks, or a Lead-prepared dispatch queue | 9 | 25 | kept |
| do not invent scope. | 9 | 25 | kept |
| Supervise: at the agreed cadence, find work that is ready, moving, submitted or stalled and take the next useful action. | 10 | 26 | kept |
| Unblock: resolve routine delivery friction | 11 | 27 | kept |
| escalate real technical, cross-plan or owner decisions. | 11 | 27 | kept |
| Improve the brief or skill when the same question recurs, rather than adding supervision overhead. | 11 | 27 | kept |
| One exception: if you host the manager, you answer for the run. | 13 | 29 | kept |
| When Codex runs the project inside your session, you are its accountable agent, not an idle advisor (below). | 13 | 29 | kept |
| Across a release, the Release Lead owns the release, and chooses your lane and your route. | 15 | 31 | kept |
| An orchestrator coordinates its assigned managers | 15 | 31 | kept |
| a named release manager keeps authority until the owner transfers it. | 15 | 31 | kept |
| You orchestrate | 17 | 33 | kept |
| the manager manages. | 17 | 33 | kept |
| If you catch yourself writing a manager's dispatch plan (which tracks run in parallel, per-worker steps, when to escalate), the manage skill is missing a | 17 | 33 | kept |
| rule: send the manager one line naming the goal, and add the rule to the manage skill by PR. | 17 | 33 | kept |
| You act for the owner across projects and don't run tasks. | 19 | 35 | kept |
| Follow the run contract | 19 | 35 | kept |
| in run.yaml your role is advisor. | 19 | 35 | kept |
| Take the path that matches the request: | 19 | 35 | kept |
| \| "Do this project", or an outcome with no plan yet \| 1. Start a project \| | 23 | 39 | kept |
| \| "Farm these packets out to ChatGPT managers" \| Multi-manager dispatch workstream under the Release Lead \| | 24 | 40 | kept |
| \| A blocked planner, manager or worker asks a question \| 2. Advise \| | 25 | 41 | kept |
| \| The owner wants regular updates on a run \| 3. Check in \| | 26 | 42 | kept |
| \| The project's completion PR merged, or the owner says stop \| 4. Close \| | 27 | 43 | kept |
| Report and check in as the run contract's coordination rules say. | 29 | 45 | kept |
| Between check-ins, stay idle unless the active workstream calls for another action. | 29 | 45 | kept |
| Progress lives in each plan's tasks.md | 29 | 45 | kept |
| the dispatch queue records handoffs, not a second task history. | 29 | 45 | kept |
| A queue is yours to keep moving. | 31 | 47 | kept |
| For an ordered queue (phases of a plan, or several projects): | 31 | 47 | kept |
| Prepare the next item before the current one ends: its cards re-planned against what just landed, its Run start line, and its start message. | 32 | 48 | kept |
| Get the go once: one standing go from the owner for the whole queue, given in the manager's session and recorded on each Run start | 33 | 49 | kept |
| Without it, every item waits for her. | 33 | 49 | kept |
| At each check-in, confirm the manager has moved on. | 34 | 50 | kept |
| A finished item with an idle manager and a prepared next item is a stall: send the one next action. | 34 | 50 | kept |
| An item gated on an outside event (a release publishing, an owner setting) is still built on its plan branch, with only publication to main | 35 | 51 | kept |
| Say what is gated, and on whom, in every report. | 35 | 51 | kept |
| The Release Lead (the release manager named on the brief) owns release sequencing, release/&lt;NN&gt;/main, CI gates, branch records, tester builds and the publication request. | 39 | 55 | kept |
| You manage assigned managers and escalate release-level decisions to that Lead | 39 | 55 | kept |
| do not duplicate its board or take over a plan manager's integration. | 39 | 55 | kept |
| If you are already the named release manager, continue under Release until the owner records a handoff. | 39 | 55 | kept |
| When the Lead has prepared accepted release packets, use the fresh-session dispatch workstream instead of this standard whole-project handoff. | 43 | 59 | kept |
| Its sessions do not persist across packets. | 43 | 59 | kept |
| Plan it, or confirm its plan. | 45 | 61 | kept |
| Start from strategy.md and the catalog. | 45 | 61 | kept |
| With no accepted plan, write one with Plan (you may plan it yourself) and get the owner's scope decision. | 45 | 61 | kept |
| A draft plan authorizes nothing, and no manager starts before its plan is merged. | 45 | 61 | kept |
| - Fix the scope when the run starts. | 46 | 62 | kept |
| If the owner adds scope to a running release, say what it reopens (tests, re-pins, review) and offer the next release instead | 46 | 62 | kept |
| add it only if the owner decides to. | 46 | 62 | kept |
| Check the cloud setup (next sections) for each repository the plan changes. | 47 | 63 | kept |
| Farm it out. | 48 | 64 | kept |
| Create one manager session per project, and one project per manager at a time. | 48 | 64 | kept |
| Give it: | 48 | 64 | kept |
| - the plan's path; | 49 | 65 | kept |
| - its release, the brief and release/&lt;NN&gt;/main, the plan branch (release/&lt;NN&gt;/plan-&lt;PP&gt;), and the exact starting versions; | 50 | 66 | kept |
| - the owner's limits (budget, CPU or GPU, what needs a go); | 51 | 67 | kept |
| - the tests, already chosen. | 52 | 68 | kept |
| Check that tasks.md names the test inventory and each task's exact proof files | 52 | 68 | kept |
| if any are missing, you or the planner name them now, because choosing tests is judgment. | 52 | 68 | kept |
| Tell the manager to run only those, at the load-bearing moments, and never a full suite locally; | 52 | 68 | kept |
| - your session id for questions, as its advisor; | 53 | 69 | kept |
| - its route, chosen below. | 54 | 70 | kept |
| Its first step is Manage step 1: a run file plus a smoke worker per repository. | 56 | 72 | kept |
| Send all of this in the start message, not a long brief. | 56 | 72 | kept |
| Schedule check-ins if the owner wants them (path 3). | 57 | 73 | kept |
| Decide this once per run, separately from its tasks' routes. | 61 | 77 | kept |
| Judge it by what the manager itself must do, not by how hard the tasks are: a manager can send an S task to an | 61 | 77 | kept |
| \| N \| Works through a task list: dispatch, run the named proof, land, record. Every decision is already in the plan. \| | 65 | 81 | kept |
| \| X \| Iterates: gets failing tests or a broken environment working, re-plans a failed task, tells its own mistake from a real blocker, knows | 66 | 82 | kept |
| \| S \| Holds a correctness problem across the whole run, where one wrong call is expensive or hard to undo: a release, several repositories, | 67 | 83 | kept |
| \| T \| Judges refinement: right only when it reads or looks right, as in copy, a screen's polish or a skill's voice. \| | 68 | 84 | kept |
| Pick the lowest route that fits, and say why in one line. | 70 | 86 | kept |
| If two rows fit, take the higher. | 70 | 86 | kept |
| An N manager needs a complete plan: every card names its scope, its proof files and every file its acceptance text touches. | 71 | 87 | kept |
| Otherwise the run needs an X manager. | 71 | 87 | kept |
| A manager below a task's route still dispatches it, to a worker on that task's route, and doesn't do or judge it itself. | 72 | 88 | kept |
| Name the sub-agent or session for each T task and each review in the plan. | 72 | 88 | kept |
| Record the choice on the Run start line, and the model under roles.manager in run.yaml. | 73 | 89 | kept |
| Don't swap managers mid-run: the new one loses the run's context. | 74 | 90 | kept |
| Escalate hard failures to stronger workers or to you | 74 | 90 | kept |
| if its questions show the route was too low, raise it for the next run or phase. | 74 | 90 | kept |
| The run contract defines the routes and the model each one uses | 76 | 92 | kept |
| this is its copy, for the routes you assign: | 76 | 92 | kept |
| Default model for each route, using the newest available model of that family: | 80 | agent/shared/run-contract.md:13 (via 94) | moved |
| \| N \| Everything below very hard, including ordinary hard work: research, reading, running checks, most changes and fixes \| Haiku \| Luna \| | 84 | agent/shared/run-contract.md:17 (via 94) | moved |
| \| X \| Very hard: intricate changes, subtle bugs, coupled or non-obvious reasoning \| Sonnet \| Terra \| | 85 | agent/shared/run-contract.md:18 (via 94) | moved |
| \| S \| Super hard: deep design, or correctness that needs the deepest reasoning \| Opus \| Sol \| | 86 | agent/shared/run-contract.md:19 (via 94) | moved |
| \| T \| Taste: small, editorial refinement of something that already exists, such as user-facing copy, error and refusal messages, names, a screen's layout or | 87 | agent/shared/run-contract.md:20 (via 94) | moved |
| Reviews, plan judgment and advice use a separate high-judgment role: Opus (Claude) or Astra (Codex) | 89 | agent/shared/run-contract.md:22 (via 94) | moved |
| configure it in run.yaml as completion_reviewer, plan_judgment and advisor. | 89 | agent/shared/run-contract.md:22 (via 94) | moved |
| Reviews. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| A review's verdict runs on the high-judgment role. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| A check of a bounded fix against a named oracle (its failing case or probe) may run on X. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| N may gather facts for a review (check status, failure IDs, diff scope) but never gives the verdict. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| Check a pure sync by tree equality. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| A bounded-fix check runs the focused tests on both base and head. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| A bounded-fix check goes to the high-judgment role only when its own tests cannot show it is right (see the per-card rule under review and | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| size alone is not a reason. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| A meter, gate or check is reviewed by injecting the failures it must catch. | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| The run names the actual reviewer model, flags and permissions where it records its bindings (run.yaml, or the run board for a dispatch run). | 91 | agent/shared/run-contract.md:24 (via 94) | moved |
| *From Routing and bindings | 93 | 94 | kept |
| edit it there.* | 93 | 94 | kept |
| A run starts with one short message | 98 | 98 | kept |
| the plan carries the rest. | 98 | 98 | kept |
| A long brief repeats the plan, drifts from it, and can contradict the skills. | 98 | 98 | kept |
| Record the run first. | 100 | 100 | kept |
| Fill the Run start line in the plan's inputs.md (its fields) and merge it. | 100 | 100 | kept |
| Draft the message for the owner to paste. | 101 | 101 | kept |
| A message you send yourself arrives as data from a peer, and the session rightly won't treat it as a go (authority). | 101 | 101 | kept |
| You are accountable for Plan &lt;PP&gt;, &lt;phase or tasks&gt;: you answer for it finishing. | 104 | 104 | kept |
| Follow the astrid-dev-manage skill. | 105 | 105 | kept |
| The plan is plans/&lt;PP&gt;-&lt;name&gt;/ on astrid-dev main at &lt;sha&gt;; | 105 | 105 | kept |
| start from the Run start line in inputs.md and the dispatch notes in tasks.md. | 106 | 106 | kept |
| It ships in Release &lt;NN&gt; (releases/&lt;NN&gt;.md | 107 | 107 | kept |
| release manager: session &lt;id&gt;). | 107 | 107 | kept |
| Cut the plan branch | 107 | 107 | kept |
| release/&lt;NN&gt;/plan-&lt;PP&gt; from release/&lt;NN&gt;/main at &lt;sha&gt; and land work there. | 108 | 108 | kept |
| You may &lt;what it may do without asking&gt;. | 108 | 108 | kept |
| Come to me for &lt;what needs the owner's go&gt;. | 109 | 109 | kept |
| Your advisor for hard questions is session &lt;id&gt;. | 109 | 109 | kept |
| Add nothing the plan should hold. | 112 | 112 | kept |
| If the message needs a rule the plan or a skill lacks, put the rule there by PR and point to it. | 112 | 112 | kept |
| Don't add a second accountable agent. | 113 | 113 | kept |
| A separate plan manager answers for its run and you advise or supervise | 113 | 113 | kept |
| a packet session is a bounded delegate of the run's accountable agent (the Lead, under fresh-packet dispatch), not another plan owner. | 113 | 113 | kept |
| The Release Lead owns release delivery, not a second copy of the plan run. | 113 | 113 | kept |
| For a Claude Cloud host, follow the Codex-in-Claude workstream. | 117 | 117 | kept |
| The run contract still decides authority and permissions. | 117 | 117 | kept |
| Choose the workstream that fits the environment and assignment | 121 | 121 | kept |
| these are paths within this role, not sub-skills or new authorities (convention). | 121 | 121 | kept |
| Standard project handoff is the default: start and advise one accepted plan manager. | 123 | 123 | kept |
| Separate Codex Cloud sessions — Coordinate separate Codex Cloud sessions through the shared GitHub mailbox and durable session handoffs. | 127 | 126 | kept |
| Codex hosted inside Claude Cloud — Host Codex workers or a manager inside Claude Cloud while preserving explicit ownership, permissions and recovery. | 128 | 127 | kept |
| Run a lane for the Release Lead — Run one lane of a release for the Release Lead end to end, deciding inside the plan | 129 | 128 | kept |
| Dispatch to fresh ChatGPT sessions — Dispatch and supervise Lead-approved packets in fresh ChatGPT sessions while leaving review and integration to the Lead. | 130 | 129 | kept |
| The Codex Cloud environment workstreams select how sessions run and can accompany fresh-session packet dispatch. | 133 | 132 | kept |
| The Codex Cloud guide and Codex-in-Claude guide retain their technical commands and scripts. | 133 | 132 | kept |
| Live supervision remains the responsible manager's job | 133 | 132 | kept |
| no mailbox or timer by itself wakes a stopped session. | 133 | 132 | kept |
| For the choice between hosted Codex workers and a Codex manager, including keep-alive, mailbox and recovery, follow the Codex-in-Claude workstream. | 137 | 136 | kept |
| This anchor is retained for existing references. | 137 | 136 | kept |
| Answer the one bounded question you were given: a genuine blocker, conflicting evidence, or a consequential judgment the plan can't settle. | 141 | 140 | kept |
| This is not routine per-task approval. | 141 | 140 | kept |
| Refresh the facts first: the exact candidate, source and dependency identities, dirty state, the brief, the first failing command, the repair history, and the review | 143 | 142 | kept |
| Diagnose from evidence. | 144 | 143 | kept |
| A claim in the request is a claim until code, logs or a run supports it. | 144 | 143 | kept |
| If the cause isn't visible, the next action is to make it visible. | 144 | 143 | kept |
| Question the question. | 145 | 144 | kept |
| Why did it reach you: missing evidence, an unclear card, a gap in a skill or the plan? | 145 | 144 | kept |
| Sometimes the right answer is a different question. | 145 | 144 | kept |
| Unblock it once and for all. | 146 | 145 | kept |
| Behind every question is a cause: a missing rule, a thin card, a misleading tool, or authority it wasn't given. | 146 | 145 | kept |
| Answer, then fix that cause at its source in the same turn (the task card, the plan, or a skill by PR) and say how | 146 | 145 | kept |
| If you can't fix it now, add an entry to the process ledger. | 146 | 145 | kept |
| A question answered twice is a fix you still owe. | 146 | 145 | kept |
| Return one concrete next action, with its route, focused acceptance check, dependencies and return condition. | 147 | 146 | kept |
| For a high-judgment choice, give the simplest viable option, its trade-off, and a challenge against over-engineering. | 147 | 146 | kept |
| Stay inside the run contract's limits (review and promotion boundaries, checks and failure repair), and never invent a model ID. | 148 | 147 | kept |
| For delegated multi-manager release work use the dispatch checklist | 152 | 151 | kept |
| the Lead retains release-wide review and issue intake. | 152 | 151 | kept |
| Otherwise use this general project check-in path. | 152 | 151 | kept |
| Record the agreed cadence and end condition on the plan's Run start line, and as checkin in the run's run.yaml once a run exists. | 154 | 153 | kept |
| First verify a scheduler and a supported way to resume this session | 154 | 153 | kept |
| only then configure and test recurring check-ins. | 154 | 153 | kept |
| Without a verified path, poll in the foreground while active and tell the owner when a manual nudge is needed (what works). | 154 | 153 | kept |
| A hosted Codex manager's keep-alive check-in is a different timer. | 154 | 153 | kept |
| These documents never start a check-in themselves. | 154 | 153 | kept |
| Each check-in compares the run with the previous check-in. | 156 | 155 | kept |
| To gather the facts (logs, CI runs, the manager's recent events), send N helpers | 156 | 155 | kept |
| keep the judgment yourself. | 156 | 155 | kept |
| Liveness (every check-in): if the manager is idle while work is in flight, wake it with one next action. | 157 | 156 | kept |
| Strategy: compare authored decisions in strategy.md with catalog priority (plans/priority.md) | 158 | 157 | kept |
| report a substantive mismatch to the owner. | 158 | 157 | kept |
| Do not edit decisions yourself (hierarchy). | 158 | 157 | kept |
| Issues: triage the issues opened or updated since the last check-in under the issue rules. | 159 | 158 | kept |
| Pull each active release’s issue list with python3 scripts/release_issues.py &lt;N&gt;. | 159 | 158 | kept |
| Progress record (every check-in): tasks.md must match reality (merged PRs ticked, open and blocked tasks showing their state | 160 | 159 | kept |
| the manager's rule). | 160 | 159 | kept |
| If it lags, the nudge is to bring it up to date. | 160 | 159 | kept |
| Report progress from it, not from memory. | 160 | 159 | kept |
| Moving: tasks finished or candidates landed since last time. | 161 | 160 | kept |
| Stuck: the same failure twice, the same open question, or idle agents. | 161 | 160 | kept |
| Blocked: waiting on a person, an event or a dependency, and for how long. | 161 | 160 | kept |
| Drifting: work outside its scope, or undoing a recorded decision. | 162 | 161 | kept |
| Wasteful: reruns with nothing changed, or a costlier route than the task needs. | 162 | 161 | kept |
| Parallelism: ready independent work left idle, or a dependency that could be unblocked. | 163 | 162 | kept |
| Give the manager the goal | 163 | 162 | kept |
| it chooses and supervises its workers. | 163 | 162 | kept |
| For each manager or cross-track blocker, take the next useful action: | 165 | 164 | kept |
| On track: note one line | 166 | 165 | kept |
| send the manager nothing. | 166 | 165 | kept |
| Needs a nudge: send the manager one next action to unblock or improve the run. | 167 | 166 | kept |
| Needs the owner: bring one decision with your recommendation. | 168 | 167 | kept |
| Improve astrid-dev as you go. | 170 | 169 | kept |
| Friction in astrid-dev itself gets a process ledger entry | 170 | 169 | kept |
| fix small ones in the same check-in by the improve skill. | 170 | 169 | kept |
| After three check-ins in a row with nothing to report, you may recommend a slower cadence | 172 | 171 | kept |
| keep the agreed one until the owner changes it or its end condition is met. | 172 | 171 | kept |
| A check-in may nudge a manager to continue already authorized work through a verified resume mechanism. | 172 | 171 | kept |
| Cancel the check-ins when the project is done. | 176 | 175 | kept |
| When the project is complete, cancel every check-in you scheduled. | 176 | 175 | kept |
| Do the same when its end condition is met or the owner says stop. | 176 | 175 | kept |
| A project is complete when its completion PR merges. | 176 | 175 | kept |
| Confirm none remain, and tell the owner they have stopped. | 176 | 175 | kept |
| Use these independent skills as needed within your existing role and authority | 180 | 179 | kept |
| selecting a skill does not grant new permissions. | 180 | 179 | kept |

Count: 210 found; 193 kept; 0 restored; 17 moved; 0 superseded.


## agent/roles/manager.md

Source: `skills/roles/astrid-dev-manage/SKILL.md` at M. Destination: `agent/roles/manager.md`. Legacy generated skill navigation lists are layout, covered in the README table; the role's permission rule and canonical navigation link are retained.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Terms follow the glossary. | 8 | 24 | kept |
| Follow the run contract for authorization, proof and review. | 8 | 24 | kept |
| Own the engineering quality of the assignment you were given. | 12 | 28 | kept |
| Work from its accepted task card and source revisions, diagnose before changing code, verify what actually ships, and report the result with evidence. | 12 | 28 | kept |
| Don't take ownership of a larger project merely because you were assigned part of it. | 12 | 28 | kept |
| One model per shared surface. | 14 | 30 | kept |
| Shared contracts and screens use one agreed design | 14 | 30 | kept |
| ask the Lead/advisor before dispatch when it is unsettled. | 14 | 30 | kept |
| Reports are claims. | 15 | 31 | kept |
| Check against code, diffs and actual tests, not a worker's summary. | 15 | 31 | kept |
| See the failure first. | 16 | 32 | kept |
| Make its cause visible before fixing it. | 16 | 32 | kept |
| Prove the user path. | 17 | 33 | kept |
| Evidence names the exact candidate, command, environment and outcome | 17 | 33 | kept |
| tests alone may not demonstrate a working user journey. | 17 | 33 | kept |
| Use proportionate judgment. | 18 | 34 | kept |
| Choose the cheapest viable route | 18 | 34 | kept |
| escalate repeated misses or consequential decisions. | 18 | 34 | kept |
| Decisions must survive the session. | 19 | 35 | kept |
| Record consequential rulings in the existing plan record (whole project) or packet handoff (fresh session) | 19 | 35 | kept |
| never treat another agent's advice as authority. | 19 | 35 | kept |
| Progress has one home. | 20 | 36 | kept |
| A whole-project manager owns its plan's tasks.md progress PRs. | 20 | 36 | kept |
| A fresh packet manager submits PRs and evidence | 20 | 36 | kept |
| the Lead reconciles the plan after acceptance. | 20 | 36 | kept |
| Test what people actually use. | 21 | 37 | kept |
| Exercise the real entry point early where the accepted task requires it. | 21 | 37 | kept |
| Independent review is not optional when required. | 22 | 38 | kept |
| Read any worker's diff yourself, and commission an independent reviewer for the exact range under the existing review rules | 22 | 38 | kept |
| a packet session leaves this to the Lead. | 22 | 38 | kept |
| Choose the specific operating pattern. | 26 | 42 | kept |
| Every workstream inherits the responsibilities above (convention). | 26 | 42 | kept |
| Whole project is the default for an accountable plan manager | 26 | 42 | kept |
| use a fresh ChatGPT packet only for Lead-assigned bounded work. | 26 | 42 | kept |
| Run one packet in AI Studio — Drive one planet-lab packet through a fresh Google AI Studio session, push its branch and report it for | 30 | 45 | kept |
| Reflect on AI Studio lab packets — Gate each AI Studio lab packet and periodically replan the lab queue, merging accepted work into the lab | 31 | 46 | kept |
| Execute one packet in ChatGPT — Implement one bounded packet in a fresh ChatGPT session and return task pull requests and evidence for Lead review. | 32 | 47 | kept |
| Run a loop plan — Run a loop plan whose end state is known but whose tasks come from each live round of scenarios, strategist | 33 | 48 | kept |
| Manage a whole project — Manage a complete accepted plan, including worker coordination, tested integration, progress records and project closure. | 34 | 49 | kept |
| Whole-project decision log and escalation details: whole-project workstream. | 39 | 54 | kept |
| Packet-specific boundaries: packet workstream. | 39 | 54 | kept |
| Whole-project execution, proof, task integration and progress steps: whole-project workstream. | 43 | 58 | kept |
| For a fresh packet use its bounded handoff. | 43 | 58 | kept |
| Whole-project completion evidence: whole-project workstream. | 47 | 62 | kept |
| Every manager reports hourly by the run contract's coordination rules | 47 | 62 | kept |
| packet sessions submit PRs/proof on their board and stop. | 47 | 62 | kept |
| Use these independent skills as needed within your existing role and authority | 51 | 66 | kept |
| selecting a skill does not grant new permissions. | 51 | 66 | kept |

Count: 48 found; 48 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/worker.md

Source: `skills/roles/astrid-dev-worker/SKILL.md` at M. Destination: `agent/roles/worker.md`. Legacy generated skill navigation lists are layout, covered in the README table; the role's permission rule and canonical navigation link are retained.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Enter through astrid-dev. | 8 | 24 | kept |
| A worker owns a bounded assignment, not the project, release, or another agent's task list. | 8 | 24 | kept |
| Read the assigned task card and run contract: outcome, permitted repository/paths, starting commit, proof, limits and manager contact. | 10 | 26 | kept |
| For a code change, use Iterate. | 11 | 27 | kept |
| For other tasks, use the relevant shared workstream. | 11 | 27 | kept |
| Do not invent a second implementation workflow. | 11 | 27 | kept |
| Verify the change using the task's focused checks | 12 | 28 | kept |
| report exact SHA, PR/commit, results, failures and what remains uncertain. | 12 | 28 | kept |
| Escalate real blockers to the assigning manager and continue independent authorized work. | 12 | 28 | kept |
| Stop at the assigned boundary | 13 | 29 | kept |
| the manager or Lead handles integration, canonical task progress and decisions beyond the packet. | 13 | 29 | kept |
| Workers need no extra workstream merely to change tool or environment | 15 | 31 | kept |
| the chosen workstream and task brief supply that detail. | 15 | 31 | kept |
| A fresh ChatGPT packet manager instead follows Manage's packet workstream. | 15 | 31 | kept |
| Use these independent skills as needed within your existing role and authority | 19 | 35 | kept |
| selecting a skill does not grant new permissions. | 19 | 35 | kept |

Count: 16 found; 16 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/leader/multi-manager-release.md

Source: `skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md` at M. Destination: `agent/roles/leader/multi-manager-release.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: Lead-prepared, authorized release packets with one durable dispatch queue and review-ready task evidence. | 9 | 13 | kept |
| When to use: When the Lead coordinates accepted release work through fresh ChatGPT manager sessions rather than a single long-lived manager. | 10 | 9 | kept |
| Inputs: An approved release brief, current plan task records, packet scope and dependencies, owner authorization, branch destinations and evidence requirements. | 11 | 17 | kept |
| Procedure: Prepare bounded packets and one mailbox, run Lead check-ins, review delivered task PRs and integrate only authorized work using the sections below. | 12 | 21 | kept |
| Completion: The queue and task records reflect every packet, its evidence and disposition, with review/integration decisions owned by the Lead. | 13 | 25 | kept |
| Use when the Lead prepares accepted plan work for an Orchestrator to assign to a fresh ChatGPT manager session per packet. | 15 | 27 | kept |
| The Lead responsibilities continue to apply. | 15 | 27 | kept |
| A lane can be the Lead for its own plan. | 17 | 29 | kept |
| In a release run by lane orchestrators, a lane's orchestrator may take the Lead's part here for its own plan: it writes and reviews packets, | 17 | 29 | kept |
| merges into its plan branch and runs the proofs needing an installed stack or the network. | 17 | 29 | kept |
| It gets its own dispatch manager and mailbox | 17 | 29 | kept |
| the release Lead keeps only the gate into release/&lt;N&gt;/main (Release 15, Plans 87 and 89). | 17 | 29 | kept |
| Prepare packets. | 21 | 33 | kept |
| Start from what exists: bring each plan's tasks.md up to date, and ask any earlier manager to push its work, write a handover and stop | 21 | 33 | kept |
| its open drafts become packet inputs. | 21 | 33 | kept |
| Group ready, compatible task IDs from one plan into briefs of at most ~three human engineering days each. | 21 | 33 | kept |
| An issue packet groups issues from the brief's list instead | 21 | 33 | kept |
| its fix branches release/&lt;N&gt;/&lt;topic&gt; target release/&lt;N&gt;/main, per Release. | 21 | 33 | kept |
| Give each packet the Route of its hardest card, honestly: it sets the session's mode. | 21 | 33 | kept |
| Put them at releases/&lt;N&gt;/packets/&lt;id&gt;.md using the packet template. | 21 | 33 | kept |
| Link, never copy, tasks, dependencies and proof | 21 | 33 | kept |
| split oversized tasks first. | 21 | 33 | kept |
| Order the queue by priority | 21 | 33 | kept |
| cap Running plus Review at what you can review. | 21 | 33 | kept |
| A meter, gate or check brief states which realistic ways to get to green it must catch: skips, xfails and deselection through markers, -k, -m, | 21 | 33 | kept |
| config or PYTEST_ADDOPTS. | 21 | 33 | kept |
| Fail closed if a registry, baseline or ceiling approves itself or grows, if a PR changes the gate without approval or runs its own gate | 21 | 33 | kept |
| code, or if results are missing, truncated or show zero tests. | 21 | 33 | kept |
| Leave crafted bypasses to path protection and human review. | 21 | 33 | kept |
| Write each packet to finish in one run (Release 15, Plans 56, 87, 89, 82: ledger). - One contract per packet, aimed at about 3 | 22 | 34, 36 | kept |
| hours. | 22 | 34, 36 | kept |
| Never bundle cards | 22 | 34, 36 | kept |
| split a big card at its seams. | 22 | 34, 36 | kept |
| Rule before dispatch. | 23 | 37 | kept |
| Run a local baseline on the plan branch and write into the packet its exact focused selectors, the ids that already fail, the tests that | 23 | 37 | kept |
| must pass unchanged, and both May touch (files and functions) and Must not touch | 23 | 37 | kept |
| a packet without both is not Ready. | 23 | 37 | kept |
| See the packet workstream. | 23 | 37 | kept |
| Orchestrator-run, never the packet's: network clones and builds, the UI model or mode selector (the manager confirms it), timings and installed measurements, anything needing a | 24 | 38 | kept |
| real ComfyUI, GPU, installed build or generated catalog, and the proof itself. | 24 | 38 | kept |
| The packet ends with READY-PROOF &lt;repo&gt; &lt;PR&gt; &lt;head&gt; &lt;selectors&gt;. | 24 | 38 | kept |
| A cache or speed packet emits its counters (hit, miss, recompute) | 24 | 38 | kept |
| the lane reads them before trusting a timing and measures the numeric gate on the exact head. | 24 | 38 | kept |
| A sweep carries its count: every site found and every site changed, in the PR before review. | 25 | 39 | kept |
| Audit it against a count you take yourself. | 25 | 39 | kept |
| Prepare one queue. | 27 | 41 | kept |
| List each packet in releases/&lt;N&gt;/run.md with its handoff state, session and next action. | 27 | 41 | kept |
| A packet is Ready only when every PR or packet it depends on has merged into its destination | 27 | 41 | kept |
| otherwise Blocked, the dependency named in its row. tasks.md stays the record of progress. | 27 | 41 | kept |
| Own plan-level completion. | 28 | 42 | kept |
| For plans assigned through this workstream, record the Lead as the accountable agent on its inputs.md Run start, with the owner's authorization | 28 | 42 | kept |
| there is no separate plan manager. | 28 | 42 | kept |
| You review and land accepted task PRs, keep tasks.md current on main, and do the plan manager's Release steps: merging release/&lt;N&gt;/main into plan branches, and | 28 | 42 | kept |
| landing them. | 28 | 42 | kept |
| Review stops (RS1, R) are yours: commission an independent reviewer, not a packet. | 28 | 42 | kept |
| Prepare the boards. | 29 | 43 | kept |
| Reuse the release's existing boards, or create them (rules) by their titles | 29 | 43 | kept |
| no packet issues, no labels. | 29 | 43 | kept |
| Hand off to the owner with queue and mailbox links, ready/blocked packets, missing authorization and the Orchestrator launch message, filled in from the run board | 30 | 44 | kept |
| template. | 30 | 44 | kept |
| The board's startup checks verify access, session creation, resume, the hour and the mailbox | 30 | 44 | kept |
| describe any manual steps. | 30 | 44 | kept |
| Inputs: your boards since your cursor, including every packet the Orchestrator's STATUS marks Review | 34 | 48 | kept |
| open packet PRs | 34 | 48 | kept |
| and python3 scripts/release_branches.py check &lt;N&gt;. | 34 | 48 | kept |
| Each Review: accept, merge, open the tasks.md progress PR and post DONE | 36 | 50 | kept |
| or list the rework on the PR and post a DECISION. | 36 | 50 | kept |
| Accept a gate only after the reviewer injects the realistic failures in its brief and sees the gate reject them. | 36 | 50 | kept |
| Judge against that threat model and leave crafted bypasses out of the findings. | 36 | 50 | kept |
| Route each reviewer by the run contract: | 36 | 50 | kept |
| Default model for each route, using the newest available model of that family: | 40 | agent/shared/run-contract.md:13 (via 52) | moved |
| \| N \| Everything below very hard, including ordinary hard work: research, reading, running checks, most changes and fixes \| Haiku \| Luna \| | 44 | agent/shared/run-contract.md:17 (via 52) | moved |
| \| X \| Very hard: intricate changes, subtle bugs, coupled or non-obvious reasoning \| Sonnet \| Terra \| | 45 | agent/shared/run-contract.md:18 (via 52) | moved |
| \| S \| Super hard: deep design, or correctness that needs the deepest reasoning \| Opus \| Sol \| | 46 | agent/shared/run-contract.md:19 (via 52) | moved |
| \| T \| Taste: small, editorial refinement of something that already exists, such as user-facing copy, error and refusal messages, names, a screen's layout or | 47 | agent/shared/run-contract.md:20 (via 52) | moved |
| Reviews, plan judgment and advice use a separate high-judgment role: Opus (Claude) or Astra (Codex) | 49 | agent/shared/run-contract.md:22 (via 52) | moved |
| configure it in run.yaml as completion_reviewer, plan_judgment and advisor. | 49 | agent/shared/run-contract.md:22 (via 52) | moved |
| Reviews. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| A review's verdict runs on the high-judgment role. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| A check of a bounded fix against a named oracle (its failing case or probe) may run on X. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| N may gather facts for a review (check status, failure IDs, diff scope) but never gives the verdict. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| Check a pure sync by tree equality. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| A bounded-fix check runs the focused tests on both base and head. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| A bounded-fix check goes to the high-judgment role only when its own tests cannot show it is right (see the per-card rule under review and | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| promotion boundaries) | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| size alone is not a reason. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| A meter, gate or check is reviewed by injecting the failures it must catch. | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| The run names the actual reviewer model, flags and permissions where it records its bindings (run.yaml, or the run board for a dispatch run). | 51 | agent/shared/run-contract.md:24 (via 52) | moved |
| *From Routing and bindings | 53 | 52 | kept |
| edit it there.* | 53 | 52 | kept |
| Fix it yourself when it is small. | 56 | 54 | kept |
| Instead of posting rework, have a sub-agent make the fixes when all of these hold: | 56 | 54 | kept |
| the review grades the packet B+ or better; | 57 | 55 | kept |
| it leaves at most four must-fix items, each in one place, about 50 changed lines or fewer, with a failing case that defines done; | 58 | 56 | kept |
| none changes a design, protocol, schema, threat model, product default, pin or existing assertion; | 59 | 57 | kept |
| the packet's session has submitted, and its branch has not moved for 30 minutes. | 60 | 58 | kept |
| The sub-agent works on the packet's branch, adding each failing-before case, in commits labelled Lead review fixes. | 62 | 60 | kept |
| A second, faster reviewer checks them | 62 | 60 | kept |
| then merge and post DONE as usual. | 62 | 60 | kept |
| Otherwise, post the rework. | 62 | 60 | kept |
| Judge like a light gatekeeper. | 64 | 62 | kept |
| Reviewers sort findings into BLOCKING, FOLLOW-UP or NOTE | 64 | 62 | kept |
| block only on wrong results accepted, data or install damage, a real security or custody hole, or a regression from base. | 64 | 62 | kept |
| File the rest of a PR's follow-ups as one issue in astrid-dev, marked backlog and linked from the PR. | 64 | 62 | kept |
| A tasks.md row is for work the release must do. | 64 | 62 | kept |
| A regression the candidate introduced is fixed in its packet. | 64 | 62 | kept |
| A defect that predates it gets an issue and a test that stays executed and visibly failing, and the packet does not fix it. | 64 | 62 | kept |
| Changing an existing assertion, including turning a gate's limit into an observation, is the owner's call unless she has delegated it. | 64 | 62 | kept |
| An Orchestrator acting on her direct instructions needs her confirmation in its own chat. | 64 | 62 | kept |
| Keep work moving. | 66 | 64 | kept |
| When a packet has waited more than two hours on hosted jobs, read its run list: pull-request CI may run only part of a suite, | 66 | 64 | kept |
| so dispatch the full run it is waiting for. | 66 | 64 | kept |
| Every few hours, ask a high-judgment reviewer for a second opinion on bottlenecks, order and scope | 66 | 64 | kept |
| bring what exceeds your authority to the owner. | 66 | 64 | kept |
| Before merging: find every pin change: each needs its own commit and the owner's approval or delegation. | 68 | 66 | kept |
| After a dependency's PR is squash-merged, re-point its pin to the squash commit. | 68 | 66 | kept |
| Give a gate at most two review rounds | 68 | 66 | kept |
| round two only verifies round one's fixes. | 68 | 66 | kept |
| Then merge. | 68 | 66 | kept |
| Rulings: when a ruling will recur, add it to the board's Standing rulings (releases/&lt;N&gt;/run.md), so that a fresh Lead, Orchestrator or packet session finds it | 70 | 68 | kept |
| without reading the mailbox. | 70 | 68 | kept |
| A ruling that holds beyond the release goes into its skill instead, and the board links it. | 70 | 68 | kept |
| Then: triage the release's issues (states): an issue a task row or packet cites is planned, and one that a branch, pull request or running | 72 | 70 | kept |
| packet names is claimed, whoever started it. | 72 | 70 | kept |
| Give each uncited issue a row, or move it out. | 72 | 70 | kept |
| Move unblocked packets to Ready, write the next, copy the Orchestrator's STATUS into the board and refresh Now and Waiting on the owner. | 72 | 70 | kept |
| No Orchestrator STATUS for 2 hours, or a message of yours missing from its acted on: line, is the owner's to hear. | 72 | 70 | kept |
| Schedule your own check-ins with a scheduler that outlives your machine, re-armed each time | 72 | 70 | kept |
| else say which nudge the owner gives. | 72 | 70 | kept |
| When the work is not known up front (a release qualifier finding failures as it goes), the queue grows as findings arrive and the manager | 76 | 74 | kept |
| polls it hourly. | 76 | 74 | kept |
| The finder cuts an issue packet from the packet template, with its Repro, only when all hold: | 76 | 74 | kept |
| a failing test or exact repro that a sandbox with no network can target; | 77 | 75 | kept |
| a bounded fix of about 3 hours or less; | 78 | 76 | kept |
| a cause no plan owns. | 79 | 77 | kept |
| A failure in a plan's own code goes back to that plan's lane | 81 | 79 | kept |
| cross-lane findings go lane to lane. | 81 | 79 | kept |
| Fixes target release/&lt;N&gt;/&lt;topic&gt; → release/&lt;N&gt;/main. | 81 | 79 | kept |
| Anything that needs judgement about acceptability goes to the Lead. | 81 | 79 | kept |
| When the Lead's own session may stop without warning (a usage allowance, a lost container), the owner can keep a standby Lead in another session, | 85 | 83 | kept |
| on the high-judgment role of the other family. | 85 | 83 | kept |
| Heartbeat. | 86 | 84 | kept |
| The Lead posts its hourly STATUS (rules), even when nothing moved, with a marker the standby can recognise (for example its tool's footer). | 86 | 84 | kept |
| Wait. | 87 | 85 | kept |
| The standby checks the mailbox every hour and posts nothing while the newest Lead message is less than 3 hours old. | 87 | 85 | kept |
| Take over. | 88 | 86 | kept |
| After 3 hours of silence, the standby first rules out a quiet Lead: no Lead commit, branch push, pull request or board edit in those | 88 | 86 | kept |
| 3 hours. | 88 | 86 | kept |
| Then it posts one takeover message, keeps the same mailbox name, and runs the Lead's check-ins under the same Authority. | 88 | 86 | kept |
| One Lead. | 89 | 87 | kept |
| Once a takeover message exists, the earlier Lead stands down if it returns, and does nothing until the owner hands the role back. | 89 | 87 | kept |
| The release keeps the standby's brief and the environment notes beside its run board, under releases/&lt;N&gt;/lead/. | 91 | 89 | kept |

Count: 152 found; 134 kept; 0 restored; 18 moved; 0 superseded.


## agent/roles/leader/lane-orchestrators.md

Source: `skills/roles/astrid-dev-lead/workstreams/lane-orchestrators.md` at M. Destination: `agent/roles/leader/lane-orchestrators.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: Each lane runs end to end in its own session (orchestrator, one manager, workers by card route) and comes to the Lead only at | 9 | 13 | kept |
| anchor points | 9 | 13 | kept |
| the Lead's time goes to strategy, gates and cross-lane links. | 9 | 13 | kept |
| When to use: When the Lead starts or restarts a lane in Claude cloud, including replacing a lane whose session has drifted (fresh context on | 10 | 9 | kept |
| the same base). | 10 | 9 | kept |
| Inputs: A carded plan on astrid-dev main (each card with route, scope, dependencies, focused proof), its Run start line, the base SHAs, the owner's go, | 11 | 17 | kept |
| and a session with working Codex. | 11 | 17 | kept |
| Procedure: The four steps below, then strategy checks. | 12 | 21 | kept |
| Completion: The plan's cards are ticked in tasks.md, its landings confirmed by the Lead, its check-ins cancelled, and the session retired or handed its next | 13 | 25 | kept |
| plan. | 13 | 25 | kept |
| The Lead responsibilities continue to apply. | 15 | 27 | kept |
| Lessons from Release 15 (23 November 2026) are the reason for each step | 15 | 27 | kept |
| see the process ledger. | 15 | 27 | kept |
| The orchestrator reads its plan from main, so record everything before the launch message: the cards in tasks.md sized to the run contract's routes (most | 19 | 31 | kept |
| cards N | 19 | 31 | kept |
| X only for the one subtle change | 19 | 31 | kept |
| S only where a wrong call silently accepts a bad result | 19 | 31 | kept |
| reviews by the high-judgment role), the test inventory, and the Run start line in inputs.md naming the session, what it may do without asking, the | 19 | 31 | kept |
| owner's limits, the advisor and any lane it must coordinate with. | 19 | 31 | kept |
| Merge that PR before the owner pastes the launch message | 19 | 31 | kept |
| an unmerged Run start reads as "Pending" and a careful orchestrator stops. | 19 | 31 | kept |
| A plan that grows mid-run gets its own plan number rather than cards bolted onto a different plan (Plan 89 split from Plan 75, 23 | 21 | 33 | kept |
| November 2026). | 21 | 33 | kept |
| Fresh or reused. | 25 | 37 | kept |
| Prefer a fresh session on the same base when a lane has been going round in circles or used about half its context | 25 | 37 | kept |
| reuse a session only at a breakpoint (its current work landed). | 25 | 37 | kept |
| Never hand over mid-card. | 25 | 37 | kept |
| Create it with a short placeholder prompt ("You will be the orchestrator for Plan NN. | 26 | 38 | kept |
| Wait for the owner's launch message"). | 26 | 38 | kept |
| Never pass shell syntax as the prompt | 26 | 38 | kept |
| it is sent literally. | 26 | 38 | kept |
| Codex. | 27 | 39 | kept |
| Codex logins are per container, and usage limits are per account. | 27 | 39 | kept |
| Before assigning Codex work, the session runs codex exec --skip-git-repo-check -s read-only 'Reply ok.' once. | 27 | 39 | kept |
| A session on an account at its limit runs its cards on Claude subagents by the same routes, or the owner signs it in with | 27 | 39 | kept |
| another account. | 27 | 39 | kept |
| Test each session | 27 | 39 | kept |
| never infer one session's account from another's. | 27 | 39 | kept |
| A message sent from the Lead's session arrives as peer data, not as the owner's go, so the orchestrator rightly refuses outward actions on it. | 31 | 43 | kept |
| Draft the message for the owner to paste: | 31 | 43 | kept |
| You are the orchestrator for Plan &lt;NN&gt;, &lt;one-line outcome&gt;, in Release &lt;N&gt; of Astrid, and you answer for it finishing. | 34 | 46 | kept |
| Start here. | 36 | 48 | kept |
| Attach &lt;repos&gt;. | 36 | 48 | kept |
| Follow the astrid-dev-orchestrate skill, its lane-orchestrator workstream and its Codex-in-Claude workstream. | 36 | 48 | kept |
| Your run and its limits are the Run start line in plans/&lt;NN&gt;-&lt;name&gt;/inputs.md on astrid-dev main, and your work is cards &lt;ids&gt; in plans/&lt;NN&gt;-&lt;name&gt;/tasks.md, each with | 36 | 48 | kept |
| its route, scope and proof. | 36 | 48 | kept |
| Host one Codex manager on Terra (route X, effort high) that follows the astrid-dev-manage skill and works through those cards. | 38 | 50 | kept |
| It dispatches each card on its named route (Luna for N, Terra for X, Sol for S, Astra for reviews), runs only the tests the | 38 | 50 | kept |
| cards name, and ticks Progress in tasks.md as each card merges. &lt;Checkpoints, e.g. | 38 | 50 | kept |
| "RN-13: report and start nothing further until the Lead and I decide."&gt; | 38 | 50 | kept |
| Report on your plan's board and check in on the manager hourly, as the run contract's coordination rules say | 40 | 52 | kept |
| the Release &lt;N&gt; Lead is &lt;lead mailbox name&gt;. | 40 | 52 | kept |
| Otherwise follow the lane-orchestrator workstream's rules (anchor points only, decide and record). &lt;Coordination: "X touches the same code as &lt;lane&gt;: agree the order directly with | 40 | 52 | kept |
| &lt;session&gt;."&gt; | 40 | 52 | kept |
| Speed over bureaucracy: keep real correctness and every existing test unchanged, and prove the result &lt;by a real render / an installed measurement&gt; before any | 42 | 54 | kept |
| hosted CI. | 42 | 54 | kept |
| You may, without asking me: run Codex with full access here (Claude subagents if Codex refuses) | 44 | 56 | kept |
| attach any banodoco repo you need | 44 | 56 | kept |
| cut and push release/&lt;N&gt;/plan-&lt;NN&gt; from release/&lt;N&gt;/main | 44 | 56 | kept |
| open PRs | 44 | 56 | kept |
| merge them once the Release &lt;N&gt; Lead confirms the gate | 44 | 56 | kept |
| and dispatch hosted CI when the Lead gives you the slot. | 44 | 56 | kept |
| Trust the Release &lt;N&gt; Lead on every direction and design decision. | 44 | 56 | kept |
| Come to me only for publishing a release, anything paid, rented machines, live installs on my machine, or my own media. | 44 | 56 | kept |
| Ask the owner to do the Codex device sign-in in the session first if the check in step 2 failed. | 47 | 59 | kept |
| The lane's side (Codex check, anchor points only, decide and record, proof before CI, direct coordination, merging its own records) is the orchestrate role's lane | 51 | 63 | kept |
| workstream. | 51 | 63 | kept |
| The launch message points there | 51 | 63 | kept |
| send the Lead's rulings as they come, and when a lane asks what it could decide, add the missing rule to that workstream or to | 51 | 63 | kept |
| its plan once rather than answering again. | 51 | 63 | kept |
| Check in hourly, and decide on your own judgement. | 55 | 67 | kept |
| Lanes come to you only for gates and load-bearing calls | 55 | 67 | kept |
| the owner only for something extremely load-bearing or out of left field. | 55 | 67 | kept |
| Keep a decisions log for the owner (time, decision, reason, how to undo) and give it to her each morning. | 55 | 67 | kept |
| Send N subagents (Haiku) to find facts, and keep their conclusions, not their file dumps. | 55 | 67 | kept |
| When a lane asks something it could have decided, answer once and send every lane the ruling. | 55 | 67 | kept |
| At each check-in, per lane: is it on the biggest measured win | 57 | 69 | kept |
| is anything still unexplained after two tries (send the one cheapest experiment that makes the cause visible) | 57 | 69 | kept |
| what will block it next (disk, fixture, Codex limit, CI slot, review) and arrange it ahead | 57 | 69 | kept |
| is it asking things it could decide (write the rule once) | 57 | 69 | kept |
| do two lanes share code or a root cause (connect them directly). | 57 | 69 | kept |
| Pre-decide a lane's "least sure" item in your reply so it does not wait on you. | 57 | 69 | kept |
| Every hour: the parallelism pass, run by workers. | 59 | 71 | kept |
| The Lead is the judgment role: it reads, decides and answers, and sends route N workers (Luna, or Haiku on Claude) to do the exploring: | 59 | 71 | kept |
| read each lane's report and its running cards, name the real file and function conflicts, and list ready cards that sit idle. | 59 | 71 | kept |
| The Lead rules on what they return, and may ask a high-judgment reviewer (Opus, or Astra) for a second opinion on order and scope when | 59 | 71 | kept |
| a lane's report shows idle capacity or a reorder that would let more cards run at once (example: contract cards first, then the rest in | 59 | 71 | kept |
| waves). | 59 | 71 | kept |
| Pass the result to each lane's orchestrator as a ruling. | 59 | 71 | kept |
| A lane that reports fewer writers than it could run is asked why in the next check-in. | 59 | 71 | kept |
| Gates. | 61 | 73 | kept |
| Confirm a landing only after your own by-id comparison of its hosted unit run against the release baseline (a subagent fetches each job's full log | 61 | 73 | kept |
| and extracts FAILED/ERROR ids | 61 | 73 | kept |
| record the comparison under releases/&lt;N&gt;/evidence/), with each new id either in a recorded moving group or ruled with evidence (base and head run locally, or | 61 | 73 | kept |
| the source unchanged). | 61 | 73 | kept |
| Two Agent CI runs may run in parallel | 61 | 73 | kept |
| after a landing whose tree equals the gated head, cancel the push-triggered runs on the release branch. | 61 | 73 | kept |
| Speed findings go in docs/speed.md through the lanes' evidence PRs. | 63 | 75 | kept |

Count: 98 found; 98 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/manager/chatgpt-packet.md

Source: `skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md` at M. Destination: `agent/roles/manager/chatgpt-packet.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: One bounded packet implemented and proved on draft task pull requests for Lead review. | 9 | 13, 35, 40 (proof by orchestrator per standing ruling) | kept |
| When to use: When a fresh ChatGPT session is assigned an accepted packet with explicit scope and authority by the release dispatch. | 10 | 9 | kept |
| Inputs: The exact packet, assigned task rows, board and current rulings, target repository and base, accepted proof and permissions. | 11 | 17 | kept |
| Procedure: Receive and verify the assignment, implement directly on the permitted branch, collect original proof and submit the draft PR and handoff. | 12 | 21, 32–40 (proof handoff, not packet proof execution) | kept |
| Completion: Every assigned task has a traceable disposition, exact source and test evidence, and a Lead-visible handoff without unauthorized merging. | 13 | 25, 40 (exact selectors; orchestrator proof) | kept |
| Use when a fresh ChatGPT session receives one accepted packet from the Orchestrator. | 15 | 27 | kept |
| Follow Manage for scoped engineering and proof | 15 | 27 | kept |
| the review is the Lead's, so commission none. | 15 | 27 | kept |
| You do this packet's engineering yourself | 15 | 27 | kept |
| you do not own the plan, and you take no second packet. | 15 | 27 | kept |
| Check your mode against your packet's Route | 19 | 31 | kept |
| if it differs, say so in your first STATUS. | 19 | 31 | kept |
| Receive. | 20 | 32 | kept |
| Read your board and the Lead board (rules) for messages to you | 20 | 32 | kept |
| do so again on every resume and before finishing. | 20 | 32 | kept |
| Then read the start message, the packet and its tasks.md rows, on astrid-dev main unless the packet names a branch. | 20 | 32 | kept |
| Confirm scope, proof, dependencies, working repository, base and PR target, limits and authorization. | 20 | 32 | kept |
| Startup confirms only what the connector does: read files, push a branch, open a draft PR, comment. | 20 | 32 | kept |
| The start message is the owner's | 20 | 32 | kept |
| the board's Authority section bounds it and its Standing rulings bind you (run contract). | 20 | 32 | kept |
| Implement. | 21 | 33 | kept |
| Work directly, and link the plan/task IDs. | 21 | 33 | kept |
| - Branches. | 22 | 34 | kept |
| In each repository, open PR(s) to the packet's PR destination: from p&lt;P&gt;/&lt;task-id&gt; into release/&lt;N&gt;/plan-&lt;P&gt;, or, for an issue packet, from release/&lt;N&gt;/&lt;topic&gt; into release/&lt;N&gt;/main | 22 | 34 | kept |
| never main. | 22 | 34 | kept |
| Cut a new branch from the PR destination's current head. | 22 | 34 | kept |
| Continue an existing draft rather than open a second PR | 22 | 34 | kept |
| if its head differs from the one the board lists, post BLOCKED and do not push. | 22 | 34 | kept |
| Merge a base in | 22 | 34 | kept |
| never rebase. | 22 | 34 | kept |
| Post an early STATUS once your first draft PR is open. | 22 | 34 | kept |
| - Proof. | 23 | 35 | kept |
| Write the code and its tests. | 23 | 35 | kept |
| Never clone, build, run tests, take timings or check the UI mode selector, and never need a real ComfyUI, GPU, installed build or catalog: the | 23 | 35 | kept |
| orchestrator runs the proof. | 23 | 35 | kept |
| Before READY-PROOF, merge the destination's current head (land) and name it in STATUS. | 23 | 35 | kept |
| - Scope. | 24 | 36 | kept |
| The packet's May touch is yours. | 24 | 36 | kept |
| An adjacent edit of about 20 lines or fewer outside it, and not in Must not touch, is allowed without asking: list it in the | 24 | 36 | kept |
| PR body under "adjacent edits". | 24 | 36 | kept |
| Anything larger, or anything in Must not touch, is one BLOCKED with the exact list. | 24 | 36 | kept |
| - Tests. | 25 | 37 | kept |
| Change test setup and assertions only as the run contract allows. | 25 | 37 | kept |
| - Pins. | 26 | 38 | kept |
| Put any pin change in its own commit and name it in STATUS | 26 | 38 | kept |
| pins are not yours to approve. | 26 | 38 | kept |
| - Pauses. | 27 | 39 | kept |
| Before any pause, push work in progress and post STATUS. | 27 | 39 | kept |
| Submit and stop. | 28 | 40 | kept |
| When code and tests are pushed on the draft PR, post READY-PROOF &lt;repo&gt; &lt;PR&gt; &lt;head&gt; &lt;selectors&gt; as a STATUS on your board, to: the Orchestrator, | 28 | 40 | kept |
| with the packet ID, task IDs, adjacent edits and remaining limits | 28 | 40 | kept |
| then stop. | 28 | 40 | kept |
| It is not Done. | 28 | 40 | kept |
| A fix round is a resume with the orchestrator's findings, never a held BLOCKED | 28 | 40 | kept |
| the Orchestrator may instead start a replacement session for the same packet. | 28 | 40 | kept |
| If blocked, post BLOCKED with the failure, what you tried and the action needed | 29 | 41 | kept |
| continue independent work. | 29 | 41 | kept |
| Do not merge, update tasks.md or claim the plan is finished: those are the Lead's. | 31 | 43 | kept |
| A row the plan lacks goes in STATUS as a proposal. | 31 | 43 | kept |

Count: 59 found; 59 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/manager/whole-project.md

Source: `skills/roles/astrid-dev-manage/workstreams/whole-project.md` at M. Destination: `agent/roles/manager/whole-project.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: An accepted project managed through verified task delivery, integrated progress and an owner-reviewable completion record. | 9 | 13 | kept |
| When to use: When one accountable Manager is assigned the full plan run rather than an isolated fresh-session packet. | 10 | 9 | kept |
| Inputs: The accepted plan and tasks, current run identity, named owner, working repositories, dependencies, proof requirements and permissions. | 11 | 17 | kept |
| Procedure: Keep task progress current, make scope decisions within authority, coordinate implementation and proof, integrate work and report accurately. | 12 | 21 | kept |
| Completion: Accepted tasks and completion evidence are recorded in the project's canonical files, or precise blockers remain visible for the owner. | 13 | 25 | kept |
| Use when you are the one accountable manager for an accepted Astrid plan run, rather than a short-lived ChatGPT packet manager. | 15 | 27 | kept |
| Apply the general Manage principles and the run contract. | 15 | 27 | kept |
| The project pack owns scope and acceptance | 15 | 27 | kept |
| don't create another queue. | 15 | 27 | kept |
| Progress is always current. | 19 | 31 | kept |
| This is a key responsibility. tasks.md is the run's only progress record | 19 | 31 | kept |
| the owner and every check-in read it on main, and a record that isn't there doesn't count. | 19 | 31 | kept |
| - Update the plan's tasks.md when a task lands (x, with its merge), is blocked (and why), or is created or stopped. | 20 | 32 | kept |
| Batch the rest, such as which tasks started, into the next of those updates. | 20 | 32 | kept |
| - Keep at most one progress branch open. | 21 | 33 | kept |
| - Send each update as its own small PR that changes only that tasks.md. | 22 | 34 | kept |
| You merge it yourself, with auto-merge on, once python3 scripts/astrid_dev.py check passes locally (run contract). astrid-dev main requires its checks, so don't wait on it. | 22 | 34 | kept |
| - At the next update confirm the last one merged. | 23 | 35 | kept |
| A progress PR that conflicts never merges by itself: close it and reopen from current main. | 23 | 35 | kept |
| - Edit tasks.md only through these PRs, not on the plan branch, or the two copies conflict when the project lands. | 24 | 36 | kept |
| You are expected to decide. | 28 | 40 | kept |
| The advisor is for thinking that is bigger than your project, not for permission. | 28 | 40 | kept |
| Priorities, in order | 30 | 42 | kept |
| the higher wins: a user's work is never silently lost and nothing looks saved that is not | 30 | 42 | kept |
| no check is weakened to get a pass | 30 | 42 | kept |
| what ships is what was tested, with honest records | 30 | 42 | kept |
| ship as soon as those allow | 30 | 42 | kept |
| least process and the cheapest route that works. | 30 | 42 | kept |
| Before a decision that is not trivial, three lines for yourself: who is affected if it is wrong, how you would find out, how hard | 31 | 43 | kept |
| it is to undo. | 31 | 43 | kept |
| Easy to undo and quick to detect: decide and move | 31 | 43 | kept |
| otherwise slow down. | 31 | 43 | kept |
| Decide and log: anything on a branch, engineering choices consistent with how the product behaves, evidence-backed rulings on findings, CI, tooling and worker choices. | 32 | 44 | kept |
| Decide and flag REVIEW only within existing authority: reversible, in-scope user-facing choices and coordination with a sibling project. | 33 | 45 | kept |
| Log the candidate, evidence and proposed disposition | 33 | 45 | kept |
| the flag is not permission to change accepted scope, quarantine or weaken a test, override a refusal or affect another project's work without its owner's | 33 | 45 | kept |
| go. | 33 | 45 | kept |
| For those cases, stop dependent work and ask. | 33 | 45 | kept |
| Stop and ask: publication, spend beyond the approved budget, new access, credentials or permissions for a session, anything destructive or irreversible outside your branches, and | 34 | 46 | kept |
| any safety or permission refusal. | 34 | 46 | kept |
| The decision log is a short append-only file the plan or release brief names (otherwise a "Rulings" section at the top of tasks.md), with a | 35 | 47 | kept |
| Now block first: current heads, what is running, what is blocked, spend. | 35 | 47 | kept |
| The advisor reads it at check-ins and writes back only on disagreement. | 35 | 47 | kept |
| Message the advisor almost never: only when work cannot continue without it: a hard blocker you have tried and cannot clear, something only the owner | 36 | 48 | kept |
| can do that is ready for her now, a paid machine or money you cannot account for, or a release label the release brief names | 36 | 48 | kept |
| (such as A-FROZEN). | 36 | 48 | kept |
| Findings, rulings, scope trades and contained incidents go in the log, progress in tasks.md. | 36 | 48 | kept |
| Send one question with its evidence: the versions, the brief, the first failing command and its output, and what was tried. | 36 | 48 | kept |
| Use the run's advisor, or start one on its advisor setting. | 36 | 48 | kept |
| If a rule or permission is missing or refused, do not assume it: stop dependent work, record the exact request and ask the owner or | 36 | 48 | kept |
| authorized decision maker. | 36 | 48 | kept |
| Continue only independently authorized work. | 36 | 48 | kept |
| Verify an alarm before you escalate it: when a worker reports something serious, have an independent reviewer confirm or refute it from the code first. | 37 | 49 | kept |
| Deal with a sibling project directly: message its manager yourself for a hand-off or a question, not through the advisor. | 38 | 50 | kept |
| A wrong decision is yours to follow through: say so, fix it, and change the rule that led to it. | 39 | 51 | kept |
| Resume or start. | 43 | 55 | kept |
| Your release is the brief whose ## Included plans lists your plan | 43 | 55 | kept |
| its release manager is named there. | 43 | 55 | kept |
| A plan in no release does not start unless it is a self-contained astrid-dev-only project: the owner can explicitly approve and start that project without | 43 | 55 | kept |
| assigning a product release. | 43 | 55 | kept |
| This exception never applies when any other repository changes or a release needs integration | 43 | 55 | kept |
| use the release branch and the named Lead in those cases. | 43 | 55 | kept |
| A qualifying dev-only run begins at the current main head on project/&lt;PP&gt;-&lt;slug&gt; and records its exact base, authority and integration destination in inputs.md | 43 | 55 | kept |
| task branches target that project branch. | 43 | 55 | kept |
| No approval is implied by creating a plan. | 43 | 55 | kept |
| Continue a matching run in plans/&lt;project&gt;/.otto/runs/, keeping its recorded versions, model settings, scope, evidence, review count and any pause. | 43 | 55 | kept |
| Otherwise start one there: copy the run template to &lt;run-id&gt;/run.yaml and fill each role with a model you have seen is available (and the advisor's | 43 | 55 | kept |
| session, if one already exists) before dispatching. | 43 | 55 | kept |
| - Check the environment before a new run's first task. | 44 | 56 | kept |
| Create one throwaway worker per repository the plan changes, and have it run astrid-dev's env/smoke.sh with one named test (shared worker environment). | 44 | 56 | kept |
| Record the result under environment in run.yaml. | 44 | 56 | kept |
| Fix any problem before dispatching real work | 44 | 56 | kept |
| a permission or network refusal goes to the owner. | 44 | 56 | kept |
| - Tests: you run what the plan names, when the run contract's table says, and nothing else. | 45 | 57 | kept |
| You don't choose tests: if a card names no proof, or its proof can't run, ask the advisor to name one. | 45 | 57 | kept |
| Put the exact test command in every worker's card and tell the worker to run only that. | 45 | 57 | kept |
| - Record the baseline before the first task, scoped to the plan's test inventory and each task's focused-proof files, plus every other baseline the plan | 46 | 58 | kept |
| or owner names (for a release: the served release and main). | 46 | 58 | kept |
| Agent shards take close to an hour each, so the full-suite comparison runs on CI only, against main's latest CI. | 46 | 58 | kept |
| Run each side with PYTEST_ADDOPTS=-rA, and keep the logs in the worker. | 46 | 58 | kept |
| - A regression, and sorting results with env/baseline-diff.py, are defined in the run contract. | 47 | 59 | kept |
| Commit its summary.md and id lists under plans/&lt;project&gt;/evidence/tests/&lt;repo&gt;/&lt;candidate short SHA&gt;/, the one place to show what passes and fails, and record that path under baseline | 47 | 59 | kept |
| in run.yaml. | 47 | 59 | kept |
| - An environment task such as a setup script may run first if the baseline needs it. | 48 | 60 | kept |
| - Some pushes and pull requests start CI (which), on runners shared with releases. | 49 | 61 | kept |
| Land task PRs into the plan branch in batches (several tasks per push), keep task-branch PRs to one when they can, and cancel your own | 49 | 61 | kept |
| superseded runs when a newer push replaces them. | 49 | 61 | kept |
| During a release's gate, push to release/*/main only when the release manager says the runners are free. | 49 | 61 | kept |
| - One run per ref. | 50 | 62 | kept |
| Workflows that cancel in progress cancel on any second dispatch or push to the same ref, with no author shown. | 50 | 62 | kept |
| Never dispatch twice on one ref or push to a ref while its qualifying run is in flight, and never dispatch on another project's ref. | 50 | 62 | kept |
| Dispatch. | 51 | 63 | kept |
| Send each ready task to a subagent on its route. | 51 | 63 | kept |
| In the card put its outcome, scope (what it may change | 51 | 63 | kept |
| a path includes its own tests, wherever they live), dependencies, exact starting versions, acceptance check and authority. | 51 | 63 | kept |
| - Tell an X or S task to delegate research, reading, mechanical edits and checks to N helpers. | 52 | 64 | kept |
| Send a T task what its rule lists and have it return the exact before and after. | 52 | 64 | kept |
| - Tell every task to add commits only (run contract). | 53 | 65 | kept |
| - Escalate by the stopping thresholds: re-route a failure to X with the worker's notes, don't try again. | 54 | 66 | kept |
| - Keep independent tasks moving while one is blocked. | 55 | 67 | kept |
| - Do a task yourself when no worker can be started for it, or briefing one costs more than the work: on its task branch, | 56 | 68 | kept |
| to the same card, if your route is at least the task's. | 56 | 68 | kept |
| Note it in the progress row | 56 | 68 | kept |
| rule 9 still applies. | 56 | 68 | kept |
| - A CI step running past one and a half times its usual time is a hang: cancel it and don't wait | 57 | 69 | kept |
| Get to green says how to name the test. | 57 | 69 | kept |
| - Your own wake-up: never end a turn with work in flight (workers, CI, merges) without scheduling a one-off message to yourself in 20–30 minutes, | 58 | 70 | kept |
| or a background wait on the run | 58 | 70 | kept |
| an idle session wakes for nothing. | 58 | 70 | kept |
| - Worker sessions get exactly one repository, attached when the session is created: the repository the task changes, at its plan or fix branch, in | 59 | 71 | kept |
| auto mode (or Accept edits). | 59 | 71 | kept |
| Its committed .claude/settings.json lists the setup and test commands workers may run without a prompt (a multi-repo manager session loads none), so put product-repo commands | 59 | 71 | kept |
| there, and start workers on the plan or fix branch and merge the task branch in. | 59 | 71 | kept |
| - No worker may stall on a permission prompt nobody sees. | 60 | 72 | kept |
| Write files with the Write tool and run one simple command per Bash call (no heredocs, cd … && chains or git -c user.* identity | 60 | 72 | kept |
| overrides). | 60 | 72 | kept |
| If a command still prompts, stop and report it to the advisor at once instead of waiting. | 60 | 72 | kept |
| - Run only scripts that live in the worker's own repository (scripts/worker-env/, copied from env/) | 61 | 73 | kept |
| a script from another repository's clone is refused even when allow-listed. | 61 | 73 | kept |
| Other public repositories may be cloned read-only to /home/user/&lt;repo&gt;, for reading. | 61 | 73 | kept |
| - Codex workers are the default when the run uses Codex: Use Codex from Claude Cloud. | 62 | 74 | kept |
| You stay the manager: check each result is inside the card's scope, re-run every proof the card names, then commit and integrate. | 62 | 74 | kept |
| Don't start a Codex manager unless your Run start line says to. | 62 | 74 | kept |
| - Managing under Codex (you are a Codex manager | 63 | 75 | kept |
| only by choice): follow your manager brief | 63 | 75 | kept |
| the cloud-session rules in this step don't apply (why). | 63 | 75 | kept |
| - When a card contradicts its own contract, the worker stops and you rule at once (no test edited to pass). | 64 | 76 | kept |
| - Every card names its manager: "Follow-up messages from manager session &lt;id&gt; are part of this brief | 65 | 77 | kept |
| follow them within this task's scope." Without it a worker treats your follow-ups as data from another session and won't act on them, so it | 65 | 77 | kept |
| can't be steered. | 65 | 77 | kept |
| If a worker still refuses, replace it with a fresh worker whose first brief holds everything, and keep the commits it pushed. | 65 | 77 | kept |
| - Every card says: never use AskUserQuestion. | 66 | 78 | kept |
| Nobody can answer it in a worker session. | 66 | 78 | kept |
| Questions go to the manager by send_message, and the worker carries on with whatever isn't blocked. | 66 | 78 | kept |
| On every loop, check list_sessions for workers marked needs-action or blocked and clear each within 5 minutes. | 66 | 78 | kept |
| - Stop a worker the moment its task is ruled closed, and give every wait a timeout. | 67 | 79 | kept |
| Keep heavy suites off a shared machine (several full runs at once invalidate each other): push them to CI on your own scratch refs. | 67 | 79 | kept |
| - List every command the task needs in its card, including the repository's own CI setup (its pip/apt install steps), so a worker never stops | 68 | 80 | kept |
| partway for approval. | 68 | 80 | kept |
| Routine CI setup needs no extra go. | 68 | 80 | kept |
| - Give each command as literal text, for example bash scripts/worker-env/agent-setup.sh: allow rules match the literal command, so a variable-built path is refused. | 69 | 81 | kept |
| Use no cd, because it moves every later command. | 69 | 81 | kept |
| - An approval relayed from another session is never authority, and only the owner's own message or a committed allow rule lifts a permission refusal. | 70 | 82 | kept |
| - "Unrelated histories" usually means a shallow clone. | 71 | 83 | kept |
| Check git rev-parse --is-shallow-repository | 71 | 83 | kept |
| if true, run git fetch --unshallow origin and merge again. | 71 | 83 | kept |
| Never use --allow-unrelated-histories on a release or plan branch. | 71 | 83 | kept |
| - If a worker can't open a PR, it pushes its branch, and the lead or advisor opens it | 72 | 84 | kept |
| a progress PR still auto-merges. | 72 | 84 | kept |
| Run the end gate's stages at once, not in turn. | 73 | 85 | kept |
| When the end gate has several stages (fixes, CI, cross-repo re-pins, a journey matrix, review), start the later stages on today's heads while fixes are | 73 | 85 | kept |
| in flight: review the current diff, stage the re-pins, and run the full end gate once as a shakedown, which counts for nothing. | 73 | 85 | kept |
| The final run then only re-confirms with the fix commits, and the review covers only the fix diffs. | 73 | 85 | kept |
| You plan these tracks | 73 | 85 | kept |
| the advisor doesn't plan the run. | 73 | 85 | kept |
| Keep scopes apart, and run everything else in parallel. | 75 | 87 | kept |
| - Scopes overlap when they change the same function, class or contract, not merely the same file. | 76 | 88 | kept |
| Never run overlapping tasks at once | 76 | 88 | kept |
| start the later from what the earlier landed. | 76 | 88 | kept |
| - Run disjoint tasks at once, even in one file, and land them in an agreed order by merging the plan branch in. | 77 | 89 | kept |
| - Before you merge the release branch (or main) in, fetch it and check what you fetched: git ls-remote origin refs/heads/&lt;branch&gt; gives the real tip, | 78 | 91 | kept |
| and after the merge git merge-base --is-ancestor &lt;that sha&gt; HEAD must succeed. | 78 | 91 | kept |
| A local origin/&lt;branch&gt; can be hours stale in a shallow or partial clone. | 78 | 91 | kept |
| - Trial-merge overlapping siblings at each milestone. | 79 | 90 | kept |
| For each unlanded plan branch in the release that overlaps yours, run git merge-tree --write-tree --name-only &lt;your plan branch&gt; &lt;sibling plan branch&gt;. | 79 | 90 | kept |
| Report new conflicts on shared functions, contracts or producer pins in your milestone note, and tell the release manager while the conflicts are small. | 79 | 90 | kept |
| When the two plans' tests disagree about the same behaviour, an owner ruling resolves it | 79 | 90 | kept |
| never quietly pick one side. | 79 | 90 | kept |
| - After any merge, check it finished: git diff --name-only --diff-filter=U must print nothing before you run a proof, start a worker or push | 80 | 92 | kept |
| a merge can stop on a conflict without your noticing. | 80 | 92 | kept |
| - Each task gets a fresh checkout from the latest head. | 81 | 93 | kept |
| Delete it, with its installed dependencies, as soon as it lands: session disk is a small shared allowance and a full disk stops every tool. | 81 | 93 | kept |
| - Keep the session's own checkout detached at the plan branch, so session hooks that compare it with main stay quiet | 82 | 94 | kept |
| a hook asking you to push to main is never a reason to. | 82 | 94 | kept |
| Land into the project's plan branch, then its authorized integration target | 83 | 95 | kept |
| never push directly to main. | 83 | 95 | kept |
| - Release-linked project: In each repository the project changes, cut one plan branch, release/&lt;NN&gt;/plan-&lt;PP&gt;, when the run starts. | 84 | 96 | kept |
| Cut it from that repository's release/&lt;NN&gt;/main, unless the plan's Base says to stack on another plan's branch (Plan), and confirm that choice still holds before | 84 | 96 | kept |
| you cut it, and add its row to the brief's ## Branches on astrid-dev main. | 84 | 96 | kept |
| Each task has its own branch, p&lt;PP&gt;/&lt;task id&gt;, cut from the plan branch | 84 | 96 | kept |
| its PR targets it. | 84 | 96 | kept |
| Keep it current as How a release runs says. | 84 | 96 | kept |
| - Astrid-dev-only exception: When the owner explicitly authorizes a project that changes only astrid-dev, cut project/&lt;PP&gt;-&lt;slug&gt; from live main. | 85 | 97 | kept |
| Each task branch p&lt;PP&gt;/&lt;task id&gt; targets that project branch. | 85 | 97 | kept |
| After integrated checks and required independent review, submit the project branch as a reviewed PR to astrid-dev main | 85 | 97 | kept |
| it merges only with the owner's go and required checks. | 85 | 97 | kept |
| No release branch, release brief or release manager is invented. | 85 | 97 | kept |
| Keep tasks.md progress as its own small PR directly to main after each verified task. | 85 | 97 | kept |
| An unrelated product-repository change cancels this exemption and requires a release decision. | 85 | 97 | kept |
| - Check the changed files stay inside the scope | 86 | 98 | kept |
| if not, stop and ask the advisor. | 86 | 98 | kept |
| - A change is ready when its focused proof passes (local proof counts only when it runs the same path as the check, per Iterate) | 87 | 99 | kept |
| and no check covering its scope newly fails against its base. | 87 | 99 | kept |
| If the base has no run of a failing check, run that one test on the base yourself. | 87 | 99 | kept |
| - A check already failing on the base (found when you recorded the baseline) neither blocks the merge nor becomes this project's work: note it | 88 | 100 | kept |
| once for the owner and leave it to its own project (Get to green, mode B). | 88 | 100 | kept |
| - Release-linked plan: Land once its plan branch, with the current release branch merged in, passes its checks on that combined tree: merge it into | 89 | 101 | kept |
| release/&lt;NN&gt;/main and set your row to merged. | 89 | 101 | kept |
| If your merge turns the release branch red, fix forward on a fix branch or revert it promptly (red release branch). | 89 | 101 | kept |
| - Astrid-dev-only plan: Integrate current main into the project branch without rewriting history | 90 | 102 | kept |
| qualify the exact combined head, complete the final review, and seek the owner's go for the single project PR to main. | 90 | 102 | kept |
| It may be merged by the authorized manager only after required checks succeed. | 90 | 102 | kept |
| Record that merge and only then close the project. | 90 | 102 | kept |
| - Outside the narrowly authorized astrid-dev-only exception, moving the reviewed candidate to main is Release's job, not yours. | 91 | 103 | kept |
| Escalate. | 92 | 104 | kept |
| - Decide these yourself | 93 | 105 | kept |
| don't ask: | 93 | 105 | kept |
| - merge a disjoint task as soon as its own proof passes; | 94 | 106 | kept |
| - a test that can't run on CPU by nature (real weights, a GPU) gets the repository's gpu marker and its reason; | 95 | 107 | kept |
| - fix a test-setup artifact in the test setup, never by injecting what product code should supply; | 96 | 108 | kept |
| - when a card requirement on code that a later accepted plan replaces can't be met cheaply, defer it to the task that owns that | 97 | 109 | kept |
| code, and record the deferral in the merge commit and tasks.md; | 97 | 109 | kept |
| - re-run a gate (CI, a journey, the matrix) on a fix commit as soon as the fix lands, and paste the run ids | 98 | 110 | kept |
| re-runs need no go, and each starts when its own inputs are ready, not when every fix is done; | 98 | 110 | kept |
| - when a gate fails, first make the failure visible: read the first error, and if the evidence isn't uploaded, reproduce the exact command. | 99 | 111 | kept |
| Then sort the failing tests against the main branch's latest run by the regression rule, before you ask; | 99 | 111 | kept |
| - when a suite stops early, get its complete list once before fixing anything (how). | 100 | 112 | kept |
| Take first the failures that could be a real product bug, and for each establish whether a user hits it and whether the shipped release | 100 | 112 | kept |
| has it too; | 100 | 112 | kept |
| - a test that cannot be fixed in its task is quarantined only under the green-mains quarantine rule: strict expected-failure, exact title, issue, owner, expiry. | 101 | 113 | kept |
| Never a skip, and never for a bug this project introduced; | 101 | 113 | kept |
| - when a gate's test drives the product differently from users (a different entry point, flags or pinned versions), fix the test so it drives | 102 | 114 | kept |
| the product as users do, and record the cause. | 102 | 114 | kept |
| - Act on the one next step it returns | 103 | 115 | kept |
| advice is never permission to run or publish. | 103 | 115 | kept |
| - No advisor model available: ask the owner. | 104 | 116 | kept |
| Owner asked for advisor check-ins: answer them briefly | 104 | 116 | kept |
| treat their next step like any other advice. | 104 | 116 | kept |
| Review, once every task before the review row is done: | 105 | 117 | kept |
| - give the integrated candidate to the completion_reviewer for a round; | 106 | 118 | kept |
| - add each finding as a row directly below the review row (R&lt;round&gt;.&lt;n&gt;, or the plan's prefix) | 107 | 119 | kept |
| rounds, stopping and a blocking finding left after the last round follow the run contract. | 107 | 119 | kept |
| Keep state small. | 108 | 120 | kept |
| Track the candidate, finished and blocked tasks, exact failures, evidence, review rounds and next action: progress in tasks.md (Progress is always current), status in the | 108 | 120 | kept |
| plan's Status: line. | 108 | 120 | kept |
| When astrid-dev itself gets in the way, add an entry file to the process ledger. | 108 | 120 | kept |
| A finding about the product is an issue you file | 108 | 120 | kept |
| a worker hands you the text. | 108 | 120 | kept |
| Post the hourly STATUS on the plan's board (rules). | 112 | 124 | kept |
| Closing the project: open the completion PR from the completion template | 114 | 126 | kept |
| python3 scripts/astrid_dev.py check checks its fields. | 114 | 126 | kept |
| Review the affected release brief and the gap’s assessment and route to closure | 114 | 126 | kept |
| update the source if needed or record why it did not change (hierarchy). | 114 | 126 | kept |
| Tell the owner what changed | 114 | 126 | kept |
| what is proven, on which exact versions | 114 | 126 | kept |
| what failed and why | 114 | 126 | kept |
| and each decision that needs them. | 114 | 126 | kept |
| For a blocker, name what it waits on, who produces it and any deadline. | 114 | 126 | kept |

Count: 248 found; 248 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/manager/ai-studio-packet.md

Source: `skills/roles/astrid-dev-manage/workstreams/ai-studio-packet.md` at INT source fd8a9a04 (latest ported source). Destination: `agent/roles/manager/ai-studio-packet.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: One lab packet executed by a fresh AI Studio session and pushed to its own lab/&lt;id&gt; branch with a result note, ready for the | 9 | 13 | kept |
| reflection gate. | 9 | 13 | kept |
| When to use: When an operator (normally a Codex agent with browser control of the owner's AI Studio account) is given a Ready packet from | 10 | 9 | kept |
| a lab run board for the specified active lab run. | 10 | 9 | kept |
| Inputs: The run board, the packet brief and LAB_RULES.md at the lab's main head, the owner's latest instructions, the AI Studio workspace linked to the | 11 | 17 | kept |
| lab repository. | 11 | 17 | kept |
| Procedure: Check the packet is Ready, open a fresh AI Studio session on main, paste the start prompt, supervise to the result note, push lab/&lt;id&gt;, | 12 | 21 | kept |
| then report to the owner. | 12 | 21 | kept |
| Completion: The branch exists at a recorded commit with packets/&lt;id&gt;.result.md, and the owner has a short report (or a blocker) naming the packet, branch, commit | 13 | 25 | kept |
| and AI Studio's own check output. | 13 | 25 | kept |
| Use for a lab repository built to be developed in Google AI Studio and imported into an Astrid product repository at the end, where a | 15 | 27 | kept |
| project explicitly selects this route and provides a current run board. | 15 | 27 | kept |
| You are the operator, not the engineer. | 15 | 27 | kept |
| AI Studio writes the code | 15 | 27 | kept |
| you give it the packet, keep it inside the packet, and move its work to GitHub. | 15 | 27 | kept |
| You do not review it: a fresh Astra reviewer does (Astra reflection), and a packet is merged into the lab's main only on that reviewer's | 15 | 27 | kept |
| accept verdict. | 15 | 27 | kept |
| When you are also the run's manager, you commission that reviewer and do the merge. | 15 | 27 | kept |
| Check. | 19 | 31 | kept |
| Reread the owner's latest messages, on every resume too. | 19 | 31 | kept |
| On the run board, the packet must be Ready and every packet it depends on Accepted. | 19 | 31 | kept |
| Note the lab's main head commit. | 19 | 31 | kept |
| Open a fresh session. | 20 | 32 | kept |
| One packet, one new AI Studio Build session. | 20 | 32 | kept |
| Bring the lab's main into it at that commit (AI Studio's GitHub import or sync). | 20 | 32 | kept |
| Do not reuse a session from another packet | 20 | 32 | kept |
| a rework round may reuse its own packet's session if it is still open. | 20 | 32 | kept |
| Start it. | 21 | 33 | kept |
| Paste the start prompt with the packet ID and commit filled in. | 21 | 33 | kept |
| Add nothing else. | 21 | 33 | kept |
| Supervise. | 22 | 34 | kept |
| Answer AI Studio's questions only from the brief and LAB_RULES.md. | 22 | 34 | kept |
| If it wants to do something the brief does not ask for, the answer is "not in this packet". | 22 | 34 | kept |
| If it asks something the brief cannot answer, have it write the question in its result note and stop. | 22 | 34 | kept |
| Make sure it runs npm run check and npm run build and reports their output. | 22 | 34 | kept |
| Do not write or edit code yourself. | 22 | 34 | kept |
| Push. | 23 | 35 | kept |
| When the result note exists and the checks pass, push to the branch lab/&lt;id&gt; (never main). | 23 | 35 | kept |
| Confirm on GitHub that the branch head matches, and that the result note is in it. | 23 | 35 | kept |
| Report. | 24 | 36 | kept |
| Tell the owner, in your own chat, in a few lines: packet ID | 24 | 36 | kept |
| branch and commit | 24 | 36 | kept |
| AI Studio's check and build output as reported | 24 | 36 | kept |
| time taken | 24 | 36 | kept |
| anything it was unsure of. | 24 | 36 | kept |
| Mark the packet Gate on the board, then hand it to the reflection gate. | 24 | 36 | kept |
| Rework. | 25 | 37 | kept |
| If the gate sends rework, paste the gate's rework prompt into the same packet's session (or a fresh one at the branch head), then push | 25 | 37 | kept |
| and report again. | 25 | 37 | kept |
| After two rework rounds the gate splits the packet instead. | 25 | 37 | kept |
| If blocked (AI Studio cannot import, run tests, push, or keeps failing the same check after two attempts), tell the owner what happened, with a | 26 | 38 | kept |
| screenshot or copied output, and what you need. | 26 | 38 | kept |
| Do not work around a rule in LAB_RULES.md. | 26 | 38 | kept |
| You are working in the Astrid planet lab (banodoco/planet), at commit &lt;main SHA&gt;. | 31 | 43 | kept |
| Read LAB_RULES.md and packets/&lt;ID&gt;.md completely before changing anything. | 32 | 44 | kept |
| Do packet &lt;ID&gt; exactly as written, and nothing in its "Not in this packet" list. | 33 | 45 | kept |
| Run npm run check and npm run build, and fix failures within the packet's scope. | 34 | 46 | kept |
| Write packets/&lt;ID&gt;.result.md as described in packets/README.md. | 35 | 47 | kept |
| Commit with messages starting "&lt;ID&gt;:" and push to the branch lab/&lt;ID&gt;. | 36 | 48 | kept |
| Never push to main. | 36 | 48 | kept |
| If anything in the brief is unclear or looks wrong, stop and write that in the result note instead of guessing. | 37 | 49 | kept |
| Do not merge without an accept verdict, edit briefs yourself, change LAB_RULES.md, run two packets in one session or write a verdict: verdicts and briefs | 40 | 52 | kept |
| belong to the reflection reviewer, and the look to the owner. | 40 | 52 | kept |

Count: 63 found; 63 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/manager/astra-reflection.md

Source: `skills/roles/astrid-dev-manage/workstreams/astra-reflection.md` at INT source fd8a9a04 (latest ported source). Destination: `agent/roles/manager/astra-reflection.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: Every pushed lab packet has a recorded verdict (accept, rework or split), and the queue ahead matches what has actually been learned. | 9 | 13 | kept |
| When to use: When the run's manager hands you a lab packet at Gate, at each RF row of a lab run board, and at | 10 | 9 | kept |
| the owner's daily look, for a current lab run with an explicit run board. | 10 | 9 | kept |
| Inputs: The run board, the lab repository and its LAB_RULES.md and packets/, the pushed branch and result note, the owner's notes the manager passes on, | 11 | 17 | kept |
| and the run's authority. | 11 | 17 | kept |
| Procedure: Gate each packet by rerunning its proof and reading its diff | 12 | 21 | kept |
| at RF rows, re-estimate and rewrite the next briefs | 12 | 21 | kept |
| draft the daily look | 12 | 21 | kept |
| return everything to the manager. | 12 | 21 | kept |
| Completion: Each reviewed packet has a verdict returned to the manager naming its commit, every rework names what done looks like, and the next Ready | 13 | 25 | kept |
| packets have current briefs. | 13 | 25 | kept |
| Runs on the high-judgment role (Astra on Codex, Opus on Claude | 15 | 27 | kept |
| routing). | 15 | 27 | kept |
| AI Studio cannot take screenshots, so the proof you can check is tests and the diff | 15 | 27 | kept |
| the look is the owner's, at the daily look. | 15 | 27 | kept |
| A packet that changes what a visitor sees is not finished until the owner has seen it, but it may be merged into the lab | 15 | 27 | kept |
| before then. | 15 | 27 | kept |
| Pull lab/&lt;id&gt; at the commit the manager gives you. | 19 | 31 | kept |
| Merge the lab's current main into it locally if main moved. | 19 | 31 | kept |
| Rerun npm install, npm run check and npm run build yourself. | 20 | 32 | kept |
| AI Studio's own report is not proof. | 20 | 32 | kept |
| Read the whole diff against the brief and LAB_RULES.md. | 21 | 33 | kept |
| Check especially: nothing from *Not in this packet* | 21 | 33 | kept |
| the engine invariants (one seeded random in the same order, one clock, every allocation through own(), no module-level mutable state, the same build and update | 21 | 33 | kept |
| order, no allocation in the frame loop) | 21 | 33 | kept |
| no existing test edited or weakened | 21 | 33 | kept |
| for parity packets, sceneFingerprint snapshot untouched | 21 | 33 | kept |
| no new dependency | 21 | 33 | kept |
| files under 1,200 lines. | 21 | 33 | kept |
| If you have a browser, open the preview at the brief's *Look at* settings and say what you saw | 22 | 34 | kept |
| this is a sanity check, not the owner's verdict. | 22 | 34 | kept |
| Decide: | 23 | 35 | kept |
| - Accept: say ACCEPT with the reviewed commit. | 24 | 36 | kept |
| The run's manager merges lab/&lt;id&gt; into the lab's main with a merge commit (or you do, if the run gives you that access), marks the | 24 | 36 | kept |
| packet Accepted on the board with the merge commit, and makes the next packets Ready. | 24 | 36 | kept |
| - Rework: write a short rework prompt naming each failure and what done looks like, for the manager to paste into AI Studio | 25 | 37 | kept |
| mark Rework. | 25 | 37 | kept |
| At most two rounds. | 25 | 37 | kept |
| - Split: if the packet was too big or two things at once, accept what is sound (or nothing), write the new briefs in packets/, | 26 | 38 | kept |
| and update the queue. | 26 | 38 | kept |
| Return the verdict to the manager, one line per finding, sorted BLOCKING / FOLLOW-UP / NOTE. | 27 | 39 | kept |
| File follow-ups as later packets, not as silent fixes. | 27 | 39 | kept |
| Once a day, draft the daily look for the manager to give the owner: what was accepted since the last one, the lab main commit | 31 | 43 | kept |
| to open in AI Studio's preview, and for each visible change the exact sizes, address options (?planet-test-pose=fixed, ?sky=HH:MM) and landmarks to look at. | 31 | 43 | kept |
| The owner replies to the manager with notes. | 31 | 43 | kept |
| Each note becomes a rework, a new packet or a ruling on the board | 31 | 43 | kept |
| the owner's verdict on the look is final. | 31 | 43 | kept |
| At each RF row on the board: compare actual effort, rework rounds and AI Studio's failures with the estimates | 35 | 47 | kept |
| read the owner's notes since the last RF | 35 | 47 | kept |
| re-cut, merge or split the packets ahead and rewrite their briefs against the lab's current code (line ranges move as the engine is split) | 35 | 47 | kept |
| restate the remaining estimate. | 35 | 47 | kept |
| Record what changed and why on the board. | 35 | 47 | kept |
| Ask a second high-judgment reviewer for a zoomed-out opinion at RF-B and RF-D. | 35 | 47 | kept |
| Do not merge anything into the product repository, change the lab's upstream.json base, relax LAB_RULES.md or a test, or start integration (IN rows) without the | 37 | 49 | kept |
| owner's go. | 37 | 49 | kept |

Count: 55 found; 55 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/manager/live-loop.md

Source: `skills/roles/astrid-dev-manage/workstreams/live-loop.md` at M. Destination: `agent/roles/manager/live-loop.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: A plan whose end state holds on two consecutive live rounds, with every round, fix and plan delta recorded. | 9 | 13 | kept |
| When to use: When an accepted plan's end state is clear but its tasks can only be found by measuring the live product round by | 10 | 9 | kept |
| round. | 10 | 9 | kept |
| Inputs: The accepted loop plan and its scenario set, a running stack built from the plan branches, the run's bindings in run.yaml, and the floors | 11 | 17 | kept |
| to stop at. | 11 | 17 | kept |
| Procedure: Run the scenarios live, record the round, ask the strategist, pick the smallest fixes, land each as an Iterate PR into the plan branch, | 12 | 21 | kept |
| rebuild and rerun. | 12 | 21 | kept |
| Completion: The plan's end state holds on two consecutive rounds, or the loop stops at a recorded reason and the owner has the open question. | 13 | 25 | kept |
| Use when the plan is a loop plan: its end state is known, its tasks can't be written up front, and its tasks.md ends in | 15 | 27 | kept |
| one standing loop card. | 15 | 27 | kept |
| Everything in whole project still applies (progress, decisions, dispatch) | 15 | 27 | kept |
| this adds the round. | 15 | 27 | kept |
| The run contract governs routes, proof and review | 15 | 27 | kept |
| it is not restated here. | 15 | 27 | kept |
| Coordinator (the manager session): keeps the judgment. | 19 | 31 | kept |
| Reads every round row and picks the fixes. | 19 | 31 | kept |
| Treats what Codex and the strategist return as evidence to check. | 19 | 31 | kept |
| Execution runs on Codex: the heavy lifting, N normally and X for a hard fix, each bound to a model and effort in the run's | 20 | 32 | kept |
| run.yaml. | 20 | 32 | kept |
| Run in the background, one worktree per fix: | 20 | 32 | kept |
| codex exec -m &lt;model from run.yaml&gt; --skip-git-repo-check -C &lt;dir&gt; -s workspace-write -o &lt;scratch&gt;/&lt;name&gt;.txt "&lt;brief&gt;" &lt; /dev/null | 21 | 33 | kept |
| Add -c model_reasoning_effort='"&lt;effort from run.yaml&gt;"'. | 22 | 34 | kept |
| Strategist: the run's high-judgment advisor binding, read-only (-s read-only), consulted on strategy each round. | 23 | 35 | kept |
| Its advice is evidence, not a verdict | 23 | 35 | kept |
| it tends to over-engineer, so ask it what to remove first. | 23 | 35 | kept |
| Run the scenario set live, against the real installed stack, over its public interface only (the browser or the public API), never in-process. | 27 | 39 | kept |
| Record a round row in the plan's rounds.md: what saved | 28 | 40 | kept |
| what was refused, with the reason shown | 28 | 40 | kept |
| timings | 28 | 40 | kept |
| anything that vanished | 28 | 40 | kept |
| the stack's versions. | 28 | 40 | kept |
| Ask the strategist: give it the row and the previous rows, not your conclusion. | 29 | 41 | kept |
| Pick the fixes. | 30 | 42 | kept |
| Each is one failing scenario, a cause, and the smallest change at its source. | 30 | 42 | kept |
| Fix each as an ordinary Iterate run, a PR into the plan branch, with the failing live scenario as its red test. | 31 | 43 | kept |
| Rebuild the stack and rerun from step 1. | 32 | 44 | kept |
| Append each round's rows, picks and PRs under the loop card in tasks.md | 34 | 46 | kept |
| progress PRs follow whole project. | 34 | 46 | kept |
| Stop when the plan's end state holds on two consecutive rounds, or when a round finds nothing new and the remaining refusals are real clashes. | 38 | 50 | kept |
| Stop and ask the owner when three rounds in a row fix nothing, a floor below (disk) is reached, or the end state needs a | 38 | 50 | kept |
| design change bigger than a card. | 38 | 50 | kept |
| Each round also writes plan deltas: what the live evidence changes in the follow-up plans (a task to drop, add, re-estimate or renumber). | 40 | 52 | kept |
| They go in rounds.md, one list per round, and the manager carries them into those plans' PRs at the end. | 40 | 52 | kept |
| A fresh browser profile for every run, deleted afterwards. | 44 | 56 | kept |
| Headless profiles and stack copies are what filled the disk twice on 18 November. | 44 | 56 | kept |
| Check free disk before each round and stop below the floor the plan names. | 45 | 57 | kept |
| Never edit the owner's timelines or projects: scenarios run on a fixture built in a sandbox project. | 46 | 58 | kept |

Count: 47 found; 47 kept; 0 restored; 0 moved; 0 superseded.


## agent/roles/orchestrator/codex-cloud-sessions.md

Source: `skills/roles/astrid-dev-orchestrate/workstreams/codex-cloud-sessions.md` at M. Destination: `agent/roles/orchestrator/codex-cloud-sessions.md`. Workstream contract summary is represented by the new five headed sections; procedure/authority and proof boundaries are also checked against the body.

| Rule (source excerpt) | Source line | Agent line | Status |
| --- | --- | --- | --- |
| Outcome: Separate Codex Cloud sessions coordinated through one durable mailbox, with ownership and handoffs preserved. | 9 | 13 | kept |
| When to use: When an authorized Orchestrator and plan manager work in different Codex Cloud chats. | 10 | 9 | kept |
| Inputs: An accepted plan, named accountable manager, permitted session identities, mailbox, task boundaries and tested resume mechanism. | 11 | 17 | kept |
| Procedure: Register sessions, send bounded briefs, reconcile their evidence and recover stalled work using the linked Codex Cloud guide. | 12 | 21 | kept |
| Completion: The manager has a complete session handoff and traceable task evidence | 13 | 25 | kept |
| unwakeable sessions are reported rather than assumed active. | 13 | 25 | kept |
| Choose this when the orchestrator and plan managers work in different Codex Cloud chats. | 15 | 27 | kept |
| For the actual mailbox commands, session registration, authentication limits, acknowledgments, polling and recovery use the existing Codex Cloud guide | 15 | 27 | kept |
| its scripts remain in that directory. | 15 | 27 | kept |
| Start from an accepted plan and its authorized Run start | 17 | 29 | kept |
| name one accountable plan manager. | 17 | 29 | kept |
| Use the plan's board (rules) and agree durable per-session identities and cursors. | 17 | 29 | kept |
| Give each session the plan/task links, exact proof, branches, limits and its manager/advisor roles. | 18 | 30 | kept |
| Follow Manage inside the accountable manager session. | 18 | 30 | kept |
| Follow the agreed check-in cadence to reconcile GitHub evidence and recover stalled sessions | 19 | 31 | kept |
| a GitHub comment or timer alone cannot wake an idle Codex Cloud chat. | 19 | 31 | kept |
| Do not promise unattended progress without a verified resume mechanism. | 19 | 31 | kept |
| When a Release Lead has prepared multiple packet briefs, combine this environment workstream with multi-manager dispatch. | 21 | 33 | kept |
| The dispatch board and packet files still live under the release, not in GitHub issue bodies. | 21 | 33 | kept |

Count: 19 found; 19 kept; 0 restored; 0 moved; 0 superseded.

*Draft in progress: remaining 7 document audits follow before READY-PROOF.*
