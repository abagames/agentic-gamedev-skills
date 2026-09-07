---
name: directing-game-visuals
description: "Directs readable, coherent game visuals. Use when defining visual hierarchy, palette roles, screen composition, event feedback, or reducing generic AI-looking game art without relying on HUD text."
---

Make visuals communicate play state rather than merely decorate it. Put the full plan in `<PROJECT_DIR>/VISUAL_DESIGN.md` when a project is known; keep any existing README/design visual-audio section to a short summary, updated only when direction changes. If tags are absent, derive and label 2–3 `concept-derived` tags from the concept's material, geometry, motion, or atmosphere.

Core rules:
- Establish one protagonist, one primary danger, and one primary reward before detail.
- Assign every palette color a gameplay role.
- Feedback must be legible without UI text: motion, shape, impact, timing, contrast, and sound hooks should carry meaning.
- Keep the center readable; push noisy texture and secondary motion to the periphery unless the mechanic demands otherwise.
- Transform familiar template symbols through the game's own visual logic.

Workflow:
1. Extract mood, material, geometry, and motion from the concept or constraints.
2. Synthesize one visual phrase for the whole game.
3. Map mechanics to visual state changes and feedback effects.
4. Choose a 3-5 color palette with explicit gameplay roles.
5. Validate protagonist, danger, and reward in one still frame without HUD text.
6. Only when implementation and probing are in scope, expose stable palette roles and HUD anchors as **runtime-readable data** shared by drawing and semantic probes. Do not require fixed coordinates for responsive/scene-graph layouts or turn visual-direction-only work into code changes.

When pixel-art generation will follow, include an asset handoff: what remains procedural, what becomes assets, palette constraints, and readability acceptance criteria.

Read `references/visual-design-guide.md` for pattern tables, checklists, and the anti-generic visual addendum template.
