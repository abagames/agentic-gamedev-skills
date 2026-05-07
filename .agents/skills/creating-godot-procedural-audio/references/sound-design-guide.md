# Sound Design Guide

A guide for designing the sound layer of action mini-games using procedural audio generation in Godot 4.2+. Sound design derives its direction from visual tags — no separate sound tags are used. No external audio assets are required; all sounds are synthesized at runtime via GDScript.

## 1. Design Challenges

- Generating distinctive, satisfying sound effects without pre-recorded assets.
- Maintaining audio–visual coherence — sounds must feel like they belong to the same world as the visuals.
- Providing clear auditory feedback that reinforces (not duplicates) visual feedback.
- Keeping procedural audio code compact and performant within the mini-game scope.

## 2. Five Core Audio Principles and Evaluation Criteria

### (1) Event Clarity

- Principle: Every significant game event must produce a distinct sound. The player should be able to identify what happened by sound alone — scoring, damage, near miss, and game over must be aurally distinguishable.
- Evaluation: Can a player identify the event type with eyes closed? Are different event magnitudes (1 point vs. 10 points) audibly different?

### (2) Audio–Visual Coherence

- Principle: Sound style must match the visual identity. A neon-glow game should sound synthetic and resonant; a geometric-primitive game should sound clean and percussive. The visual tags drive both domains.
- Evaluation: Does the sound feel like it comes from the same world as the visuals? Would swapping in generic 8-bit sounds feel out of place?

### (3) Restraint

- Principle: Fewer, well-designed sounds are better than many generic ones. A mini-game needs 4–8 distinct sound events at most. Each sound should be short (50–500ms) and purposeful. Silence is a valid design element.
- Evaluation: Does any sound feel unnecessary? Is there sonic clutter during intense gameplay?

### (4) Dynamic Response

- Principle: Sounds should react to game state — pitch rises with combo multiplier, impact sounds scale with velocity, danger sounds intensify as difficulty increases. Static, unchanging sounds feel lifeless.
- Evaluation: Do sounds change with gameplay intensity? Can the player sense escalation through audio alone?

### (5) Semantic Lock (In-Game) and Variation (Cross-Game)

- Principle: Within a single game, each event family (`score / danger / damage / state change`) should keep a consistent timbral identity for fast recognition. Across different games, that identity must be redesigned from visual tags and game concept — not copied as a global template.
- Clarification:
  - **In-game fixed**: Event meaning ↔ timbre mapping stays stable during one game's session.
  - **Cross-game variable**: Waveform set, pitch range, envelope shape, modulation style, and rhythmic spacing should change per game.
- Evaluation: Is event meaning instantly recognizable in this game? Would this game's sounds be distinguishable from another generated game?

## 3. Visual Tag → Sound Direction Mapping

Sound direction is derived from visual tags. The following table provides starting points — not rigid rules.

### 3.1 Render Tags

| Visual Tag Category             | Sound Direction           | Waveform Tendency       | Character                     |
| :------------------------------ | :------------------------ | :---------------------- | :---------------------------- |
| `render-glow-outline`           | Warm, resonant, sustained | Sine + light overdrive  | Smooth attack, lingering tail |
| `render-soft-bloom-outline`     | Soft, padded, ambient     | Filtered sine           | Gentle onset, breathy         |
| `render-wireframe-lines`        | Thin, precise, dry        | Triangle / narrow pulse | Sharp attack, no reverb       |
| `render-edge-emphasis`          | Crisp, clicking, defined  | Square (short duty)     | Staccato, percussive          |
| `render-uniform-stroke`         | Clean, consistent, flat   | Pure square             | Even volume, mechanical       |
| `render-gradient-contour`       | Pitch-sliding, smooth     | Sine with glide         | Portamento, flowing           |
| `render-double-stroke`          | Layered, chorused         | Detuned sine pair       | Slight phasing, thick         |
| `render-depth-stroke-variation` | Depth-varied, filtered    | Sine + LP filter sweep  | Near=bright, far=muffled      |

### 3.2 Geometry Tags

| Visual Tag Category                 | Sound Direction            | Waveform Tendency                 | Character            |
| :---------------------------------- | :------------------------- | :-------------------------------- | :------------------- |
| `geometry-primitive-modularity`     | Simple, blocky, 8-bit-like | Square / pulse                    | Retro, minimal       |
| `geometry-regular-polygon-language` | Harmonic, bell-like        | Sine harmonics (3rd, 5th)         | Crystalline, pure    |
| `geometry-grid-alignment`           | Quantized, rhythmic        | Square with strict timing         | Metronomic, precise  |
| `geometry-radial-duplication`       | Echoed, circular           | Sine + short delay                | Spiraling, repeating |
| `geometry-concentric-structure`     | Resonant, layered          | Multiple sine (octaves)           | Deep, nested         |
| `geometry-scale-hierarchy`          | Wide frequency range       | Mixed (bass sine + treble square) | Contrasting scales   |

