---
name: generating-retro-arcade-concepts
description: "Batch-generates, evaluates, and specs multiple fixed-screen arcade game concepts in the style of 1978-1985 cabinets (default profile: 1980-1983). Use for a concept slate or for turning era constraints into ranked concepts and implementation specs. For one already-chosen concept, use designing-mini-games instead."
---

# Generating Retro Arcade Concepts

Create a slate of original small games, evaluate it, then spec the best two. Read [concept-generation-format.md](references/concept-generation-format.md) for the era profiles, mechanism taxonomy, mandatory 14 fields, rubric, nearest-precedent check, and spec template.

## Hard Constraints

Every concept must:

- use one fixed screen, movement plus one button, no complex hand-built levels, and at most three enemy/obstacle types whose rules each fit in 1–2 sentences;
- escalate only numerical values, present a clear threat within 30 seconds, use lives rather than immediate game-over, and sustain endless waves/rounds;
- prevent random instant deaths and avoid idle or button-mashing as a dominant strategy;
- provide interesting no-input attract motion and a one-phrase audio identity;
- fit the selected Era Hardware Profile (default 1980–1983).

A project brief may replace only the hardware profile. Later profiles do not relax the other constraints.

Use classic fixed-screen pressure, lane, reflection, defense, transformation, push, carry, and self-constraint patterns as seeds, but avoid cloning classics or making maze, platform, formation, scrolling, or terrain-level design the primary source of play.

## Workflow

1. Before ideation, shuffle the five reward-conversion values in the reference and assign one to each of five slots without replacement. If the brief constrains economy type, note the override, skip this assignment, and apply all reward-conversion distinctness and selection rules to risk shape instead.
2. Generate exactly five concepts in the reference's 14-field format, honoring the slot assignments.
3. Score all five with the reference rubric. For each differentiation score, first perform the mandatory Nearest-Precedent Check, including at least two well-known candidates, the nearest precedent's four-axis signature, matching-axis cap, concrete rule overlap, and recall confidence. Do not use this repository's shipped games as precedents.
4. Select the two strongest concepts, favoring low level-design dependency and differentiation. They must differ on reward conversion (or risk shape under an economy override); promote the next-best eligible concept and explain when necessary.
5. Write both implementation specs using the reference template.

## Validation

- Explicitly reject any concept that violates a hard constraint; ensure the active diversity axis uses five unique values and every concept pair differs on at least two of the four mechanism axes.
- State numerical escalation formulas and concrete attract-mode moments for all concepts.
- For each selected spec, give tile-cell screen regions that fit the active profile's grid, objects, transitions, collision tests, numerical difficulty formulas, lives/game-over behavior, and enough detail to begin implementation.
