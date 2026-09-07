#!/usr/bin/env python3
"""Cluster and select a structurally diverse game-concept portfolio.

This script intentionally does not judge fun. It assumes prose has already been
normalized into mechanism signatures by the calling skill/agent.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SIGNATURE_AXES = [
    "time_model",
    "control_topology",
    "state_topology",
    "primary_operation",
    "progress_conversion",
    "risk_coupling",
    "information_model",
    "failure_shape",
    "skill_channel",
]

CORE_AXES = ["primary_operation", "progress_conversion", "risk_coupling"]

# A matching core tuple may bridge sparse records, but it must not erase a
# known difference that can change what the player reads or how strategy works.
STRATEGY_SPLIT_AXES = [
    "time_model",
    "control_topology",
    "state_topology",
    "information_model",
    "skill_channel",
]

HARD_REJECT_EVIDENCE_TYPES = {
    "reasoning_trace",
    "state_trace",
    "executable_observation",
    "named_human_observation",
}

EVIDENCE_KEYS = [
    "decision_evidence",
    "strategy_evidence",
    "skill_evidence",
    "learning_evidence",
    "risk_reward_evidence",
    "feasibility_evidence",
]


def axis_distance(a: Any, b: Any) -> float:
    """Categorical/Jaccard distance with neutral uncertainty for missing values."""
    if a is None or b is None:
        return 0.5
    if isinstance(a, list) or isinstance(b, list):
        sa = set(a if isinstance(a, list) else [a])
        sb = set(b if isinstance(b, list) else [b])
        if not sa and not sb:
            return 0.0
        return 1.0 - len(sa & sb) / len(sa | sb)
    return 0.0 if a == b else 1.0


def structural_distance(a: dict[str, Any], b: dict[str, Any]) -> float:
    sa, sb = a.get("signature", {}), b.get("signature", {})
    axes = [k for k in SIGNATURE_AXES if k in sa or k in sb]
    if not axes:
        return 0.5
    return sum(axis_distance(sa.get(k), sb.get(k)) for k in axes) / len(axes)


def core_same(a: dict[str, Any], b: dict[str, Any]) -> bool:
    sa, sb = a.get("signature", {}), b.get("signature", {})
    return all(sa.get(k) is not None and sa.get(k) == sb.get(k) for k in CORE_AXES)


def has_known_strategy_split(a: dict[str, Any], b: dict[str, Any]) -> bool:
    sa, sb = a.get("signature", {}), b.get("signature", {})
    return any(
        sa.get(axis) is not None
        and sb.get(axis) is not None
        and axis_distance(sa[axis], sb[axis]) > 0
        for axis in STRATEGY_SPLIT_AXES
    )


def duplicate_pair(a: dict[str, Any], b: dict[str, Any], threshold: float) -> bool:
    distance = structural_distance(a, b)
    if distance <= threshold:
        return True
    return (
        core_same(a, b)
        and distance <= max(0.45, threshold)
        and not has_known_strategy_split(a, b)
    )


def assign_clusters(concepts: list[dict[str, Any]], threshold: float) -> None:
    """Assign stable greedy complete-link clusters.

    Every pair in a cluster must satisfy the duplicate predicate, so A-B and
    B-C similarity cannot merge distant A and C through a single-link chain.
    """
    clusters: list[list[dict[str, Any]]] = []
    for concept in sorted(concepts, key=lambda c: str(c.get("id", ""))):
        for cluster in clusters:
            if all(duplicate_pair(concept, member, threshold) for member in cluster):
                cluster.append(concept)
                break
        else:
            clusters.append([concept])

    for index, cluster in enumerate(clusters, start=1):
        for concept in cluster:
            concept["duplicate_cluster"] = f"cluster-{index:02d}"


def evidence_scores(c: dict[str, Any]) -> dict[str, int]:
    raw = c.get("evidence_scores", {}) or {}
    out: dict[str, int] = {}
    for key in EVIDENCE_KEYS:
        if key in raw and raw[key] is not None:
            value = int(raw[key])
            if not 0 <= value <= 3:
                raise ValueError(f"{c.get('id')}: {key} must be in 0..3")
            out[key] = value
    return out


def dominates(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Pareto dominance only on evidence dimensions supplied by both concepts."""
    sa, sb = evidence_scores(a), evidence_scores(b)
    overlap = sorted(set(sa) & set(sb))
    if len(overlap) < 2:
        return False
    return all(sa[k] >= sb[k] for k in overlap) and any(sa[k] > sb[k] for k in overlap)


def evidence_support(c: dict[str, Any]) -> tuple[int, int, int]:
    scores = evidence_scores(c)
    positive = sum(v >= 2 for v in scores.values())
    executable_or_human = sum(v >= 3 for v in scores.values())
    total = sum(scores.values())
    return positive, executable_or_human, total


