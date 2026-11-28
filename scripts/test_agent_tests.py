"""Agent-test module: case parsing, validation, prompts, results, registry and CLI on the real repository."""
import contextlib
import io
import tempfile
import time
import unittest
from pathlib import Path

import agent_tests
import astrid_dev
import checks

ROOT = Path(__file__).resolve().parents[1]

FRONT = """---
id: {id}
role: lane orchestrator, launched by the owner
covers:
  - agent/roles/orchestrator.md
brief: releases/16/brief.md
host: claude-cloud
actor: N
---
"""

BODY = """
# A sample first hour

## Given

Start the lane from the board named in the brief.

## Fixture

- The board exists and is empty.

## Expect

- The session posts a STATUS line on the board.

## Must not

- The session pushes to main.

## Ask the owner

- Does the lane start on the board?
"""


def make_root(tmp):
    root = Path(tmp)
    (root / "agent/roles").mkdir(parents=True)
    (root / "agent/roles/orchestrator.md").write_text("# Orchestrator\n\nRole text.\n", encoding="utf-8")
    (root / "releases/16").mkdir(parents=True)
    (root / "releases/16/brief.md").write_text("# Brief\n", encoding="utf-8")
    (root / agent_tests.CASES_DIR).mkdir(parents=True)
    return root


def write_case(root, id="sample-case", front=None, body=None):
    text = (front if front is not None else FRONT.format(id=id)) + (body if body is not None else BODY)
    path = root / agent_tests.CASES_DIR / f"{id}.md"
    path.write_text(text, encoding="utf-8")
    return path


def errors_for(**kwargs):
    """Write one case (file name from kwargs.pop('name', 'sample-case')) into a fresh repo; return validate()."""
    name = kwargs.pop("name", "sample-case")
    with tempfile.TemporaryDirectory() as tmp:
        root = make_root(tmp)
        write_case(root, name, **kwargs)
        return agent_tests.validate(root)


class ParseTests(unittest.TestCase):
    def test_valid_case_file_parses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            path = write_case(root, front=FRONT.format(id="sample-case").replace("actor: N\n", ""))
            case = agent_tests.parse_case(root, path)
            self.assertEqual(case.id, "sample-case")
            self.assertEqual(case.role, "lane orchestrator, launched by the owner")
            self.assertEqual(case.host, "claude-cloud")
            self.assertEqual(case.covers, ["agent/roles/orchestrator.md"])
            self.assertEqual(case.brief, "releases/16/brief.md")
            self.assertIsNone(case.after)
            self.assertEqual(case.actor, "N")  # default when the actor field is omitted
            self.assertEqual(case.title, "A sample first hour")
            self.assertEqual(case.lines("Expect"), ["The session posts a STATUS line on the board."])
            self.assertEqual(case.lines("Must not"), ["The session pushes to main."])
            self.assertIn("Start the lane", case.sections["Given"])


