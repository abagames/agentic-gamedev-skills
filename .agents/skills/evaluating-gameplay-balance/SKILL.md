---
name: evaluating-gameplay-balance
description: "Evaluates and improves gameplay balance from telemetry in any engine. Use when comparing monotonous vs exploratory play, diagnosing death/spawn/scoring/input issues, or proposing structural balance fixes instead of numeric tuning."
---

Use this skill to analyze whether a game rewards skillful play and to propose structural improvements.

Engine-neutral contract:
- Produce comparable runs for monotonous policies and exploratory policies.
- Define the public input schema and visible-state features available to policies.
- Keep seeds, tick rate, max duration, policy definitions, search budget, and aggregation logic comparable across runs.
- Record score, elapsed time, end state, and telemetry for death, spawn, scoring, and input behavior.
- Compute `exploratory_ratio = exploratory.best.score / monotonous.max_score`.
- Treat the ratio as a quality detector, not an optimization target.

Experience guardrails:
- Reject changes that degrade play experience even if metrics improve.
- Score only in-game causal events; do not award points for raw input facts.
- Game-over should be tied to hazards or world-state collapse.
- Do not add hidden behavior that only helps or hurts test agents.
- Avoid numeric-only tuning, branch-only fixes, and added randomness as the primary answer.

Workflow:
1. Locate an existing simulation harness. If none exists, design one using the harness contract before judging balance.
2. Run comparable monotonous and exploratory policies with deterministic seeds.
3. Validate that the report includes run configuration plus death, spawn, scoring, and input telemetry.
4. If telemetry is incomplete, report the gap and request instrumentation/rerun instead of judging balance from score alone.
5. Analyze death, spawn, scoring, and input patterns.
6. Identify root causes in rules or generation logic.
7. Propose at least three candidate fixes with expected impact, risk, and complexity.
8. Re-test with the same policies, seeds, budgets, and aggregation after implementation.

Project checker triage, when the report includes `ratio.diagnostic`:
- Before applying any verdict below, check instrument confidence using evidence independent of the final score comparison. The verdicts are trustworthy only when the exploratory search demonstrably played the game: its best score improved across search iterations instead of staying flat from the start, or its runs engaged scoring opportunities and mechanics that the monotonous policies never touched. If neither signal is present, treat the result as instrument failure (the searcher could not find skilled play), not as evidence about the design: route the game to human or LLM review instead of triggering redesign or structural fixes. If the report lacks the search history or engagement telemetry needed to judge this, report the gap and request instrumentation rather than applying a verdict.
- `mono_dominant`: a monotonous policy outscores exploratory play. Inspect input and scoring telemetry for a missing tradeoff, reusable scoring pulse, safe scoring, or raw-input reward. If the current README invariants do not prevent idle, hold-only, or safe-waiting dominance, this is a **design issue**: report it as such so the caller can revise the README and re-implement. Otherwise prefer structural code-level fixes (input-state, per-target, resource, cooldown, or risk-scoring).
- `tied`: exploratory play cannot meaningfully exceed the monotonous baseline. This is a **design issue** unless telemetry clearly shows a single unfair hazard blocking both policies. Report it as a design issue so the caller can revise the README and re-implement; do not attempt code-level fixes for a fundamentally flawed mechanic.
- `marginal`: exploratory play is ahead but not enough. Determine whether a specific code-level cause is identifiable (implementation issue) or whether the scoring/tradeoff structure itself is missing (design issue). For an implementation issue, prefer risk-based scoring, combo reset causes, scoring scale, or clearer scoring opportunities before touching raw spawn/speed numbers.

**Abandonment criteria**: If the root cause requires changing the Core Experience or discarding the tag relationship to fix, or if 3 improvement attempts have already been exhausted, report that the design **cannot be salvaged within framework constraints** and recommend producing a Failure Report instead of forcing another redesign. Do not propose fixes that would invent a new game under the same slug just to pass the gate.

When this skill runs inside a selection funnel — many candidates are generated, ranked, and culled rather than repaired — the Failure Report path does not apply: report the diagnosis and let the ranking eliminate the artifact. Reserve repair attempts and the 3-attempt limit for post-selection winners.

For this repository's generated one-button games, verbose checker output should be used for improvement diagnosis, but do not infer fixes from monotonous-policy logs alone. Use the GA `detailedLog` to understand what exploratory play tried, then compare only the relevant policy summaries or focused probes needed to verify the suspected invariant.

When telemetry is summarized or sparse, request or add the smallest focused probe before editing. Useful probes include: death hazard id/type/age and player input window, spawn position and safety distance, score reason/target id/risk context, input cadence around score/death, active entity counts, and score per unique opportunity.

Read these references as needed:
- `references/simulation-harness.md` for designing deterministic simulators, input policies, and telemetry emitters.
- `references/log-contract.md` for the engine-neutral telemetry schema.
- `references/improvement-analysis.md` for analysis perspectives and report templates.
- `references/balance-patterns.md` for structural balance patterns.
- `references/godot-implementation-notes.md` for translating common balance fixes into Godot/GDScript.

## Companion skills

- For Godot projects, use `scaffolding-godot-mini-games` for project setup and `running-headless-godot` for simulator execution, tests, logs, and export checks.
- Structural fixes that touch rules are design changes, not numeric tuning; do not silently re-tune numbers without revisiting the design.
