# Lever doc tests with a small model (18 Nov 2026)

Five creative asks were given to five Haiku agents, each with only the lever document. The agents couldn't run commands. The asks were:
- bridge two clips;
- recast a man and redub a line in a reference voice;
- ControlNet motion onto a cartoon fox;
- exact start, guided end, voice and a late LoRA;
- continue a take while regenerating a mouth, with motion taken from another take and a timed line.

**Round 1** used two documents (a brief and a skill).
- All five chose the right families and the right place, guide and reference ladder. None invented a mode.
- Average confidence was 4.4 out of 10.
- Gaps found:
  - "the last 2 s of a clip" needed the file's length;
  - placing at the end needed arithmetic;
  - how long a placed still lasts;
  - how overlapping edits combine;
  - still versus tracked masks;
  - a mouth change without its audio;
  - no way to time a spoken line in generated time;
  - LoRA id versus file;
  - control types and parameters;
  - size format and the submit command.

**Round 2** used one shorter page, adding end-relative time, timed prompts, what a placement covers and one-line defaults.
- All five structures were correct, including the combined continue.
- Average confidence was 4.2 out of 10, for two reasons. The page had dropped how to set `duration`. And the agents couldn't dry-run, which every one named as what would settle its doubts.
- Remaining gaps were fixed in [skill-draft.md](skill-draft.md):
  - `duration`;
  - `at: end`;
  - a control-parameter example;
  - what a control carries;
  - tags only on references;
  - mask selection.

**Conclusion:** the abstraction is learnable cold. The next test needs a real `describe` and `--dry-run` (CC-2, CC-3, CC-9), using these five asks as the CC-6 cold-read exercise.
