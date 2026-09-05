---
name: maximizing-game-feel
description: "Improves the tactile satisfaction (\"game feel\") of action games whose visuals are functional but flat. Use when a game runs correctly but feels lifeless; applies to players, enemies, obstacles, projectiles, and items."
---

# Maximizing Game Feel

Improve the response and readability of an already-working action game. Consider every important object category, but apply only effects justified by that object's role and event; uniform polish creates noise.

## Workflow

### 1. Establish the baseline

Inspect current entities, collision bounds, rendering hierarchy, feedback helpers, performance constraints, and any visual-direction artifact. Identify the specific moments that feel weak—movement start/stop, jump/land, hit, kill, spawn, reward, near miss, or state change—before choosing techniques.

For a substantial project, record the chosen register, weak moments, effect budgets, and validation thresholds in `FEEL_TUNING.md`. For a one-file mini-game, use a short README or source-header note instead. Do not create documentation heavier than the implementation.

### 2. Choose the expressive register

Infer tone from the title, object names, shapes, palette, and existing direction. Follow an existing `directing-game-visuals` artifact when present.

| Register | Prefer | Avoid |
|---|---|---|
| Character/playful | pronounced squash, eyes, lively overshoot, particles | effects that obscure small characters |
| Abstract/minimal | tilt, trails, light pulses, restrained particles | faces and cartoon deformation |
| Serious/tense | weighty impact, restrained deformation, short camera kick | bouncy or noisy feedback |

When uncertain, choose the more restrained register. Motion and light generalize better than faces or bounce.

### 3. Map events to a small feedback vocabulary

Select effects by event and gameplay importance, not by object category alone. Consider players, enemies, movable hazards, fixed hazards, projectiles, and rewards, then explicitly choose an effect or `none` for each important event.

Keep distinct vocabularies:

- danger: sharp silhouettes, alert flashes, sparks, short hard impacts;
- reward: glints, radial particles, softer pops, bright confirmation;
- state change: localized pulse, transition motif, controlled camera response;
- near miss: satisfying but visibly weaker than an actual reward.

Read [technique-catalog.md](references/technique-catalog.md) when selecting or implementing squash, tilt, eyes, particles, trails, easing, hit flash, hit stop, camera response, or recoil. It also contains engine-specific constraints.

### 4. Implement presentation without corrupting mechanics

- Keep gameplay and collision state authoritative. Apply deformation, rotation, trails, and flashes to render-only visuals where the engine permits it.
- Clamp every deformation and camera displacement, and return it to rest.
- Gate costly or disruptive effects by speed, charge, impact value, or event rarity.
- Preserve buffered input during hit stop and never move the authoritative player into danger only for visual recoil.
- Use small local helpers or presentation components instead of building a large juice framework for a mini-game.
- Cap active particles and trails for Web, mobile, and low-end targets; define a minimum acceptable frame rate when performance is at risk.

### 5. Apply in impact-per-effort order

Choose only effects supported by the game:

1. event confirmation: hit flash, short impact particles, landing response;
2. impact weight: hit stop or restrained camera kick;
3. motion expression: tilt, squash/stretch, easing and anticipation;
4. world consistency: give relevant enemies, hazards, projectiles, and rewards an appropriate response;
5. high-speed polish: trails and afterimages;
6. character expression such as eyes, only when the register and on-screen size support it.

### 6. Validate in play

Compare before/after behavior at normal play speed and inspect at least one rendered frame from a high-feedback moment.

- Controls remain immediate and buffered input is not dropped.
- Visual bounds do not misrepresent collision bounds.
- Player, primary hazard, and reward remain readable during the busiest effect stack.
- Strongest feedback is reserved for the most important events.
- Effects return to rest and do not accumulate or leak.
- Performance remains within the target budget.

If polish materially changes hazard readability or practical difficulty, rerun only the relevant balance or mechanic check. Do not trigger a full telemetry sweep merely because effects changed.

## Reference routing

- [technique-catalog.md](references/technique-catalog.md) — load when choosing concrete effects or adapting them to crisp-game-lib, Godot, or another 2D engine.
- `directing-game-visuals` — use its palette and hierarchy decisions when they already exist; do not invoke it only to satisfy a dependency.
