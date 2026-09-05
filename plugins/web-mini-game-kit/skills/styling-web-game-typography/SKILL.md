---
name: styling-web-game-typography
description: "Implements readable, licensed typography for distributed games (web export, downloadable, packaged). Use when defining theme-based text roles, adopting fonts, handling font licenses for redistribution, or checking HUD readability. Engine-agnostic core; Godot 4.2+ implementation patterns live in references/godot-patterns.md."
---

Use this skill when a game needs intentional text styling, font adoption, or license-compliant font bundling for distribution.

Default artifacts:
- `<PROJECT_DIR>/TYPOGRAPHY_DECISION.md` — typography decisions, role mapping, fallback/adoption state, license status.
- `<PROJECT_DIR>/VISUAL_DESIGN.md` — short visual-policy summary (roles, size hierarchy, colors, event text effects); do not duplicate font provenance or license detail here.
- `<PROJECT_DIR>/assets/fonts/` — bundle ONLY adopted font weights, not bulk candidate dumps.
- `<PROJECT_DIR>/licenses/fonts/` — full license texts for adopted fonts.
- `<PROJECT_DIR>/THIRD_PARTY_LICENSES.md` — adopted external font source and license summary.

When updating an existing project, inspect its current theme/style directory, typography docs, font directory, and license directory before choosing file paths. If the named project path is absent, produce a standard path-based plan and state that project inventory was skipped.

During fallback-font implementation, explicitly record that no external font is adopted yet and do not create font license files or third-party font entries.

During font adoption, bundle only the selected weights. If fonts came from a scratch/download folder, verify the exact source release and license before copying; if provenance cannot be established, re-acquire only the selected weights from an authoritative source.

Core rules:
- Centralize font, color, and size through the engine's theme/style system; minimize per-element overrides.
- Use explicit roles: Heading, Info, Numeric, and Emphasis.
- Keep HUD text informational; reserve emphasis treatments for events.
- Use stable-width (monospaced or tabular) numeric presentation for score, timers, and counters.
- Ensure text stays readable over motion or noisy backgrounds with outline, shadow, or contrast bands.
- Bundle only adopted fonts and include their license texts.
- For procedurally rendered effect text (engine canvas / `_draw` / immediate-mode draw API), handle baseline positioning, horizontal centering, and outline/shadow composite offsets explicitly; verify the rendered result in the actual export target.

Workflow:
1. Start with the engine's default/fallback font during early implementation.
2. Define role tokens in a theme/style resource.
3. During final adoption, compare candidate fonts against visual direction and readability.
4. Select the minimum weights needed for the roles, then bundle only those files.
5. Update license docs and export-target checks (e.g. ensure non-resource license text files are not dropped on web export).

References:
- `references/typography-implementation-guide.md` — engine-agnostic guide: design principles, phased flow, theme tokens, implementation patterns, license operation, deliverables, review checklist, web visual check, anti-patterns.
- `references/godot-patterns.md` — Godot 4.2+ specifics: `Theme` / `ThemeDB.fallback_font` / `FontFile` setup, `Label` vs `_draw()` choice, `draw_string()` baseline + composite offset (with GDScript pattern), `res://` paths, Godot Web export font-drop check.
