---
name: designing-minimal-game-rules
description: "Turns an abstract game-design seed into a minimal discrete-state rule system by generating conflict-axis candidates, stress-testing with Rule Breaker and Strategy Breaker roles, then reducing to the smallest surviving core. Use when designing a compact turn-based or step-based game that must work without numeric tuning, manual level design, or aesthetic polish."
---

# Designing Minimal Game Rules

## Purpose

Turn an abstract game-design seed into a minimal game rule system.

The goal is not to expand a fun-sounding idea.
The goal is to reject weak ideas early and keep only a rule machine that survives basic attacks.

Reject ideas that rely on:

- dominant simple strategies
- undefined rule machinery
- high implementation load
- manual level design
- visual polish, animation quality, or content volume
- numeric tuning as the main source of fun
- exception rules or rescue buttons

## When to Use

- designing a discrete-state, turn-based, or step-based small game
- the input is an abstract seed (not a fully formed concept)
- the goal is a rule system that survives strategy attacks before any implementation

Scope: small boards, slots, queues, gauges, lists, or abstract state spaces; few inputs; rules explainable in about one minute.

## When Not to Use

Do not use for action games, physics games, or precision timing games, or for games whose appeal depends primarily on feel or aesthetics. For those, use an input-model and prototype-testing workflow instead.

## Required Input

The seed should provide these fields. Infer missing ones and state assumptions explicitly.

```text
- Priority conflict axis:
- Score source:
- Danger source:
- Score-danger connection:
- Candidate state spaces:
- Dominant strategies to watch:
- Premature concretizations to watch:
- Quality-dependence reduction policy:
```

## Core Principle

The player should want something that is also dangerous.

Every candidate rule core must answer all five:

```text
What does the player want?
Why is that same thing dangerous?
Why does safe play lose score?
Why does high-score play damage the future?
Does this happen without extra exception rules?
```

## Role Execution Model

Run these roles as independent subagents when the runtime supports it.
If subagents are unavailable, run them as isolated sequential passes — each pass reads only the current candidate rules and prior pass outputs. A breaker pass must not silently repair what it finds.

| Role               | Priority |
| ------------------ | -------- |
| Rule Breaker       | High     |
| Strategy Breaker   | High     |
| Simulation Breaker | High     |
| Editor             | Medium   |
| Final Reducer      | Medium   |
| Designer           | Low      |

### Designer

Create small rule candidates from: state, operations, automatic update, scoring, failure condition, turn order.

Must not add theme, lore, content volume, upgrades, shops, complex AI, or manual level design.

### Rule Breaker

Find rule-machine failures. Check:

- undefined terms, ambiguous timing, unclear targets
- impossible updates, non-firing updates, runaway loops
- ambiguous simultaneous processing
- danger that never appears or appears too much
- variables that never change
- visible state tracks that do not change any decision
- automatic danger growth that can outpace the player's per-turn repair capacity

Must not fix rules or add mechanics.

### Strategy Breaker

Attack the rules with these simple strategies:

- always safest action
- always highest score action
- always highest visible score / largest visible payout, ignoring hidden state
- always most dangerous target
- always lowest value target
- always wait
- always first legal target
- always same positional rule
- if the player operation is contextual, always apply it using the same target-selection rule
- ignore one visible state track at a time

For each strong strategy ask: does it require reading the current state? If it works without state reading, it is a dominant-strategy warning.
For any visible number used in scoring or danger, include at least one strategy that greedily maximizes that visible number.

Must not tune numbers or add mechanics.

### Editor

Repair only after breaker findings. Prefer deletion, merging, target changes, causal rewiring, replacing permanent effects with temporary effects, merging score source and danger source.

Must not add exception rules, rescue actions, special events, extra currencies, shops, or complex AI.

### Simulation Breaker

Compare simple strategies via traces. Goal: expose weak rules, dead variables, unused operations, obvious dominant strategies. Not optimal play search.

Must not search for optimal play or tune the game.

Also run an action-economy check:

