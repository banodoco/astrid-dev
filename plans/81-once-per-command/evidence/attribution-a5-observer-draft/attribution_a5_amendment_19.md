# Amendment 19: count-based sibling gate preparation

This note records amendment 19 for the sibling gate preparation. The earlier
wall-ceiling helper was removed because it conflicted with this amendment.
Seconds are reported, not gated, except the explicitly retained 10% per-process
uncovered-wall bound in ruling 3. The old US-2 gate and its existing baselines
remain unchanged; any separate required comparison belongs to that old gate.
There is no approved new count baseline in this checkout.

`attribution_a5_count_policy.py` sketches a fail-closed policy interface for
hash calls, bytes hashed, YAML loads, discovery occurrences and launcher starts.
It checks each sample against separately approved minimum and maximum counts for
its exact group and number of attempts. An absent route/attempt policy fails;
no per-attempt average, assumed constant count, fabricated baseline, or wall
ceiling is used. The policy must explain expected zero work, and required
positive work and receipt checks remain independently necessary. Introductions,
changes and ratchets require documented authority and preserved earlier
approved values. This helper does not yet enforce those baseline migrations.

Before use, an independent worker must measure the real operation call sites
and bytes, identify process/worker boundaries and stable event definitions, and
associate counters with each actual attempt and route. The worker making a
change does not measure that change. Capture raw per-process and per-attempt
observations and distinct matched Runtime task and target prompt receipts;
drain trials between processes or isolate endpoints. Keep controller and worker
request counts separate, and retain required stage occurrence checks as well as
the 10% residual check. Establish approved counts from observed, repeatable
fixture runs, with provenance, then implement and validate versioned ratchets
without deleting previously approved groups or weakening the existing checks.
The count helper alone cannot verify instrumentation coverage, receipt identity,
individual attempt records, or baseline authority.

Still required: the absent US-2 fixture and A-1–A-3 prerequisites; five real
fresh processes for each W/I/E group; approved clock tolerance; matching three
monotonic boundaries and drained receipts; real-operation delay and controlled
1.5-second unscoped-delay proof; focused adversarial tests and independent gate
review. No test, timing, count measurement, profile or CI run was performed
while preparing this amendment. This is not operational readiness or proof.

The prepared `check_sample` requires a caller-supplied stage policy for the
exact route and attempt count, including explicit dispositions for the three
distinct admission preflights. The policy must be checked against the actual
instrumented routes and real-operation proof before integration. Its required
stage minima are not an amendment-19 counter budget. Keep the existing tests unchanged, and do not use
that unreviewed helper as evidence that an operation occurred.
