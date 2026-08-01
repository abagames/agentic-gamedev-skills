# Audio Event and Kit Contract

Use this contract when a project lacks an equivalent typed boundary. Adapt names and syntax to
the host engine; preserve dependency direction and invariants.

## Contents

- Runtime layers
- Suggested interfaces
- Generic validation manifest
- Required invariants

## Runtime layers

```text
game code -> AudioBus.emit(name, options)
          -> active kit resolves alias/program/cue
          -> adapter plays resolved data
          -> synth/output
```

- **Bus:** own mute, demo gating, priority, repeat caps, active-kit selection, and logging.
- **Kit:** own aliases, program/cue data, budgets, and clamped master settings.
- **Adapter:** expose a narrow engine-facing player interface.
- **Synth/player:** play resolved data; own no game-named preset library.
- **Mock adapter:** record resolved IDs and parameters without producing sound.

## Suggested interfaces

```ts
type AudioEmitOptions = {
  demo?: boolean;
  intent?: number | readonly [number, number];
  seed?: number;
};

interface GameAudioBus {
  emit(name: string, options?: AudioEmitOptions): void;
  setMuted(muted: boolean): void;
  setDemoSoundEnabled(enabled: boolean): void;
  setIntent(value: number | readonly [number, number]): void;
  beginFrame(frameId: number): void;
  stopAll(): void;
}

interface AudioAdapter<Program, Cue> {
  init(): Promise<void> | void;
  configureMaster(master: unknown): void;
  playProgram(program: Program, options?: AudioEmitOptions): void;
  playCue(cue: Cue, options?: AudioEmitOptions): void;
  stopAll(): void;
}
```

Use engine-native equivalents where appropriate. Keep gameplay code dependent only on the bus
or a still narrower event emitter.

## Generic validation manifest

The bundled validator accepts JSON with this shape:

```json
{
  "version": 1,
  "audioMode": "active",
  "hardwareProfile": {
    "id": "generic-four-voice",
    "fidelity": "era-inspired",
    "voiceLimit": 4,
    "primitives": ["pulse", "bass", "noise"]
  },
  "budgets": {
    "sfxMaxDurationSeconds": 0.6,
    "jingleMaxDurationSeconds": 1.6,
    "maxStepsPerProgram": 24,
    "bgmLoopMaxDurationSeconds": 32,
    "bgmLoopMaxTailSeconds": 0
  },
  "programs": {
    "fire": {
      "id": "fire",
      "kind": "sfx",
      "steps": [
        { "offset": 0, "duration": 0.08, "voice": "pulse1" }
      ]
    },
    "jingle:start": {
      "id": "jingle:start",
      "kind": "jingle",
      "steps": [
        { "offset": 0, "duration": 0.1, "voice": "pulse1" },
        { "offset": 0.1, "duration": 0.16, "voice": "pulse1" }
      ]
    }
  },
  "aliases": {
    "player:fire": "fire",
    "start": "jingle:start",
    "stage": { "kind": "cue", "id": "main" }
  },
  "events": [
    { "name": "player:fire", "classification": "sfx", "priority": 100 },
    { "name": "start", "classification": "jingle", "priority": 60 },
    { "name": "stage", "classification": "bgm", "priority": 20 },
    { "name": "ui:focus", "classification": "none", "priority": 0 }
  ],
  "bgmCues": {
    "main": {
      "id": "main",
      "durationSeconds": 8,
      "loopStartSeconds": 0,
      "loopEndSeconds": 8,
      "steps": [
        { "offset": 0, "duration": 0.25, "voice": "pulse1" }
      ]
    }
  }
}
```

Program and cue steps describe occupied intervals for validation. Runtime program data may
contain additional oscillator, pitch, envelope, and filter fields; the validator ignores them.
String aliases are a compatibility shorthand for `{ "kind": "program", "id": "..." }`.
Use a typed alias for BGM cues and whenever the target kind should be explicit.

Set `audioMode` to `active` for an audible kit. Set it to `silent` only when the game is
intentionally silent; a silent manifest contains no programs, cues, or aliases, though it may
list explicit `none` events. For `hardware-faithful`, also set a non-empty
`hardwareProfile.targetHardware` naming the verified target. Every event carries a numeric
`priority`, including a `none` event: a declared silence has priority zero because it never
asks for a voice.

### Producing the manifest

Two shapes are acceptable, and one is not:

- **Derive it from the runtime.** Emit the manifest from the kit's own data through a debug
  hook, a build step, or a CLI export, so it is a projection of what actually plays. Prefer
  this whenever the host can be asked.
- **Validate the source directly.** Port these invariants into the project's own test suite
  and assert them against the typed kit data. Prefer this when the host cannot export.
- **Do not hand-maintain a parallel manifest.** A second copy of the kit, edited by hand, is
  wrong the first time someone changes a program: it passes the validator while the game plays
  something else.

Whichever validating command you run, require it to **report what it checked** — counts of
programs, cues, and events, and the profile it read. A validator that prints nothing on
success cannot be distinguished from one that never ran, and "no output, exit 0" is the shape
almost every silent failure takes: a mistyped path, an entry-point guard that did not fire, an
empty or partially written file. Treat an empty success as a failed gate until you have seen
it name the artifact it validated.

## Required invariants

- Keep event names unique.
- Resolve every `sfx`, `jingle`, and `bgm` event to existing data through its name or alias.
- Keep `none` events unmapped.
- Require an active kit to contain at least one audible event; permit an empty audible registry
  only through explicit `audioMode: silent`.
- Match each registry key to its internal `id`.
- Keep all offsets finite and non-negative and all durations finite and positive.
- Treat steps as occupied intervals: do not overlap intervals on one physical voice. Represent
  non-occupying automation separately in host data.
- Start at most one note per voice per scheduler tick at runtime, and never exceed the voice
  limit within a tick. Declare which policy resolves the losers — drop, coalesce, redistribute,
  or defer — and make the choice observable in the emission log, so a test can tell a dropped
  request from one that never arrived.
- Keep program duration, cue loop duration, loop-tail duration, step count, and simultaneous
  voices within the frozen budgets.
- Clamp exposed intent controls and master parameters at the bus/adapter boundary.
- Make a fixed seed and fixed options reproduce the same resolved timeline.
- Mark attract-mode emissions with `demo: true` and test suppression.

If the host already has typed data that can enforce these invariants directly, validate that
source rather than maintaining this manifest as duplicate production data.
