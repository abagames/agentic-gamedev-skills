---
name: probing-web-game-mechanics
description: "Verifies that implemented game mechanics match their spec by injecting game state into a live headless browser and asserting the resulting transitions (phase changes, scoring formulas, gates, resets). Use after implementing or changing a specific mechanic in a browser game — when a smoke test (runtime health) passes but spec conformance is unverified, or when a mechanic is too rare or slow to reach through organic play. Not for crash detection (use smoke-testing-web-games) or play-quality judgment (use evaluating-gameplay-balance)."
---

# Probing Web-Game Mechanics

## Purpose

Deterministically verify that a specific mechanic behaves as specified, by driving a real browser to the exact game state where the mechanic fires. Organic play (bots, manual input) reaches rare states slowly and non-deterministically; state injection reaches them in milliseconds and asserts exact outcomes.

This sits between two other layers — keep them separate:

- **Runtime health** ("the build runs"): `smoke-testing-web-games`
- **Spec conformance** ("the mechanic does what the spec says"): this skill
- **Play quality** ("the game is fun/balanced"): `evaluating-gameplay-balance`

## When to Use

- After implementing or changing a mechanic with discrete expected outcomes: scoring formulas, phase/state transitions, cooldowns, gates, multiplier resets, spawn rules.
- When the target state is rare or slow to reach organically (game over at high score, round 7 modifier, an enemy-vs-enemy interaction).
- To verify anti-degenerate-play invariants with bot comparison (idle bot vs. active bot).

## When Not to Use

- The game's state is not reachable from the page's global scope and no debug handle can be added (see Required Inputs).
- You only need "does it load and survive input" — that is a smoke test.
- You are judging difficulty or fun — that is balance evaluation, not spec verification.

## Required Inputs

- A runnable build (local `index.html` or dev-server URL) and Playwright + Chromium resolvable from the project directory.
- **State reachability**: game variables readable/writable via `page.evaluate`. Top-level `let`/`var` in a classic `<script>` (e.g. crisp-game-lib games) are reachable by evaluating their names as expressions. For bundled/module games, expose a deliberate debug handle first (e.g. `window.__game = { state, step }`) — do not skip verification because state is hidden; add the handle.
- The spec of the mechanic under test, stated as concrete expected values ("bank of n=3 at mult 2 adds 180 and sets mult to 3").

## Procedure

1. **Copy the harness**: start from `scripts/probe-template.mjs` (copy into the project scratch area and adapt; it is a template to edit, not a runner to execute as-is). It resolves Playwright from the project cwd, captures `pageerror`/`console.error` in every phase, and exits non-zero on any error.
2. **Start the game for real**: load the page, wait for init, send the input that leaves the title screen. Never assert against a game still on its title/attract state.
3. **Inject the minimal state and neutralize confounders**: set only the variables the mechanic needs, and explicitly park everything else that could interfere — disable spawn timers (set them huge), clear other entity arrays, make the player invulnerable if death would interrupt the probe. An unneutralized confounder is the main source of flaky probes.
4. **Let frames settle, then assert**: wait a small real-time interval (100–400 ms) so the game loop processes the injected state, then read back concrete values and compare with the spec. Record before/after pairs (`window.__s0 = score` at injection time) so assertions are deltas, not absolutes.
5. **Chain scenarios in one session** but reset shared state (storage keys, lives, phase) between them; a leftover from scenario A silently corrupts scenario B.
6. **For invariants, compare bots**: run the same build with (a) no input after start and (b) random/scripted input, sampling score/lives/entity counts every few seconds. The invariant is the *comparison* (idle must not out-survive or out-score active play), not either run alone.

## Validation

- Every probe asserts at least one concrete expected value from the spec; a probe that only checks "no errors" is a smoke test in disguise.
- The full probe run exits 0 with zero captured page errors *and* all assertions matching.
- When a probe fails, first decide: implementation bug, spec ambiguity, or **probe artifact** (see failure modes) — do not patch game code until the probe itself is validated.
- Screenshot any probe that exercises a dedicated screen (game over, tables, overlays); rendering bugs (clipped text, same-frame screen skips) pass value assertions but are visible in one screenshot.

## Common Failure Modes

- **Injected state vs. per-frame logic**: entities with follow/homing/clamp logic move away from where you placed them on the very next frame. Observed case: a follower placed next to an enemy snapped back to its leader before the enemy could reach it, making the probe silently test nothing. Place entities so the mechanic fires within a frame or two, and position their anchors (leader, target) consistently with the injected layout.
- **Unneutralized spawners/timers**: background spawns wander into the probe area mid-scenario. Park all timers you don't need.
- **Same-frame input bleed**: one key press can be consumed by two systems in the same frame (finish name entry *and* skip the next screen). Probes that drive UI flows should press keys with real delays between them, and this bug class is worth an explicit probe.
- **Replay/attract determinism**: engines that record inputs for attract replay re-run your update with replayed input; persistence writes (localStorage) must be guarded by the engine's replay flag or the probe (and the attract mode) will double-write.
- **Asserting absolutes instead of deltas**: prior scenarios changed score/lives; record baselines at injection time.
- **Threshold premises rot as the suite grows**: a scenario premised on an accumulating global staying below/above a fixed threshold (e.g. "score is still too low to qualify for the table") breaks when scenarios added earlier change the accumulation. Seed the comparison state explicitly (e.g. write a known high-score table to storage) instead of relying on what the session happens to have accumulated.

## Output

A probe script kept with the project (scratch area or `tests/`), a pass/fail line per scenario with expected-vs-actual values, and screenshots for screen-level scenarios. Report probe-artifact failures separately from real bugs.
