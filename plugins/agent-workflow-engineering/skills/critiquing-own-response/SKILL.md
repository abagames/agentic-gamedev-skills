---
name: critiquing-own-response
description: "Reviews the agent's own immediately preceding response as an advisory pass, surfacing assumptions, reasoning gaps, alternatives, and unverified claims. Use ONLY when the user explicitly asks for self-critique, critical thinking, or challenges to the agent's prior answer. Do not use for normal follow-ups, someone else's work, automatic checking, or independent quality assurance."
---

# Critiquing Own Response

Use only when the user explicitly requests critique of the agent's own immediately preceding response and that response exists. Analyze that response only, not the user, unrelated turns, or the whole conversation. This same-model critique shares the original answer's blind spots; it is advisory and never verification or formal review of a high-impact change.

Write entirely in the primary language of the preceding response.

## Procedure

1. State the response's central claim or recommendation in one sentence.
2. Identify the assumptions it depends on, prioritizing any whose failure would invalidate the claim.
3. Point to specific skipped reasoning, overreach, or conflict with an earlier constraint.
4. Give a concrete counterexample or alternative the response omitted.
5. Separate verified evidence from asserted but unverified claims.
6. State whether the findings raise, preserve, or lower confidence, and name the finding that moved it.

Every finding must cite a specific claim, assumption, or step in the preceding response. Do not manufacture weaknesses; when a category has no real finding, say so briefly.

## Output

```text
Core claim:
Important assumptions:
Potential failure modes:
Counterexamples or alternatives:
Evidence still needed:
Revised confidence: higher | unchanged | lower
```

Close with the single most useful next check when one exists. Do not assign a numeric confidence score or rewrite the answer; the user decides what to act on.
