# Hardware Profile Selection

Use a profile to constrain composition and synthesis before authoring game-specific material.
Treat these as capability families, not claims that all historical boards in a family behaved
identically.

## Fidelity levels

### Era-inspired

Use a compact, fixed capability model that evokes the period without naming an exact board.
Document the voice limit and primitives. This is the default when the user names only an era
or aesthetic.

### Hardware-faithful

Use the target's verified channel count, waveform/noise behavior, pitch/timer limitations,
envelopes, and update cadence. Prefer primary technical documentation when exactness matters.
Do not silently substitute familiar console assumptions for an arcade board or another chip.
Record the named target separately from the `hardware-faithful` fidelity value.

## Capability families

| Family | Starting capability contract | Good BGM modes | Main risk |
|---|---|---|---|
| Discrete/early logic | 1-3 tone or noise voices, hard gates, minimal envelopes | none, event-music, tiny fixed loop | over-composing beyond the board character |
| Simple PSG | 3 tone voices plus constrained/shared noise | fixed-loop, seeded-loop, event-music | treating noise and tone as unlimited independent channels |
| Pulse/bass/noise console | 2 pulse-like voices, 1 restricted bass voice, 1 noise voice | fixed-loop, seeded-loop, layered-adaptive | hiding channel steals and release collisions |
| Small wavetable/custom | a few short-wave voices, optional noise, limited modulation | fixed-loop, seeded-loop, layered-adaptive | using modern pads/effects that erase the small-table character |
| Generic four-voice inspired | 2 bright tone voices, 1 bass voice, 1 noise voice | any bounded mode | incorrectly describing the result as exact emulation |

## Contract fields

Record at least:

```text
profile id
fidelity level
voice limit
primitive names
noise ownership
per-voice pitch/timbre restrictions
parameter update granularity
master chain and clamps
BGM/SE sharing policy
```

## Master-chain baseline

Fix the master chain per profile before authoring sounds. Record conservative gain/headroom,
all nonlinear stages, output clamps, and any filtering or spatial processing. Use DC blocking
when the synthesis path can create offset. Prefer mono-first output unless the profile or target
runtime declares a spatial behavior; do not add automatic stereo widening merely to make a
small voice set sound larger.

Treat these as safety and identity constraints, not a universal effect recipe. A nonlinear
mixer curve, output-coupling high-pass, limiter, compressor, or other stage belongs only when
the selected capability model justifies it. Hardware-faithful profiles must not silently add
modern mastering that changes the named target's behavior.

When BGM and SE share voices, specify whether the runtime steals, ducks, pauses, shortens, or
drops material. Do not assume parallel playback is free.

## Arbitration baseline

Use this default priority order, then adjust for the game:

1. player-control feedback;
2. immediate danger warning;
3. causal consequence such as hit, block, or capture;
4. rare reward/cabinet state;
5. ambient event;
6. BGM ornament;
7. sustained BGM support voice.

Prefer shortening or dropping the lowest-priority new event over leaving an unmatched note or
exceeding the physical voice limit.

### A voice limit has a time resolution, not just a count

Two note-starts that land on the same voice within one scheduler tick — a frame, an audio
callback block, a sequencer step — are not two sounds. A monophonic voice retriggered
microseconds after it started produces a click, a truncated note, or nothing; it does not
produce both events. Decide this before authoring, because it is invisible in program data
and audible immediately.

Allocate voices in priority order within the tick, then apply one declared policy to the
requests that lose:

| Policy | Behavior | Use when |
|---|---|---|
| `drop` | later request is discarded | default; the honest reading of a small board |
| `coalesce` | merge into one note, louder/longer/detuned | the events are the same kind and their count is information |
| `redistribute` | move to a free sibling voice of the same family | the profile has one to spare and a small timbre shift is acceptable |
| `defer` | schedule onto following ticks | a cluster should read as a fast arpeggio or flam — bound the deferral, or a burst becomes a melody |

Never resolve a same-tick collision by stealing: a steal implemented as a fast fade on a note
that has not sounded yet removes it without replacing it.

State the policy in the contract alongside the voice limit, and record its interaction with
per-frame repeat caps. **A repeat cap of N on one event does not mean N audible sounds.** The
cap bounds queue growth and bookkeeping; the voice policy decides how many are heard. Choosing
`drop` with a cap above one is coherent — the surplus becomes measurable evidence that
arbitration ran — but only if the two numbers are documented as answering different questions.

## BGM mode decision

- Choose `none` when event rhythm already carries play, silence aids concentration, or the
  capability budget cannot support music without masking feedback.
- Choose `fixed-loop` for a strong, stable cabinet identity and short sessions.
- Choose `seeded-loop` when each run/stage may vary while exact replay remains useful.
- Choose `layered-adaptive` only when the runtime can arbitrate layers predictably.
- Choose `event-music` when repeated gameplay events themselves can create pulse and form.

Do not use runtime generation merely because it is available. Prefer the least dynamic mode
that expresses the game's pacing.
