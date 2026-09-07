# Human Review Contract

Human review is an execution-dependent investment checkpoint, not a fourth mandatory workflow stage. For this skill, place it after curation and before material implementation or publication investment.

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
- `approval` is an investment decision, not an evidence score or proof that a concept is correct.

Present stable IDs and equal-format normalized mechanism records before or beside pitch prose. Interactive work may request review when it changes the investment decision. Unattended or batch work must not block: omit invented entries, return the portfolio and open questions, and complete with `status: review_pending`.
