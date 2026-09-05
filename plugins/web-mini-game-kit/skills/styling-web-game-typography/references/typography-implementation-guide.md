# Typography Implementation Guide (engine-agnostic)

Implementation guide for typography in distributed games (web export, downloadable, packaged). Covers theme-based role separation, phased font adoption, and license operation, while staying consistent with the broader visual design.

For engine-specific implementation details (e.g. Godot `Theme` / `draw_string()`), see the matching reference under the same skill (`references/godot-patterns.md` for Godot 4.2+).

## 1. Purpose

- Design UI/HUD/effect text using the same visual language as the game concept.
- Balance readability with symbolic style and atmosphere.
- Prevent license issues in redistribution (web, downloadable bundles).

## 2. Design Principles

1. Role separation
   - Split display roles into `Heading / Info / Numeric / Emphasis`.
   - Fix size/weight/color/motion rules per role.

2. Consistency
   - Keep text in the same world as the rest of the visuals by matching stroke quality, color temperature, and motion quality.

3. Readability first
   - For critical info (HP, score, warnings), prioritize readability speed over decoration.
   - On noisy backgrounds, secure contrast with outlines/shadows.

4. State communication
   - Use text as a state indicator, not decoration.
   - Provide visual reactions for score gain, damage, danger, combos, etc.

## 3. Phased Implementation Flow

Typography is usually implemented in two stages: a fallback-font stage during early implementation, then a full font-adoption stage after the game feel and visual direction are stable.

When updating an existing project, first inspect its current theme/style directory, typography docs, fonts directory, license directory, and `THIRD_PARTY_LICENSES.md`. Preserve existing conventions if they already exist. If the named project path is absent, do not invent project inventory; produce a standard path-based plan and explicitly state that the local project could not be inspected.

### Initial implementation

- Implement with the engine's default/fallback font only (no external font bundling).
- Define role-based size/color tokens in a theme/style resource (see §4).
- Keep font slots empty and finish layout/effect logic first.
- Record in `TYPOGRAPHY_DECISION.md` that fonts are not selected yet and fallback is in use.
- Do not create `licenses/fonts/` or font entries in `THIRD_PARTY_LICENSES.md` for fallback-only typography.
- If `VISUAL_DESIGN.md` exists, keep only a short typography policy there: roles, size hierarchy, colors, and event text effects.

### Full font adoption

- Compare and select fonts using human feedback.
- Select the minimum font weights needed for the roles, then bundle only those adopted files into `assets/fonts/` (no bulk candidate bundling).
- If a font came from a scratch/download folder, verify the exact source release, file identity, and license before copying it. If provenance cannot be established, re-acquire only the selected weights from an authoritative source.
- Complete license checks and bundling following §7.
- Record rationale/comparison/license info in `TYPOGRAPHY_DECISION.md`.
- Update `THIRD_PARTY_LICENSES.md` and `licenses/`.

## 4. Unified Font Management via Theme/Style System

Treat the engine's theme/style system as the typography unit for the project. The token names below are recommendations; map them onto whatever the engine calls its theme/style primitives.

### 4.1 Recommended Token Set

- Font families:
  - `font_ui_base` (body/general)
  - `font_ui_display` (headings/effects)
  - `font_ui_numeric` (score/timer)
- Sizes:
  - `size_xs`, `size_sm`, `size_md`, `size_lg`, `size_xl`
- Colors:
  - `text_primary`, `text_muted`, `text_positive`, `text_warning`, `text_danger`
- Effects:
  - `outline_size`, `outline_color`, `shadow_size`, `shadow_color`

### 4.2 Operational Rules

1. Define globally in the theme/style resource first; minimize per-element overrides.
2. Keep heading/body to at most two families; at most three including numeric.
3. Reuse the same token for the same semantic meaning (e.g., all warning text uses `text_warning`).
4. Avoid readability-breaking decoration (excessive glow, heavy blur).

## 5. Implementation Patterns

### 5.1 Basics

- Set the font in the theme/style resource and apply globally to UI elements.
- Use per-element font overrides only for exceptions.
- Use monospaced or stable-width fonts for numeric HUD.

### 5.2 Practical Styling

- Edge emphasis: small outlines for background separation.
- Layer feel: subtle shadows for depth.
- State color: shift to warm hue only during danger.
- Kinetic display: brief scale/position change only during combos.
- Contextual decoration: emphasize only on important events.

### 5.3 Choosing Procedural Effect Text

Most engines distinguish between two text-rendering paths:

