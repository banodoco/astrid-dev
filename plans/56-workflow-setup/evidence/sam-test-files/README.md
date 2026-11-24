# Fixtures for Plan 56

- `sam-audio-separation.api.json`: the owner's API-format workflow (Load Audio, SAM Audio loader, text separator, two Save Audio nodes). Every card that needs "the SAM fixture" uses this file.
- **The pack:** https://github.com/ethanfel/ComfyUI-SAM-Audio, HEAD `3cfbd03da3019c7252ba13efd5694b1b2ff487e5` on 23 November 2026 (`git ls-remote` and `git clone` work; the GitHub API is refused for other owners in agent sessions). Its UI example is its own `examples/text_separation_workflow.json`.
- **Its three `--no-deps` packages** (from its `install.py`; declared through LE-13, never run from `install.py`):
  - `dacvae @ git+https://github.com/facebookresearch/dacvae.git@414c20785fc3a28373073ea8ef7a1316eeeaca6e`
  - `perception-models @ git+https://github.com/facebookresearch/perception_models.git@e72b6810b1133e1c879f2cc965d276eb73803f1f`
  - `sam-audio @ git+https://github.com/facebookresearch/sam-audio.git@bb4c6999d2677c7402360e426afc01ddfad6dce0`
- **The CPU stand-in target** (used by every "stand-in" proof): no GPU, no model weights. It is a fake ComfyUI HTTP server that answers `object_info` for the classes you give it, plus the "fake pod runner" the plan's cards name (a recorded-answer `git`/`pip`/`nodes restore` runner on a temp tree). It proves node and model readiness, consent, the restore refusal and the doctor check; it never runs SAM. No card builds it up front: the first card that needs it builds it under that area's `tests/.../fixtures` and later cards reuse it. The only real SAM run is WS-L, by the owner.
- Recorded answers (`git ls-remote`, registry and Manager JSON) are created inline in the card that needs them.
