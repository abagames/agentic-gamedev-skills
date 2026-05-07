---
name: directing-game-visuals
description: "Directs readable, coherent game visuals. Use when defining visual hierarchy, palette roles, screen composition, event feedback, or reducing generic AI-looking game art without relying on HUD text."
---

Use this skill to make game visuals communicate play state, not just decorate the screen.

Default artifacts:
- If a project directory is known, put the full visual plan in `<PROJECT_DIR>/VISUAL_DESIGN.md`.
- If the project already has a README or design note with a visual/audio section, keep that section as a short summary and update it only when the visual direction changes.
- When pixel-art assets will be generated later, include an asset handoff section that states which elements stay procedural, which become assets, palette constraints, and readability acceptance criteria.
- If no visual tags are provided, derive 2-3 `concept-derived` tags from the concept's material, geometry, motion, or atmosphere, and label them as such in `VISUAL_DESIGN.md`.

Core rules:
- Establish one protagonist, one primary danger, and one primary reward signal before adding detail.
- Assign palette colors to gameplay roles.
- Feedback must be legible without UI text: motion, shape, impact, timing, contrast, and sound hooks should carry meaning.
- Keep the center readable; push noisy texture and secondary motion to the periphery unless the mechanic demands otherwise.
- Avoid familiar template symbols unless they are transformed by the game's visual logic.

Workflow:
1. Extract the mood, material, geometry, and motion implied by the game concept or visual constraints.
2. Synthesize one visual phrase for the whole game.
3. Map mechanics to visual state changes and feedback effects.
4. Choose a 3-5 color palette with explicit gameplay roles.
5. Validate that the protagonist / primary danger / primary reward read in a single still frame without HUD text.

Read `references/visual-design-guide.md` for detailed pattern tables, design checklists, and the anti-generic visual addendum template.
