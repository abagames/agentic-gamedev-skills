---
name: extracting-agent-skills
description: "Distills reusable agent skills (procedures, validation loops, debugging methods, tool-use patterns, decision rules) from completed, abandoned, paused, or failed projects. Use when closing/archiving a project, reducing side-project sprawl, or when the user asks to extract/harvest/distill/generalize project knowledge into reusable agent capabilities. Enforces trigger/validation/transferability checks to avoid creating weak skills."
---

# Extract Reusable Agent Skills from a Project

Extract ways of working, not a summary of what the source project was. A failed or abandoned product may still contain a strong workflow; a successful project may contain nothing worth turning into a skill.

## Workflow

### 1. Inspect available evidence

Inspect the smallest useful set of source artifacts: instructions, source, tests, scripts, build/export commands, logs, errors, reviews, history, and generated outputs. State what was unavailable; never imply that missing material was inspected.

Identify the project outcome only to interpret the evidence. Product success is not the extraction criterion.

### 2. Find behavior-changing candidates

Look for a repeatable agent action such as:

- a safe tool or file-editing sequence;
- a diagnosis or failure-classification method;
- a validation loop that catches a known blind spot;
- a decision or stop/escalation rule;
- a reproducible environment or build pattern.

Exclude project lore, feature wishes, temporary TODOs, ordinary setup instructions, personal motivation, and one-off implementation facts. Prefer zero or one strong candidate over several weak ones.

### 3. Gate each candidate

Recommend a skill only when the candidate:

- has a distinct trigger and repeatable procedure;
- plausibly transfers to several future tasks after project names are removed;
- changes agent behavior beyond “be careful” or “test thoroughly”;
- includes a concrete success check and prevents an observed or credible failure;
- belongs in a skill rather than a README, script comment, issue, or postmortem;
- can remain focused without unrelated background material.

Reject a candidate that fails most of these checks. Do not create a skill merely to give a closed project a positive outcome.

### 4. Update before creating

Search the current skill collection before proposing a new directory.

- Update an existing skill when trigger, workflow, and validation are substantially the same.
- Split candidates when their triggers, tools, procedures, or validation methods differ.
- Merge candidates when they are project-named variants of the same workflow.

Prefer procedure, validation, and debugging skills. Express judgment skills as decision rules rather than essays. Put long examples, templates, and stable domain reference material under `references/`.

### 5. Generalize without erasing the useful detail

Remove source-project names and paths, but retain the causal rule, ordering constraint, tool behavior, failure signal, and validation method that made the technique work. Keep concrete commands only when the skill is specifically about that tool or environment.

Define the boundary through frontmatter and the procedure: required inputs, actions, output, validation, exclusions, and failure handling. Avoid repeating the trigger throughout the body.

### 6. Draft and review

Load [output-templates.md](references/output-templates.md) when formatting candidates, drafting `SKILL.md`, or writing the final report. Choose at most three strong recommendations by default.

Before finalizing:

1. Confirm `name` and `description` make the trigger discoverable.
2. Confirm the procedure is concrete and the validation covers its likely failure.
3. Move details that are not needed on every invocation to a directly linked reference.
4. Load [failure-modes.md](references/failure-modes.md) and reject or revise any candidate that matches its anti-patterns.
5. Review the [current official Agent Skills authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) when reachable. If it is unreachable, perform the structural checks above and report the limitation rather than blocking extraction.
6. Load [empirical-tuning-gate.md](references/empirical-tuning-gate.md) after drafting and decide whether fresh-executor testing is worth its cost. Self-review is structural review, not empirical validation.

### 7. Report an honest state

Use one of these states:

- **Draft** — extracted but not tested;
- **Structurally reviewed** — checked for scope, clarity, links, and validation design;
- **Empirically tuned** — exercised by fresh executors on realistic scenarios and revised from observed failures;
- **Rejected** — not worth creating or merging.

Report whether to create, update, merge, or reject; what source material was intentionally excluded; and what validation remains. Never present an untested draft as proven.

## Reference routing

- [output-templates.md](references/output-templates.md) — load only while producing candidate, draft, or final-report output.
- [failure-modes.md](references/failure-modes.md) — load during candidate review or when extraction feels self-justifying.
- [empirical-tuning-gate.md](references/empirical-tuning-gate.md) — load only after a draft exists.
