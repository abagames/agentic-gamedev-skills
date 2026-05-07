# Testing Headless

Preconditions inherited from `SKILL.md`: the XDG block and `--headless --path <PROJECT_DIR>` shape from "Required rules" / "Minimum smoke wrapper template" apply to every command shown below.

Scope (only this):
- Logic, resource loading, and minimal scene startup
- Rendering-dependent checks, render output validation, and input/window operations are out of scope

Minimal strategy:
- Keep `res://tools/tests/run_tests.gd` in the project and run it via `--script`
- Treat `res://tools/tests/run_tests.gd` as an agent-maintained project file (not bundled in this skill)
- You can bootstrap from `tools/templates/run_tests.gd` in this skill and copy it into the project
- Keep `run_tests.gd` focused on project-specific logic/resource checks; do not depend on it for `run/main_scene` startup coverage
- `quit(1)` on failed `assert` / exceptions; `quit(0)` on success
- After applying patches, add a smoke run that actually starts `run/main_scene` (to catch `_ready` errors)
- Do not assume metrics such as `score`, `game_over`, enemy counts, or fixed input actions unless the project already defines them

For known script warnings (RID/Object leak, etc.), see `headless_cli.md`.

Startup smoke (minimal):
```bash
mkdir -p <PROJECT_DIR>/logs
timeout 5s godot --headless --path <PROJECT_DIR> 2>&1 | tee <PROJECT_DIR>/logs/smoke_main.log
```
- Treat `Node not found` and script errors as failures
- After patches, add checks for important node counts (e.g., verify expected singleton nodes exist exactly once)

Required:
- Scripts run via `--script` must extend `SceneTree` or `MainLoop` (Godot 4)
- Use startup smoke for post-copy and scene startup coverage. Use `res://tools/tests/run_tests.gd` for project-specific logic, scoring, telemetry, and balance checks after those systems exist.

Optional:
- You may use external test frameworks (GUT, etc.), but this skill does not document those workflows.
