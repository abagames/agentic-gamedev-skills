---
name: probing-web-game-mechanics
description: "Verifies that implemented game mechanics match their spec by injecting game state into a live headless browser and asserting the resulting transitions (phase changes, scoring formulas, gates, resets). Use when a change actually reaches a mechanic whose spec conformance is unverified — a smoke test (runtime health) passes but the mechanic's own behavior has not been checked, or when a mechanic is too rare or slow to reach through organic play. Not for crash detection (use smoke-testing-web-games) or play-quality judgment (use evaluating-gameplay-balance)."
---

# Probing Web-Game Mechanics

## Purpose

Deterministically verify that a specific mechanic behaves as specified, by driving a real browser to the exact game state where the mechanic fires. Organic play (bots, manual input) reaches rare states slowly and non-deterministically; state injection reaches them in milliseconds and asserts exact outcomes.

This sits between two other layers — keep them separate:

- **Runtime health** ("the build runs"): `smoke-testing-web-games`
- **Spec conformance** ("the mechanic does what the spec says"): this skill
- **Play quality** ("the game is fun/balanced"): `evaluating-gameplay-balance`

## When to Use

- After implementing or changing a mechanic with discrete expected outcomes: scoring formulas, phase/state transitions, cooldowns, gates, multiplier resets, spawn rules. Probe the mechanics the change reaches, not the whole rule set.
- When the target state is rare or slow to reach organically (game over at high score, round 7 modifier, an enemy-vs-enemy interaction).
- To verify anti-degenerate-play invariants with bot comparison (idle bot vs. active bot).

## When Not to Use

- The change under review does not reach the mechanic in question.
- The game's state is not reachable from the page's global scope and no debug handle can be added (see Required Inputs).
- You only need "does it load and survive input" — that is a smoke test.
- You are judging difficulty or fun — that is balance evaluation, not spec verification.

## Required Inputs

- A runnable build (local `index.html` or dev-server URL) and Playwright + Chromium resolvable from the project directory.
- **State reachability**: game variables readable/writable via `page.evaluate`. Top-level `let`/`var` in a classic `<script>` (e.g. crisp-game-lib games) are reachable by evaluating their names as expressions. For bundled/module games, reaching state usually requires a deliberate debug handle (e.g. `window.__game = { state, step }`). Adding one is a change to the product, so decide it explicitly rather than by default: add the minimal handle when the current work already includes testability or touches that surface; otherwise report the mechanic as unprobeable instead of widening the change. If verification genuinely requires changing a production surface, say so and state why.
- The spec of the mechanic under test, stated as concrete expected values ("bank of n=3 at mult 2 adds 180 and sets mult to 3").

**Treat the debug handle as a maintained contract, not one-time setup.** It grows with the game: any state a rule depends on must stay reachable through it, because a rule buried in a frame-local variable is unverifiable — it cannot be probed, and it will be the rule nobody notices breaking. Two sub-patterns are worth building deliberately rather than discovering late:

- **Measurement hooks** — record causal attribution *at the event*, not reconstructed afterwards from a snapshot. One project's death log returns each death's cause **and how many frames after the player's own action it occurred**; that single field turns "is this mechanic unfair?" from an argument into a query. Reconstructing the same attribution after the fact is usually impossible: the state that caused it has already been overwritten.
- **Machine-readable visual contract** — expose palette-role assignments and HUD layout coordinates as data (e.g. `visualContract()` returning `{palette: {player: "cyan", danger: "red", ...}, hud: {row1Y: 2, gaugeX: 31, ...}}`) so probes assert them as values and the renderer reads the same object. Part of what is assumed to be screenshot-only territory becomes machine-checkable, and the drawing code and the assertion become incapable of disagreeing.

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
- Screenshot any probe that exercises a dedicated screen (game over, tables, overlays), **and any probe that exercises a newly added persistent readout during play**; rendering bugs (clipped text, same-frame screen skips) pass value assertions but are visible in one screenshot. The highest-frequency defect in this class is not a rendering bug at all: it is a rule that is correct in the simulation, passes every assertion you wrote for it, and was **never drawn**. No value assertion can catch that, because the value is right.
- A probe that drives a UI flow must exercise **at least two synonym keys per named action** (e.g. `ArrowUp` and `KeyW` if both are bound to "up"). Probing one key per action leaves every other binding untested and green — observed case: a name-entry cursor bound to arrows only, in a game whose movement also accepted WASD, so WASD players could not enter their initials while both the probe suite and the screenshot harness stayed green.

## Common Failure Modes

- **Injected state vs. per-frame logic**: entities with follow/homing/clamp logic move away from where you placed them on the very next frame. Observed case: a follower placed next to an enemy snapped back to its leader before the enemy could reach it, making the probe silently test nothing. Place entities so the mechanic fires within a frame or two, and position their anchors (leader, target) consistently with the injected layout.
- **Unneutralized spawners/timers**: background spawns wander into the probe area mid-scenario. Park all timers you don't need.
- **Injection collision**: entities injected at the same or nearly the same coordinate interact with *each other* rather than with the mechanic under test. Observed case: several mines injected at one point annihilated each other before the scenario began, so the probe passed while testing nothing. Spread injected entities deliberately, and assert the setup (entity count, positions) before asserting the mechanic.
- **Boot-frame race**: calling a debug entry point before the engine's first frame gets silently clobbered by the engine's own first-frame initialization. Observed case: `startGame()` issued before the boot frame, which then ran `startAttract()` and discarded it. Never gate on a fixed timeout — wait on an **observable state** (`waitForFunction(() => state().phase === "attract")`) before injecting anything.
- **Same-frame input bleed**: one key press can be consumed by two systems in the same frame (finish name entry *and* skip the next screen). Probes that drive UI flows should press keys with real delays between them, and this bug class is worth an explicit probe.
- **Replay/attract determinism**: engines that record inputs for attract replay re-run your update with replayed input; persistence writes (localStorage) must be guarded by the engine's replay flag or the probe (and the attract mode) will double-write.
- **Asserting absolutes instead of deltas**: prior scenarios changed score/lives; record baselines at injection time.
- **Threshold premises rot as the suite grows**: a scenario premised on an accumulating global staying below/above a fixed threshold (e.g. "score is still too low to qualify for the table") breaks when scenarios added earlier change the accumulation. Seed the comparison state explicitly (e.g. write a known high-score table to storage) instead of relying on what the session happens to have accumulated.

## Output

A probe script kept with the project (scratch area or `tests/`), a pass/fail line per scenario with expected-vs-actual values, and screenshots for screen-level scenarios. Report probe-artifact failures separately from real bugs.
