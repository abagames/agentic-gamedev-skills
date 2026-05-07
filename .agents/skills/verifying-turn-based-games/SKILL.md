---
name: verifying-turn-based-games
description: "Verifies two-player strict-alternating-turn games via a pure-function engine contract and bot-ladder / WP-tension metrics. Use when designing or implementing board/card games that need replay, search, bot ladders, win-rate analysis, tension metrics, or decision-density evaluation. Skip for real-time, simultaneous-action, 3+ player, or single-player puzzle games."
---

# Turn-Based Game Verification

A reusable contract + measurement methodology for two-player turn-based games.

Two parts:

1. **Engine Interface Contract** — pure-function shape any conforming engine must satisfy, enabling search, replay, and quality analysis to be written generically.
2. **Quality Measurement Methodology** — vocabulary and metrics for judging game quality beyond raw win-rates.

This skill prescribes the *what* (contract and metric definitions). It does not prescribe language / runtime / file layout / build system / tooling commands, ideation or tag workflows, player-facing documentation format, or engine code generation — those are project-local choices.

---

## Scope

In scope:

- Two-player, strict alternating turns
- Perfect or imperfect information
- Finite turn cap
- Deterministic RNG via explicit seed (no side-effect randomness)

Out of scope (do not apply):

- Simultaneous actions, reaction/interrupt windows
- 3+ players
- Real-time / non-turn-based
- Single-player puzzles

If the target game does not fit the in-scope list, stop and tell the user this skill does not apply rather than forcing the contract.

---

## Part 1: Engine Interface Contract

The engine MUST expose these pure functions. Signatures shown in TypeScript-ish notation; translate to the host language as needed.

```
init(config?: Config, seed?: number): State
step(state: State, action: Action): { state: State, reward?: number, done: boolean, info: object }
getLegalActions(state: State): Action[]
getObservation(state: State, playerId: PlayerId): State
getResult(state: State): { done: boolean, winners: PlayerId[], reason: string, scores?: Record<PlayerId, number> }
scoreState(state: State, playerId: PlayerId): number
replayLog(state: State): string
cloneState?(state: State): State
```

Contract notes:

- `getLegalActions` and `step` use `state.currentPlayer` implicitly. The contract assumes strict alternating turns; do not extend it to simultaneous play.
- `state.history: Event[]` MUST exist and MUST be appended to inside `step`. `replayLog` is a pure formatter over `state.history`; no external collector.
- `state.rngSeed` MUST exist; all randomness inside `step` derives from it deterministically. No `Math.random()`, clock reads, or other side-effect randomness.
- `getObservation` returns the same `State` type with hidden fields nulled or masked, NOT a different observation type. This keeps bots type-compatible with the engine.
- `getResult` replaces a simpler `getWinner` so callers can distinguish *win-by-HP* / *win-by-deck-out* / *draw-by-turn-cap*. The `reason` string is required.
- `scoreState` is required by the measurement layer (Part 2). An engine that omits `scoreState` cannot be quality-evaluated by this skill.
- `cloneState` is only required when `State` is not fully immutable. If the host language guarantees immutability (or you use structural sharing), omit it.

### Required invariants

- No global mutable state.
- `step` does not mutate its input state. Branch search via `step(cloneState(s), a)` or rely on immutability.
- **Replay determinism**: given a fixed `seed` and a fixed action sequence, `init` followed by repeated `step` produces byte-identical states across runs.
- **Single illegal-action policy**: choose ONE and document it in the engine — throw, return `{ state: s, done: false, info: { illegal: true } }` without state change, or auto-pass. Do not mix policies.
- `Action` and `State` must be JSON-serializable (replay, persistence, search caching all depend on this).

### Pre-implementation checklist

Before writing the engine, the rules document must specify:

- Exact data model for `State` (turn, currentPlayer, public board, private state, rngSeed, history)
- All terminal conditions in priority order, each with its `reason` string
- Action schema and preconditions for each action type
- Pass behavior when `getLegalActions` returns empty
- Hidden information policy (which fields are nulled in `getObservation`)
- Numeric caps that guarantee finite game length

If any item above is unspecified, do not start engine implementation — return to rule design first.

---

## Part 2: Quality Measurement Methodology

Once the engine satisfies Part 1, evaluate quality on two layers.

### Layer A: Win-rate ladder

Implement three bots over the contract:

- **Random** — uniform sample from `getLegalActions`
- **Baseline** — greedy 1-step argmax of `scoreState`
- **Strong** — shallow search (1–2 ply lookahead) over `scoreState`

Measure with **N ≥ 200 games per matchup**, swapping seats to control for first-move advantage.

| Metric | Definition | Target |
|---|---|---|
| Baseline vs Random win rate | Fraction of games the Baseline bot wins against Random, averaged across swapped seats | ≥ 0.65 |
| Strong vs Baseline win rate | Fraction of games the Strong bot wins against Baseline, averaged across swapped seats | ≥ 0.60 |
| First-player advantage | win-rate gap between seats in the same matchup | ≤ 0.10 |
| Action usage distribution | per-action usage rate, per bot | no core action below 0.05 |

### Layer B: Experience metrics

Per game, snapshot `scoreState` each turn. Derive WP (win probability) as `WP = sigmoid((score0 − score1) / T)`. Calibrate temperature `T` per game so that Random-vs-Strong terminal WP for Strong averages ≈ 0.9.

| Metric | Definition | Target |
|---|---|---|
| Tension Score | std-dev of the WP time-series | 0.15–0.35 |
| Lead Change Count | times WP crossed 0.5 | ≥ 2 per game |
| Comeback Rate | fraction of games won by a player who had WP ≤ 0.25 | 0.05–0.25 |
| Flatness Ratio | fraction of games with ≥ 5 consecutive turns of \|ΔWP\| ≤ 0.03 | ≤ 0.20 |
| Final-Stretch Volatility | WP std-dev in the last 25% of turns | ≥ 0.8 × Tension Score |
| Decision Density | mean count of distinct legal actions per turn | game-dependent; report distribution |

### Failure-pattern checklist

When metrics miss targets, look for:

- **Degenerate strong play** — Strong wins but uses only 1–2 distinct actions
- **Dead mechanic** — a specific action never used by any bot (dominated or over-costed)
- **Seat-order flip** — win/loss reverses entirely when seats swap (first-move balance broken)
- **Low-impact loop** — long games dominated by repeated near-zero ΔWP turns

### Improvement-loop discipline

- Change either rules OR bots in a single experiment, never both. Attribution dies if both move.
- Define pass/fail thresholds **before** the rerun, not after the numbers come back.
- Keep a per-experiment changelog: hypothesis / changed files / before-after metrics / decision (adopt or revert).

