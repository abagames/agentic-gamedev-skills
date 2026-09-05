---
name: scaffolding-godot-mini-games
description: "Scaffolds a minimal Godot mini-game project from a reusable infrastructure-only template. Use when starting a Godot 4.2+ mini-game that needs headless tests, Web export defaults, canvas shell, telemetry helpers, and procedural audio primitives."
---

Use this skill to initialize a Godot mini-game from the bundled base project.

Template path:
- `assets/godot-base/`

Core rules:
- The template is infrastructure only. Do not treat it as gameplay, visual identity, or audio identity.
- Implement game-specific mechanics, visuals, and SFX in the target project after copying.
- Keep `main.gd` as orchestration and split responsibilities into focused scripts.
- Preserve Web export canvas sizing rules unless the project updates `project.godot`, `export_presets.cfg`, and `web/custom_shell.html` together.
- Do not hardcode machine-specific export template paths in the bundled template. After copying, a project may set `custom_template/debug` and `custom_template/release` to absolute local paths when using project-local XDG directories.

Set `SKILL_DIR` to the absolute directory containing this loaded `SKILL.md`, including when installed through a plugin. Then scaffold from its bundled assets:

```bash
PROJECT_DIR=tmp/games/<slug>
mkdir -p "$PROJECT_DIR"
cp -R "${SKILL_DIR:?Set SKILL_DIR to this skill directory}/assets/godot-base/." "$PROJECT_DIR"/
mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/build/web"
```

This copies the template contents directly into `<PROJECT_DIR>`. If `<PROJECT_DIR>` already contains files, inspect it before copying and do not overwrite unrelated work unless the user explicitly asked for a fresh scaffold.

Post-copy validation:

The XDG preconditions from `running-headless-godot` ("Required rules" — always set project-local `XDG_DATA_HOME` / `XDG_CONFIG_HOME` / `XDG_CACHE_HOME`) apply here too. The simplest way is to set them inline before the validation pair:

```bash
export XDG_DATA_HOME="$PROJECT_DIR/.godot-xdg/data"
export XDG_CONFIG_HOME="$PROJECT_DIR/.godot-xdg/config"
export XDG_CACHE_HOME="$PROJECT_DIR/.godot-xdg/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME"

if godot --headless --path "$PROJECT_DIR" --version > "$PROJECT_DIR/logs/version.log" 2>&1; then
  version_status=0
else
  version_status=$?
fi

if timeout 5s godot --headless --path "$PROJECT_DIR" > "$PROJECT_DIR/logs/smoke_main_initial.log" 2>&1; then
  smoke_status=0
else
  smoke_status=$?
fi

printf 'version_exit=%s\nsmoke_exit=%s\n' "$version_status" "$smoke_status"
```

Pass criteria for the validation pair:
- `version_status` is `0`, and `version.log` shows a Godot 4.2+ version line and no "Project file not found" / GDScript parse errors.
- `smoke_status` is `124`, proving `timeout` ended the run as expected for this template's lack of a
  quit hook. `smoke_main_initial.log` shows clean boot to that exit; treat any `SCRIPT ERROR` /
  `ERROR:` line outside a project-known-warning whitelist as failure.

Validation milestones:
- Post-copy: version check plus startup smoke is enough; the template intentionally has no game-specific logic.
- Post-implementation: add or update project-specific `res://tools/tests/run_tests.gd` before claiming logic, telemetry, scoring, or balance coverage.
- Pre-export: run startup smoke again, run project-specific tests when present, then export Web to `build/web/index.html`.

After copying, continue with scene editing, runtime verification, and Web export through a reproducible headless-Godot workflow (the XDG preconditions above apply throughout).
Read `assets/godot-base/TEMPLATE_SCOPE.md` before changing the template itself.
Read `references/visual-implementation-patterns.md` when implementing a visual direction from `directing-game-visuals` in Godot.
Read `references/godot-balance-pattern-examples.md` when applying `evaluating-gameplay-balance` patterns in GDScript.
