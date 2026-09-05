---
name: migrating-agents-md-to-control-flow
description: "Audits repositories that rely heavily on AGENTS.md, CLAUDE.md, copilot instructions, or similar agent instruction files, then migrates repeatable workflows into skills, mandatory checks into scripts/hooks/CI, and leaves only stable repo context, policy, and workflow entrypoints in repo instructions. Use when the agent is asked to reduce long natural-language agent instructions, create agent skills from repo workflows, codify mandatory checks, or produce an instruction migration report."
---

# Agent Instruction Migration

## Purpose

Use this skill when a repository depends on large agent instruction files such as `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or equivalent docs for both repository context and workflow execution.

The goal is to move repeated or mandatory behavior into the right control surface without replacing
one giant prose file with giant generated prompts hidden in skills or scripts.

## Resources

Load `references/failure-modes.md` during final review or when a candidate migration feels weak.

Bundled scripts, relative to this skill directory:

- `scripts/validate-migration-skill.sh <skill-dir>`: validate this skill or a generated migration skill.
- `scripts/validate-migration-report.sh <migration-report.md>`: validate required migration report sections.

## Applicability Gate

Proceed with migration when at least two are true:

- agent instructions are long, duplicated, or frequently re-read
- the repo contains repeated workflows agents are expected to follow
- important steps are often skipped unless written in prose
- some rules are mechanically checkable
- existing scripts or CI already encode part of the workflow
- the project will likely be maintained or revisited

Prefer audit-only output when most are true:

- instructions are short and mostly stable context
- the workflow is one-off or unlikely to recur
- rules depend mostly on taste, product judgment, or human approval
- no meaningful checks can be scripted
- migration would create more files than behavior change
- the repo is being archived with no expected future work

If uncertain, produce a report and recommend against file changes until the user confirms the migration value.

## Routing Model

Extract distinct operational rules, split rules that span categories, and assign each rule exactly one
primary target:

| Rule shape | Primary target |
| --- | --- |
| Stable repository context, architecture constraints, naming, edit boundaries | Concise `AGENTS.md` policy |
| Approval boundaries for dependencies, schemas, production config, external contracts, or critical deletion | Concise `AGENTS.md` policy; never automate away approval |
| Reusable workflow that still needs judgment after deterministic checks are removed | `skills/<name>/SKILL.md`, only if the Skill Candidate Test passes |
| Mechanically checkable behavior such as lint, schema/file validation, drift checks, formatting, or builds | `scripts/`, hooks, CI, or task-runner entries |
| Required ordering, blocking gates, retries, fallbacks, or machine-readable state | Task runner, script, CI, hook configuration, or orchestrator |

Ask "can this be runtime control flow?" before creating a skill. Use the LLM for interpretation,
tradeoffs, explanation, and residual-risk analysis; use deterministic mechanisms for mandatory or
mechanically decidable behavior. Label prose-only required behavior as advisory unless an actual
script, hook, CI job, task runner, or orchestrator enforces it.

## Procedure

1. Discover instruction surfaces:
   Inspect `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, README workflow sections, docs mentioning required agent behavior, helper scripts, CI, and hook/config files. Record path, purpose, context/procedure/enforcement type, and freshness.

2. Extract actionable statements:
   Normalize each instruction into a concise operational rule such as "Run tests after edits" or "Ask for approval before adding dependencies." Do not preserve rhetorical wording.

3. Classify and model rules:
   Use the routing model above. For each repeated or mandatory workflow candidate, sketch:

   ```text
   inputs -> states -> deterministic checkpoints -> success/failure status -> next action
   ```

   Include required inputs, ordered states, blocking checks, retry/fallback behavior, machine-readable output if useful, LLM-only judgment, stop conditions, and escalation conditions.

4. Decide each candidate's target:
   Record each candidate as create skill, update existing skill, merge, keep in `AGENTS.md`, convert
   to script/hook/CI, convert to orchestration, or reject. Check existing repo-local and available
   skills before creating a new one, and apply the Skill Candidate Test below before choosing a skill.

5. Produce a migration report before broad edits:
   Write `migration-report.md` with these sections:

   1. Summary
   2. Workflow Migration Gate Decision
   3. Instruction Sources Found
   4. Rule Inventory
   5. Classification Table
   6. Runtime Shapes and Control-Flow Candidates
   7. Scriptable Checks and LLM-Only Judgments
   8. Proposed Migrations
   9. Files to Generate or Modify
   10. Control-Flow Assets Produced
   11. Skill Candidate Decisions
   12. Existing Skill Relationships
   13. Rules Intentionally Left in AGENTS.md
   14. Rules Not Safely Automatable
   15. Risks / Ambiguities
   16. Verification Plan
   17. Finalization State

   If the repo is large or ambiguous, stop here unless the user explicitly asked to apply changes.

6. Apply changes conservatively when requested:
   Shorten `AGENTS.md` without turning it into a stub. When a procedure moves into a skill, script,
   hook, CI job, task runner, or orchestrator, remove duplicated procedural prose from `AGENTS.md`;
   leave concise context, policy, approval boundaries, and workflow entrypoints that point to the new
   control surface. Produce only the approved artifacts: the report, updated instructions, qualifying
   repo-local skills, deterministic helpers, or control-flow configuration. For a generated skill,
   include a clear name and trigger, applicability boundaries, required inputs, an ordered procedure,
   validation, stop/escalation conditions, output expectations, and links to enforcing mechanisms.
   Keep project-specific lore out of skill bodies, and include concrete commands only when the skill
   is specifically about that tool, framework, or environment. Add hooks only for zero-exception behavior.

7. Review failure modes:
   Load `references/failure-modes.md` and verify no weak skill, README duplication, prompt relocation, false enforcement claim, fake state machine, unsupported policy inference, or unnecessary hook was introduced.

8. Validate:
   Run relevant existing tests or lightweight checks when safe. For this skill or generated migration skills, run `scripts/validate-migration-skill.sh`. For reports, run `scripts/validate-migration-report.sh`.

## Skill Candidate Test

Create or update a skill only when deterministic control flow is insufficient and most are true:

- It would help in at least three future tasks or repositories.
- It describes an agent action, not background knowledge.
- It is a repeatable procedure with validation.
- It includes non-trivial judgment that cannot be replaced by a script, hook, CI job, task runner, schema check, or short `AGENTS.md` policy.
- It invokes or references deterministic checks for mandatory behavior.
- It avoids asking the LLM to perform checks that a script could perform.
- It prevents a known failure mode or skipped workflow.
- It remains useful after removing project-specific names.
- It is better than README content, a script comment, an issue, or a report note.

Reject candidates that merely relocate long instructions without an executable checkpoint, clearer entrypoint, or real judgment procedure. Prefer no new skill over a narrow, repo-specific, or low-reuse skill.

## Safety Boundaries

Do not automatically:

- delete large documentation sections without replacement
- enable hooks with destructive side effects
- add expensive or noisy hooks for situational behavior
- change CI behavior unless the user asked for it
- infer approval policy not present in the repo
- invent architectural constraints unsupported by repository evidence
- claim enforcement without an actual enforcing mechanism
