# App re-pin candidate — 23 November 2026

The Lead cancelled lane-specific App re-pins. The release manager will generate one App pin at the release freeze; this candidate is a record, not an approved pin or a pull request.

The [unapplied patch](app-repin-candidate-2026-11-23.patch) was generated against App `release/15/main` at `e3dbad64d402724ac5a35fb6447f18e432c64b78`, using Agent `bd94a6e11dd0e9fb5e488e66f349db564a8220a8` and Runtime `53a035ba7c04156dc45aa096f099b4c0224dfb14`. It changes exactly `public/install-manifest.json`, `runtime.lock.json`, `config/astrid-cli-surface/vendor.lock.json`, and the generated `config/astrid-cli-surface/cli-surface.json` (adding Agent's optional `--operations` argument). The manifest release remains 14 and its `required` field is untouched.

The Agent dual-consumer `scripts/regenerate_runtime_pins.py` generated the manifest and Runtime lock. App `scripts/vendor-lock.mjs update config/astrid-cli-surface/vendor.lock.json --producer <Agent checkout>` generated the Agent lock and CLI surface. Both App producer lock checks and `node scripts/installer/pin.mjs --check` passed; the focused installer manifest and release tests passed 24/24. The guard rejected the unbumped candidate. App CI compares against the pull request's base SHA, so a later tuple change after a prior bump would require another increment.

Guard outputs:

- Generated candidate against App `e3dbad64`, still release 14: `install tuple changed (manifest (without release and required)) but release is 14; a tuple change requires release 15 (exactly +1 from 14)`.
- A subsequent tuple change against a hypothetical release-15 base: `install tuple changed (manifest (without release and required)) but release is 15; a tuple change requires release 16 (exactly +1 from 15)`.
- Existing App `release/15/main` at `e3dbad64` against published `origin/main`: `release guard refused: install tuple changed (manifest (without release and required)) but release is 14; a tuple change requires release 15 (exactly +1 from 14)`.

The second case is a controlled hypothetical guard input, not a committed release-15 candidate. The final freeze pin must be regenerated against the then-current landed commits and checked against its actual base.
