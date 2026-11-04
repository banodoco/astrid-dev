# B-owned Pinokio custody provider report

Status: **source-backed, fail-closed implementation delivered.** This makes no
live Pinokio engine, hosted evidence, M4-4a, M4-6, G3, qualification, or
release claim.

## Repository identity and changed paths

- Agent worktree: `queue/running/M4-6-native-verifier/astrid-agent`
- Branch: `r1/M4-6-native-verifier`
- Required observed Q base: `64e18fb6b6812e04732f0bedd75e6e0f251ee6a9`
- Separate direct-observer commit already present before this work:
  `4e60a4b249ddd4a4d2478ad3637127158a94aefc`
- B Pinokio commit/head:
  `98fc9af5752216ba298e34daa094435f8117a3b6`
- Pinokio commit parent: `4e60a4b249ddd4a4d2478ad3637127158a94aefc`

The commit includes only:

- `scripts/m4_6_pinokio_custody_provider.py`
- `tests/test_m4_6_pinokio_custody_provider.py`

Task-local coordination output is historical `Q_COORDINATION.md` task-local note (not copied). No
direct-observer/provider path, Q adapter, shared driver, checker, workflow, or
host watcher file (`last.txt`, `exit`, `pid`, `started`) was edited.

## Pinned source and settlement contract

The immutable research basis is
`queue/running/M4-4a-pinokio-source-contract/PINOKIO-ENGINE-CONTRACT.md`:

- source custody/checksums: lines 9–25;
- URI dispatch/action selection: lines 53–75; derived wrapper seam: lines
  172–241;
- acceptance is not settlement: lines 82–106;
- errors/refusal/readback/transport: lines 128–156; and
- action byte identity/no direct Node: lines 158–170.

Exact retained pins are `pinokiocomputer/pterm@5be43718701c448b43daf0ce51d8935f170065bb`
and `pinokiocomputer/pinokiod@add4a674ad1ba95bb62ec427fce519fe5bf0e9bf`.
The evidence specifically supports unawaited socket processing
(`server/socket.js:271-307`), queue-only `Queued` events
(`kernel/api/index.js:1678-1787,2032-2035`), ordered step/result/stop and
disconnect events (`kernel/api/index.js:1387-1434,1525-1531,1574-1618,641-664`),
errors/refusal controls (`kernel/api/index.js:1884-1910,1942-1977,1437-1468,1621-1645`),
and pterm's unsafe zero-exit/disconnect behavior (`pterm/script.js:133-166,257-273`).

`PinokioActionGraph` binds bounded, resolved regular bytes for
`pinokio/start.js`, `pinokio/stop.js`, `pinokio/update.js`, and each statically
resolvable relative helper. It rejects symlinks, escape, dynamic imports,
missing files, and changed graph bytes. `PinokioSelectedApp` binds the parsed
`pinokio://host:port/api/<id>` ref, selected app ID/root, and status path.
`PreparedPinokioRequest` supplies only daemon-shaped `{uri,id,action:"run",input}`
data; it has no Node, installer, shell, socket, daemon, or action invocation.

`PinokioRequestSettlement` keeps acceptance and settlement distinct:

1. `record_sent()` records queued acceptance only for the fixed ID.
2. `error` becomes error; blocked/cancelled `launch.requirements.control`
   becomes refused; foreign/malformed packets, timeout, disconnect, and any
   client exit including zero become unknown. Even `result` then `event:stop`
   is `unknown/missing-engine-task-readback`, because pinned source exposes no
   general terminal task readback.

There is deliberately no success-producing path, receipt constructor, or
authorization result.

## Distinct Pinokio custody

`PINOKIO_CUSTODY_PROVIDER` accepts only the six fixed `pinokio-backend-*` and
`pinokio-fully-local-*` slots. Direct slots are rejected and no native
login-service fallback exists. Its Q-shaped owner exposes the required owner
method names, but every live operation refuses before mutation because no
authenticated selected-app, engine/action/session, controller/descendant
incarnations, or independent postconditions exist.

`PinokioCustodyObserver` maintains a private bounded ledger and imports
`scripts.m4_6_process_observer` rather than duplicating OS observation. The
current B observer is bounded polling and therefore refuses authorization; an
absent observer, gap, source failure, sequence gap, or overflow remains a hard
refusal. Caller-provided controller/descendant census is explicitly marked
non-authoritative and also refuses.

## Checks

Final-head focused check:

`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_m4_6_pinokio_custody_provider.py tests/test_m4_6_process_observer.py tests/test_m4_6_platform_session_provider.py tests/test_native_service_adapter.py -k 'pinokio or m4_6'`

Result: `25 passed, 136 deselected in 0.47s`. The pre-existing sandbox guard
warned that `ps` inspection is not permitted; it was not treated as success.

Also passed:

- `ruff check --no-cache scripts/m4_6_pinokio_custody_provider.py tests/test_m4_6_pinokio_custody_provider.py`
- `ruff format --check --no-cache scripts/m4_6_pinokio_custody_provider.py tests/test_m4_6_pinokio_custody_provider.py`
- `git diff --check`

The tests cover descriptor/helper drift, app mismatch, source-shaped request
data, acceptance versus terminal settlement, errors/refusal/disconnect/timeout/
foreign packet/missing readback/zero exit, direct-versus-Pinokio ownership, and
absent or imported-B-observer gap refusal.

## Q coordination and remaining live evidence

The review is in historical `Q_COORDINATION.md` task-local note (not copied). Q's five-method
contract is revision `58ae94b637fc5f6497c9e4728450c9f6e904129d`, but its
handoff remains pending root/Q+B review/freeze. The B worktree still lacks
those newer Q dataclasses. Q's provisional
`scripts.m4_6_trusted_launcher.TrustedCollectorContext` was reviewed but not
imported: it has no production minting backend and explicitly raises `NEEDS`.
No context, token, environment claim, JSON, fixture, or private channel was
treated as authority.

Live admission remains closed pending all of:

1. production-minted collector/workflow/attempt authentication and frozen Q
   integration;
2. a real selected app, immutable action graph, engine/action/session identity,
   and authenticated terminal task readback;
3. independent gap-free controller/descendant observation and post-action
   custody evidence;
4. independently verified action-specific process/app/data postconditions and
   removal/cleanup plan; and
5. root-owned hosted artifact provenance and checker-side reauthentication.

No daemon/action invocation, install, clone, fetch, hosted dispatch,
credentials, central edit, or release claim was performed.
