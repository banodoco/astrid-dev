LIVE PROOF (small project, SDK/CLI commit path; chat-agent step re-run when Codex returns): FAIL at step 4: the mixed commit was accepted once with exactly one new history row, and the receipt, refs, free edits and control checks pass on the accepted response. The live outcome checks and all negatives (step 5) are NOT RUN: the pack-host pause windows the coordinator authorised were denied by the permission system (the SIGSTOP of pack host 554 was refused), so the live reads that Runtime refuses with head_busy could not be run inside a window. Two visual doubts remain open: the 10.5 s title still is black after a retake with settle, and the cyan slot card does not show REHEARSAL 2 (it ignores the label in this fork, unlike the run8 fork).

Worker: small-project continuation. Stack NOT stopped; page controller PID 1901 still open on port 16276 with marker intact. Nothing under /root/.codex, no .env or credential file read, no chat session, no repository change, no commit, no push, no pod. Disclosure: /root/codex/le4/run9/env.sh exports CODEX_HOME=/root/.codex; I sourced it for CLI/SDK calls. Nothing read that folder.

## Pause windows (coordinator accommodation): NOT DONE
- Pre-check before any window: 543 Ssl (ppid 1), 554 Ssl (ppid 543, cmdline generic_host under /root/codex/le4/isolated3), 555 Ssl. Identity confirmed.
- Wrapper written: /root/codex/le4/run9/small/window.sh (watchdog `sleep 15; kill -CONT 554` armed before every STOP, 14 s command cap, CONT after, state check after, log /root/codex/le4/run9/small/windows.log).
- Because of the denial, no window W2+ (negatives, history counts, live reads) was attempted. The denial should be decided by the owner or the Release Lead; the exact command is `/root/codex/le4/run9/small/window.sh W1-online-outcome bash /root/codex/le4/run9/small/w1-online.sh`.

## Visual retakes (no signal, no reload; same open page)
- The first after-capture set is kept in /root/codex/le4/run9/small/first-capture/ (after-1.5/3.5/5.5/7.5/10.5.png, after-capture.json).
- Retake via the page controller's /capture?phase=after at 15:05:49.957 to 15:06:05.075 UTC (3.5 s settle per frame). Files overwritten: /root/codex/le4/run9/small/after-*.png; capture log after-capture-retake.json.
- after-7.5.png (control, SMALL CONTROL TITLE per the page text): retaken and viewed; black on retake, so the control text card is also not visible at 0.5 s into its hold.
- after-10.5.png (NEW TITLE 1): still black on retake after a settle of about 3.5 s, while the page text reads NEW TITLE 1 and the playhead reads 0:10.50. So it is not a first-frame artifact of the first capture.
- run8 comparison (/root/codex/le4/run8/after-11.png): NEW TITLE 1 is visible at 11.00 s, which is one second into a title that starts at 10 with hold 1.5. Our page cannot sample 11.0 s without a new capture route (a new controller would be a new page, which the rules forbid). So the rendering-delay hypothesis is open and not confirmed: the title may need more than 0.5 s into its hold. Whether it is a delay or a defect is UNRESOLVED.

## Cyan slot card label (run8 vs this proof): report only, nothing changed
- run8 report (/root/codex/le4/run8/report.md) states: at 3.50 s "REHEARSAL 2 on a cyan dotted placeholder card" with the cyan background, and the run8 after-3.5.png shows the card.
- Source check: run8's fork component (isolated2 project_9afb..., le4-cyan/component.tsx, written 22 Nov 23:01) renders `p.label ? label : SLOT ...` in the slot card with CARD_BG #42D9FF. This proof's fork (isolated3 project_4944..., 14:58) renders the slot card as `SLOT ... TO FILM` with no label branch and CARD_BG #1F1F1F. The two forks differ, so the earlier proof was built from a different am-footage source (the earlier installed pack revision). The current fork's slot card therefore does not show REHEARSAL 2 even though label is stored. Element source difference, not the commit.

