# BGM Composition Workflow

Use this only after selecting a BGM mode other than `none`.

## Phase 1: Intent and structure

Define:

- gameplay role: pulse, tension, spatial identity, reward, or pacing;
- tempo or event clock relationship;
- loop length and maximum acceptable repetition interval;
- tonal center or pitch collection, if tonal music is appropriate;
- sections or layers and the gameplay conditions that select them;
- voice roles and the physical voice budget;
- variation seed ownership.

Choose the smallest gameplay-facing intent surface that preserves meaningful control. Zero
continuous axes is valid for a fixed cue; one axis often represents escalation; two axes may
separate independent concerns such as danger and success or urgency and density. Derive mood,
tempo, register, arrangement, and technique probabilities internally. Expose more axes only
when the game supplies independently meaningful variables and tests can cover their interaction.

Keep form proportional to a play unit. A short round usually needs a compact loop, not a
multi-minute song form.

## Phase 2: Motifs and patterns

Select a small, tagged vocabulary for rhythm, pitch contour, bass motion, percussion, and
transitions. Require each motif to declare its duration and compatibility constraints.

- Include deliberate rests or held space.
- Link real variants instead of duplicating near-identical motifs.
- Preserve a recognizable hook across variations.
- Keep cadence/loop-safe variants for boundaries.
- Avoid an idle pattern that makes waiting musically or mechanically optimal.

Use deterministic weighted selection when generation occurs at load/runtime. Record selected
IDs for replay and diagnosis.

## Phase 3: Event realization

Map musical roles to physical/logical voices under the chosen hardware profile.

- Resolve collisions by priority; never silently exceed the voice limit.
- Keep noise monophonic when the profile shares one noise generator.
- Treat bass-only or restricted voices according to their declared pitch/timbre limits.
- Quantize timing to the target update granularity when fidelity requires it.
- Keep BGM and SE arbitration visible in diagnostics.

## Phase 4: Timbral techniques

Apply only techniques supported by the fixed primitive set: duty/timbre changes, pitch slides,
hardware-like sweeps, arpeggiation, short echo simulation, noise-mode changes, or bounded gain
motion. Gate techniques by style/section and keep them from becoming constant modulation.

Do not solve weak motifs with unlimited effects. Repair motif, register, rhythm, or arrangement
first.

## Phase 5: Timeline and loop

Finalize sorted events and compute:

- matched starts/releases;
- active voices over time;
- maximum concurrency;
- loop head/tail event windows;
- release or automation overhang;
- allowed loop-tail duration from the frozen contract;
- selected motif and arrangement IDs;
- replay options and seed.

Prefer a seamless boundary over a generic fade-out. Use a fade only when the cue is intentionally
one-shot or the game transition calls for it.

## Variation checks

Across representative seeds or runs, compare:

- event/timeline hashes;
- motif and arrangement spread;
- density and register;
- transition coverage;
- fallback frequency;
- loop and voice-budget violations.

Reject meaningless randomization that changes numbers without changing audible structure, and
reject uncontrolled variation that destroys cue identity.
