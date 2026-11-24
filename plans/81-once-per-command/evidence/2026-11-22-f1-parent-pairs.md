# F-1 parent comparisons — 22 November 2026

Three alternating source-checkout workflow pairs used five fresh processes per arm against the same Runtime and stand-in ComfyUI, under one timing lock. Agent parent `c532bef434323108663cda5f581c20e4ef4aaf61` and candidate `71fe5a09d5604f49455d953f236c169599210b69` ran with Runtime `182311f9d363712c0339254bd27e091d0e18318d` and VibeComfy `799d90f619a6723d0b376b7e77aef09c244a0821`. Each measured process produced a distinct Runtime task and target acknowledgement; all six fixture teardowns returned zero. The timing ends at CLI exit; target acknowledgements are tracked separately.

| Pair | Parent median | Candidate median | Difference |
| --- | ---: | ---: | ---: |
| 1 | 13.764 s | 12.187 s | -1.576 s |
| 2 | 12.480 s | 11.256 s | -1.225 s |
| 3 | 12.690 s | 11.775 s | -0.915 s |

The median difference is -1.225 s (range -1.576 to -0.915); the control medians span 1.283 s. Under the host's comparison rule the timing difference is not distinguishable from noise. The shared container's one-minute load during these samples ranged from 1.67 to 3.63. Raw manifests and receipts are in `/tmp/p81-f1-parent-pair{1,2,3}-{control,candidate}/` on the run host; the script and log are `run/f1-parent-pairs.sh` and `run/f1-parent-pairs.log`. This is a source fixture, not an installed-machine result. The manager reran the four focused tests on the candidate; a separate fresh-process Runtime request count found whole-window handshakes 4→2, health 30→20 and generation settings reads 4→4. These counts include launcher and host activity. The classified, timestamped Runtime request evidence and manifest are at `/tmp/p81-f1-counts-parent/` and `/tmp/p81-f1-counts-candidate/`; both runs produced task and target receipts and clean teardown.
