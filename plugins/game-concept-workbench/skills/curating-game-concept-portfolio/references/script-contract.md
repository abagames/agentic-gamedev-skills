# Portfolio Script Contract

`scripts/curate_portfolio.py` accepts either a JSON array or `{ "concepts": [...] }`.

Minimal concept:

```json
{
  "id": "c07",
  "hard_reject": false,
  "signature": {
    "time_model": "turn",
    "primary_operation": "route",
    "progress_conversion": "deliver",
    "risk_coupling": "delayed-debt"
  },
  "evidence_scores": {
    "decision_evidence": 2,
    "skill_evidence": 1,
    "feasibility_evidence": 3
  },
  "unknowns": ["Does expert routing remain legible at high density?"]
}
```

`id` must be a unique stable string. `hard_reject: true` is accepted only with all of:

```json
{
  "hard_reject": true,
  "hard_reject_reason": "The required goal is unreachable in the supplied transition trace.",
  "hard_reject_evidence": {
    "type": "state_trace",
    "provenance": "ruleset v3, trace t-017"
  }
}
```

Accepted evidence types are `reasoning_trace`, `state_trace`, `executable_observation`, and `named_human_observation`. Missing reason, type, or provenance is an input error rather than a silent exclusion. `named_human_observation` also requires non-empty `test_context` and `observation`. Preference, approval, and unqualified stress-test statuses are not hard-reject evidence.

Missing evidence dimensions are unknown, not zero. Missing signature axes contribute neutral uncertainty to pair distance rather than maximal similarity or difference.

## Deterministic method

1. validate stable unique IDs and typed hard-rejection evidence, then remove qualifying `hard_reject: true` records;
2. assign stable greedy complete-link structural duplicate clusters, so every pair in a cluster passes the duplicate predicate;
3. treat distance `<= --cluster-threshold` as duplicate; when the three-field core tuple matches, extend the limit to `max(0.45, threshold)` only if no known `time_model`, `control_topology`, `state_topology`, `information_model`, or `skill_channel` value differs;
4. within each cluster, Pareto-screen only when at least two evidence dimensions are supplied by both candidates;
5. retain every non-dominated frontier member as a global coverage candidate;
6. select the requested portfolio with greedy max-min structural distance, choosing at most one candidate per cluster;
7. use evidence breadth only as a tie-breaker and break final ties by stable `id`.

The output reports both `eligible_cluster_count` and `eligible_frontier_count`, preserves each selected candidate's cluster member/frontier IDs, and includes typed hard-rejection provenance. The `0.45` core-tuple extension mainly lets a sparse compatible record join a more complete one; it cannot override a known strategic-axis difference.

The script is a reproducible heuristic. It does not judge fun and does not replace human normalization of ambiguous prose.

## Command

```bash
python .agents/skills/curating-game-concept-portfolio/scripts/curate_portfolio.py concepts.json -n 4 -o portfolio.json
```

Optional `--cluster-threshold` defaults to `0.30`.
