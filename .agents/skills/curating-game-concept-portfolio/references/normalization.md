# Concept Normalization

Normalize each supplied idea before comparing it. Do not reward concepts for longer or more persuasive prose.

## Minimal record

- `id` (stable across ranking, selection, and handoff)
- `one_sentence_core`
- `key_decision`
- `state_read`
- `progress_conversion`
- `risk_coupling`
- `skill_expression`
- `signature`
- `hard_reject`, `hard_reject_reason`, and typed evidence with provenance, if demonstrated
- `evidence_scores`, if evidence exists
- `provenance` for imported or derived evidence/status claims
- `unknowns`

## Signature axes

Use short categorical labels:

- `time_model`
- `control_topology`
- `state_topology`
- `primary_operation`
- `progress_conversion`
- `risk_coupling`
- `information_model`
- `failure_shape`
- `skill_channel`

Examples of useful categorical values:

- primary operation: evade / intercept / transform / allocate / route / combine / split / trade / commit / predict / construct / destroy / mixed / other;
- progress conversion: collect / survive / chain / convert / deliver / territory / solve / race / exhaust-opponent / build-state / mixed / other;
- risk coupling: same-action-creates-risk / danger-enables-reward / reward-consumes-safety / delayed-debt / opportunity-cost / adversarial / independent / mixed / other.

## Missing details

Do not silently infer a favorable mechanic just to complete the record. Use `unknown` for material missing relationships. For script input, omit unknown signature axes rather than inventing values.

When comparing candidates, present the normalized fields in the same order and granularity before or beside pitch prose. Imported stress-test classifications may be retained with provenance, but they are not automatic evidence scores or hard rejections.
