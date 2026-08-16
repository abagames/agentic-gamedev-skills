---
name: generating-dot-assets
description: "Generates transparent pixel-art object assets from a subject and target pixel size using a host-provided image-generation tool, chroma-key removal, pixelization, exact canvas fitting, and PNG validation. Use for game objects, sprites, props, item icons, and diorama layers. Requires Codex's built-in `image_gen` (or an equivalent image-generation entry point) and ImageMagick `convert` on PATH."
---

# Dot Asset Generator

Create transparent pixel-art object assets from a natural-language subject and an exact target size such as `32x32`, `64x64`, or `96x48`.

Use this skill when the user asks for a game object, sprite-like prop, item icon, diorama object, or transparent pixel-art asset generated from image generation.

## Environment requirements

- An image-generation tool callable from the agent. The bundled workflow assumes Codex's built-in `image_gen` and reads its output from `$CODEX_HOME/generated_images/...`. On other hosts (Claude Code, plain CLI), substitute an equivalent generator and copy the chosen image into `<PROJECT_DIR>/assets/source/<stem>.raw.png`.
- In Codex CLI, built-in `image_gen` output may not appear under `$CODEX_HOME/generated_images` even when generation succeeds. If no current output file is visible, recover the PNG from the Codex session JSONL before retrying generation; see `references/imagegen-cli-recovery.md`.
- ImageMagick `convert` on PATH. The bundled `scripts/*.mjs` shell out to it; if it is missing, stop and report the dependency rather than fabricating output.

## Inputs

Require:

- subject, e.g. `old wooden school desk`
- final size, e.g. `64x64`
- output path or output directory

Optional:

- style notes
- palette JSON with a `colors` array
- raw output directory
- color count
- chroma-key color
- fit mode: `contain` or `stretch`

Default project layout:
- Use `<PROJECT_DIR>/assets/source/` for prompt records, copied raw images, cutouts, pixelized intermediates, and optional palette JSON files.
- Use `<PROJECT_DIR>/assets/sprites/` for final validated transparent PNGs.
- Use `<stem>.prompt.md`, `<stem>.raw.png`, `<stem>.cutout.png`, `<stem>.pixel.png`, and `<stem>.palette.json` for generated working files.
- If the final filename already exists and overwrite was not explicitly requested, use `<stem>_v2.png`, then `_v3`, etc. Apply the same suffix to prompt, raw, cutout, pixel, and palette files for that run.
- For role-based game assets, read `<PROJECT_DIR>/VISUAL_DESIGN.md` or the README visual direction first. Explicit user or scenario constraints may be used when those files are unavailable; report the missing design docs and record the constraints in the prompt file. If neither design docs nor explicit constraints define role colors, define a minimal Player / Danger / Reward palette (or run a visual-direction pass first) before generating.
- Use `--colors <N>` for exploratory or one-off assets when exact project colors are not required. Create and pass a palette JSON when assets must share a project palette, match role colors, or stay consistent across a set.

## Workflow

1. Read `references/prompt-patterns.md`, then prompt built-in `image_gen` for an oversized source image of exactly one object on the selected chroma-key background.
2. Copy the selected generated image from `$CODEX_HOME/generated_images/...` into the project raw directory.
3. Run `scripts/cutout.mjs` to remove the chroma-key background.
4. Run `scripts/pixelize.mjs` to reduce detail and apply a palette or color limit.
5. Run `scripts/fit-canvas.mjs` to enforce the exact requested `WxH` transparent canvas.
6. Run `scripts/validate-pixel-asset.mjs`, then apply the automated and visual acceptance checks in `references/validation.md`.
7. Save a prompt record in the source directory using `<stem>.prompt.md` unless the project has a stronger convention.

Prefer project-local equivalent tools if they already exist and satisfy the same contract. Otherwise use this skill's bundled scripts.

## Commands

Examples assume the current repository layout and set `SKILL_DIR` explicitly.

```bash
SKILL_DIR=.agents/skills/generating-dot-assets
node "$SKILL_DIR/scripts/cutout.mjs" raw.png tmp/cutout.png --trim --fuzz 8%
node "$SKILL_DIR/scripts/pixelize.mjs" tmp/cutout.png tmp/pixel.png --width 96 --colors 24 --dither off
node "$SKILL_DIR/scripts/fit-canvas.mjs" tmp/pixel.png final.png --size 64x64 --fit contain --gravity center
node "$SKILL_DIR/scripts/validate-pixel-asset.mjs" final.png --size 64x64 --max-colors 24 --transparent-corners
```

With a palette:

```bash
SKILL_DIR=.agents/skills/generating-dot-assets
node "$SKILL_DIR/scripts/pixelize.mjs" tmp/cutout.png tmp/pixel.png --width 96 --palette palette.json --dither off
```

Palette files must contain a `colors` array of hex colors:

```json
{
  "colors": ["#1b1f3a", "#f04438", "#f97316", "#facc15", "#38bdf8", "#f8fafc"]
}
```

## Rules

- Do not rely on image generation to produce exact pixel dimensions.
- Do not leave final sizing to `pixelize`; always enforce the requested dimensions with `fit-canvas`.
- Use `contain` for most object assets so the subject is not cropped.
- Generate one object per image. Batches should use one built-in `image_gen` call per object.
- Keep raw generated images and final transparent PNGs separate.
- Do not overwrite existing assets unless explicitly asked; create a versioned filename instead.
- Do not require an explicit palette for every asset. Use one when the project already defines colors, when role colors matter, or when multiple assets must look like they belong to the same set.
- Default pixelize resize: use an intermediate long edge about 2x the final long edge. For square or landscape assets, set `--width` to `final_width * 2`; for portrait assets, set `--height` to `final_height * 2`. Use both `--width` and `--height` only when intentional pre-fit stretching is acceptable.

## Failure Handling

- If chroma-key removal leaves a colored fringe, retry `cutout` with a higher `--fuzz` or regenerate with more padding and stricter flat-background wording.
- If built-in `image_gen` appears to succeed but no output file is available under `$CODEX_HOME/generated_images`, do not assume generation failed. Recover the PNG from the Codex session JSONL using `references/imagegen-cli-recovery.md`, then continue from the raw-image copy step.
- If the subject is cropped, regenerate with stronger padding instructions or use a larger intermediate size.
- If the object becomes unreadable at final size, regenerate with simpler shapes or pixelize from a less detailed source.
- If ImageMagick `convert` is unavailable, report that the bundled scripts require ImageMagick and stop.

## References

- `references/prompt-patterns.md` — canonical image-generation prompts and key-color selection.
- `references/validation.md` — canonical automated and visual acceptance checks.
- `references/imagegen-cli-recovery.md` — recover successful Codex CLI image output when no generated file is visible.