### 3.3 Motion/Effect Tags

| Visual Tag Category             | Sound Direction     | Waveform Tendency        | Character             |
| :------------------------------ | :------------------ | :----------------------- | :-------------------- |
| `motionviz-impact-ripple`       | Expanding, decaying | Noise burst → sine tail  | Boom + ring           |
| `motionviz-afterimage-trail`    | Trailing, delayed   | Sine + feedback delay    | Echo, ghostly         |
| `motionviz-elastic-deformation` | Bouncy, pitch-bent  | Sine with pitch envelope | Cartoon-like, springy |
| `motionviz-velocity-hue-shift`  | Pitch tracks speed  | Sine (dynamic frequency) | Doppler-like          |
| `motionviz-energy-glow-build`   | Rising, tensioning  | Sine sweep upward        | Building pressure     |
| `motionviz-trajectory-trace`    | Continuous, flowing | Sine with slow LFO       | Smooth, directional   |

### 3.4 Background/Atmosphere Tags

| Visual Tag Category         | Sound Direction      | Waveform Tendency        | Character           |
| :-------------------------- | :------------------- | :----------------------- | :------------------ |
| `background-noise-field`    | Textured, ambient    | Filtered noise           | Static, atmospheric |
| `background-wave-field`     | Undulating, rhythmic | Sine with amplitude LFO  | Oceanic, breathing  |
| `background-particle-layer` | Sparse, granular     | Random short sine pings  | Scattered, delicate |
| `analog-micro-jitter`       | Unstable, gritty     | Noise-modulated sine     | Lo-fi, imperfect    |
| `analog-chromatic-offset`   | Detuned, split       | Detuned sine pair (wide) | Unsettling, glitchy |
| `analog-luminance-pulse`    | Pulsing, throbbing   | Sine with slow AM        | Heartbeat-like      |

### 3.5 Typography Tags

| Visual Tag Category          | Sound Direction             | Waveform Tendency         | Character               |
| :--------------------------- | :-------------------------- | :------------------------ | :---------------------- |
| `typography-objectification` | Typewriter-like, mechanical | Short noise + sine        | Click-clack, discrete   |
| `typography-kinetic-motion`  | Whooshing, sweeping         | Noise with bandpass sweep | Kinetic, motion         |
| `typography-numeric-focus`   | Counting, stepped           | Square with pitch steps   | Digital counter, arcade |

## 4. Sound Event Catalogue

Every mini-game should define sounds for the following events. Not all events apply to every game — select those relevant to the mechanics.

### 4.1 Core Events (Required)

| Event              | Purpose                | Typical Duration | Design Notes                                                      |
| :----------------- | :--------------------- | :--------------- | :---------------------------------------------------------------- |
| **Score gain**     | Positive reinforcement | 50–150ms         | Bright, upward pitch. Scale pitch/layers with point value.        |
| **Damage / death** | Failure signal         | 200–500ms        | Low, dissonant, or noisy. Must contrast sharply with score sound. |
| **Game over**      | Terminal state         | 300–800ms        | Descending pitch or fade-out. Finality.                           |

### 4.2 Enhancement Events (Recommended)

| Event                     | Purpose          | Typical Duration | Design Notes                                                 |
| :------------------------ | :--------------- | :--------------- | :----------------------------------------------------------- |
| **Near miss**             | Tension / reward | 50–100ms         | Subtle, quick. Pitched slightly lower than score sound.      |
| **Collision (non-fatal)** | Physics feedback | 30–100ms         | Short, percussive. Pitch/volume scales with impact velocity. |
| **State change**          | Mode transition  | 100–300ms        | Distinctly different timbre from other sounds.               |
| **Combo / multiplier**    | Escalation       | 50–150ms         | Same family as score but rising pitch with each step.        |
| **Charge complete**       | Action readiness | 100–200ms        | Bright ping after buildup.                                   |

### 4.3 Ambient Events (Optional)

| Event                | Purpose       | Typical Duration     | Design Notes                                           |
| :------------------- | :------------ | :------------------- | :----------------------------------------------------- |
| **Background drone** | Atmosphere    | Continuous / looping | Very low volume. Matches background visual style.      |
| **Difficulty shift** | Pacing signal | 200–400ms            | Subtle tonal shift. Player may not consciously notice. |

## 5. Procedural Audio in Godot 4.2+ — Implementation Guidance

