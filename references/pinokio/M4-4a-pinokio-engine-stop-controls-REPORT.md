# M4-4a Pinokio engine/control report

## Result

**Blocked at the real Pinokio-engine boundary; no product change was made.**
The requested implementation cannot be honestly completed from the local
inputs. The candidate contains Astrid launcher descriptors and lifecycle code,
but this machine has no Pinokio kernel/action-engine source, package, executable,
or reachable daemon. Adding a guessed `kernel.api.process` wrapper, a disposable
command, or a direct `node pinokio/stop.js` fallback would violate the brief and
would not satisfy Q's accepted adapter.

This report makes no G3, M4-4a, publication, or release claim. The host watcher
owns `last.txt` and `exit`; neither was edited.

## Exact checkout custody

- Requested base: `c5b42701641889ecb916c60cde09a717f83d62ff`.
- Candidate source checkout: `work/coord/pinokio-integration`, clean at that
  exact base before the worktree was created.
- Created worktree: `work/coord/r1/M4-4a-pinokio-engine-stop-controls`.
- Branch: `r1/M4-4a-pinokio-engine-stop-controls`.
- Current head: `c5b42701641889ecb916c60cde09a717f83d62ff` (no commit added;
  worktree is clean).
- Canonical checkout preserved at
  `work/central/astrid-pinokio` `8379093196a521754261fd10fd66c2956781ab78`;
  its pre-existing `tests/launcher.test.mjs` modification remains the only
  central change.
- No clone, install, fetch, cleanup, central edit, push, hosted dispatch, or
  publication was performed.

## Local engine/API discovery

The local evidence distinguishes a real Pinokio engine from the launcher
descriptors, but does not make the engine available here:

1. The candidate has no `package.json`, lockfile, vendored Pinokio kernel, or
   Pinokio dependency. It is a launcher repository, not the Pinokio daemon.
2. `~/.pinokio/config.json` declares Pinokio home
   `historical configured Pinokio home`, but that directory is absent. The
   home-derived executable `historical configured Pinokio executable` is
   absent, `/Applications/Pinokio.app` is absent, and `pterm` is not on `PATH`.
3. `GET http://127.0.0.1:42000/pinokio/home` and
   `GET http://127.0.0.1:42000/pinokio/path/pterm` both failed with curl exit 7
   (connection refused). The configured peer
   `http://192.168.4.99:42000/` also refused all three probes attempted.
4. A local filesystem search found no `kernel/api/index.js`,
   `server/socket.js`, or Pinokio `rpc.js` source. Therefore the exact
   `kernel.api.process` request signature, transport envelope, task identifier,
   and settlement/readback API cannot be verified from local source or
   dependencies.
5. The checked-in research evidence
   `work/docs/pinokio/evidence/P09-agent-native-pinokio.md` identifies the real
   upstream boundary as Pinokio daemon WebSocket JSON-RPC, with script requests
   processed by `kernel.api.process`; `pterm` is only a client. The evidence is
   historical documentation, not a live engine or a locally available source
   dependency. The local review at
   `Documents/reigh-workspace/pinokio-pr3-repair-20261029/docs/INTERFACE.md:128-134`
   further records that `kernel.api.stop` is the direct-method stop path and
   that URI processing is queued rather than awaited in the inspected Pinokio
   8.1.1 source. The deployed engine/version is unknown.

## Existing immutable launcher bindings

No action bytes, arrays, provenance, or order were changed.

| Binding | Candidate value |
| --- | --- |
| launcher ref | `c5b42701641889ecb916c60cde09a717f83d62ff` |
| `pinokio/update.js` SHA-256 | `87d81aa58e1bc12f5f0c932d668b3e387c17e1754a066995c54eaf2972c1bd8b` |
| `pinokio/stop.js` SHA-256 | `f9d62e4e6a826fccd9791ee211dae933f46c8f99019e145abb3db3bf9595fd48` |
| `pinokio/start.js` SHA-256 | `442ff8fb73d65047bc4dd34de997bd36920efab16733aeb6ddd967afe291c037` |

The current source bindings are:

