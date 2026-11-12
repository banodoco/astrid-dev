"""Focused, synthetic tests for the plan-completion decision gate."""
import tempfile
import unittest
from pathlib import Path

from check_completion import assess_completion, check_pr, strategy_errors, transitions_to_done
from check_docs import DIVIDER, HEADER

PLAN = ("# Zero-to-first-image\n\n"
        "**Vision gaps:** [Creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).\n\n"
        "## Completion\nA real generated image appears on the timeline with captured recovery evidence.\n")
ENABLER = "# Documentation refactor\n\n**Vision role:** Foundational enabler — no direct gap.\n"
RECEIPT = """## Completion assessment — Plan 20

Evidence: [real task run](https://github.com/banodoco/astrid-agent/actions/runs/123)
Completion: Yes — A real image reached the timeline in the supported environment.
Implementation PRs: https://github.com/banodoco/astrid-agent/pull/123
Integrated candidate: abcdef0123456789abcdef0123456789abcdef01
Unproven: Other inference providers and machines are unqualified.
Routes used: N for the build tasks, S for review.
Gap F-003: Partially evidenced — One complete route works, but not all inference backends or machines.
"""


def catalog(status: str) -> dict[str, str]:
    """The completion gate receives folder-to-status maps, never page text."""
    return {"20-zero-to-first-image": status}


class CompletionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        target = self.root / "plans/20-zero-to-first-image"
        target.mkdir(parents=True)
        (target / "plan.md").write_text(PLAN, encoding="utf-8")

    def test_only_new_done_transition_requires_receipt(self):
        self.assertEqual(transitions_to_done(catalog("active"), catalog("done")),
                         ["20-zero-to-first-image/plan.md"])
        self.assertEqual(transitions_to_done(catalog("done"), catalog("done")), [])
        self.assertEqual(transitions_to_done(catalog("queued"), catalog("active")), [])

    def test_missing_receipt_fails(self):
        issues = check_pr(["20-zero-to-first-image/plan.md"], "", self.root)
        self.assertEqual(len(issues), 1)
        self.assertIn("missing", issues[0])

    def test_missing_linked_gap_fails(self):
        body = """## Completion assessment — Plan 20
Evidence: https://github.com/example/repo/actions/runs/123
Completion: Yes — The plan completion criteria were tested on the reviewed source.
"""
        issues = check_pr(["20-zero-to-first-image/plan.md"], body, self.root)
        self.assertTrue(any("F-003" in issue for issue in issues))

    def test_valid_assessment_passes(self):
        self.assertEqual(check_pr(["20-zero-to-first-image/plan.md"], RECEIPT, self.root), [])

    def test_placeholder_evidence_fails(self):
        body = RECEIPT.replace(
            "[real task run](https://github.com/banodoco/astrid-agent/actions/runs/123)",
            "a run happened")
        self.assertTrue(any("Evidence" in error for error in
                            check_pr(["20-zero-to-first-image/plan.md"], body, self.root)))

    def test_future_project_ids_and_concise_reasons(self):
        future = RECEIPT.replace("Plan 20", "Plan 100").replace(
            "One complete route works, but not all inference backends or machines.",
            "One route works; others are unproven.")
        self.assertEqual(assess_completion("100-later/plan.md", PLAN, future), [])
        placeholder = RECEIPT.replace(
            "One complete route works, but not all inference backends or machines.", "TBD")
        self.assertTrue(any("F-003" in error for error in
                            assess_completion("20-zero-to-first-image/plan.md", PLAN, placeholder)))

    def test_enabler_needs_explicit_no_gap_impact(self):
        self.assertTrue(assess_completion("21-site/plan.md", ENABLER,
                        """## Completion assessment — Plan 21
Evidence: https://github.com/example/repo/pull/4
Completion: Yes — The existing homepage work passes its stated requirements.
Implementation PRs: None — Communication-only project.
Integrated candidate: None — Reviewed documentation and non-code assets.
Unproven: None within the recorded communication deliverable.
"""))
        self.assertEqual(assess_completion("21-site/plan.md", ENABLER,
                         """## Completion assessment — Plan 21
Evidence: https://github.com/example/repo/pull/4
Completion: Yes — The existing homepage work passes its stated requirements.
Implementation PRs: None — Communication-only project.
Integrated candidate: None — Reviewed documentation and non-code assets.
Unproven: None within the recorded communication deliverable.
Gap impact: None — It is a communication deliverable, not proof that a gap was closed.
Routes used: Unknown — Historical run did not record routes.
"""), [])

    def test_completion_requires_cross_repo_review_context(self):
        bad = RECEIPT.replace(
            "Implementation PRs: https://github.com/banodoco/astrid-agent/pull/123\n", "")
        issues = assess_completion("20-zero-to-first-image/plan.md", PLAN, bad)
        self.assertTrue(any("Implementation PRs" in x for x in issues))
        bad = RECEIPT.replace(
            "Integrated candidate: abcdef0123456789abcdef0123456789abcdef01",
            "Integrated candidate: TBD")
        self.assertTrue(any("Integrated candidate" in x for x in
                            assess_completion("20-zero-to-first-image/plan.md", PLAN, bad)))

    def test_new_catalog_during_migration_is_not_transition(self):
        # A new done folder requires an assessment, even without an old catalog.
        required = transitions_to_done({}, catalog("done"))
        self.assertEqual(required, ["20-zero-to-first-image/plan.md"])
        self.assertTrue(any("missing" in error for error in check_pr(required, "", self.root)))

    def test_route_use_is_explicit_but_unknown_is_honest(self):
        line = "Routes used: N for the build tasks, S for review.\n"
        check = lambda r: assess_completion("20-zero-to-first-image/plan.md", PLAN, r)
        missing = RECEIPT.replace(line, "")
        self.assertTrue(any("Routes used" in x for x in check(missing)))
        unknown = RECEIPT.replace(line.strip(),
            "Routes used: Unknown — The agent runtime did not disclose its route.")
        self.assertEqual(check(unknown), [])
        empty_unknown = RECEIPT.replace(line.strip(), "Routes used: Unknown — TBD")
        self.assertTrue(any("route provenance" in x for x in check(empty_unknown)))
        self.assertEqual(check(RECEIPT.replace(line.strip(), "Routes used: S review")), [])
        self.assertEqual(check(RECEIPT.replace(line.strip(), "Routes used: T for the copy pass")), [])
        override = RECEIPT.replace(line.strip(),
            "Routes used: N for builds, X for UR-13n (override: <name>)")
        self.assertEqual(check(override), [])
        linked = RECEIPT.replace(line.strip(),
            "Routes used: https://github.com/banodoco/astrid-dev/pull/9")
        self.assertEqual(check(linked), [])
        vague = RECEIPT.replace(line.strip(), "Routes used: Some models were used")
        self.assertTrue(any("needs a route" in x for x in check(vague)))

    def test_existing_done_is_not_rechecked(self):
        self.assertEqual(check_pr(transitions_to_done(catalog("done"), catalog("done")), "", self.root), [])




