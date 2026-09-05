# Post-Creation Empirical Tuning Gate

Load this file after drafting a recommended `SKILL.md` to decide whether empirical prompt tuning is worth applying.

The methodology itself lives in a separate skill called `empirical-prompt-tuning`. Locate it in this priority order before treating it as unavailable:

1. **Local skill (preferred):** look inside the same skills collection (typically `.agents/skills/empirical-prompt-tuning/SKILL.md` or equivalent). If present, use that as the methodology source.
2. **External fallback:** [https://github.com/mizchi/skills/blob/main/empirical-prompt-tuning/SKILL.md](https://github.com/mizchi/skills/blob/main/empirical-prompt-tuning/SKILL.md)
3. **Degraded fallback:** if neither is reachable, run the `Minimum tuning loop` at the end of this file as a best-effort substitute and explicitly report `empirical tuning: degraded (methodology source unreachable)` in the final note.

Do not skip the gate decision just because the external URL is unreachable; check the local skill first.

This file only governs the **gate decision** for skills produced by the extraction procedure.

## Apply empirical prompt tuning when

- The skill is expected to be reused frequently.
- The skill controls expensive, destructive, or hard-to-debug agent behavior.
- The skill was extracted from a failed or ambiguous project.
- The skill depends on non-obvious trigger conditions.
- The skill contains branching procedures or judgment rules.
- Previous agents have misunderstood similar instructions.
- The skill will be shared with other agents or users.

## Usually skip empirical prompt tuning when

- The skill is a small one-off helper.
- The skill is experimental and may be discarded soon.
- The user only needs a rough draft.
- No separate executor or subagent environment is available.
- The cost of testing exceeds the expected reuse value.

## Minimum tuning loop

If applying tuning, at minimum:

1. Check consistency between the skill description and body.
2. Prepare 2–3 realistic use scenarios, including at least one edge case.
3. Define a requirements checklist before running the test.
4. Have a fresh executor apply the skill to each scenario.
5. Record unclear points, discretionary fill-ins, failures, and excess steps.
6. Apply the smallest fix that addresses the observed ambiguity.
7. Repeat only while the improvement justifies the cost.

Do not treat self-review as empirical validation.

Self-review is structural review. Empirical validation requires observing how the skill is applied.
