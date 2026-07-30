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

Non-deterministic harnesses:

The contract above assumes a seeded forward model. Some rigs cannot provide one — a real browser driven over a wall-clock window, an engine whose RNG you do not control, a policy comparison run against live rendering. Seeding is still the first choice; when it is genuinely unavailable, the following replaces it, and skipping it produces confident conclusions from noise:

- Report a **min–max band over n ≥ 3 runs per policy**, never a point estimate. A single run of a long-tailed distribution proves nothing about either policy.
- To claim a band has **moved**, require **n ≥ 5** and no overlap with the recorded prior band. A sample that overlaps the previous band is not a finding, however plausible the mechanism that would explain it.
- **Record the accepted band and its known tails** in the project's spec, so later runs compare against history instead of rediscovering the same spread. If a policy is known to land near a bad-looking value in some fraction of runs (e.g. "~20 % of idle runs reach 0.18 of skilled score, by design, because the field can collapse on its own"), that tail is documented and settled — not re-litigated every time it appears.
- **Retraction is a valid and expected output.** A conclusion published from a small sample that a larger sample does not support should be withdrawn in place: keep the mechanism if it was real, and state that its effect size was indistinguishable from noise. Observed case: a band shift published at n=4, with a coherent causal story attached, was retracted at n=6 as the same spread the project had already recorded twice.

Experience guardrails:
- Reject changes that degrade play experience even if metrics improve.
- Score only in-game causal events; do not award points for raw input facts.
- Game-over should be tied to hazards or world-state collapse.
- Do not add hidden behavior that only helps or hurts test agents.
- Avoid numeric-only tuning, branch-only fixes, and added randomness as the primary answer.

Workflow:
1. Locate an existing simulation harness. If none exists, design one using the harness contract before judging balance.
2. Choose the comparison protocol:
   - If seeding is available, run comparable monotonous and exploratory policies with the same deterministic seeds.
   - If seeding is genuinely unavailable, use the non-deterministic band protocol above and keep run count, wall-clock window, policy definitions, and sampling cadence comparable.
3. Validate that the report includes run configuration plus death, spawn, scoring, and input telemetry.
4. If telemetry is incomplete, report the gap and request instrumentation/rerun instead of judging balance from score alone.
5. Analyze death, spawn, scoring, and input patterns.
6. Identify root causes in rules or generation logic.
7. Propose at least three candidate fixes with expected impact, risk, and complexity.
8. Re-test with the same policies, budgets, aggregation, and comparison protocol after implementation. Preserve the same seeds for deterministic runs; preserve the same run count and sampling setup for non-deterministic runs.

Project checker triage, when the report includes `ratio.diagnostic`:
- Before applying any verdict below, check instrument confidence using evidence independent of the final score comparison. The verdicts are trustworthy only when the exploratory search demonstrably played the game: its best score improved across search iterations instead of staying flat from the start, or its runs engaged scoring opportunities and mechanics that the monotonous policies never touched. If neither signal is present, treat the result as instrument failure (the searcher could not find skilled play), not as evidence about the design: route the game to human or LLM review instead of triggering redesign or structural fixes. If the report lacks the search history or engagement telemetry needed to judge this, report the gap and request instrumentation rather than applying a verdict.
- `mono_dominant`: a monotonous policy outscores exploratory play. Inspect input and scoring telemetry for a missing tradeoff, reusable scoring pulse, safe scoring, or raw-input reward. If the current README invariants do not prevent idle, hold-only, or safe-waiting dominance, this is a **design issue**: report it as such so the caller can revise the README and re-implement. Otherwise prefer structural code-level fixes (input-state, per-target, resource, cooldown, or risk-scoring).
- `tied`: exploratory play cannot meaningfully exceed the monotonous baseline. This is a **design issue** unless telemetry clearly shows a single unfair hazard blocking both policies. Report it as a design issue so the caller can revise the README and re-implement; do not attempt code-level fixes for a fundamentally flawed mechanic.
- `marginal`: exploratory play is ahead but not enough. Determine whether a specific code-level cause is identifiable (implementation issue) or whether the scoring/tradeoff structure itself is missing (design issue). For an implementation issue, prefer risk-based scoring, combo reset causes, scoring scale, or clearer scoring opportunities before touching raw spawn/speed numbers.

**Abandonment criteria**: If the root cause requires changing the Core Experience or discarding the tag relationship to fix, or if 3 improvement attempts have already been exhausted, report that the design **cannot be salvaged within framework constraints** and recommend producing a Failure Report instead of forcing another redesign. Do not propose fixes that would invent a new game under the same slug just to pass the gate.

When this skill runs inside a selection funnel — many candidates are generated, ranked, and culled rather than repaired — the Failure Report path does not apply: report the diagnosis and let the ranking eliminate the artifact. Reserve repair attempts and the 3-attempt limit for post-selection winners.

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
