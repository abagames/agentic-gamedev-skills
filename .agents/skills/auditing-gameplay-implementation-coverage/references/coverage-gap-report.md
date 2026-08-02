# CoverageGapReport

Return a compact report with this schema. Use file/line or document-section evidence where
available.

```yaml
subject:
  build:
  audited_artifacts: []
  authority_order: []
  known_exclusions: []

method:
  frozen_axes: []
  pruning_rules: []
  verification_harness:

summary:
  confirmed_novel_defects: 0
  implementation_gaps: 0
  presentation_gaps: 0
  probe_gaps: 0
  spec_conflicts: 0
  intent_questions: 0
  unverified: 0

findings:
  - id: GAP-<surface>-<number>
    status: confirmed-defect | implementation-gap | presentation-gap | probe-gap | spec-conflict | intent-unknown | unverified
    novelty: novel | known
    obligation_id:
    obligation:
    derivation: explicit | structural-sibling | metamorphic | producer-consumer | boundary
    authority:
    implementation_evidence:
    observable:
    existing_test:
    expected:
    observed:
    reproducer: []
    inverse_case:
    impact:
    proposed_probe:
    human_decision_required:

covered_high_risk:
  - obligation_id:
    obligation:
    distinguishing_test:

unexamined_scope: []
effect_evidence:
  novel_confirmed_findings: []
  adjudicated_false_positives: []
  coverage_delta: []
  recall: unknown-on-live-build
```

## Evidence Rules

- `confirmed-defect` requires a reproducible expected/observed mismatch against explicit authority.
- `implementation-gap` requires explicit authority and a complete enough code census to support
  `none found`; otherwise use `unverified`.
- `presentation-gap` requires a documented decision-changing state plus inspection of the reached
  screen.
- `probe-gap` requires existing behavior and a proposed assertion that fails under a named omission.
- `spec-conflict` does not decide which side is correct; put that decision in
  `human_decision_required`.
- `intent-unknown` is a useful result, not a softened defect claim.
- `effect_evidence` must exclude every item listed in `known_exclusions`.

## Measuring This Procedure Itself

Only relevant when the audit is the subject rather than the tool.

Freeze the procedure before applying it. On a live build the defect denominator is unknown, so
report precision of adjudicated findings and coverage deltas — newly confirmed findings and
adjudicated false positives — and do not report recall. When recall or generalization has to be
measured, run it against hidden defective cases plus a clean control, so both a miss and a
fabricated finding are observable.

