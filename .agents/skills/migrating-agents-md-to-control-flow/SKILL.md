---
name: migrating-agents-md-to-control-flow
description: "Audits repositories that rely heavily on AGENTS.md, CLAUDE.md, copilot instructions, or similar agent instruction files, then migrates repeatable workflows into skills, mandatory checks into scripts/hooks/CI, and leaves only stable repo context, policy, and workflow entrypoints in repo instructions. Use when the agent is asked to reduce long natural-language agent instructions, create agent skills from repo workflows, codify mandatory checks, or produce an instruction migration report."
---

# Agent Instruction Migration

## Purpose

Use this skill when a repository depends on large agent instruction files such as `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or equivalent docs for both repository context and workflow execution.

The goal is to move repeated or mandatory behavior into the right control surface:

- `AGENTS.md`: stable repo context, architecture constraints, approval policy, and workflow entrypoints
- `skills/`: broadly reusable agent workflows that still require judgment after deterministic checks are factored out
- `scripts/`: executable checks, enumeration, validation, and helper commands
- hooks, CI, task runners, or orchestrators: mandatory ordering, blocking gates, retries, and machine-readable state
- reports: what moved, what stayed advisory, and what remains risky

Do not replace one giant prose file with giant generated prompts hidden in skills or scripts.
Do not treat skill creation as the default outcome of control-flow migration.

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

## Core Heuristics

Ask "can this be runtime control flow?" before creating a skill. Skill creation is a fallback for reusable judgment-heavy workflows, not the first destination for extracted prose.

Prefer deterministic control flow for:

- mandatory ordering
- required validation before proceeding
- retries or fallback branches
- artifact existence or freshness checks
- forbidden paths or operations
- machine-readable status
- repeated command sequences
- pass/fail decisions that do not require product judgment

Use a skill only when the workflow needs agent judgment, repository interpretation, or flexible problem solving after scriptable checks have been removed. Skills should call or reference deterministic checks where those checks exist.

Do not create skills for:

- a single command sequence with fixed pass/fail behavior
- one-off migration notes or temporary project state
- project background, rationale, or roadmap context
- rules that are better represented as concise `AGENTS.md` policy
- checks that can be expressed as scripts, hooks, CI, task runners, or schema validation

Label prose-only required behavior as advisory unless a script, hook, CI job, task runner, or orchestrator enforces it.

Script checks when practical for:

- instruction surface discovery
- file existence and section/schema validation
- command sequencing
- generated-file drift checks
- forbidden-path checks
- required artifact checks
- skill frontmatter validation
- machine-readable summaries

Use the LLM for interpretation, classification, tradeoffs, concise explanation, and residual-risk analysis.

## Classification

Extract distinct operational rules from instruction surfaces and classify each into exactly one primary category. Split rules that span categories.

### A. Stable Repo Context

Architecture, directory ownership, invariants, preferred stack, naming conventions, forbidden edit zones, and approval boundaries.

Target: keep concise material in `AGENTS.md`.

### B. Reusable Workflow

Bug fix process, UI change process, release prep, dependency upgrade process, migration authoring process, or test triage sequence.

Target: move to `skills/<name>/SKILL.md` only if it remains useful as a repeatable agent procedure across future tasks or repositories after deterministic checks are factored out.

### C. Mandatory Executable Check

Lint/typecheck/test execution, instruction enumeration, schema validation, report validation, forbidden-path blocking, artifact checks, generated-file verification, screenshots, diff policy checks, formatting, and build verification.

Target: `scripts/`, hooks, CI, or task runner entries.

### D. Approval Policy

Dependency additions, schema changes, production config changes, external API contract changes, and deletion of critical assets.

Target: keep a concise statement in `AGENTS.md`; do not silently automate away approval.

### E. Deterministic Orchestration

Multi-step workflows with required ordering, checkpoint gates, retry limits, fallback paths, structured manifests, task runners, package scripts, Makefiles, CI workflows, or hook coordination.

Target: task runner scripts, Makefile/package scripts, CI, hook configuration, or machine-readable status files.

## Procedure

1. Discover instruction surfaces:
   Inspect `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, README workflow sections, docs mentioning required agent behavior, helper scripts, CI, and hook/config files. Record path, purpose, context/procedure/enforcement type, and freshness.

2. Extract actionable statements:
   Normalize each instruction into a concise operational rule such as "Run tests after edits" or "Ask for approval before adding dependencies." Do not preserve rhetorical wording.

3. Classify rules:
   Use categories A-E above. For each repeated or mandatory workflow candidate, sketch:

   ```text
   inputs -> states -> deterministic checkpoints -> success/failure status -> next action
   ```

   Include required inputs, ordered states, blocking checks, retry/fallback behavior, machine-readable output if useful, LLM-only judgment, stop conditions, and escalation conditions.

4. Decide each candidate's target:
   Prefer script/hook/CI/orchestration for mandatory or mechanically checkable behavior. Record each candidate as create skill, update existing skill, merge, keep in `AGENTS.md`, convert to script/hook/CI, convert to orchestration, or reject. Check existing repo-local and available skills before creating a new one.

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
   Shorten `AGENTS.md` without turning it into a stub. When a procedure moves into a skill, script, hook, CI job, task runner, or orchestrator, remove duplicated procedural prose from `AGENTS.md`; leave concise context, policy, approval boundaries, and workflow entrypoints that point to the new control surface. Create narrow skills only for reusable judgment-heavy workflows. Create scripts for deterministic checks. Add orchestration when it exposes real pass/fail state. Add hooks only for zero-exception behavior.

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

## Output Requirements

Unless the user asks for analysis only, produce appropriate artifacts from this set:

- `migration-report.md`
- updated `AGENTS.md`
- one or more repo-local skill files, such as `.agents/skills/<skill-name>/SKILL.md` when that is the repository convention, only when the skill candidate test passes
- helper scripts under `scripts/`
- task runner, hook, or CI snippets/files when they add real control flow
- residual-risk notes in the report

When writing generated skills, include:

- clear name and trigger
- applicability boundaries
- required inputs
- ordered procedure
- validation
- stop and escalation conditions
- output expectations
- references to scripts, hooks, CI jobs, task runners, or status files when applicable

Keep project-specific lore out of skill bodies. Include concrete commands only when the skill is specifically about that tool, framework, or environment.

## Safety Boundaries

Do not automatically:

- delete large documentation sections without replacement
- enable hooks with destructive side effects
- add expensive or noisy hooks for situational behavior
- change CI behavior unless the user asked for it
- infer approval policy not present in the repo
- invent architectural constraints unsupported by repository evidence
- claim enforcement without an actual enforcing mechanism

## Final Checklist

- Gate decision made and documented.
- Instruction sources inventoried.
- Operational rules extracted and classified.
- Runtime shape defined for repeated or mandatory workflow candidates.
- Deterministic control flow preferred for mandatory sequencing and validation.
- Scriptable checks scripted or explicitly left advisory with justification.
- Weak skill candidates rejected.
- Existing skills checked before new skills were created.
- Stable context, policy, approval boundaries, and short workflow entrypoints preserved in `AGENTS.md`.
- Duplicated procedural prose removed from `AGENTS.md` after equivalent skill/script/hook/CI/task-runner assets were created.
- Generated assets reviewed against `references/failure-modes.md`.
- Migration report produced when appropriate.
- Finalization state assigned to each generated or updated skill.
- Remaining advisory guidance clearly identified.
