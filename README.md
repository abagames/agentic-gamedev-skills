# Agentic Gamedev Skills

English | [日本語](README.ja.md)

This repository collects agent skills extracted from game-development work and related agentic-workflow research. Each skill lives under `.agents/skills/`, uses `SKILL.md` as its entry point, and may include `references/`, `assets/`, `scripts/`, `tools/`, or `agents/` directories.

The main use case is building mini-games with one-button controls, strong visual feedback, procedural audio, telemetry-guided tuning, and optional pixel-art assets. A few adjacent skills support that workflow: skill extraction, prompt/process review, and bilingual English/Japanese writing polish.

## How To Use

- Invoke a skill by name, or let the task trigger the skill through its `description` field.
- Treat each `SKILL.md` as the canonical workflow for that capability.
- Use `AGENTS.md` for repository-level maintenance rules.

## Skill Authoring Conventions

Local skills follow [Anthropic's Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) where practical:

- Names use lowercase letters, numbers, and hyphens.
- New local skills should prefer gerund-style names, such as `designing-mini-games`.
- Descriptions should state what the skill does and when to use it, written in third person.
- `SKILL.md` should stay concise and point to `references/`, `assets/`, `scripts/`, `tools/`, or `agents/` only as needed.

External imported skills may keep their upstream names and structure.

## Bundled Skills

### Game Design

| Skill                        | Purpose                                                                                                                                                                                      |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`designing-mini-games`](.agents/skills/designing-mini-games/SKILL.md)             | Designs compact game rules, controls, scoring, hazards, rewards, and game-over conditions. It helps prevent idle, hold-only, or button-mashing strategies from becoming optimal.             |
| [`designing-one-button-games`](.agents/skills/designing-one-button-games/SKILL.md) | Designs original one-button mini-games using tap, hold, and release controls, with emphasis on novelty, risk/reward, and a short difficulty curve.                                           |
| [`generating-retro-arcade-concepts`](.agents/skills/generating-retro-arcade-concepts/SKILL.md) | Batch-generates, evaluates, and specs multiple fixed-screen arcade game concepts in the style of 1978–1983 cabinets, then selects and writes implementation specs for the top concepts.   |
| [`verifying-turn-based-games`](.agents/skills/verifying-turn-based-games/SKILL.md) | Defines a pure-function engine interface contract and quality measurement methodology (bot-ladder win-rates, tension/decision-density metrics) for two-player strict-alternating-turn games. |

### Game Implementation

| Skill                            | Purpose                                                                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`scaffolding-godot-mini-games`](.agents/skills/scaffolding-godot-mini-games/SKILL.md)     | Scaffolds a minimal Godot 4.2+ mini-game project with Web export defaults, tests, telemetry helpers, and procedural audio primitives.                           |
| [`running-headless-godot`](.agents/skills/running-headless-godot/SKILL.md)                 | Defines reproducible headless Godot workflows for CLI usage, logs, scene editing through scripts, tests, and Web export.                                        |
| [`developing-with-crisp-game-lib`](.agents/skills/developing-with-crisp-game-lib/SKILL.md) | Implements or repairs browser mini-games with `crisp-game-lib`, including CDN/npm setup, game loop structure, drawing-order collision, scoring, and validation. |
| [`implementing-gameplay-invariants`](.agents/skills/implementing-gameplay-invariants/SKILL.md) | Translates game design promises into engine-neutral implementation invariants and validation checks that prevent idle, hold-only, mashing, or repeated scoring dominance. |

### Game Presentation

| Skill                             | Purpose                                                                                                                                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`directing-game-visuals`](.agents/skills/directing-game-visuals/SKILL.md)                   | Defines readable visual hierarchy, palette roles, screen composition, and event feedback without relying on explanatory HUD text.                                                                 |
| [`maximizing-game-feel`](.agents/skills/maximizing-game-feel/SKILL.md)                       | Adds engine-independent tactile feedback such as squash/stretch, tilt, particles, trails, and impact polish to make gameplay feel more responsive.                                                |
| [`creating-godot-procedural-audio`](.agents/skills/creating-godot-procedural-audio/SKILL.md) | Designs and implements runtime procedural audio in Godot using built-in APIs, with distinct sounds for gameplay events and state changes.                                                         |
| [`styling-web-game-typography`](.agents/skills/styling-web-game-typography/SKILL.md)         | Implements readable, licensed typography for distributed games (web export, downloadable, packaged), engine-agnostic at the core with Godot 4.2+ implementation patterns provided as a reference. |
| [`designing-retro-arcade-sound-kits`](.agents/skills/designing-retro-arcade-sound-kits/SKILL.md) | Designs and validates event-driven retro-arcade sound kits (SFX and jingles) where game code emits abstract event names and an adapter layer resolves and plays them. Engine-agnostic; prevents SEs from drifting into background music. |
| [`generating-dot-assets`](.agents/skills/generating-dot-assets/SKILL.md)                     | Generates transparent pixel-art object assets by combining image generation, chroma-key removal, pixelization, exact canvas fitting, and validation.                                              |

