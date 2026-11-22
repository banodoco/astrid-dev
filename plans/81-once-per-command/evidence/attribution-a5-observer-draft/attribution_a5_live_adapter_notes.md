# A-5 live adapter: incomplete preparation

`attribution_a5_live_adapter.py` supplies opt-in observation primitives, not a
runner, gate, baseline, or evidence of operation coverage. No tests or timing
were run. The US-2 base fixture is unavailable; compatibility with it and with
final A-1–A-3 instrumentation is unverified. Integrate as a sibling without
editing that fixture, its checks, or its baseline.

The sink records per-process role, PID, trial, optional actual attempt identity,
sequence, and monotonic timestamp. Its start/end events and file identity permit
a consumer to reject missing, truncated, replaced, or incomplete observation;
the consumer still must implement those checks and detect missing processes.
Null attempt means unattributed, not zero. Product-path sink errors poison observer health instead of escaping the
observed call; the harness must explicitly check health and reject incomplete
streams. Setup and close failures remain harness errors. Do not propagate trial/attempt via Runtime wire
or product payload; obtain correlation from actual fixture observations.

The YAML wrapper observes only calls to the two module attributes installed
while its context is active. The nesting guard avoids counting safe_load's
nested load twice. Earlier bound aliases, direct loader calls, native work,
other processes and operations before installation remain unobserved. Discovery
rows must be raw exclusive collector occurrence rows; aggregation is not proof
of coverage. Launcher events wrap the real `_invoke_launcher` entry and return,
but do not establish a successful subprocess start: that requires a separately
instrumented actual process-creation boundary. The wrapper preserves the
actual action (including connect, up, bootstrap and recovery). None of these
observations may be read as whole-operation totals. Hash calls and byte counts,
actual launcher starts and per-attempt assignment remain to be implemented and
validated. Controller, launcher, daemon, worker and host observations must be
separately identified, including unobserved domains.

The A4 source runner's real Runtime `_send` post-write admission hook, target
`PodComfy.submit` and HTTP handler post-response hook, and terminal task polling
are candidate integration points. Match the task ID from actual CLI output to
the Runtime receipt, and target prompt identity and request content to the same
trial; reject duplicates and ambiguity. Drain the actual task and pending
observations after timed endpoints before the next trial. The sample's spawn,
admission, target response and exit clocks must be independently captured.
Do not infer that a task ID, prompt ID or attempt identity corresponds merely
because it appeared in the same time window.

Before use, implement and independently validate the missing counter hooks,
sink deletion and bypass failures, real-operation delay/deletion seams, and a
controlled external 1.5-second delay. Measure observer overhead and calibrate a
defensible clock tolerance. Obtain real independent route and absence evidence,
separate controller/worker `/object_info` counts, establish independently
pinned per-group and per-attempt policies, and verify five fresh matched and
drained processes for each group. No measured counts, bounds, or qualifying
results are supplied here. All measurement and calibration must take the timing
lock for the entire run and record load.
