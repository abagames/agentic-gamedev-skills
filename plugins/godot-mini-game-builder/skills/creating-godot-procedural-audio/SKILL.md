---
name: creating-godot-procedural-audio
description: "Designs and implements procedural audio for Godot games. Use when creating runtime SFX with Godot built-in audio APIs, mapping game events to timbre, or avoiding external audio assets."
---

Use this skill for audio synthesized inside a Godot project.

Artifacts and boundaries:
- If a project directory is known, put the full audio plan in `<PROJECT_DIR>/SOUND_DESIGN.md`.
- Keep an existing README `Visual And Audio Direction` or `Required sounds` section to a short summary, updated only when direction changes.
- Implement through a small project-specific module such as `<PROJECT_DIR>/audio_controller.gd`; keep `main.gd` as orchestration.
- Reuse the template's existing `audio_synth.gd`, or resolve `assets/audio_synth.gd` relative to this loaded skill. Copy only when the helper is missing or materially different.
- Map unfamiliar project/concept visual tags to the nearest material, geometry, motion, or atmosphere family and record the mapping in `SOUND_DESIGN.md`.
- Continuous sounds should expose a minimal control surface: `start_<sound>()`, `update_<sound>(params)`, `release_<sound>()`, and `stop_<sound>()`. Headless/no-op handles must preserve the same calls so tests can verify state transitions without playback.

Rules:
- Use built-in Godot audio; external files require explicit project permission.
- Keep event families semantically stable within a game: score, danger, damage, and state change should have distinct timbral identities.
- Vary waveform, pitch, envelope, modulation, rhythm, and density between games; do not reuse a global beep vocabulary.
- Prefer generated sample streams; use `AudioStreamGenerator` only for required real-time synthesis.

Workflow:
1. Derive sound character from mechanics and visual direction.
2. Choose 1–2 base waveforms and modulation.
3. Define event-to-timbre mappings.
4. Make combo, speed, danger, or difficulty audibly modulate at least one event.
5. Implement through a small audio responsibility module.

Read `references/sound-design-guide.md` for event catalogues, synthesis patterns, and checks. Reusable primitives are in `assets/audio_synth.gd`.

## Companion skills

- `directing-game-visuals` produces `<PROJECT_DIR>/VISUAL_DESIGN.md`, which sound character should derive from.
- `scaffolding-godot-mini-games` ships the template `audio_synth.gd` referenced above; copy this skill's `assets/audio_synth.gd` only when no template copy exists in the project.
