# Part 2 end-check measurement — 675f5dc

Independent counts-only comparison of the committed read-set candidate with
the two end-check functions selected in-process. No product files were
modified, and no installed or wall-time measurements were run.

## Source, environment, inputs

- Candidate: `/tmp/option-a`, clean at `675f5dc2658197318a95e0e1b7c5b232b17cd9d5`.
- Baseline: detached read-only worktree `/tmp/measure-675f-base950`, clean at
  `950023c8846233f0006aac100d26b76711c42515`.
- Runtime: Python 3.13.18 from `/tmp/option-a/.venv/bin/python`.
- Cache: `/tmp/f1-options-common-cache`, 63 files / 13,655,519 bytes; per-file
  SHA-256 manifest in `input-manifest.json`. This is the same path recorded by
  the prior 950 53-template proof and W proxy proof.
- The candidate commit changes only the read-set implementation and focused
  tests relative to 950; no ready template or `template_index.json` changed.
- Every arm used its own fresh output directory. `full` is the default
  `_bundle_end_witness`; `stat` was selected with the requested
  `consume._bundle_end_witness = consume._bundle_end_stat_witness` monkeypatch.

## Exact commands

Each command was prefixed with a nonblocking lock check and then held the same
lock for the measurement, at low scheduler priority:

```sh
flock -n /tmp/astrid-timing.lock true && flock -n /tmp/astrid-timing.lock nice -n 19 /tmp/option-a/.venv/bin/python run/evidence/part2/measure-675f/measure.py baseline w /tmp/measure-675f-base950 /tmp/f1-options-common-cache run/evidence/part2/measure-675f/baseline-W-v2
flock -n /tmp/astrid-timing.lock true && flock -n /tmp/astrid-timing.lock nice -n 19 /tmp/option-a/.venv/bin/python run/evidence/part2/measure-675f/measure.py full w /tmp/option-a /tmp/f1-options-common-cache run/evidence/part2/measure-675f/full-W-v2
flock -n /tmp/astrid-timing.lock true && flock -n /tmp/astrid-timing.lock nice -n 19 /tmp/option-a/.venv/bin/python run/evidence/part2/measure-675f/measure.py stat w /tmp/option-a /tmp/f1-options-common-cache run/evidence/part2/measure-675f/stat-W-v2
flock -n /tmp/astrid-timing.lock true && flock -n /tmp/astrid-timing.lock nice -n 19 /tmp/option-a/.venv/bin/python run/evidence/part2/measure-675f/measure.py full templates /tmp/option-a /tmp/f1-options-common-cache run/evidence/part2/measure-675f/full-templates
flock -n /tmp/astrid-timing.lock true && flock -n /tmp/astrid-timing.lock nice -n 19 /tmp/option-a/.venv/bin/python run/evidence/part2/measure-675f/measure.py stat templates /tmp/option-a /tmp/f1-options-common-cache run/evidence/part2/measure-675f/stat-templates
```

The two W arms were repeated after correcting the witness-call counter to
include absent-path checks; the final W figures below use the `*-W-v2` raw
files. The original 53-template arms already counted every successful
SHA-256 digest and match the baseline proof's witness counter semantics.

## Counter method

The script wraps `hashlib.sha256` process-wide after imports and counts every
construction plus every byte passed at construction or through `update()`.
That includes raw SHA-256 calls outside `cache_file_witness`. Artifact digest
calculation for the report is deliberately excluded. A separate counter wraps
the production witness aliases and records both all witness invocations
(including absent paths) and successful file digests/bytes. The aggregate
`all_sha256_*` metric is therefore the authoritative hash count; the
`successful_witness_sha256_*` metric isolates SHA-256 work done by successful
object-info file witnesses. This instrumentation counts SHA-256 only, the
algorithm used for cache byte witnesses and the measured end-check option.

## Results

### W proxy

W is `ready_templates/image/qwen_image_2_1_turbo.py` (13 distinct classes),
emitted against the common cache. The baseline's 240 witness invocations
include 73 absent `CURRENT` checks that do not hash bytes; my first summary
counted only the 167 successful file digests. The corrected counter now
separates those values. The 950 raw W record also reports 240 invocations and
203,538,906 witness bytes.

| Arm | All SHA-256 calls / bytes | Witness invocations | Successful witness SHA-256 calls / bytes |
|---|---:|---:|---:|
| 950 baseline | 310 / 203,743,464 | 240 | 167 / 203,538,906 |
| 675 full byte check | 1,703 / 1,522,314,434 | 2,094 | 1,557 / 1,519,285,518 |
| 675 stat/identity check | 1,697 / 1,516,665,710 | 2,086 | 1,551 / 1,513,636,794 |

All three arms have the same output member sizes and SHA-256 digests, bundle
revision, warning list, and no refusal. Full versus stat differs by 6 SHA-256
calls and 5,648,724 input bytes. The W-v2 pair's raw SHA-256 byte totals were
3 bytes above the earlier W run in each mode; call counts, output, warnings,
bundle revision and the full/stat delta were unchanged.

### 53 ready templates

Both 675 modes have identical output member names, byte counts and digests,
bundle revisions, warnings and refusals. Both match the existing 950 proof in
`../phase2-root-9500/templates.json` on all 53 template IDs and those same
fields. The cache path and template IDs match; no candidate code change touched
template sources or the template index. `full-vs-950.json` and
`comparison-summary.json` record the per-template comparisons.

| Arm | All SHA-256 calls / bytes | Successful witness SHA-256 calls / bytes | Other SHA-256 calls / bytes |
|---|---:|---:|---:|
| 950 baseline witness record | not measured globally / not measured globally | 42,345 / 15,746,497,786 | — |
| 675 full byte check | 1,741,985 / 629,339,901,399 | 1,730,558 / 629,317,107,046 | 11,427 / 22,794,353 |
| 675 stat/identity check | 1,741,635 / 629,010,188,743 | 1,730,208 / 628,987,394,390 | 11,427 / 22,794,353 |

Full versus stat differs by 350 SHA-256 calls and 329,712,656 bytes. Against
the 950 witness-only baseline, both 675 modes hash far more because the new
read-set is validated across memo hits; the end-check choice itself accounts
for only a small fraction of the total. These counts provide no wall-time or
installed-performance result.

## Raw evidence

- Runner: `measure.py`.
- W detailed outputs: `baseline-W-v2/result.json`, `full-W-v2/result.json`,
  `stat-W-v2/result.json`, and `w-comparison.json`.
- 53-template raw outputs: `full-templates/result.json` and
  `stat-templates/result.json`.
- 950 output comparison: `full-vs-950.json` and `comparison-summary.json`.
- Earlier W run outputs are preserved in `baseline-W/`, `full-W/`, and
  `stat-W/`; the v2 runs added the all-invocation witness counter.
