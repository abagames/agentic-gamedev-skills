# Breaker Roles and Reduction Rules

Load this file before running breaker passes or simulation.

## Contents

- Isolation contract
- Rule Breaker
- Strategy Breaker
- Editor and Final Reducer
- Simulation Breaker

## Isolation contract

Use these roles in order: Rule Breaker → Strategy Breaker → Editor → Simulation Breaker → Final Reducer. Breakers report failures without repairing them. The Editor changes only defects already reported. The Final Reducer deletes after the revised candidate has been traced.

## Rule Breaker

Check for:

- undefined terms, targets, or timing;
- impossible, non-firing, or runaway updates;
- ambiguous simultaneous processing;
- danger that never appears or overwhelms immediately;
- variables that never change or never affect a decision;
- automatic danger growth that exceeds the player's repair/cash-out capacity.

For an important issue, give a 3–5 turn trace containing initial state, action, changed variables, score effect, danger effect, freedom/space effect, and the resulting failure.

## Strategy Breaker

Attack each candidate with every applicable policy:

- always safest action;
- always highest immediate score or payout;
- greedily maximize each visible number in turn;
- always most dangerous or lowest-value target;
- always wait;
- always choose the first legal target;
- always use the same positional or contextual target rule;
- ignore one visible state track at a time.

For each strong policy, record whether it must read current state. A policy that succeeds without state reading is a dominant-strategy warning. Do not tune numbers or add mechanics during this pass.

## Editor and Final Reducer

Apply repairs in this order and stop as soon as the structural defect is covered:

1. define missing terms and ordering;
2. fix non-firing updates;
3. localize danger growth;
4. make danger handling create score or position rather than pure removal;
5. remove operations or change their targets;
6. merge score and danger into the same object or variable;
7. make permanent effects temporary;
8. replace unnecessary position dependence with state dependence;
9. change automatic-update direction;
10. simplify failure conditions or state space;
11. reject the candidate.

Never repair by adding rescue buttons, exception rules, special events, extra currencies, shops, or complex AI. The Final Reducer must not make the game safer by adding rules.

## Simulation Breaker

The goal is to expose weak rules, not find optimal play or tune constants.

1. Run the strongest simple policy until game end or turn 20. If no policy reaches the score/win target, flag it as uncalibrated. If games normally end before turn 10, shorten later comparisons accordingly.
2. Compare applicable simple policies across 12–20 turns, or the reachable game duration, from three fixed initial states.
3. For countdowns, refills, or growing hazards, run long enough for every automatic cycle to complete once.
4. Count how many independent hazards worsen per automatic update and how many one player action can repair or cash out. Flag an unsupported mismatch.
5. Record survival turns, score, failure reason, operation use, variables that did not matter, repeated best sequences, visible-greedy results, and action-economy results.

When exact simulation is unavailable, use a 3–5 turn manual trace and mark all reachability or dominance claims that remain uncertain.
