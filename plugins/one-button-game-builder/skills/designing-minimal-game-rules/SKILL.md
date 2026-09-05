---
name: designing-minimal-game-rules
description: "Turns an abstract game-design seed into a minimal discrete-state rule system by generating conflict-axis candidates, stress-testing with Rule Breaker and Strategy Breaker roles, then reducing to the smallest surviving core. Use when designing a compact turn-based or step-based game that must work without numeric tuning, manual level design, or aesthetic polish."
---

# Designing Minimal Game Rules

Produce a small rule machine that survives basic rule, strategy, and reachability attacks before implementation. Reject candidates whose appeal depends on numeric tuning, manual content, exception rules, or presentation quality.

## Core test

Every surviving candidate must answer:

```text
What does the player want?
Why is that same thing dangerous?
Why does safe play lose score?
Why does high-score play damage the future?
Does this happen without exception rules?
```

The target is a discrete-state, turn-based, or step-based game using a small board, queue, gauge, list, slot set, or similar state space. Do not apply this workflow to real-time physics or precision-action games.

## Input

Use the available seed to identify:

- priority conflict axis;
- score source, danger source, and their causal connection;
- candidate state spaces;
- obvious dominant strategies and premature genre assumptions to attack;
- which quality-dependent elements must be removed.

Infer missing fields and label the assumptions.

## Workflow

### 1. Generate conflict cores

Create eight one-sentence candidates in the form “The player wants A, but A also creates danger B.” Reject renamed genres, separated score/danger systems, manual level design or content volume, high implementation load, and candidates defeated by always-wait, always-defend, always-maximize, or always-minimize. Keep the smallest three.

### 2. Specify three rule machines

For each, define: name, strange core, conflict axis, diagnostic label, state variables and initial state, player operations, automatic update, score, failure, turn order, and invariants. If entities move, state whether accumulated state travels with them or remains in place.

### 3. Break rules and strategies independently

Read [breaker-roles.md](references/breaker-roles.md), then run its Rule Breaker and Strategy Breaker against each candidate. Use independent subagents when the runtime supports them; otherwise use isolated sequential passes that see only the candidate and preceding findings. Breaker passes report defects and must not silently repair them.

For every strong simple strategy, ask whether it succeeds without reading current state. Explicitly test greedy use of every visible score/danger value and any fixed contextual targeting rule.

### 4. Edit by reduction

Repair only after breaker findings. Apply the canonical repair order in [breaker-roles.md](references/breaker-roles.md); keep repairs reductive and causal rather than additive. Do not add rescue actions, exception events, currencies, shops, complex AI, or local numeric patches.

### 5. Trace or simulate

Run the Simulation Breaker rules in [breaker-roles.md](references/breaker-roles.md). Use exact simulation only when rules are sufficiently defined; otherwise provide a labeled 3–5 turn manual trace and mark uncertain conclusions.

Record survival, score, failure reason, operation usage, unused variables, repeated best actions, action economy, visible-greedy results, and reachability. Numeric comparison diagnoses structure here; it is not permission to tune the game into working.

### 6. Reduce again

Remove unused or duplicate variables, unused operations, extra failure conditions, exception rules, numeric-only repairs, and genre-shaped residue. State the strangest structural feature that remains. If none remains, report that the result may be safe but weak.

### 7. Produce the result

Load [final-output-template.md](references/final-output-template.md) only at output time. Keep the audit log compressed, distinguish exact simulation from manual trace, and justify any high-cost element such as physics, precision input, shops, deckbuilding, complex AI, solver-dependent generation, rescue rules, exception events, or status effects.

## Completion criteria

- all terms, targets, and same-turn ordering are defined;
- score and danger are causally coupled;
- no tested simple strategy dominates without state reading;
- automatic danger growth is compatible with the player's action economy;
- the scoring target and failure condition are reachable under at least one tested policy;
- every remaining variable and operation changes a decision;
- uncertainty and rejected candidates are visible in the output.

## Companion skills

- Use `designing-mini-games` instead when the input is already a formed action-game concept.
- Use `evaluating-gameplay-balance` for an implemented game's telemetry and tuning, not for this pre-implementation rule reduction.
