"""Lane-brief check: one injected-failure test per contract §5 failure, and the real h3 brief passes."""
import tempfile
import unittest
from pathlib import Path

import checks
from records import is_lane_brief, lane_brief

ROOT = Path(__file__).resolve().parents[1]
RUN_START_UNSET = "# Inputs\n\n**Run start:** Pending — no run is authorized.\n"


def plan_text(status="queued"):
    fields = {"Project": "Fixture", "Goal": "Build one thing", "Status": status,
              "Owner": "Ada", "Estimate": "TBD", "Waiting on": "—"}
    return "# Plan\n\n" + "\n\n".join(f"**{key}:** {value}" for key, value in fields.items()) + "\n"


def release_text(number, lines):
    return (f"# Release {number} — Fixture\n\n**Release:** {number}\n**State:** Draft\n**Kind:** minor\n\n"
            "## Highlight\n\nFixture.\n\n## Intent\n\nFixture.\n\n## Approach\n\nFixture.\n\n"
            f"## Included plans\n\n{lines}\n\n## Publication\n\nFixture.\n")


def brief(lane="alpha", releases="16", state="prepared", go="Pending", rows=(("66-alpha", "16"),),
          option="packets"):
    table = "\n".join(f"| [Plan {folder[:2]}](../../../plans/{folder}/plan.md) | {release} | Now | astrid-dev `main` |"
                      for folder, release in rows)
    return f"""# Lane brief — {lane} fixture

**Lane:** {lane}
**Releases:** {releases}
**State:** {state}; fixture
**Go:** {go}
**Orchestrator:** route X; session not yet started
**Reviewer:** the fixture reviewer
**Board:** `board: lane {lane}`, linked once opened

## Outcome

A fixture lane.

## Plans and order

| Plan | Release | Starts when | Branches |
| --- | --- | --- | --- |
{table}

## Queue

- [Plan 66 execution units](../../../plans/66-alpha/tasks.md)

## How it runs

**Option:** {option}

- **Start.** Open the board, then post one STATUS.
- **Dispatch.** One unit at a time.
- **Proof.** The author runs the focused proof.
- **Reviews.** The reviewer accepts the stops the brief names.
- **Merges.** The orchestrator merges on green.
- **Check-ins.** One STATUS per check-in.

## Roles

- **Orchestrator:** the fixture orchestrator, signing `{lane}-orchestrator`.

## Standing rulings

None yet.

## Context

- **Decisions:** none.

## Cut line and coordination

- **Never slips:** the fixture.

## Owner only

- Scope changes.

## Launch

```text
Follow the astrid-dev-orchestrator skill. Your brief is releases/{releases.split(',')[0]}/briefs/{lane}.md on banodoco/astrid-dev main. Created by session fixture, signing lead.
```

## Status

Read `python3 scripts/astrid_dev.py release status {releases.split(',')[0]}`.
"""


def make_root(root, briefs, included=None, run_starts=None):
    """Write plans, releases and briefs. `briefs` maps root-relative paths to text."""
    included = {16: ["66-alpha", "67-beta"], 17: ["68-gamma"]} if included is None else included
    for folder in ("66-alpha", "67-beta", "68-gamma"):
        target = root / "plans" / folder
        target.mkdir(parents=True, exist_ok=True)
        (target / "plan.md").write_text(plan_text(), encoding="utf-8")
        (target / "inputs.md").write_text((run_starts or {}).get(folder, RUN_START_UNSET), encoding="utf-8")
    for number, folders in included.items():
        lines = "\n".join(f"- [Plan {folder[:2]}](../plans/{folder}/plan.md) — Fixture plan {folder}."
                          for folder in folders) or "None yet"
        (root / "releases").mkdir(exist_ok=True)
        (root / "releases" / f"{number}.md").write_text(release_text(number, lines), encoding="utf-8")
    for relative, text in briefs.items():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def lane_errors(root):
    entry = next(entry for entry in checks.REGISTRY if entry.id == "lane-briefs")
    return entry.run(checks.Context(root))


