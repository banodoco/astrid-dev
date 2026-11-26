# P95-PK — Package the templates and guidance so an installed Otto finds them

**Source tasks:** [`tasks.md`](../tasks.md) — a gap found by P95-12 and recorded here: OT-12 and OT-17 ship `templates/` and `guidance/` as sibling folders of the `otto` package, which an installed wheel does not carry. Needed before OT-22 and OT-23.
**Route:** X (ChatGPT mode: Extra High; [run contract](../../../agent/shared/run-contract.md#chatgpt-session-modes))
**Estimate:** about 2 hours
**Outcome:** After `pip install` of Otto from a git tag into a clean virtual environment, the template manifests, the common pack and the guidance are found by the same code paths that find them in a source checkout, so `otto check` and `otto skills build` behave identically in both.
**Dependencies:** OT-12 and OT-17 merged. Otto `main` at `d67cacfb49947464cc0f441a3be3390f00b0a562`, named in the orchestrator's DECISION.
**May touch (in `banodoco/otto` only):** `pyproject.toml` (package data), the resource-location code in `otto/templates.py` (`PACKAGE_ROOT` and where it is used), and any moves of `templates/` and `guidance/` into the package that the chosen design needs, plus `tests/test_packaging.py` (new) and the test fixtures' references to those locations; nothing else.
**Must not touch:** `docs/contract.md` (if its paths must change, post BLOCKED; the orchestrator amends it), `tests/fixtures/`, other modules, anything in astrid-dev.
**Proof:** the orchestrator's: all Otto tests pass; in a clean venv, `pip install "banodoco-otto @ git+https://github.com/banodoco/otto@<sha>"` then a script that builds a temporary workspace and checks that the standard and loop templates and the guidance are found and `otto skills build` for namespace `otto-` and root `guidance` of the installed copy equals the build from a source checkout (same tree hash). Selectors for READY-PROOF: `tests`.
**PR destination:** `banodoco/otto` `p95/ot-pk` → `main`
**Authority:** [run board](../run.md#authority)

One packet starts **one fresh ChatGPT session**. The session opens task PRs and ends with `READY-PROOF`, **never merging or editing `tasks.md`**. The orchestrator runs the proof and reviews; the orchestrator integrates.

## Step 1 (post before writing)

Post a STATUS with two or three designs for where the assets live (for example, move them under the package and keep a repo-root symlink or alias for the paths the contract names; or resource roots via `importlib.resources`; or setuptools data files), the one you recommend and why, every code path and test it touches, and what changes in the contract's paths, if anything. The orchestrator rules within 45 minutes. Smallest design that makes a wheel work and keeps source-checkout behaviour unchanged.

## Contract

- Standard library and setuptools only. No change to any behaviour except where the assets are found. If a design needs the contract's paths to move, say so in Step 1 and wait for my ruling.
