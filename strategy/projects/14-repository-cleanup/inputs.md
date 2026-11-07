# Inputs and provenance: repository cleanup

## Initial audit evidence

The recorded Astrid Agent snapshot `2958bacea3e3c7961788fa9c625dd9db0be282de` contains tracked `tests/.test_durations` (6,784,305 bytes), example material under `projects/astrid-intro/build/`, a prompt artifact under `output/imagegen/`, and repeated large card images across rendering examples. These are inspection targets only. Determine whether timing data, examples, and assets still serve a purpose; establish equivalent evidence in other repositories before adding cleanup tasks.

Preserve required checksum manifests and dependency locks. The [execution host refactor](../13-execution-host-refactor/plan.md) owns the giant module. Coordinate with [Plan 16](../16-streamlined-agent-experience/plan.md) where catalogs or integration instructions overlap.

## Starting code and destinations

Record actual identities at setup. Historical observations do not establish a live execution base.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| Astrid Agent | TBD at start | TBD at start | TBD at start | TBD at start | `pre-main`, verify at start |
| Astrid App | TBD at start | TBD at start | TBD at start | TBD at start | `pre-main`, verify at start |
| Astrid Runtime | TBD at start | TBD at start | TBD at start | TBD at start | `pre-main`, verify at start |
| Related first-party pack/inference repositories | TBD after bounded inventory | TBD at start | TBD at start | TBD at start | `pre-main` where applicable; verify at start |

No candidate file is preapproved for deletion. Confirm current repositories, branches and SHAs, existing work to preserve, verified predecessor inputs, fresh candidate branches, and intended destinations before implementation. Define the bounded inventory and focused selectors after source inspection.

## Constraints and evidence limits

The recorded Agent snapshot is historical, not a live source identity. It establishes the listed audit observations only; it does not establish that files are unused, removable, or representative of other repositories. Determine references, packaging use, and current purpose before changing candidates. Preserve active experiments, unpublished work, useful examples and historical evidence, package data, release evidence, checksum manifests, and dependency locks. No broad suites or automatic test discovery; see the [shared run contract](../../skills/astrid-dev-shared/run-contract.md) for routing and execution policy.
