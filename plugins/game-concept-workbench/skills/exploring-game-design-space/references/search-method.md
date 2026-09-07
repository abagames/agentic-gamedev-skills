# Search Method

## 1. Force structural spread before ideation

Choose 3–5 axes relevant to the brief and pre-assign neighborhoods across concept slots. Useful axes:

- primary operation: intercept, transform, allocate, route, combine, split, trade, commit, predict, construct, destroy;
- progress conversion: chain, convert, deliver, territory, survival, race, solve, build-state, opponent exhaustion;
- risk coupling: same action creates danger, danger enables reward, reward spends safety, delayed debt, opportunity cost, adversarial pressure;
- state topology: continuous space, grid, graph, queue, stack, slots, hand, gauges;
- information: perfect, local, stochastic, delayed, predictive, hidden;
- skill channel: timing, planning, inference, prioritization, prediction, aiming, memory.

Record the first obvious concept suggested by the prompt. For at least half of the root population, forbid its core tuple of `primary_operation + progress_conversion + risk_coupling`.

## 2. Generate in batches

Generate 6–9 concepts at a time. After each batch, remove mechanical reskins before generating more. Do not rank during root generation.

A concept is weakly specified if it cannot answer:

1. What state does the player read?
2. What alternatives compete at the recurring decision?
3. How does an action change future options?
4. How does progress-seeking create danger, cost, or commitment?
5. What could an expert do that a state-blind policy cannot?

Weak specification is not automatically a hard rejection. Mark the missing causal link as unknown.

## 3. Anti-reskin test

Strip nouns and theme. Two concepts are structural neighbors when four of these five answers remain functionally equivalent:

1. state read before acting;
2. primary state transformation;
3. progress conversion;
4. risk coupling;
5. expert-vs-simple-policy distinction.

## 4. Mutation operators

Use a mutation only when it targets a named weakness or unexplored neighborhood.

- **invert coupling**: progress-seeking action also creates danger, or danger becomes the progress resource;
- **delay consequence**: move cost/reward into future state so short-term and long-term choices diverge;
- **cash-out**: stored potential matters only when committed under risk;
- **information mutation**: perfect → local/delayed/predictive, or make an action reveal information while changing state;
- **topology mutation**: continuous ↔ lanes/grid/graph, unordered pool ↔ queue/stack/slots, local state ↔ moving-entity state;
- **commitment mutation**: reversible action → prepare/commit, choose target before outcome, recovery consumes future opportunity;
- **hazard transformation**: hazard becomes redirectable/exploitable instead of merely avoidable;
- **reduction**: delete a state variable, merge reward and danger sources, or remove a rescue action so prevention emerges from the primary operation.

For every child record: parent, operator, exact rule change, expected behavioral change, and new risk introduced.
