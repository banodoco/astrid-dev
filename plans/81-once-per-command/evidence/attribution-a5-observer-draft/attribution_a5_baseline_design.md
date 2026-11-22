# A-5 independently verified count and stage baseline: blocked design

This is a schema and comparison contract, not an operational gate. The US-2
fixture, real W/I/E traces, counter definitions, independently gathered
observations and a documented baseline are absent. Consequently neither
`attribution_a5_checks.py` nor `attribution_a5_count_policy.py` can by itself
establish required work or qualify a candidate. In particular, free-text
rationales do not prove a stage or count is legitimately absent. Do not wire
these helpers into a passing gate until the independent oracle described below
exists and has been exercised against real operations.

## Required independently controlled baseline

Store a versioned, immutable baseline independently from the candidate under
test. Bind its version and digest to the gate invocation, along with exact
fixture, instrumented product and dependency revisions, executable, route,
seed and target inventory. Baseline updates change the trusted digest under
the run’s existing authority and retain documented evidence. A candidate-supplied policy or rationale cannot
establish this trust. The baseline contains all five groups `same`, `changed`,
`image_same`, `image_changed`, `image_entry`, each with every observed supported
attempt-count case and explicit coverage of the attached W/I/E routes.

Each group and attempt case contains:

- A complete mandatory metric map: `hash_calls`, `hash_bytes`, `yaml_loads`,
  `discovery_occurrences`, and `launcher_starts`. Each metric specifies an
  documented nonnegative integer lower and upper bound and an oracle reference.
  A positive expectation has a strictly positive lower bound; an allowed zero
  must identify independent evidence for the particular operation's absence.
  Never infer a zero or positive expectation from a timing row or rationale.
- A stage map recording positive minimum occurrences for every operation proved
  applicable, with an independent oracle reference. It explicitly addresses
  `SDK admission preflight`, `Remote admission preflight`, and `Workspace
  admission preflight` individually: each is either required with a positive
  minimum or has a verified conditional absence for this exact route and
  attempt case. The three names are not interchangeable.
- Route-specific attempt identities and correlation rules for the task,
  target prompt and independently captured counters. An unknown case, missing
  metric, missing preflight disposition, missing oracle, unverified absence,
  or unmatched receipt fails closed. No baseline values are invented here.

The oracle is a separately versioned, independently measured fixture observation
that proves actual operation execution or the stated conditional absence for
that exact route and attempt case. It must include raw per-process and
per-attempt counts, real operation hooks, source identity and matched receipts;
its evidence must be checked against the independently pinned fixture, not
accepted solely because the candidate says it is verified. The author of a
code change does not measure that change. Validate the oracle by independently
removing or bypassing each expected operation and confirming that the gate
fails; prove conditional absence using the real route. A plausible policy or
an arbitrary trusted callback is not evidence of that validation.

## Comparison and changes

At execution, load the independently pinned baseline and its validated oracle,
reject unknown versions or digest mismatch, then require every sample's exact
group and attempt case. Check mandatory observed metrics and stage rows against
the baseline and correlate them with that process's attempts and receipts.
Reject missing, duplicate, negative or malformed observations. Separately
check the W/S/R/C partition and 10% uncovered-wall bound; report seconds rather
than gate wall ceilings. Keep existing gate and timeline checks unchanged.

For an ordinary ratchet, compare candidate policy against the pinned baseline:
no prior group, attempt case, mandatory metric or required stage may disappear;
no upper count bound may increase; no positive lower bound may become zero;
a changed minimum requires independently verified route/attempt evidence,
including measurements showing when a real optimization lowers it to another
positive value; a required preflight cannot become absent. New groups,
attempt cases, metrics or stages require independently verified evidence and a
documented baseline introduction. A change in fixture or a legitimate removal
of previously required work needs a documented baseline migration within the
run’s existing authority, with both versions and evidence retained and the
existing no-weakening rule observed; it is not an ordinary ratchet. Verify
that the actual gate reads the pinned baseline rather than trusting the
candidate's replacement.

No tests, measurements or qualification were run for this design. Before an
operational gate can exist, obtain the US-2 fixture and final instrumentation,
measure and verify route/attempt evidence independently, record the baseline,
implement the comparison and oracle validation, and run focused adversarial and
real-operation delay proofs after the quiet window. The author of this design
cannot infer the missing counts or valid conditional absences from this tree.

## Counter coverage and self-validation

The current A-2 observer covers only a CLI subset. Direct or native hashing,
already-bound aliases, subprocesses, the daemon and host work are not thereby
observed. Do not label its values as whole-operation totals. Document each
instrumented API and process boundary, the work outside it, and the precise
meaning of every recorded metric. Carry PID and attempt provenance in the
observation side channel, and separate controller, launcher and host counts;
associate each observation with the real route, attempt and matched receipts.
The observation channel itself must be monitored: deleting the event sink or
bypassing an instrumented API must cause the gate to fail closed, not return a
plausible zero.

The YAML instrumentation must avoid double counting nested `yaml.safe_load` and
`yaml.load` calls with a nesting guard, while retaining independent actual loads.
Use the `pack discovery` occurrence rows for the stage that is actually counted.
Count launcher starts at the real `autobootstrap._invoke_launcher` subprocess
boundary, distinguishing connect and up; a generic host event is not a launcher
start. Validate positive known operations and byte counts for hashing, YAML,
launcher and discovery against independent fixture observations. Exercise both
sink deletion and API bypass as adversarial failures. Conditional legitimate
zeros need actual route/attempt trace evidence, including which process was
observed; a free-text rationale is insufficient. Until the missing coverage and
these validations exist, this preparation cannot claim a complete count gate.

`attribution_a5_ratchet.py` prepares a pure comparison to a separately supplied
pinned prior digest and requires references for each introduced group, case,
metric and stage, and for minimum changes. It does not verify those references,
measure an optimization, or establish actual counter and receipt oracles. The
caller must independently validate the evidence and obtain the trusted digest
outside the candidate under test. Synthetic tests cannot qualify a live gate.