### Evaluation And Tuning

| Skill                         | Purpose                                                                                                                                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`evaluating-gameplay-balance`](.agents/skills/evaluating-gameplay-balance/SKILL.md) | Evaluates balance through telemetry by comparing monotonous play policies against exploratory or intended-skill policies, including guidance for simulation harnesses and telemetry emitters. |

### Agent Workflow

| Skill                     | Purpose                                                                                                                                                                                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`extracting-agent-skills`](.agents/skills/extracting-agent-skills/SKILL.md) | Distills reusable agent procedures, validation loops, debugging methods, and decision rules from completed, paused, abandoned, or failed projects.                                                                                                              |
| [`extracting-spec-design-ladders`](.agents/skills/extracting-spec-design-ladders/SKILL.md) | Reverse-engineers source code into a two-layer artifact ladder — a concrete reproduction spec and an abstract design doc — with non-overlapping responsibilities and an auditable extraction log.                                                              |
| [`gating-by-blind-restoration`](.agents/skills/gating-by-blind-restoration/SKILL.md) | Validates that an abstraction layer (spec, design doc, schema, or contract) is self-sufficient by spawning an isolated sub-agent that sees only that layer and must reconstruct the adjacent one, returning pass / weak-pass / fail.                            |
| [`migrating-agents-md-to-control-flow`](.agents/skills/migrating-agents-md-to-control-flow/SKILL.md) | Audits large repo agent instruction files, then moves repeatable workflows into skills, mandatory checks into scripts/hooks/CI, and stable policy back into concise repo instructions. |
| [`critiquing-own-response`](.agents/skills/critiquing-own-response/SKILL.md) | Performs structured, ruthless self-critique of the agent's immediately preceding response, covering assumptions, logical integrity, AI-specific pitfalls, risks, and revised confidence. Invoke explicitly when adversarial review of a prior answer is needed. |

### Writing And Localization

| Skill                             | Purpose                                                                                                                                            |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`humanizing-bilingual-ai-writing`](.agents/skills/humanizing-bilingual-ai-writing/SKILL.md) | Revises English and Japanese AI-sounding prose into natural, credible writing while preserving facts, intent, audience, and bilingual consistency. |

## Supporting Directories

- `references/`: detailed guides, checklists, design templates, and implementation patterns.
- `assets/`: reusable templates, Godot scripts, fonts, or other project assets.
- `scripts/`: automation for asset generation, validation, or related workflows.
- `tools/`: helper utilities, especially for safe headless Godot operations.
- `agents/`: optional model- or agent-specific configuration used by a skill.

## External Skill References

The following skills are imported or referenced from other repositories and are listed in `.gitignore` so they can be fetched and used locally without being committed here. Run `tools/install-external-skills.sh` to fetch them (or pass specific names as arguments).

- [`empirical-prompt-tuning`](https://github.com/mizchi/skills/blob/main/empirical-prompt-tuning/SKILL.md): iterative methodology for evaluating and improving prompts, skills, slash commands, and `AGENTS.md`-style guidance.
- [`karpathy-guidelines`](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md): coding-agent guidelines that bias toward simple, surgical, assumption-aware, and verifiable changes.
- [`develop-web-game`](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/creative-design/develop-web-game): web-game iteration and Playwright validation loop for browser/canvas games. Useful as a reference for non-Godot web game testing.
- [`godot-master`](https://github.com/thedivergentai/gd-agentic-skills): Godot 4 architecture and implementation reference from `gd-agentic-skills`. Use selectively; do not install the full skill set by default (`install-external-skills.sh` deliberately skips it).
- [`systematic-debugging`](https://github.com/mxyhi/ok-skills/blob/main/systematic-debugging/SKILL.md): root-cause-first debugging workflow for bugs, test failures, and unexpected behavior.

## Repository Tools

- `tools/install-external-skills.sh` — fetch external skills listed above into `.agents/skills/<name>/`.
- `tools/check-readme-skills.sh` — verify that every skill directory under `.agents/skills/` is mentioned in this README's tables (and vice versa). Exits non-zero on drift.
