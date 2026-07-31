---
name: arcadifying-mini-games
description: 'Converts a working mini-game into a complete arcade game by adding round structure, ceremony screens (READY / round clear / death / game over), a score economy (extends, round bonuses, initials entry, high-score table), and jingle/SE separation. Use when a playable game with a verified core loop still "feels like a minigame" and needs arcade completeness — rounds or waves, 1UP extends, name entry, attract mode. Not for designing the core mechanic itself (use designing-mini-games first).'
---

# Arcadifying Mini-Games

**Status: Validated (2 reuses)** — extracted from TAIL CONVOY; validated on BUBBLE BROKER (2026-07-10): the phase-machine rules pre-empted three bug classes and the screenshot requirement caught a real visual bug that value assertions passed. Caveat: the validating executor had incidental prior exposure to source-project code fragments, so it was not a fully blind reuse. Second reuse on CHAIN DRIFT (2026-07-31): the persistence rules (factory table, merge-at-read, never write defaults back, new-entry-wins ties) were adopted verbatim and produced no bugs; the project diverged deliberately on the always-run entry phase and covered the declared attract-mode gap itself — both now folded back in below.

## Purpose

The gap between a mini-game and a finished arcade game is rarely mechanics — it is **time structure and ceremony**: discrete rounds with personalities, ritual screens, an economy of extra lives, and persistent recognition (initials, score table). This skill adds that layer around an existing, already-fun core loop.

## When to Use

- A playable game exists, its core loop is verified (runs clean, idle/mash-proof, balance checked), and the goal is "make it a complete arcade game". Confirm that from evidence that already exists — prior test runs, telemetry, play reports. Absent evidence is not a trigger to sweep smoke, mechanics probes, and balance evaluation before starting: run only the smallest check the arcadification itself depends on, or record the gap as a stated uncertainty.
- The current difficulty is a monotonic drift and needs round-based pacing.

## When Not to Use

- The core loop is known to be unfun or known to be broken — fix that first (`designing-mini-games`, `evaluating-gameplay-balance`).
- Turn-based/puzzle games: round ceremony assumes real-time waves.

## Procedure

### 1. Diagnose what is missing

Check against the completeness list: discrete rounds / clear condition / ready-clear-death ceremony / extend economy / initials + persistent score table / attract mode / round-and-progress HUD. Implement only the missing ones.

### 2. Design the round table (before touching code)

- 6–10 rounds per lap, each a **personality profile made only of parameter mixes** of existing pieces (enemy count/speed/ratio, spawn bias, reward abundance, environment timers) — no new content types. Numeric profiles produce qualitatively different rounds (swarm / hunter / raid / harvest).
- **Non-monotonic tension curve**: place a deliberate breather (abundant, easier) round after the hardest stretch.
- Clear condition = a quota in the game's existing currency (deliveries, kills, survival). When the game has both score points and a countable in-world event (units banked, deliveries made), quota the *event count*, not points — points inflate with multipliers and make quotas drift. Loop laps with a multiplier on all values (×1.15 per lap is a workable start).
- Rule *changes* (not just numbers — gates, altered goals) at most 1–2 per lap; more breaks arcade legibility.
- Replacing a time-based difficulty drift with round pacing also removes intra-round time pressure — check that slow play still has a cost. The standard patch is a round-clear time bonus (par time scaled by the quota; overtime bottoms out at 0, no timeout miss), and verify arithmetically that the speed reward cannot beat the existing scoring economy's marginal gains.

### 3. Implement a phase state machine

Phases: `ready` → `play` → (`clear` → `ready`) / (`death` → `play` or game-over path → `entry` → `table` → engine game over). Rules that prevent the observed bug classes:

- One `phase` variable is the single source of truth; every update section and every input handler checks it.
- **Same-frame bleed**: a press that ends one phase is still "just pressed" for later code in the same frame. Guard chained phases with grace frames (~20) before they accept the same confirm input.
- **Mid-frame transitions**: code later in the same frame's update (spawners especially) must re-check `phase`, or enemies spawn during the clear ceremony.
- Freeze semantics per phase: `ready`/`clear`/`death` are draw-only — skip input, spawning, collisions, AND all entity state mutation (movement, timers, cooldowns). A "frozen" field that still moves or re-arms breaks the ceremony contract.

### 4. Score economy

