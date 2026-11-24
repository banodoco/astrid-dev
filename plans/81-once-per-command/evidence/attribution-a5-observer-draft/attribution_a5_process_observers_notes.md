# Partial process observers

These opt-in hooks have not been tested, timed, calibrated, or connected to a
fixture. They are not a gate or measured baseline. Install independently in each
relevant process before product imports and aliases, associate actual attempt
identity using the live adapter's context, and require observer start/end,
coverage events, sequence integrity and all expected process observations. A
missing event stream or null attempt is unknown, never zero. Worker, launcher,
controller, daemon and host coverage must be recorded separately.

`observe_launcher_starts` records a child PID only after successful Popen
initialization while the actual autobootstrap `_invoke_launcher` is active in
the same context. A failed process creation is not a start. Other threads,
other processes, previously bound invoker aliases, and launch paths outside
this wrapper remain unobserved. This process-global patch assumes exclusive
ownership during its context. Review interaction with subprocess and concurrent
operations before use. Sink errors poison observer health without escaping the observed call, including
after process creation. The fixture must still manage and drain the child.

`observe_hashlib` returns the original native object and passes native calls
through unchanged, with sink errors contained in observer health. It records successful
`hashlib.sha256` constructor calls and the initial input size only when safely
available for exact built-in bytes, bytearray or memoryview; otherwise the size
is null. It records successful `hashlib.file_digest` calls with unknown
algorithm and bytes, because inspecting arbitrary digest factories or streams
can alter behavior. It does not observe native object updates or copies,
`hashlib.new`, other algorithms, bound aliases, native callers, or subprocesses.
Consequently neither complete calls nor byte totals can be inferred, even if
no events were seen. The older A2 probe wrapped returned native hash objects and
estimated stream bytes from offsets; that can change object or stream semantics,
so this preparation deliberately leaves those bytes unknown. Failed calls are
not counted as successful calls; exceptions from the native call propagate.
Observer failures invalidate a trial; the harness must inspect health outside
the product call and must reject missing or incomplete event streams.

The YAML observer in the companion adapter sees only `yaml.safe_load` and
`yaml.load` module attributes in an installed process; nested calls count once.
Earlier aliases and other APIs remain unobserved. Prove positive known calls,
byte coverage, API bypass and deleted-sink failures independently, quantify
overhead, and compare with the actual route and fixture before any count policy
is used. No coverage claim or conditional absence follows from these hooks.

## Required proof before use

The context managers yield an `ObserverHealth`; the harness must retain it and
call `assert_healthy()` after the observed work, independently require sink
start/end markers, contiguous sequences and expected process/attempt coverage,
and reject missing, dropped, unattributed, or malformed events. A killed
process cannot report its in-memory poison flag, so an absent end marker is
invalid. `EventSink.close` and setup are harness operations and can fail there;
they must never be interpreted as a successful zero. Health alone cannot prove
API coverage, detect a silently dropped write or prove route absence, so these
observers are not gate-ready.

After the quiet window, independently exercise an injected raising sink before
and after successful native SHA and file digest calls, native exceptions, and
successful and failed launcher creation. Compare native result type, value and
exception against the unobserved operation, verify the child is retained and
drained, and require the harness to reject poisoned or missing observations.
Exercise sink deletion, dropped/truncated event streams, bound-alias bypass,
multiple processes and attempts, YAML nesting and distinct loads, and exact
known constructor input sizes. Confirm null file/update bytes never become
zero. Quantify observer overhead and prove the actual fixture route before any
independent count policy or gate use. No such proof has yet been run.

## Stream preparation

`attribution_a5_event_stream.read_event_stream` can validate one closed sink
against a creation-time file identity and independently observed trial, process
and attempt identities. `attribution_a5_observed_counts.observed_lower_bounds`
retains only observed event counts by process and attempt; missing metrics are
not zero totals and hash bytes remain unknown. These helpers do not discover
expected processes, verify observer health or prove that any API coverage is
complete. Their synthetic checks do not establish a live fixture, an oracle or
an upper budget. The eventual fixture must reject missing streams and unhealthy
observers, and establish complete independent coverage before checking counts
against the pinned baseline.
