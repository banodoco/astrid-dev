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

*Draft in progress: remaining 15 document audits follow before READY-PROOF.*
