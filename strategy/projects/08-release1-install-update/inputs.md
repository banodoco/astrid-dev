# Inputs: Release 1 install and update

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

The source plan records `int/r1` as the integration branch in each repository, with landing-specific base and donor identities in the R1 merge fixes log. Those are historical branch observations, not frozen execution identities. No full source SHAs were included in the source plan; freeze and record the exact base, donor, and candidate identities in the existing strict run before relying on evidence. No dirty work is carried.

| Repository | Recorded branch; SHA | Retained work / donor custody | Verified predecessor | Candidate branch | Destination |
|---|---|---|---|---|---|
| astrid-agent | `int/r1`; freeze exact SHA at run | Per landing in merge fixes log; no dirty work carried | R0 served by public install line (`tests/upgrade/releases.json`, `served` row) | Lane branch named per landing | `int/r1`, fast-forward mirrored to `pre-main` |
| astrid-runtime | `int/r1`; freeze exact SHA at run | Per landing in merge fixes log; no dirty work carried | R0 served by public install line | Lane branch named per landing | `int/r1`, fast-forward mirrored to `pre-main` |
| astrid-app | `int/r1`; freeze exact SHA at run | Per landing in merge fixes log; no dirty work carried | R0 served by public install line | Lane branch named per landing | `int/r1`, fast-forward mirrored to `pre-main` |
| astrid-pinokio | `int/r1`; freeze exact SHA at run | Per landing in merge fixes log; no dirty work carried | R0 served by public install line | Lane branch named per landing | `int/r1`, fast-forward mirrored to `pre-main` |

The `pre-main` destination and fast-forward mirror rule are preserved from the source plan; verify live branch identities and existing run state at execution. Do not assume a branch exists based on this historical record.

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| R1 merge plan, decisions, failure ledger, and merge fixes log | Active coordinator's detailed scope, accepted decisions, historical failures, per-landing source custody, and run evidence | [R1 merge docs](https://github.com/hannahsubmarine/repo/tree/claude/jolly-feynman-l6ckx7/docs/merge-plan) (`R1-PLAN.md`, `DECISIONS.md`, `status/FAILURES.md`) | The source plan names the branch but contains no full commit SHAs or landing selectors; recover/freeze these from the active run and merge fixes log. Preserve existing review rounds and authority there. |
| Journey matrix, workflow, and evidence checker | Strict R1 gate membership and evidence requirements | `scripts/journey_matrix.py` (`RELEASE1_MATRIX`), `.github/workflows/journey.yml`, `scripts/check_journey_evidence.py` | Must require exactly five rows: `direct-linux`, `direct-macos`, `direct-linux-fresh`, `direct-macos-fresh`, `direct-windows`. |
| R0 served release record | R0 predecessor installed by the public install line | Agent `tests/upgrade/releases.json`, `served` row | Resolve the served identity from the frozen run; do not substitute a different historical R0. |
| Hosted runners | Required provenance for strict gate | `ubuntu-24.04`, `macos-15`, `windows-2022` | Local runs do not satisfy hosted provenance. |

### Five-row behavior

- `direct-linux` and `direct-macos`: R0-to-R1 upgrade, install checks, task, and cleanup asserting refusal of uninstall after upgrade.
- `direct-linux-fresh` and `direct-macos-fresh`: fresh install, install checks, task, then update to a stand-in next version.
- `direct-windows`: fresh install, install checks, task, update to a stand-in next version, and safe refusal of R0-to-R1 upgrade.

The update stand-in is generated from the same code at release + 1. Its result establishes update mechanics only; it is not evidence of a real version-to-version migration. The canonical behavior and evidence requirements are detailed in [tasks.md](tasks.md).

## Constraints

Keep the active Release 1 merge coordinator, scope, evidence, review state, and publication authority intact. A plan does not start or resume product work. Use the shared [run contract](../../../skills/astrid-dev-shared/run-contract.md) for identity, proof, review, and authority rules; do not reset accepted choices or add approval stages. The owner ship call records a decision and does not itself broaden the accepted publication authority.
