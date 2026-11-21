# Markdown-first agent documents and generated skills

**Project:** Markdown-first agent documents and generated skills

**Goal:** Astrid contributors and their agents can write each role and workstream once as an ordinary Markdown document, opt it into skill discovery with `skill: true`, and reliably use its generated skill without maintaining a separate authoring layout.

**Status:** active

**Owner:** ChatGPT Manager — Plan 73

**Estimate:** 8–12 engineering days, provisional until the reference-packaging probe and current baseline.

**Waiting on:** First package-contract review RS1 before migration, then final independent review R and required CI before main integration.

**Run route:** astrid-dev-only

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six fields above define the catalog row; do not edit the generated catalog or add this plan to [priority.md](../priority.md) without an owner decision. The entry links here deliberately reference the current system until the implementation migration.

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary).

**Contributes to closure:** CA-005: one canonical source for each agent instruction, a repeatable method to publish that source as a skill, a fresh-agent extension trial, and refusals for duplicate or broken generated skill packages. This does not prove the gap's real ten-contributor trial.

## Outcome and scope

**End state:** There is only one authored kind of agent instruction: Markdown under `agent/`. Roles are identities with standing responsibilities; workstreams are procedures. A role owns its specific workstreams, while shared workstreams live under `agent/shared/workstreams/`. Skill publication is a property of the document, not of its directory.

```text
agent/
  start.md
  roles/
    leader.md
    orchestrator.md
    manager.md
    worker.md
    leader/multi-manager-release.md
    orchestrator/{codex-cloud-sessions,codex-in-claude-cloud,multi-manager-dispatch}.md
    manager/{whole-project,chatgpt-packet}.md
  shared/
    run-contract.md
    glossary.md
    domains.md
    release-sources.md
    workstreams/{bugfix,gap,gpu-validate,green,improve,iterate,merge,plan,release}.md
    templates/
  guides/
    codex-cloud/
    codex-in-claude-cloud/
```

Every authored agent Markdown document has a short `description` in frontmatter. The optional literal `skill: true` marks an installable entry; omission means ordinary documentation. The name is `astrid-dev-` plus the Markdown filename stem, regardless of folder. Duplicate generated names fail. Any exception to that rule requires a new owner decision, not a hidden naming alias. The main `agent/start.md` thus becomes `astrid-dev-start`; roles become `astrid-dev-leader`, `astrid-dev-orchestrator`, `astrid-dev-manager` and `astrid-dev-worker`. All nine current shared workstreams retain their existing `astrid-dev-*` names. The six role-owned workstreams remain linked documents by default; each could independently opt in later.

The Markdown body is the complete instruction. Workstreams express when to use, outcome, inputs, procedure, completion and boundaries as readable sections; roles express standing responsibility, authority, responsibilities and handoff. Do not require a summary paragraph that duplicates a later procedure. Preserve every existing consequential rule, including permission boundaries, provenance, test integrity, release authority, model routing and evidence standards. A workstream's packaging cannot grant authority absent from the run.

**Derived output:** `python3 scripts/astrid_dev.py skills build` deterministically generates standard `.generated/skills/astrid-dev-<stem>/SKILL.md` packages with valid `name` and `description`, plus whatever accessible references are necessary. `skills check` validates source and generated package contracts; `skills install` builds and installs only this repository's packages into supported agent skill directories, with a dry run and conflict protection. The existing Markdown-view regeneration stays distinct, exposed as `views generate` rather than another ambiguous `sync` operation. Generated packages are ignored by Git and never become authored sources.

**Scope includes:** migrating the 14 packaged skills and six role-specific Markdown workstreams; relocating supporting guides, executable helpers, shared templates and references; replacing installer and dual-format validators; updating generated view declarations and documentation CI; changing all active references and examples that rely on old paths; removing legacy directory symlinks and obsolete index machinery; and exercising real Claude/Codex discovery on supported checkout-based setups.

**Boundaries:** no changes to product behavior, project/release authority, the public vision feed, plan statuses or release membership; no new agent role, approval step, database, framework or manually maintained skill registry. No broad refactor of unrelated project records or generated views. Historical evidence should preserve the paths actually used at the time; use revision-pinned links where useful, not false rewrites. Portability to arbitrary copied repositories or standalone published archives is deferred unless the packaging probe shows it is required for the supported installation path. Nothing here authorizes changing active Release 14 sessions, running product tests, or merging to `main`.

**The meaningful contrasts:**

1. **Documents define skills; skill folders no longer define documents.**
2. **One `skill: true` creates a discoverable skill; no registry or folder ceremony is added.**
3. **A role states who is responsible; a workstream states how to complete a particular job.**
4. **Leader, Orchestrator, Manager and Worker keep their standing authority regardless of the workstream selected.**
5. **Role-specific procedures live beside their role, while reusable procedures have one home under `shared/`.**
6. **One filename gives one predictable skill name; collisions fail rather than silently rename.**
7. **The build produces disposable standard skill packages; authors never edit `SKILL.md` output.**
8. **Shared run rules remain authoritative once, not duplicated into every generated package.**
9. **Old installation and alias code disappears rather than becoming a permanent compatibility layer.**
10. **A fresh agent can add a document and enable a skill with only metadata and documented checks.**

## Existing work and decision

