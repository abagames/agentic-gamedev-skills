# Visual Design Guide

A guide for designing the visual layer of action mini-games using visual tags as creative seeds. Parallel to the `designing-mini-games` skill (which covers mechanics), this document covers screen composition, rendering style, feedback effects, and visual coherence.

## 1. Design Challenges

- Establishing a visually distinctive identity with minimal art assets.
- Ensuring gameplay readability — every object's role must be instantly recognizable.
- Making action feedback (hits, scoring, danger) feel satisfying through visuals alone.
- Maintaining visual coherence when combining multiple tag directions.

## 2. Four Core Visual Principles and Evaluation Criteria

### (1) Readability

- Principle: The player must instantly distinguish their character, threats, collectibles, and safe zones. Use contrast in color, brightness, size, and motion — not labels or icons.
- Evaluation: Can a first-time player identify every object's role within 2 seconds of seeing it?

### (2) Feedback Clarity

- Principle: Every meaningful game event (scoring, damage, near miss, state change) must produce a visible response. The magnitude of visual response should match the magnitude of the event.
- Evaluation: Can the player tell what happened without looking at the score counter? Is the difference between "scored 1 point" and "scored 10 points" visually obvious?

### (3) Aesthetic Coherence

- Principle: All visual elements — objects, background, particles, UI — must feel like they belong to the same world. A shared rendering style (stroke weight, color temperature, motion quality) unifies the screen.
- Evaluation: Does any element feel visually out of place? Would removing any one element break the visual identity?

### (4) Dynamic Life

- Principle: Nothing on screen should be perfectly static. Subtle motion (breathing, pulsing, drifting) keeps the world alive. Object motion should communicate physics and weight, not just position change.
- Evaluation: Does the game feel alive even when the player is not pressing anything? Do objects feel like they have mass and inertia?

## 3. Role of Visual Tags

Visual tags follow the same philosophy as mechanism tags from the `designing-mini-games` skill:

- **Stimulus, not constraint**: Tags suggest a visual direction; the final design may depart from them.
- **Contradiction is opportunity**: Conflicting tags create unique visual identities (see §7).
- **Deviation allowed**: No problem if the final visual cannot be explained by tags alone.
- **Purpose**: Prevents LLM from defaulting to generic visual styles.

## 4. Visual Tag Categories

### 4.1 Category Overview

| Category | Role | Design Impact |
|:---|:---|:---|
| `render-*` | How objects are drawn | Stroke style, fill, outline treatment for all game objects |
| `geometry-*` | Shape language | What primitives and compositional rules define the visual vocabulary |
| `motionviz-*` | Motion visualization | How movement, impact, and energy are made visible |
| `background-*` | Background treatment | Dynamic backdrop style and atmospheric depth |
| `lighting-*` | Light and atmosphere | Edge glow, depth cues, fog, bloom compositing |
| `analog-*` | Organic imperfection | Jitter, shimmer, noise, chromatic artifacts |
| `typography-*` | Text integration | How scores, labels, and glyphs exist in the game world |
| `composition-*` | Screen layout | Spatial organization, negative space, visual hierarchy |

> Note: Typography implementation and font licensing policy belongs in the engine/platform-specific typography skill for the target project.

### 4.2 Category Interaction Map

Categories are not independent. Typical synergies:

| Combination | Effect |
|:---|:---|
| `render-*` + `lighting-*` | Render style defines edges; lighting adds atmosphere on top |
| `geometry-*` + `composition-*` | Shape vocabulary fills the spatial structure defined by composition |
| `motionviz-*` + `analog-*` | Motion effects gain organic texture from analog imperfections |
| `background-*` + `lighting-*` | Background and lighting together define the depth/atmosphere stack |
| `typography-*` + `geometry-*` | Glyphs become geometric entities when both tags are present |

## 5. Procedure for Visual Design from Tags

Design in the following order after the core mechanics are defined.

1. **Tag Interpretation**: Read each tag's `description` and `keywords`. Verbalize the mood, texture, and motion quality they suggest.
2. **Cross-Tag Synthesis**: Find the visual theme that unifies all selected tags. Express it in one phrase (e.g., "pulsing neon organisms," "crisp geometric clockwork").
3. **Mechanics Integration**: Identify where visual style intersects with game mechanics:
   - Which visual technique best communicates the core mechanic?
   - Which game events deserve the strongest visual response?
   - Does the visual style suggest new feedback opportunities the mechanics design didn't consider?
4. **Palette Decision**: Choose 3–5 colors derived from the tag mood. Assign each color a gameplay role. Typical roles include Player, Threat, Background, Positive feedback, Warning — but adapt roles to the game's actual needs (e.g., a game with state-switching may need State-A / State-B instead of fixed Threat / Warning).
5. **Layer Structure**: Define visual depth layers:
   - Background (atmospheric, low contrast)
   - Play field (mid layer, primary action)
   - Foreground effects (particles, flashes, UI)
6. **Feedback Mapping**: For each game event, define the visual response using the tag style:
   - Score gain → (e.g., additive glow burst, ripple expansion)
   - Damage / game over → (e.g., chromatic split, screen shake)
   - Near miss → (e.g., subtle rim flash, trail intensification)
   - State change → (e.g., palette shift, geometry transformation)
7. **Checklist Verification**: Confirm with the checklist in §10.

## 6. Mechanics × Visual Integration Patterns

Visual design is not decoration — it communicates game state. The following patterns show how visual tags directly serve gameplay.

### 6.1 Game Feel Techniques

Apply these to **all objects** (player, enemies, obstacles, items), not just the player. Consistent application across objects creates a cohesive "lively" world.