class ValidateTests(unittest.TestCase):
    def test_valid_case_has_no_errors(self):
        self.assertEqual(errors_for(), [])

    def test_id_must_equal_file_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root, "other-name", front=FRONT.format(id="sample-case"))
            errors = agent_tests.validate(root)
            self.assertTrue(any("id must equal the file name" in e for e in errors), errors)

    def test_unknown_field_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root, front=FRONT.format(id="sample-case").replace("actor: N\n", "actor: N\ncolour: red\n"))
            errors = agent_tests.validate(root)
            self.assertTrue(any("unknown fields" in e and "colour" in e for e in errors), errors)

    def test_unknown_host_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root, front=FRONT.format(id="sample-case").replace("claude-cloud", "mainframe"))
            errors = agent_tests.validate(root)
            self.assertTrue(any("host must be one of" in e for e in errors), errors)

    def test_actor_must_be_n_x_or_s(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root, front=FRONT.format(id="sample-case").replace("actor: N", "actor: Q"))
            errors = agent_tests.validate(root)
            self.assertTrue(any("actor must be a route" in e for e in errors), errors)

    def test_missing_given_is_an_error(self):
        errors = errors_for(body=BODY.replace("## Given\n\nStart the lane from the board named in the brief.\n\n", ""))
        self.assertTrue(any("'## Given' is missing or empty" in e for e in errors), errors)

    def test_empty_expect_is_an_error(self):
        errors = errors_for(body=BODY.replace("- The session posts a STATUS line on the board.", "No bullet here."))
        self.assertTrue(any("'## Expect' needs at least one '- ' line" in e for e in errors), errors)

    def test_unknown_section_is_an_error(self):
        errors = errors_for(body=BODY + "\n## Notes\n\nExtra.\n")
        self.assertTrue(any("unknown sections" in e and "Notes" in e for e in errors), errors)

    def test_covered_file_must_exist(self):
        errors = errors_for(front=FRONT.format(id="sample-case").replace(
            "agent/roles/orchestrator.md", "agent/roles/missing.md"))
        self.assertTrue(any("covered file does not exist: agent/roles/missing.md" in e for e in errors), errors)

    def test_brief_must_exist(self):
        errors = errors_for(front=FRONT.format(id="sample-case").replace(
            "releases/16/brief.md", "releases/16/nope.md"))
        self.assertTrue(any("covered file does not exist: releases/16/nope.md" in e for e in errors), errors)

    def test_after_must_name_a_known_case(self):
        errors = errors_for(front=FRONT.format(id="sample-case").replace("actor: N\n", "actor: N\nafter: ghost\n"))
        self.assertTrue(any("after names an unknown case: ghost" in e for e in errors), errors)

    def test_after_cycle_of_two_cases_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root, "case-a", front=FRONT.format(id="case-a").replace("actor: N\n", "actor: N\nafter: case-b\n"))
            write_case(root, "case-b", front=FRONT.format(id="case-b").replace("actor: N\n", "actor: N\nafter: case-a\n"))
            errors = agent_tests.validate(root)
            self.assertTrue(any("forms a cycle" in e for e in errors), errors)

    def test_upstream_placeholder_without_after_is_an_error(self):
        errors = errors_for(body=BODY.replace("Start the lane from the board named in the brief.",
                                              "Start the lane. Upstream said: {upstream}"))
        self.assertTrue(any("uses {upstream} but the case names no 'after' case" in e for e in errors), errors)

    def test_result_for_unknown_case_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root)
            (root / agent_tests.RESULTS_DIR).mkdir(parents=True)
            (root / agent_tests.RESULTS_DIR / "ghost.md").write_text("# Result — ghost\n", encoding="utf-8")
            errors = agent_tests.validate(root)
            self.assertTrue(any("result for an unknown case" in e and "ghost.md" in e for e in errors), errors)


class PromptTests(unittest.TestCase):
    EXPECT = "- EXPECTLINE-ALPHA the session posts its status."
    MUST_NOT = "- MUSTNOTLINE-BETA the session pushes to main."

    def case_with_marked_lines(self, root, id="sample-case", given="Begin with the lane skill. GIVENMARK-ONE"):
        body = BODY.replace("Start the lane from the board named in the brief.", given)
        body = body.replace("- The session posts a STATUS line on the board.", self.EXPECT)
        body = body.replace("- The session pushes to main.", self.MUST_NOT)
        path = write_case(root, id, body=body)
        return agent_tests.parse_case(root, path)

    def test_actor_prompt_hides_expectations_and_has_given_and_host(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            case = self.case_with_marked_lines(root)
            prompt = agent_tests.actor_prompt(root, case, "/checkout/astrid-dev")
            self.assertNotIn("EXPECTLINE-ALPHA", prompt)
            self.assertNotIn("MUSTNOTLINE-BETA", prompt)
            self.assertNotIn("posts a STATUS line", prompt)
            self.assertNotIn("pushes to main", prompt)
            self.assertIn("GIVENMARK-ONE", prompt)
            self.assertIn(agent_tests.HOST_LINES["claude-cloud"], prompt)
            self.assertIn("/checkout/astrid-dev", prompt)

    def test_chained_case_without_upstream_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root, "case-first")
            path = write_case(root, "case-second",
                              front=FRONT.format(id="case-second").replace("actor: N\n", "actor: N\nafter: case-first\n"),
                              body=BODY.replace("Start the lane from the board named in the brief.",
                                                "Continue from {upstream}"))
            case = agent_tests.parse_case(root, path)
            with self.assertRaises(ValueError):
                agent_tests.actor_prompt(root, case, "/checkout")

    def test_chained_case_with_upstream_replaces_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root, "case-first")
            path = write_case(root, "case-second",
                              front=FRONT.format(id="case-second").replace("actor: N\n", "actor: N\nafter: case-first\n"),
                              body=BODY.replace("Start the lane from the board named in the brief.",
                                                "Continue from {upstream} now."))
            case = agent_tests.parse_case(root, path)
            prompt = agent_tests.actor_prompt(root, case, "/checkout", upstream="UPSTREAM-OUTPUT-GAMMA\n")
            self.assertIn("Continue from UPSTREAM-OUTPUT-GAMMA now.", prompt)
            self.assertNotIn("{upstream}", prompt)

    def test_judge_prompt_numbers_lines_and_includes_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            body = BODY.replace("- The session posts a STATUS line on the board.",
                                "- FIRSTEXPECT\n- SECONDEXPECT")
            body = body.replace("- The session pushes to main.", "- FIRSTMUST\n- SECONDMUST")
            case = agent_tests.parse_case(root, write_case(root, body=body))
            prompt = agent_tests.judge_prompt(case, "REPORT-BODY-DELTA\n", "/checkout")
            self.assertIn("E1. FIRSTEXPECT", prompt)
            self.assertIn("E2. SECONDEXPECT", prompt)
            self.assertIn("M1. FIRSTMUST", prompt)
            self.assertIn("M2. SECONDMUST", prompt)
            self.assertIn("REPORT-BODY-DELTA", prompt)
            self.assertIn("VERDICT: pass", prompt)


