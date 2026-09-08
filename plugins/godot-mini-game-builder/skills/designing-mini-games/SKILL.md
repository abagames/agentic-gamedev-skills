---
name: designing-mini-games
description: "Designs original, compact mini-games — rules, controls, scoring, hazards, and difficulty curves — for any input scheme, including one-button (tap / hold / release) games. Use when defining a new mini-game concept, converting creative constraints or seeds into mechanics, choosing an input scheme, checking state-variable necessity, or preventing idle, hold-only, or mashing play from becoming optimal."
---

Design or audit compact games for any input scheme. This skill owns rules, controls, scoring, hazards, difficulty intent, and engine-neutral invariants—not rendering, collision code, audio implementation, or numeric tuning.

Keep constants qualitative unless a balance claim requires a threshold. Defer frame counts to implementation from the intended action cycle. When deterministic generation does not exist yet, specify the seed/precheck invariant and mark the first-case check for implementation-time validation.

## Core Rules

- Express the core experience in one sentence. Fix button count and the role of each phase/button before secondary systems; respect a brief's count and record the **physical binding** for every action so screens cannot invent conflicting keys.
- Game-over is single, visually obvious, and follows from a hazard or world-state collapse — never from a "did not press" punishment.
- Make every available monotonous policy strictly worse than skilled play: idle and mashing always; hold-only for one-button; single-button spam and hold-everything for multi-button.
- Score in-world causes (precision, graze, chain, route, pressure cash-out), never raw input facts. Keep survival score only when survival is the mastery signal and name the skilled pattern that separates it from monotony.
- Add state only for a new player decision. Each important variable needs a trigger, in-world feedback (never only a HUD number), and a decision purpose; otherwise remove it. Zero-state designs are valid when geometry/physics alone creates decisions—say why.
- Pair safety/power inputs with a readable cost such as lost score, drain, exposure, hitbox, speed, pressure, or recovery.
- Name which quantities scale and why. Default smooth motion/spawn pressure to `sqrt(difficulty)`; use steeper scaling only for intentional escalation.
- For every balance-critical monotony claim, give at least one testable, engine-neutral implementation invariant.

One-button-specific rules:

- One binary input only: press, hold, release—no second key, chord, or swipe.
- Explicitly justify unused phases; never add a meaningless action to fill a table.

## Design Procedure

1. **Associate:** state the first images/sensations. For contradictory seeds (for example, `on_pressed:jump` plus `on_pressed:shoot`), read the reference guide §7 and treat the contradiction as tension; do not discard one side.
2. **Deviate:** record the first obvious mechanic, forbid it, and explore an opposite, negation, or extreme.
3. **Commit:** state the momentary core experience, then fix button count, bindings, and phase/button roles.
4. **Harden:** define decision-making state, triggers, in-world feedback, and safe/risky tradeoffs.
5. **Reject monotony:** explain why every applicable monotonous policy loses and why remaining inputs still create skill when a phase is unused.
6. **Specify economy:** define causal score events and justified difficulty scaling.
7. **Sketch invariants:** state the implementation rule behind each risky claim; expand pulses, shields, charge, combos, and repeated score windows with `implementing-gameplay-invariants`.
8. **Verify:** run reference guide §9. If implementation exposed an emergent behavior, document it and explicitly preserve it as a design revision or reject it.

> Treat seeds as stimulus for steps 1–2. From step 3 onward, do not be bound by them. A finished design that no longer references the original tags is fine.

For a new design, deliver: name/slug, seeds, core mechanics, state/tradeoff, object specifications, design-principle analysis, novelty basis, similarity check, causal scoring, difficulty intent, controls/bindings, and implementation invariants. Use reference Appendix A as a layout example.

## References

- `references/mini-game-design-guide.md` — detailed principles, input/movement tables, contradiction handling, checks, output format, and SCAMPER prompts.
- `implementing-gameplay-invariants` — translate risky balance claims into code-level checks.
- `maximizing-game-feel` — use after rules/balance stabilize or when polish affects play.
