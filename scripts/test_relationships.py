"""Focused tests for the shared read-only relationship contract."""
import unittest

from relationships import RecordRef, Relationship, RelationshipError, RelationshipIndex


G = RecordRef("goal", "pillar:artistic-ambition/finish-a-work")
A = RecordRef("gap", "AA-001")
B = RecordRef("gap", "AA-002")
P = RecordRef("project", "72")
R = RecordRef("release", "15")
I = RecordRef("issue", "123")
S = "vision/gaps/AA-001.md"


def link(source=A, kind="measures", target=G, role="primary", path=S):
    return Relationship(source, kind, target, role, path)


class RelationshipTests(unittest.TestCase):
    def test_canonical_namespaced_identity(self):
        self.assertEqual(str(G), "goal:pillar:artistic-ambition/finish-a-work")
        self.assertEqual({G, RecordRef("goal", G.id)}, {G})
        with self.assertRaisesRegex(RelationshipError, "unknown record kind"):
            RecordRef("widget", "a")
        for value in ("", " AA-001 ", "AA 001", "AA\n001"):
            with self.subTest(value=value), self.assertRaises(RelationshipError):
                RecordRef("gap", value)

    def test_endpoints_roles_and_provenance(self):
        with self.assertRaisesRegex(RelationshipError, "requires gap -> goal"):
            link(source=P)
        with self.assertRaisesRegex(RelationshipError, "invalid role"):
            link(role="included")
        with self.assertRaisesRegex(RelationshipError, "provenance"):
            link(path="../other.md")
        with self.assertRaisesRegex(RelationshipError, "unknown relationship"):
            link(kind="follows")

    def test_deterministic_forward_and_reverse_lookup(self):
        edges = [
            link(source=P, kind="addresses", target=A, path="plans/72/plan.md"),
            link(source=R, kind="includes", target=P, role="included", path="releases/15.md"),
            link(),
        ]
        records = [R, G, A, P]
        one = RelationshipIndex(records, edges)
        two = RelationshipIndex(reversed(records), reversed(edges))
        self.assertEqual(one.relationships, two.relationships)
        self.assertEqual(one.incoming(G, "measures"), (link(),))
        self.assertEqual(one.outgoing(P, "addresses")[0].target, A)
        self.assertEqual(len(one.incoming(P, "includes")), 1)
        self.assertEqual(one.incoming(P, "listed-in"), ())

    def test_duplicates_unknowns_and_missing_primary_fail_closed(self):
        with self.assertRaisesRegex(RelationshipError, "duplicate record identity"):
            RelationshipIndex([A, A], [link()])
        with self.assertRaisesRegex(RelationshipError, "unknown"):
            RelationshipIndex([A], [link()])
        with self.assertRaisesRegex(RelationshipError, "duplicate or contradictory"):
            RelationshipIndex([A, G], [link(), link(role="supporting")])
        with self.assertRaisesRegex(RelationshipError, "one primary"):
            RelationshipIndex([A, G], [link(role="supporting")])
        with self.assertRaisesRegex(RelationshipError, "one primary"):
            RelationshipIndex([A, B, G], [link()])

    def test_primary_per_domain_and_explicit_enabler(self):
        edges = [
            link(),
            link(source=P, kind="addresses", target=A, path="plans/72/plan.md"),
        ]
        self.assertEqual(len(RelationshipIndex([G, A, P], edges).relationships), 2)
        with self.assertRaisesRegex(RelationshipError, "one primary"):
            RelationshipIndex([G, A, P], [link()])
        enabler = RelationshipIndex([G, A, P], [link()], enablers=[P])
        self.assertIn(P, enabler.enablers)
        with self.assertRaisesRegex(RelationshipError, "foundational enabler"):
            RelationshipIndex([G, A], [link()], enablers=[P])

    def test_frozen_issue_release_link(self):
        edge = link(source=I, kind="listed-in", target=R, role="frozen",
                    path="releases/15.md")
        snap = RelationshipIndex([I, R], [edge])
        self.assertEqual(snap.outgoing(I), (edge,))
        with self.assertRaisesRegex(RelationshipError, "invalid role"):
            link(source=I, kind="listed-in", target=R, role="planned")


if __name__ == "__main__":
    unittest.main()
