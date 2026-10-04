# Agentic Gamedev Skills

English | [日本語](README.ja.md)

This repository collects agent skills extracted from game-development work and related agentic-workflow research. Each skill lives under `.agents/skills/`, uses `SKILL.md` as its entry point, and may include `references/`, `assets/`, `scripts/`, `tools/`, or `agents/` directories.

The main use case is building mini-games with one-button controls, strong visual feedback, procedural audio, telemetry-guided tuning, and optional pixel-art assets. The collection also covers pre-implementation concept exploration, adversarial concept review, and mechanically diverse portfolio curation. A few adjacent skills support those workflows: skill extraction, workflow refinement from real execution artifacts, and gating or dispatching expensive agent work.

Games built with these skills live in [agentic-gamedev-games](https://github.com/abagames/agentic-gamedev-games).

## How To Use

- Invoke a skill by name, or let the task trigger the skill through its `description` field.
- Treat each `SKILL.md` as the canonical workflow for that capability.
- Use `AGENTS.md` for repository-level maintenance rules.

## Plugin Distributions

Seven repository-hosted plugins package the skills for Codex and Claude Code. Their versioned installable roots and catalogs are generated from the canonical skills and compositions in this repository. GitHub distribution is separate from submission to an OpenAI or Anthropic curated directory. See the [maintainer guide](PLUGIN_RELEASE.md) for regeneration, validation, versioning, and the publication boundary.

| Plugin | Skills |
| --- | ---: |
| [Game Concept Workbench](plugins/game-concept-workbench/README.md) | 3 |
| [One-Button Game Builder](plugins/one-button-game-builder/README.md) | 9 |
| [Gameplay Verification & Debugging Toolkit](plugins/gameplay-debugging-toolkit/README.md) | 5 |
| [Retro Arcade Game Finisher](plugins/retro-arcade-game-finisher/README.md) | 5 |
| [Godot Mini-Game Builder](plugins/godot-mini-game-builder/README.md) | 4 |
| [Web Mini-Game Kit](plugins/web-mini-game-kit/README.md) | 4 |
| [Agent Workflow Engineering](plugins/agent-workflow-engineering/README.md) | 9 |

The bundles cover 37 local skills with 39 memberships; externally referenced skills are excluded.

After GitHub publication, Claude Code users can add `abagames/agentic-gamedev-skills` as a marketplace and install `<plugin>@agentic-gamedev-skills`. Codex CLI users can add the same `owner/repo` marketplace, list available plugins, and install `<plugin>@agentic-gamedev-skills`; workspace administrators can import the GitHub repository through plugin management. The repository contains the standard Codex catalog, an API-key-login Codex catalog, and the Claude Code catalog. Maintainers regenerate them with `python3 tools/plugin-bundles/published.py --repo . --write`.

## Skill Authoring Conventions

Local skills follow [Anthropic's Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) where practical:

- Names use lowercase letters, numbers, and hyphens.
- New local skills should prefer gerund-style names, such as `designing-mini-games`.
- Descriptions should state what the skill does and when to use it, written in third person.
- `SKILL.md` should stay concise and point to `references/`, `assets/`, `scripts/`, `tools/`, or `agents/` only as needed.
- Keep load-bearing decisions and the shortest complete workflow in `SKILL.md`; route variant setup, technique catalogs, long examples, and conditional edge cases to directly linked `references/` with explicit read conditions.
- Do not preserve project validation history in the executable skill body. Retain only the generalized rule or failure mode that changes future agent behavior.

External imported skills may keep their upstream names and structure.

## Bundled Skills

### Game Design

| Skill                        | Purpose                                                                                                                                                                                      |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`exploring-game-design-space`](.agents/skills/exploring-game-design-space/SKILL.md) | Explores varied game mechanics and returns testable concept hypotheses. Use before narrowing the design space to a few candidates. |
| [`designing-mini-games`](.agents/skills/designing-mini-games/SKILL.md) | Designs compact games with rules, controls, scoring, hazards, and difficulty progression for any input scheme, including one-button play. |
| [`designing-minimal-game-rules`](.agents/skills/designing-minimal-game-rules/SKILL.md) | Turns an abstract design seed into a minimal discrete-state ruleset, tested against simple strategies. |
| [`generating-retro-arcade-concepts`](.agents/skills/generating-retro-arcade-concepts/SKILL.md) | Generates and evaluates multiple fixed-screen arcade concepts inspired by 1978–1985 games, then writes implementation specs for the selected concepts. |
| [`curating-game-concept-portfolio`](.agents/skills/curating-game-concept-portfolio/SKILL.md) | Selects a small, mechanically diverse portfolio from supplied game concepts using structural comparison and available evidence. |
| [`verifying-turn-based-games`](.agents/skills/verifying-turn-based-games/SKILL.md) | Verifies two-player games with strictly alternating turns through a pure-function engine contract and bot-based quality measurements. |

### Game Implementation

| Skill                            | Purpose                                                                                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`scaffolding-godot-mini-games`](.agents/skills/scaffolding-godot-mini-games/SKILL.md) | Scaffolds a minimal Godot 4.2+ mini-game with Web export, testing, telemetry, and procedural audio infrastructure. |
| [`running-headless-godot`](.agents/skills/running-headless-godot/SKILL.md) | Runs reproducible headless Godot workflows for scene editing, tests, and Web exports. |
| [`developing-with-crisp-game-lib`](.agents/skills/developing-with-crisp-game-lib/SKILL.md) | Creates or repairs browser mini-games specifically using `crisp-game-lib`, covering its input, drawing, collision, and game-loop conventions. |
| [`arcadifying-mini-games`](.agents/skills/arcadifying-mini-games/SKILL.md) | Finishes a working mini-game as an arcade game with rounds, ceremony screens, score economy, rankings, and attract mode. |
| [`implementing-gameplay-invariants`](.agents/skills/implementing-gameplay-invariants/SKILL.md) | Translates game-design promises into engine-neutral implementation invariants and validation checks. |

