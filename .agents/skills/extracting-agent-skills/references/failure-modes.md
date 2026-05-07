# Common Failure Modes

Load this file when reviewing candidate skills before finalization, or when an extraction feels off and you want to check it against known anti-patterns.

## Skill Cemetery

Do not turn every abandoned project into several skills.

Too many weak skills reduce agent reliability.

Prefer fewer, stronger skills.

## README Duplication

Do not copy ordinary setup instructions into a skill unless they encode non-obvious agent behavior.

A README tells a human how to use the project.

A skill tells an agent how to act reliably.

## Project Lore Leakage

Do not include long explanations of why the project existed.

Only preserve context that changes future agent behavior.

## Over-Generalization

Do not abstract away the useful part.

Bad:

> Test your work carefully.

Good:

> After changing a visual layout, export or run the app and inspect an actual rendered frame, because static code checks often miss visibility, scale, layering, and alignment failures.

## No Validation

Do not create a skill that lacks a concrete success check.

A skill should say how the agent knows it has worked.

## Tool Version Fragility

When commands, APIs, or tool behavior may change, add maintenance notes:

```markdown
Last validated:
Known tool assumptions:
Signs this skill may be obsolete:
```

## Premature Skill Creation

Do not create a skill merely because a project ended.

A project can be closed without producing a skill.

## Self-Justifying Extraction

Do not use skill extraction to make an abandoned project feel successful.

The question is not “can something be extracted?”

The question is “will this improve future agent behavior enough to justify its maintenance cost?”
