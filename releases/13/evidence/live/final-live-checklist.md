# Final live repeat checklist (on the frozen head)
- All five cells: t2i, tts, sfx (real clip source: the h3 bicycle video), music, edit (bicycle). Validate each with check.sh plus a look or listen; send samples to Hannah.
- h3: i2v (8 steps), v2v and video-edit with MORE steps (not 1), so prompt adherence can be judged.
- ONE FRESH model download through `fetch-models --apply` on a real HF file (vc-11 manual redirects, the P4.6b apply path end to end). Check sha, no .part left, timing.
- Warm reuse: t2i, then t2i again on the same pod, then edit, with `models.trust_unchanged` ON. Compare W2's phase record against the W1 baseline (13m19s / 4m35s / 4m24s).
- Seed: every `generate … --json` result's top-level `seed_used` equals the requested seed (R4.K).
- Release explicit; census pods plus balance; floor $67.41.
- h3 masks and frames (briefs/h3-frames-masks.md): T1 (frame-0 SSIM vs the input), T2 (temporal edit, frames 0–35 identical), T3 (first frame via a still-clip edit; seam check), T4 (regional mask, outside pixels identical), T5 (brighten at 8 and 20 steps). Dry-run each first; plus h3first's i2v if it ships.
