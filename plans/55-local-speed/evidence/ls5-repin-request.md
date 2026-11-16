# LS-5 exact re-pin request

**State:** proposed, not approved. No dependency pin has been changed. This request is for the Plan 55 integration candidate only.

## Proposed source change

| Source | Current published Release 13 pin | Proposed Plan 55 integration pin |
| --- | --- | --- |
| VibeComfy | `dba38f8644c46f652376f2cd5112ea161e40f09b` | `7fde33e2523281f840121b93a8a865a7f5d847de` |

The proposed source includes [VibeComfy #167](https://github.com/banodoco/VibeComfy/pull/167) and [#169](https://github.com/banodoco/VibeComfy/pull/169). Its tree is `eabc2a3e07cef763d463b4a81325b48a0787d56d`, matching the independently checked local candidate `7340fd1b6d197b6319c5e446142ae41474259068`. The cumulative source diff from the published pin is five files: `vibecomfy/runtime/run.py`, `vibecomfy/runtime/session.py`, `vibecomfy/runtime/transport.py`, `tests/test_runtime_transport.py`, and `tests/_runtime_session_helpers.py`. Templates and dependency declarations are unchanged. Focused evidence is in [tests/README.md](tests/README.md).

## Exact Agent surfaces

Use the existing `scripts/vibecomfy_pin.py <revision> --checkout <checkout-at-that-revision>` generator, after approval. It updates the two source manifests and their existing digest chain:

- `astrid/packs/runpod/pins.json`
- `astrid/packs/vibecomfy/pins.json`
- `astrid/packs/runpod/recipe.linux-cu130.json`
- `astrid/packs/vibecomfy/recipe.windows-cu130.json`
- `astrid/packs/vibecomfy/environment.windows-nvidia.json`
- `astrid/packs/runpod/extensions/generation.engine/comfyui.yaml`
- `astrid/packs/vibecomfy/extensions/generation.engine/comfyui.yaml`

The generator may rewrite other catalog files byte-identically. Template catalog hashes and dependency locks are expected to remain unchanged and must be checked. The Runtime, lifecycle, and ComfyUI pins stay unchanged. The App's published install manifest is a later release-owner concern; this request does not authorize changing it or publishing Release 14.

## Work and proof after approval

Keep this in `int/55-local-speed`. Wire the Agent's existing loopback/attested transport policy, redirect/proxy refusals, bounded responses, prompt witness and attempt journal through the new factories. Pod requests must continue through their attested transport. Do not replace those controls with VibeComfy's standalone defaults. Add progress consumption and preserve the existing typed results, one submission per attempt, and unknown-acknowledgement behavior.

The composed candidate must pass the pin generator and single-source tests, the packaged recipe authority tests, the Comfy target cases and attached output-custody/cancellation tests against the exact proposed source. New guarded HTTP/WS and consumer behavior needs focused tests, including a connector refusal that makes no POST, disconnect reconciliation with no raw-client fallback, and one attempt never reading another's outputs. The initial VibeComfy injection proof does not substitute for that composed run. The actual upstream ComfyUI success/cache/error/interruption event ordering also remains to be verified; a refused source read has not been retried.

**Recommendation:** authorize this exact VibeComfy pin and its generated digest updates for Plan 55 integration/testing. Product-main merges, any later pin, and publication remain separate owner gates. No formal review round has been consumed.
