# Structural fix for the generation placement path (Release 13): reconciled design

Sources: an independent second opinion (read-only review of rehearsal `8cf3ada9`), the manager's evidence from tonight's paid runs, and real RunPod responses recorded tonight. The owner's constraint: this must work for MANY providers (not just RunPod) and MANY inference engines (not just ComfyUI). Extend existing abstractions; don't add layers.

## Root cause
Every boundary passes an untyped value (`dict[str, Any]`, a bare `bool`, a free `str`), and each consumer re-interprets it locally:
- Provider → Agent: a pod is read five different ways (`api.list_pods`, `lifecycle_graphql.get_pod`, a raw `httpx.get` in `read_exact_pod`, `sdk.get_pod` in `h3_release.py:399`, and a private REST client in `h3_release.py:323`), with two duplicate normalisers (`pod_fields.py` and lifecycle `discovery.py:196`).
- Check → caller: a check can say "no" without saying why or what to do next. `gate` is optional; `_canonical_installed` returned a bool; retry is decided by string allowlists (`target_selection.py:627-632`); retries use `timer(1)` everywhere.
- Host → Runtime: evidence shares a key that Runtime owns (`result["error"]`), so the readback check fails.
Tests fake at the dict level, so they encode the author's belief about the provider, not the provider.

## Ground truth is RECORDED responses, not the public OpenAPI schema
Recorded tonight, sanitised: `/home/user/wt/briefs/evidence/runpod-recorded/`:
- `rest-get-pod-default.json`: `GET /v1/pods/{id}` with no parameters. It HAS `networkVolumeId` and `imageName` and has NO `networkVolume` object.
- `rest-get-pod-include-network-volume.json`: `?includeNetworkVolume=true` adds the `networkVolume` object `{id, name, size, dataCenterId}`, and still has `networkVolumeId`.
- `rest-list-pods-include-network-volume.json`: the list form.
- `sdk-graphql-myself-pods.json`: the public SDK's pod query. It has `imageName` and NO `networkVolumeId` and no `networkVolume`. This is why the enriched `list_pods` record lacked `networkVolumeId`, which was tonight's failure 1.
RunPod's OpenAPI document (`/home/user/wt/briefs/evidence/rest-pod-schema.json`) OMITS `networkVolumeId` and `imageName`, which real responses return. So never validate fixtures against the OpenAPI file. Validate against the recorded key sets. In all four fixtures, values marked `<redacted>` or ALL_CAPS are placeholders.

## Move 1 — `MachineProvider` at the existing `generation.machine` extension point
New file `astrid/core/generation/machine_provider.py` (small):
```python
@dataclass(frozen=True)
class MachineRecord:
    provider: str; machine_id: str
    state: Literal["starting", "running", "stopped", "gone"]
    name: str | None = None; image: str | None = None
    storage_id: str | None = None; storage_mount: str | None = None
    gpu_count: int | None = None; gpu_label: str | None = None
    region: str | None = None; hourly_usd: float | None = None

class MachineProvider(Protocol):
    kind: str
    def read(self, machine_id: str) -> MachineRecord | None: ...   # None ONLY when proven absent (404)
    def find(self, request_name: str) -> list[MachineRecord]: ...
```
`create`, `delete` and `leases` come later; do not add them in slice 1. Every field except `machine_id` and `state` is optional, so a local or attached machine can implement the interface too.
- RunPod implementation: `astrid/packs/runpod/provider.py`. It maps each recorded RunPod shape (SDK GraphQL record, REST GET, REST list) to a `MachineRecord` in ONE function per shape. It reads the storage id from `networkVolumeId` or `networkVolume.id`, and refuses if both are present and disagree. It always sends `includeNetworkVolume=true` on REST reads.
- In production, unknown keys are ignored and missing known keys are None. In tests, a `strict=True` parse rejects any key outside the recorded key set for that shape.
- Later, `inspect_target_records` becomes a shared check of `MachineRecord` against a contract, so its gates are written once.

## Move 2 — one refusal type, extending `EngineError`
In `astrid/core/generation/engine_contracts.py` (`EngineError` is at ~16-28):
```python
Gate = Literal["identity", "state", "image", "storage", "hardware", "region",
               "rate", "lifetime", "inventory", "capacity", "install"]
class PlacementRefused(EngineError):
    code = "placement_refused"
    def __init__(self, message: str, *, gate: Gate, retryable: bool = False,
                 retry_after: float | None = None,
                 custody: Literal["none", "exact", "unknown"] = "unknown"): ...
def next_delay(attempt: int, retry_after: float | None) -> float  # max(retry_after, min(60, 5*2**(attempt-1))) + jitter
```
- `TargetObservationError` becomes a subclass with `gate` REQUIRED. RunPod gate names map as `GPU`→`hardware`, `volume`→`storage`, `datacenter`→`region`, `machine`→`hardware`, `status`→`state`, plus the ones that already match. Keep the old names readable in receipts through a mapping until consumers migrate.
- Retry policy reads only `retryable`, `retry_after` and `custody`, never provider reason strings.
- `Placement = Literal["local", "runpod"]` (`engine_contracts.py:10`, `:493`; `engine_runner.py:221-224`) becomes a string validated against the registered machine kinds. A second provider must not need to edit core.

## Move 3 — host-owned, fixed-vocabulary failure evidence
- The host writes its failure evidence under a key Runtime does not write (`result["host_failure"]`). `_verify_terminal_evidence_readback` (`generic_host.py` ~5830-5849) compares that key, and no longer `result.error`, which Runtime overwrites (`astrid-runtime` `runtime_protocol/store.py` ~6798). This needs no Runtime change.
- `failure_diagnostics.FACT_ALLOW["node_class"]` (~37-41) is a ComfyUI list inside shared code. Key it by engine id, so a second engine adds its own table.
- Ratchet test: the count of `runpod` and `comfy` matches under `astrid/core` may not rise.

## Explicitly NOT building
A second provider or engine; a generalised offers, consent or custody-journal interface; a VCR framework; a retry library; a new exception hierarchy beyond `PlacementRefused`; a Runtime protocol change; a rename sweep.
