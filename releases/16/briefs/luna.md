# Luna brief: the plan loop

The Lead sends this every hour to one Luna helper per active plan (the newest Luna model), with `{PLAN}`, `{BOARD}` and `{LAST}` (that plan's last result line from the Lead's STATUS, or `none`) filled in. The Luna's final reply is one line.

```text
You are running one check of the Release 16 plan loop for Plan {PLAN}, board {BOARD}. Use only the commands in the command table of releases/16/run.md (banodoco/astrid-dev, main, section "Delivery: Lead and managers"). Do only these steps, then reply with one line.
1. Your last result line was: {LAST}. Read the board's comments after its cursor (0 if none). Skip any READY that already has a DONE or REWORK after it. For each packet you handle, read releases/16/packets/<packet>.md for its May touch, Must not touch and Proof.
2. For each READY <repo> <PR> <head>, check:
   a. every file the PR changes is in May touch, and none is in Must not touch;
   b. the head commit's last line is "Proof: <the packet's Proof command> — PASS ...";
   c. the PR merges cleanly into release/16/plan-{PLAN}.
   All three hold: merge the PR, and post DONE <packet> <merge sha>.
   Otherwise count that packet's REWORK and SOL comments on the board:
   - fewer than 2 REWORKs and no SOL: post REWORK <n> of 2 for <packet>: <the check that failed, in one line>;
   - 2 REWORKs and no SOL: flag SOL <packet>: <the check that failed>;
   - a SOL already: post PARKED <packet>: failed after Sol.
3. Each BLOCKED <packet>: flag SOL <packet>: <its reason>, unless the board has a SOL for it; then post PARKED <packet>: <its reason>.
4. A SOL comment over 2 hours old with no READY after it: post PARKED <packet>: Sol didn't finish.
5. Each PARKED packet: post PARKED <packet>: depends on <parked packet> for every queued packet whose Depends includes it.
6. If the manager posted NO-CHATS since your cursor, flag NO-CHATS {PLAN}.
7. The manager's last STATUS is over 2 hours old: post "r16-lead: Check-in missed. Run your loop now and post STATUS." unless your last result line says manager nudged; then flag REPLACE manager {PLAN}.
8. Every packet in the Plan {PLAN} queue is Done or Parked: flag FINISHED {PLAN}.
Reply exactly: plan {PLAN}: queued <n> running <n> ready <n> done <n> parked <n> manager <ok|nudged> | flags: <list or none> | cursor: <last comment id you read>
Never run tests, read code, or write anything but the comments above.
```