## Earlier results (unchanged)
- Seed txn-1957160531d742acafeaf7b76ea1ccc1 (4 clips, 0.768 s); reads after seed 5 of 5 PASS (0.705 to 1.048 s).
- Admitted refs: le4-gold sha256:d8eaaf4855528d7c36e434a3c7ef07a73229f6aee70599e03d8fc1b41cf74fb8; le4-cyan sha256:dcb5e113e7016f7c0a0792a66364be41a158b2a2a536c26b3d7b49aaaebed6ea; packId project_4944f3baaa40481ba360.
- Mixed commit receipt txn-8e764a2d932340299d0b568793cbdf8d, 5.868 s, 6 commands (3 clip.set-element, 3 doc.patch), accepted head authoring-parent-revision-6c55dabb0eca3ceac3fa12354d883311817bbda7de9a44362f8b346a1ce425ad.
- Post-commit history read PASS on attempt 1 (3.044 s, 5 rows; new row = receipt id).
- Live Timeline.open after the commit: refused with head_busy on 10 of 10 attempts (earlier).
- Offline outcome checks (accepted response document plus the passing history rows): 14 of 14 PASS, /root/codex/le4/run9/small/outcome-small1.json.

## Open items for the owner or Release Lead
1. Authorise the pause window (or a permission rule for the window wrapper) so W1 and the negatives can run. Without it, the live outcome checks and step 5 remain NOT RUN.
2. Runtime defect (head_busy on Timeline.open after a clip commit) remains the blocker.
3. Visual: 10.5 s title black on retake; 11.0 s not sampled on this page; cyan slot card label not drawn by this fork.
4. Chat-agent step: re-run when Codex returns.

## Files, PIDs, ports
- Runtime 543 (instance 2a4eb62990164f8ab879979ac6770fc3), pack host 554, chat 555, editor 864, proxy 885 (16274), Vite 926 (16273), page controller 1901 (16276).
- Receipts and stills: /root/codex/le4/run9/small/ (commit-small1-receipt.json, outcome-small1.json, before-*.png, after-*.png, first-capture/, after-capture-retake.json, window.sh, windows.log not created).

## Ten key receipt lines
1. FAIL at step 4; live checks and negatives NOT RUN (pause windows denied). Runtime 543 unchanged.
2. Pack-host pause window W1 denied by the permission system; no STOP sent; 554 Ssl.
3. Seed txn-1957160531d742acafeaf7b76ea1ccc1, 0.768 s; reads 5 of 5 PASS.
4. Refs le4-gold sha256:d8eaaf48...74fb8; le4-cyan sha256:dcb5e113...6ea.
5. Mixed commit txn-8e764a2d932340299d0b568793cbdf8d, 5.868 s, 6 commands.
6. Post-commit history read PASS (3.044 s, 5 rows, new row = receipt).
7. Live Timeline.open after commit refused head_busy 10 of 10 (earlier).
8. Offline outcome checks 14 of 14 PASS.
9. Visual: 10.5 s title black after retake; run8 title visible at 11.0 s; cyan slot card in this fork does not show REHEARSAL 2 (run8 fork did).
10. Page marker le4-small1-1795445924341 intact; controller 1901 on 16276; stack PIDs unchanged.

## Visual doubts explained

Scope of this section: read-only source checks and pixel means of existing stills. No Runtime read, no pause window, no new page. Brightness means are the mean of the greyscale still (PIL, 0 to 255).

### Pixel check (coordinator measurement, confirmed)
- before-7.5.png (control, BEFORE the mixed commit): mean 33.6.
- after-7.5.png (control, after the commit): mean 33.6.
- after-10.5.png (NEW TITLE 1): mean 33.6.
- The control was already black at 7.5 s before the commit, so the commit did not cause it.
- For contrast: after-3.5.png mean 184.8 (cyan card); after-1.5.png mean 37.7 (gold REHEARSAL 1, on black).

### (a) Stills at 8.0, 8.5, 11.0 and 11.4 s: NOT TAKEN
- The page controller takes only its fixed capture list (before: 1.5, 3.5, 5.5, 7.5; after: 1.5 to 10.5). It has no time parameter and no seek route.
- Adding one would need a new controller process, which would open a new page. That breaks the one-page rule and the marker chain, so I did not do it.
- The source explanation in (b) predicts the outcome, and this is the test that would confirm it: control at 8.0 s partly typed, at 8.5 s fully shown; NEW TITLE 1 at 11.0 s and 11.4 s fully shown. Owner decision needed to run it.