- Count how many independent hazards can worsen per automatic update.
- Count how many hazards one player operation can repair or cash out.
- If several hazards can worsen while only one can be handled, flag it unless trace/simulation shows reachability without making positional or greedy strategies dominate.

### Final Reducer

Remove everything not structurally necessary: unused variables, duplicate variables, unused operations, extra failure conditions, exception rules, numeric-only fixes, genre-shaped residue.

Must not make the game safer by adding rules.

## Procedure

### 1. Generate one-sentence mechanics

Create 8 candidates in this form:

```text
The player wants A.
But A also creates danger B.
```

Reject any that: are renamed existing genres; separate score and danger; require heavy implementation or manual content; become obvious with always-wait, always-defend, always-maximize, or always-minimize; concretize the seed prematurely.

Keep the smallest 3.

### 2. Create 3 minimal rule candidates

For each, specify:

```text
Name:
Strange core:
Conflict axis:
Diagnostic label:
State variables:
Initial state:
Player operations:
  (If an operation moves entities: state whether accumulated state variables travel with them or stay in place.)
Automatic update:
Score condition:
Failure condition:
Turn order:
Invariants:
```

### 3. Rule breaker pass

For each candidate, check all items from the Rule Breaker role.

For important issues, provide a 3–5 turn trace:

```text
Initial state:
Action:
Changed variables:
Score effect:
Danger effect:
Freedom/space effect:
Problem after 3–5 turns:
```

### 4. Strategy breaker pass

Test all strategies from the Strategy Breaker role.

For any strong simple strategy: does it work without reading the current state? If yes, it is a dominant-strategy warning.
Explicitly include greedy strategies based on visible score, visible danger, and any contextual one-button action target rule.

### 5. Edit by reduction

Fix problems in this order:

```text
0.  Define undefined terms
1.  Fix non-firing update conditions
2.  Localize danger growth
3.  Turn danger handling into scoring or positioning, not pure removal
4.  Remove operations
5.  Change operation targets
6.  Merge score source and danger source into the same object or variable
7.  Turn permanent effects into temporary effects
8.  Replace position dependence with state dependence
9.  Change auto-update direction
10. Simplify failure conditions
11. Replace an over-specific state space
12. Reject the candidate
```

Do not fix by adding exception rules, rescue buttons, special events, or local numeric patches.

### 6. Simulation or trace

If exact simulation is possible:

First — reachability check: run the strongest simple strategy until game-end or turn 20, whichever comes first.
If no strategy reaches the win condition within that range, flag the scoring target as uncalibrated.
If the game typically ends before turn 10, note it and shorten the comparison window to match.

Then — compare simple strategies across 12–20 turns (or the reachable game duration) and 3 fixed initial states.
For rules with countdowns, growing hazards, or refilling slots, include at least one trace long enough for each automatic cycle to complete once.

If exact simulation is not possible, provide a 3–5 turn manual trace and mark uncertain claims as uncertain.

Record per strategy: survival turns, score, failure reason, operation usage, variables that did not matter, repeated best action sequences.
Also record: action-economy result, visible greedy strategy result, and whether target score / failure limit appears reachable without letting a simple positional strategy dominate.

### 7. Final reduction

Remove: unused variables, duplicate variables, unused operations, extra failure conditions, exception rules, numeric-only fixes, genre-shaped elements not needed for the core conflict.

After reduction, state the strangest remaining structural feature.
If no strange feature remains, the design is probably safe but weak.

## High-Cost Elements

These require explicit justification if used (see output template field 14):

physics, real-time precision input, shops, deckbuilding, complex AI, solver-dependent generation, rescue buttons, exception events, status effects.

## Output

Load `references/final-output-template.md` at output time.

Keep the audit log compressed. Do not output long hidden deliberation.
Do not claim exact simulation if only a manual trace was used.

## Companion Skills

- `designing-mini-games` — controls-first practical design starting from a concrete idea; use when the input is a formed concept, not an abstract seed
- `evaluating-gameplay-balance` — simulation-based balance evaluation for already-implemented games
