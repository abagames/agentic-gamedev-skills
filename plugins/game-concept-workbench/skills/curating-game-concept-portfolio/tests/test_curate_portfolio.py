import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).parents[1] / "scripts" / "curate_portfolio.py"
spec = importlib.util.spec_from_file_location("curate_portfolio", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def concept(cid, op, progress, risk, evidence=None, hard=False, extra=None):
    signature = {
        "primary_operation": op,
        "progress_conversion": progress,
        "risk_coupling": risk,
        "time_model": "turn",
    }
    if extra:
        signature.update(extra)
    record = {
        "id": cid,
        "hard_reject": hard,
        "signature": signature,
        "evidence_scores": evidence or {},
    }
    if hard:
        record["hard_reject_reason"] = "Demonstrated unreachable core goal."
        record["hard_reject_evidence"] = {
            "type": "state_trace",
            "provenance": "fixture trace t-hard-01",
        }
    return record


class CuratePortfolioTests(unittest.TestCase):
    def test_identical_signature_distance_zero(self):
        a = concept("a", "route", "deliver", "delayed-debt")
        self.assertEqual(mod.structural_distance(a, a), 0.0)

    def test_missing_axis_is_neutral_not_maximal(self):
        a = {"id": "a", "signature": {"primary_operation": "route"}}
        b = {"id": "b", "signature": {"primary_operation": "route", "risk_coupling": "delayed-debt"}}
        self.assertAlmostEqual(mod.structural_distance(a, b), 0.25)

    def test_hard_reject_is_removed(self):
        items = [
            concept("a", "route", "deliver", "delayed-debt", hard=True),
            concept("b", "transform", "convert", "opportunity-cost"),
        ]
        result = mod.curate(items, 2, 0.30)
        self.assertEqual(result["selected_ids"], ["b"])
        self.assertEqual(result["hard_rejected_ids"], ["a"])

    def test_structural_duplicates_share_cluster(self):
        items = [
            concept("a", "route", "deliver", "delayed-debt"),
            concept("b", "route", "deliver", "delayed-debt", extra={"skill_channel": "planning"}),
        ]
        survivors = [dict(x) for x in items]
        mod.assign_clusters(survivors, 0.30)
        self.assertEqual(survivors[0]["duplicate_cluster"], survivors[1]["duplicate_cluster"])

    def test_dominated_duplicate_loses_representation(self):
        items = [
            concept("a", "route", "deliver", "delayed-debt", {"decision_evidence": 1, "skill_evidence": 1}),
            concept("b", "route", "deliver", "delayed-debt", {"decision_evidence": 2, "skill_evidence": 2}),
            concept("c", "transform", "convert", "opportunity-cost", {"decision_evidence": 1, "skill_evidence": 1}),
        ]
        result = mod.curate(items, 2, 0.30)
        self.assertNotIn("a", result["selected_ids"])
        self.assertIn("b", result["selected_ids"])

    def test_diversity_beats_near_duplicate_after_first_pick(self):
        items = [
            concept("a", "route", "deliver", "delayed-debt", {"decision_evidence": 3, "skill_evidence": 3}, extra={"state_topology": "graph"}),
            concept("b", "route", "deliver", "opportunity-cost", {"decision_evidence": 3, "skill_evidence": 2}, extra={"state_topology": "graph"}),
            concept("c", "transform", "convert", "same-action-creates-risk", {"decision_evidence": 2, "skill_evidence": 2}, extra={"state_topology": "queue", "information_model": "delayed"}),
        ]
        result = mod.curate(items, 2, 0.15)
        self.assertEqual(result["selected_ids"][0], "a")
        self.assertEqual(result["selected_ids"][1], "c")

    def test_missing_evidence_does_not_create_dominance(self):
        a = concept("a", "route", "deliver", "delayed-debt", {"decision_evidence": 3})
        b = concept("b", "route", "deliver", "delayed-debt", {"decision_evidence": 1, "skill_evidence": 3})
        self.assertFalse(mod.dominates(a, b))
        self.assertFalse(mod.dominates(b, a))

    def test_one_shared_evidence_dimension_cannot_dominate(self):
        a = concept("a", "route", "deliver", "delayed-debt", {"decision_evidence": 3})
        b = concept("b", "route", "deliver", "delayed-debt", {"decision_evidence": 0})
        self.assertFalse(mod.dominates(a, b))

    def test_full_pareto_frontier_reaches_global_coverage_selection(self):
        items = [
            concept("a", "route", "deliver", "delayed-debt",
                    {"decision_evidence": 3, "skill_evidence": 1},
                    extra={"skill_channel": "planning"}),
            concept("b", "route", "deliver", "delayed-debt",
                    {"decision_evidence": 1, "skill_evidence": 3},
                    extra={"skill_channel": "timing"}),
            concept("c", "transform", "convert", "opportunity-cost",
                    {"decision_evidence": 3, "skill_evidence": 3},
                    extra={"skill_channel": "planning"}),
        ]
        result = mod.curate(items, 2, 0.30)
        self.assertEqual(result["eligible_frontier_count"], 3)
        self.assertEqual(result["selected_ids"], ["c", "b"])

    def test_complete_link_prevents_single_link_chain(self):
        items = [
            concept("a", "route", "deliver", "delayed-debt", extra={"skill_channel": "planning"}),
            concept("b", "transform", "deliver", "delayed-debt", extra={"skill_channel": "planning"}),
            concept("c", "transform", "convert", "delayed-debt", extra={"skill_channel": "planning"}),
        ]
        survivors = [dict(x) for x in items]
        mod.assign_clusters(survivors, 0.30)
        self.assertEqual(survivors[0]["duplicate_cluster"], survivors[1]["duplicate_cluster"])
        self.assertNotEqual(survivors[0]["duplicate_cluster"], survivors[2]["duplicate_cluster"])

    def test_core_tuple_extension_bridges_sparse_records_only(self):
        full = concept("a", "route", "deliver", "delayed-debt", extra={
            "control_topology": "allocation",
            "state_topology": "graph",
            "information_model": "perfect",
            "failure_shape": "deadline",
            "skill_channel": "planning",
        })
        sparse = concept("b", "route", "deliver", "delayed-debt")
        known_split = concept("c", "route", "deliver", "delayed-debt", extra={
            "control_topology": "cursor-target",
            "state_topology": "queue",
            "information_model": "hidden",
            "failure_shape": "deadline",
            "skill_channel": "planning",
        })
        self.assertTrue(mod.duplicate_pair(full, sparse, 0.30))
        self.assertFalse(mod.duplicate_pair(full, known_split, 0.30))

    def test_hard_reject_requires_reason_type_and_provenance(self):
        item = concept("a", "route", "deliver", "delayed-debt")
        item["hard_reject"] = True
        with self.assertRaisesRegex(ValueError, "hard_reject_reason"):
            mod.curate([item], 1, 0.30)
        item["hard_reject_reason"] = "Core goal is unreachable."
        item["hard_reject_evidence"] = {"provenance": "trace t1"}
        with self.assertRaisesRegex(ValueError, "evidence type"):
            mod.curate([item], 1, 0.30)
        item["hard_reject_evidence"] = {"type": "state_trace"}
        with self.assertRaisesRegex(ValueError, "provenance"):
            mod.curate([item], 1, 0.30)

    def test_named_human_hard_reject_requires_context_and_observation(self):
        item = concept("a", "route", "deliver", "delayed-debt", hard=True)
        item["hard_reject_evidence"] = {
            "type": "named_human_observation",
            "provenance": "playtest log 04",
        }
        with self.assertRaisesRegex(ValueError, "test_context"):
            mod.curate([item], 1, 0.30)
        item["hard_reject_evidence"]["test_context"] = "prototype p2, session s04"
        with self.assertRaisesRegex(ValueError, "observation"):
            mod.curate([item], 1, 0.30)
        item["hard_reject_evidence"]["observation"] = "All five players were unable to reach the required state."
        result = mod.curate([item], 1, 0.30)
        self.assertEqual(result["hard_rejected"][0]["evidence"]["test_context"], "prototype p2, session s04")

    def test_duplicate_ids_are_rejected(self):
        item = concept("same", "route", "deliver", "delayed-debt")
        with self.assertRaisesRegex(ValueError, "duplicate concept id"):
            mod.curate([item, dict(item)], 1, 0.30)


if __name__ == "__main__":
    unittest.main()
