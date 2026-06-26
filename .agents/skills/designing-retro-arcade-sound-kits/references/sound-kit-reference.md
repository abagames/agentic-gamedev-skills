# Arcade Sound Kit Reference

## SE vs Jingle Decision Table

| Moment type | Examples | Sound choice |
| :--- | :--- | :--- |
| Player action | shot, dash, jump, place trail, rotate, clean, confirm | SE (one-shot) |
| Consequence | hit, block, collect, miss, damage, split, capture | SE (one-shot) |
| Warning | low timer, nearby threat, invalid move, overheating | SE (one-shot) |
| Ambient affecting play | spawn, wave step, object state change | SE (one-shot) |
| Cabinet/state phrase | start/ready, bonus/major reward, wave clear, danger phase, game over | Jingle |
| Cosmetic transition | UI focus move, minor blink, idle tick | usually none |

Rule of thumb: if it happens many times per run and feeds back a single action, it is an SE. If it happens rarely and marks a state the player should *register as a moment*, it is a jingle. Everything else gets no sound.

## Starting Loudness Ranges

Tune relative to sibling events; these are only starting points for one-shot programs:

- Foreground actions (shots, hits, warps, pings): peak `base` 0.5-0.6, `intensity` 0.4-0.45.
- Coin/credit-style chimes: `base` 0.4-0.5, `intensity` 0.3-0.4.
- Short pulse sounds (thrust): `base` 0.35-0.45, `intensity` 0.3-0.35.
- Noisy hit/thrust layers: noise level `base` 0.25-0.3, `intensity` 0.2-0.25.

Cabinet events (coin, start, game over) should sit slightly behind foreground play. Compare every new SE against the others in the same kit in a sound-test view rather than judging it alone.

## Budget Caps (starting values)

- SFX program length: <= ~0.6s
- Jingle length: <= ~1.6s
- Steps per program: <= ~24
- Program id should match its registry key (catches copy-paste drift).

Enforce these in an automated test against the active kit so a sound cannot silently grow into background music.

## Minimum Cabinet Kit

For the basic cabinet cycle to have sound at all, a kit should define at least a credit/coin sound and a start jingle:

```
programs:
  credit:        <short chime>          # played when the shell emits "coin"
  jingle:start:  <short rising phrase>  # played when the shell emits "start"
```

Without these, the cabinet still runs but coin insertion and game start are silent.

## Generalized Worked Example (pseudocode)

The exact API names below are illustrative — map them to the host project's authoring helpers.

```
// sound target — window:clean: bright 1-frame electric click
kit = {
  aliases: { "window:clean": "clean" },        // game vocabulary -> local program
  programs: {
    clean: program("clean", [
      { offset: 0, duration: 0.04,
        oscillator: { type: "square", freq: 920, endFreq: 1280 },
        filter: { type: "bandpass", freq: 2400, q: 8 },
        envelope: { peak: 0.12, hold: 0.004 },
        distortion: 6, bitCrush: 6 }
    ]),
    "jingle:bonus": jingle("jingle:bonus", [4, 7, 11, 14], { gain: 0.95 })
  },
  master: { /* clamped, era-appropriate drive / filter / intensity */ }
}

// game code, never touching the synth:
audio.emit("window:clean")
audio.emit("invader", { demo: true })   // attract sound, suppressible
```

Two authoring modes are typical: author a fully custom program from raw steps, or build a jingle from scale-degree indices. Derive a near-duplicate via a tweak helper from one of *your own* programs when a game needs two similar sounds — never from another game's program.

## Anti-Patterns

- Calling the synth directly from game logic (breaks the event boundary and the per-game kit swap).
- Giving every state transition a sound (masks the SEs that matter).
- Tuning one SE in isolation (it ends up too loud or too quiet against its siblings).
- Long, melodic, or sampled audio (leaves the event-like, fixed-hardware register).
- Adding new synth primitives per game instead of recombining the fixed set (era character drifts).
