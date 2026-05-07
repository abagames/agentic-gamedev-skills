# Export And Import

Preconditions inherited from `SKILL.md`: the XDG block and `--headless --path <PROJECT_DIR>` shape from "Required rules" / "Minimum smoke wrapper template" apply to every command shown below.

Minimal rules:
- Use `--export-release` / `--export-debug` / `--export-pack` based on your goal
- `--export-*` is only available in the **editor build** (not in export template binaries)
- Treat `--export-*` as implicitly including `--import`
- If the output path is relative, assume it resolves from **`project.godot` (= project root)**
- For `--export-pack`, the output format is determined by extension (`.pck` or `.zip`)

Prerequisites (minimal):
- `export_presets.cfg` exists
- Export templates are installed

## Web Export

Command:
```bash
mkdir -p <PROJECT_DIR>/build/web <PROJECT_DIR>/logs
godot --headless --path <PROJECT_DIR> \
  --export-release "Web" build/web/index.html \
  2>&1 | tee <PROJECT_DIR>/logs/web_export.log
```

`export_presets.cfg` example:
```ini
[preset.0]
exclude_filter="build/web/*"

[preset.0.options]
custom_template/debug="/home/alice/.local/share/godot/export_templates/4.6.1.stable/web_nothreads_debug.zip"
custom_template/release="/home/alice/.local/share/godot/export_templates/4.6.1.stable/web_nothreads_release.zip"
```

- `exclude_filter`: prevents previously generated outputs from being re-included in the next export
- `custom_template/*`: pins absolute paths to Export Templates (required if you switch XDG directories)

### XDG and Export Templates

The XDG block is set per "Required rules" in `SKILL.md`. Export-specific consequences:

- Once `XDG_DATA_HOME` points into the project (per the rule), the Export Templates lookup path also moves to `XDG_DATA_HOME/godot/export_templates/...` — Godot will not find templates installed under the user's global `~/.local/share/godot/`.
- To keep using a globally-installed template set, pin absolute paths under `custom_template/*` in `export_presets.cfg` (as in the example above).
- Before setting `custom_template/*`, run `godot --version` and look for matching Web templates under the global user data directory, e.g. `~/.local/share/godot/export_templates/<version>/web_nothreads_release.zip`. If templates cannot be found, report the missing template path and the export log instead of guessing.

### Known Warnings

You may see `TCP listen` warnings in headless runs. If `build/web/index.html` / `index.pck` / `index.wasm` are generated, it is usually fine.
