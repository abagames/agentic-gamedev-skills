# Migration Skill Failure Modes

Load this file when reviewing generated skills, scripts, hooks, or a migration report before finalization.

## Skill Cemetery

Do not create a separate skill for every paragraph removed from `AGENTS.md`.
Too many weak skills reduce discoverability and increase stale instruction risk.

Prefer zero or one strong skill over several marginal skills.

## README Duplication

Do not move ordinary setup instructions into a skill unless they encode non-obvious agent behavior.

A README tells a human how to use the project.
A skill tells an agent how to act reliably.

## Prompt Relocation

Do not replace one long repo instruction file with long generated prompts hidden in skill bodies or scripts.

Skills should contain reusable procedures.
Scripts should execute, validate, enumerate, or prepare structured data.

## Missing Control Flow

Do not call a migration complete when mandatory sequencing remains dependent on the agent remembering prose.

If a rule requires order, blocking validation, retry, fallback, or stop behavior, prefer a script, hook, CI job, task runner, structured status file, or explicit orchestrator.

## Scriptable Check Left to the LLM

Do not ask the LLM to repeatedly inspect facts that a small script can check.

Script these when practical:

- instruction files present in the repo
- required report sections
- skill frontmatter validity
- expected output artifacts
- forbidden paths
- generated-file drift
- command sequence pass/fail status

Leave the LLM responsible for interpretation, classification, tradeoffs, and residual-risk explanation.

## Fake State Machine

Do not describe states in prose without creating a way to observe them when observation is needed.

Use machine-readable output, logs, status files, exit codes, or CI checks for workflows that need visible state.

## Project Lore Leakage

Do not include long explanations of why the repo exists, project history, roadmap context, or team narrative unless it changes future agent behavior.

Keep stable architecture and policy in `AGENTS.md`.
Move only repeated agent actions into skills.

## Over-Generalization

Do not abstract away the useful part.

Bad:

> Test your work carefully.

Good:

> After changing a visual layout, run the app and inspect an actual rendered frame because static checks often miss visibility, scale, layering, and alignment failures.

## No Validation

Do not create a skill, script, hook, or report section that lacks a concrete success check.

Every generated skill should say how the agent knows the workflow worked.
Every generated script should have a clear non-zero failure condition.

## False Enforcement

Do not claim a rule is enforced unless an actual script, hook, CI job, or tool configuration enforces it.

If the rule remains prose-only, label it advisory.

## Premature Hooking

Do not add hooks for expensive, noisy, fragile, or situational actions.

Hooks are only for zero-exception behavior.

## Tool Version Fragility

When generated commands depend on tool behavior that may change, keep the migration asset narrowly scoped and record the fragile assumption in the relevant procedure or validation step. Do not add a separate trailing upkeep section.

```markdown
Use <tool/API> only when <observable condition> holds; if <obsolete signal> appears, re-check this workflow before relying on it.
```

## Unsupported Policy Inference

Do not invent approval rules, architectural constraints, forbidden paths, or compliance requirements that are not evidenced by the repository or user request.

State uncertainties in the migration report instead.
