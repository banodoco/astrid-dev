# Extending Astrid-dev

This guide covers the repository's standard-library check registry, generated views, project record, and Markdown-first agent documents. Examples are from PM-3 (`20ccde8`, `3e39d01`) and PM-6a/6b (`45ea4e0`, `cae89a9`). Start from the real implementation and tests in [`checks.py`](../scripts/checks.py), [`views.py`](../scripts/views.py), and [`records.py`](../scripts/records.py).

## Add a check

A check is a `checks.Check` with a one-line id, trigger (`always` or `pr`), description, and callable accepting `checks.Context` and returning error strings. Implement the rule, then add its `Check(...)` to `checks.REGISTRY`. The smallest PM-3 registration diff added one entry, alongside the `_generated_views` rule:

```python
# In REGISTRY:
Check('generated-views', 'pr', 'Validate generated views that a pull request changes', _generated_views),
```

PM-3's corresponding test in [`test_views.py`](../scripts/test_views.py) checks the registry entry's id, trigger, description, and callable:

```python
registered = [entry for entry in checks.REGISTRY if entry.id == "generated-views"]
self.assertEqual(len(registered), 1)
self.assertEqual(registered[0].trigger, "pr")
```

Put the tests for a new check in [`test_checks.py`](../scripts/test_checks.py): a registration test like the one above, one case where the rule passes and one where it fails (build a small temporary tree for each and call the registered rule with `checks.Context(root=tree)`; `ProjectCatalogContractTests` in `test_checks.py` is a model), and `python3 scripts/astrid_dev.py list` must show the id. Start the rule with `if not _catalog_ready(context): return []` when it reads plans, so it stays quiet while the catalog itself is broken (a rule that only reads Markdown files needs no gate). Run:

```sh
python3 -m unittest discover -s scripts -p "test_checks.py"
python3 scripts/astrid_dev.py list
python3 scripts/astrid_dev.py check
python3 scripts/astrid_dev.py check --base <base commit> --body-file /dev/null
python3 -m unittest discover -s scripts -p "test_golden.py"
```

The oracle `scripts/fixtures/golden.txt` pins what the check list says about every fixture tree. A new check runs on all of them: `git diff --stat <base commit> -- scripts/fixtures/golden.txt` must print nothing unless your card lists the lines it changes.

Registering a check changes a generated page: `docs/checks.md` lists every check with its description. Edit the check's registry entry and description, not the page. Run `python3 scripts/astrid_dev.py views generate` and commit the page it writes with your change; `main` also refreshes the page after merge. `views generate` reports the targets it updates, and a generated file in your PR must equal that output. The description is copied into that page word for word, so do not put in it text that your own rule forbids. If your rule lists tracked files, take the list from `git ls-files` run in the repository root, and make it return no error rather than raise when the tree has no `.git`: some tests copy the repository without it. A rule over Markdown files walks `root.rglob("*.md")` and skips `.git`, as `markdown-links` and `link-anchors` do, because the oracle's fixture trees hold untracked files. Use the trigger that matches when the rule has enough context: `always` for repository-wide checks; `pr` for checks that need a base, event, or PR body. Return one concise string per problem; the command formats it with the check id.

## Add a generated view

A `views.View` names its sources and target, and has a render function taking the repository `Path` and returning text. Register it in `views.VIEWS`. For a generated region, set `region` to its marker name and keep the surrounding target text intact. PM-6b added the plan catalog as a `plan-catalog` region sourced from project plans and priority, with its renderer and registry entry in [`views.py`](../scripts/views.py); PM-3's focused tests in [`test_views.py`](../scripts/test_views.py) establish the smaller pattern: render a temporary view, generate it, verify it, then hand-edit it and assert a failure.

A **shared block** is a rule written once and copied to every place that needs it. Wrap the rule in its owner file between `<!-- block-source:NAME:start -->` and `<!-- block-source:NAME:end -->` (exactly one owner per name, hand-written, never a target). Put an empty `<!-- block:NAME:start -->` / `<!-- block:NAME:end -->` pair, each on its own line, in any Markdown file that needs the rule at the point of action, and run `views generate`: `views.block_views` scans the tracked Markdown files and registers one view per copy, filling it with the owner's text, links rebased for the copy's directory, and a closing "From ..." link to the owner's heading. A copy is generated output like any other region: edit the owner. A copy with no owner, two owners, a copy inside its owner file, or unpaired markers is an error that names the file. Copies are allowed only under `agent/`, `templates/` and `docs/`, never `docs/ledger/` or `docs/handoffs/`. Markers inside code fences are ignored. `check` and `views generate` report these errors instead of failing at import. Tests are in `SharedBlockTests` in [`test_views.py`](../scripts/test_views.py).

