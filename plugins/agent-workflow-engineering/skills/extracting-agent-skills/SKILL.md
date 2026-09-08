---
name: extracting-agent-skills
description: "Distills reusable agent procedures, validation loops, debugging methods, tool-use patterns, and decision rules from completed, paused, abandoned, or failed projects. Use when closing or archiving a project, reducing side-project sprawl, or when asked to harvest project knowledge into reusable agent capabilities. Gates candidates for trigger clarity, validation, and transferability to avoid weak skills."
---

# Extracting Agent Skills

Extract behavior-changing ways of working, not a project summary. Project outcome is context, not the criterion: a failed project may yield a strong procedure, while a successful one may yield none.

## Workflow

1. Inspect the smallest useful evidence set: instructions, source, tests, scripts, commands, logs, errors, reviews, history, and outputs. State what was unavailable; do not imply it was inspected.
2. Identify repeatable actions: safe tool/editing sequences, diagnosis methods, validation loops, decision or stop rules, and reproducible environment patterns. Exclude lore, wishes, TODOs, ordinary setup, motivation, and one-off facts.
3. Recommend a skill only when the candidate has:
   - a distinct trigger and repeatable procedure;
   - plausible transfer to several future tasks after project names are removed;
   - behavior-changing guidance beyond “be careful”;
   - a concrete success check tied to an observed or credible failure;
   - a better home in a skill than in a README, comment, issue, or postmortem;
   - a focused scope.
4. Search the current skill collection before proposing a directory. Update when trigger, workflow, and validation substantially match; merge project-named variants; split candidates whose triggers, tools, procedures, or checks differ.
5. Generalize names and paths while preserving causal rules, ordering, tool constraints, failure signals, and validation. Keep tool commands only for tool-specific skills. Put conditional detail and long examples in directly linked `references/` files.
6. Draft and review at most three strong recommendations by default. Use [output-templates.md](references/output-templates.md) for candidate, draft, and report formats, then use [failure-modes.md](references/failure-modes.md) to reject or revise anti-patterns. If reachable, review current official Agent Skills authoring guidance; otherwise report that limitation rather than blocking.
7. After drafting, use [empirical-tuning-gate.md](references/empirical-tuning-gate.md) to decide whether fresh-executor testing is worth its cost. Structural self-review is not empirical validation.

Prefer zero strong candidates to several weak ones. Do not create skills merely to salvage a project or satisfy a requested quantity.

## Final State

Report create/update/merge/reject decisions, intentionally excluded material, and remaining validation. Label each result honestly:

- **Draft** — extracted but untested.
- **Structurally reviewed** — checked for scope, clarity, links, and validation design.
- **Empirically tuned** — exercised by fresh executors and revised from observed failures.
- **Rejected** — not worth creating or merging.
