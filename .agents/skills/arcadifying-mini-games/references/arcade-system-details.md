# Arcade System Design Details

Load only the sections for arcade layers being implemented or changed.

## Contents

- Round structure and pacing
- Score economy and extends
- Initials and ranking persistence
- Replay-driven attract mode
- Scripted autopilot
- Ceremony layout and validation traps

## Round structure and pacing

- Start with roughly 6–10 rounds per lap. Give each a personality through parameter mixes of existing enemies, speeds, ratios, spawn bias, rewards, and environment timers; do not require new content types.
- Use a non-monotonic tension curve with a deliberate abundant/easier breather after the hardest stretch.
- Prefer quotas based on countable in-world events such as deliveries, kills, units banked, or survival goals. Score points drift when multipliers change.
- Limit true rule changes such as gates or altered goals to roughly one or two per lap. More harms arcade legibility.
- Loop later laps by scaling the round table; about ×1.15 is a starting hypothesis, not a universal constant.
- Replacing continuous difficulty with rounds may remove time pressure. When slow play becomes free, add a time bonus tied to quota/par time, bottom it at zero rather than timing the player out, and verify that it cannot dominate the existing marginal scoring economy.

## Score economy and extends

- Place the first extend around 2–5 times a decent early-run score, then use a fixed interval. Estimate the early-run score from quota, typical score chunks, and bonuses over the first rounds, or measure it with an existing policy; do not guess without a model.
- Announce an extend through a dedicated jingle and visible feedback; cap displayed lives even if internal limits differ.
- Scale round-clear bonuses from existing economy signals such as round number, quota, time, or remaining lives. Avoid a bonus that eclipses skilled in-round scoring.

## Initials and ranking persistence

Use a three-character entry with a bounded timeout, typically around 15–30 seconds for human play. Keep the resulting ranking visible and preview the current run at its rank with placeholder initials without writing storage. Define how incomplete names are padded on END or timeout.

Two entry models:

| Model | Interaction | Trade-off |
|---|---|---|
| Cycle | Up/down changes a letter; left/right moves the caret | Compact and period-authentic, but deletion/completion must be made visible |
| Board | Cursor selects characters plus visible DEL and END cells | Uses more screen space but exposes every action |

Prefer the board when space permits. In either model, make completion visible rather than relying only on timeout knowledge.

Ship a factory-default top-five table whose bottom is reachable within one or two rounds and whose top represents a good run. Merge defaults at read time; never persist defaults alone. Write only a qualifying real score and break ties in the new entry's favor.

For non-qualifying scores:

- With input replay, keep the entry phase structurally deterministic and guard only the save when skipping the phase would desynchronize replay.
- With scripted autopilot, no replay sequence depends on the phase. It is valid to skip entry when recognition is reserved for table qualifiers.

Record which rule was selected and why.

## Replay-driven attract mode

Use engine replay only when it captures the controls required by the game.

- Guard persistence with the replay flag because game-over paths repeat during attract loops.
- Keep custom phases input-deterministic.
- Ensure game-over and title paths are safe to re-enter repeatedly.
- If the engine records unified pointer input but not per-key state, keyboard movement will not replay. Use a game-state-driven control policy under replay instead.
- Shorten or bypass human-length entry timeouts during replay without changing normal-play timing.

## Scripted autopilot

Expose a policy interface such as `setAutopilot(false | true | "naive")` that feeds the same named control record as keyboard/pointer input. Do not wire bot decisions directly into attract rendering or phase code.

The display policy should produce readable representative play. Add a separate deliberately mediocre/naive policy only when the project also needs fairness measurement; a polished demo policy is biased evidence for that question. If used, pair the naive policy with a death log containing cause and frames since the player's own action.

This second policy is optional for attract mode itself. Do not build it solely to complete arcade ceremony.

## Ceremony layout and validation traps

- Schedule game-over notes before any engine call that stops `update()`.
- Re-check phase after mid-frame transitions so spawners cannot run during clear/death.
- Use grace frames between confirm-driven screens to prevent one press from completing several phases. Start around 20 frames at 60 FPS, then shorten only if the screen remains readable and the triggering input cannot be reused.
- Size interactive cursors so their outermost position remains inside the playfield frame.
- Screenshot every changed ceremony state, including edge cursor positions when layout is tight.
- Test every promised binding family; arrow-only automation does not validate WASD synonyms.
- Guard replay persistence and run the complete attract/game-over loop twice to expose repeated side effects.
