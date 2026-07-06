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
timeout -k 2 5 godot --headless --path <PROJECT_DIR> > <PROJECT_DIR>/logs/smoke_main.log 2>&1
echo "godot_exit=$?"
```
- Treat `Node not found` and script errors as failures
- After patches, add checks for important node counts (e.g., verify expected singleton nodes exist exactly once)
- **Do not pipe this command through `tee`** (i.e. do not use `timeout ... | tee log`). When a project has no internal quit condition (no `--quit-after`, no `quit()` call), `timeout` is the only thing killing the process; observed in practice, that combination can leave the pipeline blocked well past the timeout in headless/sandboxed environments (the run hung for the surrounding tool's full default wall-clock limit instead of exiting at 5s), even though redirecting straight to a file with the same `timeout` terminates cleanly. Redirect to a file (`> log 2>&1`) instead, and `cat`/read the file afterward if you want to see it inline. This only applies when `timeout` is the sole thing ending the process — a script that calls `quit(0|1)` itself, or a run using `--quit-after N`, exits on its own and is not affected, so piping through `tee` there is fine.

Required:
- Scripts run via `--script` must extend `SceneTree` or `MainLoop` (Godot 4)
- Use startup smoke for post-copy and scene startup coverage. Use `res://tools/tests/run_tests.gd` for project-specific logic, scoring, telemetry, and balance checks after those systems exist.
- Reference project-defined global classes (anything declared with `class_name`) via `const Foo = preload("res://path/to/foo.gd")` inside any file invoked directly with `--script`, not by the bare global class name. The global class cache (`.godot/global_script_class_cache.cfg`) is built when the editor opens/scans the project; a script run via `--script` right after a new `class_name` file is added (e.g. a freshly generated `res://tools/tests/run_tests.gd` referencing a same-session `res://engine/foo.gd`) can hit `Identifier "Foo" not declared in the current scope` because that cache does not exist yet. `preload()` sidesteps the cache entirely and works regardless of scan state.
- When a `--script` test instantiates a real scene (via `load(...).instantiate()` + `add_child`) rather than just calling pure functions, be aware that `_ready()`/`@onready` var propagation and `SceneTreeTimer` (`create_timer().timeout`) both depend on the main loop actually iterating:
  - Override `_initialize()` for one-time setup that must run after the tree is live, not `_init()` — code in `_init()` runs before the loop starts, so a node added there can still report `is_inside_tree() == false` and its `@onready` vars can still be unset.
  - When waiting for something scheduled with `create_timer()`/`await`, budget on wall-clock time (`Time.get_ticks_msec()`), not a frame count — headless mode iterates as fast as the CPU allows, so a fixed frame budget can correspond to a wildly different amount of real elapsed time than the same budget in windowed mode, and a timer keyed to real seconds needs a real-time budget to match it.

Optional:
- You may use external test frameworks (GUT, etc.), but this skill does not document those workflows.
