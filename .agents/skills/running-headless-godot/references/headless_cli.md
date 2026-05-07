# Headless CLI

Preconditions inherited from `SKILL.md`: the XDG block + `--headless --path <PROJECT_DIR>` shape from "Required rules" and "Minimum smoke wrapper template" applies to every command shown below.

Recommended CLI shape for `--script` runs (assumes the XDG preconditions above are already exported):
```bash
mkdir -p <PROJECT_DIR>/logs
godot --headless --path <PROJECT_DIR> --script <SCRIPT_PATH> -- <ARGS...> 2>&1 | tee <PROJECT_DIR>/logs/run.log
```

Conventions:
- Write scripts assuming **relative paths resolve from `project.godot` (= the project root)**
- If `--headless` is unavailable on the target binary, fall back to `--display-driver headless --audio-driver Dummy`
- Scripts run via `--script` must always `quit(0|1)` (never hang)

Known script warnings:
- `Failed to open 'user://logs/...'` followed by a crash is an environment failure; re-run with the XDG-safe wrapper before debugging project code
- `RID/Object leak` warnings can appear after `--script` scene generation/saving even when execution succeeds
- If exit code is `0` and expected outputs were generated, treat this as a known warning (not an immediate failure)
- If exit code is non-zero, or expected test output is missing, treat as failure regardless of warning type
- Prefer reducing leaks by explicitly freeing temporary nodes/resources and keeping script lifetime short before `quit(0|1)`

Minimal sanity checks:
```bash
godot --version
mkdir -p <PROJECT_DIR>/logs
godot --headless --path <PROJECT_DIR> --version 2>&1 | tee <PROJECT_DIR>/logs/version.log
```