def assert_reports(testcase, errors, fragments):
    if not any(all(part in line for part in fragments) for line in errors):
        testcase.fail(f"no error containing {fragments!r} in {errors!r}")


class LaneBriefCheckTests(unittest.TestCase):
    def test_registered_once_as_an_always_check(self):
        entries = [entry for entry in checks.REGISTRY if entry.id == "lane-briefs"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].trigger, "always")

    def test_valid_fixture_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_root(root, {"releases/16/briefs/alpha.md": brief()})
            self.assertEqual(lane_errors(root), [])

    def test_failure_1_missing_field_or_placeholder(self):
        good = brief()
        cases = {
            "missing Reviewer header": (good.replace("**Reviewer:** the fixture reviewer\n", ""),
                                        ("header **Reviewer:** is missing",)),
            "placeholder in a header value": (good.replace("route X;", "route <X or S>;"),
                                              ("header **Orchestrator:**", "placeholder")),
            "placeholder in a Plans cell": (good.replace("| 16 | Now |", "| <N> | Now |"),
                                            ("Plans and order", "placeholder")),
            "placeholder in Launch": (good.replace("releases/16/briefs/alpha.md", "releases/<N>/briefs/<lane>.md"),
                                      ("Launch", "placeholder")),
            "missing Option line": (good.replace("**Option:** packets\n", ""),
                                   ("needs an **Option:** line",)),
            "missing Owner only section": (good.replace("## Owner only\n\n- Scope changes.\n\n", ""),
                                           ("section ## Owner only is missing",)),
        }
        for name, (text, fragments) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_root(root, {"releases/16/briefs/alpha.md": text})
                assert_reports(self, lane_errors(root), fragments)
        with self.subTest(case="placeholder in section prose is not scanned"), tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_root(root, {"releases/16/briefs/alpha.md": good.replace("A fixture lane.", "A fixture <lane> prose.")})
            self.assertEqual(lane_errors(root), [])

    def test_failure_2_malformed_header_or_reused_lane(self):
        cases = {
            "Lane differs from the file name": ({"releases/16/briefs/alpha.md": brief().replace("**Lane:** alpha", "**Lane:** beta")},
                                                ("differs from the file name alpha",)),
            "first Releases number differs from the path": ({"releases/16/briefs/alpha.md": brief(releases="17, continuing in 16")},
                                                            ("first **Releases:** number 17 differs",)),
            "State is not a known value": ({"releases/16/briefs/alpha.md": brief(state="started")},
                                           ("must start with prepared, running, paused or done",)),
            "Go is Pending while running": ({"releases/16/briefs/alpha.md": brief(state="running", go="Pending")},
                                            ("Go:** is Pending while State is running",)),
            "lane slug reused under another release": ({"releases/16/briefs/alpha.md": brief(),
                                                        "releases/17/briefs/alpha.md": brief(releases="17", rows=(("68-gamma", "17"),))},
                                                       ("lane alpha is also in",)),
        }
        for name, (briefs, fragments) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_root(root, briefs)
                assert_reports(self, lane_errors(root), fragments)

    def test_failure_3_unknown_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_root(root, {"releases/16/briefs/alpha.md": brief(rows=(("99-missing", "16"),))})
            assert_reports(self, lane_errors(root),
                           ("alpha.md", "does not link an existing plans/<PP>-<slug>/plan.md"))

    def test_failure_4_plan_not_in_the_named_release(self):
        cases = {
            "plan absent from releases/16.md": (brief(rows=(("68-gamma", "16"),), releases="16"),
                                                ("plans/68-gamma/plan.md", "not in releases/16.md ## Included plans")),
            "plan listed for the wrong release": (brief(rows=(("66-alpha", "17"),), releases="16, continuing in 17"),
                                                  ("plans/66-alpha/plan.md", "not in releases/17.md ## Included plans")),
            "release brief does not exist": (brief(rows=(("66-alpha", "18"),), releases="16, continuing in 18"),
                                             ("plans/66-alpha/plan.md", "releases/18.md does not exist")),
        }
        for name, (text, fragments) in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                make_root(root, {"releases/16/briefs/alpha.md": text})
                assert_reports(self, lane_errors(root), fragments)

    def test_failure_5_plan_in_two_active_lanes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_root(root, {"releases/16/briefs/alpha.md": brief(),
                             "releases/16/briefs/beta.md": brief(lane="beta")})
            assert_reports(self, lane_errors(root),
                           ("plans/66-alpha/plan.md", "in more than one active lane brief", "beta.md"))
        with self.subTest(case="a done lane does not hold the plan"), tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_root(root, {"releases/16/briefs/alpha.md": brief(),
                             "releases/16/briefs/beta.md": brief(lane="beta", state="done", go="owner go 1 Dec 2026")})
            self.assertEqual([line for line in lane_errors(root) if "active lane" in line], [])

    def test_failure_6_started_lane_plan_needs_run_start_pointer(self):
        started = brief(state="running", go="owner go 1 Dec 2026")
        with self.subTest(case="no pointer"), tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_root(root, {"releases/16/briefs/alpha.md": started})
            assert_reports(self, lane_errors(root),
                           ("plans/66-alpha/inputs.md", "must link this lane brief", "releases/16/briefs/alpha.md"))
        with self.subTest(case="pointer present"), tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pointer = "**Run start:** Lane [alpha](../../releases/16/briefs/alpha.md): the brief records the go.\n"
            make_root(root, {"releases/16/briefs/alpha.md": started}, run_starts={"66-alpha": pointer})
            self.assertEqual(lane_errors(root), [])

    def test_only_lane_marked_files_under_releases_are_briefs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            make_root(root, {"releases/16/briefs/notes.md": "# Notes\n\nNot a lane brief.\n"})
            self.assertEqual(lane_errors(root), [])
            self.assertEqual(checks._lane_brief_files(root), {})

    def test_real_h3_brief_passes_and_template_is_not_scanned(self):
        self.assertTrue(is_lane_brief((ROOT / "templates/release/lane.md").read_text(encoding="utf-8")))
        briefs = checks._lane_brief_files(ROOT)
        self.assertEqual(list(briefs), ["releases/16/briefs/h3.md"])
        parsed = briefs["releases/16/briefs/h3.md"]
        self.assertEqual((parsed["errors"], parsed["state"], parsed["releases"]), ([], "prepared", [16, 17]))
        self.assertEqual(lane_errors(ROOT), [])


