Date: 2026-11-17
Kind: issue
Source: the Release 14 Lead, after an owner-requested deep review of Plan 55's meter, 17 November 2026
Resolved by: 2026-11-17-probe-the-yardstick

The Lead merged Agent #359, Plan 55's standing speed meter (LS-2), on a reviewer's verdict of "merge". That reviewer checked that the diff changed no product code, that the hosted run passed, and that no skip was added. It did not trace whether the meter can detect what it exists to detect. An hour later the owner asked for an independent deep review, which graded it C+ as a gate:
- the tolerance lets a 60% slower median through, with dozens of extra sleeps, flushes and commits;
- it misses `Event.wait` and `asyncio.sleep`;
- the harness polls 50 times faster than the product;
- it would fail a genuine improvement, a resident worker.

Every later Plan 55 task proves its speed against this meter. A measuring instrument needs a review that probes it, injecting the failures it must catch, before it is accepted. The Lead workstream does not say so.
