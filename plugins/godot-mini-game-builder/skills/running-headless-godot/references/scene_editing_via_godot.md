# Scene Editing Via Godot

Preconditions inherited from `SKILL.md`:
- Set project-local `XDG_DATA_HOME` / `XDG_CONFIG_HOME` / `XDG_CACHE_HOME` before any `godot` invocation in this file (see SKILL.md "Required rules" and "Minimum smoke wrapper template" — the same XDG block prefix applies to every command shown below).

Goal:
- Update `.tscn` safely (**no direct text edits**)

One-way flow:
- `patch.json` (reviewable) -> `godot_apply_patch.gd` (apply) -> save `.tscn`

Standard patch commands (assume the XDG preconditions above are already exported):
```bash
mkdir -p <PROJECT_DIR>/logs
godot --headless --path <PROJECT_DIR> --script res://tools/godot_apply_patch.gd -- <PATCH_JSON_PATH> --dry-run 2>&1 | tee <PROJECT_DIR>/logs/patch_dry_run.log
godot --headless --path <PROJECT_DIR> --script res://tools/godot_apply_patch.gd -- <PATCH_JSON_PATH> 2>&1 | tee <PROJECT_DIR>/logs/patch_apply.log
```

Patch input requirements:
- `<PATCH_JSON_PATH>` must be an absolute path or `res://` (no relative paths)
- Run `--dry-run` first for NodePath/type pre-validation

Patch JSON minimal schema:
```json
{
  "scene_path": "res://path/to/scene.tscn",
  "operations": [
    { "op": "set_property", "node": "SomeNode", "property": "visible", "value": true }
  ]
}
```

Allowed operations:
- `set_property`: `node` `property` `value` (primitive) / `value_variant` (for `str_to_var`)
- `rename_node`: `node` `new_name`
- `add_child_scene`: `parent` `child_scene` (PackedScene) `name` (optional)
- `delete_node`: `node` (requires `--allow-delete`; disallowed by default)

Extra rules for `rename_node`:
- After renaming, always update code references to the old node name (`$OldName`, `get_node("OldName")`, etc.)
- If you are not going to update references, do not use `rename_node` (use `set_property`, etc.)

Patch run rules:
- If `add_child_scene` specifies `name`, replace an existing node with the same name for idempotent application
- Do not use `set_property` in the same patch against nodes under an instance added via `add_child_scene`; the instanced scene already defines those properties, so overriding them causes duplication or silent conflicts after save — edit that original scene instead

Safety:
- Run `--dry-run` first (NodePath resolution / type checks only)
- Create a `.bak` before saving (restore it on failure and `quit(1)`)
- Abort immediately if NodePath resolution fails (no partial application)
- `--dry-run` does not catch runtime errors (e.g. broken references inside `_ready`); always run a smoke start after applying

Save strategy:
- `PackedScene.load -> instantiate -> edit -> PackedScene.pack -> ResourceSaver.save`
- Saving can change `owner` and other details, so keep patches small and minimal.
