---
name: critiquing-own-response
description: "Reviews the agent's own immediately preceding response as an advisory pass, surfacing assumptions, logical gaps, alternatives, and claims that remain unverified. Use ONLY when the user explicitly asks for self-critique, critical thinking, or for the agent to challenge or poke holes in its own prior answer. This is not independent quality assurance — it shares blind spots with the response it critiques. Do not use for normal follow-up questions, review of someone else's code, an automatic gate before finishing work, or a ritual self-check before every answer."
---

# Critiquing Own Response

## Purpose

Re-examine the agent's own immediately preceding answer from a skeptical stance, surfacing assumptions, logical gaps, unconsidered alternatives, and claims that were asserted without verification.

This is an advisory pass, not a verdict. It does not certify the prior answer as correct.

## When to Use

- The user explicitly asks for `criticalthink`, "critical thinking mode", "self-critique", "poke holes in your last answer", "challenge your previous response", "批判的に検討", or invokes this skill by name.
- The user asks the agent to examine the assumptions, reasoning, weaknesses, or counterexamples of its own immediately preceding answer.

## When Not to Use

- A normal follow-up, clarification, or extension of the prior answer.
- Review of someone else's code or document.
- An automatic check before finishing work, or a ritual self-check before every final answer.
- Formal review of a high-impact or irreversible change — that needs a reviewer who did not write the artifact and who works from the artifact and its verification results, not from this critique.
- There is no immediately preceding agent response to critique.

## Known Limitation

The critique comes from the same model that wrote the answer, in the same context. It inherits the same blind spots, so a clean critique is weak evidence of correctness. Report it as one perspective on the prior answer, never as verification.

## Required Inputs

- The agent's own immediately preceding response in the current conversation.
- Earlier conversation context, to check whether stated constraints and requirements were respected.

## Language Matching

Detect the primary language of the immediately preceding agent response and write the entire critique in that language.

## Procedure

Analyze ONLY the immediately preceding response. Critique it; do not rewrite it into an improved answer.

1. State its central claim or recommendation in one sentence.
2. Name the assumptions it depends on, prioritizing those whose falsification would invalidate it.
3. Identify where the reasoning skips a step, overreaches, or contradicts an earlier constraint in the conversation.
4. Give a concrete alternative or counterexample that the answer did not consider.
5. Separate what was verified from what was asserted. Name the specific claims still resting on nothing.
6. State whether the critique raised or lowered confidence in the answer, and which finding moved it.

Every finding must point at a specific claim, assumption, or step in the prior answer. If a section has nothing real to report, say so and move on. Do not invent a flaw to fill it.

## Output

```text
Core claim:
Important assumptions:
Potential failure modes:
Counterexamples or alternatives:
Evidence still needed:
Revised confidence: higher | unchanged | lower
```

`Revised confidence` records only the direction the critique moved confidence in, relative to how strongly the prior answer asserted itself. Do not produce a numeric score — a number assigned after the fact is a generated self-explanation, not a measurement.

Close with the single most useful next check if one exists. Do not append a rewritten answer; the user decides what to act on.

## Common Failure Modes

- **Defending instead of critiquing.** Restating the prior answer's strengths. Fix: lead with weaknesses.
- **Generic critique.** Platitudes such as "could be more robust". Fix: cite the specific claim or step being criticized.
- **Manufactured findings.** Inventing flaws so the critique looks thorough. Fix: an honest "nothing found here" beats a fabricated concern.
- **Scope drift.** Critiquing the user's request, the whole conversation, or unrelated earlier turns. Fix: restrict scope to the immediately preceding agent message.
- **Skipping the language match.** Switching to English when the prior response was Japanese.
- **Claiming verification.** Presenting the critique as confirmation that the answer is correct. Fix: see Known Limitation.
