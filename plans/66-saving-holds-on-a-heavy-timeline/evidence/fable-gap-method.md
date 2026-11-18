# How to find the gap between 4-5 s per save and near-instant

18 Nov. Thinking, not measurement. Builds on `fable-diagnosis-check.md` (same folder). Facts marked "read" I checked in the installed code or `runtime.log`; "reader" = reported by a Haiku reader; "estimate" = my arithmetic, unmeasured. Nothing here was run.

## 1. The frame

Stop asking "which function is slow". Ask "what is the time a function OF". Write a commit as

    time = fixed + passes x document size + history term + edit term

and find the coefficients. A hotspot hunt assumes one large term in one place. The evidence so far points the other way:

- Twelve commits of the same one-clip nudge cost 4086-4399 ms warm, a spread of 7% (read). A cost that steady for a tiny edit is set by the document, not by the edit.
- The provider makes many whole-document passes per commit: deepcopy, serialise, digest, compile, project, each more than once (read, `commit.py:1251` onward).
- Four real fixes each left the total large. That is what removing one pass out of many looks like.

So the working hypothesis is architectural: every commit re-proves the whole document, and the 4 s is the sum of the passes. A hotspot is still possible; one experiment tells them apart (step 1 below), and the profile's shape confirms it:

- Hotspot: one function or stage holds more than half of cumulative time.
- Thousand passes: no stage above about 30%, and when the profile is regrouped by primitive (`copy.deepcopy`, `json.dumps`, hashing, jsonschema, compile) the primitives are large while their callers are many.

Read the cProfile run both ways: by stage and by primitive. Caution: cProfile charges per call, so it inflates deepcopy-heavy code. Trust its ranking of stages, not its absolute numbers; stage spans (section 4) give the true numbers.

One attribution to hold loosely: "96% is the Agent's provider" is true of the span, but the span also contains the Runtime's own port reads called from inside the provider (`port.revision_closure` deep-copies its result; history-object checks on each read scope - reader) and `port.accept` (198-468 ms, read). Some of the 3.8 s may be Runtime code.

## 2. Bisection sequence

All of these write, so they run on a sandbox timeline or a copy of the stack, never on the timeline the owner is viewing. Every number is the median of at least five warm commits, with the first commit after a Runtime start reported separately.

**Step 1 - size.** The same nudge on a one-clip timeline in the same stack.
- Under ~300 ms: the cost is proportional to the document. Hotspot framing is dead; go to step 2.
- Still ~4 s: the cost is fixed or history-bound (history scan, store, something per process). Go to step 3 first.
- In between: read off fixed (the tiny result) and per-document (the difference) and budget each.

**Step 2 - which axis of "document".** Three variants of Almost Ready, one change each: half the clips; the transcripts/pinned documents removed; a fresh duplicate (same document, no history).
- Time follows clips: schema and timing validation per clip.
- Time follows pinned documents: hydrate and word-anchor work.
- The duplicate is much faster: history, not the document.
- Halving anything roughly halves the time: it is passes over the whole closure, and no single stage is to blame.

**Step 3 - which stage, by subtraction.** With the spans from section 4 in place this is a log read. Without them: a `dry_run` commit against the real one (everything except the store accept), then, on a copy only, skip `validate_final_candidate` and `_check_readers` in turn.
- One skip removes more than half: trim that stage, expect a real win.
- Each skip removes 10-25%: confirmed death by passes; trimming yields at best 2x; the remaining lever is what a commit must prove.

Warm against cold is already answered by the log (5116 cold, ~4150 warm, read) and needs no experiment. A no-op commit adds little once step 1 is done.

## 3. The budget

What the person sees is already instant: the edit is applied locally. "Near-instant" is about the badge and the queue:

- One edit: "Saved" within 1 s of the key press.
- A burst of ten: drained within 3 s of the last edit.

That means about 300 ms per commit end to end, or coalescing a burst into one or two commits, and no more than ~100 ms of browser overhead per commit.

Floors if the work were proportional to the edit (estimates):

| Stage | Now | Floor | What the floor assumes |
|---|---|---|---|
| Load + verify base | unknown | ~0 | Head bundle kept in memory keyed by revision id; revisions are immutable, so this is safe |
| Execute command | unknown | ms | Already edit-sized |
| Schema validation | unknown | ms | Only clips the edit touched; the baseline was accepted |
| Timing validation | unknown | 10-100 ms | Only dependants of the moved clip, or a cached compile of the base |
| Build + digest document | unknown | 20-50 ms | One serialise + hash of the changed revision image; unavoidable while a revision is one content-addressed blob |
| Reader check | unknown | ms | Baseline known readable; check the delta |
| Store accept | 200-470 ms (read) | 30-80 ms | One durable write |
| Durable reconciliation | 140-200 ms (read) | ~10 ms | |

