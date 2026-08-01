---
name: building-era-authentic-game-audio
description: "Designs, implements, and validates a complete game-specific procedural audio system inspired by late-1970s to mid-1980s arcade and console hardware, including BGM loops, adaptive cues, sound effects, jingles, event wiring, synthesis adapters, arbitration, and automated audio-contract tests. Use for tasks that include BGM or require an integrated BGM/SE subsystem across gameplay events. For an engine-agnostic SE/jingle-only kit, use designing-retro-arcade-sound-kits; for Godot-specific procedural SFX implementation without broader music/system design, use creating-godot-procedural-audio. Do not use for a modern sample-based soundtrack or exact chip emulation unless the user explicitly requests those goals."
---

# Build Era-Authentic Game Audio

Build a small audio subsystem for the game in front of you. Derive its musical and sonic
identity from gameplay, then implement it in the host engine with explicit hardware-like
constraints and machine-checkable contracts.

## Core rules

- Inspect the game before choosing sounds. Design from actions, consequences, hazards,
  pacing, rounds, and attract-mode behavior rather than from a preset catalogue.
- Treat silence and `no BGM` as valid results. Do not force continuous music onto a game
  whose rhythm is already carried by movement or event sounds.
- Keep game logic behind an event boundary: game code emits abstract names; an audio bus
  resolves them through the active game kit; an adapter plays resolved program data.
- Keep named programs in the per-game kit, never in the shared synth.
- Represent BGM cues, SEs, and jingles as deterministic data when the host permits it.
  Make duration, voice use, loop boundaries, and variation seeds measurable.
- Fix and clamp the primitive set and master chain before authoring the kit. Recombine the
  fixed set per game; do not add a new synth primitive merely to rescue one sound.
- Distinguish **era-inspired** from **hardware-faithful**. Claim hardware fidelity only when
  a named target and verified capability/timing constraints are in scope.
- Tune sibling sounds together under gameplay load. A good isolated sound can still make a
  bad kit.

## Workflow

### 1. Discover the host and gameplay

Read repository instructions, game rules, runtime entry points, event/state transitions,
existing audio code, tests, and build commands. Identify:

- engine and available audio APIs;
- whether an audio bus, synth, mixer, or asset pipeline already exists;
- player actions and consequences that require immediate feedback;
- rare cabinet/state moments that deserve a jingle;
- gameplay variables that could drive intensity or arrangement;
- attract/demo mode and its sound policy.

Preserve an existing sound architecture when it already provides the required boundary.
Repair or extend it instead of installing a parallel audio stack.

### 2. Freeze the audio contract

Read [hardware-profiles.md](references/hardware-profiles.md). Choose and record:

- fidelity level: `era-inspired` or `hardware-faithful`, plus a named target for the latter;
- primitive set and physical/logical voice limit, plus the policy for two note-starts landing
  on one voice in the same tick;
- BGM mode: `none`, `fixed-loop`, `seeded-loop`, `layered-adaptive`, or `event-music`;
- channel arbitration and ducking policy;
- deterministic seed ownership and replay behavior;
- duration, step-count, density, and loop-tail budgets.

Do not author sounds until this contract is stable. Change it later only when gameplay
evidence shows that the chosen capability model cannot express the required feedback.

### 3. Map gameplay moments

Classify every candidate moment as `sfx`, `jingle`, `bgm`, or `none`. Include expected
frequency, priority, concurrency, and demo behavior. Write a one-line target before coding,
for example:

```text
player:fire — dry narrow pulse, instant attack, readable at eight shots/second
enemy:split — two-step downward metallic tear, distinct from player damage
jingle:clear — compact rising phrase, celebratory but shorter than the ready cadence
```

Prefer shared cabinet vocabulary (`coin`, `start`, `warning`, `jingle:clear`) when it is
semantically correct. Use game-specific names when they make game code clearer.

### 4. Build or adapt the event boundary

Read [audio-contract.md](references/audio-contract.md) when implementing the runtime.
Maintain this dependency direction:

```text
game -> emit(event) -> bus -> kit/alias resolution -> adapter -> synth/output
```

Put mute/demo gating, per-frame repeat caps, priority, and event logging in the bus. Provide
a silent/mock adapter so headless tests can assert resolved program IDs without audio output.

