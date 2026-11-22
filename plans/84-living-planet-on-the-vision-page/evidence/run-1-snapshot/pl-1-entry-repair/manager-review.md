# Entry repair review

2026-11-22T22:13:06.892325+00:00

Causal proof reviewed: warm engine-disabled direct title 1390 ms versus live 6449 ms; constructor 214.8 ms followed by 5211 ms main-thread task, first onReady at 3541.6 ms inside that task. Shared-cache initial probe excluded. Repair addresses readiness ordering, not rendering cost.

Reviewed diff at 7f80225: explicit navigation promise holds expensive visual work until transitions settle; content readiness and cancellable animation-frame paint opportunities before import and initialization; poster remains until first actual frame. Original test was initially rewritten; manager rejected that diff and worker restored it byte-for-byte, adding new tests separately. Independent route N verification pending.

Route N source audit found context-loss poster restoration missing after first frame; this is an explicit early PL-4 requirement and remains open there. No claim that this entry repair completes fallback coverage.
