---
name: stress-testing-game-concepts
description: "Audits one or more game concepts, rule specs, or early prototypes adversarially for unreachable goals, dominant simple policies, agency collapse, irrelevant mechanics, reward exploits, and unsupported design claims while separating demonstrated defects from uncertainty. Use to challenge an existing game idea before implementation, review a ruleset, diagnose why a prototype may be shallow, or decide what must be tested next."
---
# Stress-Testing Game Concepts

Try to falsify the design claims that can be tested from the available rules or behavior. Do not answer the vague question "is it fun?". Determine whether the claimed decisions, tradeoffs, and skill expression survive adversarial analysis.

## Scope

This skill works independently on:

- a natural-language concept;
- a rules/spec document;
- a transition model or simulator;
- an early playable prototype plus observations or telemetry.

Missing executable evidence is `unknown`, not failure.

Accept stable concept records from another workflow when available, but do not require them. Preserve supplied IDs and mechanism signatures; otherwise assign stable IDs before analysis. Show equal-format normalized causal/mechanism fields before or beside pitch prose when comparing concepts.

## Workflow

1. **Extract the causal model.** Identify actions, state read by the player, automatic dynamics, progress/scoring, failure/loss, and claimed skill expression. Attach source/method provenance to imported evidence and derived verdicts. Do not fill material gaps with favorable assumptions.
2. **List falsifiable claims.** Examples: "timing matters", "taking danger enables more score", "safe play sacrifices future options", "experts can recover from states novices cannot".
3. **Run the failure taxonomy.** Read [references/failure-taxonomy.md](references/failure-taxonomy.md).
4. **Attack with simple policies.** Read [references/policy-library.md](references/policy-library.md). Use only policies applicable to the control scheme and state model.
5. **Probe the key decision.** Construct at least two reachable states where different actions should be preferred for different reasons. If this cannot be shown, record an agency-collapse risk.
6. **Trace consequences.** For discrete enough rules, trace 3–8 decision steps. If a faithful simulator or prototype exists, prefer executable tests over verbal confidence.
7. **Separate evidence states.** Classify each major claim as `fails`, `weak`, `unknown`, or `survives`. A whole concept is `hard_reject` only when a demonstrated core defect makes its stated loop nonfunctional or strategically empty.
8. **Specify the next discriminator.** For every unresolved important claim, state the smallest test that could materially change the conclusion.
9. **Record review after named tests.** When a named prototype or playtest produced human observations, use [references/human-review.md](references/human-review.md). Interactive work may request review before the next investment; unattended or batch work must finish as `review_pending` rather than block or invent evidence.

## Hard-rejection policy

Hard reject only from demonstrated core defects, such as:

- required progress/success is unreachable;
- unavoidable failure occurs regardless of meaningful action;
- a simple state-blind policy dominates every described alternative in the relevant state range;
- nominal actions collapse to strategic equivalence and no recurring choice remains;
- a required rule is contradictory or underspecified enough that the core loop cannot be defined;
- the claimed core interaction cannot exist within a stated hard constraint.

Do not hard reject because a concept is unfamiliar, visually plain, hard to pitch, risky, or dependent on tuning.

A stress-test classification is diagnostic evidence with provenance. Downstream curation may retain it, but must not automatically map `fails`, `weak`, `unknown`, or `survives` to `hard_reject` or an ordinal evidence score. A downstream `hard_reject` needs its own demonstrated reason, accepted evidence type, and provenance.

## Repair boundary

Default behavior is diagnosis, not redesign. If the user asks for repairs, first preserve the failure trace, then suggest the smallest rule-level change that targets that trace. Do not bury the diagnosis under a rewritten concept.

## Output contract

Use [references/report-contract.md](references/report-contract.md). Evidence must name the tested policy, trace, invariant, telemetry observation, or missing information. Never use an LLM's holistic fun judgment as evidence.

## Routing and handoff

Use this skill to attack existing concepts without redesigning them by default. Use `exploring-game-design-space` when the primary need is to generate structurally varied hypotheses, and `curating-game-concept-portfolio` when the primary need is coverage-based selection from a supplied set. All three can run independently; preserve stable IDs, normalized signatures, provenance, and unknowns when handing records between them.

## Completion criteria

- every hard rejection has a reproducible reasoning trace or executable observation;
- unknown is distinct from negative evidence;
- simple-policy viability is not confused with dominance;
- positive claims describe observable strategic behavior;
- the report identifies the cheapest next test for consequential unknowns.
- preference and approval are never reported as evidence, and observed human evidence names its test context and observation.
