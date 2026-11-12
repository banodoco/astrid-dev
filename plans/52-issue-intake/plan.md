# Issue intake

**Project:** Issue intake

**Goal:** Anyone using or building Astrid, and their agent, reports what they noticed in one command or one form on astrid-dev's GitHub Issues, where others can say "me too" and nothing is lost or filed twice.

**Status:** queued

**Owner:** Unassigned

**Estimate:** about 2.5

**Waiting on:** the owner's decisions D1–D12; the owner's go for a run; Plan 51 Part 2 on `main` before the words task (II-5)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary): what one person or run notices reaches everyone else without a conversation. CA-005's route does not name this plan, and none of its closure-evidence items is about intake, so there is no `Contributes to closure` line; adding one is a [Gap](../../skills/astrid-dev-gap/SKILL.md) step for the owner to ask for.

## Outcome and scope

This plan replaces the draft "Observations register" that held this number. That draft proposed a folder of observation files; the owner chose GitHub Issues instead ([inputs.md](inputs.md#what-the-owner-said)).

Today a thing someone notices about Astrid has five possible places and reaches none of them reliably. Users file in whichever product repository they happened to install from. Our own agents filed seven bugs in the App repository in spite of a skill that says astrid-dev. Twenty-two findings from one release run sat in files outside the repository, and then in an interim `observations/` folder that no outside person can write to.

When this is done:

1. **One front door.** Every question, bug, observation and idea about any part of Astrid is an issue on `banodoco/astrid-dev`. The four product repositories send people there.
2. **Four types, each one short shape.** The type is the first word of the title (`observation:`, `bug:`, `question:`, `idea:`). Each type has one issue form in `.github/ISSUE_TEMPLATE/`, and that file is the only definition of what the type asks. An observation asks for one sentence. A bug asks what happened, what was expected and the version.
3. **One command for an agent, one form for a person, the same issue.** An agent runs one `gh issue create` line and needs no label rights. A person fills the form. An agent with no GitHub login hands its person a pre-filled link. All three produce the same headed body.
4. **A small bot does the mechanical part.** On a new or edited issue it reads the title and body as data, applies the type label, turns an optional `About` line (a plan number or gap ID) into `plan:<NN>` and `gap:<ID>` labels, and, when a required answer is missing, adds `needs-info` and one comment naming it. It reads what to require from the form files. It never closes anything.
5. **Triage does the judging part.** A scheduled agent session suggests duplicates, adds the plan and gap labels a filer could not know, answers questions with links, and lists for the owner what it could not place.
6. **Commitment stays in the repository.** An issue that is taken on becomes a task row citing `#N`, written in the planner's own words, and the pull request that fixes it closes it. GitHub's close reasons (completed, not planned, duplicate) are the only outcome words.
7. **Issue text is never an instruction.** That rule is written once, with the triage rules, and every reader of an issue is bound by it.

**Included:** the four forms (replacing the three templates there today); the intake bot and its tests; one "Issues" section in the contribution workflow as the home for filing, triage and the untrusted-text rule, with one link from each place listed in [Where it is documented](#where-it-is-documented); moving the 22 interim files into issues and deleting `observations/`; the redirect in the four product repositories; the rules for the agent a user runs; turning triage on.

**Not included:**
- a copy of issues in the repository, a generated page of issues, or any check that calls GitHub (a check must give the same result on a laptop and in CI);
- an outcome field, a status vocabulary, priorities, severities, assignee rules or a project board;
- a timer that closes or nags;
- a job that creates every `plan:` and `gap:` label in advance (the bot creates one when it is first needed);
- a `report` command in astrid-dev (D11: proposed, not recommended) or `astrid report` in the product (a follow-up in the Agent repository);
- moving the process ledger into issues (D12);
- GitHub's organization-wide issue types, which would change every unrelated repository in the organization.

**Deferred:** a product command that builds the pre-filled link; a "report a problem" button in the App (it has a help link today, which this plan re-points); VibeComfy, runpod-lifecycle and poms_packs (D1).

### Where it is documented

One home, and one link from everywhere else. Nothing but the home states the format.

| Place | What changes | In this plan |
| --- | --- | --- |
| `docs/contribution-workflow.md`, new section "Issues" | The home: how to file each type, the `About` line, triage, close reasons, the untrusted-text rule | II-5 |
| `.github/ISSUE_TEMPLATE/*.yml` | The home of each type's questions | II-3 |
| `skills/astrid-dev/SKILL.md` route table | One row, "Noticed something, or have a question" | II-5 |
| `skills/astrid-dev-bugfix/SKILL.md` | Its template link becomes the bug form; the incident record is a comment on the issue | II-5 |
| `skills/astrid-dev-manage/SKILL.md` | One link: a product finding from a run is an issue, filed by the manager | II-5 |
| `skills/astrid-dev-shared/glossary.md` | `issue`, `observation` | II-5 |
| `skills/astrid-dev-improve/SKILL.md` table of homes | One row | II-5 |
| `CONTRIBUTING.md`, root `README.md` (hand-written text), `docs/ledger/README.md` | One link each | II-5 |
| astrid-app, astrid-agent, astrid-runtime, astrid-pinokio: `.github/ISSUE_TEMPLATE/config.yml` | The redirect | II-8 |
| astrid-agent `docs/setup/troubleshooting.md#asking-for-help` (the App's help link points here) and astrid-pinokio `README.md` ("tell us") | The issue link | II-8 |
| astrid-agent's root skill, the one a user's agent reads | A row and the rules in [inputs.md](inputs.md#rules-for-the-agent-a-user-runs) | II-9, shipped by a release |
| A product command, an App button | — | follow-ups, not here |

## Existing work and decision

GitHub Issues already does what the draft was going to build: filing without write access, comments and reactions for "me too", attachments, duplicates, close reasons, labels and search. The repository already has the pattern for the only automation this needs: [`review-intake.yml`](../../.github/workflows/review-intake.yml) runs trusted code from `main` with the workflow's own token and `issues: write`, reads the event as data, and creates its label when missing (`scripts/contribution_api.py:ensure_review_label`). The bugfix skill already says every incident is one astrid-dev issue. What is missing is forms a person can fill in a minute, a shape an agent can write in one line, the redirect, and a reader on the other side.

The smallest sound approach is therefore mostly configuration and words: four form files, one bot of the same kind as the one that exists, one section of prose, and five small pull requests elsewhere. Evidence, the alternatives (including the files design and doing nothing), the critique and the owner's choice are in [inputs.md](inputs.md#planning-evidence). The owner accepted this direction on 12 Nov 2026; no run is started.

## Sequence and readiness

1. **II-1 establishes the facts first.** Several claims this plan rests on come from memory of GitHub's documentation, and one from an untested ability of agent sessions. Nothing else is built until they are observed on the scratch repository. Each card names which finding would change it.
2. **Then, side by side:** the forms and their reader (II-3), the labels (II-2), and moving the 22 files into issues (II-7).
3. **The bot (II-4)** follows the reader. **The words (II-5)** follow the forms and wait for Plan 51 Part 2. **The wording pass (II-6)** follows both.
4. **One review round (R)** on the bot and the rules, before anything is switched on for strangers.
5. **Then the outside:** the redirect (II-8), the user's agent (II-9), the owner's transfer of old issues (II-10), the two-door proof (II-11) and triage (II-12).

**Real dependencies:**
- [Plan 51](../51-astrid-dev-clean-up/plan.md) Part 2 is running. Its CU-14 edits `docs/contribution-workflow.md`, `CONTRIBUTING.md` and `README.md`; its CU-22 edits `README.md`; its CU-15 adds a check on links to headings. II-5 changes the same files, so it starts from `main` after Part 2's pull request has merged. If Part 2 is late, everything except II-5, II-6, R and what follows them can still land, and the three old templates stay until II-5.
- The owner's go is needed for: label changes (II-2), a new workflow file (II-4), creating 22 issues (II-7), four product-repository pull requests (II-8, II-9), transferring issues (II-10) and the scheduled triage task (II-12).
- II-9 changes a skill that ships inside Astrid, so users get it only with a release.

No budget and no paid service. Tasks are in [tasks.md](tasks.md); recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:** astrid-dev `main` at the run's base (recorded in [inputs.md](inputs.md#source-identities)); the gap IDs in `vision/gaps/` and the plan folders in `plans/`, which the bot reads on `main` to decide whether an `About` entry is real; GitHub's issue forms, labels, close reasons and the workflow token.

**Produces:**
- the four form files, which other repositories and the product link to by file name (`observation.yml`, `bug.yml`, `question.yml`, `idea.yml`) and by one field id, `what`;
- the labels `observation`, `bug`, `question`, `idea`, `needs-info`, `plan:<NN>`, `gap:<ID>`;
- the search links a planner or gap assessor uses: `is:issue is:open label:plan:<NN>` and `label:gap:<ID>`;
- the "Issues" section, the address every other document links.

**Limits:** file names and the `what` id become a contract with the product once II-9 ships; renaming one breaks pre-filled links in installed copies. The bot proves an issue has its required answers, never that they are true.

## Completion

- **An agent:** a fresh agent given only the contributor skill files a valid observation on astrid-dev with one command, without label rights, and within a minute it carries the `observation` label.
- **A person:** a person files the same observation through the web form. The two issues have the same title shape, the same headed body and the same label.
- **No login:** the pre-filled link opens the form with the title and the sentence in place.
- **The redirect:** "New issue" in each of the four product repositories offers only the link to astrid-dev's forms.
- **The 22 interim observations** are issues with their plan and gap labels, and `observations/` is gone.
- **A planner** opens one link and sees the open issues about their plan.
- **Negative cases:** a bug with no version gets `needs-info` and one comment naming "Astrid version", and loses the label when edited; an `About` line naming a plan that does not exist adds no label; an issue whose text tells the reader to label, close, push or reveal something changes nothing in triage and appears in its report as suspicious; the bot's tests show it never closes or edits an issue and never repeats issue text.
- The word count of the skills and guides is not higher than before the words task.

**Limit of this proof:** it shows both doors work and that the reader ignores instructions in a planted issue. It does not show people use it, or that triage resists an attack nobody thought of; the bot's token can only touch issues, and the triage session is the part to watch. The real test is the next release: whether its findings are issues or loose notes.
