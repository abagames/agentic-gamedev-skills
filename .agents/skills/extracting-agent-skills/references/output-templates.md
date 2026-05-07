# Output Templates

Load this file when producing candidate skills, drafting a new `SKILL.md`, or writing the final report to the user.

## Candidate Output Format

For each candidate skill, use this format:

```markdown
## Candidate Skill: <name>

### Use Case

<When this skill should be invoked.>

### Reusable Core

<The generalized procedure or principle.>

### Evidence from Project

<Briefly describe what in the project suggests this is useful. Avoid long narrative.>

### Transferability

<Explain what kinds of future projects could reuse it.>

### Validation Method

<How an agent can check whether the skill worked.>

### Exclusions

<Project-specific details that should not be included.>

### Existing Skill Relationship

<Create new / Merge with existing skill / Update existing skill / Do not create.>

### Recommendation

Create / Merge / Update / Do not create
```

## Draft `SKILL.md` Template

For each recommended skill, provide a draft `SKILL.md` using this structure:

```markdown
---
name: <short-kebab-case-name>
description: <specific description that helps the agent know when to invoke this skill>
---

# <Skill Name>

## Purpose

## When to Use

## When Not to Use

## Required Inputs

## Procedure

## Validation

## Common Failure Modes

## Output

## Maintenance Notes
```

The frontmatter `name` and `description` are important.

The description should make the invocation condition clear. Avoid vague descriptions such as “helps with projects” or “improves quality.”

## Minimal Final Report Template

The `## Recommended Skills` section has three branches. Pick the one matching `Recommended action`. Other top-level headings (`## Result`, `## Excluded Material`, `## Notes`) are the same in all branches.

### Branch: "Create"

```markdown
## Result

Recommended action: Create

## Recommended Skills

1. <new skill name> — <Draft / Structurally reviewed / Empirically tuned>
   - Why it is worth preserving:
   - Validation method:
   - Empirical tuning: <recommended / not necessary>
   - Draft `SKILL.md` (inline as a fenced markdown block immediately below):

     ```markdown
     <full draft SKILL.md content per the Draft `SKILL.md` Template above>
     ```

## Excluded Material

- <project-specific item excluded>
- <README-level item excluded>
- <weak candidate excluded>

## Notes

<Any maintenance risk, obsolete assumption, or follow-up testing needed.>
```

### Branch: "Update existing skill"

```markdown
## Result

Recommended action: Update existing skill (<existing skill name>)

## Recommended Skills

1. <existing skill name> — <Draft / Structurally reviewed / Empirically tuned>
   - What is added: <one-line summary of the new rule, paragraph, or note>
   - Where it goes: <`<file path>: <section>` for single-file edits, OR a short bulleted list of `<file path>: <section>` lines when the existing skill spans multiple files (e.g. `SKILL.md` plus reference files)>
   - Why fold in vs create new: <one-line justification grounded in step 8>
   - Empirical tuning: <recommended / not necessary>

## Excluded Material

- <project-specific item excluded>
- <README-level item excluded>
- <weak candidate excluded>

## Notes

<Any maintenance risk, obsolete assumption, or follow-up testing needed.>
```

### Branch: "Do not create"

```markdown
## Result

Recommended action: Do not create

## Recommended Skills

None.

## Excluded Material

- <project-specific item excluded>
- <README-level item excluded>
- <weak candidate excluded>

## Notes

<Reason for "Do not create", grounded in the SKILL.md candidate-rejection criteria (e.g. lacks a clear trigger, fails the Step 3 questions, would be better as a README note, Skill-Cemetery risk).>
<Any other maintenance risk or follow-up note.>
```
