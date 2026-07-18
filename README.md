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
| [`designing-mini-games`](.agents/skills/designing-mini-games/SKILL.md)             | Designs original mini-games — rules, controls, scoring, hazards, and difficulty curves — for any input scheme, including one-button (tap / hold / release) games. It helps prevent idle, hold-only, or button-mashing strategies from becoming optimal. |
| [`designing-minimal-game-rules`](.agents/skills/designing-minimal-game-rules/SKILL.md) | Turns an abstract game-design seed into a minimal discrete-state rule system by generating conflict candidates, stress-testing simple strategies, and reducing to the smallest surviving core. |
| [`generating-retro-arcade-concepts`](.agents/skills/generating-retro-arcade-concepts/SKILL.md) | Batch-generates, evaluates, and specs multiple fixed-screen arcade game concepts in the style of 1978–1983 cabinets, then selects and writes implementation specs for the top concepts.   |
| [`verifying-turn-based-games`](.agents/skills/verifying-turn-based-games/SKILL.md) | Defines a pure-function engine interface contract and quality measurement methodology (bot-ladder win-rates, tension/decision-density metrics) for two-player strict-alternating-turn games. |

### Game Implementation

| Skill                            | Purpose                                                                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`scaffolding-godot-mini-games`](.agents/skills/scaffolding-godot-mini-games/SKILL.md)     | Scaffolds a minimal Godot 4.2+ mini-game project with Web export defaults, tests, telemetry helpers, and procedural audio primitives.                           |
| [`running-headless-godot`](.agents/skills/running-headless-godot/SKILL.md)                 | Defines reproducible headless Godot workflows for CLI usage, logs, scene editing through scripts, tests, and Web export.                                        |
| [`developing-with-crisp-game-lib`](.agents/skills/developing-with-crisp-game-lib/SKILL.md) | Implements or repairs browser mini-games with `crisp-game-lib`, including CDN/npm setup, game loop structure, drawing-order collision, scoring, and validation. |
| [`arcadifying-mini-games`](.agents/skills/arcadifying-mini-games/SKILL.md) | Converts a working mini-game into a complete arcade game by adding round structure, ceremony screens (READY / clear / death / game over), a score economy (extends, initials entry, high-score table), and attract mode around a verified core loop. |
| [`implementing-gameplay-invariants`](.agents/skills/implementing-gameplay-invariants/SKILL.md) | Translates game design promises into engine-neutral implementation invariants and validation checks that prevent idle, hold-only, mashing, or repeated scoring dominance. |
| [`smoke-testing-web-games`](.agents/skills/smoke-testing-web-games/SKILL.md) | Smoke-tests a browser game build headlessly with idle time and input bursts, failing on console errors, uncaught exceptions, or crashes. Catches code that passes mock or simulator tests but crashes in a real browser. |
| [`probing-web-game-mechanics`](.agents/skills/probing-web-game-mechanics/SKILL.md) | Verifies that implemented mechanics match their spec by injecting game state into a live headless browser and asserting the resulting transitions (phase changes, scoring formulas, gates, resets). Sits between smoke testing (runtime health) and balance evaluation (play quality). |

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
| [`refining-workflows-from-artifacts`](.agents/skills/refining-workflows-from-artifacts/SKILL.md) | Refines reusable agent workflows from real execution artifacts by classifying failure causes before proposing the smallest evidence-based workflow diff. |
| [`critiquing-own-response`](.agents/skills/critiquing-own-response/SKILL.md) | Performs structured, ruthless self-critique of the agent's immediately preceding response, covering assumptions, logical integrity, AI-specific pitfalls, risks, and revised confidence. Invoke explicitly when adversarial review of a prior answer is needed. |

## Supporting Directories

- `references/`: detailed guides, checklists, design templates, and implementation patterns.
- `assets/`: reusable templates, Godot scripts, fonts, or other project assets.
- `scripts/`: automation for asset generation, validation, or related workflows.
- `tools/`: repository maintenance utilities, such as README/skill-list checks and external skill installation.
- `agents/`: optional model- or agent-specific configuration used by a skill.

## External Skill References

The following individual skills are imported or referenced from other repositories because they complement a specific local workflow. They are listed in `.gitignore` so they can be evaluated or used locally without being committed here. `tools/install-external-skills.sh` fetches the supported entries; reference-only entries are reviewed and adapted individually rather than installed as a whole upstream collection.

- [`empirical-prompt-tuning`](https://github.com/mizchi/skills/blob/main/meta/empirical-prompt-tuning/SKILL.md): iterative methodology for evaluating and improving prompts, skills, slash commands, and `AGENTS.md`-style guidance.
- [`godot-master`](https://github.com/thedivergentai/gd-agentic-skills): Godot 4 architecture and implementation reference from `gd-agentic-skills`. Pull individual engine-topic skills only (e.g. `godot-tweening`, `godot-particles`, `godot-debugging-profiling`) via `install_subtree` in `install-external-skills.sh`; its architecture doctrine and genre skills target production-scale Godot 4.7+ games and conflict with this repo's minimal mini-game approach, so never install the full set (the script deliberately skips it).
- [`writing-great-skills`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md): skill-authoring reference for trigger design, checkable completion criteria, progressive disclosure, and pruning no-op, duplicated, or stale instructions. Use alongside `extracting-agent-skills` and `refining-workflows-from-artifacts` when tightening a newly extracted or empirically revised skill; keep this repository's frontmatter convention when upstream invocation metadata differs.
- [`source-driven-development`](https://github.com/addyosmani/agent-skills/blob/main/skills/source-driven-development/SKILL.md): version-aware implementation workflow grounded in official documentation. Use alongside `developing-with-crisp-game-lib`, `running-headless-godot`, or `scaffolding-godot-mini-games` when behavior depends on a current engine, browser, or library API; it complements those domain workflows without replacing their project-specific validation.
- [`browser-testing-with-devtools`](https://github.com/addyosmani/agent-skills/blob/main/skills/browser-testing-with-devtools/SKILL.md): live-browser diagnosis using console, network, DOM, and performance evidence. Use after `smoke-testing-web-games` or `probing-web-game-mechanics` localizes a browser-game problem that needs deeper runtime investigation; adapt the workflow when Chrome DevTools MCP is unavailable.
- [`performance-optimization`](https://github.com/addyosmani/agent-skills/blob/main/skills/performance-optimization/SKILL.md): measure-first performance investigation and before/after verification. Use as a source for extending `smoke-testing-web-games` or `maximizing-game-feel` with performance gates, replacing general Web-app targets with game-relevant frame time, input latency, memory growth, load size, and representative-device budgets.
- [`systematic-debugging`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md): root-cause-first debugging workflow for bugs, test failures, and unexpected behavior.

## Repository Tools

- `tools/install-external-skills.sh` — fetch supported external skills into `.agents/skills/<name>/`; reference-only entries above are not automatic targets.
- `tools/check-readme-skills.sh` — verify that every skill directory under `.agents/skills/` is mentioned in this README's tables (and vice versa). Exits non-zero on drift.
