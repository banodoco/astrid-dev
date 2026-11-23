# Plan 73 — independent fresh-agent and real client verification protocol

**Status:** execution packet prepared, **not executed**. Keep this evaluator protocol **out of the fresh-agent brief and context** until the attempt is complete. The independent actor receives only [the short assignment](ms10-fresh-agent-assignment-20261123.md), the original staged `agent/README.md` in a disposable checkout, and exact sandbox/authority boundaries.

## Proctor preflight

1. Identify an agent with a **fresh session** that did not author, review, rehearse or receive findings from Plan 73 MS4–MS11. Record the observed product, account/session identity (non-secret ID), actual model and effort, start time, tool permissions, and whether the agent has been exposed to prior project context. If independence cannot be established, log it as a rehearsal, not a fresh-agent result.
2. Supply an isolated clean checkout at a **verified full Git SHA**. Record `git rev-parse HEAD`, `git status --porcelain`, parent branch and which original tracked files existed. Old authored `skills/` remain authoritative; do not give the agent permission to write them, real homes, other repos, release branches, or main.
3. Supply **separately created disposable skill destinations** and authorized client installations. Do not copy credentials or authentication caches; if interactive login is necessary, the authorized owner performs it directly without recording tokens. Use a sandbox/VM whose home and user scope are dedicated to this experiment.
4. Hand the actor exactly the **Assignment** document. Do not send examples, target filename, earlier scripts, output expectations, failure screenshots, or the evaluation rubric. Preserve the complete uncoached task/chat transcript and the final agent-authored work.

## Reproducible filesystem and client preparation

From a fresh isolated Linux/macOS VM or other supported host, not a production checkout:

```sh
export SOURCE_SHA="<verified-40-character-commit>"
export SCRATCH="$(mktemp -d)"
git clone https://github.com/banodoco/astrid-dev.git "$SCRATCH/astrid-dev"
cd "$SCRATCH/astrid-dev"
git checkout --detach "$SOURCE_SHA"
test "$(git rev-parse HEAD)" = "$SOURCE_SHA"
git status --porcelain
python3 scripts/astrid_dev.py skills build
python3 scripts/astrid_dev.py skills check
mkdir -p "$SCRATCH/home/.agents/skills" "$SCRATCH/home/.claude/skills"
python3 scripts/astrid_dev.py skills install --dry-run --destination "$SCRATCH/home/.agents/skills"
python3 scripts/astrid_dev.py skills install --dry-run --destination "$SCRATCH/home/.claude/skills"
```

The *actor* should decide how to use the README. This setup shows the proctor which directories to provision, not a step-by-step answer to give the actor. After the actor creates its workstream, repeat build/check and install in those disposable destinations. For each client, **ensure the actual client uses that disposable user home or explicitly supported repository skill root**. A `HOME` override may also hide that client's login, so use a dedicated sandbox login or authorized ephemeral session rather than reusing any personal credential directory.

## Actual client discovery — two distinct receipts per client

**Codex CLI** (current official [skill guidance](https://learn.chatgpt.com/docs/build-skills)): record `codex --version` and availability of the tool on the tested host. Codex's published user skill root is `$HOME/.agents/skills` and its interactive selector is `/skills`; an explicit skill mention uses `$astrid-dev-<actual-stem>`. Start a *fresh* Codex session from the intended checkout and an isolated home, demonstrate that the newly generated name appears in the selector **and** explicitly invoke it. Capture its tool trace reading the installed `SKILL.md`, the relative source reference and actual answer. Merely having a symlink and reading it with `cat` is not a client-discovery PASS.

**Claude Code** (current official [skill guidance](https://code.claude.com/docs/en/skills)): record `claude --version` and the tested host/permissions. The published user skill root is `$HOME/.claude/skills`; an explicit invocation uses `/astrid-dev-<actual-stem>`. Launch a fresh Claude Code session in the isolated home; show the new name listed as an available skill or accepted by the command interface, explicitly invoke it, and capture evidence of full instructions being loaded and followed. If this version uses a different supported display/invocation mechanism, capture `claude --help` or the relevant official client documentation and use the verified mechanism, not guesswork.

For **each tested client**, separately record a natural-language request that matches the new skill description but **does not** mention the skill by name; capture whether it was selected implicitly. An implicit miss does not invalidate an explicit discovery PASS, but must be disclosed. Record NO-RESULT for uninstalled/uncredentialed or unsupported clients and Windows/macOS if not actually run.

## Retirement and isolation proof

Once the actor disables its chosen source's `skill: true`, run `skills build`, `skills check` and `skills install --destination` for every disposable skill root again. **Restart** or refresh the real client according to its documented discovery policy; verify the retired skill is no longer available in its skill selector, while original skills remain. Keep one unrelated foreign test entry in each destination and compare its bytes before/after. Check that the agent's authored plain Markdown source remains and that `git status` changes are restricted to permitted disposable paths.

## Evaluator checklist (do not give to actor in advance)

- Recorded independent session identity, model/effort, prior-context isolation, precise host OS and reproducible source SHA
- Actor demonstrably read the staged README without receiving a bespoke implementation recipe
- Valid independently chosen `.md` workstream and `skill: true`, with mandatory headings and original skills preserved
- Actual successful build/check, no surprise generated writes, valid install/dry-run and repeat idempotence
- Actual **client selector/skill invocation** and instruction loading for each claimed client; no false inference from filesystem links
- Accepted foreign preservation and clean opt-out retirement; old authoritative `skills/` untouched
- Friction, failure, attempts, tool limits, network/authorization observations and raw exits retained
- An independent reviewer—not the author or proctor—adjudicates the result under existing review and round limits; **never auto-upgrade an unexecuted or scripted rehearsal to ACCEPT**

## Evidence template

```text
SOURCE_SHA:
HOST_OS / OS_VERSION:
CLIENT / VERSION / MODEL / EFFORT:
NEW_AGENT_SESSION_ID (non-secret):
PRIOR_CONTEXT_EXPOSURE:
STARTED_UTC / COMPLETED_UTC:
DISPOSABLE_CHECKOUT:
DISPOSABLE_SKILL_ROOT:
AGENT_RAW_TRANSCRIPT:
AGENT_AUTHORED_DIFF:
BUILD_CHECK_INSTALL_LOGS:
ACTUAL_CLIENT_SKILL_LIST:
EXPLICIT_INVOCATION_AND_SKILL_READ_TRACE:
IMPLICIT_MATCH_RESULT:
RETIREMENT_AND_FOREIGN_ENTRY_RECEIPTS:
ORIGINAL_GIT_STATUS_BEFORE_AND_AFTER:
RESULTS (PASS / FAIL / NO-RESULT for each):
FRICTION_AND_UNRESOLVED_LIMITS:
INDEPENDENT_EVALUATOR_ID_AND_VERDICT (only when actually completed):
```

Do not store secrets in GitHub artifacts. No reviewer may claim a platform, app or permissions level not present in the original trace.

**Current Plan 73 state:** fresh-agent and real client discovery are NO-RESULT. The original RS1 technical verdict remains BLOCK; six bounded remediation rulings are not a new RS1 review or final R. D5/MS7/MS9/MS11 and owner-approved main merge remain gated.
