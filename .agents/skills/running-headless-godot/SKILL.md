---
name: running-headless-godot
description: "Runs reproducible headless Godot 4.2+ workflows for CLI commands, exports, scripted scene edits, and tests. Use when running Godot CLI commands, editing .tscn via script, capturing logs, or exporting in headless mode."
---

Rules for making headless Godot (4.2+) development reproducible, avoiding drift and environment-specific failures.

Scope:
- Godot 4.2+ (Godot 3.x is out of scope)

Required rules (highest priority):
- Always use `--headless --path <PROJECT_DIR>` (removes `cwd` dependency)
- Always capture logs under the project: `2>&1 | tee <PROJECT_DIR>/logs/<name>.log`
- Always set project-local `XDG_DATA_HOME`, `XDG_CONFIG_HOME`, **and** `XDG_CACHE_HOME` for any scripted Godot run. Set all three together — Godot writes to all three categories, and partial redirection still hits the unwritable default for the unset ones. Required to avoid CI/sandbox write failures (`Can't open file for writing: ~/.config/godot/...`); harmless on a developer machine because the only effect is that per-project metadata/cache live under `<PROJECT_DIR>/.godot-xdg/` instead of the user's globals. Add `.godot-xdg/` to `.gitignore`.
  - These `export`s affect every process started from the same shell, not just `godot`. If the same shell session also runs non-Godot tooling that honors XDG vars (e.g. a Node/Playwright browser-automation step for web-export testing), that tooling's own cache/data lookup silently moves under `<PROJECT_DIR>/.godot-xdg/` too and can fail to find things it installed elsewhere (observed: Playwright reporting a missing browser executable). Export these three vars only in the specific command/subshell that invokes `godot`, or explicitly unset/restore them before running unrelated tools in the same shell.
- Never edit `.tscn` as raw text (edits must go through `--headless --script`)
- For repeated validation commands, standardize them as `tools/*.sh`; after manual tweaks, re-run via the same scripts
- If `res://tools/godot_apply_patch.gd` is missing, copy `.agents/skills/running-headless-godot/tools/godot_apply_patch.gd` to `<PROJECT_DIR>/tools/godot_apply_patch.gd` before running patch commands
- Keep startup smoke and logic tests separate: smoke starts `run/main_scene`; `run_tests.gd` holds project-specific logic checks

## Minimum smoke wrapper template

For repeated startup verification, standardize as `<PROJECT_DIR>/tools/smoke.sh`. Other repeated invocations (`run_tests.sh`, `export_web.sh`, ...) follow the same shape — only the godot arguments and the log filename change.

```bash
#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Project-local XDG (always; see Required rules above).
export XDG_DATA_HOME="$PROJECT_DIR/.godot-xdg/data"
export XDG_CONFIG_HOME="$PROJECT_DIR/.godot-xdg/config"
export XDG_CACHE_HOME="$PROJECT_DIR/.godot-xdg/cache"
mkdir -p "$XDG_DATA_HOME" "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$PROJECT_DIR/logs"

# Smoke = launch run/main_scene headlessly, quit after a few frames.
# --quit-after <N> bounds the run by frame count.
godot --headless --path "$PROJECT_DIR" --quit-after 60 \
  2>&1 | tee "$PROJECT_DIR/logs/smoke.log"
echo "godot_exit=${PIPESTATUS[0]}"
```

Pass criteria for smoke:
- Captured exit code (`${PIPESTATUS[0]}`) is `0`.
- `logs/smoke.log` contains no `ERROR`, `SCRIPT ERROR`, `Failed to load`, or `Parse Error` line outside the project's known-warning whitelist (see `references/headless_cli.md`).
- A startup-visible marker is present (e.g. a `print()` from the main scene's `_ready`, or absence of "Main scene can't be loaded").

If you get stuck, provide:
- Full command lines and `logs/*.log`
- `godot --version` output
- Whether `export_presets.cfg` exists (when exporting)

Out of scope:
- GUI/OS-specific setup beyond the project-local XDG wrapper
- Level design, render validation, performance tuning
- Game-specific scoring, win/loss rules, controls, and simulation policies

When you need details, read these files (relative to this skill's base directory):
- `references/headless_cli.md` — CLI conventions, XDG setup, known warnings
- `references/export_and_import.md` — export/import rules
- `references/scene_editing_via_godot.md` — safe `.tscn` editing, patch JSON schema and operations
- `references/testing_headless.md` — headless testing strategy

If unsure about Godot CLI or features, consult:
- https://docs.godotengine.org/en/4.4/tutorials/editor/command_line_tutorial.html
- https://docs.godotengine.org/en/4.4/tutorials/export/exporting_for_dedicated_servers.html
- https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html