class RunStartPointerTests(unittest.TestCase):
    def dev_only_root(self, root, lane_state, lane_name="alpha"):
        briefs = {f"releases/16/briefs/{lane_name}.md": brief(lane=lane_name, state=lane_state,
                                                              go="owner go 1 Dec 2026" if lane_state != "prepared" else "Pending")}
        make_root(root, briefs, included={16: ["67-beta"], 17: ["68-gamma"]})
        (root / "plans/67-beta/plan.md").write_text(plan_text("active") + "\n**Run route:** astrid-dev-only\n",
                                                    encoding="utf-8")
        (root / "plans/67-beta/inputs.md").write_text(
            f"# Inputs\n\n**Run start:** Lane [{lane_name}](../../releases/16/briefs/{lane_name}.md): the brief records the go.\n",
            encoding="utf-8")

    def active_errors(self, root):
        entry = next(entry for entry in checks.REGISTRY if entry.id == "active-plans-in-releases")
        return entry.run(checks.Context(root))

    def test_astrid_dev_only_plan_accepts_pointer_to_running_lane_brief(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.dev_only_root(root, "running")
            self.assertEqual(checks._catalog(checks.Context(root)), [])
            self.assertEqual(self.active_errors(root), [])

    def test_astrid_dev_only_plan_refuses_pointer_to_prepared_lane_brief(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.dev_only_root(root, "prepared")
            errors = self.active_errors(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("a Run start pointer to a running lane brief", errors[0])


if __name__ == "__main__":
    unittest.main()
