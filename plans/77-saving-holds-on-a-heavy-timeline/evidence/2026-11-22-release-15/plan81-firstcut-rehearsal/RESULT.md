# Plan 77 first-cut rehearsal against frozen Plan 81 Part 1

The rehearsal used the Lead's frozen Plan 81 Runtime and Agent inputs and the locally qualified Plan 77 first-cut sources. Both ordinary local merge commits were conflict-free. All rehearsal refs and generated pins are local. The actual cut freezes only after both predecessor plans land.

| Repository | Plan 77 input | Frozen Plan 81 input | Local merge |
| --- | --- | --- | --- |
| Runtime | `77c38d037f98f744bd8f41c15d95429c124a8003` | `72b129e5a2296dc58360a9896cc65fab9db4ad0c` | `332c140f476edb72257c452f3ebc6a3a4f7a42db` |
| Agent | `b7f0e96a4934ddb4c123eab791a6e18efb8f79ac` | `a29383661ad990da7ab43185f1a07132e074fadf` | `2c1ba2c43dc9ad4c3e8ac1a25e772ff735fd9062` |

Runtime received `runtime_protocol/source_identity.py` and the upstream source-identity budget test without conflicts. The Runtime 0.2.15 contract and generated package files were identical. The Agent auto-merge kept the verified-head method, capability and remote bundle reader. Agent inherited an end-of-file whitespace warning in `tests/sdk/test_generation_snapshot_lifecycle_a3.py` already present in the exact incoming diff.

| Scope | Exact previous first-cut control | Rehearsal candidate | Result |
| --- | --- | --- | --- |
| Runtime first-cut memo, pinned read and custody selectors | `77c38d03` | `332c140f` | 12 passed on each, zero failed IDs |
| Runtime protected `tests/test_v33_protected_acceptance.py` | `77c38d03` | `332c140f` | 165 passed on each, zero failed IDs |
| Agent `tests/sdk/test_workspace_client_timeline_commit.py` and `tests/editing_conformance/test_verified_head_reader.py` | `5e301956`, pinned to Runtime `77c38d03` | `26737ad8`, pinned to Runtime `332c140f` | 29 passed on each, zero failed IDs |

The Runtime proof corrected one archived path transcription to `tests/test_timeline_verified_reads.py::test_verified_head_replays_after_restart_then_reuses_the_completed_proof`. The worker ran the same selected IDs on both sides. The paired Agent check used each side's exact Runtime checkout on its import path. A third proposed CLI batch file exists only on the merged tree and was outside the paired result. The first collect failure and default candidate-only deselection were setup evidence. All successful suites reported the same missing local pytest timeout-option warning.

Run the official Agent `scripts/regenerate_runtime_pins.py` from the exact final Runtime to produce both Agent lock copies and the App Runtime lock. Then rerun with the generated Agent commit to update App's installer manifest. The local rehearsal pinned Runtime `332c140f` in Agent `26737ad8`, then Agent `26737ad8` and Runtime `332c140f` in App `c9a2a6b6`. The second generation pass was clean. All 16 Agent and 14 App artifact payloads matched the exact Runtime source object and their consumer bytes. The manifest schema digest was unchanged. Repeat the generation and witness checks after the actual ordered merges, starting with the accepted Runtime and Agent landing identities. [Exact local witness](pin-artifact-witness.json)

No installation, product push, publication or hosted CI was part of this rehearsal. The pre-freeze Lead-machine recheck is a separate, read-only request with its own launch authorization. [432-clip command and custody addendum](432-firstcut-recheck-addendum.md)