All sounds are generated procedurally in GDScript. No pre-recorded `.wav`, `.ogg`, or `.mp3` assets are used.

This section focuses on design decisions. Template assets are the source of truth for implementation code.

- Waveform primitives and simple envelopes: `.agents/skills/creating-godot-procedural-audio/assets/audio_synth.gd`
- Test-driven implementation examples in this repository use `tmp/games/<slug>/main.gd` and `tmp/games/<slug>/tools/tests/run_tests.gd`; adapt paths to the project.

### 5.1 Runtime Architecture (Recommended)

Use a hybrid approach by default.

1. **One-shot SFX (score / danger / damage / state change)**  
   Use `procedural generate -> PCM cache -> AudioStreamWAV` as the default.
2. **Continuous controlled audio (engine / thrust / beam, etc.)**  
   First try `procedural generate -> PCM cache -> AudioStreamWAV(loop)`. If requirements can be met via `volume_db / pitch_scale`, use it as the default.  
   `AudioStreamGenerator` + `AudioStreamGeneratorPlayback` should be adopted only when real-time synthesis is indispensable.
3. Use `11025` or `22050` as baseline `mix_rate` (prioritize GDScript load).
4. For the same event, keep a fixed motif with small variation and avoid pure randomness.
5. **Prefer sample-capable paths**: Prefer streams playable as samples by `AudioStreamPlayer` (e.g., `AudioStreamWAV`) and avoid routine use of non-sample streams (mainly `AudioStreamGenerator`).

Implementation notes:

- Keep PCM cache in `PackedByteArray` (16-bit PCM), convert to `AudioStreamWAV`, and reuse.
- For continuous sound only, monitor `frames_available` / `get_skips()` and retry queues or adjust load when needed.
- In headless runs (`OS.has_feature("headless")`), skip `AudioStreamPlayer` creation/playback/buffer filling and return no-op handles so tests remain logic-only.

### 5.2 Event Semantics Lock (In-Game)

Lock the timbre mapping of `score / danger / damage / state change` within a single game.

- `score`: bright short tones with an upward or opening impression
- `danger`: mid-high noise or dissonant components signaling tension
- `damage`: low-end leaning + short noise transient
- `state change`: independent motif indicating semantic transition (typically 120-350ms)

### 5.3 Variation Budget (Recommended Ranges)

Apply randomization only within ranges that preserve recognizability.

- Pitch detune: `±2%-±6%`
- Duration variation: `0-20%` of baseline
- Envelope variation:
  - Attack ratio: `±0.03`
  - Release ratio: `±0.20`
- Duty variation (square/pulse): `±0.03-0.12`
- Noise mix variation: `±0.05-0.15`

### 5.4 Continuous Sound Control (Engine/Thrust/Beam)

Control continuous sound in the following three stages.

1. Target: derive target gain/target pitch from input, velocity, and danger level
2. Smoothing: smooth with `current += (target - current) * alpha`
3. Release: after input release, apply ~100-250ms of decay

Operational rules:

- If `AudioStreamWAV(loop)` + `volume_db / pitch_scale` satisfies requirements, make it the first choice
- Specify stop conditions and stop method (gain decay only or with `clear_buffer()`).
- Use a stable control API for continuous sounds: `start_<sound>()`, `update_<sound>(params)`, `release_<sound>()`, and `stop_<sound>()`. In headless mode, these calls should update internal state and return no-op handles without creating players or filling buffers.
- Avoid frequency-band conflicts between continuous and short sounds (prioritize score audibility)
- When adopting `AudioStreamGenerator`, explicitly document why WAV loop cannot substitute in `SOUND_DESIGN.md`.

### 5.5 Debug Checklist

- No sound:
  - One-shot SFX: Check PCM cache key resolution and `AudioStreamWAV.data` length
  - Continuous sound: verify `play()` -> `get_stream_playback()` -> `frames_available` order
  - Verify event-queue retry works for continuous sound
- Clipping/distortion:
  - Keep samples within `[-1.0, 1.0]`
  - Reduce noise mix ratio and simultaneous voice count
- Dropout:
  - Monitor `get_skips()` and adjust `mix_rate` / simultaneous voices / computation load

### 5.6 Performance Patterns

1. **High-frequency one-shots should default to cache**
   - Target: high-frequency, short one-shot SFX with small parameter variation
   - Recommendation: generate `procedural -> PCM cache -> AudioStreamWAV` at startup/load and select from pool at playback
   - Exception: allow runtime synthesis only when waveform itself must change significantly by immediate game state