class StrategyGateTests(unittest.TestCase):
    def test_completion_without_strategy_update_fails(self):
        self.assertEqual(len(strategy_errors({"plans/index.md", "vision/gaps/F-001-platform-reliability.md"})), 1)

    def test_completion_with_strategy_update_passes(self):
        self.assertEqual(strategy_errors({"plans/index.md", "strategy.md"}), [])


if __name__ == "__main__":
    unittest.main()


class ProjectStatusTests(unittest.TestCase):
    def test_working_tree_always_uses_fields_even_with_a_hand_written_catalog(self):
        from check_completion import project_statuses
        from test_records import ProjectRecordTests as Records
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            Records.write(root, "20-zero-to-first-image", Records.plan(Status="done"))
            (root / "plans/index.md").write_text(
                HEADER + "\n" + DIVIDER + "\n"
                "| Image | Goal | active | Ada | TBD | — | [Plan 20](20-zero-to-first-image/plan.md) |\n",
                encoding="utf-8")
            self.assertEqual(project_statuses(root), {"20-zero-to-first-image": "done"})
            (root / "plans/index.md").write_text("hand-edited page\n", encoding="utf-8")
            self.assertEqual(project_statuses(root), {"20-zero-to-first-image": "done"})

    def test_historical_catalog_fallback_only_before_generated_marker(self):
        from check_completion import project_statuses
        from test_records import ProjectRecordTests as Records
        for status in ("active", "done"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                Records.git(root, "init", "-q")
                Records.git(root, "config", "user.name", "Contract test")
                Records.git(root, "config", "user.email", "contract@example.invalid")
                Records.write(root, "20-zero-to-first-image", PLAN)
                index = root / "plans/index.md"
                index.write_text(HEADER + "\n" + DIVIDER + "\n"
                                 f"| Image | Goal | {status} | Ada | TBD | — | [Plan 20](20-zero-to-first-image/plan.md) |\n",
                                 encoding="utf-8")
                Records.git(root, "add", ".")
                Records.git(root, "commit", "-qm", "old catalog")
                old = Records.git(root, "rev-parse", "HEAD")
                # The current generated page is deliberately stale: fields win.
                Records.write(root, "20-zero-to-first-image", Records.plan(Status="done"))
                index.write_text("<!-- Generated by Astrid Dev view: plan-catalog; sources: plans/*/plan.md. Do not edit. -->\n"
                                 "# Stale page\n", encoding="utf-8")
                Records.git(root, "add", ".")
                Records.git(root, "commit", "-qm", "record catalog")
                generated = Records.git(root, "rev-parse", "HEAD")
                before = project_statuses(root, old)
                self.assertEqual(before, {"20-zero-to-first-image": status})
                self.assertEqual(transitions_to_done(before, project_statuses(root)),
                                 [] if status == "done" else ["20-zero-to-first-image/plan.md"])
                Records.write(root, "20-zero-to-first-image", Records.plan(Status="queued"))
                self.assertEqual(project_statuses(root, generated), {"20-zero-to-first-image": "done"})

    def test_unreadable_base_status_counts_as_not_done(self):
        from check_completion import project_statuses
        from test_records import ProjectRecordTests as Records
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            Records.git(root, "init", "-q")
            Records.git(root, "config", "user.name", "Contract test")
            Records.git(root, "config", "user.email", "contract@example.invalid")
            Records.write(root, "20-zero-to-first-image", Records.plan().replace("**Status:** queued\n", ""))
            # One unreadable record must not discard another project's done status.
            Records.write(root, "21-existing", Records.plan(Status="done"))
            (root / "plans/index.md").write_text(
                "<!-- Generated by Astrid Dev view: plan-catalog; sources: plans/*/plan.md. Do not edit. -->\n", encoding="utf-8")
            Records.git(root, "add", ".")
            Records.git(root, "commit", "-qm", "missing base status")
            base = Records.git(root, "rev-parse", "HEAD")
            Records.write(root, "20-zero-to-first-image", Records.plan(Status="done"))
            self.assertEqual(transitions_to_done(project_statuses(root, base), project_statuses(root)),
                             ["20-zero-to-first-image/plan.md"])


class CompletionRecordIntegrationTests(unittest.TestCase):
    def test_catalog_page_alone_cannot_skip_or_satisfy_completion(self):
        from unittest.mock import patch
        import check_completion as gate
        import checks
        for before, after, completes in (({"20-zero-to-first-image": "active"}, {"20-zero-to-first-image": "done"}, True),
                                         ({"20-zero-to-first-image": "done"}, {"20-zero-to-first-image": "done"}, False),
                                         ({}, {"20-zero-to-first-image": "done"}, True),
                                         ({"20-zero-to-first-image": "active"}, {"20-zero-to-first-image": "active"}, False)):
            with self.subTest(before=before, after=after), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                project = root / "plans/20-zero-to-first-image"
                project.mkdir(parents=True)
                (project / "plan.md").write_text(PLAN, encoding="utf-8")
                (root / "plans/index.md").write_text("arbitrary hand edit\n", encoding="utf-8")
                body = root / "body.txt"
                body.write_text("", encoding="utf-8")
                revisions = []
                def statuses(actual_root, revision=None):
                    self.assertEqual(actual_root, root)
                    self.assertIn(revision, (None, "base"))
                    revisions.append(revision)
                    return before if revision else after
                with patch.object(gate, "project_statuses", side_effect=statuses) as reader, \
                     patch.object(gate, "changed_paths", return_value={"plans/index.md"}):
                    errors = checks._completion_impl(checks.Context(root, "base", body_file=body))
                self.assertEqual(reader.call_count, 2)
                self.assertCountEqual(revisions, ["base", None])
                if completes:
                    self.assertTrue(any("missing '## Completion assessment" in error for error in errors), errors)
                    self.assertIn(gate.strategy_errors({"plans/index.md"})[0], errors)
                else:
                    self.assertEqual(errors, [])
