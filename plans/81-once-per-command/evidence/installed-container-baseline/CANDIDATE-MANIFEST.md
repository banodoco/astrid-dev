# Pinning an installed A/B after arm

An after-arm manifest selects a tuple of four source pins: Agent repository and commit, Runtime repository and commit, VibeComfy repository and commit, plus the lifecycle and other manifest fields required by the installer. Keep the candidate manifest as a distinct file and record its SHA-256 alongside the published manifest, the npm override manifest, and the vc48 fallback manifest.

The installer checks that manifest.vibecomfy.sha matches the VibeComfy revision in the selected Agent source's own pin data. A manifest that changes only the VibeComfy field can fail before installation when the Agent still pins another revision.

For a local qualification route, set the candidate's agent.repo to an isolated scratch clone containing the intended Agent commit. The scratch clone used for this evidence started from release/15/plan-81 at 9c95c680e645335a4a2ea8091f02b88934a2492b; its local pin bump was generated with:

    python scripts/vibecomfy_pin.py 36ea976ffa24ac3ab5b5e48b7b279af7565d5c41 --checkout <VibeComfy checkout at that revision>

The resulting local Agent commit was bc75d6c592e16582fffc5f1ca1a6aa35508c9ddf; its six-file diff is pin-bump.diff. The owner owns the real pin bump when it lands in the plan branch; this scratch clone and local manifest repo path are qualification inputs, not a substitute for that landing.
