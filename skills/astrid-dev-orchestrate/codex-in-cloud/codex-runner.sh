#!/usr/bin/env bash
# Keep a Codex run alive while the orchestrator is idle.
# Usage: codex-runner.sh <workdir> <prompt-file> <run-dir> [max-resumes] [model]
# Start detached:  setsid nohup codex-runner.sh ... >/dev/null 2>&1 < /dev/null &
# See README.md next to this file. CODEX_PASS_ENV adds env var names Codex may see
# (comma-separated), e.g. CODEX_PASS_ENV=RUNPOD_API_KEY. Nothing else is passed.
# The prompt must tell Codex to end its final message with a line
#   RUN-STATUS: DONE   or   RUN-STATUS: BLOCKED: <reason>
# Files in <run-dir>: status (running|done|blocked|gave-up), heartbeat, codex.log,
#   result.md (Codex's last message), money.log (RunPod balance + pods, only when
#   RUNPOD_API_KEY is passed; never the key), to-orchestrator.md / to-codex.md (mailbox).
set -u
WD=$1; PROMPT=$2; RUN=$3; MAX=${4:-6}; MODEL=${5:-}
mkdir -p "$RUN"; cd "$WD" || exit 1
echo running > "$RUN/status"; echo $$ > "$RUN/runner.pid"
export PIP_CACHE_DIR=/tmp/codex-pip-cache XDG_CACHE_HOME=/tmp/codex-xdg-cache  # ~/.cache is read-only in the sandbox
NAMES="PATH,HOME,HTTPS_PROXY,HTTP_PROXY,NO_PROXY,SSL_CERT_FILE,REQUESTS_CA_BUNDLE,NODE_EXTRA_CA_CERTS,PIP_CACHE_DIR,XDG_CACHE_HOME${CODEX_PASS_ENV:+,$CODEX_PASS_ENV}"
PASS="[$(echo "$NAMES" | sed 's/[^,][^,]*/"&"/g')]"
FLAGS=(-C "$WD" -s workspace-write
  -c sandbox_workspace_write.network_access=true
  -c 'approval_policy="never"'
  -c "shell_environment_policy.include_only=$PASS"
  -c shell_environment_policy.ignore_default_excludes=true
  -o "$RUN/result.md")
# resume takes no -C/-s: same settings through -c
RFLAGS=(-c 'sandbox_mode="workspace-write"' "${FLAGS[@]:4}")
[ -n "$MODEL" ] && { FLAGS+=(-m "$MODEL"); RFLAGS+=(-m "$MODEL"); }

money() {  # balance and pod ids only; the key never leaves memory
  [ -n "${RUNPOD_API_KEY:-}" ] && [[ ",${CODEX_PASS_ENV:-}," == *",RUNPOD_API_KEY,"* ]] || return 0
  curl -sS -m 20 https://api.runpod.io/graphql -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{"query":"query { myself { clientBalance pods { id name desiredStatus costPerHr } } }"}' \
    | jq -c --arg t "$(date -u +%FT%TZ)" '{t:$t,balance:.data.myself.clientBalance,pods:[.data.myself.pods[]|{id,name,desiredStatus,costPerHr}]}' 2>/dev/null
}
( while kill -0 $$ 2>/dev/null; do date -u +%FT%TZ > "$RUN/heartbeat"
    [ $(( $(date +%s) / 60 % 5 )) -eq 0 ] && money >> "$RUN/money.log"; sleep 60; done ) &

finished() { grep -qE '^RUN-STATUS: (DONE|BLOCKED)' "$RUN/result.md" 2>/dev/null; }
touch "$RUN/to-orchestrator.md" "$RUN/to-codex.md"
MAILBOX="

## Mailbox (talking to the Claude orchestrator)
- To tell or ask the orchestrator something, APPEND a dated note to $RUN/to-orchestrator.md. It is woken within a minute.
- Read $RUN/to-codex.md after every major step and before renting any pod; follow new notes from the orchestrator there.
- If you cannot continue without an answer, append the question to to-orchestrator.md, release or keep pods as is safe (say which), and end your final message with RUN-STATUS: WAITING. You will be resumed with the reply.
- Otherwise end with RUN-STATUS: DONE or RUN-STATUS: BLOCKED: <reason>."
money >> "$RUN/money.log"
echo "=== start $(date -u +%FT%TZ)" >> "$RUN/codex.log"
codex exec "${FLAGS[@]}" "$(cat "$PROMPT")$MAILBOX" >> "$RUN/codex.log" 2>&1
SID=$(grep -m1 -oiE 'session id: [0-9a-f-]{36}' "$RUN/codex.log" | awk '{print $3}')
n=0
waiting() { grep -q '^RUN-STATUS: WAITING' "$RUN/result.md" 2>/dev/null; }
while ! finished && [ "$n" -lt "$MAX" ]; do
  MSG="You were interrupted or stopped before finishing. Re-check pod state first (count before/after, release anything you rented that is not in use), then continue the task from where you left off. End with RUN-STATUS: DONE, BLOCKED: <reason>, or WAITING."
  if waiting; then
    echo waiting > "$RUN/status"; seen=$(wc -c < "$RUN/to-codex.md")
    echo "=== waiting for reply $(date -u +%FT%TZ)" >> "$RUN/codex.log"
    while [ "$(wc -c < "$RUN/to-codex.md")" -le "$seen" ]; do sleep 20; done
    sleep 5; echo running > "$RUN/status"
    MSG="Reply from the orchestrator (also in $RUN/to-codex.md): $(tail -c +$((seen+1)) "$RUN/to-codex.md") — continue the task. End with RUN-STATUS: DONE, BLOCKED: <reason>, or WAITING."
    : > "$RUN/result.md"
  else
    n=$((n+1)); sleep 20
  fi
  echo "=== resume $n $(date -u +%FT%TZ) sid=$SID" >> "$RUN/codex.log"
  if [ -n "$SID" ]; then TARGET=("$SID"); else TARGET=(--last); fi
  codex exec resume "${RFLAGS[@]}" "${TARGET[@]}" \
    "$MSG" \
    >> "$RUN/codex.log" 2>&1
done
money >> "$RUN/money.log"
if grep -q '^RUN-STATUS: DONE' "$RUN/result.md" 2>/dev/null; then echo done > "$RUN/status"
elif grep -q '^RUN-STATUS: BLOCKED' "$RUN/result.md" 2>/dev/null; then echo blocked > "$RUN/status"
else echo gave-up > "$RUN/status"; fi