### Game Presentation

| Skill                             | Purpose                                                                                                                                                                                           |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`directing-game-visuals`](.agents/skills/directing-game-visuals/SKILL.md) | Defines visual hierarchy, palette, composition, and event feedback so players can read the game from its screen. |
| [`maximizing-game-feel`](.agents/skills/maximizing-game-feel/SKILL.md) | Improves the responsiveness and impact of a working action game through animation and effects. |
| [`creating-godot-procedural-audio`](.agents/skills/creating-godot-procedural-audio/SKILL.md) | Designs and implements procedural sounds for game events and state changes using Godot’s built-in audio APIs. |
| [`building-era-authentic-game-audio`](.agents/skills/building-era-authentic-game-audio/SKILL.md) | Builds a complete procedural game-audio system inspired by early arcade hardware, including music, effects, and jingles. |
| [`styling-web-game-typography`](.agents/skills/styling-web-game-typography/SKILL.md) | Implements readable, properly licensed typography for distributed games, with Godot examples. |
| [`designing-retro-arcade-sound-kits`](.agents/skills/designing-retro-arcade-sound-kits/SKILL.md) | Designs and validates retro-arcade effects and jingles triggered by abstract game events, independently of the engine. |
| [`generating-dot-assets`](.agents/skills/generating-dot-assets/SKILL.md) | Generates and validates transparent pixel-art object assets at a specified canvas size. |

### Evaluation And Tuning

| Skill                         | Purpose                                                                                                                                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`stress-testing-game-concepts`](.agents/skills/stress-testing-game-concepts/SKILL.md) | Adversarially tests existing concepts, rulesets, or early prototypes, separating demonstrated defects from unanswered questions. |
| [`evaluating-gameplay-balance`](.agents/skills/evaluating-gameplay-balance/SKILL.md) | Evaluates balance through telemetry and comparisons of simple and intended play. Detects exploits and tunes difficulty using simulated players calibrated against play reports. |
| [`refining-game-prototypes`](.agents/skills/refining-game-prototypes/SKILL.md) | Autonomously refines a playable prototype through structure, difficulty and progression, presentation, and cleanup. Chooses fixes from the game’s intent and observed evidence, keeping a revision log and unresolved findings. |
| [`auditing-game-screen-readability`](.agents/skills/auditing-game-screen-readability/SKILL.md) | Audits frames at gameplay events and overlapping notices to find unreadable, hidden, or unnecessary screen elements. |
| [`gating-intent-legibility`](.agents/skills/gating-intent-legibility/SKILL.md) | Tests whether an isolated reader can infer the game’s goal, choices, and risks from gameplay images alone. |

