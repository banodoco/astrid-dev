RENDER-FAILURE
Release 15 installed qualification; film failed the requested 1920x1080 check and has a visible editor/output color difference at 3s.
App 7676df48f4104fb8ebe2b19de64dea25b9ec3dc7
Agent dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5; Runtime 686ca695469bda48cd40a70824c4ccef2a137284
VibeComfy 55c3948212d23cf037fae8a4c6faad77d33e7279 (manifest pin; not verified installed)
Motion pack 2379ab54aca522019ff4f869cfdf9375bdb56dfc; PIN/computed digest 75234c10217e67ec0f111a4cb6be4a6252e172a9cd382506498d07ce1d241029
Heavy fixture PASS: 616 clips, 46 shots. Editor open Saved 8.4s on valid repeat.
Two consecutive saves PASS: Saved after 30.315s/32.046s; no banner in either 120s watch; each reload Saved with all 616 clip records and digest identical.
Save 1 page gesture/post/200/saved marks ms: 80100/82819/109822/110927; Runtime CPU mean/peak 267.27/1120 ms/s; peak RSS 7445737472 bytes.
Save 2 marks ms: 73665/76828/105452/106486; CPU mean/peak 285.12/1100 ms/s; peak RSS 7881195520 bytes.
Short image-only: PASS; 87.169s, 48131 bytes, 1.000s, 30 frames, 1920x1080/30fps, full decode; peak RSS 4094920 KiB.
Film-shaped: 970.895s, 27991434 bytes, 195.967s, 5879 frames, 1280x720/30fps, peak RSS 5255823360 bytes.
Film decode, audio and project-declared 1280x720/30fps PASS; requested 1920x1080 dimension check FAIL.
Film visual comparison: editor/output align at 0s/1s, visible color difference at 3s on the same source frame; cause undetermined.
Standard 616: PASS; ~1125.6s, 11108134 bytes, 233.000s, 6990 frames, 1920x1080/30fps, decode/audio/known colors pass.
Standard observed peak RSS 7897412 KiB is a lower bound due sampling gap; editor comparison overlapped render and its load was not quantified.
Evidence: preflight.txt; two-save-evidence-repeat1.jsonl; pack-identity-verification.log; short-render-verification.json; film-render/verify.json and verify-declared.json; film-render/editor-comparisons/report.txt; standard-render/verify.json and process-samples.jsonl.
Cleanup and disk free: pending.
RUN-STATUS: DONE
