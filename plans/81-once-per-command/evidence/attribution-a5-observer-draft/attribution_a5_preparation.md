# A-5 sibling gate preparation

This is unfinished preparation, not a gate or qualification. The US-2 gate and
its fixture are absent from the base used here. Existing tests, baseline,
ceilings and the timeline gate must remain untouched. No count baseline or delay
proof has been established. The helpers here require integration and review against
the actual US-2 fixture and final A-1–A-3 interfaces before use.

## Per-process interface

`attribution_a5_checks.check_sample` consumes a successful process's parent wall
and raw collector JSON: `ok`, `wall_seconds`, `collector_span_seconds`, and
`timings` (individual exclusive occurrence rows and exactly one `other command
work` row). It computes S, R, C, W−C and the paired uncovered share. Its clock
tolerance is an explicit caller input, not a calibrated or approved value. The
caller must establish and document that tolerance, and ensure the input rows
are the collector's non-overlapping exclusive occurrences, not aggregates or
inclusive totals. It must also supply a policy for the exact group and attempt
count, with positive minimum counts for every required stage. The policy must
explicitly classify each of `SDK admission preflight`, `Remote admission
preflight`, and `Workspace admission preflight` as required or inapplicable,
with a reason; applicable preflights must have positive required counts. Derive
and independently verify these classifications against the real trace. Counts must
be checked against approved upper ratchets separately; the helper alone is not a
complete count gate. Controller and worker `/object_info` counts must remain
separate, associated with the actual attempts and independently ratcheted.

`check_receipts` describes a proposed adapter for fixture observations: each
sample supplies unique `attempt_id`, `task_id`, `target_prompt_id` and matching
`task_attempt_id` and `target_attempt_id`, plus absolute host-clock monotonic
`spawn_monotonic`, `admission_monotonic`, `target_ack_monotonic`,
`exit_monotonic`, and `drained_monotonic`, and `drained: true`. The fixture must
actually observe and correlate these, not synthesize identities or timestamps.
Drain happens after the relevant timed endpoints, before the next trial. Runtime
admission, target acceptance and CLI exit are distinct boundaries; label the
endpoint used by each budget. The separate parent measurement of W must use the
same spawn and exit boundaries. Attempt counts and applicable route-specific
expectations must be determined from observed behavior; do not assume every
candidate takes the same route or attempt count.

## Remaining work before qualification

- Bring in the exact US-2 fixture and its comparison base; integrate a sibling
  invocation without modifying the old gate or timeline. Wire actual W/I/E
  commands, 5 fresh processes per `same`, `changed`, `image_same`,
  `image_changed`, and `image_entry`; obtain distinct matched task and target
  receipts and drain each trial. Capture controller/worker counts separately.
- Complete A-1–A-3 instrumentation and verify required stages and positive
  occurrence counts on each sample, including per-attempt and per-route counts.
  At this base only some required wrappers are present; absence must fail.
- Establish and document a defensible clock tolerance and the sampling and
  counting policies. Independently measure deterministic operation counts and
  record authority, provenance and raw observations in a versioned count
  baseline. Ratchet approved counts and document introductions. Do not invent
  count limits. Report seconds without gating them, except for the retained
  per-process 10% uncovered-wall bound.
- Add focused sibling tests and exercise the real fixture. Inject delay at each
  real newly timed operation to show its diagnostic, with unrelated count checks
  held clear. Inject 1.5 seconds outside the collector in a controlled process
  whose wall makes the 10% uncovered bound fail.
  A synthetic stage alone does not prove a production wrapper exists.
- Run all measurements, profiling, calibration and gate work serially under
  `flock /tmp/astrid-timing.lock` for the entire run and record load average.
  No such run or tests were authorized during this quiet window. Keep raw
  observations and report first failures; do not represent preparation as proof.