Roughly 100-250 ms. Three tiers of change get there:

1. **Trim** duplicate passes: plausibly 4 s to 1.5-2 s. Not the target.
2. **Cache by immutable revision id** across commits (verified bundle, compiled timing, reader verdict of the head): plausibly under 1 s, with no change to what is proved. This is the cheapest large step and should be sized before anything bigger.
3. **Prove the delta, not the document** (baseline accepted, so check only what the edit can affect): the only route to ~300 ms. That changes what a commit has to prove, which is Plan 64's question, not a trim.

Coalescing a burst in the browser is independent of all three and divides the burst cost by up to ten at today's speed.

## 4. Instrumentation (permanent, minimal)

Provider, added to the existing `timings_ms` line (the helper `timing.stage` already exists; only `port_store_accept` uses it - reader):

- `load_base`, `hydrate`, `execute`, `validate_schema`, `validate_timing`, `build_document`, `check_readers`, `prepare_records`.

Same line, as dimensions, so growth is visible without an experiment:

- `timeline_id`, `document_bytes`, `clip_count`, `history_depth`, `rebased` (head differed from base), `first_in_process`.

Browser, one diagnostic line per commit:

- `capture_to_first_send_ms`, `outbox_write_ms`, `outbox_record_bytes`, `queue_length`, `round_trip_ms`, and the server's `handler` echoed back so client-only time is a subtraction.

One alarm is enough: warn when unattributed time (provider_commit minus the sum of its stages) exceeds 20%.

## 5. Not fooling ourselves

- **Predict before fixing.** A fix lands only with a measured "this stage costs X ms" and a stated "after, the total will be Y". #400 was justified from code reading; it missed twice because nobody had measured that those copies were the bulk. The fix was installed (read: `_BasisReader` is in the installed file), so the miss is in the prediction, not the deployment.
- **Installed against source.** Check the installed file, by commit, not by label: this stack's `last-run.json` says "Release 13 (build 2829f180)" (reader) and the astrid-app clone's working tree is not the commit under test (read).
- **Cold against warm.** E1 (5317 ms) was the first commit of the process. The Runtime was restarted again at 12:32:40 (read, `discovery.json`), so the next first commit is cold too. Quote warm medians; report cold separately.
- **One run is an anecdote.** E2 shows ordering held once, with base equal to head on every commit. It says nothing about rebase, two tabs, an agent commit mid-burst, or a reload mid-drain.
- **Fake IndexedDB costs nothing.** Unit tests with a fake store cannot see multi-megabyte structured clones or strict-durability writes. Outbox claims need a real browser with a real-sized document.
- **Profiler bias.** See section 1.
- **Conclusions this casts doubt on:**
  - "#400 removed the deep-copy cost" - it removed some copies; `_commit_timing_validation.py` and `commit.py` still deep-copy the bundle in many places (read).
  - "The provider is the Agent's time" - see section 1.
  - "Each earlier fix was a cause of slow saves" - health-lock contention and the upload size may have been causes of stalls or failures rather than of the steady 4 s; worth restating each fix as "removed X ms from stage Y" or "fixed a stall", from its own before/after.
  - "Correctness is done" (C6).
  - "The gap is server-side" - at a 300 ms commit the browser's own overhead would be the larger part.

## 6. The browser side

Same frame: cost = accesses x record bytes. From the code (read):

- Each queued edit stores three whole documents (`before`, `after`, `displayBasis`).
- Every append and every dispatch reads, deep-clones and rewrites the whole record, queue included, with strict durability.
- Nothing is sent until the queued appends are written.

So "Dirty" time should grow with the square of the burst length, and the gap between commits should shrink as the queue drains - which the log shows (1.39 s falling to 0.40 s, read).

Experiments, in a real browser on a sandbox timeline, with a performance trace:

1. Bursts of 1, 2, 5 and 10 nudges; record key press to first POST. Linear growth means per-edit cost; faster than linear confirms the whole-record rewrite. Subtract the 500 ms debounce (reader).
2. The same bursts on a one-clip timeline. If "Dirty" collapses to about the debounce, it is record bytes and nothing else.
3. In the trace, split the gap between commits into IndexedDB time, clone time, and the reads the editor makes after an accept.

Budget: first send at debounce + 20 ms; under 20 ms between commits. Reachable only by storing a patch plus a base reference per intent instead of documents, one row per intent, and keeping just the head in `accepted`. That also removes most of the stale-row weight. A second whole-document write per edit goes to the separate `astrid.timeline-drafts` store (reader); measure it in the same trace.
