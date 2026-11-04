# Astrid development roles

Use the guide that matches the work being done:

- [Plan](astrid-dev-plan/SKILL.md): decide the smallest useful end state and prepare a new project plan.
- [Manage](astrid-dev-manage/SKILL.md): coordinate an accepted plan, route ready work, and maintain run state.
- [Work](astrid-dev-work/SKILL.md): deliver one assigned task and report exact evidence.
- [Advise](astrid-dev-advise/SKILL.md): diagnose a genuine blocker or provide explicitly requested bounded advice.
- [Release](astrid-dev-release/SKILL.md): prepare a scoped release from an accepted candidate and its evidence.

The [shared run contract](astrid-dev-shared/run-contract.md) and [run template](astrid-dev-shared/templates/run.yaml) are the single shared references for model bindings, source identity, proof policy, and review budgets. The role guides link here rather than copy shared mechanics. Install the five role guides and the namespaced shared references with `../sync.sh`. This directory replaces the former vendored Megado skill tree; it is adapted from that tree's task routing, source identity, failure repair, and budget-preservation mechanics, with its broad default gates and duplicated coordinator machinery removed.

This is repository guidance, not a scheduler or authorization. Installing or editing it does not start product work or reset existing run choices, counters, candidate identities, or review budgets.
