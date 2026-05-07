---
name: creating-godot-procedural-audio
description: "Designs and implements procedural audio for Godot games. Use when creating runtime SFX with Godot built-in audio APIs, mapping game events to timbre, or avoiding external audio assets."
---

Use this skill for Godot game audio that is synthesized or generated inside the project.

Default artifacts:
- If a project directory is known, put the full audio plan in `<PROJECT_DIR>/SOUND_DESIGN.md`.
- If the project README has a `Visual And Audio Direction` or `Required sounds` section, keep it as a short summary and update it only when the audio direction changes.
- Implement through a small project-specific module such as `<PROJECT_DIR>/audio_controller.gd`; keep `main.gd` as orchestration.
- Reuse `.agents/skills/creating-godot-procedural-audio/assets/audio_synth.gd` or the template's existing `audio_synth.gd` primitives. Copy the helper into the project only if it is missing or materially different.
- If visual tags are project-specific or concept-derived rather than exact guide entries, map them by nearest material, geometry, motion, or atmosphere family and record that mapping in `SOUND_DESIGN.md`.
- Continuous sounds should expose a minimal control surface: `start_<sound>()`, `update_<sound>(params)`, `release_<sound>()`, and `stop_<sound>()`. Headless/no-op handles must preserve the same calls so tests can verify state transitions without playback.

Core rules:
- Use Godot built-in audio only; avoid external audio files unless the project explicitly allows them.
- Keep event families semantically stable within a game: score, danger, damage, and state change should have distinct timbral identities.
- Vary waveform, pitch range, envelope, modulation, rhythm, and density between games instead of reusing a global beep vocabulary.
- Continuous sounds need explicit start, stop, and release behavior.
- Prefer simple generated sample streams when possible; use `AudioStreamGenerator` when real-time synthesis is required.

Workflow:
1. Derive sound character from the visual direction and mechanics.
2. Choose 1-2 base waveforms plus a modulation method.
3. Define event-to-timbre mappings.
4. Link dynamic parameters (combo / speed / danger / difficulty) so they audibly modulate at least one event, not just the score number.
5. Implement through a small audio responsibility module.

Read `references/sound-design-guide.md` for event catalogues, procedural audio patterns, and design checklists.
Reusable primitives are in `assets/audio_synth.gd`.

## Companion skills

- `directing-game-visuals` produces `<PROJECT_DIR>/VISUAL_DESIGN.md`, which sound character should derive from.
- `scaffolding-godot-mini-games` ships the template `audio_synth.gd` referenced above; copy this skill's `assets/audio_synth.gd` only when no template copy exists in the project.
