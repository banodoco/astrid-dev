# Release 12 host attachment reproduction

Agent `6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7` with Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641` failed `machines setup` before a pod claim with `astrid.pack_host_attach_rejected`, `live.check_raised=ApiError`. Runtime doctor reported healthy; this does not establish attach readiness. No pod was rented.

The [test patch](reproducer.patch) is a CPU-only reproduction against the Agent SHA above. It uses synthetic fixture credentials and models the Runtime's owner-only executor observation as a 403 for the worker. Apply it to a disposable checkout and run:

```sh
PYTHONPATH=. python -m pytest tests/sdk/test_host_recovery.py::test_attach_does_not_require_worker_to_observe_executor -q --tb=short
```

On 11 Nov, the test failed in 2.57 seconds: the observed attach diagnostic was `live.check_raised=ApiError` and the test caught an attempt to retire the healthy resident. This fake is a reproduction of the behavior, not a real-server authorization proof. Runtime source requires `admin` and actor `owner` for executor observation; the worker handshake uses a scoped worker credential. The ordinary launcher credential is scoped too, not an owner credential. Independent advice recommends a narrowly authorized observer tied to the same Runtime while retaining worker handshake and all identity/readiness checks; the supported owner-observer lifecycle and repair ownership remain open in [R12-F2](../../tasks.md). Never grant the worker admin or bypass custody checks.
