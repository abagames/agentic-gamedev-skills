---
name: designing-one-button-games
description: "Designs original one-button mini-games using tap, hold, and release controls, with emphasis on novelty, risk/reward, and a short difficulty curve. Use when planning mechanics, scoring, game-over conditions, and difficulty curves for games controlled by a single binary input. For multi-button mini-games, use `designing-mini-games` instead."
---

# Designing One-Button Mini-Games

A library-agnostic guide for designing one-button mini-games. The aim is an intuitive, visually self-explanatory game that rewards skilled play and contains at least one mechanic the player has never seen before.

## When to Use

- Invent a new one-button game from a theme, prompt, or set of inspiration tags.
- Audit an existing one-button design for monotonous-input dominance, unfair death, or lack of novelty.
- Decide between competing mechanic ideas before implementation.

This skill covers **design only**. Implementation details (rendering, collision, audio) belong to engine-specific skills such as `developing-with-crisp-game-lib` or the target engine's implementation skill.

Design deliverables should still name implementation-facing invariants when balance depends on them. An invariant is a testable rule the later implementation must preserve, such as "repeated taps within 12 frames cannot create another scoring pulse." Do not write engine code here; write the rule that implementation must uphold.

At design time, keep constants qualitative unless the balance claim depends on a threshold. It is acceptable to write "minimum-age bloom" or "short cooldown" here, then defer choosing frame counts to the implementation pass, derived from the intended action cycle. If a deterministic seed or generator does not exist yet, state the seed/precheck invariant now and mark the actual first-case check as an implementation-time validation item.

## Companion skills

- `designing-mini-games` — use instead when the brief allows two or more buttons.
- `implementing-gameplay-invariants` — use after or alongside this skill when turning idle / hold-only / mashing weaknesses into code-level invariants and validation checks.
- `maximizing-game-feel` — use after core rules and balance are stable, or when readability/polish could affect play.

## Core Rules (one-button-specific)

- One binary input only — tap (press), hold, or release. No second key, no chord, no swipe.
- Game-over is single, visually obvious, and follows from a hazard or world-state collapse — never from a "did not press" punishment.
- Mashing, hold-only, and idle play must each be strictly worse than skilled play.
- Score must come from in-world causality (close calls, precise timing, chain reactions), not raw input facts (taps per second).
- Every important state variable must have a trigger, visible in-world feedback, and a decision purpose. Do not add bookkeeping state that does not change player decisions.
- Designs with zero state variables are valid when complexity emerges purely from geometric or physical interaction. If no state variables are used, justify why the interaction space alone creates decisions.
- If an input phase grants safety or power, pair it with a readable cost: lost scoring, resource drain, exposure, larger hitbox, speed, pressure, or recovery time.
- Prefer causal scoring events such as stomp, graze, batch erase, precise catch, cluster clear, route selection, or pressure cash-out. Survival score is acceptable only when survival itself is the core mastery signal; if used, explicitly state what skilled survival pattern separates good play from idle, hold-only, or mashing.
- State which quantities scale with difficulty and why. Use `sqrt(difficulty)` as the default for smooth motion/spawn pressure, and use steeper scaling only when the design intentionally needs escalating pressure.
- For each monotonous-input weakness that balance depends on, state at least one implementation invariant. The invariant should be testable without naming a specific engine API.

## Design Procedure

Phase 1: Idea generation

1. **Free Association**: verbalize the first images and sensations the input or seeds evoke. *If the seeds visibly contradict each other (e.g. `on_pressed:jump` + `on_pressed:shoot`), read `references/one-button-design-guide.md` §7 (Tag / Prompt Contradiction = Creative Tension) before continuing — do not pick one and discard the other.*
2. **Deviation Exploration**: verbalize the first mechanic that comes to mind, record it explicitly, then treat it as forbidden. Consider opposites, negations, and extremes; push toward unexpected directions. Do not proceed with the first association as the final design.
3. **Core Experience Decision**: define the momentary sensation the player should feel, in a single phrase.
4. **Mechanics Construction**: design the single tap / hold / release that realizes that sensation.

Phase 2: Specification hardening

5. **State and Tradeoff Definition**: name the state variables that create decisions, their triggers, their in-world feedback, and the safe/risky behavior pair.
6. **Monotonous-Input Rejection**: write why idle, hold-only, and mashing each lose to skilled play. If a phase is intentionally unused, say why the remaining phases still create skill.
7. **Scoring and Difficulty Definition**: define the causal scoring event and the quantities that scale with difficulty.
8. **Implementation-Invariant Sketch**: for each risky weakness claim, add the implementation rule that must make it true. Expand this into a fuller invariant translation when the design has pulses, shields, charge, combos, or repeated scoring windows.

Phase 3: Verification

9. **Emergence Review**: if implementation revealed a behavior not in the original spec, document it and decide whether to preserve it as a design revision. Unintentional but interesting mechanics should be formalized rather than fixed away.
10. **Consistency Verification**: run the checklist below.

> Treat seeds as stimulus for steps 1–2. From step 3 onward, do not be bound by them. A finished design that no longer references the original tags is fine.

## Design Quality Checklist

- [ ] Does it complete with one button (no second input required)?
- [ ] Is the game-over condition single and visually obvious?
- [ ] Are button mashing, hold-only, and idle play strictly suboptimal, and does the deliverable explicitly include `Idle weakness`, `Hold-only weakness`, `Mashing weakness`, and `Skilled play` bullets?
- [ ] Does each important monotonous-input weakness include at least one testable implementation invariant?
- [ ] Does the design document the state model and tradeoff, or explicitly justify the absence of state variables with a geometric/physical decision space?
- [ ] Can you give a reasoned answer to all four principles in §2 of the reference guide?
- [ ] Is score tied to an in-world causal event? If using survival score, is survival itself the central skill expression?
- [ ] Are persistent consequences or safety costs specified where needed (lost multiplier, shrinking space, fuel drain, crumbling platform, cooldown, exposed hitbox, etc.)?
- [ ] Does the design state what scales with difficulty and why?
- [ ] Did the idea start from the seed but contain elements beyond it?
- [ ] Is there a "I've never seen this before" moment?
- [ ] Is this **not** a clone or minor variation of a widely-known existing game?
- [ ] **For new-design tasks**, does the document capture the required content (name + slug, seeds, core mechanics, state/tradeoff, object specs, design principle analysis, basis for novelty, similarity check)? See `references/one-button-design-guide.md` Appendix A for an example layout.

## References

- `references/one-button-design-guide.md` — self-contained design vocabulary for one-button games: four core principles, input/movement/environment tables, state/tradeoff checks, abstract-question prompts, contradiction-as-tension table, recommended output format, and SCAMPER appendix.
