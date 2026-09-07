# Concept Record

Use this compact record for root concepts and mutations. YAML, JSON, or a table is acceptable.

## Required fields

- `id`: stable identifier that does not change with rank, shortlist position, or handoff.
- `lineage`: `root` or parent id plus mutation label.
- `one_sentence_core`: player action + consequence + pressure.
- `player_goal`: what the player tries to improve, preserve, reach, discover, or complete.
- `key_decision`: recurring choice that should require reading state.
- `actions`: player operations, including intentionally unavailable actions when relevant.
- `state_read`: state that can change the preferred action.
- `automatic_dynamics`: what changes without player action.
- `progress_conversion`: how action becomes score, progress, territory, survival, or win state.
- `risk_coupling`: how the progress-seeking behavior creates cost, danger, commitment, or lost opportunity.
- `skill_expression`: what a better player should do differently from an obvious simple policy.
- `learning_change`: what can become newly exploitable after several attempts.
- `signature`: normalized structural signature.
- `evidence`: named observations or reasoning traces.
- `provenance`: source and method for every imported or derived evidence/status claim.
- `unknowns`: unresolved claims.
- `status`: `root`, `survives`, `weak`, `hard_reject`, or `duplicate`.

## Signature axes

Use short categorical values, not promotional prose.

- `time_model`: realtime / discrete-tick / turn / simultaneous-turn / phase-based / other.
- `control_topology`: direct-avatar / cursor-target / lane-choice / allocation / routing / placement / selection / mixed / other.
- `state_topology`: continuous-space / grid / graph / queue / stack / slots / cards-hand / scalar-gauges / mixed / other.
- `primary_operation`: evade / intercept / transform / allocate / route / combine / split / trade / commit / predict / construct / destroy / mixed / other.
- `progress_conversion`: collect / survive / chain / convert / deliver / territory / solve / race / exhaust-opponent / build-state / mixed / other.
- `risk_coupling`: same-action-creates-risk / danger-enables-reward / reward-consumes-safety / delayed-debt / opportunity-cost / adversarial / independent / mixed / other.
- `information_model`: perfect / local / hidden / stochastic / delayed / predictive / mixed / other.
- `failure_shape`: collision / depletion / overflow / deadlock / deadline / opponent / invalid-state / opportunity-loss / mixed / other.
- `skill_channel`: timing / aiming / planning / inference / memory / prioritization / prediction / dexterity / mixed / other.

## Evidence vocabulary

Write observations, for example:

- `idle cannot progress because the delivery counter advances only on committed routes`;
- `greedy immediate reward consumes the only escape token in the next state`;
- `safe and risky actions are equivalent under the stated rules`;
- `unknown: spawn distribution is unspecified`.

Do not record `fun: 8/10`, `interesting: high`, or similar holistic judgments as evidence.

When comparing candidates, show these normalized fields in the same order and granularity before or beside any pitch prose. A later stress-test classification may be attached with provenance, but do not convert `fails`, `weak`, `unknown`, or `survives` into this record's `hard_reject` status or into an ordinal evidence score without separate qualifying evidence.