### Gameplay Verification And Debugging

Ordered from the cheapest gate to the most expensive instrument: runtime health, spec conformance,
coverage of behavior families, defect localization, repair validation, and measurement of the
instruments themselves.

| Skill | Purpose |
| --- | --- |
| [`smoke-testing-web-games`](.agents/skills/smoke-testing-web-games/SKILL.md) | Smoke-tests a browser game under idle and input phases to catch console errors, uncaught exceptions, and crashes. |
| [`probing-web-game-mechanics`](.agents/skills/probing-web-game-mechanics/SKILL.md) | Verifies browser-game mechanics against their spec through state injection and transition assertions, including visual and input bindings. |
| [`auditing-gameplay-implementation-coverage`](.agents/skills/auditing-gameplay-implementation-coverage/SKILL.md) | Audits specification, implementation, presentation, and tests for missing cases within related gameplay behaviors. |
| [`localizing-game-state-divergence`](.agents/skills/localizing-game-state-divergence/SKILL.md) | Replays a reproducible gameplay defect to find the first event where a checked state invariant fails. |
| [`adversarially-validating-game-repairs`](.agents/skills/adversarially-validating-game-repairs/SKILL.md) | Stress-tests an existing game fix with adversarial cases reachable by the change and cases that should remain unaffected. |
| [`generating-semantic-game-mutants`](.agents/skills/generating-semantic-game-mutants/SKILL.md) | Injects controlled gameplay defects to measure a test suite’s detection power or an agent workflow’s repair behavior. |

### Agent Workflow

| Skill                     | Purpose                                                                                                                                                                                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`extracting-agent-skills`](.agents/skills/extracting-agent-skills/SKILL.md) | Extracts reusable agent procedures and decision rules from completed, paused, abandoned, or failed projects. |
| [`extracting-spec-design-ladders`](.agents/skills/extracting-spec-design-ladders/SKILL.md) | Reverse-engineers source code into a concrete reproduction spec and an abstract design document. |
| [`gating-by-blind-restoration`](.agents/skills/gating-by-blind-restoration/SKILL.md) | Tests whether a spec or other abstraction is self-sufficient by giving it alone to an isolated agent for reconstruction. |
| [`gating-expensive-batch-work`](.agents/skills/gating-expensive-batch-work/SKILL.md) | Separates cheap trials from expensive batch execution, freezing the method before irreversible resources are spent. |
| [`migrating-agents-md-to-control-flow`](.agents/skills/migrating-agents-md-to-control-flow/SKILL.md) | Moves repeatable workflows from large agent instruction files into skills and mandatory checks into scripts, hooks, or CI. |
| [`refining-workflows-from-artifacts`](.agents/skills/refining-workflows-from-artifacts/SKILL.md) | Improves reusable agent workflows from actual execution results, identifying failure causes before proposing targeted changes. |
| [`critiquing-own-response`](.agents/skills/critiquing-own-response/SKILL.md) | Reviews the agent’s preceding response for assumptions, reasoning gaps, and unverified claims. Explicit use only; it is not an independent review. |
| [`dispatching-agent-work`](.agents/skills/dispatching-agent-work/SKILL.md) | Routes work to suitable tasks, agents, or automations while preserving context and authority. Persistent dispatch mode is opt-in. |

## Supporting Directories

- `references/`: detailed guides, checklists, design templates, and implementation patterns.
- `assets/`: reusable templates, Godot scripts, fonts, or other project assets.
- `scripts/`: automation for asset generation, validation, or related workflows.
- `tools/`: repository maintenance utilities, such as README/skill-list checks and external skill installation.
- `agents/`: optional model- or agent-specific configuration used by a skill.

## External Skill References