| Technique | Description | Relevant Visual Tags |
|:---|:---|:---|
| **Squash & Stretch** | Deform objects on impact, jump, landing. Idle objects breathe subtly. | `motionviz-elastic-deformation`, `analog-micro-jitter` |
| **Dynamic Tilt** | Tilt objects toward movement direction. Spinning enemies rotate with velocity. | `motionviz-rotation-reactive`, `geometry-diagonal-dominance` |
| **Afterimage Trail** | Leave fading copies during fast movement. Apply to enemies and projectiles too. | `motionviz-afterimage-trail`, `analog-frame-blend` |
| **Impact Particles** | Scatter fragments on collision, destruction, landing, spawning. | `motionviz-impact-ripple`, `background-particle-layer` |
| **Glow Buildup** | Gradually intensify glow to telegraph danger or charge state. | `motionviz-energy-glow-build`, `lighting-additive-glow` |

### 6.2 Mechanic-to-Visual Mapping Examples

| Mechanism Tag | Visual Tag | Combined Effect |
|:---|:---|:---|
| `player-rotate` | `motionviz-velocity-hue-shift` | Color shifts with rotation speed — faster = warmer hue |
| `weapon-ray` | `render-glow-outline` | Laser rendered as bright emissive line with bloom halo |
| `obstacle-chase` | `motionviz-afterimage-trail` | Pursuing enemies leave ghost trails showing trajectory |
| `on_holding-charge` | `motionviz-energy-glow-build` | Held button builds visible glow around player |
| `field-auto_scroll` | `background-flow-lines` | Scrolling direction visualized by flowing streamlines |
| `rule-combo_multiplier` | `typography-numeric-focus` | Combo counter grows in size/brightness with multiplier |
| `on_pressed-reverse_state` | `analog-chromatic-offset` | State flip triggers brief RGB split across entire screen |
| `player-bounce` | `motionviz-elastic-deformation` | Bouncing object squashes on contact, stretches in air |

## 7. Visual Tag Contradiction and Creative Tension

When contradicting visual tags are given, invent a unified style, don't pick one.

| Contradiction | Conventional Approach | Creative Interpretation |
|:---|:---|:---|
| `render-wireframe-lines` + `lighting-additive-glow` | Choose wireframe OR glow | Wireframe lines that glow additively — luminous skeletal forms |
| `composition-negative-space` + `geometry-primitive-modularity` | Sparse OR dense | Dense clusters isolated in vast empty space — "islands of complexity" |
| `analog-micro-jitter` + `geometry-grid-alignment` | Organic OR geometric | Grid-locked positions that tremble with analog vibration — "restless order" |
| `background-noise-field` + `composition-centered-stage` | Noisy OR clean | Clean center surrounded by noisy periphery — noise as vignette |
| `typography-kinetic-motion` + `render-uniform-stroke` | Dynamic text OR static lines | Text moves but maintains uniform stroke — disciplined kinetics |

**Principle**: Same as mechanism tags — don't resolve the contradiction, invent a new concept that makes both true simultaneously.

## 7.1 VISUAL_DESIGN.md Required Addendum Template (AI-Generated Look Suppression)

When producing a visual design document, include the following section template verbatim and fill each field.

```markdown
## 7. AI-Generated Look Suppression Rules

### 7.1 Visual Hierarchy Rules

- Protagonist:
- Threat:
- Reward:
- 2-second recognition check:

### 7.2 Limits on Familiar Template Symbols

- Adopted familiar elements (max 2):
- Replaced unique element:

### 7.3 UI-Independent Feedback

| Event | Non-UI visual response | Intensity (Low/Med/High) |
| :---- | :--------------------- | :----------------------- |
| Score | ...                    | ...                      |
| Damage | ...                   | ...                      |
| Near miss | ...                | ...                      |

### 7.4 Composition and Gaze Guidance

- Initial focal point:
- Visual flow:
- Anti-center-clutter implementation:
```

## 8. Implementation Handoff

This guide defines visual direction and feedback semantics, not engine implementation.
After choosing an engine, translate the visual plan into that engine's rendering primitives.

Engine-specific implementation examples belong in engine-specific skills or project references, not in this visual-direction guide.

## 9. Output Format

Output in the following format to the project's visual design document.
If no visual tags were provided, replace `**Visual Tags**` with `**Concept-Derived Visual Tags**` and list 2-3 inferred tags based on material, geometry, motion, or atmosphere.

```markdown
# Visual Design: <GAME_NAME>

**Visual Tags**: #vtag1, #vtag2

## 1. Visual Concept

<Overall mood and direction in one phrase>

## 2. Color Palette

| Role | Color | Hex | Usage |
|:---|:---|:---|:---|
| <role_1> | ... | #... | ... |
| <role_2> | ... | #... | ... |
| <role_3> | ... | #... | ... |

Assign 3–5 roles based on the game's actual needs (e.g., Player, Threat, Background, Positive feedback, Warning — or substitute with game-specific roles like State-A / State-B).

## 3. Object Rendering Specifications

<Drawing style for each object, with reference to visual tags>

## 4. Background & Environment

<Dynamic background expression, layer structure>

## 5. Feedback Effects

| Event | Visual Response | Tag Reference |
|:---|:---|:---|
| Score gain | ... | ... |
| Damage | ... | ... |
| Near miss | ... | ... |
| Game over | ... | ... |
| State change | ... | ... |

## 6. Relationship with Visual Tags

<How each tag influenced the design decisions>
```

## 10. Visual Design Quality Checklist

The §2 evaluations cover readability, feedback clarity, aesthetic coherence, and dynamic life. Run those, plus this tag-handling check:

- [ ] Visual style is grounded in the selected tags but goes beyond literal interpretation (tags as seeds, not specifications).
