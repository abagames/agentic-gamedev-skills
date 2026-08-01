# Verification Gates

Run the cheapest deterministic gates first, then evaluate the live result.

## Static contract

- Validate IDs, aliases, classifications, budgets, and numeric ranges.
- Confirm every audible gameplay event is wired and every intentional `none` is explicit.
- Confirm an empty audible registry is declared `audioMode: silent`, not accidentally omitted.
- Review unreachable program/cue warnings; retain an orphan only when sound-test, debug, or
  future-variant ownership is explicit.
- Confirm the primitive set and master controls remain within the hardware profile.
- Confirm no direct synth calls leaked into gameplay code.

Use `scripts/validate-audio-kit.mjs` for the generic manifest or port its invariants into the
host project's tests.

The generic validator proves only manifest-local constraints. It cannot prove coverage against
events omitted from the manifest or runtime BGM/SE arbitration across arbitrary event orderings.
Compare the manifest with a game-owned event inventory or mock emission log, and test shared
voices with project-native scenarios.

## Headless behavior

With a mock adapter, assert:

- each gameplay action emits the expected abstract event;
- alias resolution selects the expected program/cue;
- mute and demo-sound gates suppress output;
- the per-frame repeat cap works;
- priority/arbitration drops or shortens the intended lower-priority voice;
- no voice starts more than one note in a single scheduler tick, and total starts per tick
  stay within the voice limit, under the densest event burst the game can produce;
- the declared same-tick policy is what actually happened — dropped, coalesced,
  redistributed or deferred — rather than a silent retrigger;
- BGM plus worst-case SE/jingle collisions stay within the effective shared voice limit;
- fixed options and seed reproduce exactly.

## Timeline and BGM

- Assert note/program intervals have positive duration.
- Assert active voices never exceed the profile limit.
- Assert shared-noise collisions are resolved.
- Assert loop starts/releases pair and no tail exceeds the allowed boundary.
- Assert adaptive layer changes occur only at declared musical/game boundaries.

## Rendered-output measurement

Schema and timeline checks prove that program data is well formed. They cannot distinguish a
program that plays from one that is silent, clipped, or buried under the music. Whenever the
host can render faster than real time or capture its output — an offline render, a file
bounce, an engine capture node, a headless mixer, a hardware-accurate emulator — measure the
result and assert on it.

This is what an executor that cannot listen has instead of listening. It is not a
replacement: it catches what a listener notices in the first second, and nothing beyond that.

Measure at least peak level, RMS, onset time, and last audible sample, per program and per
cue. Then assert:

- **nothing is silent** — peak above an audibility floor;
- **nothing clips** — peak below the ceiling the master chain declares;
- **onset matches the declared start** — a program that begins late has a bug in its first
  step, not a taste problem;
- **the tail ends inside the declared bound** — program duration, or the loop boundary for a
  cue.

### Compare levels only within a co-occurrence group

Group events by what can actually sound at the same time: per state, per screen, per cue.
Require each event in a group to clear the continuous material of that group by a margin
recorded in the frozen contract.

Comparing every event against the loudest cue in the whole game is the common error, and it
fails in both directions — it rejects events that can never be heard against that cue, and it
passes events that are inaudible under the one they actually share a screen with.

Prefer asserting the **intended ordering** over absolute numbers: control feedback above the
bed it plays over, reward and danger above ordinary consequence, ambience below both, BGM
under all of it. Ordering survives a change to the master gain; absolute thresholds do not.
Where a margin is needed, record one per group and justify it, rather than inheriting a number
from another project.

### When rendering is not available

Some hosts cannot be captured, and some targets define levels in hardware the project does not
run. Say so in the completion report, then fall back to the weaker check the data still
supports: declared gains compared against each other and against the master chain, in the same
co-occurrence groups. Do not let the absence of a renderer turn into an absence of any level
reasoning at all.

## Runtime health

Load the real game in its target runtime. Exercise idle, normal input bursts, rapid repeated
actions, death/clear transitions, pause/resume, restart, and attract mode. Fail on console/audio
exceptions or an uninitialized-context path that loses events permanently.

## Experience evaluation

Audition at conservative volume during play, not only in a sound-test screen. Check:

- player actions remain readable during the densest BGM passage;
- hit, danger, reward, and cabinet sounds occupy distinct pitch/timbre/time regions;
- repetitive actions do not create painful machine-gun stacking;
- jingles remain rare phrases and do not become background music;
- BGM repetition supports rather than obscures the game's rhythm;
- silence is preserved where it increases tension or clarity;
- several seeds vary audibly while retaining the same game identity.

Document listening limitations when audio output cannot be auditioned. Do not replace listening
with waveform/schema checks, and do not replace deterministic checks with listening alone.

## Completion evidence

Record:

- hardware profile and fidelity claim;
- BGM mode and cue count;
- SE/jingle/event coverage counts;
- maximum measured program and cue durations;
- maximum measured concurrency, and maximum note-starts per voice per tick;
- measured peak/RMS per program and cue, the co-occurrence groups compared, and the margin
  used — or an explicit statement that the host could not be rendered or captured;
- determinism and loop results;
- runtime test command;
- listening context and unresolved risks.