- **Node/widget-based** (high-level UI primitives such as labels): maintainability first.
- **Procedural / immediate-mode draw**: effect first, used for one-off animated text such as score popups, `GAME OVER`, combo callouts.

Rule: informational text is node/widget-based; effect text is draw-based.

### 5.4 Procedural Draw Layout Notes (Important)

When drawing text via the engine's procedural/immediate-mode draw API, the following pitfalls apply across most engines:

- Draw `position` is typically baseline-based, not visual-center based.
- Engine "center alignment" flags often do not center as expected when given `width = -1` (or its equivalent).
- For center-fixed text (e.g. `GAME OVER`), use one of:
  1. Set `width = viewport_width` and center-align drawing.
  2. Measure text and manually apply `x -= width / 2`.
- Correct vertical centering with font ascent/descent rather than treating the baseline as the center.
- Extra shadow/outline draws shift the visual center to bottom-right; compensate for the composite offset, or use symmetric outline drawing, then verify final placement on screen.

For an engine-specific minimum centering pattern (Godot 4.2+ `draw_string()`), see `references/godot-patterns.md`.

## 6. Mapping to Visual Tags

- `typography-*`: primary axis for font selection, spacing, and motion behavior
- `render-*`: consistency of outline/fill/line quality
- `lighting-*`: compatibility with glow/additive expressions
- `analog-*`: subtle jitter/aberration only on events
- `composition-*`: whitespace and gaze-guidance for text placement

## 7. License Operation for Distribution

### 7.1 Recommended Licenses

- `SIL Open Font License 1.1 (OFL)`
- `Apache License 2.0`
- `Ubuntu Font Licence`

### 7.2 Pre-Adoption Checklist

- [ ] Redistribution (bundling) is explicitly permitted
- [ ] Embedding use is permitted
- [ ] Commercial-use conditions are satisfied
- [ ] Naming conditions for modifications are understood (e.g., OFL RFN)
- [ ] License-text bundling requirement can be met
- [ ] Exact source URL/release and bundled file names/weights are recorded
- [ ] Scratch/download files are matched to the source release, or replaced with files acquired from an authoritative source

### 7.3 Bundling Steps

1. Place only selected font weights in `assets/fonts/`.
2. Place corresponding license texts in `licenses/fonts/`.
3. Verify export settings so non-resource text files are not dropped (this is engine-specific; see `godot-patterns.md` §Web export filtering for Godot).
4. Document font name, source URL/release, bundled file names, weights, and license in `THIRD_PARTY_LICENSES.md`.
5. Confirm the build no longer relies only on the engine's fallback font; explicitly load the adopted font file(s).

## 8. Recommended Directory Structure

```text
<PROJECT_DIR>/
  assets/fonts/
    UiBase-Regular.ttf
    UiDisplay-Bold.ttf
    UiNumeric-Semibold.ttf
  themes/                 # or styles/, depending on engine convention
    default_theme.<ext>
  licenses/fonts/
    OFL-UiBase.txt
    LICENSE-UiDisplay.txt
```

## 9. Required Deliverables per Game

For each game project, record the typography decision and license state under the project directory.

- `TYPOGRAPHY_DECISION.md`
  - Record fallback/adoption state, role mapping, selected font files, rationale, and license status.
- `VISUAL_DESIGN.md`
  - Document a short typography policy summary only (roles, size hierarchy, colors, effect rules).
- `THIRD_PARTY_LICENSES.md`
  - Document adopted external font source and license; omit font entries while using fallback only.
- `licenses/`
  - Include full license texts for adopted external fonts only.

## 10. Review Checklist

The §2 Design Principles (role separation, consistency, readability first, state communication) cover the foundational checks. After running those, also verify:

- [ ] Distribution-target license bundling is completed
- [ ] Center-fixed text (e.g. game over) is visually centered in real rendering (procedural-draw align/width checked)
- [ ] Baseline-derived Y offset is within acceptable range
- [ ] After non-visual tests (headless / unit) pass, UI layout is still correct in the actual export target

## 11. Final-Target Visual Check (Required)

Headless or non-visual tests can miss typography placement drift. After exporting to the real target (web build, packaged binary), check at minimum:

- HUD remains readable in both 16:9 and tall-ish windows.
- Center text like `GAME OVER` is truly centered.
- Decorations (shadow/outline/color separation) do not hurt readability.
- The final rendered composite is centered, not just the fill glyph; use a temporary center guide or screenshot overlay if needed.

## 12. Anti-Patterns

- Bundling fonts without license verification
- Assuming engine center-alignment flags alone guarantee centering and skipping visual confirmation
