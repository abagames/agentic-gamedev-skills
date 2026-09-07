---
name: maximizing-game-feel
description: "Improves the tactile satisfaction (\"game feel\") of action games whose visuals are functional but flat. Use when a game runs correctly but feels lifeless; applies to players, enemies, obstacles, projectiles, and items."
---

Improve an already-working action game's response and readability. Consider every important object category, but use only role- and event-justified effects.

## Workflow

### 1. Establish the baseline

Inspect entities, collision bounds, render hierarchy, feedback helpers, performance constraints, and visual direction. Name weak moments before choosing techniques.

For a substantial project, record register, weak moments, effect budgets, and validation thresholds in `FEEL_TUNING.md`; for a one-file game, use a short README or source-header note. Documentation must stay lighter than the implementation.

### 2. Choose the expressive register

Infer tone from title, objects, shapes, palette, and existing direction. Follow an existing `directing-game-visuals` artifact.

| Register | Prefer | Avoid |
|---|---|---|
| Character/playful | pronounced squash, eyes, lively overshoot, particles | effects that obscure small characters |
| Abstract/minimal | tilt, trails, light pulses, restrained particles | faces and cartoon deformation |
| Serious/tense | weighty impact, restrained deformation, short camera kick | bouncy or noisy feedback |

When uncertain, be restrained; motion and light generalize better than faces/bounce.

### 3. Map events to a small feedback vocabulary

For each important event across players, enemies, movable/fixed hazards, projectiles, and rewards, choose a justified effect or explicitly `none`.

Keep distinct vocabularies:

- danger: sharp silhouettes, alert flashes, sparks, short hard impacts;
- reward: glints, radial particles, softer pops, bright confirmation;
- state change: localized pulse, transition motif, controlled camera response;
- near miss: satisfying but visibly weaker than an actual reward.

Read [technique-catalog.md](references/technique-catalog.md) when choosing or implementing concrete techniques; it includes engine-specific constraints.

### 4. Implement presentation without corrupting mechanics

- Keep gameplay/collision authoritative; apply deformation, rotation, trails, flashes, and recoil to render-only visuals where possible.
- Clamp every deformation and camera displacement, and return it to rest.
- Gate costly/disruptive effects by speed, charge, impact, or rarity.
- Preserve buffered input during hit stop and never move the authoritative player into danger only for visual recoil.
- Prefer small local presentation helpers over a large juice framework.
- Cap particles/trails on constrained targets and set a minimum acceptable frame rate.

### 5. Apply in impact-per-effort order

Apply only supported effects, in this order:

1. event confirmation: hit flash, short impact particles, landing response;
2. impact weight: hit stop or restrained camera kick;
3. motion expression: tilt, squash/stretch, easing and anticipation;
4. world consistency: give relevant enemies, hazards, projectiles, and rewards an appropriate response;
5. high-speed polish: trails and afterimages;
6. character expression only when register and on-screen size support it.

### 6. Validate in play

Compare before/after at normal speed and inspect a rendered high-feedback frame.

- Controls remain immediate and buffered input is not dropped.
- Visual bounds do not misrepresent collision bounds.
- Player, primary hazard, and reward remain readable during the busiest effect stack.
- Strongest feedback is reserved for the most important events.
- Effects return to rest without accumulation/leaks.
- Performance remains within the target budget.

If polish materially changes hazard readability or practical difficulty, rerun only reachable balance/mechanic checks—not a full telemetry sweep by default.

## Reference routing

- [technique-catalog.md](references/technique-catalog.md) — concrete effects and crisp-game-lib/Godot/other 2D-engine adaptations.
- `directing-game-visuals` — reuse existing palette/hierarchy decisions; do not invoke it only to satisfy a dependency.