- Extend (1UP): first threshold ≈ 2–5× a decent first-run score, then a fixed interval (e.g. 5,000 then every 20,000). Estimate "a decent first-run score" from the round economy (quota × typical scoring chunk + clear bonuses over the first 2–3 rounds), or measure it with an autopilot/bot run — do not guess blind. Announce with a dedicated jingle + blinking text; cap displayed lives.
- Round-clear bonus scaled by round number and remaining lives, tallied on the clear screen.
- Initials entry (3 chars, ~15–30 s timeout) and a persisted top-5 table. When the engine owns the game-over screen and stops the update loop there (crisp-game-lib's `end()` does), run entry/table as phases *before* that call; engines where you draw the game-over screen yourself have no such ordering constraint.

  Two input models, and the choice is not cosmetic:

  | Model | Interaction | Trade |
  |---|---|---|
  | **Cycle** | Up/Down changes the letter under the caret, Left/Right moves the caret | Compact, ~4 lines of code, authentically period — but **deletion and completion are invisible**; the player learns "how do I finish?" only by waiting out the timeout |
  | **Board** | A character grid with `DEL` and `END` as selectable cells; arrows move a cursor, confirm picks | Needs most of a screen — but every available action is visibly on it |

  Prefer **board** when the screen has room. It puts "how do I finish" in front of the player instead of relying on a timeout, which is the same defect class as any other rule that is correct and undrawn.

  Two patterns worth copying regardless of model: **keep the ranking visible during entry**, and **preview the current run at its resulting rank using padded placeholder initials** (`---` before input) **without writing storage** — together they answer "why am I typing?" on the screen itself. Define the padding rule for incomplete names (right-pad with a filler character on `END` or timeout) so a walked-away player still produces a well-formed row.
- Ship a factory-default score table (5th place reachable within a round or two, 1st ≈ a good single run, below the first extend) — an empty table makes the first game rank #1 for free and gives new players no target. Merge defaults at read time and never persist them on their own; only a qualifying real score writes storage. Break ties in the new entry's favor.

- **Non-qualifying scores** — keep the entry phase always-run (skip only the save) **when attract mode uses the engine's input replay**, so replays stay deterministic. That is a replay-determinism constraint, not a design rule, and it is easy to misread as one. With a scripted autopilot there is no replay to desynchronize, and the recognition design may win instead: entering a name is the reward for reaching the visible table, so a score below the cut goes straight to the rankings. Decide from which attract mode you built, and record the reason.

### 5. Sound: jingles vs SEs

Map ceremonies to jingles (round start, clear, extend, game over) and moments to one-shot SEs; keep them distinct (see `designing-retro-arcade-sound-kits`). Without a jingle API, schedule pitched one-shots on a frame-indexed queue processed in the update loop — and in engines whose game-over call stops that loop, jingles queued past the call never play; fire them while the loop still runs.

### 6. Attract mode

Reuse the engine's replay-recording facility if present. Two traps: the attract loop re-runs game-over paths (must be safe to hit repeatedly), and persistence writes must be guarded by the engine's replay flag or attract re-saves every loop. Keep custom phases input-deterministic so replays stay in sync.

Two additional traps for keyboard-controlled games when the engine's replay records only a unified pointer input, not per-key state (crisp-game-lib does): movement dies in attract mode unless a game-state-driven autopilot takes over under the replay flag, and any input-with-timeout ceremony (initials entry) stalls the attract loop for its full timeout — shorten such timeouts under the replay flag. Branching on the replay flag is deterministic per mode and safe.

#### Scripted autopilot (no replay facility, or replay declined)

When the engine has no replay recorder — or the project turned it down — the demo is a bot driving the real game. Two points carry the weight:

- **Expose it as a policy interface**, not as attract-mode code: `setAutopilot(false | true | "naive")`, feeding **the same control record the keyboard produces**. One implementation then serves three consumers — the attract demo, the balance harness's skilled policy, and any harness that needs a live play screenshot. Wiring the bot directly into the attract branch instead is what forces the other two to be rebuilt later.
- **A demo-quality bot is useless for fairness measurement.** It is tuned to look good, so it flees well and rarely dies, and "is this mechanic unfair?" comes back empty. Ship a **second, deliberately mediocre policy** alongside it — walk at the nearest target, act whenever the affordance is lit, never retreat — and ask fairness questions of that one. Pair it with a death log that records cause and frames-since-the-player's-own-action (see `probing-web-game-mechanics`), and the question becomes a query instead of an argument.

Because the bot plays through the real phase machine, it also exercises the full cycle on every attract loop: game-over paths must stay safe to re-enter, and persistence writes still need guarding.

## Validation

- Probe every phase transition and economy rule with state injection (`probing-web-game-mechanics` for browser games; an equivalent state-injection harness, e.g. headless engine tests, otherwise): quota → clear → next round, extend threshold, entry saving, gate/goal variants. Keep `phase`, round number, and computed round parameters probe-reachable (top-level variables in a classic-script setup, a deliberate debug handle in a bundled one) so probes can read and set them — a rule variant buried in frame-local consts is unverifiable.
- **Screenshot each ceremony screen** — the entry/table class of bug (screen skipped in the same frame, clipped text) passes value assertions and only shows in screenshots.
- **Size and place interactive cursors so they clear the playfield frame on the outermost rows and columns.** The clipped-cursor/clipped-text class is cheaper to prevent by geometry at layout time than to catch by screenshot after the fact — and a cursor that only clips on the top row or the outer column is exactly the case a single screenshot misses.
- **Drive UI flows with at least two synonym keys per named action.** Probing arrows only leaves the WASD path untested and green; observed case, a name-entry cursor that accepted arrows alone in a game whose movement accepted both, which no gate caught.
- Full-cycle check: title → attract loop → game → game over → entry → table → title, twice in a row.
- Re-run the runtime smoke gate after wiring (`smoke-testing-web-games` for browser games; the project's equivalent runtime gate otherwise).

## Common Failure Modes

- Confirm-press bleeding through entry → table → dismiss in one frame.
- Spawners running during clear/death because a mid-frame phase change wasn't re-checked.
- Game-over jingle queued after the engine game-over call — never fires.
- Attract replay diverging because a phase branches on non-deterministic state (e.g. skipping entry only when the score qualifies against a mutable table); prefer always-run phases with guarded side effects.
- Round "variation" that is only bigger numbers — personality comes from changing the *mix*, not the magnitude.

## Output

A round parameter table (data, not code branches), a phase state machine in the existing update loop, extend/entry/table wiring with persistence, a jingle map, and passing probes + ceremony screenshots.
