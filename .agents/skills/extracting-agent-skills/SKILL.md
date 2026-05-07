---
name: extracting-agent-skills
description: "Distills reusable agent skills (procedures, validation loops, debugging methods, tool-use patterns, decision rules) from completed, abandoned, paused, or failed projects. Use when closing/archiving a project, reducing side-project sprawl, or when the user asks to extract/harvest/distill/generalize project knowledge into reusable agent capabilities. Enforces trigger/validation/transferability checks to avoid creating weak skills."
---

# Extract Reusable Agent Skills from a Project

## Purpose

Extract reusable agent skills (procedures, tool-use patterns, debugging methods, validation loops, constraints, decision rules) from an existing project, whether completed, abandoned, paused, or failed. The goal is not to summarize the project; a project that failed as a product can still contain valuable operational knowledge worth preserving as a closure step.

## Reference Files

Load these only when the corresponding step calls for them — do not pre-load.

- `references/output-templates.md` — formats for candidate skills, draft `SKILL.md`, and the final report. Load at output time.
- `references/failure-modes.md` — anti-patterns to check candidates against before finalizing. Load during review.
- `references/empirical-tuning-gate.md` — decision rules for whether to run empirical prompt tuning on the produced skill. Load after drafting.

## Core Principle

Extract skills about **how to work**, not about **what this project is**.

Good skill material:

- repeatable procedures
- tool invocation patterns
- validation loops
- environment setup gotchas
- debugging strategies
- failure classifications
- safety constraints
- prompt decomposition methods
- build / test / export / inspect workflows
- human review checkpoints
- criteria for stopping, retrying, or escalating

Poor skill material:

- project-specific lore
- feature wishlists
- product positioning
- one-off implementation details
- temporary TODOs
- personal motivation
- long narrative history
- content that belongs in a README, changelog, issue, or postmortem

Prefer extracting zero or one strong skill over creating multiple weak skills.

## When to Use This Skill

Use this skill when:

- A project is being abandoned, paused, archived, or declared complete.
- A project produced useful workflows, scripts, prompts, tests, debugging methods, or validation loops.
- The user wants to preserve knowledge from a project without continuing the project itself.
- The project contains repeated agent mistakes that should be prevented in future work.
- The project involved tools, environments, frameworks, engines, APIs, or file formats that required non-obvious handling.
- The user asks to extract, harvest, distill, generalize, archive, or convert project knowledge into an agent skill.
- The project is part of a broader workflow where many side projects are started, but only some should be preserved as reusable agent capabilities.

Do not use this skill when:

- The user only wants a normal project summary.
- The project is too trivial to contain reusable process knowledge.
- The useful information is already fully captured in existing documentation.
- The candidate skill would only apply to one specific project and not transfer elsewhere.
- The user is asking to finish the project rather than extract reusable knowledge from it.

## Skill-Cemetery Warning

A weak skill is worse than no skill because it adds retrieval noise, outdated assumptions, and misleading instructions. Create a new skill only if it changes future agent behavior in a concrete and useful way.

## Step 0: Check Current Agent Skill Best Practices

Before creating or revising any `SKILL.md`, review the current official Agent Skills best practices:

https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Use the official guidance as a quality gate, especially for:

- concise instructions
- clear `name` and `description`
- discoverability by the agent
- progressive disclosure for long materials
- explicit distinction between executable scripts and reference files
- testing with realistic tasks
- iterating based on observed agent failures

Do not copy the best-practices document into the skill.

Apply it as a review checklist.

If the URL is unreachable (no network, sandboxed environment), do not skip the gate. Use the `Best-Practices Review` checklist later in this skill as a degraded-mode substitute and note `best-practices source: unreachable` in the final report's `## Notes`.

## Inputs to Inspect

When available, inspect:

- README files
- design documents
- source code
- scripts
- tests
- build/export commands
- CI configuration
- prompt files
- existing agent instruction files
- logs
- error messages
- screenshots or generated artifacts
- Git history or commit messages
- issue notes
- postmortems
- user comments about what worked or failed

If the full project is not available, work from the provided files, notes, or user description.

Do not pretend to have inspected files that are not available.

## Extraction Procedure

### 1. Identify the Project Outcome

Determine the project state — what process knowledge survived matters more than whether the final artifact succeeded:

- completed and useful
- completed but not reused
- paused
- abandoned
- failed technically
- failed as a product
- successful as an experiment
- useful mainly as a source of scripts or workflows
- useful mainly as a source of negative examples

### 2. Identify Reusable Work Patterns

Look for patterns such as:

- “To modify this kind of file safely, do X instead of Y.”
- “Before trusting the output, run these checks.”
- “When this error appears, inspect these logs first.”
- “Do not edit generated files directly.”
- “Use a small reproducer before changing the full system.”
- “Use screenshots, video, or traces because textual tests miss visual failures.”
- “Ask the model to produce a patch script rather than raw edits.”
- “Run a fast smoke test before a slow full validation.”
- “Classify failures before attempting fixes.”
- “Avoid overfitting to a single example.”
- “Stop when the project has yielded a reusable skill, even if the product is not worth finishing.”

