"""The project's lifecycle vocabulary and the requirements for entering it."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Status:
    name: str
    terminal: bool
    meaning: str
    needs: tuple[str, ...] = ()


NAMED_OWNER = "named-owner"
COMPLETION_ASSESSMENT = "completion-assessment"
NEEDS = (NAMED_OWNER, COMPLETION_ASSESSMENT)


STATUSES = (
    Status("queued", False, "planned, not started"),
    Status("active", False, "explicitly started", (NAMED_OWNER,)),
    Status("blocked", False, "known impediment"),
    Status("paused", False, "deliberately stopped"),
    Status("done", True, "accepted completion evidence", (COMPLETION_ASSESSMENT,)),
    Status("cancelled", True, "intentionally abandoned, with reason in the plan"),
)


def names():
    return tuple(status.name for status in STATUSES)


def terminal():
    return tuple(status.name for status in STATUSES if status.terminal)


def phrase():
    values = names()
    return ", ".join(values[:-1]) + " or " + values[-1]


def route_pattern():
    return r"(?i)\b(" + "|".join(re.escape(name) for name in names()) + r")\b"


def requiring(need):
    if need not in NEEDS:
        known = ", ".join(NEEDS)
        raise ValueError(f"unknown lifecycle need {need!r}; known needs: {known}")
    return tuple(status.name for status in STATUSES if need in status.needs)


def definitions():
    return "; ".join(f"`{status.name}` = {status.meaning}" for status in STATUSES) + "."


# Who is responsible for what, level by level. This table is the one statement of it; docs/lifecycle.md is
# generated from it, and the role pages link there instead of restating it. astrid-dev holds every record;
# the product repositories (astrid-agent, astrid-app, astrid-runtime and the others a release lists) hold
# only the branches named here.

FLOW = (
    "Work goes down one start message at a time and comes back one pull request at a time. "
    "The owner decides scope, the lane split, every go and publication. "
    "The Lead runs the release and is the only session that merges into `release/<N>/main`. "
    "A lane orchestrator, or outside a lane a plan's manager, runs its plans and merges into their plan branches. "
    "Workers and chats do one task each and never merge. "
    "Whoever runs a level closes it, and each level's `done` needs the level below it."
)


@dataclass(frozen=True)
class Level:
    name: str
    record: str
    states: str
    opens: str
    runs: str
    merges: str
    closes: str
    branch: str
    checked: str


LEVELS = (
    Level("Release",
          "`releases/<N>.md`: `**State:**` and the `## Branches` table",
          "`Draft`, `Final`; branch rows `open`, `merged`, `published`",
          "the Lead, as release manager, from the template; the owner chooses what it ships",
          "the Lead",
          "the Lead: each ready plan or fix PR into `release/<N>/main`, in landing order",
          "the Lead, after the owner's go to publish: `Final`, rows `published`",
          "`release/<N>/main` in each repository the release changes",
          "`release-documents`; `release_branches.py check <N>`"),
    Level("Lane",
          "`releases/<N>/briefs/<lane>.md`: `**State:**` and `**Go:**`",
          "`prepared`, `running`, `paused`, `done`",
          "the Lead writes the brief after the owner chooses the split; the owner records the go and sends the launch",
          "its orchestrator, the accountable agent for every plan in it",
          "its orchestrator: unit PRs into its plan branches, and its own progress PRs",
          "its orchestrator, once every plan is `done`: State `done`, manager stopped, check-in cancelled, closing note to the Lead",
          "none of its own; its plans' branches",
          "`lane-briefs`: a `done` lane's plans are `done` or `cancelled`"),
    Level("Plan",
          "`plans/<PP>-<slug>/plan.md`: `**Status:**` and `**Owner:**`",
          ", ".join(f"`{status.name}`" for status in STATUSES),
          "a scope PR the owner greenlights; `active` when its accountable agent starts it",
          "its accountable agent: the lane orchestrator in a lane, otherwise its manager",
          "its accountable agent: task PRs into the plan branch; then it makes the plan ready and opens its PR into `release/<N>/main`, which the Lead merges",
          "its accountable agent opens the completion PR once the Lead has merged it; `done` when that PR merges after independent review",
          "`release/<N>/plan-<PP>` in each repository it changes; `project/<PP>-<slug>` for an astrid-dev-only plan",
          "`plan-catalog`, `completion-assessment`, `project-planning-evidence`, `active-plans-in-releases`"),
    Level("Task",
          "one row of `plans/<PP>-<slug>/tasks.md`: its Progress cell",
          "`[ ]`; `[x]` with its merge; or a disposition such as `blocked: <reason>`",
          "its plan's accountable agent, by a start message ([start-session](../agent/shared/workstreams/start-session.md#procedure) step 7)",
          "one worker: a worker session, a subagent or a ChatGPT chat",
          "its plan's accountable agent, into the plan branch, after re-running the focused proof",
          "whoever merged it ticks it in its next progress PR; a worker never edits `tasks.md`",
          "`p<PP>/<id>`, cut from the plan branch, with its PR into it",
          "none: a tick is a recorded tick, which `release status` reports"),
)


def responsibility_page() -> str:
    columns = ("Level", "Record", "States", "Opened by", "Run by", "Merges", "Closed by", "Branch", "Checked by")
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for level in LEVELS:
        rows.append("| " + " | ".join((f"**{level.name}**", level.record, level.states, level.opens, level.runs,
                                        level.merges, level.closes, level.branch, level.checked)) + " |")
    return ("# Who is responsible for what\n\n" + FLOW + "\n\n" + "\n".join(rows) + "\n\n"
            "Defined in `scripts/lifecycle.py`. Change it there, then run `python3 scripts/astrid_dev.py views generate`.\n")
