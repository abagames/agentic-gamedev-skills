---
name: designing-retro-arcade-sound-kits
description: "Designs and validates event-driven retro-arcade sound kits (SFX + jingles) where game code emits abstract event names and an adapter/synth layer maps and plays them. Use when authoring a per-game arcade sound set, deciding which moments need a one-shot SE vs a jingle vs no sound, keeping SEs from drifting into background music, or preserving a fixed-hardware audio character. Engine-agnostic; for Godot built-in audio APIs specifically, use creating-godot-procedural-audio instead."
---

Use this skill to design a compact, era-authentic arcade sound kit and prove it stays event-like rather than turning into background music. It assumes an event-boundary architecture: game logic emits abstract event names and a separate audio layer resolves each event to a program and plays it.

## Core Rules

- **Event boundary.** Game code emits abstract event names (e.g. `emit("laser")`); it never instantiates or calls the synth directly. The audio layer owns the event -> program mapping and playback.
- **Design from gameplay moments, not synth presets.** List the moments the player must hear first, then decide which need sound.
- **Classify each moment as SE, jingle, or nothing.** Do not give every state transition a sound.
  - SE = short, repeated gameplay feedback: player actions (shot, dash, place, rotate, confirm), consequences (hit, block, collect, miss, split, capture), warnings (low timer, nearby threat, invalid move), and ambient events that affect play (spawn, wave step).
  - Jingle = rare state changes that should read as a musical phrase: start/ready, bonus or major reward, wave/stage clear, danger entering a new phase, final miss / game over.
- **Keep it readable under load.** Repeated SEs must stay distinct when several fire in one frame; rare jingles must not mask player-control feedback.
- **Write a one-line sound target before coding each sound** (e.g. `// wave clear: rising 5-note glassy arpeggio`). Author to the target, not to whatever the synth happens to produce.
- **Per-game identity.** Each game ships its own kit; do not reuse a sample kit unchanged, and derive variants from your own programs, not from another game's.
- **Era authenticity.** Recombine a fixed primitive set (oscillators, LFSR/metallic noise, distortion, bit-crush) through one fixed, clamped master chain. Add no new synth primitives, no samples, no long modern tracks. The fixed master chain is what keeps the "1980 board" character regardless of how a kit is built.

## Workflow

1. List the moments the player must hear from the game design.
2. Classify each moment as SE / jingle / none.
3. Write a one-line sound target for each chosen sound.
4. Choose event names: reuse shared cabinet vocabulary when it fits (`coin`/`start`/`hit`/`warning`/`jingle:bonus`); use game-specific names (`gun:fire`, `window:clean`) when they make the code clearer, and map them to local programs via aliases.
5. Author each program from the primitive set; set a clamped master tone for the kit.
6. Validate against the budget and loudness checks below before finishing.

## Validation (required)

A sound kit is not done until these pass:

- **Budget, enforced by an automated test.** Cap SFX and jingle length and step count so SEs cannot drift into background music. Starting caps: SFX <= ~0.6s, jingles <= ~1.6s, <= ~24 steps per program. Wire this into the test suite, not just a manual check.
- **Relative loudness.** Tune each SE against its sibling events in the same kit, not in isolation. Foreground actions (shots, hits, warnings) must stay readable during play; cabinet chimes (coin/start/game-over) sit slightly behind foreground play.
- **Demo/attract muting.** Attract-mode sounds pass a `demo` flag (or equivalent) so they can be suppressed by a demo-sound setting.
- **Safety.** Keep the master volume conservative; with aggressive distortion/noise programs, test at low speaker/headphone volume.

## References

- `references/sound-kit-reference.md` — SE-vs-jingle table, starting loudness ranges, budget caps, and a generalized worked kit example. Read when authoring a kit.
- `references/reference-implementation.md` — one concrete realization of the event-boundary runtime (the four layers, program-as-data, fixed clamped master chain, bus-level guards, mock-adapter testing, data-driven validation). Read when building or evaluating the system that plays the kits, not when authoring a single kit.
