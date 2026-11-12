# Extending Astrid-dev

This guide covers the repository's standard-library check registry, generated views, and project record. Examples are from PM-3 (`20ccde8`, `3e39d01`) and PM-6a/6b (`45ea4e0`, `cae89a9`). Start from the real implementation and tests in [`checks.py`](../scripts/checks.py), [`views.py`](../scripts/views.py), and [`records.py`](../scripts/records.py).

## Add a check

A check is a `checks.Check` with a one-line id, trigger (`always` or `pr`), description, and callable accepting `checks.Context` and returning error strings. Implement the rule, then add its `Check(...)` to `checks.REGISTRY`. The smallest PM-3 registration diff added one entry, alongside the `_generated_views` rule:

```python
# In REGISTRY:
Check('generated-views', 'always', 'Validate registered generated views', _generated_views),
```

PM-3's corresponding test in [`test_views.py`](../scripts/test_views.py) checks the registry entry's id, trigger, description, and callable:

```python
registered = [entry for entry in checks.REGISTRY if entry.id == "generated-views"]
self.assertEqual(len(registered), 1)
self.assertEqual(registered[0].trigger, "always")
```

The same change tests a hand-edited target and verifies its diagnostic. Add focused pass and failure cases for a new rule, including that `python3 scripts/astrid_dev.py list` shows the id. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p "test_checks.py"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py list
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py check
```

Use the trigger that matches when the rule has enough context: `always` for repository-wide checks; `pr` for checks that need a base, event, or PR body. Return one concise string per problem; the command formats it with the check id.

## Add a generated view

A `views.View` names its sources and target, and has a render function taking the repository `Path` and returning text. Register it in `views.VIEWS`. For a generated region, set `region` to its marker name and keep the surrounding target text intact. PM-6b added the plan catalog as a `plan-catalog` region sourced from project plans and priority, with its renderer and registry entry in [`views.py`](../scripts/views.py); PM-3's focused tests in [`test_views.py`](../scripts/test_views.py) establish the smaller pattern: render a temporary view, `sync` it, verify it, then hand-edit it and assert a failure.

Add a test for the new view that checks its registered definition and source/target, its expected rendered content, `sync` idempotence, and stale or hand-edited output. If it owns a region, also verify text outside the markers is preserved. Generated targets are outputs: change their sources or renderer, then run `PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py sync`; do not edit generated content by hand. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p "test_views.py"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py sync
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py check
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

When adding a field, update `PROJECT_FIELDS`, `project_fields` validation, and every consumer that builds or checks a project record. In this branch those include `records.projects`, the plan-catalog renderer in `views.py`, the public feed in `export_public_vision.py`, the project template, and relevant completion checks. Add tests for a valid value and for missing, duplicate, empty, malformed, and body-only values; update fixtures only when the change requires it. Regenerate declared views with `sync`. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p "test_records.py"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p "test_views.py"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py sync
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py check
```

The project field list is a contract shared by the plan, catalog, feed, and checks. Keep its order and meaning consistent across those readers.