Record only patterns that plausibly transfer to future projects.

### 3. Separate Skill Candidates from Project Notes

For each candidate, ask:

- Would this help in at least three future projects?
- Is it about an agent action, not just human background knowledge?
- Can it be described as a repeatable procedure?
- Does it include a validation step?
- Does it prevent a known failure mode?
- Can it fit in a concise `SKILL.md`?
- Is it still useful if all project-specific names are removed?
- Is it better as a skill than as a README note, issue, script comment, or postmortem?

Reject candidates that fail most of these checks.

### 4. Classify the Candidate Skill Type

Classify each candidate as one of:

- Procedure skill: a concrete workflow or tool-use sequence.
- Validation skill: a method for checking whether output is correct.
- Debugging skill: a failure diagnosis and recovery method.
- Judgment skill: a structured way to make a decision that agents often handle poorly.
- Closure skill: a method for ending, archiving, or extracting value from a project.
- Reference skill: a compact way to retrieve and apply stable background knowledge.

Prefer procedure, validation, and debugging skills.

Judgment skills are valuable but must be written as checklists or decision rules, not essays.

Reference skills should usually use progressive disclosure and external reference files rather than putting long material directly in `SKILL.md`.

### 5. Merge or Split Candidates

Prefer small, focused skills.

Split candidates when:

- They apply to different tools.
- They have different trigger conditions.
- They require different validation methods.
- They would become too long if combined.
- They mix procedural steps with unrelated background knowledge.

Merge candidates when:

- They are variants of the same workflow.
- They differ only by project-specific names.
- They share the same trigger, method, and validation loop.
- They would create retrieval noise if kept separate.

### 6. Remove Project-Specific Details

Replace project-specific details with general forms.

Bad:

> In `maze-town-v3`, edit `src/mazeRenderer.ts` and run `npm run maze-check`.

Better:

> For visual-generation projects, identify the renderer entry point, make the smallest possible change, then run the project’s fastest visual or structural validation command before judging quality.

Keep concrete commands only when the skill is specifically about that tool, framework, or environment.

### 7. Define the Skill Boundary

Each extracted skill must clearly state:

- when to use it
- when not to use it
- what inputs it needs
- what steps to follow
- what output to produce
- how to validate success
- what common mistakes to avoid
- what should remain outside the skill

A skill without a validation step is usually incomplete.

### 8. Check for Existing Skill Updates

Before recommending a new skill, check whether an existing skill should be updated instead.

Prefer updating an existing skill when:

- the new material is an edge case of an existing workflow
- the trigger condition is the same
- the validation method is the same
- the new material only adds a known failure mode
- the new material is a tool-version note

Create a new skill only when the trigger, procedure, or validation method is meaningfully different.

## Producing the Output

Use the formats in `references/output-templates.md`:

- `Candidate Output Format` for each candidate identified in step 3.
- The draft `SKILL.md` template for each recommended skill.
- The `Minimal Final Report Template` for the final response to the user.

Choose at most three strong skills by default.

## Best-Practices Review

Before finalizing any extracted skill, check:

- Is the skill short enough to fit comfortably in agent context?
- Are `name` and `description` specific enough for automatic discovery?
- Is the trigger condition clear?
- Does the skill avoid loading long reference material unless needed?
- Are scripts, templates, examples, and references clearly labeled by intended use?
- Does the skill distinguish between files to execute and files to read?
- Is the procedure concrete enough to change agent behavior?
- Does the skill include a validation method?
- Does the skill include common failure modes?
- Is there anything that should be moved out of `SKILL.md` into a separate reference file?
- Is the skill likely to remain useful after the source project is forgotten?

If the answer is weak on several points, do not create the skill.

Then load `references/failure-modes.md` and check the candidate against each anti-pattern.

## Empirical Tuning Gate

After drafting a recommended `SKILL.md`, decide whether empirical prompt tuning is worth applying. Load `references/empirical-tuning-gate.md` for the decision rules and the minimum tuning loop.

Do not treat self-review as empirical validation.

## Finalization State

Every extracted skill should be reported with one of these states:

- Draft: extracted but not tested.
- Structurally reviewed: checked for clarity, scope, and best-practices alignment.
- Empirically tuned: tested with realistic scenarios using a fresh executor and revised based on observed failures.
- Rejected: not worth creating as a skill.

For high-importance skills, prefer `Empirically tuned`.

For low-importance or experimental skills, `Draft` or `Structurally reviewed` is acceptable.

Do not present an untested skill as proven.

## Recommended Final Response to the User

Use the `Minimal Final Report Template` in `references/output-templates.md`. Include:

- whether any skills should be created (or that the project contains no reusable agent skill)
- the top one to three recommended skills, why each is worth preserving, and what was intentionally excluded
- whether each skill is Draft, Structurally reviewed, Empirically tuned, or Rejected
- whether an existing skill should be updated instead
- whether empirical tuning is recommended