This is a new, separately useful authoring-and-distribution outcome after the completed [Plan 48](../48-one-record-model/plan.md) and [Plan 51](../51-astrid-dev-clean-up/plan.md); neither owns converting authored `SKILL.md` packages into canonical Markdown and rebuilding the install flow. It contributes to the same existing CA-005 gap rather than inventing a gap that measures a particular implementation.

Reuse [`scripts/document_structure.py`](../../scripts/document_structure.py) for frontmatter and headings; [`scripts/workstreams.py`](../../scripts/workstreams.py) for workstream semantics where still useful; [`scripts/views.py`](../../scripts/views.py) for general generated-page projections and link rebasing; and [`scripts/astrid_dev.py`](../../scripts/astrid_dev.py) as the CLI entry. The old [`sync.sh`](../../sync.sh) has safety behaviors worth retaining in the new installer, but not its package-discovery model. The existing doc [CI workflow](../../.github/workflows/docs.yml) must keep its protected, declared-target writeback guard. Prior-art findings and rejected approaches live only in [inputs.md](inputs.md#planning-evidence).

The owner chose the **direction** in a 20 November 2026 planning conversation: Markdown sources, `skill: true`, filename-derived names, noun-based roles (Leader/Orchestrator/Manager/Worker), role-owned workstreams and shared workstreams in `shared/`, with permission for an aggressive cleanup. That initial direction alone was not an execution go; the later owner-authorized astrid-dev-only start is recorded in [inputs.md](inputs.md#owner-decisions). Reference packaging and active cutover choices remain open.

## Sequence and readiness

Four phases, with the task-level dependencies and focused proofs in [tasks.md](tasks.md):

1. **Contract and package proof.** Parse the simple source contract, generate a real standards-compliant package, and prove reference access and boundary refusals on fixtures. A proposed review stop protects the later mass migration.
2. **Content and installation.** Implement build/check/install, move all authored agent documents and supporting resources, and preserve the responsibilities and step-by-step procedures.
3. **Consumers and deletion.** Replace old references, active cloud commands, view/validation dependencies and CI declarations; then remove the old layout and aliases together.
4. **Cold-start qualification.** Check idempotence, safety and all local documentation checks; exercise a fresh agent reading the entry point, a role and a workstream from real installed packages; finish with the proposed independent review.

The source migration and reference rewrite must land together; do not introduce a prolonged hybrid where both authored formats are authoritative. Resolve the packaging choice and get the independent architecture critique before dispatch, since tests, generated views and live release instructions depend on this design. The new scope PR may remain draft while the owner decides; it is not a request to start implementation. Place a future implementation run in an owner-chosen release or integration branch after rechecking the live base, current writers and the active Release 14 instructions. Current priority is deliberately unchanged.

## Interfaces and handoff

**Consumes:** astrid-dev `main` planning snapshot `6d174521e6f3996349044e393d51b9fa06dbc625` (20 Nov 2026), the existing `skills/` tree, Python standard-library checks, documented Claude/Codex skill conventions, the current installation targets, and the continuing shared run contract. Before implementation, refresh current source, tests, consumers, release instructions and branch identity in [inputs.md](inputs.md#source-identities).

**Produces:** one canonical `agent/` source tree; documented frontmatter and heading rules; deterministic generated skill packages and an installation command; a rewritten source-to-output validation path; explicit, working references to shared rules and tools; an updated extension guide; and a migration/cold-start evidence record tied to the exact integrated commit. It must leave no runtime dependency on the retired `skills/` authoring layout.

**Handoff:** agents use `agent/start.md` in source or install `astrid-dev-start` and select an appropriate role. Roles link the relevant role-owned and shared workstreams. No run gains permissions from a skill name. The final PR identifies the actual candidate tree, CI result, observed discovery sessions and known unsupported environments. A later owner go is required for integration and any release-level rollout.

## Completion

An independent fresh agent, given only the repository and authoring guide, adds an ordinary workstream Markdown file, opts it into skill publication with `skill: true`, builds, checks and installs; the named `astrid-dev-<stem>` appears in a real supported agent environment and the agent can read the full referenced procedure and shared run contract. Removing the flag removes only the owned generated and installed skill while leaving its Markdown source.

The exact integrated tree passes `python3 scripts/astrid_dev.py check`, the focused migration tests and the existing documentation/unit inventory on CI. `skills build` is deterministic and idempotent; `skills check` detects stale output. Rebuilding and installing twice produces the same owned package set. A collision between two source basenames, an invalid `skill` value, missing dependency, path escape, broken anchor, stale output or a foreign occupied installation target causes a clear failure without damaging unrelated files.

All twenty primary documents have an old-to-new mapping and a reviewable rule-preservation audit. The nine shared skill identities and four role identities are verified; the main entry rename is explicit. Old authored `SKILL.md` files, legacy aliases and `sync.sh` are gone. No active references or runnable commands still depend on retired locations; immutable historical receipts remain accurate. The existing general views, check registry, golden oracles, public vision output and protected CI writeback are preserved unless a specifically enumerated contract decision authorizes an intentional change.

**Proof limits:** Valid packages and CI do not by themselves prove that all installed agents discover a skill; observe actual Claude/Codex sessions. A single fresh-agent trial does not close CA-005, whose ten-contributor evidence remains outstanding. Planning this project grants no execution, merge, publication or permission to alter existing running sessions.
