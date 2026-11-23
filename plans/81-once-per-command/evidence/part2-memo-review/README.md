# Part 2 memo review: Plan 82 handoff

Part 2 tried a scoped object-info memo and read-set end checks at VibeComfy PR #182 candidate `675f5dc2658197318a95e0e1b7c5b232b17cd9d5`, comparing a full-content end hash with a separate stat end check. The independent blind review **failed**: an overlapping public emit published after its index became persistently invalid because revocation made its publication callbacks return without checking. Under the Lead's rule the class (i) finding stops Part 2 for this release. PR #182 stays unmerged at `675f5dc2`; nothing is pinned.

| Class | Finding and reproduction |
| --- | --- |
| (i) Publication regression | In [overlapping emits](./scratch/overlap_min.py), the head publishes after owner revocation while the base refuses: [base](./scratch/minimal-base.log), [head](./scratch/minimal-head.log). The [transient memo-hit case](./scratch/transient.py) also changes refusal to publication. |
| (ii) Stable-input parity | Malformed generation and unused cache symlink loops change error or refusal order: [generation loop](./scratch/static_generation_loop.py), [empty workflow](./scratch/empty.py). See the [blind report](./blind-review-report.md) for paired outputs and the CPython version qualification. |
| (iii) Read-set and refusal gaps | [Warm directory](./scratch/warm_dir.py), [generation provenance](./scratch/generation.py), [supplemental reader](./scratch/supplemental.py), [ready wrapper](./scratch/wrapper.py), [observed root](./scratch/observed_root.py), [first refusal](./scratch/compare.py), [capture](./scratch/capture.py), and [reconciliation](./scratch/unscoped.py) show missed dependencies or changed refusal points. Some are inherited by the base, not newly introduced. |
| (iv) Resource boundary | On CPython 3.11.18, the fixed input at JSON nesting depth 978 publishes on base and raises `RecursionError` on head; 977 succeeds and 979 refuses on both. The blind report groups this under stable-input parity; the Lead called it a resource boundary. See [reproduction](./scratch/depth.py), [base](./scratch/isolated-depth-base.log), [head](./scratch/isolated-depth-head.log), and the [boundary investigation](./depth-boundary.md). |

## Counted SHA-256 work

These are process-wide SHA-256 construction counts and bytes, not wall-time savings. W is the 13-class workflow proxy; the second column pair totals 53 templates. Measurements and caveats are in the [measurement summary](./measurement-summary.md); the `950023c8` row is the earlier candidate, and the original base is `48b5fa9e`.

| Revision / end check | W calls | W bytes | 53-template calls | 53-template bytes |
| --- | ---: | ---: | ---: | ---: |
| Base `48b5fa9e` | 7,608 | 5.42 GB | 1.73 million | 630 GB |
| `950023c8` | 240 | 203 MB | 37,391 | 13.85 GB |
| `675f5dc2` full hash | 1,703 | 1.52 GB | 1,741,985 | 629 GB |
| `675f5dc2` stat | 1,697 | 1.517 GB | 1,741,635 | 629.0 GB |

The [staging probe](./scratch/staging.py) did not reproduce alleged leftover 0600 staged files: refusals preserved existing members and cleaned temporary staging. The zero-byte lock is inherited and remains on both sides. In the [mirror](./scratch/mirror.py), a change after first observation is refused by the head where the base can mix old and new reads; a change before the first observation succeeds on both. The [360-schedule sweep](./scratch/sweep.py) found 206 same refusals at the same point, 87 refusals on both at different errors or points, seven publications only on base, and 60 publications on both. These are finite fixture schedules, not exhaustive concurrency coverage.

For Plan 82, move memo scope into the emitters; owner revocation must never bypass publication checks. Observe paths before resolving them, include supplemental readers in the read set, and prove stable-input parity including symlink loops and the recursion-depth boundary. The [read-set design](./part2-readset-design.md), [checks summary](./checks-summary.md), and [warm-generation differential](./warm-generation-differential.md) preserve the remaining context. The stat option can miss an in-place same-size, restored-mtime rewrite; it must not be represented as full byte validation.

## Package and omissions

The [blind review](./blind-review-report.md) is the reviewer's report; its relative link targets were prefixed with `./` and its external PR link rendered as plain text for this package; external links in the reviewed PR body are likewise rendered as plain text. The `scratch/` directory contains the reviewer's top-level Python reproductions, paired base/head logs and the report's other linked small artifacts, including sweep and mirror rows. The design and measurement notes contain original local paths and commands as historical provenance; files they mention in plain text are not all included. The two small warm-generation logs are included beside the differential.

Excluded: extracted `base/`, `head/`, `mut/` and other output/member trees; Python environments, dependencies, `__pycache__` and other caches; unlinked stderr files and unrelated temporary logs. The supplied review's paths to those trees and environments are not a portable rerun environment; reproduce only after providing the exact source revisions and dependencies. No new measurement or reproduction was run to assemble this package.
