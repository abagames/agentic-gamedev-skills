# Retro Arcade Concept Format, Evaluation, and Spec

## Per-Concept Format (13 fields)

Generate each concept with all of these fields:

1. **Title**
2. **One-sentence concept**
3. **Player controls** (movement + one button; state what the button does)
4. **Core rules**
5. **Enemy / obstacle types** (max 3; one rule per type, 1-2 sentences each)
6. **Score system** (must reward in-world event causality, not raw input)
7. **Risk-for-reward element**
8. **What worsens over time** (the numerical escalation lever)
9. **Guarantee that randomness will not feel unfair** (how instant deaths are prevented)
10. **Differentiators from existing games**
11. **Lives system and miss conditions** (what consumes a life)
12. **Attract-mode highlight** (the specific moment that looks great in auto-play)
13. **Audio identity** (representative SFX and jingle direction, in one phrase)

## Evaluation Rubric

After generating 5 concepts, score all 5 against each criterion and justify briefly:

- Ease of implementation
- Clarity of rules
- Works on a single screen
- Low dependency on level design
- Strength of risk/reward
- Replayability
- Differentiation from existing games
- Attract-demo visual appeal
- Ease of implementation within 256x224 / 16x16 sprite / 64-color constraints

Then select the 2 most promising concepts. Prefer concepts that score well on *low level-design dependency* and *differentiation* — those are the hardest to recover later and the easiest to fake at the concept stage.

## Implementation Specification Template

For each of the 2 selected concepts, produce:

```markdown
# <TITLE> — Implementation Spec

## Screen Layout
<HUD vs playfield regions on the fixed screen; key fixed positions>

## Object List
<player, each enemy/obstacle type, projectiles, rewards: shape, size, behavior>

## State Transitions
<spawn -> active -> hit/miss -> despawn; player miss -> respawn; wave -> next wave>

## Collision Detection
<which rectangles/points are tested against which; what each collision triggers>

## Difficulty Escalation Formula
<initial values, growth cadence, and expected range for each numerical lever,
 e.g. speed = base + k*wave, spawn_interval = max(min, start - step*wave)>

## Game-Over Condition
<lives reach zero; what a miss costs; how the run ends and loops>
```

## Notes

- The hardware numbers (256x224, 16x16 sprites, 64 colors, 8x8 tiles) are the 1978-1983 era default. If a project brief specifies different limits, substitute those and keep the rest of the procedure.
- Use the target/avoid direction lists in `SKILL.md` as ideation seeds, then deliberately deviate from the most obvious interpretation of each seed.
