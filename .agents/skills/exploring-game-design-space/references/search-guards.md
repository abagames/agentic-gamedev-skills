# Cheap Search Guards

These are lightweight verbal or hand-trace checks used inside concept exploration. They are not a substitute for deep prototype evaluation.

## Hard defects

A concept may be marked `hard_reject` when the stated rules demonstrate one of these:

- required progress or success is unreachable;
- failure is unavoidable before any meaningful decision;
- the core loop is internally contradictory or undefined;
- a state-blind policy such as idle, repeat-one-action, or always-greedy dominates every described alternative across the relevant states;
- nominal actions are strategically equivalent and no meaningful choice remains;
- the concept's claimed core value depends entirely on presentation/content outside the stated budget.

## Cheap simple-policy attacks

Consider, when applicable:

- idle;
- repeat one action;
- mash/random;
- always choose immediate safety;
- always choose immediate reward;
- always hoard or always spend;
- fixed target priority;
- fixed timing interval.

A simple policy being viable is not itself a defect. The defect is that it dominates the intended state-reading play.

## Agency check

For every claimed key decision, try to state two reachable situations where different actions are preferred for different reasons. If this cannot be done, mark `weak: possible agency collapse` rather than inventing depth.

## Unknowns that should survive to prototype

Do not reject automatically when value depends on:

- a narrow balance window;
- stochastic distributions not yet chosen;
- audiovisual timing or embodiment;
- authored surprise or narrative meaning;
- social behavior;
- long-horizon learning that cannot be inferred from the rules.