A view is either a whole file (`region` unset: the render function returns the entire target) or one region between markers. Add a test for the new view in `test_views.py` that checks its registered definition and source/target, its expected rendered content, generation idempotence, and stale or hand-edited output; a temporary tree for the test must start without the target file, or generation has nothing to write. If it owns a region, also verify text outside the markers is preserved. Generated targets are outputs: change their sources or renderer, not the generated content; the target refreshes itself on `main` after merge. Run `views generate` locally to see what it writes; a generated file in your PR must equal that output. Run:

```sh
python3 -m unittest discover -s scripts -p "test_views.py"
python3 scripts/astrid_dev.py views generate
python3 scripts/astrid_dev.py check
```

## Add a project field

Project facts are bold, single-line fields in the `plan.md` header, before its first `## ` heading. PM-6a declared the required field tuple and pinned the contract; PM-6b implemented the reader and moved consumers. The real test in [`test_records.py`](../scripts/test_records.py) checks the declared fields and that header values are read while same-named body fields are ignored:

```python
PROJECT_FIELDS = ("Project", "Goal", "Status", "Owner", "Estimate", "Waiting on")

# In test_six_fields_preserve_values_and_ignore_body_fields:
self.assertEqual(records.PROJECT_FIELDS, self.FIELDS)
self.assertEqual(records.project_fields(text), dict(zip(self.FIELDS,
                 ("Catalog name", "Build **one** thing", "queued", "Ada", "TBD", "—"))))
```

When adding a field, update `PROJECT_FIELDS`, `project_fields` validation, and every consumer that builds or checks a project record. Those include `records.projects`, the plan-catalog renderer in `views.py`, the public feed in `export_public_vision.py`, the project template, and relevant completion checks. Add tests for a valid value and for missing, duplicate, empty, malformed, and body-only values; update fixtures only when the change requires it. Regenerate declared views with `views generate`. Run:

```sh
python3 -m unittest discover -s scripts -p "test_records.py"
python3 -m unittest discover -s scripts -p "test_views.py"
python3 scripts/astrid_dev.py views generate
python3 scripts/astrid_dev.py check
```

The project field list is a contract shared by the plan, catalog, feed, and checks. Keep its order and meaning consistent across those readers.

## Add or edit a workstream

Write the instruction once as a regular Markdown document in `agent/`. The [workstream authoring convention](../agent/README.md) describes the shared purpose; the steps below are the Markdown-first authoring procedure. The source reader is `scripts/agent_documents.py`, backed by reusable [Markdown structure checks](../scripts/document_structure.py). The former dual-format parser is [`workstreams.py`](../scripts/workstreams.py) (migration history, not the new authoring format).

**1. Choose the document's home.**

- A continuing role belongs in `agent/roles/<role>.md`; use the ordered `## Responsibility`, `## Authority`, `## Responsibilities`, and `## Handoff` sections.
- A procedure owned by a role belongs in `agent/roles/<role>/<name>.md`; an independently callable shared procedure belongs in `agent/shared/workstreams/<name>.md`. Both use the ordered `## When to use`, `## Outcome`, `## Inputs`, `## Procedure`, and `## Completion` sections.
- A guide or shared reference belongs in the appropriate `agent/` reference location, such as `agent/guides/` or `agent/shared/`. It does not need the role or workstream headings.

Reuse an existing instruction where possible. Give each required section real content, state authority and boundaries in the relevant document, and keep the actual steps in the procedure rather than duplicating them in a five-field preamble. A role's linked summary is not another source of the procedure.

**2. Write the Markdown and choose whether to publish a skill.** Every document starts with frontmatter containing a `description:`: a nonempty, plain-text sentence of at most 240 characters, ending in `.`, `!` or `?`. The first nonblank body line is a nonempty `# Title`. Add the literal `skill: true` only if the document should be independently discoverable by an agent; omission or `skill: false` keeps it an ordinary document. Do not add a `name:` field.

For example, to try the process in a disposable checkout, create `agent/shared/workstreams/record-checkout-identity.md` with this entire content (illustrative only; do not commit an example skill just to exercise the guide):

~~~markdown
---
description: Record the exact revision and working-tree state of a checkout before reviewing it.
skill: true
---

# Record checkout identity

## When to use

Before examining a candidate in an already authorized read-only review.

## Outcome

A record identifying the checkout's exact commit and whether its working tree is clean.

## Inputs

The repository checkout and the review assignment.

## Procedure

1. From the checkout root, read the commit with `git rev-parse HEAD`.
2. Read the working-tree state with `git status --short`.
3. Report both observations and any error without changing the checkout.

## Completion

The report names the commit, observed working-tree state and any limit; it does not claim tests passed or authorize a merge.
~~~

The opted-in filename stem must be lowercase kebab-case and unique across all opted-in documents. Here the generated name is `astrid-dev-record-checkout-identity`, irrespective of the folder. A duplicate name fails rather than silently selecting a source. There is no hand-maintained package registry and no separately authored `SKILL.md`. Keep role-specific procedures linked from their role by default; add a navigation link for a new shared workstream when it is accepted for general use. Opting in changes discovery only: the active assignment and owner still govern authority.