### 5. Author BGM

Read [composition-workflow.md](references/composition-workflow.md) when the chosen BGM mode
is not `none`. Apply the generalized pipeline:

1. plan intent, form, tempo, loop length, and voice roles;
2. select or generate motifs/patterns;
3. realize roles onto constrained voices;
4. apply timbral techniques without breaking the voice budget;
5. finalize a deterministic timeline and loop diagnostics.

Prefer short recognizable cells, deliberate rests, and gameplay-responsive density over a
modern full arrangement. Keep variation structural enough to matter but bounded enough that
the cue retains identity.

### 6. Author SEs and jingles

Read [sound-effect-workflow.md](references/sound-effect-workflow.md). Design sibling sounds as
one kit, then author them from the fixed primitive set. Use short one-shots for repeated
feedback and short phrases for rare state changes. Starting caps:

- SFX duration: `<= 0.6s`;
- jingle duration: `<= 1.6s`;
- steps per program: `<= 24`.

Override these only in the frozen contract and add a test for the new budget. Keep cabinet
chimes slightly behind foreground play; never let a jingle mask control feedback.

### 7. Integrate and arbitrate

Wire abstract events at the gameplay source. Avoid synthesizer calls in entities, scenes,
or rules code. Define a collision policy before testing dense play:

1. preserve player-control feedback and danger warnings;
2. preserve consequences needed for causality;
3. duck or drop reward/ambient sounds;
4. reduce BGM ornaments before silencing essential SEs.

Resolve the collision policy per scheduler tick, not only per note: allocate voices in priority
order within the tick, and apply the declared same-tick policy to the requests that lose. Two
starts on one monophonic voice in one tick are one sound however the host mixes them, and a
per-frame repeat cap does not change that.

Expose the smallest meaningful control surface, usually zero to two continuous gameplay axes.
Clamp it and derive tempo, density, register, arrangement, timbre, or variation intent inside
the kit. Add another exposed axis only when it represents an independent gameplay variable;
never swap to an unrelated sound identity merely because a control crosses a threshold.

### 8. Validate before declaring completion

Read [verification.md](references/verification.md). Require all applicable gates:

- schema, alias, ID, duration, step-count, voice-limit, and event-coverage checks;
- deterministic replay for fixed options and seed;
- matched note starts/releases and bounded loop tails;
- mock-adapter assertions for emitted events, mute/demo gates, and repeat caps;
- rendered or captured output measured for silence, clipping, onset and tail, with levels
  compared inside each co-occurrence group rather than across the whole game;
- runtime smoke test in the real engine or browser;
- stress test at realistic maximum event density;
- multi-seed comparison for generated BGM/SE variation;
- low-volume audition of the complete sibling kit during actual play.

When the project can emit the generic manifest described in
[audio-contract.md](references/audio-contract.md) — derived from runtime kit data, never
hand-maintained beside it — run:

```bash
node <skill-dir>/scripts/validate-audio-kit.mjs <manifest.json>
```

A passing run prints the artifact it read and the counts it checked. **If it prints nothing,
it did not run**; fix the invocation before believing the exit code.

When maintaining or modifying the bundled validator, also run:

```bash
node <skill-dir>/scripts/validate-audio-kit.mjs --self-test
```

Otherwise port the same invariants into the project's native test suite. Do not require a
second manifest if it would become an unsynchronized duplicate of typed runtime data.

## Completion report

Report the implemented event boundary, hardware profile, BGM mode, event coverage, generated
program/cue counts, arbitration policy, validation commands, and remaining listening risks.
State explicitly when audio is era-inspired rather than an exact hardware emulation.

## Reference routing

- Read [hardware-profiles.md](references/hardware-profiles.md) whenever choosing constraints.
- Read [audio-contract.md](references/audio-contract.md) when building the bus, kit, adapter,
  mock, or validation manifest.
- Read [composition-workflow.md](references/composition-workflow.md) when implementing BGM.
- Read [sound-effect-workflow.md](references/sound-effect-workflow.md) when designing SEs or
  jingles as part of the integrated kit.
- Read [verification.md](references/verification.md) before final validation and handoff.
