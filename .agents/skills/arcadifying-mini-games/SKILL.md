---
name: arcadifying-mini-games
description: 'Converts a working mini-game into a complete arcade game by adding round structure, ceremony screens (READY / round clear / death / game over), a score economy (extends, round bonuses, initials entry, high-score table), and jingle/SE separation. Use when a playable game with a verified core loop still "feels like a minigame" and needs arcade completeness — rounds or waves, 1UP extends, name entry, attract mode. Not for designing the core mechanic itself (use designing-mini-games first).'
---

# Arcadifying Mini-Games

Add time structure, ceremony, score economy, recognition, and attract behavior around an existing real-time core loop. Implement only missing layers; do not redesign the core mechanic under this workflow.

## Entry gate

Confirm that a playable loop exists and is not known to be broken or unfun. Use existing runtime, play, or telemetry evidence when available. Missing prior evidence does not require a sweep of every game-verification skill; run only the smallest check needed before wrapping the loop, and report remaining uncertainty.

## Workflow

### 1. Inventory missing arcade layers

Check for rounds/waves, clear condition, READY/clear/death/game-over ceremony, extend economy, initials and persistent rankings, attract mode, progress HUD, and separated jingles/SEs. Preserve working layers and implement only the gaps.

### 2. Define round data before code

Create a data table rather than branching round logic. Use parameter mixes of existing pieces to create round personalities, include a deliberate breather after a hard stretch, and choose a clear quota in a stable in-world event rather than multiplier-inflated score. Read [arcade-system-details.md](references/arcade-system-details.md) before setting round counts, lap scaling, quotas, or time bonuses.

### 3. Install one phase machine

Use one `phase` variable as the source of truth:

```text
ready → play → clear → ready
             ↘ death → play
                       ↘ entry → table → game-over/title path
```

Preserve these invariants:

- Every update section and input handler checks the current phase.
- A transition re-checks phase before later same-frame spawners, collisions, or scoring run.
- Chained confirm-driven phases use a short grace period so one just-pressed edge cannot skip several screens.
- READY, clear, and death freezes stop input, spawning, collision, movement, timers, and cooldown mutation; drawing and ceremony scheduling may continue.
- Engine calls that stop the update loop happen only after custom entry/table phases and scheduled jingle work are complete.

### 4. Add a coherent score economy

Define extends, round-clear bonuses, name entry, top-five persistence, default rankings, tie behavior, and non-qualifying-score behavior as one system. Read [arcade-system-details.md](references/arcade-system-details.md) before implementation; it contains thresholds, entry UI models, merge-at-read persistence, and replay-dependent qualification rules.

### 5. Separate ceremony audio

Map round start, clear, extend, and game over to jingles; map momentary actions to one-shot SEs. When the engine has no jingle API, process a frame-indexed note queue while the update loop is still active. Use `designing-retro-arcade-sound-kits` only when the game needs a full event-kit design, not merely to satisfy this link.

### 6. Build attract mode

Prefer an existing deterministic replay facility when it records the controls the game needs. Otherwise drive the real game through a policy interface that emits the same control record as human input. Read [arcade-system-details.md](references/arcade-system-details.md) for replay guards, keyboard limitations, scripted autopilot, and the optional naive policy used for fairness measurement.

Attract mode must not write rankings, stall indefinitely in entry screens, or diverge because of mutable/non-deterministic phase decisions.

## Validation

Scope checks to the layers changed, but validate the integrated cycle when the full wrapper changed.

- Inject or arrange state to test quota → clear → next round, extend crossing, entry save/skip, ranking ties, and any rule-changing round.
- Capture each changed ceremony screen; value assertions do not catch clipped text, skipped screens, or off-frame cursors.
- Exercise each named UI action through at least two configured synonym keys when multiple bindings are promised.
- Run title → attract → play → game over → entry/table → title twice to catch re-entry and persistence defects.
- Run the project's runtime smoke check after wiring browser or engine entry flow.

Keep phase, round number, and computed round parameters reachable through the project's existing debug/test boundary. Do not expose production internals more broadly than validation requires.

## Output

Produce a round parameter table, phase machine, score/extend/entry/ranking wiring, attract implementation, jingle map, and evidence for the applicable transition, persistence, screen, and runtime checks.

## Reference routing

- [arcade-system-details.md](references/arcade-system-details.md) — load the relevant section before implementing rounds, score economy, name entry, persistence, or attract mode.
- `probing-web-game-mechanics` — use for browser state injection only when changed mechanics are otherwise slow or unreliable to reach.
- `smoke-testing-web-games` — use after a browser-runtime change, not for documentation or design-only work.
