---
name: exploring-game-design-space
description: "Explores a broad game-design space by generating structurally varied concepts, attacking obvious failures, mutating promising mechanisms, and returning a small set of distinct testable hypotheses without ranking speculative fun. Use for open-ended game ideation, mechanic-space exploration, game-jam concept search, or deriving multiple mechanical directions from a seed. Do not use merely to audit one existing concept or to choose among a supplied shortlist."
---
# Exploring Game Design Space

Treat game ideation as search over mechanics, not as a one-shot brainstorm. Produce several distinct design hypotheses, remove only demonstrable dead ends or mechanical duplicates, and mutate around useful uncertainties.

## Core rules

- Never use one holistic `fun`, `quality`, or `best concept` score to drive the search.
- Structural diversity comes before theme, fiction, art direction, content quantity, progression systems, or polish.
- A surviving concept is not proven fun. It is a mechanically distinct hypothesis worth a prototype or playtest.
- Give every candidate a stable ID that does not change with rank. Present equal-format normalized mechanism fields before or beside pitch prose.
- Preserve the provenance and uncertainty of evidence. A cheap guard result is not equivalent to a later stress-test verdict.
- This skill is self-contained. Do not require another skill to complete its workflow.

## Inputs

Infer missing fields when safe and state important assumptions:

- platform and input constraints;
- target session length and learning horizon;
- desired experience or player tension;
- implementation budget and forbidden mechanisms;
- references that may inspire but must not be copied;
- optional existing seed mechanic;
- optional search budget.

Default search budget when unconstrained: 18 root concepts, 6 first-round survivors, up to 2 mutation rounds, 4 final concepts.

## Workflow

1. **Normalize the brief.** Separate hard constraints from preferences. Identify what can vary freely.
2. **Plan structural coverage.** Read [references/search-method.md](references/search-method.md). Pre-assign mechanism neighborhoods so the population cannot collapse into reskins of the first association.
3. **Generate root concepts.** Record each concept using [references/concept-record.md](references/concept-record.md). Every concept must name a recurring decision, the state read before that decision, and how expert behavior could differ from a simple policy.
4. **Apply cheap adversarial guards.** Use [references/search-guards.md](references/search-guards.md). Remove only explicit hard failures. Mark uncertain claims as `unknown` rather than negative evidence.
5. **Collapse structural neighbors.** Compare mechanism signatures after stripping theme nouns. Keep one representative per near-duplicate neighborhood unless close variants are intentionally being studied.
6. **Mutate mechanisms, not cosmetics.** For promising but weak concepts, change a causal relationship, information structure, commitment, topology, or risk/reward coupling. Preserve lineage and state what behavior the mutation is expected to change.
7. **Repeat selectively.** Re-apply the cheap guards and duplicate pass. Stop when new children mostly map to existing signatures, add rules without new decisions, or fail to change the targeted weakness.
8. **Return a hypothesis slate.** Present 3–5 structurally distinct concepts. For each, state why it remains in the slate, its strongest structural evidence and provenance, its main risk, one unresolved question, and the smallest prototype or playtest that could resolve it.
9. **Place review at the investment boundary.** Before costly testing or prototyping, use [references/human-review.md](references/human-review.md). In an interactive run, request review when it affects the next investment. In unattended or batch work, finish with `status: review_pending`; never invent a response or block completion.

## Routing and handoff

Use this skill to create a broad hypothesis slate. For adversarial review of one or more existing concepts, hand the stable concept records to `stress-testing-game-concepts`. For selection among a supplied set, hand the same records to `curating-game-concept-portfolio`. Either later skill can also start independently. Preserve IDs, normalized signatures, evidence provenance, and unknowns across handoffs; never translate another skill's status into `hard_reject` or an evidence score automatically.

## Search discipline

Prefer breadth before depth. During root generation, do not improve weak ideas with upgrades, shops, metaprogression, narrative, audiovisual juice, or more content. During mutation, alter one important causal relationship at a time when possible.

Do not silently turn missing details into favorable assumptions. If a concept's viability depends on spawn distributions, tuning windows, social behavior, authored surprise, or presentation, preserve that dependency as an unresolved question.

## Stop conditions

Stop the search when any two are true:

- a new batch mostly duplicates existing mechanism signatures;
- mutations repeatedly add complexity without creating a new decision;
- the final slate already covers the meaningful structural neighborhoods allowed by the brief;
- remaining uncertainty requires implementation, simulation, or human play rather than more verbal ideation.

## Completion criteria

- root concepts are mechanically varied rather than themed variants;
- every removal has a named hard defect or duplicate relationship;
- no candidate is removed solely because another one "sounds more fun";
- each final concept exposes a different design hypothesis or explicitly justified close variant;
- every final concept contains a falsifiable next question and smallest useful test.
- any review record separates preference, observed human evidence, and approval; unattended work can complete as `review_pending`.
