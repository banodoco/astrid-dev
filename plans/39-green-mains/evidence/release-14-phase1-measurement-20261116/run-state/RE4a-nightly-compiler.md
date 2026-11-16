# RE4a — Nightly integration has its locked TypeScript compiler

Manager: `/root`. Follow-up messages from that manager are part of this brief. Never use AskUserQuestion; send questions to the manager and continue unblocked work.

Route: N (`gpt-6-luna`, high), escalating to X on the first unexplained failure. This is a phase-1 wiring acceptance follow-up found by provisional G2, not a formal RS1 round or a phase-2 behavior change.

Repository: `banodoco/astrid-runtime`, local starting commit `ac9e6d2e7f6a0a6961d7a2d924040f61832925d1`, tree `3fff009d7cb8c46a1a1df21f3f541596b98480bd`, identical to merged plan head `4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce`.

Observed cause: Nightly run `43938386391`, attempt 1, job `133548961758` has three outer setup errors in `tests/test_operation_handle_integration.py`, all `FileNotFoundError: [Errno 2] No such file or directory: 'tsc'`. Nightly does not install the repository's locked TypeScript dependency tree. RE4's two named unit contract files pass locally (110 passed); this follow-up addresses the newly measured integration fixture.

Allowed scope: `.github/workflows/nightly.yml` to install Node 22 and run `npm ci` in `packages/typescript`, matching existing CI; `tests/test_operation_handle_integration.py` only to resolve the compiler from `packages/typescript/node_modules/.bin` using the established repository convention. Preserve all assertions, credentials/scope refusals, lost-ack/rebind/retry/dispose checks, markers, test IDs and parameterization. Preserve pin equality, full history, legacy diagnostic, SF3a summaries and artifacts. No product edits, no baseline rewrites, no quarantine changes, no Plan 38/55 test changes.

First inspect the fixture and confirm this cause from the saved log. Focused command, before and after: `bash scripts/worker-env/runtime-pytest.sh -q -m "" tests/test_operation_handle_integration.py`. Save complete stdout/stderr and exit status. Use the repository's existing environment. Do not run broad suites. If another cause blocks this exact file, record it and stop after one attempt; do not alter contracts to make it pass. Static workflow review and `git diff --check` are also required.

Work on local branch `p39/re4a-nightly-compiler`; add commits only. Do not publish, push, merge remotely or dispatch workflows. Return exact before/after summaries, commit/tree, complete diff and proof paths under `/workspace/scratch/cd53b069f320/p39-g2-evidence/runtime/re4a-nightly-compiler/`. Root will read the diff and commission independent review before publication.
