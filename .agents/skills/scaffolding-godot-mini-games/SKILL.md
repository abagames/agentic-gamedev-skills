---
name: scaffolding-godot-mini-games
description: "Scaffolds a minimal Godot mini-game project from a reusable infrastructure-only template. Use when starting a Godot 4.2+ mini-game that needs headless tests, Web export defaults, canvas shell, telemetry helpers, and procedural audio primitives."
---

The bundled `assets/godot-base/` is infrastructure, not gameplay or visual/audio
identity. After copying it, keep `main.gd` as orchestration and implement
game-specific responsibilities in focused scripts.

Set `SKILL_DIR` to the absolute directory containing the loaded `SKILL.md`
(including plugin installs). Inspect a nonempty destination first; never overwrite
unrelated work without explicit fresh-scaffold authorization. Then run:

```bash
PROJECT_DIR=tmp/games/<slug>
mkdir -p "$PROJECT_DIR"
cp -R "${SKILL_DIR:?Set SKILL_DIR to this skill directory}/assets/godot-base/." "$PROJECT_DIR"/
mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/build/web"
```

Use project-local XDG directories for this and every later headless Godot command:

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

Pass only when `version_status=0`, the log reports Godot 4.2+ with no missing
project or parse error, and `smoke_status=124` (the template has no quit hook).
Any non-whitelisted `SCRIPT ERROR` or `ERROR:` in the startup log fails the check.

Validation milestones:
- Post-copy: version check plus startup smoke is enough; the template intentionally has no game-specific logic.
- Post-implementation: add or update project-specific `res://tools/tests/run_tests.gd` before claiming logic, telemetry, scoring, or balance coverage.
- Pre-export: run startup smoke again, run project-specific tests when present, then export Web to `build/web/index.html`.

Preserve Web canvas sizing unless `project.godot`, `export_presets.cfg`, and
`web/custom_shell.html` change together. Never put machine-specific export-template
paths in the bundled template; a copied project may use absolute local custom
template paths with project-local XDG directories.

Before editing the template read `assets/godot-base/TEMPLATE_SCOPE.md`. For later
Godot work, read `references/visual-implementation-patterns.md` when implementing
`directing-game-visuals`, and `references/godot-balance-pattern-examples.md` when
implementing `evaluating-gameplay-balance` patterns.
