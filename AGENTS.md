# AGENTS.md

## Mission

This repository is a collection of agent skills extracted from game-development work and related personal research.

Treat `.agents/skills/` as the primary project content. Each skill should be reusable outside the project that produced it, clear about when it applies, and concise enough for an agent to follow without unnecessary context.

## Repository Rules

- Keep skills under `.agents/skills/<skill-name>/`.
- Use `SKILL.md` as the entry point for every skill.
- Keep supporting material in skill-local directories such as `references/`, `assets/`, `scripts/`, `tools/`, or `agents/`.
- Update both `README.md` and `README.ja.md` when adding, removing, renaming, or materially changing a skill.
- Do not place generated experiments, game projects, or throwaway outputs at the repository root.

## Skill Maintenance

- Prefer small, behavior-changing skills over broad documentation dumps.
- Write skill descriptions so an agent can decide when to use the skill.
- Put detailed examples, long checklists, and implementation notes in `references/` instead of overloading `SKILL.md`.
- Preserve concrete workflows, validation steps, failure modes, and tool-use patterns.
- Remove or revise instructions that only made sense for the original project and do not transfer.

## Frontmatter Convention

Local skills should follow this style; external skills may keep their upstream form.

- Quote multi-clause descriptions: `description: "Does X. Use when ..."`.
- Open `description` with a third-person present verb (`Designs ...`, `Verifies ...`, `Generates ...`), not a noun phrase.
- Include both _what the skill does_ and _when to use it_ in the description so the agent can match on either.
- The only required directory name for in-skill documentation is `references/`. Do not use `skills/`, `docs/`, or other variants.

## Verification Scope

Applies both to work done in this repository and to the verification steps skills prescribe.

- Choose verification by what the change can reach at runtime and what a failure would cost, not by diff size or by which skill produced the change.
- Start from the cheapest check that covers the change and stop once the current failure mode is covered.
- Do not enter an expensive gate — real-browser runs, bot ladders, telemetry sweeps, independent agent review — merely because a skill mentions it, because an earlier step used a related skill, or because prior evidence is absent rather than negative.
- Keep strict rules that exist for reproducibility, sandboxing, or irreversible cost; they are not scope creep.

## Validation

Before finishing skill changes:

- Run `bash tools/check-readme-skills.sh`. It must exit 0; it diffs `.agents/skills/` against both `README.md` and `README.ja.md`.
- Run `bash tools/tests/test-repository-tools.sh` after changing anything under `tools/`.

The script only matches skill names. These still need a human or agent read:

- Check that the relevant `SKILL.md` has a clear `name` and a `description` following the frontmatter convention above.
- Confirm linked supporting files exist.
- Confirm the README overview paragraphs and section groupings still describe what the repository actually contains.
- Note any validation that was not possible.
