# Evidence — Agent main green

[Plan](../plan.md) · [Inputs](../inputs.md) · [Tasks](../tasks.md)

What fails in astrid-agent's own CI on `release/15/main`, grouped by where each test fails, and which card owns each group.

## The measurement

| | Value |
| --- | --- |
| Head | `release/15/main` at `b324d7c1`, the latest head with both CI and Lanes complete (23 November 2026) |
| Runs | [CI 45183456598](https://github.com/banodoco/astrid-agent/actions/runs/45183456598), [Lanes 45183456544](https://github.com/banodoco/astrid-agent/actions/runs/45183456544) |
| CI | the eight `unit` shards and `darwin native`: 1,087 distinct failing or erroring (job, id) pairs (1,095 rows: a test failing in several subtests is listed more than once) in 274 files, 437 clusters |
| Lanes | `integration` 1–4 and `opt-in`: 787 distinct (job, id) pairs in 129 files, 104 clusters |
| Green on the same head | `fast checks`, `boundary`, `windows-native-and-installer`, both release wheels, `installed wheel`, `Chat service`, `Windows task host journey`, `Windows runtime retention` |
| Compared with | Agent `main` at `c0ad6b54` (Release 14): 1,070 CI IDs fail on both; Lanes has 36 IDs that are new on `release/15/main` |

## Files

| File | What it is |
| --- | --- |
| [release-15-b324d7c1/ci-clusters.md](release-15-b324d7c1/ci-clusters.md) | CI clusters, largest first, then failing IDs by test file. `ci:C<n>` in the tasks refers to row `C<n>` here |
| [release-15-b324d7c1/lanes-clusters.md](release-15-b324d7c1/lanes-clusters.md) | The same for Lanes (`lanes:C<n>`) |
| [release-15-b324d7c1/ci-failing-ids.tsv](release-15-b324d7c1/ci-failing-ids.tsv), [lanes-failing-ids.tsv](release-15-b324d7c1/lanes-failing-ids.tsv) | Every failing ID with its cluster, outcome and job. The job column tells a `darwin native` failure from a Linux one, so key by (job, id). AG-1 seals its ceiling from the lists AG-0 regenerates |
| [release-15-b324d7c1/assignment.json](release-15-b324d7c1/assignment.json) | The one record of which Wave A or B card owns which cluster, and which test files (by glob). AG-A8 shares AG-A7's cluster and splits it by refusal message |
| [release-15-b324d7c1/wave-c-cards.md](release-15-b324d7c1/wave-c-cards.md) | Every unowned ID, as one card per test file, with the count of IDs per card owner |
| [release-15-b324d7c1/prune-candidates.md](release-15-b324d7c1/prune-candidates.md) | The IDs whose failure points at removed, retired, moved or legacy code, for AG-P1 to sort into retire, redundant or keep |
| [cluster_failures.py](cluster_failures.py) | Groups pytest failures in job logs by the frame that raised them; writes the clusters and the TSV |
| [make_wave_c.py](make_wave_c.py) | Reads the TSVs and `assignment.json` and writes `wave-c-cards.md` and `prune-candidates.md`, counting each (job, id) once |
| [critique.md](critique.md) | The independent critique and the two ambiguity passes, and what each changed |

## How it was made, and how to redo it

1. Download a run's log archive (the Actions API's run logs URL) and unzip it into an empty directory.
2. Run `python3 -I cluster_failures.py <out> <unit shard logs> <darwin native log>` for CI, and the same with the integration and opt-in logs for Lanes. Rename the outputs as above.
3. Update `assignment.json` if a cluster's number moved, then run `python3 -I make_wave_c.py <release folder>`.

The grouping key is the exception type and the file and line that raised it. When the raise is inside the standard library or pytest, the key is the first frame in the Agent's or Runtime's code. One cause can span several clusters (for example a fixture shape that fails at several assertions), and one cluster can hold two causes (for example a `FileNotFoundError` raised in `pathlib` for different missing files). The [triage rules](../tasks.md#triage-rules) settle both on the card.

Test IDs, paths and messages come from public CI logs. The logs themselves are not kept here.