The following individual skills are imported or referenced from other repositories because they complement a specific local workflow. They are listed in `.gitignore` so they can be evaluated or used locally without being committed here. `tools/install-external-skills.sh` fetches the supported entries; reference-only entries are reviewed and adapted individually rather than installed as a whole upstream collection.

- [`empirical-prompt-tuning`](https://github.com/mizchi/skills/blob/main/meta/empirical-prompt-tuning/SKILL.md): iterative methodology for evaluating and improving prompts, skills, slash commands, and `AGENTS.md`-style guidance.
- [`writing-for-agents`](https://github.com/mattpocock/skills/blob/main/docs/productivity/writing-for-agents.md): reference for making agent-facing skills, instructions, specifications, and prompts predictable by tightening completion criteria, controlling context load, and pruning no-op, duplicated, or stale guidance. Use alongside `extracting-agent-skills` and `refining-workflows-from-artifacts`; keep this repository's frontmatter convention when upstream invocation metadata differs.
- [`source-driven-development`](https://github.com/addyosmani/agent-skills/blob/main/skills/source-driven-development/SKILL.md): version-aware implementation workflow grounded in official documentation. Use alongside `developing-with-crisp-game-lib`, `running-headless-godot`, or `scaffolding-godot-mini-games` when behavior depends on a current engine, browser, or library API; it complements those domain workflows without replacing their project-specific validation.
- [`browser-testing-with-devtools`](https://github.com/addyosmani/agent-skills/blob/main/skills/browser-testing-with-devtools/SKILL.md): live-browser diagnosis using console, network, DOM, and performance evidence. Use after `smoke-testing-web-games` or `probing-web-game-mechanics` localizes a browser-game problem that needs deeper runtime investigation; adapt the workflow when Chrome DevTools MCP is unavailable.
- [`performance-optimization`](https://github.com/addyosmani/agent-skills/blob/main/skills/performance-optimization/SKILL.md): measure-first performance investigation and before/after verification. Use as a source for extending `smoke-testing-web-games` or `maximizing-game-feel` with performance gates, replacing general Web-app targets with game-relevant frame time, input latency, memory growth, load size, and representative-device budgets.
- [`systematic-debugging`](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md): root-cause-first debugging workflow for bugs, test failures, and unexpected behavior. Not installed by default: it claims every technical issue as its trigger, so it outranks `localizing-game-state-divergence`, `adversarially-validating-game-repairs`, `smoke-testing-web-games`, and `probing-web-game-mechanics` rather than complementing them, and its Phase 4 points at `superpowers:` sibling skills this repository does not carry. Pull it by name (`install-external-skills.sh systematic-debugging`) for non-game work, or for crashes, build failures, and multi-component boundary isolation, which the local debugging skills deliberately exclude.

## Repository Tools

- `tools/install-external-skills.sh` — stage and validate supported external skills before replacing `.agents/skills/<name>/`; failed updates preserve the installed version. Reference-only entries above are not automatic targets.
- `tools/check-readme-skills.sh` — verify local skill directories and external `.gitignore` entries against this README. Exits non-zero on drift.
- `tools/tests/test-repository-tools.sh` — exercise installer success, failure recovery, path containment, and README consistency without network access or changes to installed skills.
- `python3 tools/plugin-bundles/build.py plugin-bundles/<bundle>.json --target codex|claude` — build a self-contained plugin with a v3 payload hash/mode inventory. `--publishable` gates clean inputs; it does not imply strict reproducibility or official approval. Rebuild ignored `dist/` outputs instead of editing or committing them.
- `tools/tests/test-plugin-bundles.sh` — validate compositions, generated artifacts, deterministic skill hashes, and rejection of unsafe or malformed inputs.
- `python3 tools/plugin-bundles/published.py --write|--check` — regenerate or verify the seven tracked plugin roots and the Codex, Codex API-key, and Claude catalogs from compositions and canonical skills. The check rejects stale payloads, missing or extra roots, path escape, and identity/version drift.
- `python3 tools/plugin-bundles/package.py --output <new-dir>` — build and round-trip all seven bundles as ZIPs with checksums and a validation report. See the release guide for platform validator options.
