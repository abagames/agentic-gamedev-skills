---
name: generating-retro-arcade-concepts
description: "Batch-generates, evaluates, and specs multiple fixed-screen arcade game concepts in the style of 1978-1983 cabinets. Use when asked to brainstorm several new arcade games at once, produce a concept slate to choose from, or turn era/hardware constraints into ranked concepts plus implementation specs. For hardening a single already-chosen concept, use designing-mini-games instead."
---

Use this skill to invent a *slate* of new small arcade games and pick the best ones, not to recreate existing classics. The deliverable is several concepts → an evaluation → a shortlist → implementation specs. If the user already has one concept and wants its mechanics hardened, that is a different job (single-design), not this one.

## Hard Constraints

Every generated concept must satisfy all of these:

- Self-contained on a single screen; scrolling stages are prohibited.
- No hand-crafted complex level design; no maze navigation, platforming, or long enemy spawn tables.
- Player controls are movement plus one button.
- At most 3 types of enemies or obstacles; each enemy's behavior rule is expressible in 1-2 sentences.
- Difficulty escalates only through numerical changes (speed, count, spawn interval, hit points, score multipliers).
- A clear threat must emerge within 30 seconds.
- Randomness is allowed but must never cause unfair instant deaths.
- Lives system: a mistake consumes a life rather than ending the game immediately.
- No definitive ending; sustain infinite waves/rounds through numerical escalation.
- In attract mode with no input, the game must still produce visually interesting motion.
- Expressible within 256x224 logical resolution, 16x16 sprites, 64-color / 8x8 tile equivalents (the era default; a project brief may override these numbers).
- The audio identity must be describable in a single phrase covering its signature SFX and jingle direction.

## Target And Avoid Directions

Pull toward (seeds, not templates): Game & Watch situational judgment, Space Invaders approach pressure, Centipede splitting/transformation, Frogger lane dodging, Missile Command defense decisions, Snake self-imposed constraint, Breakout reflection/destruction, Pengo push/crush/herd.

Steer away from designs where level design is the primary fun: Pac-Man maze AI, Galaga formation staging, Xevious scrolling placement, Donkey Kong platform/ladder stages, Dig Dug combined terrain+enemy pressure.

## Slate Diversity Policy

Slates tend to collapse toward one economy type per run (whichever pattern is freshest in context). Diversity is enforced *intrinsically* via the Mechanism Signature taxonomy below — NOT by comparing against this project's own previously produced games. Do not scan the working repository's shipped-game directories (in this repo, `tmp/games/<slug>/` and `docs/<slug>/`) as a differentiation reference. Referencing, differentiating from, and drawing on well-known commercial games remains allowed and expected (seeds above, field 10 in the format).

## Workflow

1. Before any ideation, shuffle the reward-conversion values from the Mechanism Signature taxonomy in `references/concept-generation-format.md` and pre-assign one to each of the 5 concept slots without replacement — this makes a single-economy slate structurally impossible regardless of what was built recently. If the project brief itself constrains the economy type (e.g. "five defense games"), the brief wins: skip the axis-1 pre-assignment, note the override, and apply every reward-conversion distinctness requirement below to the risk-shape axis instead.
2. Generate 5 concepts, each in the 14-field format from `references/concept-generation-format.md`, honoring each slot's assigned reward-conversion value.
3. Evaluate all 5 against the criteria in that reference (implementability, rule clarity, single-screen fit, low level-design dependency, risk/reward strength, replayability, differentiation, attract appeal).
4. Select the 2 most promising concepts. They must differ on the reward-conversion axis; if the two best scorers share it, promote the next-best concept with a different value and say so.
5. Write an implementation specification for each selected concept (screen layout, object list, state transitions, collision detection, difficulty-escalation formula, game-over condition).

Read `references/concept-generation-format.md` for the per-concept field list, the evaluation rubric, and the implementation-spec template.

## Validation Before Finishing

- Each concept passes every Hard Constraint above (check explicitly; reject concepts that need scrolling, a second button, hand-built levels, or more than 3 enemy types).
- Difficulty escalation is stated as a numerical formula, not as new content.
- The attract-mode highlight is a concrete moment, not "it looks cool."
- Idle and button-mashing are not the dominant strategy in any selected concept.
- The slate honors the pre-assigned reward-conversion slots (no two concepts share a value), and every pair of concepts differs on at least 2 of the 4 mechanism-signature axes.
- The 2 selected concepts differ on the reward-conversion axis.
- Every concept's differentiation score went through the Nearest-Precedent Check in the reference: nearest well-known commercial precedent named with its 4-axis signature, matching-axes score cap applied, recall confidence stated.
- Each selected concept's spec is concrete enough to start implementing from.
