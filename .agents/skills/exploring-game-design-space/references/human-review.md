# Human Review Contract

Human review is an execution-dependent investment checkpoint, not a required fourth workflow stage. For this skill, use it after exploration when the next action would be costly testing or prototyping.

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

- `preference` records desired experience, aesthetics, or product priority. It is design input, not evidence or a hard rejection.
- `observed_human_evidence` requires both a named `test_context` and a recorded `observation`, with provenance retained. Never infer it from a preference or approval.
- `approval` records an investment decision. It is neither an evidence score nor proof that a concept is correct.

In an interactive run, present stable IDs and equal-format normalized mechanism records before or beside pitch prose, then request review if it changes the next investment. In an unattended or batch run, leave unanswered entries absent and complete with `status: review_pending`, known uncertainty, and the recommended next decision.
