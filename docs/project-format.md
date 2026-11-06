# Project folders: one entry point, room to grow

Each project gets a stable folder under `plans/`. A reader should be able to open **`plan.md`** and understand the outcome, what already exists, what happens next, and what counts as done. The other two files answer practical questions:

| Required file | What belongs here |
|---|---|
| `plan.md` | The goal, scope, starting point, sequence, completion boundary, and a [vision gap](../visions/gaps.md) relationship (or enabler rationale). Link supporting details. |
| `tasks.md` | The work index. A ready task identifies its outcome, route or responsible role, dependencies, focused evidence, and progress. |
| `inputs.md` | The sources the work relies on: code and branches, a brief, visual references, research data, an existing decision, or a predecessor's output. Record identity and limitations where they matter. |

These are three questions, not three long forms. A draft can answer each in a few lines and name what is unknown. A software change needs base and donor commits; a design study may need a brief, source frames, and comparison criteria instead. See the [copyable template](../templates/project/plan.md).

## Extend for a real job

Add a file or folder when a reader needs to **use or maintain that material independently**. Link it from its natural home: specifications from `plan.md`, assignments from `tasks.md`, and source material from `inputs.md`. Keep a single authoritative copy. A small project can stay at three files throughout its life.

The [Astrid website](../plans/21-astrid-website/plan.md) illustrates the distinction:

| Website material | Why it has its own home |
|---|---|
| [`design.md`](../plans/21-astrid-website/design.md) | Many tasks depend on the same visitor journey, copy, visual rules, and motion specification. The plan can explain the goal in a page. |
| [`mockups/`](../plans/21-astrid-website/mockups/) | Day/night reference frames show the intended result. Link the exact frame from the task that needs it. |
| [`tasks/`](../plans/21-astrid-website/tasks/) | The 34 implementation cards have five distinct phases. `tasks.md` indexes them; each phase file holds its cards once. |
| [`evidence/`](../plans/21-astrid-website/evidence/) | Prior inspections and reviews record what was observed and why decisions were made. A mockup is a target, not proof that the site matches it. |

Generation has a different extension: its [environment recipes](../plans/02-consistent-generation/env/README.md) describe the setup needed to reproduce its focused checks. Those recipes belong with that project; other projects do not need an `env/` folder by default.

Use the same test for other kinds of work. A research project might link a question to a study protocol, a dataset version, and findings. A release might need a platform matrix and release receipts. Use names that describe the material; don't create all of those folders for every project. Keep large generated artifacts in their durable source store and link the version needed for review. Material used by several projects belongs in a shared source, linked by each project.

Keep work inside a project when it serves that project's outcome. Give it its own project when it has an independently useful result, can be prioritized or owned separately, and can hand a named output back. A long specification alone is a reason for a supporting document, not a new project.

## At catalog scale

Keep folder IDs stable as priorities, owners, and status change. Link dependencies to project or task outputs, not to row numbers. Archiving moves the index entry; it does not move its sources or break its links.

Today the [queue](../README.md) owns active/upcoming metadata and the [archive](../ARCHIVE.md) owns terminal entries. At hundreds or thousands of projects, discovery becomes the constraint: the front page should show active work and a short upcoming list, with searchable views of the rest. When the manual index stops serving that job, **migrate** its fields to one small record per project (for example `plan.md` front matter), and derive views by status, owner, or project type. Do not start hand-maintaining both a catalog and copies of the same metadata. The folder structure need not change for that migration.
