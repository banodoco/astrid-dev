# Inputs: execution host refactor

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| `banodoco/astrid-agent` | TBD at start; historical observations below are not a current base | TBD at start; inspect applicable execution changes, including sandbox process control from PR #109 | TBD; no verified predecessor output recorded | TBD at start | `pre-main`, verify its existence and preserve existing publication policy |

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| `astrid/core/execution/generic_host.py` on `pre-main` | Historical observed size: **17,067 lines** | Inspected 2026-11-05; [source](https://github.com/banodoco/astrid-agent/blob/pre-main/astrid/core/execution/generic_host.py); blob `b0ea83326115ec172a79260d657be7dd01c3c4a1` | Historical observation only; recheck the selected starting commit. |
| `astrid/core/execution/generic_host.py` on `main` | Historical observed size: **14,453 lines** | Inspected 2026-11-05; [source](https://github.com/banodoco/astrid-agent/blob/main/astrid/core/execution/generic_host.py); blob `da61b21aed220a4c35c27d62baca19eeef1b09c4` | Different historical snapshot, not the proposed execution base. |
| Agent PR #109 | Changes `generic_host.py` for sandbox process control; its work may need preservation | [PR #109](https://github.com/banodoco/astrid-agent/pull/109) | Not itself the decomposition project. Determine applicability against the selected base; do not assume PR state or merge status. |
| Inspected `main` snapshot | Handwritten orchestration includes Runtime protocol access, capability discovery, task execution and settlement, local preparation, persistent supervision, and process handoff. Generated protocol client is separate in `astrid_runtime_client/generated.py`. | Historical code inspection, 2026-11-05 | Candidate boundaries only; coupling must be checked on the actual base. |
| [Multiple inference routes](../12-multiple-inference-routes/plan.md) | Owns the shared inference lifecycle. | Project plan | Context, not a scheduling gate. |
| [Streamlined agent experience](../16-streamlined-agent-experience/plan.md) | Owns the single agent extension path. | Project plan | Context, not a scheduling gate. |

The historical counts and blob SHAs are evidence about inspected snapshots, not live source identity or authorization. The roughly 18,000-line recollection is only a clue for locating the file.

## Constraints

At setup, confirm repositories, actual base branches and SHAs, work to preserve, verified predecessor inputs, a fresh candidate branch, and the intended `pre-main` destination. The original draft specifies no review rounds or limits; retain the run configuration and existing authority at setup without adding review stages. Derive task boundaries and exact focused selectors from that source. Preserve existing execution behavior; characterize before extraction and rerun the same checks, including any touched lifecycle, cancellation, process ownership, and result-handling behavior. Do not conflate moving code with semantic fixes. Follow the [shared run contract](../../../skills/astrid-dev-shared/run-contract.md) for routes, source identity, proof, and publication limits. This draft does not authorize implementation or broad test discovery.