**3. Regenerate declared views, build and check.** From the repository root, run:

~~~sh
python3 scripts/astrid_dev.py views generate
python3 scripts/astrid_dev.py skills build
python3 scripts/astrid_dev.py skills check
python3 scripts/astrid_dev.py check
~~~

`views generate` updates declared Markdown views, not installed skills. `skills build` creates the ignored `.generated/skills/` packages. For the example, inspect `.generated/skills/astrid-dev-record-checkout-identity/SKILL.md`: the generated frontmatter supplies the skill name and description, and the body carries the authored instructions with accessible references. Never edit or commit generated skill output. On a refusal or stale-output report, fix the Markdown source or its references, rebuild and check again. The checks establish structure and package consistency, not whether an instruction is wise or its actor authorized.

**4. Dry-run and install into a safe destination.** To exercise the generated packages without changing your real agent catalog, use a fresh temporary directory. Run these commands from the same checkout after a successful build and check:

~~~sh
demo=$(mktemp -d) &&
  python3 scripts/astrid_dev.py skills install --dry-run --destination "$demo" &&
  python3 scripts/astrid_dev.py skills install --destination "$demo"
~~~

The dry run requires current packages and displays intended link changes. The real install builds and links the repository's owned packages; foreign entries occupying an intended name are refused, not overwritten. The destination must already exist as a real directory, and `--destination` may be repeated. Inspect the resulting package directory symlinks in the temporary directory; remove that temporary directory when finished. An installed package must remain a directory symlink into this checkout so its references remain accessible; copying a generated file elsewhere is not the supported installation. If you tried the illustrative source, discard it in the disposable checkout and rebuild to remove its generated package.

Only install into real Claude, Codex or other supported agent skill roots when the owner authorizes that installation. With no explicit destination, the installer uses existing supported skill roots. Use an explicit authorized destination and review the dry run first; verify the agent can discover the expected skill and read its references. Building or installing packages never grants execution, spending, merge or publishing authority.

## Compose existing delivery relationships

Plan 72's [project-delivery reader](../scripts/project_delivery.py) assembles a
**read-only** typed snapshot of canonical Markdown records. The authored records
are still the sources of truth: aspirations in the subject pages, gap metadata,
project headers, release briefs and *frozen* release issue lists. The
[relationship types](../scripts/relationships.py) own only a small shared
mechanism (record identity, typed endpoints, roles, provenance, deterministic
traversal and structural refusals), not domain interpretation or a new registry.

**To extend an existing delivery composition:**

1. Find the owning reader first: [vision_subject.py](../scripts/vision_subject.py),
   [gap_relationships.py](../scripts/gap_relationships.py),
   [project_contract.py](../scripts/project_contract.py) or
   [records.py](../scripts/records.py). Do not duplicate its parsing rules.
2. Define a typed link only when both ends have canonical stable identities,
   a source declaration and a meaningful, provable direction. The relationship
   module's kind/endpoint rules are deliberately small.
3. Add the source adapter to [project_delivery.py](../scripts/project_delivery.py)
   or the existing appropriate reader, with positive, missing, contradictory
   and duplicate fixtures in [test_project_delivery.py](../scripts/test_project_delivery.py).
4. Prove existing public feeds and generated pages retain their shapes and
   classification. New generated views belong in [views.py](../scripts/views.py);
   repository checks belong in [checks.py](../scripts/checks.py), not a new
   pipeline-specific validation framework.

For example, a `project:53` **addresses** the `gap:CA-003` it names in its own
plan, and a release **includes** that project only if the release brief
lists it. A project's completion never closes its gap.

The registered `project-delivery` check runs on every repository
`python3 scripts/astrid_dev.py check`, using the same delivery reader. Try the
standalone read-only queries on a qualified checkout:

~~~sh
python3 scripts/project_delivery.py check
python3 scripts/project_delivery.py goal principle:open-by-design/open-decisions-and-working-knowledge
python3 scripts/project_delivery.py issue 578
~~~

- `check` prints the number of validated records and typed relationships on
  success; an invalid authored relationship is an error, not silently dropped.
- `goal` prints one line per supported goal → gap → project → release path,
  with four typed IDs and the primary/supporting role in parentheses after
  the gap and the project. The query takes the aspiration ID without the
  `goal:` prefix; the printed goal ID includes it.
- `issue` prints recorded frozen release membership. Issue 578 appears in
  the [frozen Release 14 issue ledger](../releases/14.md#issues), so the
  output includes `issue:578 -> release:14`. A GitHub label or a non-frozen
  issue listing alone does not establish membership; even frozen membership
  does not prove the issue shipped or was fixed.

For goal and issue queries, empty output means *no supported recorded
relationship*, not proof that the goal was achieved or that the issue was
irrelevant or unfixed. No GitHub API access is needed or performed. A second
pipeline, scheduler, generic DSL, approvals system or graph database is
explicitly **not** part of this layer. This reader's domain scope must be
reviewed when the underlying authoring contract changes.
