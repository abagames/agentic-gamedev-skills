# Spec Preservation Checklist

Load this while writing the reproduction spec (procedure step 1). It is the detailed
preserve-vs-drop rule set; the SKILL.md body only names the categories.

The guiding test for every detail: **does it change observable behavior, risk, timing,
scoring, failure, or the dominant strategy?** If yes, preserve it. If it is purely
presentational, drop it.

## Preserve

- **Constants, ranges, thresholds, formulas** that affect balance, difficulty, or timing.
- **Same-tick ordering.** Add an explicit ordering rule whenever the order of operations
  within one tick changes scoring, collision, spawning, state transitions, input edges, or
  failure. Give such rules stable IDs (e.g. `RULE-ORDER-01`) so they can be referenced.
- **Collision/geometry semantics** — collision shape, hitbox scale, distance thresholds,
  overlap rules, and draw-order-dependent collision — when they affect scoring, failure,
  safety, or strategy.
- **Collision footprints of "drawn" objects (dual-use cosmetic).** When collision is
  drawn-sprite/shape overlap, the *dimensions* of the colliding objects are behavior-critical
  even though their *art* is cosmetic: a sprite's size/shape and any drawn hazard's radius and
  thickness define the actual win/lose thresholds. Preserve those dimensions (and that a given
  sprite is a collision surface) while still dropping color, animation frames, and styling.
  Do not file the whole object under "cosmetic" just because it is rendered.
- **Rendered attributes that carry a rule are not cosmetic**, even when that attribute is
  usually droppable:
  - a *color* that a collision or state check keys on (e.g. "collides with the red box",
    "safe only while shown in color X"), or that is the player's only readout of
    lethal-vs-safe / vulnerable-vs-safe, must be preserved as a state cue and collision key;
  - *coordinates* that define the playfield, track, lane, or spawn/base geometry are
    load-bearing — only a one-off decorative position is cosmetic.
- **Spawn & selection** — spawn timing, target-selection rules, random ranges/probabilities —
  when they affect risk, timing, or which policy dominates.
- **Input-edge behavior** — press vs. release vs. hold vs. tap edges, debounce, toggles — when
  the edge (not just the state) drives an outcome.
- **Reusable pulses** — any scoring or safety action that can be repeated cheaply, since these
  are where dominant/degenerate strategies hide.
- **Game-specific terms** — define each at first use.

## Express Clearly

- For complex physics, targeting, collision, chained propagation, or input-edge state
  machines, use **numbered steps or pseudocode** rather than prose when prose would be
  ambiguous about order or condition.

## Drop

- Decorative rendering details — colors, sprites, exact coordinates, sound labels — unless they
  affect player decisions, state recognition, or game feel.
- Source structure (function/file organization, naming) that does not change play.
- Redundant prose restating the same rule.

## Self-Check Before Gating

- Could a reader reproduce the dominant strategy and the failure conditions from this spec
  alone, without the source?
- Is every preserved constant tied to a behavior it affects (not copied "just in case")?
- Is every same-tick interaction that matters covered by an ordering rule?
