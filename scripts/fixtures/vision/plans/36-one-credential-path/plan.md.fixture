# One credential path

**Project:** One credential path

**Goal:** Every secret Astrid uses (fal, provider keys, RunPod token) is stored, granted and revoked through the Runtime's credential records, never in plain env files or settings.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** scope agreement

**Vision gaps:** [User control and recovery](../../vision/gaps/F-002-safe-user-control.md) (primary) · [Local-first projects](../../vision/gaps/F-005-local-files-cloud-assist.md) (supporting).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

**Draft; not ready for execution.** Every secret Astrid uses is stored, granted and revoked one way, through the Runtime's credential records (`<data-root>/credentials/`, `controlRemoteCredential`). It is never kept in app-state, preferences, a settings document or a plaintext dotenv file.

## Goal and scope

- **Included (from the 9 Nov audit, code-read and unverified):**
  - `FAL_KEY` (env or an explicit env file; `packs/generation/actions/generate_*/run.py`, `core/util/secrets.py:118-132`);
  - `~/.astrid/astrid.env` (`core/util/secrets.py:54-60`, `credential_store.py:38`);
  - `~/.hermes/.env` plaintext provider keys written by VibeComfy's agent (`vibecomfy/comfy_nodes/agent/provider.py:2746-2790`);
  - the RunPod pod `https-token` file (`packs/runpod/target_selection.py:413-426`);
  - settings that name a credential (`machines.runpod.credential_ref`, compute profiles) keep the name only.
- **To check:** the Codex `auth.json` copy in a run folder (`packs/generation/actions/generate_image_codex/run.py:23-35`) is removed on every exit path, not only on interrupt.
- **Not included:** harness-owned secrets (`~/.codex/auth.json`, OMP's own store), the backup HMAC key, and the paired-connector secret, all of which stay where they are by design.

See [tasks.md](tasks.md) and [inputs.md](inputs.md).

## Completion

Each listed secret is read only through the credential path, has a one-time import from its old location, and the old file is no longer read. A grep finds no provider key read from a plain env file outside that path.
