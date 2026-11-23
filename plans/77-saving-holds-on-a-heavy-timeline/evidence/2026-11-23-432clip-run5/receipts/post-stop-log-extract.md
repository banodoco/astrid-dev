# Post-stop log extract

## Compiled build command and endpoint

`run5/receipts/build.sh:11–12`:

```text
 "${owned[@]}" PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci
 "${owned[@]}" ASTRID_RUNTIME_PYTHON="$PYTHON" ASTRID_RUNTIME_SOURCE_MANIFEST="$ADOPTED_SOURCE" PORT=2400 ASTRID_APP_LOOPBACK_ORIGIN=off node scripts/dev-local-workspace.mjs --data-root "$DATA" --build
```

`run5/receipts/build.log:45–46`:

```text
Astrid's engine isn't running. Start it first: astrid-runtime up --profile astrid
Details: runtime is unavailable at http://127.0.0.1:38175 (run astrid-runtime up --profile astrid): The operation was aborted due to timeout
```

`run5/receipts/discovery-safe.json:7–8`:

```text
  "endpoint": "http://127.0.0.1:38175",
  "door_endpoint": "http://127.0.0.1:17501"
```

`firstcut-432-reviewed-pins/app/scripts/dev-local-workspace.mjs:429–432,458–459,467–468,481–484,491–494`:

```text
    const response = await fetch(new URL('/v1/health', endpoint), {
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
      signal: AbortSignal.timeout(3000),
    });
    const handshakeResponse = await fetch(new URL('/v1/handshake', endpoint), {
      method: 'POST',
      signal: AbortSignal.timeout(3000),
    });
    const realmResponse = await fetch(new URL('/v1/realm', endpoint), {
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
      signal: AbortSignal.timeout(3000),
    });
  } catch (error) {
    if (allowStart && error.cause?.code === 'ECONNREFUSED') return NOT_RUNNING;
    const recovery = pinokioManaged ? 'Start Astrid in Pinokio' : `run ${runtimeUpCommand}`;
    return fail(ENGINE_STOPPED, `runtime is unavailable at ${endpoint.origin} (${recovery}): ${error instanceof Error ? error.message : String(error)}`);
```

The log does not identify which of the three requests raised the timeout. Each quoted request specifies 3,000 ms.

## Runtime and service logs

`run5/stack/home/.local/state/astrid-runtime/logs/runtime.log:19` contains the startup field `"endpoint": "http://127.0.0.1:38175"`; other fields are omitted. The 19-line file has no timestamped request, duration, lock or verification entries. `runtime-service.log` is empty. The service logs below have no per-entry timestamps; their lines cannot be assigned to 05:34:00–05:36:30 UTC or mapped individually to the five restarts in the health receipt.

`run5/stack/home/.local/state/astrid-runtime/logs/service-pack-host.log`, first five error/retry sequences:

```text
27 generic host CLI exiting after failure: error_type=FileNotFoundError
43 FileNotFoundError: [Errno 2] No such file or directory: '/root/codex/p77box/run5/stack/installed-data/runtime/discovery.json'
44 Service exited (1); retrying in 1s (exited).
47 generic host CLI exiting after failure: error_type=FileNotFoundError
63 FileNotFoundError: [Errno 2] No such file or directory: '/root/codex/p77box/run5/stack/installed-data/runtime/discovery.json'
64 Service exited (1); retrying in 2s (exited).
67 generic host CLI exiting after failure: error_type=FileNotFoundError
83 FileNotFoundError: [Errno 2] No such file or directory: '/root/codex/p77box/run5/stack/installed-data/runtime/discovery.json'
84 Service exited (1); retrying in 4s (exited).
87 generic host CLI exiting after failure: error_type=FileNotFoundError
103 FileNotFoundError: [Errno 2] No such file or directory: '/root/codex/p77box/run5/stack/installed-data/runtime/discovery.json'
104 Service exited (1); retrying in 8s (exited).
107 generic host CLI exiting after failure: error_type=FileNotFoundError
123 FileNotFoundError: [Errno 2] No such file or directory: '/root/codex/p77box/run5/stack/installed-data/runtime/discovery.json'
124 Service exited (1); retrying in 16s (exited).
```

`run5/stack/home/.local/state/astrid-runtime/logs/service-chat.log:1–11`:

```text
1 Astrid chat listening on 127.0.0.1:42805
2 Astrid chat listening on 127.0.0.1:43323
3 Service exited (0); retrying in 1s (readiness_timeout).
4 Astrid chat listening on 127.0.0.1:37815
5 Service exited (0); retrying in 2s (readiness_timeout).
6 Astrid chat listening on 127.0.0.1:39929
7 Service exited (0); retrying in 4s (readiness_timeout).
8 Astrid chat listening on 127.0.0.1:44355
9 Service exited (-15); retrying in 8s (readiness_timeout).
10 Astrid chat listening on 127.0.0.1:35863
11 Service exited (0); retrying in 16s (readiness_timeout).
```

## Adoption timestamps

`run5/receipts/adopt-start.txt:1`: `2026-11-23T05:20:21Z`; `adopt-end.txt:1`: `2026-11-23T05:33:48Z`. `run5/stack/direct-data/runtime/adopt-journal.json` records the following raw epoch values and states; UTC conversions are shown alongside:

```text
11–12 "at": 1795411225.4463637, "state": "planned"    05:20:25.446Z
15–16 "at": 1795411225.4481797, "state": "copying"    05:20:25.448Z
19–20 "at": 1795411229.230864,  "state": "copied"     05:20:29.230Z
23–24 "at": 1795411486.0692976, "state": "migrated"   05:24:46.069Z
27–28 "at": 1795411486.0723383, "state": "published"  05:24:46.072Z
31–32 "at": 1795411729.1026025, "state": "attached"   05:28:49.102Z
35–36 "at": 1795412028.7503994, "state": "failed"     05:33:48.750Z
```

`adopt-journal.json:8`: `"error": "transport_timeout: runtime request timed out"`.

`run5/receipts/adopt.json:2`: `"error": "realm materialized at /root/codex/p77box/run5/stack/direct-data/runtime/realms/0d6fd08f-8754-489c-8af9-276dcde43762; finish with astrid-runtime up after resolving: transport_timeout: runtime request timed out"`.

`adopt.stderr` and `section3.log` are empty. No final-verification start or end timestamp is named in the available journal or Runtime logs. `run5/receipts/readiness-end.txt:1` is `2026-11-23T05:34:24Z`.
