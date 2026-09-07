# Human Review Contract

Human review is an execution-dependent investment checkpoint, not a substitute for adversarial analysis. For this skill, use it after a named prototype or playtest, or before a consequential next investment.

```yaml
human_review:
  checkpoint: post_exploration | post_named_test | pre_investment
  status: review_pending | completed
  concept_ids: [stable-concept-id]
  entries:
    - kind: preference | observed_human_evidence | approval
      statement: "..."
      test_context: "named build/ruleset/session; observed_human_evidence only"
      observation: "recorded behavior/reaction; observed_human_evidence only"
```

- `preference` is design input, not evidence or a hard rejection.
- `observed_human_evidence` requires both a named `test_context` and recorded `observation`, with provenance retained. Never infer it from preference or approval.
- `approval` is an investment decision, not an evidence score or concept verdict.

Interactive work may request review when it changes the next investment. Unattended or batch work must not wait for a response: omit invented entries, return the analysis and cheapest next discriminator, and complete with `status: review_pending`.
