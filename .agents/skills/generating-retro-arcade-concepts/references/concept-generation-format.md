# Retro Arcade Concept Format, Evaluation, and Spec

## Mechanism Signature Taxonomy

Four axes of abstract mechanisms (no game names involved). Axis 1 values are
pre-assigned to the 5 concept slots without replacement before ideation; the
other axes are declared per concept in field 14 and used for the within-slate
distinctness check (every pair of concepts must differ on >= 2 of the 4 axes).

- **Axis 1 — Reward conversion**: instant-scoring / carry-and-bank /
  streak-multiplier-upkeep / defense-survival / territory-conversion
- **Axis 2 — Risk shape**: proximity-daring / growing-liability /
  irreversible-commitment / timing-window / spend-to-score
- **Axis 3 — Core verb**: shoot / push / reflect / halt / carry / detach / place
- **Axis 4 — Threat source**: homing / ballistic-stream / environmental-cycle /
  self-generated

Axis 1 is a closed list — its five values are the slot-assignment currency.
Axes 2-4 are open: if a concept's true value is not listed, declare a new
self-named value rather than shoehorning it into the nearest label (the
declared label feeds both the distinctness check and the precedent match, so
a forced fit corrupts both).

## Per-Concept Format (14 fields)

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
14. **Mechanism signature** (the concept's value on each of the 4 taxonomy axes; axis 1 must match the slot's pre-assigned value)

## Evaluation Rubric

After generating 5 concepts, score all 5 against each criterion and justify briefly:

- Ease of implementation within the hardware constraints (256x224 / 16x16 sprites / 64 colors, or the project brief's limits)
- Clarity of rules
- Works on a single screen
- Low dependency on level design
- Strength of risk/reward
- Replayability
- Differentiation from existing games (well-known commercial games only — never this project's own shipped games; score only via the Nearest-Precedent Check below)
- Attract-demo visual appeal

### Nearest-Precedent Check (mandatory before scoring differentiation)

For each concept, in this order:

1. Recall at least 2 well-known commercial candidates that resemble the concept, searching *adversarially* — try to defeat the concept's novelty, not defend it. Match on mechanism (economy, risk shape, verb, threat source), never on theme or fiction.
2. Name the single nearest precedent and write out its mechanism signature on the same 4 taxonomy axes.
3. Count matching axes M (0-4), then add one sentence naming the strongest concrete rule-level overlap beyond the axes.
4. Apply the score cap mechanically: M=4 → differentiation ≤ 1; M=3 → ≤ 2; M=2 → ≤ 3; M ≤ 1 → 4-5 allowed. The cap is a ceiling, not the score — the rule-level-overlap sentence may justify scoring below it, never above.
5. State recall confidence. If the precedent's mechanics may be misremembered, or the design space is one where obscure/doujin/post-cutoff precedents are plausible, say so explicitly. This check catches known-but-unretrieved precedents only; it cannot prove novelty, and external novelty verification remains a human-review responsibility.

### Selection

Then select the 2 most promising concepts. Prefer concepts that score well on *low level-design dependency* and *differentiation* — those are the hardest to recover later and the easiest to fake at the concept stage. The 2 selections must differ on the reward-conversion axis (or, when a brief-level economy override is in effect, on the risk-shape axis); if the two best scorers share it, promote the next-best concept with a different value and note the substitution.

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
