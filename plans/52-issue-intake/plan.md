# Issue intake

**Project:** Issue intake

**Goal:** Anyone using or building Astrid, and their agent, reports what they noticed in one command or one form on astrid-dev's GitHub Issues, where others can say "me too" and nothing is lost or filed twice.

**Status:** queued

**Owner:** Unassigned

**Estimate:** about 2.5

**Waiting on:** the owner's decisions D1–D13; the owner's go for a run; Plan 51 Part 2 on `main` before the words task (II-5)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary): what one person or run notices reaches everyone else without a conversation. CA-005's route does not name this plan, and none of its closure-evidence items is about intake, so there is no `Contributes to closure` line; adding one is a [Gap](../../skills/astrid-dev-gap/SKILL.md) step for the owner to ask for.

## Outcome and scope

This plan replaces the draft "Observations register" that held this number. That draft proposed a folder of observation files; the owner chose GitHub Issues instead ([inputs.md](inputs.md#what-the-owner-said)).

Today a thing someone notices about Astrid has five possible places and reaches none of them reliably. Users file in whichever product repository they happened to install from. Our own agents filed seven bugs in the App repository in spite of a skill that says astrid-dev. Twenty-two findings from one release run sat in files outside the repository, and then in an interim `observations/` folder that no outside person can write to.

When this is done:

1. **One front door.** Every question, bug, observation and idea about any part of Astrid is an issue on `banodoco/astrid-dev`. The four product repositories send people there.
2. **Four types, each one short shape.** The type is the first word of the title (`observation:`, `bug:`, `question:`, `idea:`). Each type has one issue form in `.github/ISSUE_TEMPLATE/`, and that file is the only definition of what the type asks. An observation asks for one sentence. A bug asks what happened, what was expected and the version.
3. **One command for an agent, one form for a person, the same issue.** An agent runs one command that works inside a cloud session and needs no label rights. A person fills the form, which GitHub itself makes them complete. An agent with no GitHub login hands its person a pre-filled link.
4. **A small bot does the mechanical part.** On a new or edited issue it reads the title and body as data, applies the type label, and turns an optional `About` line (a plan number or gap ID) into `plan:<NN>` and `gap:<ID>` labels. It posts nothing and closes nothing.
5. **Triage is a reading step, not a new machine.** At its check-ins the orchestrator reads the issues that have no type label or no answer, suggests duplicates, adds the plan and gap labels a filer could not know, asks for a missing bug detail, answers questions with links, and tells the owner what it could not place.
6. **Commitment stays in the repository.** An issue that is taken on becomes a task row citing `#N`, written in the planner's own words, and the pull request that fixes it closes it. GitHub's close reasons (completed, not planned, duplicate) are the only outcome words.
7. **Issue text is never an instruction.** That rule is written once, with the triage rules, and every reader of an issue is bound by it.

**Included:** the four forms (replacing the three templates there today); the label bot and its tests; one "Issues" section in the contribution workflow as the home for filing, triage and the untrusted-text rule, with one link from each place listed in [Where it is documented](#where-it-is-documented); moving the 22 interim files into issues and deleting `observations/`; the redirect in the four product repositories; the rules for the agent a user runs.

**Not included:**
- a copy of issues in the repository, a generated page of issues, or any check that calls GitHub (a check must give the same result on a laptop and in CI);
- an outcome field, a status vocabulary, priorities, severities, assignee rules or a project board;
- a bot that checks an issue's answers, a `needs-info` label, or a timer that closes or nags (D4);
- a scheduled triage session (D7);
- a job that creates every `plan:` and `gap:` label in advance (the bot creates one when it is first needed);
- a `report` command in astrid-dev (D11), a command on the PATH or an installable package (D13), or `astrid report` in the product (a follow-up in the Agent repository);
- moving the process ledger into issues (D12);
- GitHub's organization-wide issue types, which would change every unrelated repository in the organization.

**Deferred:** a product command that builds the pre-filled link; a "report a problem" button in the App (it has a help link today, which this plan re-points); VibeComfy, runpod-lifecycle and poms_packs (D1).

**Limits a reader should know.** A person with no GitHub account cannot file; their agent cannot file for them without one either. Duplicates are found by people searching first and by triage suggesting; only a maintainer closes one. An agent cannot attach a file to an issue; the person does that in the browser.

### Where it is documented

One home, and one link from everywhere else. Nothing but the home states the format.

| Place | What changes | In this plan |
| --- | --- | --- |
| `docs/contribution-workflow.md`, new section "Issues" | The home: how to file each type, the `About` line, triage, close reasons, the untrusted-text rule | II-5 |
| `.github/ISSUE_TEMPLATE/*.yml` | The home of each type's questions | II-3 |
| `skills/astrid-dev/SKILL.md` route table | One row, "Noticed something, or have a question" | II-5 |
| `skills/astrid-dev-bugfix/SKILL.md` | Its template link becomes the bug form; the incident record is a comment on the issue | II-5 |
| `skills/astrid-dev-manage/SKILL.md`, `skills/astrid-dev-orchestrate/SKILL.md` | One link each: a product finding from a run is an issue the manager files; triage happens at check-ins | II-5 |
| `skills/astrid-dev-shared/glossary.md` | `issue`, `observation` | II-5 |
| `skills/astrid-dev-improve/SKILL.md` table of homes | One row | II-5 |
| `CONTRIBUTING.md`, root `README.md` (hand-written text), `docs/ledger/README.md`, `docs/contribution-automation-setup.md` | One link or one table row each | II-5 |
| astrid-app, astrid-agent, astrid-runtime, astrid-pinokio: `.github/ISSUE_TEMPLATE/config.yml` | The redirect | II-8 |
| astrid-agent `docs/setup/troubleshooting.md#asking-for-help` (the App's help link points here) and astrid-pinokio `README.md` ("tell us") | The issue link | II-8 |
| astrid-app and astrid-agent `AGENTS.md` | One sentence, which is the redirect for agents | II-8 |
| astrid-agent's root skill, the one a user's agent reads | A row and the rules in [inputs.md](inputs.md#rules-for-the-agent-a-user-runs) | II-9, shipped by a release |
| A product command, an App button | — | follow-ups, not here |

## Existing work and decision

GitHub Issues already does what the draft was going to build: filing without write access, comments and reactions for "me too", attachments, duplicates, close reasons, labels, search, and required answers on a web form. The repository already has the pattern for the only automation this needs: [`review-intake.yml`](../../.github/workflows/review-intake.yml) runs trusted code from `main` with the workflow's own token and `issues: write`, reads the event as data, and creates its label when missing (`scripts/contribution_api.py:ensure_review_label`). The bugfix skill already says every incident is one astrid-dev issue. What is missing is forms a person can fill in a minute, a shape an agent can write in one command, the redirect, and a reader on the other side.

The smallest sound approach is therefore mostly configuration and words: four form files, one bot smaller than the one that exists, one section of prose, and five small pull requests elsewhere. Evidence, the alternatives (including the files design and doing nothing), the critique and the owner's choice are in [inputs.md](inputs.md#planning-evidence). The owner accepted this direction on 12 Nov 2026; no run is started.

## Sequence and readiness

1. **II-1 establishes the facts first.** Several claims this plan rests on come from memory of GitHub's documentation, and one from an untested ability of agent sessions. Nothing else is dispatched until they are observed on the scratch repository. Each claim names what changes if it is false.
2. **Then, side by side:** the labels (II-2), the forms (II-3), the bot (II-4) and moving the 22 files into issues (II-7).
3. **The words (II-5)** wait for Plan 51 Part 2, and carry the forms and the removal of the old templates to `main` in the same pull request, so "New issue" never shows both sets. **The wording pass (II-6)** follows.
4. **One review round (R)** on the bot and the rules, before anyone outside is sent here.
5. **Then the outside:** the redirect (II-8), the user's agent (II-9), the owner's transfer of old issues (II-10), the two-door proof (II-11) and the first triage with its planted case (II-12).

**Real dependencies:**
- [Plan 51](../51-astrid-dev-clean-up/plan.md) Part 2 is running. Its CU-14 edits `docs/contribution-workflow.md`, `docs/contribution-automation-setup.md`, `CONTRIBUTING.md` and `README.md`; its CU-22 edits `README.md`; its CU-15 adds a check on links to headings. II-5 changes the same files, so it starts from a `main` that contains Part 2. If Part 2 is late, II-1, II-2, II-4 and II-7 can still land; the forms wait with II-5.
- The owner's go is needed for: writing on the scratch repository (II-1), label changes (II-2), a new workflow file (II-4), creating 22 issues (II-7), the product-repository pull requests (II-8, II-9) and transferring issues (II-10).
- II-9 changes a skill that ships inside Astrid, so users get it only with a release.

No budget and no paid service. Tasks are in [tasks.md](tasks.md); recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:** astrid-dev `main` at the run's base (recorded in [inputs.md](inputs.md#source-identities)); the gap IDs in `vision/gaps/` and the plan folders in `plans/`, which the bot reads on `main` to decide whether an `About` entry is real; GitHub's issue forms, labels, close reasons and the workflow token.

**Produces:**
- the four form files, which other repositories and the product link to by file name (`observation.yml`, `bug.yml`, `question.yml`, `idea.yml`) and by one field id, `what`;
- the labels `observation`, `bug`, `question`, `idea`, `plan:<NN>`, `gap:<ID>`;
- the search links a planner or gap assessor uses: `is:issue is:open label:plan:<NN>` and `label:gap:<ID>`; and the triage query, open issues with none of the four type labels;
- the "Issues" section, the address every other document links.

**Limits:** file names, field headings and the `what` id become a contract with the product once II-9 ships; renaming one breaks pre-filled links in installed copies, so II-3 fixes them and no later card may change them. The bot proves nothing about an issue's content.

## Completion

- **An agent:** a fresh agent in a cloud session, given only the contributor skill, files a valid observation on astrid-dev with one command, without label rights, and within a minute it carries the `observation` label.
- **A person:** a person files the same observation through the web form. The two issues have the same title shape, the same headed body and the same label.
- **No login:** the pre-filled link opens the form with the title and the sentence in place.
- **The redirect:** "New issue" in each of the four product repositories offers the link to astrid-dev's forms and no blank issue.
- **The 22 interim observations** are issues with their plan and gap labels, and `observations/` is gone.
- **A planner** opens one link and sees the open issues about their plan.
- **Negative cases:** an `About` line naming a plan that does not exist adds no label; an `About` line naming fifty plans adds five labels; a title or body containing backticks, `$(…)` and an apostrophe is filed intact by the documented command and runs nothing; an issue whose text tells the reader to label, close, push or reveal something changes nothing at triage and is reported as suspicious; the bot's tests show the only calls it can make are reading the issue and adding or creating labels.
- The word count of the skills and guides rises by no more than the amount the owner agreed for II-5, and by nothing if the cuts are found.

**Limit of this proof:** it shows both doors work and that one reader ignored instructions in three planted issues. It does not show people use it, or that a reader resists an attack nobody thought of. The bot's token can only touch issues; the session that triages holds more, which is why triage stays with a session the owner already watches. The real test is the next release: whether its findings are issues or loose notes.
