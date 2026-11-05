# Inputs: Install and update confidence

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

The source plan records `pre-main` as the intended base and destination for each repository. These are historical rules, not verified live refs. Freeze each current head at IU-0. No full base or donor SHAs were recorded in the source plan; record them at start. The exact Plan 08 verified heads and reusable donor commits must be recovered from its existing run evidence. Do not treat the R1 stand-in update as proof of a real released-version migration.

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| astrid-agent | `pre-main`; exact SHA TBD at IU-0 | Plan 08 update step and stand-in generator; exact commits/custody TBD at start | Plan 08 verified head; exact identity TBD | Fresh create-only candidate name recorded at execution | `pre-main` |
| astrid-runtime | `pre-main`; exact SHA TBD at IU-0 | Plan 08 update step if applicable; exact commits/custody TBD at start | Plan 08 verified head; exact identity TBD | Fresh create-only candidate name recorded at execution | `pre-main` |
| astrid-app | `pre-main`; exact SHA TBD at IU-0 | Plan 08 update step if applicable; exact commits/custody TBD at start | Plan 08 verified head; exact identity TBD | Fresh create-only candidate name recorded at execution | `pre-main` |

No dirty-work custody is specified in the source plan; establish and record custody at start rather than assuming a clean tree. Confirm branches and existing run state before use. Plan 01's `cli.py`/`backend.py` overlap is a sequencing dependency: IU-1 coordinates with Plan 01 I-02 and whichever lands second rebases as required.

## References and evidence

| Source | What it establishes | Identity or link | Limits / missing information |
|---|---|---|---|
| Plan 08 Release 1 | Verified predecessor output, five-row gate, and update step | [Plan 08](../08-release1-install-update/plan.md), [inputs](../08-release1-install-update/inputs.md), [tasks](../08-release1-install-update/tasks.md) | Exact run heads/donor commits must be recovered; stand-in update is not a real version migration. |
| Plan 01 installer consent | Shared installer-file sequence | [Plan 01](../01-installer-consent/plan.md), task I-02 | Exact branch/file state must be reconciled at start. |
| Per-OS coverage baseline | Path × OS matrix classified real, mocked, or absent | IU-0, to be recorded at start | No baseline exists in this plan yet; define the supported-path rows from this plan's scope and record evidence per Linux, macOS, and Windows. |
| Runtime CLI schema and installer/service routes | Contract, update entry points, platform-specific behaviors named in scope | Source paths and line references in the original plan: `astrid/installer/local_update.py`, `update_job.py`, `app_update.py`, `custody.py`, `service.py` (~110–127 and ~972–983) | Source identities are not frozen; inspect at task start. |

## Constraints

Preserve user data and the last working version on failed or unsupported operations. Use real hosted tests for supported user paths; mocked coverage does not satisfy the OS/path matrix. Pinokio remains in Plan 07 and pack install/update/rollback remains in Plan 06 PK-9. Follow the shared [run contract](../../skills/astrid-dev-shared/run-contract.md) for identity, routes, checks, review, and publication. No plan authorizes execution; preserve existing authority and review limits.