class RecordStatusTests(unittest.TestCase):
    VERDICT = "E1. met. Evidence quoted.\n\nVERDICT: pass (every line met)\n"

    def test_record_writes_verdict_and_inputs_then_status_reports_pass_then_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            case = agent_tests.parse_case(root, write_case(root))
            out = agent_tests.record(root, case, self.VERDICT, "test-actor-model", "test-judge-model",
                                     today="2026-01-02")
            self.assertEqual(out, root / agent_tests.RESULTS_DIR / "sample-case.md")
            text = out.read_text(encoding="utf-8")
            self.assertIn("**Verdict:** pass", text)
            self.assertIn("**Inputs:**", text)
            self.assertIn("`agent/roles/orchestrator.md`", text)
            self.assertIn("`releases/16/brief.md`", text)
            self.assertIn("VERDICT: pass", text)
            self.assertEqual(agent_tests.status(root), [("sample-case", "pass")])

            time.sleep(0.01)
            (root / "agent/roles/orchestrator.md").write_text("# Orchestrator\n\nChanged role text.\n", encoding="utf-8")
            self.assertEqual(agent_tests.status(root), [("sample-case", "stale")])

    def test_record_without_verdict_line_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            case = agent_tests.parse_case(root, write_case(root))
            with self.assertRaises(ValueError):
                agent_tests.record(root, case, "E1. met.\nNo verdict here.\n", "a", "j", today="2026-01-02")
            self.assertFalse((root / agent_tests.RESULTS_DIR / "sample-case.md").exists())

    def test_case_without_result_reports_never_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            write_case(root)
            self.assertEqual(agent_tests.status(root), [("sample-case", "never run")])


class RegistryTests(unittest.TestCase):
    def test_registry_has_one_always_agent_tests_check_that_passes_on_real_repo(self):
        matches = [check for check in checks.REGISTRY if check.id == "agent-tests"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].trigger, "always")
        self.assertEqual(matches[0].run(checks.Context(root=ROOT)), [])


class RealRepositoryTests(unittest.TestCase):
    def test_coverage_uncovered_entries_are_agent_markdown_paths(self):
        by_doc, uncovered = agent_tests.coverage(ROOT)
        self.assertIsInstance(by_doc, dict)
        self.assertIsInstance(uncovered, list)
        for path in uncovered:
            self.assertTrue(path.startswith("agent/"), path)
            self.assertTrue(path.endswith(".md"), path)

    def test_cli_agent_test_list_exits_zero_on_real_repo(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = astrid_dev.main(["agent-test", "list"], root=ROOT)
        self.assertEqual(code, 0)
        self.assertNotIn("ERROR", output.getvalue())


if __name__ == "__main__":
    unittest.main()
