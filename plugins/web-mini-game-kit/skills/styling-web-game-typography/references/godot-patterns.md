# Godot 4.2+ Typography Implementation Patterns

Engine-specific implementation patterns for `styling-web-game-typography` when the target engine is Godot 4.2+. Read the engine-agnostic principles in `typography-implementation-guide.md` first; this file only fills in the Godot-specific surface (resource types, paths, draw API, web export quirks).

Scope:
- Godot 4.2+ (Godot 3.x is out of scope).

## Theme and Font Resources

- Treat `Theme` as the typography unit for the project. Map the engine-agnostic token set in §4 of the guide onto Godot `Theme` properties:
  - Font families → `font_*` theme entries holding `FontFile` resources
  - Sizes → `default_font_size` plus per-control size overrides via theme types
  - Colors → theme color entries (`font_color`, `font_color_disabled`, etc.)
  - Effects → `font_outline_color`, `outline_size`, shadow offset/color
- Place the project theme at `res://themes/default_theme.tres` and apply it globally so individual controls inherit by default.
- Use `theme_override_*` properties on `Label` / `RichTextLabel` only for explicit per-instance exceptions.

## Fallback Font Stage

- Implement with `ThemeDB.fallback_font` only — do NOT bundle external font files yet.
- Define role-based size/color tokens in the `Theme` resource as usual; only the font slots stay empty.
- Record in `TYPOGRAPHY_DECISION.md` that fonts are not yet selected and `ThemeDB.fallback_font` is in use.
- Do not create `res://licenses/fonts/` or font entries in `THIRD_PARTY_LICENSES.md` while only the fallback is in use.

## Adoption Stage

- Bundle only the selected font weights under `res://assets/fonts/`.
- Place the corresponding license texts under `res://licenses/fonts/`.
- Update `THIRD_PARTY_LICENSES.md` with font name, source URL/release, bundled file names, weights, and license.
- Confirm code no longer relies only on `ThemeDB.fallback_font`; the `FontFile` resources are explicitly loaded into the `Theme`.

## Label vs `_draw()` Choice

Godot exposes two text-rendering paths and the choice should be deliberate:

- Normal UI: `Label` / `RichTextLabel` (maintainability first).
- Effect UI: `CanvasItem._draw()` + `draw_string()` (effect first; one-shot animated text such as score popups, `GAME OVER`, combo callouts).

Rule: informational text is node-based; effect text is draw-based.

## `draw_string()` Layout Notes (Important)

- `draw_string()` `position` is baseline-based, not visual-center based.
- With `HORIZONTAL_ALIGNMENT_CENTER`, `width = -1` may not center as expected.
- For center-fixed text (e.g. `GAME OVER`), use one of:
  1. Set `width = viewport_width` and center-align drawing.
  2. Measure text with `font.get_string_size()` and manually apply `x -= width / 2`.
- Correct vertical centering with font ascent/descent rather than treating the baseline as the center.
- Extra shadow/outline draws shift the visual center to bottom-right; compensate for the composite offset or use symmetric outline drawing, then verify final placement on screen.

### Minimum centering pattern (GDScript)

```gdscript
var viewport_size := get_viewport_rect().size
var text_size := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size)
var ascent := font.get_ascent(font_size)
var descent := font.get_descent(font_size)
var composite_offset := Vector2.ZERO

# Example: a single positive shadow at Vector2(4, 4) shifts the perceived center.
# Shift the whole composite back by half of the min/max effect offset span.
composite_offset = Vector2(-2, -2)

var baseline := Vector2(
    viewport_size.x * 0.5 - text_size.x * 0.5,
    viewport_size.y * 0.5 + (ascent - descent) * 0.5
) + composite_offset
```

## Recommended Godot Directory Structure

```text
res://
  assets/fonts/
    UiBase-Regular.ttf
    UiDisplay-Bold.ttf
    UiNumeric-Semibold.ttf
  themes/
    default_theme.tres
  licenses/fonts/
    OFL-UiBase.txt
    LICENSE-UiDisplay.txt
```

## Web Export Filtering

Godot's web export presets can drop non-resource text files unless they are included via `Resources → Filters to export non-resource files/folders`. To preserve license texts in the web build:

- Add `licenses/fonts/*.txt` (and any `THIRD_PARTY_LICENSES.md` you ship inside the export) to the export filters.
- Re-verify after export by inspecting the `.pck` / `.zip` contents to confirm the license texts are present.

## Cross-Reference

- For role separation, phased flow rationale, license operation, deliverables, review checklist, and final-target visual check, see `typography-implementation-guide.md`.
- For headless Godot CLI workflow used during iteration (running tests, exports, scripted scene edits), see the sibling `running-headless-godot` skill.
