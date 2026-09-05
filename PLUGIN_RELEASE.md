# GitHub Plugin Distribution Maintenance

The six repository-native plugins are distributed from this repository after a reviewed commit is pushed to GitHub. The tracked `plugins/` directories are the installable payloads; ignored `dist/` output is only for disposable ZIP-package checks. GitHub distribution does not submit a plugin to an OpenAI or Anthropic curated directory.

## Source of truth and generated files

- `.agents/skills/<skill>/` contains canonical skill content and support files.
- `plugin-bundles/<plugin>.json` defines each plugin's membership, identity, version, and target metadata.
- `plugins/<plugin>/` is generated from those inputs and contains both `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`, plus the complete self-contained payload.
- `.agents/plugins/marketplace.json` is the standard Codex catalog.
- `.agents/plugins/api_marketplace.json` is the equivalent Codex catalog for API-key login users.
- `.claude-plugin/marketplace.json` is the Claude Code catalog.

The two Codex catalogs follow the layout used by the OpenAI-owned [plugins repository](https://github.com/openai/plugins). Claude Code uses the same repository-relative `./plugins/<plugin>` roots, as described in Anthropic's [marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).

## Regenerate and check

After changing a composition, canonical skill, generator template, or root license, regenerate the tracked payloads:

```bash
python3 tools/plugin-bundles/published.py --repo . --write
```

Before committing, verify that the tracked roots and all catalogs exactly match their sources:

```bash
python3 tools/plugin-bundles/published.py --repo . --check
```

The check rejects stale payload bytes or executable modes, missing or extra roots, unexpected files, path escape, symlinks, and manifest or catalog identity/version drift.

## Catalog and layout summary

Each catalog exposes these six plugin identities:

```text
one-button-game-builder
gameplay-debugging-toolkit
retro-arcade-game-finisher
godot-mini-game-builder
web-mini-game-kit
agent-workflow-engineering
```

Catalog entries resolve to `./plugins/<plugin>` from the repository root. Each root is independent: installed hosts copy its bundled `skills/` directories and plugin-local support files without relying on repository-level paths.

After the repository is pushed, Claude Code users can add `abagames/agentic-gamedev-skills` and install `<plugin>@agentic-gamedev-skills`. Codex CLI users can add the same `owner/repo` marketplace, list available plugins, and install `<plugin>@agentic-gamedev-skills`. Workspace administrators can import the GitHub repository through OpenAI's [plugin management](https://learn.chatgpt.com/codex/enterprise/plugin-management).

## Validation

Run the repository checks after any plugin-distribution change:

```bash
bash tools/check-readme-skills.sh
bash tools/tests/test-repository-tools.sh
bash tools/tests/test-plugin-bundles.sh
python3 tools/plugin-bundles/published.py --repo . --check
git diff --check
```

`test-plugin-bundles.sh` includes the generated-tree mutation suite and package round-trip checks. It also verifies all six composition definitions. Run the plugin-creator validator against all six Codex roots and `claude plugin validate --strict` against the Claude marketplace and each root when those host tools are available.

Use disposable configuration directories for marketplace add/list/install or removal checks. Do not use normal user plugin configuration for validation.

## Version and update procedure

The composition `version` is the version emitted into both plugin manifests. Before changing a published payload, bump that version in its composition, regenerate the tracked root, and run the validation commands above. A commit with an unchanged version should not alter the generated payload of an already published plugin.

For a user-facing update, push the reviewed version bump and regenerated catalogs/roots. Claude Code users refresh their marketplace and update the installed plugin through its documented marketplace workflow. Codex users refresh or reinstall through their configured marketplace according to their current host version and policy.

## Publication boundary

The final publication action is to review the intended source inputs, generated roots, catalogs, tests, and documentation; commit them; and push the commit to `abagames/agentic-gamedev-skills`. No archive upload, curated-directory submission, or account configuration is required for GitHub repository distribution.
