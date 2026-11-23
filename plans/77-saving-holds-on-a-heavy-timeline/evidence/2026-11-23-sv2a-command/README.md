# Plan 77 SV-2a command package

This is a one-save diagnostic for the already retained synthetic 300-clip sandbox. The prior sandbox and both public accepted saves are recorded in the [profile receipts](../2026-11-23-save-profile/RESULT.md). The package needs the separate save session's written approval of the Runtime SHA and manifest digest before it can start the stack.

| Input | Exact identity |
| --- | --- |
| Runtime diagnostic | `667c450b927a4dc2471bbaa02f2631e6f6907cf2` |
| Archived tree | `34ee458236bc10ab5cbdca3460cc721a14601b88` |
| Retained Runtime source | `77c38d037f98f744bd8f41c15d95429c124a8003` |
| Retained program generation | `4b62ab1a6521` |
| Already compiled App | `148eaf381e3f02dc0f0d5dfc61e61ebf37dbc715` |
| Already installed Agent | `5e301956dc49c8b9ba4d23a7ce96c6564bd74d2f` |
| Local harness tooling | `a0339fe76048857cc11218ee766016d987a438a7` |
| Browser trace helpers' source tooling | `c027946e3bf77a187a88e981183486b9dfd1638f` |

`package.sha256` covers the eight command inputs. `package-digest.txt` records the SHA-256 of that manifest. On the lane box, `bash run-sv2a-overlay.sh <diagnostic SHA> <approved manifest SHA-256>` is the sole execution entry point. The optional `SV2A_STATIC_DRY_RUN=1` branch reads the package files and prints only the fixed inputs. The static dry run completed. The extracted archive's raw Git tree was independently reconstructed and matched, and the compared dependency and wire paths had an empty diff. The detached source fetch, syntax checks and dry run did not start any product process or inspect the retained stack.

The entry point archives the exact diagnostic source into a new private sibling directory. It verifies Git tree identity and records every archive file digest. The wrapper uses the retained interpreter with `-I -B`, selects the archived Runtime explicitly, and permits the normal direct Runtime bootstrap. The normal child import witness, owner discovery, archived module digests, source profile and catalog all have to agree before the editor is opened. Copies of the original catalog and source profile go into the private receipts before launch. Before and after inventories cover the retained interpreter, site-packages and `current` pointer. The direct path stays on the synthetic realm in the original stack.

The Runtime's `ASTRID_TIMELINE_MEMO_TRACE` opt-in writes `timeline-memo-trace.jsonl` in the fresh receipt directory. Before navigation and the one drag, the browser driver issues one authenticated local history GET with `limit=1`. The response must match the retained accepted revision and publication, and the trace must already contain `trace_runtime_source` with the exact live PID and the proven archived module path. Browser navigation then proves the original full public head, clips and occurrences again. The driver requires one commit POST, one accepted receipt, confirmed Saved and the expected exact canonical move. This diagnostic history GET can warm proof before the save, so these timings are not a performance gate sample. [Runtime trace writer](https://github.com/banodoco/astrid-runtime/blob/667c450b927a4dc2471bbaa02f2631e6f6907cf2/runtime_protocol/_timeline_memo_trace.py#L58) [History route](https://github.com/banodoco/astrid-runtime/blob/667c450b927a4dc2471bbaa02f2631e6f6907cf2/runtime_protocol/server.py#L970)

The command monitors a 16 GiB free-space floor, uses a fresh browser profile, and requires idle-safe Runtime down, the exact owner gone and the owned ports closed. It removes the disposable profile and retains private outputs under `run/evidence/plan-77/round7-acceptance/sv2a-first-save-<diagnostic SHA>/`. It leaves the signed source backup and retained program intact. No credential material, private launch receipts, RunPod input or raw host output is included in this archive.
