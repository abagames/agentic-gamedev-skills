---
name: curating-game-concept-portfolio
description: "Curates a supplied set of game ideas into a small mechanically diverse portfolio by normalizing prose into mechanism signatures, clustering structural duplicates, excluding demonstrated hard failures, comparing available evidence without treating missing data as zero, and selecting for coverage rather than one subjective score. Use for pitch triage, game-jam shortlist selection, prototype portfolio planning, or choosing among many existing concepts."
---
# Curating a Game Concept Portfolio

Turn an existing pile of concepts into a small decision-ready portfolio. The goal is not to declare one speculative winner. Preserve distinct design hypotheses while removing redundancy and candidates with demonstrated core failures.

## Core rules

- This skill is self-contained; it must work from natural-language concept descriptions alone.
- Do not require prior stress-test output. If such evidence exists, use it; otherwise preserve uncertainty.
- Do not use a weighted `fun` score or prose appeal as the primary selector.
- Theme, art direction, setting, and content volume do not establish mechanical diversity.
- Preserve stable IDs and show equal-format normalized mechanism fields before or beside pitch prose.

## Inputs

Accept any of:

- a brainstorm list;
- design notes or pitch blurbs;
- normalized concept records;
- concepts plus prototype/telemetry evidence;
- a requested portfolio size and optional business or implementation constraints.

Default portfolio size: 4 concepts.

## Workflow

1. **Normalize each concept.** Read [references/normalization.md](references/normalization.md). Extract a mechanism signature and keep unknown mechanical details explicit.
2. **Respect demonstrated failures.** Exclude only concepts with a non-empty reason, accepted evidence type, and provenance for `hard_reject`. A prior stress-test label is not enough by itself. Do not invent negative evidence because details are missing.
3. **Cluster structural duplicates.** Strip theme nouns and compare normalized signatures using [references/structural-similarity.md](references/structural-similarity.md). Require pairwise compatibility throughout a cluster so single-link chains cannot merge distant endpoints. If JSON records are available, `scripts/curate_portfolio.py` can perform a deterministic first pass.
4. **Compare evidence locally.** Within a duplicate cluster, one candidate dominates another only when at least two supplied evidence dimensions overlap, it is no worse on every shared dimension, and it is strictly better on one. Missing evidence is unknown, not zero. Preserve the whole non-dominated frontier for global coverage selection.
5. **Select for coverage.** Choose at most one concept per duplicate cluster while considering every frontier member as the possible representative. Maximize distance from already selected mechanism signatures. Evidence breadth may break distance ties, but must not erase structural coverage.
6. **Preserve useful uncertainty.** Keep a high-uncertainty concept when it occupies a distinct structural region and its key uncertainty can be cheaply tested.
7. **Build the portfolio.** For each selected concept state: why retained, key decision, strongest evidence, main risk, unresolved question, and smallest next test. If the user requests one recommendation, recommend what to prototype first based on expected information gain and implementation cost—not what is guaranteed to be the best final game.
8. **Place review before material investment.** Use [references/human-review.md](references/human-review.md). Interactive work may request approval or preference at this boundary; unattended or batch work must complete as `review_pending` without inventing human input.

## Evidence encoding

When structured data is useful, optional evidence dimensions are ordinal `0..3`:

- `decision_evidence`
- `strategy_evidence`
- `skill_evidence`
- `learning_evidence`
- `risk_reward_evidence`
- `feasibility_evidence`

Interpretation: 0 = negative evidence, 1 = weak/ambiguous, 2 = positive reasoning/trace evidence, 3 = positive executable or observed human evidence. Human evidence qualifies only with a named test context, recorded observation, and provenance. Missing means unknown and is excluded from dominance comparison.

Imported stress-test statuses retain their source/method provenance. Do not automatically translate `fails`, `weak`, `unknown`, or `survives` into `hard_reject` or any ordinal evidence score.

Read [references/script-contract.md](references/script-contract.md) before running the bundled script.

## Routing and handoff

Use this skill for coverage-based triage of a supplied set. Use `exploring-game-design-space` to generate a broader hypothesis slate, or `stress-testing-game-concepts` to adversarially audit one or more existing candidates. Neither is a prerequisite. When records are handed over, preserve stable IDs, normalized signatures, unknowns, and provenance.

## Output

Produce 3–5 concepts unless the user requests another count. Use [references/portfolio-output.md](references/portfolio-output.md). Include a short coverage note describing how the selected concepts differ mechanically and a brief rejection summary for materially important discarded clusters.

## Completion criteria

- natural-language inputs can be curated without another skill;
- structural duplicates do not consume most final slots;
- no candidate is removed solely because its prose is less polished;
- hard failures are distinguished from unknowns;
- selected concepts represent different design hypotheses or explicitly justified close variants;
- every selected concept has one falsifiable next question.
- review records keep preference, observed human evidence, and approval distinct, and batch work can finish as `review_pending`.