- `pinokio/update.js:11-18` preserves the fully-local route; backend update is
  the ordered `preflightStop -> launcher pull -> installer` sequence at
  `pinokio/update.js:20-22`.
- `pinokio/stop.js:3` exports the existing Stop action descriptor.
- `pinokio/lib.js:403-435` performs owned cleanup and, when the Start action is
  active, calls `await kernel.api.stop({ params: { uri } })`; refusal happens
  before lock admission and before the success output.

That last call is a Pinokio-engine call only when Pinokio invokes the descriptor
inside its own action engine. Loading either descriptor with Node is not an
engine execution and was not used as live evidence.

Selected installed app identity, mode, immutable action byte binding at
execution time, task settlement, and engine-owned cleanup could not be observed
because no installed app or engine was available. The existing code can read
`backend` versus `local` mode and owns its Runtime/controller cleanup, but that
does not establish the missing external invocation surface.

## Busy/unknown seams

No genuine seam was added or claimed.

The existing unit tests pass injected lifecycle/kernel doubles and verify refusal
ordering, identity preservation, and retry behavior. They do not invoke a real
Pinokio action engine. The Q adapter's current local `stop_controls` fixtures
execute disposable print/exit commands; Q's accepted readiness matrix explicitly
marks those commands as non-qualifying and requires `busy_stop` and
`unknown_stop` to bind to the immutable Pinokio Stop action.

Consequently there is no valid local evidence for either of these required
states:

- busy: the real selected app remains live while the immutable Stop action
  refuses before signal/tree cleanup, with unchanged process/listener/health and
  state identity;
- unknown: a real controller transport loss or bounded Stop/down timeout
  refuses before cleanup, then the same session is restored and stopped through
  the same immutable Stop action.

## Checks

From the isolated candidate worktree:

```text
node --test tests/lifecycle.test.mjs tests/launcher.test.mjs tests/environment.test.mjs tests/process.test.mjs
1..121
# pass 121
# fail 0
```

This is focused source/test evidence only; it is not hosted lifecycle evidence
and does not prove a live action-engine invocation.

The final candidate and central custody checks were clean/preserved as described
above. No source/test commit exists because there is no safe implementation to
commit without the missing engine interface.

## Concrete NEEDS to resume implementation

The owner/integrator must provide all of the following before a Pinokio-owned
implementation can be added:

1. A real Pinokio daemon/desktop fixture or hosted runner with an installed
   selected app, a valid `PINOKIO_HOME`, and the deployed Pinokio version.
2. The exact supported engine contract: either the in-process `kernel.api`
   object passed to an action, or the daemon WebSocket JSON-RPC method and
   envelope for `kernel.api.process`, `kernel.api.stop`, task IDs, and awaited
   settlement. The contract must state whether URI processing is queued or
   awaited and how a caller reads terminal task state.
3. A stable product-owned command/API whose input is the selected app identity,
   mode, action name (`update` or `stop`), immutable action bytes/ref/SHA-256,
   and owned-cleanup policy. It must construct/verify the action before the
   engine call, invoke it through the real engine, await settlement, and return
   a structured terminal result. It must not execute the descriptor with Node,
   call the installer directly, or use a disposable refusal command.
4. An engine-backed busy fixture and an engine-backed unknown/timeout fixture
   that both invoke the same immutable `pinokio/stop.js`, preserve the selected
   app/session identity, prove zero mutation and unchanged process/listener/
   health snapshots on refusal, then restore and retry Stop successfully.
5. Q integration that binds its `stop_controls.busy_stop` and
   `stop_controls.unknown_stop` argv to that engine-backed command, plus the
   three authentic hosted rows (`macos-14`, `ubuntu-24.04`, `windows-2022`) and
   the aggregate checker. Native Pinokio Stop/Quit refusal-veto behavior remains
   a separate hosted/deployed-version NEEDS; the local historical review says
   Pinokio 8.1.1 swallowed hook errors before forced cleanup and Quit bypassed
   the hook.

## Exit

`1` — implementation blocked by absent real Pinokio action engine/API. No
fabricated behavior, G3/M4-4a/release claim, or hosted evidence is reported.