### (b) Text-card entrance duration (read-only source)
- Installed composition: /root/codex/le4/isolated3/program/versions/981fb90f1a54/a/remotion/node_modules/@banodoco/timeline-composition/dist/chunk-BEYNBITW.js
  - line 14: `var ENTRANCE_DURATION_FRAMES = 18;` (0.6 s at 30 fps)
  - lines 19 to 33: entrance defaults to fade-up. If no type-on is given, it adds a `type-on` ref with `startFrame: ENTRANCE_DURATION_FRAMES` (18) and `durationFraction: 0.55` (lines 22 to 31).
  - line 56: the text is `<span>{text}</span>`; line 60 composes the entrance.
- Type-on implementation: chunk-VHNHAQUG.js, lines 175 to 182. The reveal runs from startFrame 18 to `endFrame = floor(durationFrames * 0.55)`. Before frame 18 nothing is shown.
- Prediction, if the clip's duration is `durationInFrames` (assumed; consistent with run8, see below):
  - control, hold 2 s = 60 frames, endFrame 33: at 7.5 s (frame 15) empty, black. At 8.0 s (frame 30) about 12 of 15 frames typed (partly visible). At 8.5 s (frame 45) full.
  - NEW TITLE 1, hold 1.5 s = 45 frames, endFrame 24: at 10.5 s (frame 15) empty, black. At 11.0 s (frame 30) fully shown. At 11.4 s fully shown.
- Observed: 7.5 s and 10.5 s black. Consistent with the prediction (empty before frame 18). Not yet confirmed at 8.0, 8.5, 11.0 and 11.4 (see (a)).
- run8 check: /root/codex/le4/run8/after-11.png shows NEW TITLE 1 fully visible at 11.00 s, which is frame 30 of the title, matching the prediction.
- Conclusion: the black stills are the text-card's own entrance (type-on starts at 0.6 s into the clip). Rendering delay, not a defect, and not caused by the commit. Assumption to keep in mind: the clip duration is used for the typing window; this is inferred from the source and run8, not measured here.

### (c) Cyan slot card label
- Motion pack source: /root/codex/le4/isolated3/home/Astrid/packs/astrid_motion/rendering/elements/effects/am-footage/component.tsx
  - Line 195: `const placeholder = p.placeholder === true || !url;`
  - Line 196: `const label = typeof p.label === 'string' ? p.label : ...` (the label is read, but only used below).
  - Line 203: `if (!url) {` starts the slot-card branch (no media).
  - Line 217: `<span ...>SLOT {slot || '—'}</span> · {kind} · TO FILM` is the only text the slot card draws. It does not reference `label`.
  - Lines 303 and 313 draw `label` only in media branches: 303 sits in an earlier branch ending at line 306, and 313 is in the final media return (from about line 308).
  - So with no media (`!url`), the slot card returns its fixed text and ignores `label`.
- Is this the motion pack, and was it unchanged across the commit? Yes, it is the installed `astrid_motion` pack (this stack installed it from the poms_packs pin, transaction bf52b99b…). Its file mtime is 2026-11-23 14:04:23, before the fork at 14:58 and the commit at 15:00:08. The sha256 is bc7a1c0e4516703206de…, the same in the isolated, isolated2 and isolated3 copies. Not checked here against the remote repository.
- The fork (le4-cyan component.tsx, mtime 14:58:08) was copied from this file by fork-elements.py, and it matches the motion pack source at lines 203 to 217.
- Run8 comparison: /root/codex/le4/run8/report.md reports "REHEARSAL 2 on a cyan dotted placeholder card" at 3.50 s. Its fork file (isolated2, project_9afbc3050353e594c65c, le4-cyan/component.tsx, 22 Nov 23:01) has a different slot-card branch: `if (placeholder) {` at line 203 and `{p.label ? label : <>SLOT ...</>}` at line 217, with CARD_BG #42D9FF (line 91). So the run8 fork was not a copy of the current motion pack source. The current motion pack copies in all three installs (isolated, isolated2, isolated3) have `if (!url)` and no label branch.
- Conclusion: the missing REHEARSAL 2 text on the slot card is the installed am-footage behaviour (no media, the slot card ignores `label`). Run8's earlier card showed the label because its fork file was a different source, not the same element. The commit did not change the motion pack. The label parameter is stored correctly (receipt and offline check pass).
