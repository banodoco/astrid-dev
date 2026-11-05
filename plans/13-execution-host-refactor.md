# 13 — Execution host refactor

**Draft scope — not yet fully specified.** Current status and owner are in the [README queue](../README.md).

## Goal

Make Astrid's execution host understandable and maintainable by separating its responsibilities into cohesive modules while preserving existing execution behavior.

## Starting evidence

The likely oversized Python file is [`astrid/core/execution/generic_host.py`](https://github.com/banodoco/astrid-agent/blob/pre-main/astrid/core/execution/generic_host.py). GitHub inspection on 2026-11-05 counted **17,067 lines on `pre-main`** (blob `b0ea83326115ec172a79260d657be7dd01c3c4a1`) and **14,453 on `main`** (blob `da61b21aed220a4c35c27d62baca19eeef1b09c4`). This is the likely match for the remembered roughly 18,000-line file; recheck the chosen starting commit.

[Agent PR #109](https://github.com/banodoco/astrid-agent/pull/109) changes this file for sandbox process control; it is not itself the decomposition project. Preserve applicable sandbox work and other execution changes when choosing the base.

The inspected main snapshot identifies handwritten orchestration rather than generated client code: Runtime protocol access, capability discovery, task execution/settlement, local preparation, persistent supervision, and process handoff live together. The generated protocol client is separate in `astrid_runtime_client/generated.py`. Use these as candidate boundaries, then check their coupling on the actual working base.

## Intended work and focused proof

- Map the file's responsibilities, callers, shared state, and existing focused tests; choose natural extraction boundaries.
- Extract one cohesive responsibility at a time, preserving public entry points and avoiding a replacement execution framework.
- Characterize affected behavior before extraction and rerun those exact checks afterwards. Explicitly cover any touched lifecycle, cancellation, process ownership, and result-handling boundaries.
- Keep semantic bug fixes separate and named when required; moving code alone must not silently change execution contracts.

## Completion

The agreed responsibilities have clear owners and module boundaries, existing callers still work, and focused before/after evidence demonstrates preserved behavior. Success is simpler code and fewer coupled responsibilities, not an arbitrary line-count target.

## Before implementation

Confirm current repositories, base branches and SHAs, existing work to preserve, verified predecessor inputs, a fresh candidate branch, and the intended `pre-main` destination. Break the work into bounded tasks with difficulty levels and explicit focused checks after inspecting those inputs. Links to other projects provide context, not blanket scheduling gates. No broad suites or automatic test discovery.