2. **Separate local cooldown from global emission budget**
   - Per-event cooldown alone can cause a surge in simultaneous voices as event types increase
   - In addition to per-type control, combine `global cooldown` and `per-frame emission cap` to smooth peak load

3. **Use table-driven profiles in hot paths**
   - Store waveform/envelope/priority profiles in `const` tables and avoid per-call regeneration
   - Suppress hot-path `match`-based dictionary generation and excess temporary objects

4. **Continuous noise components need state-gating**
   - Do not keep noise components of continuous sound (engine/thrust/beam etc.) constant; gate by speed, danger level, and input state
   - Reduce constant noise feel in low-load states and preserve audibility of informational sounds (score/damage)

## 6. Procedure for Sound Design from Visual Tags

Design after the visual direction is complete.
If the visual direction uses custom or concept-derived tags that are not exact entries in §3, map them to the nearest material, geometry, motion, or atmosphere family and document the mapping before choosing waveforms.
Example: `render-luminous-glass` can map to `render-glow-outline` plus `geometry-regular-polygon-language` (resonant sine/triangle partials); `motionviz-reflection-bursts` can map to `motionviz-impact-ripple` plus `motionviz-afterimage-trail` (short noise transient into a ringing tail or echo tap).

1. **Tag Interpretation**: Read each visual tag's `description` and `keywords`. Identify the sonic qualities they imply (refer to §3 mapping table).
2. **Cross-Tag Audio Synthesis**: Find the shared audio character across all selected visual tags. Express it in one phrase (e.g., "resonant synthetic pulses," "gritty percussive clicks").
3. **Waveform Selection**: Choose 1–2 primary waveforms and modulation techniques that match the direction.
4. **Semantic Timbre Mapping**: Define a stable in-game mapping for `score / danger / damage / state change` (same meaning, same timbral family).
5. **Cross-Game Variation Plan**: Explicitly decide what will vary versus previous games:
   - waveform palette
   - pitch range
   - envelope profile
   - modulation method (FM/AM/noise mix/filter sweep)
   - rhythm/gap pattern
6. **Event Mapping**: For each game event (§4), design a specific sound using the chosen waveform family and envelope style.
7. **Dynamic Parameters**: Identify which sound parameters should respond to game state (combo, velocity, difficulty).
8. **Continuous-Sound Policy** (if used): Define trigger condition, stop condition, and acceptable release tail.
9. **Integration Check**: Verify audio–visual coherence and event coverage with the checklist in §8.

## 7. Output Format

Output in the following format to the project's sound design document, e.g. `tmp/games/<slug>/SOUND_DESIGN.md` in this repository.

```markdown
# Sound Design: <GAME_NAME>

**Visual Tags (Sound Source)**: #vtag1, #vtag2

## 1. Audio Concept

<Overall sonic direction in one phrase, derived from visual tags>

## 2. Waveform Palette

| Role            | Waveform | Parameters       | Usage |
| :-------------- | :------- | :--------------- | :---- |
| Primary tone    | ...      | freq, duty, etc. | ...   |
| Texture / noise | ...      | ...              | ...   |

## 3. Sound Event Specifications

| Event      | Waveform | Frequency | Duration | Envelope | Dynamic Parameter   |
| :--------- | :------- | :-------- | :------- | :------- | :------------------ |
| Score gain | ...      | ...       | ...      | ...      | pitch += combo \* N |
| Damage     | ...      | ...       | ...      | ...      | —                   |
| Game over  | ...      | ...       | ...      | ...      | —                   |
| ...        | ...      | ...       | ...      | ...      | ...                 |

## 4. Relationship with Visual Tags

<How each visual tag influenced the sound design decisions>

## 5. Semantic Lock & Cross-Game Variation

### 5.1 In-Game Semantic Lock

| Event Family | Timbre Family | Why it is recognizable |
| :----------- | :------------ | :--------------------- |
| Score        | ...           | ...                    |
| Danger       | ...           | ...                    |
| Damage       | ...           | ...                    |
| State change | ...           | ...                    |

### 5.2 Cross-Game Variation Plan

- What differs from prior generated games (waveform/pitch/envelope/modulation/rhythm):
- Why these choices fit current visual tags and mechanics:
```

## 8. Sound Design Quality Checklist

The §2 evaluations cover event clarity, audio–visual coherence, restraint, dynamic response, and semantic-lock-vs-cross-game-variation. After running those, check the additional design-execution items below:

- [ ] Variation is kept within a defined budget (pitch / duration / envelope / duty / noise) so event identity remains clear (see §5.3).
- [ ] Motif-first variation is used (2–3 fixed variants + micro-variation), not pure random.
- [ ] Continuous sounds stop within the intended release time after input / state ends (see §5.4).
