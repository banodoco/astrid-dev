# Pinokio immutable stop/update engine and refusal seams

Implement the Pinokio-owned stable engine/control surface needed by B/Q's M4
journeys: invoke the selected installed app's immutable `pinokio/update.js`
and `pinokio/stop.js` through the real Pinokio action engine, await task
settlement, preserve backend versus fully-local ownership, and expose genuine
busy and unknown-stop preparation/restoration seams. The accepted Q adapter
`pinokio_platform_adapter.py` requires actual immutable Stop action execution;
its disposable print/exit commands and direct `node pinokio/stop.js` are
explicitly insufficient.

Reuse the clean local Pinokio candidate
`work/coord/pinokio-integration` at
`c5b42701641889ecb916c60cde09a717f83d62ff` and its existing object store to
create branch/worktree `r1/M4-4a-pinokio-engine-stop-controls`. Preserve the
canonical dirty checkout `work/central/astrid-pinokio` at `8379093` and its
`tests/launcher.test.mjs` custody. No clone, install, fetch, cleanup, central
edit, push, hosted dispatch, or publication.

First identify the real Pinokio kernel/action-engine API available in the
existing local source/dependencies. Do not invent an engine, use test-only
fakes as live evidence, execute a shell command that merely loads the descriptor,
or change old action arrays/provenance/order. Add a stable product-owned API
or command only if it can call the actual engine and bind immutable action
bytes/ref/hash, selected app identity, mode and owned cleanup. Busy and unknown
seams must establish real states and invoke the immutable Stop action while
proving zero mutation and unchanged process/listener/health identity. If the
actual action engine/API is absent from local inputs, report precise evidence
and a concrete interface NEEDS without fabricating behavior.

Commit only Pinokio-owned source/tests, run available focused tests using
existing dependencies, and report exact base/head, command/API, immutable
bindings, seams, checks and remaining hosted NEEDS in `REPORT.md`; exit 0/1.
No G3/M4-4a/release claim. Host watcher owns `last.txt` and `exit`.
