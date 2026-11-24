# A-5 witness observer: local unqualified draft

This document describes a local draft only. The witness observer is not a
qualified counter, baseline, or gate, and these results do not authorize its
use to accept or reject a candidate.

## Narrowly observed seam

When installed before the relevant consumer aliases are bound, the draft
observes calls routed through the patched
`vibecomfy.porting.object_info.generation.cache_file_witness` function. For
each successful `Path.read_bytes()` call made inside one such witness call, it
checks that the returned object is exactly `bytes`, records its length as
`digest_input_bytes` only when that same object is passed to one
`hashlib.sha256` call, and emits one `cache_file_witness` event. The observer
requires at most one read and one SHA call in the witness scope. It reports
`os_read_bytes: null`: the length of the returned Python buffer is not a
measurement of bytes read by the operating system. A failed read, unexpected
operation shape, witness exception, or sink error poisons observer health and
must invalidate the observation.

These are counts and byte lengths for calls seen through that scoped witness
path in that process and attempt. They do not describe all hashing or all file
I/O. The module explicitly refuses installation if the known consumer or
provider modules are already imported. Its patches are process-global, require
exclusive ownership, and its context-local scope does not propagate to other
threads or child processes. A recorded event therefore proves only that this
observer saw that operation; missing events do not prove zero operations.

## Known blind spots

The draft is not a complete hashing observer or gate. It does not cover native
hash object updates or copies, `hashlib.file_digest` internals, `hashlib.new`,
other hashing APIs, previously bound or dynamically created aliases, reads
outside the scoped witness, or subprocesses. It has no global coverage of
transitive package bootstrap imports, dynamic aliases, or process/attempt
inventory. Static inspection cannot rule out import-time calls or alias paths
that were not inspected. Consequently, observed witness calls and
`digest_input_bytes` are scoped measurements, not complete totals or valid
upper-budget inputs.

## Focused attempts and status

Two ordinary focused attempts each reported 6 failures and 22 passes. The
failures came from eager package imports binding the consumer alias before the
observer's deliberate fail-closed installation check, including when the
attempt was launched in a fresh interpreter. The guard was not relaxed. No
conftest skip or bypass was used or proven, and no existing test was changed.
The new observer tests remain unqualified; passing tests do not establish
operation coverage, fixture integration, process/attempt identity, or a
baseline. No complete counts or hashing gate can be claimed from this draft.

The next proof must arrange for the observer to install in a fresh interpreter
before any package import can bind the consumer/provider aliases, while
preserving the fail-closed check and running under the normal test setup. Until
that is demonstrated, treat this as an implementation draft with known
import-order failure, not as a usable count result.
