# Glossary

One meaning per word; a word with two meanings is two terms. Skills link here.

**owner:** decides a project; her own message in the accountable session alone gives authority. The plan's `Owner:` line names who answers for it and grants no merge right.

**maintainer:** reviews and merges contributors' pull requests.

**contributor:** a person or agent changing astrid-dev.

**orchestrator:** a standing session that plans and starts projects, advises managers, checks in.

**advisor:** the `run.yaml` role that answers blocking questions: the orchestrator, or a fresh high-judgment sub-agent with no stake in the draft.

**planner:** writes a plan and its cards.

**manager:** dispatches tasks, judges reports and keeps `tasks.md` current; normally the accountable agent.

**Codex manager:** a Codex process managing its own sub-agents inside a Claude session; only by choice.

**host:** the Claude session running a Codex manager; it answers for the run.

**accountable agent:** the one agent answering for a run finishing.

**worker:** an agent given one task: a sub-agent or a Codex call.

**helper:** an `N` worker doing bounded reading, edits or checks for a lead.

**lead:** the agent that does a task or review itself, delegating helper work.

**reviewer:** independent of the author, read-only, on an exact commit range.

**project:** work with its own owner, priority and completion proof.

**plan:** a project's `plan.md`.

**project pack:** a project's folder `plans/<NN-name>/`: `plan.md`, `inputs.md`, `tasks.md`.

**product pack:** a capability bundle in Astrid's agent repository.

**phase:** a part of a plan that delivers value alone.

**task:** one assignment in `tasks.md`; its **card** holds outcome, route, scope, dependencies and proof.

**scope:** the paths and contracts a task may change, with their tests.

**task route:** `N`, `X`, `S` or `T`, the capability band a task runs on; `T` is taste.

**manager's route:** the band chosen once per run for the manager itself.

**run:** one authorized execution of a project, begun on its `Run start` line.

**test run:** one execution of tests.

**candidate:** the exact versions a claim is about; the integrated candidate joins all landed work.

**round:** one review of the integrated candidate.

**review stop:** a row (`RS<n>`) reviewing a load-bearing part.

**track:** parallel work.

**gate:** a release's final proof stage.

**release:** a numbered integration across repositories; its **release brief** holds the plan.

**brief:** what an agent is told at its start.

**check:** a rule registered in `scripts/checks.py`.

**view:** a generated page (`scripts/views.py`).

**process ledger:** `docs/ledger/`: one file per friction, idea or fix in astrid-dev.

**decision log:** a manager's append-only list of its own rulings.

**decisions ledger:** calls made while the owner is away, for her to accept or revert.

**Owner decisions:** the `inputs.md` section listing what the owner must decide.

**home:** the one place a rule, term or fact is written.
