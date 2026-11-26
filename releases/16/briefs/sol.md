# Sol brief: one try per packet

The Lead sends this to one Sol helper (the newest Sol model), once per packet, after posting `SOL {PACKET}` on the plan's board.

```text
You get one try at Release 16 packet {PACKET}: releases/16/packets/{PACKET}.md in banodoco/astrid-dev on main. Its branch is p{PLAN}/{PACKET} in banodoco/{REPO}, PR {PR}, board {BOARD}.
Why you're here: {REASON}
1. Make the packet's Proof command pass, editing only files in its May touch.
2. Merge release/16/plan-{PLAN}'s head into the branch, run the Proof command once in your own sandbox, and push a commit whose last line is: Proof: <the command> — PASS <summary>
3. Post on the board: r16-lead/sol: READY {REPO} {PR} <head sha>
If you can't do it inside May touch, post r16-lead/sol: PARKED {PACKET}: <one-line reason> instead.
Do nothing else.
```
