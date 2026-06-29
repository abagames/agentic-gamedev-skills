---
name: refining-workflows-from-artifacts
description: "Refines a reusable agent workflow based on an actual execution result, review, failure, or simulation output. Classifies problem causes (task/execution/workflow/evaluation/capability-boundary/output-format/overconstraint) before proposing the smallest workflow diff. Use when the user wants to improve a workflow, prompt, rubric, or agent skill after applying it to a real task."
---

# Refining Workflows from Artifacts

## Purpose

Improve a reusable agent workflow based on an actual execution result.

Do not use this to improve the artifact itself.
Use this to improve the workflow that produced the artifact.

The goal is to make the next run more reliable through a small, evidence-based workflow change.

## When to Use

- A workflow, prompt, skill, or agent process has been applied to a real task
- There is an artifact, review, test result, simulation result, or human concern to examine
- Similar tasks are expected to recur

## When Not to Use

- The artifact has no associated workflow to improve
- The problem is clearly a one-off task issue with no recurrence risk
- The goal is empirical prompt accuracy evaluation with subagent dispatch (use `empirical-prompt-tuning` instead)
- The goal is extracting reusable knowledge from a completed project (use `extracting-agent-skills` instead)

## Required Inputs

Use whatever is available:

```text
1. Current workflow or skill
2. Task, seed, or input used
3. Artifact produced
4. Review, test result, simulation result, or human concern
5. Whether similar tasks will recur
```

Proceed with explicit uncertainty if inputs are incomplete. Treat missing evidence as an evaluation limitation, not as proof of workflow failure.

## Core Principle

Do not treat every artifact failure as a workflow failure.

Classify the cause first. Only workflow-caused (C), evaluation-caused (D), and output-format-caused (F) problems should normally produce workflow changes.

For capability-boundary-caused problems (E), add a human review point, tool requirement, prototype test, or observation criterion — do not pretend the agent can verify it.

## Role Execution Model

When the runtime supports subagents, use independent reviewers for:

- Success Extractor
- Failure Classifier
- Workflow Diff Editor
- Deletion Reviewer

If subagents are unavailable, run them as isolated sequential passes. The Failure Classifier must classify causes before the Workflow Diff Editor proposes changes. The Workflow Diff Editor must not change the workflow for A (task-caused) or B (execution-caused) problems unless the same issue recurs across runs.

## Cause Classification

Classify each important issue as one of:

```text
A. Task-caused
   Input was ambiguous, excessive, contradictory, or not testable.

B. Execution-caused
   The workflow said what to do, but the agent failed to follow it.

C. Workflow-caused
   The workflow lacked a needed step, criterion, output field, or repair rule.

D. Evaluation-caused
   The success or failure standard was unclear.

E. Capability-boundary-caused
   Verification requires tools, prototypes, human testing, or external data.

F. Output-format-caused
   The result existed but was hard to inspect, reuse, compare, or audit.

G. Overconstraint-caused
   The workflow was too strict and damaged novelty, flexibility, or usefulness.
```

If unsure, classify conservatively as D or E. Do not add workflow rules from weak evidence.

## Procedure

1. Summarize the current workflow's intended purpose in 1–3 sentences.
2. Identify 1–3 things that worked.
3. Identify the most important problems (no hard cap — prioritize by impact).
4. Classify each problem by cause (A–G). For each C or F: (a) did this problem appear in more than one run — if only one, prefer "only if recurs" unless the structural gap is unambiguous; (b) would this problem arise with a different artifact in this same workflow — if it depends on artifact-specific features, prefer B over C.
5. Revise only C, D, and F problems. Leave A, B, E, G problems unless they recur.
6. Propose the smallest useful workflow diff (one theme at a time).
7. State likely side effects of each diff.
8. Name at least one deletion candidate.
9. Leave 1–3 validation points for the next run.

## Revision Priority

Apply changes in this order:

```text
1. Fix output format
2. Clarify inspection criteria
3. Change execution order
4. Shorten input format
5. Add repair rules
6. Split roles
7. Add constraints
8. Add human or external-tool intervention points
```

Constraints are a late remedy. Many failures come from poor output shape or missing cause classification, not from too few rules.

## Deletion Rule

Every refinement must name at least one deletion candidate:

- unused steps
- duplicated checks
- output fields that did not aid judgment
- roles that only produced prose
- constraints that weakened the artifact
- long sections that were not used

If deletion is risky, mark it "observe next run" rather than deleting immediately. If every candidate is deferred, state explicitly why no actual deletion was made this run.

## Capability Boundary

Easier to verify: format compliance, missing fields, explicit contradictions, unresolved definitions, simple strategy comparison, test-case coverage, repeated output failures.

Harder to verify: fun, taste, feel, beauty, rhythm, persuasion, brand fit, human satisfaction.

For hard-to-verify qualities, do not pretend certainty. Add human review points, prototype tests, sample comparisons, or observation criteria instead.

## Anti-Patterns

- Treating every artifact failure as a workflow failure, then adding constraints
- Rewriting the whole workflow every run
- Expanding checklists without deleting anything
- Making unverifiable qualities look verified
- Hiding uncertainty
- Turning a compact workflow into a bureaucracy

## Output

Load `references/improvement-log-template.md` at output time.

Keep changes small, reversible, and testable in the next run.

## Companion Skills

- `empirical-prompt-tuning` — empirical accuracy measurement of skills using subagent dispatch; use when you want to measure success rate across scenarios
- `extracting-agent-skills` — extracting reusable skills from completed or abandoned projects
