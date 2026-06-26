# Reference Implementation: One Way To Build The Event Boundary

This documents *one concrete realization* of the event-boundary architecture the skill
assumes. It is an example to learn the design decisions from, not a required structure.
The ideas below are the transferable part. Read this only when you need to build (or
evaluate) the runtime that plays the kits, not when authoring a kit.

## The Four Layers

```
game code ──emit("laser")──▶ Bus ──resolve──▶ Adapter ──play(program)──▶ Synth ──▶ output
                              │                  ▲
                              │ loadKit(kit)     │ (swappable: real synth / silent mock)
                              ▼                  │
                        active game kit ─────────┘
```

1. **Bus** — the only public entry point. Owns event-name -> program resolution, runtime
   gating, and per-frame guards. Game code talks only to this.
2. **Adapter** — a narrow interface (`init`, `play(program)`, `configureMaster`,
   `setMasterVolume`, `setIntensity`, `stopAll`). Lets you swap the real synth for a
   silent mock without the rest of the code knowing.
3. **Synth** — a *pure player*. It plays a fully-resolved program and owns **no named
   preset library**. All named sounds live in the game kit, never in the synth.
4. **Kit** — the active game's data: aliases + programs (+ a clamped master tone).

The load-bearing decision: **the synth owns no presets; the kit owns the programs.**
That single rule is what makes games swappable, keeps the synth small, and lets a kit be
validated and tested in isolation.

## Key Design Decisions (the transferable core)

### Programs are data, not code

A program is a declarative list of steps (timing, oscillator/noise/filter, envelope,
distortion, bit-crush), each value optionally `{ base, intensity, random }`. Because a
program is data:

- It can be **measured** (compute duration/step-count → budget validation).
- It can be **derived** (a `tweak` helper scales pitch/time/drive of an existing program
  to make a sibling variant without re-authoring steps).
- It can be **replayed headlessly** (a mock just records the program id).

If you take one idea from this file, take this one: author sounds as data.

### Era anchor = fixed master chain + clamped settings

The synth runs every program through one fixed signal chain (input → drive → band-pass →
saturator → clipper → compressor → output). A kit may shift the cabinet tone only through
a small `master` struct, and each field is **clamped to era-appropriate bounds**. A kit
therefore cannot dial in a modern master tone no matter how its programs are built. Put
the era character in the shared chain, not in per-sound discipline.

### The Bus enforces runtime guards, not the game

- **Per-frame repeat cap.** The same event is allowed at most N times (e.g. 3) per frame,
  so a burst of collisions in one tick cannot machine-gun-stack one SE into noise.
- **Mute and demo gating.** `emit(name, { demo })` is dropped when muted, or when it is a
  demo sound and demo sounds are off. Attract-mode audio passes `{ demo: true }`.
- **Frame event log.** The Bus records which program ids fired this frame — useful for a
  sound-test view and for assertions.

Keeping these in the Bus means every game gets them for free and none can forget them.

### A mock adapter makes audio testable

A silent adapter that implements the same interface and just records played program ids
lets headless tests assert *what would have played* (and what master settings were applied)
without an audio context. The real adapter falls back to this mock before its synth is
initialized, so code paths stay identical.

### Validation is data-driven and lives in tests

Because programs are data, a `validateKit` function checks, per program: id matches its
registry key, step count within budget, and computed duration within the SFX/jingle cap.
Wire it into the test suite over the active kit so a sound cannot silently grow into music.

### Intensity as a global modulation axis

Each `{ base, intensity }` value adds an `intensity`-scaled delta at play time, and the
synth exposes a runtime intensity knob (which also moves the master drive/filter). This
lets escalating difficulty also brighten/harden the whole cabinet's timbre from one knob,
instead of authoring separate "calm" and "intense" programs.

## What To Leave Out Of A Port

The specific DSP internals (exact filter topology, the LFSR/metallic noise generators, the
chiptune scale table, the distortion/bit-crush curve math) are realization details. Reuse
the *architecture* (layers, program-as-data, fixed clamped master, bus guards, mock-adapter
testing, data-driven validation); re-derive the DSP for the target platform and taste.
