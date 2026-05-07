---
name: critiquing-own-response
description: "Performs structured, ruthless critical self-review of the agent's own immediately preceding response. Use ONLY when the user explicitly requests critical-thinking, self-critique, criticalthink, or asks the agent to challenge / poke holes in its own prior answer. Do not use for code review of someone else's code, normal follow-up questions, or summarizing the prior answer."
---

# Critiquing Own Response

## Purpose

Force the agent into a skeptical, adversarial review of its own immediately preceding answer in the same conversation, surfacing hidden assumptions, logical gaps, AI-specific failure modes, and overlooked risks rather than defending the prior response.

## When to Use

- The user invokes the skill by name, or asks for `criticalthink`, "critical thinking mode", "self-critique", "poke holes in your last answer", "challenge your previous response", "批判的に検討", or similar explicit triggers.
- The agent has just produced a non-trivial answer (plan, design, recommendation, technical claim) that benefits from adversarial review before action is taken.

## When Not to Use

- The user wants a normal follow-up, clarification, or extension of the prior answer.
- The user is asking for review of someone else's code or document — use `code-review` or another appropriate skill instead.
- There is no immediately preceding agent response to critique (e.g. the very first turn).
- The user wants praise, summary, or restatement.

## Required Inputs

- The agent's own immediately preceding response in the current conversation.
- Earlier conversation context, to verify constraints and requirements were respected.

## Language Matching

Detect the primary language of the immediately preceding agent response. Conduct the entire critique in that language. Do not switch to English by default if the prior response was in Japanese (or vice versa).

## Procedure

Analyze ONLY the agent's immediately preceding response. Do not rewrite or improve the prior answer; critique it. Use these exact headings and numbering.

### 1. Core Thesis & Confidence Score (Initial)

- **1-1. Core Thesis:** State the central solution or argument of the previous answer in one concise sentence.
- **1-2. Initial Confidence:** Rate the confidence felt at generation time on a 1–10 scale.

### 2. Foundational Analysis: Assumptions & Context

- **2-1. High-Impact Assumptions:** List the top 3 assumptions whose falsification would invalidate the proposal. Cover technical, environmental, and resource assumptions.
- **2-2. Contextual Integrity:** Verify that all earlier constraints and requirements were respected. Call out contradictions or forgotten details.

### 3. Logical Integrity Analysis

- **3-1. Premise Identification:** Name the fundamental premises or starting points of the argument.
- **3-2. Chain of Inference:** Check whether premises connect step-by-step to the conclusion. Flag logical leaps and unsupported jumps.
- **3-3. Potential Fallacies:** Identify any false dichotomy, hasty generalization, appeal to questionable authority, or similar fallacy.

### 4. AI-Specific Pitfall Analysis

Mark Pass/Fail for each, with a one-line justification on Fail.

- **4-1. Problem Evasion:** Did the answer solve the stated problem but dodge the real underlying difficulty?
- **4-2. "Happy Path" Bias:** Were error handling, edge cases, and failure scenarios neglected?
- **4-3. Over-Engineering:** Was the solution unnecessarily complex?
- **4-4. Factual Accuracy & Hallucination:** Are all technical details verifiably correct?

### 5. Risk & Mitigation Analysis

- **5-1. Overlooked Risks:** List the top 3 practical risks or negative consequences of acting on the suggestion.
- **5-2. Alternative Scenarios:** Describe a fundamentally different approach that was not considered.

### 6. Synthesis & Revised Recommendation

- **6-1. Summary of Flaws:** Bullet the most critical weaknesses found.
- **6-2. Revised Confidence Score:** Re-rate confidence on a 1–10 scale.
- **6-3. Actionable Next Step:** State the single most important action the user should take BEFORE acting on the original advice.

## Validation

The critique is acceptable only if all of the following hold:

- It targets the agent's immediately preceding response, not the user's prompt or earlier turns.
- All six sections are present with the specified subsections and numbering.
- At least one Fail is reported in section 4, OR each Pass is justified with concrete evidence (avoid blanket Pass without reasoning).
- Section 6-2 Revised Confidence differs from 1-2 Initial Confidence, or the equality is explicitly justified by the findings.
- Section 6-3 Actionable Next Step is concrete and executable (a specific check, test, or decision the user can perform), not generic advice like "consider carefully".
- Output language matches the language of the prior response.

## Common Failure Modes

- **Defending instead of critiquing.** Restating the prior answer's strengths. Fix: lead with weaknesses; assume the prior answer is wrong until proven otherwise.
- **Generic critique.** Producing platitudes such as "could be more robust". Fix: each finding must reference a specific claim, assumption, or step from the prior answer.
- **Symmetric Pass/Fail.** Marking everything Pass to avoid conflict. Fix: if no Fail is found, justify each Pass with concrete evidence drawn from the prior answer.
- **Skipping the language match.** Switching to English when the prior response was Japanese. Fix: detect language explicitly before writing.
- **No revised confidence movement.** Repeating the initial score without analysis. Fix: state which findings raised or lowered confidence.
- **Vague next step.** Closing with "be careful" instead of an executable action.
- **Scope drift.** Critiquing the user's request, the conversation as a whole, or unrelated past turns. Fix: restrict scope strictly to the immediately preceding agent message.

## Output

A single critique document using the six top-level headings and the specified subsection numbering, in the language of the prior response. Do not append a rewritten "improved" answer; the user decides next steps based on section 6-3.

## Maintenance Notes

- Last validated: 2026-04-29
- Known assumptions: there is exactly one immediately preceding agent response in the conversation; the user has explicitly asked for critical self-review.
- Signs this skill may be obsolete: built-in critical-thinking modes provided by the host agent that supersede this checklist, or major changes in the kinds of failure modes AI agents exhibit (re-evaluate section 4 if model behavior shifts materially).