def stable_best(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    """Best evidence support, then lexicographically smallest id."""
    return sorted(
        candidates,
        key=lambda c: (
            -evidence_support(c)[0],
            -evidence_support(c)[1],
            -evidence_support(c)[2],
            str(c.get("id", "")),
        ),
    )[0]


def cluster_frontier(concepts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for concept in concepts:
        grouped.setdefault(str(concept["duplicate_cluster"]), []).append(concept)

    candidates: list[dict[str, Any]] = []
    for cluster in sorted(grouped):
        group = sorted(grouped[cluster], key=lambda c: str(c.get("id", "")))
        frontier = [
            c for c in group
            if not any(other is not c and dominates(other, c) for other in group)
        ]
        frontier_ids = [c.get("id") for c in frontier]
        member_ids = [c.get("id") for c in group]
        for concept in frontier:
            candidate = dict(concept)
            candidate["_cluster_frontier_ids"] = frontier_ids
            candidate["_cluster_member_ids"] = member_ids
            candidates.append(candidate)
    return candidates


def select_maxmin(candidates: list[dict[str, Any]], count: int) -> list[dict[str, Any]]:
    if count <= 0 or not candidates:
        return []
    ordered = sorted(candidates, key=lambda c: str(c.get("id", "")))
    target_count = min(count, len({c["duplicate_cluster"] for c in ordered}))

    first = stable_best(ordered)
    selected = [first]
    remaining = [
        c for c in ordered
        if c["duplicate_cluster"] != first["duplicate_cluster"]
    ]

    while remaining and len(selected) < target_count:
        ranked = sorted(
            remaining,
            key=lambda c: (
                -min(structural_distance(c, s) for s in selected),
                -evidence_support(c)[0],
                -evidence_support(c)[1],
                -evidence_support(c)[2],
                str(c.get("id", "")),
            ),
        )
        nxt = ranked[0]
        selected.append(nxt)
        remaining = [
            c for c in remaining
            if c["duplicate_cluster"] != nxt["duplicate_cluster"]
        ]
    return selected


def hard_reject_record(concept: dict[str, Any]) -> dict[str, Any] | None:
    if not bool(concept.get("hard_reject", False)):
        return None
    reason = concept.get("hard_reject_reason")
    evidence = concept.get("hard_reject_evidence")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError(f"{concept.get('id')}: hard_reject requires a non-empty hard_reject_reason")
    if not isinstance(evidence, dict):
        raise ValueError(f"{concept.get('id')}: hard_reject requires a hard_reject_evidence object")
    evidence_type = evidence.get("type")
    if evidence_type not in HARD_REJECT_EVIDENCE_TYPES:
        allowed = ", ".join(sorted(HARD_REJECT_EVIDENCE_TYPES))
        raise ValueError(f"{concept.get('id')}: hard_reject evidence type must be one of: {allowed}")
    provenance = evidence.get("provenance")
    if not isinstance(provenance, str) or not provenance.strip():
        raise ValueError(f"{concept.get('id')}: hard_reject evidence requires non-empty provenance")
    normalized_evidence = {
        "type": evidence_type,
        "provenance": provenance.strip(),
    }
    if evidence_type == "named_human_observation":
        for field in ("test_context", "observation"):
            value = evidence.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{concept.get('id')}: named_human_observation requires non-empty {field}"
                )
            normalized_evidence[field] = value.strip()
    return {
        "id": concept.get("id"),
        "reason": reason.strip(),
        "evidence": normalized_evidence,
    }


def validate_concepts(concepts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    rejected: list[dict[str, Any]] = []
    for i, concept in enumerate(concepts):
        if not isinstance(concept, dict):
            raise ValueError(f"concept {i} must be an object")
        concept_id = concept.get("id")
        if not isinstance(concept_id, str) or not concept_id.strip():
            raise ValueError(f"concept {i} is missing stable id")
        if concept_id in seen:
            raise ValueError(f"duplicate concept id: {concept_id}")
        seen.add(concept_id)
        if not isinstance(concept.get("signature", {}), dict):
            raise ValueError(f"{concept_id}: signature must be an object")
        evidence_scores(concept)
        hard_reject = hard_reject_record(concept)
        if hard_reject:
            rejected.append(hard_reject)
    return rejected


def curate(concepts: list[dict[str, Any]], count: int, threshold: float) -> dict[str, Any]:
    hard_rejected = validate_concepts(concepts)
    survivors = [dict(c) for c in concepts if not bool(c.get("hard_reject", False))]
    assign_clusters(survivors, threshold)
    frontier = cluster_frontier(survivors)
    selected = select_maxmin(frontier, count)
    return {
        "selected": selected,
        "selected_ids": [c.get("id") for c in selected],
        "hard_rejected": hard_rejected,
        "hard_rejected_ids": [item["id"] for item in hard_rejected],
        "eligible_cluster_count": len({c["duplicate_cluster"] for c in frontier}),
        "eligible_frontier_count": len(frontier),
        "method": "validated hard-reject filter -> complete-link structural clustering -> full within-cluster Pareto frontiers -> one-per-cluster greedy max-min diversity",
        "cluster_threshold": threshold,
        "core_tuple_threshold": max(0.45, threshold),
    }


def load_concepts(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text())
    concepts = raw.get("concepts") if isinstance(raw, dict) else raw
    if not isinstance(concepts, list):
        raise ValueError("input must be a JSON array or an object with a concepts array")
    validate_concepts(concepts)
    return concepts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("-n", "--count", type=int, default=4)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--cluster-threshold", type=float, default=0.30)
    args = parser.parse_args()

    concepts = load_concepts(args.input)
    result = curate(concepts, args.count, args.cluster_threshold)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
