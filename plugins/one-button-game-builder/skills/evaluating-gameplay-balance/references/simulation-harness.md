# Simulation Harness Design

Use this when a project does not already produce the balance telemetry required by `log-contract.md`.

The harness should make game runs comparable. It does not need to be a full copy of the renderer, physics engine, or UI; it needs a deterministic forward model that can run the same game rules under several input policies and emit the same event categories every run.

## 1. Required Pieces

Build or locate these pieces before balance analysis.

- **Game adapter**: a thin wrapper around the game loop exposing `init(seed)`, `step(input, dt)`, `get_score()`, `is_game_over()`, and optional `get_state_snapshot()`.
- **Deterministic random source**: all spawn, hazard, reward, and AI randomness must use a seeded generator controlled by the harness.
- **Public input schema**: the buttons, axes, touch regions, or action states a player can actually use, including ranges, neutral values, timing semantics, and simultaneous-input constraints when relevant.
- **Visible-state schema**: the world facts policies may read, limited to what a player could infer from the screen unless the run is explicitly marked as an oracle upper bound.
- **Policy visibility map**: the visible-state features each policy can read.
- **Policy execution profiles**: `oracle`, `precise`, or `human-limited` per non-baseline policy, with the human-limit parameter values (section 5).
- **Input policies**: at minimum include idle/no-input and simple repeated-action policies; add game-specific monotonous policies when the control scheme differs.
- **Exploratory policy runner**: random search, heuristic search, replay search, or genetic search that tries multiple input sequences with fixed seeds.
- **Event logger**: records death, spawn, scoring, and input events during each simulated run.
- **Reporter**: writes a JSON object matching `log-contract.md`; stdout is acceptable, and files may be written under the project's normal `logs/`, `reports/`, `artifacts/`, or `test-results/` directory.

## 2. Adapter Contract

Keep the adapter small and engine-local.

```text
create_adapter(game, seed):
  reset game state
  install seeded RNG
  define public_input_schema
  define visible_state_schema
  return:
    step(input_frame) -> events
    score() -> number
    elapsed() -> seconds
    ended() -> bool
    snapshot() -> optional serializable state
```

For engines with a real-time update loop, run fixed ticks rather than wall-clock time. For render-dependent games, separate rule updates from drawing enough that the harness can advance the world headlessly.

If exact engine simulation is too expensive, implement the smallest faithful forward model for the systems being evaluated: player movement, hazards, rewards, scoring, damage, game-over, and spawn generation.

## 3. Input Policy Set

Policies should be explicit, reproducible functions from tick/state to input.

Recommended baseline policies:

- `no_input`: never presses the primary action.
- `hold_action`: holds the primary action for the whole run.
- `spam_action`: presses/releases on a short fixed cadence.
- `periodic_action`: presses on one or more slower cadences when timing matters.
- `random_action`: samples input from a seeded distribution.
- `exploratory`: searches over sequences or state-based choices and reports the best run.

One-button games usually need press, hold, and release timing. Multi-input games should define equivalent monotonous policies for each dominant simple strategy, such as always-left, always-fire, always-boost, or shortest-path greed.

Do not hard-code a policy that knows hidden internals unavailable to a player unless the goal is explicitly to test an upper bound. Prefer state features a player could infer from the screen.

When the control scheme is unknown, first write the public input schema, then derive policies from it:

```text
input_schema:
  move_x: axis -1..1
  move_y: axis -1..1
  primary: boolean
  secondary: boolean
  simultaneous: move axes plus at most one action

monotonous_candidates:
  no_input
  fixed_direction(move_x=1)
  hold_primary
  spam_primary(period=8 ticks)
  greedy_nearest_reward using visible positions
```

For each policy, record its visibility:

```text
policy_visibility:
  no_input: []
  fixed_direction: []
  hold_primary: []
  greedy_nearest_reward: [player_position, reward_positions]
  exploratory: [player_position, hazard_positions, reward_positions]
```

## 4. Exploratory Runner

The exploratory runner exists to detect whether skillful or varied play can outperform monotony.

Acceptable approaches:

- Random input sequence search over many seeds.
- Heuristics using visible state, such as distance to hazards, reward positions, or resource levels.
- Genetic search over input timings or compact action genomes.
- Replay mutation: mutate the best previous sequence and keep improvements.

Report the best score, elapsed time, seed, and variant. Keep the same search budget before and after changes so comparisons remain meaningful.

Record the exploratory runner's budget in the report: number of seeds, variants, generations, random samples, replay mutations, max ticks, and visible-state features. If this budget changes after a gameplay fix, rerun the baseline with the new budget before comparing.

### Running policies concurrently

Policies with fully isolated state (separate pages, processes, or engine instances, no shared storage) can run **in parallel only after a calibration run shows that concurrency does not materially change tick/frame counts or timer cadence**. A three-policy comparison over a 90 s observation window can then cost 90 s of wall time instead of 270 s. Record processed ticks/frames and observed slowdown for every run, keep the concurrency level fixed before and after a change, and discard or rerun samples affected by throttling. If policies contend differently or a parallel run diverges from a serial calibration, run them serially.

State isolation is necessary but not sufficient — shared high-score storage, RNG, or audio context correlates samples, while shared CPU/GPU, browser event loops, and background-tab throttling can change how much simulation a wall-clock window contains.

## 5. Execution Profiles

The visible-state schema limits what a policy may **know**. An execution profile limits what it can **do**. A policy that reads only visible state but acts with frame-perfect timing, zero latency, and unlimited attention still overestimates human players, and difficulty tuned against it comes out too harsh in a consistent direction.

Declare one profile per policy:

| Profile | Knowledge | Execution | Use for |
|---|---|---|---|
| `oracle` | hidden state allowed | unrestricted | upper bounds only |
| `precise` | visible state | near-perfect timing and attention | exploit and degenerate-strategy detection; the exploratory ratio |
| `human-limited` | visible state | the limits below | difficulty, timers, pacing, progression targets |

Monotonous baselines (idle, hold, fixed-cadence spam) need no profile beyond their definition; they are strategies, not skill models.

### Human limits to model

Model the limits that the game's decisions actually exercise; not every game needs all of them. Record the values used in the report.

| Limit | Model |
|---|---|
| Reaction latency | delay between a new visible event and the earliest response |
| Timing error | random error on the moment of a timed input; for aimed or rotating inputs, also angular or positional error |
| Attention lapse | per decision, probability of not checking a secondary threat (the landing area, a second enemy, an off-center hazard) |
| Perception error | error in reading positions, distances, and gauge levels from the screen |
| Information decay | stale displayed information is distrusted or forgotten rather than extrapolated indefinitely |
| Re-orientation | after the frame of reference changes (teleport, camera cut, moved pivot, screen flip), no accurate aimed action until the new picture has been read |
| Repetition limit | accurate actions cannot repeat faster than re-orientation allows; only panic or escape actions may be quicker |

Starting points from one tuned one-button game (a rotating-sweep radar shooter): reaction 200–300 ms, timing σ 50–80 ms, attention lapse 0.3–0.5, forget stale blips after ~1.5 refresh cycles, re-orientation ~0.5 sweep revolution after a teleport. These came from a single game and its designer's play reports; treat them as a first guess, not a norm, and recalibrate for other genres and control schemes.

### Calibrating against play reports

Hands-on play reports are the ground truth the human-limited profile approximates. When a report disagrees with simulated results ("still too hard", "the gauge runs out too fast", "I always die after blinking next to an enemy"):

1. Check the harness for defects first (section 6).
2. Adjust the profile parameters toward the report, preferring limits the report names or implies. Note the reporter's skill relative to the target audience (a designer is usually an expert); do not fit the profile to one expert when the audience is broader.
3. Re-run and record the report, the reporter's skill level, and the adjusted values.

In the observed case, simulated players that re-aimed immediately after every blink led to three rounds of "still too hard" reports. Modeling the designer's stated re-orientation delay reproduced the chain-oriented play that humans drifted into and the bots had not shown.

### Skill-dependent verdicts

Run the key comparison under both `precise` and `human-limited` before calling a strategy dominant or a trade-off balanced. In the observed case, precise bots scored best by shooting immediately while the human-limited bot scored ~1.8× more by waiting for chains. That is a skill-dependent design property, not a dominant strategy to remove. A flip does not exempt either optimum from the experience guardrails: if the human-limited best strategy is monotonous (idling, waiting out the clock, one-pattern spam), treat it as a defect.

### Measurement circularity

When tuning a parameter (a timer, a gauge, a spawn rate), do not measure with a policy whose behavior is defined by that parameter. A policy that waits "while the bonus bar is above 80 %" waits longer when the bar slows, so the bar never looks slow enough. Measure with a policy independent of the parameter, then check the dependent policies afterwards.

## 6. Simulated-Player Sanity Checks

The checks below use the input kinds `aimed` (a precise, targeted action), `reactive` (a response to a visible event), and `escape` (a panic or evasive action). These fit tap-style controls; for hold, analog, or multi-button schemes, define kinds that separate deliberate precise actions from panic actions and apply the same checks.

Before drawing balance conclusions, check each non-trivial policy for artifacts of its own implementation. A policy that fails a check is a harness defect, not evidence about the game.

- **Failure attribution (all profiles):** break down deaths by cause *and* by the kind of input that preceded them. A large share following one input kind (for example, 75 % of deaths after escape presses) needs an explanation before the runs are trusted.
- **Belief sanity (policies that estimate positions or hidden state):** log estimated versus true values. Stale estimates must not drift toward the player or collapse onto a single point. Observed case: stale-blip extrapolation converged on the player, so the bot panic-pressed about every 0.8 s and most of its deaths followed those presses.
- **Input rate (`human-limited` only):** report aimed and reactive/escape inputs separately. Aimed inputs stay within the re-orientation limit; escape inputs recurring on a steady cadence without a matching visible threat indicate a belief or trigger defect even when the overall rate looks human.
- **Execution probe (`human-limited` only):** confirm the policy cannot perform accurate actions closer together than its re-orientation delay; measure the minimum interval between aimed inputs.

Oracle and precise policies are expected to act faster than humans; do not apply the human input-rate checks to them.

## 7. Telemetry Events

Log raw events first, then aggregate them into `log-contract.md`.

Recommended raw event shapes:

```json
{"tick": 120, "type": "input", "pressed": true, "held": false, "kind": "aimed"}
{"tick": 184, "type": "spawn", "kind": "hazard", "x": 92, "y": 38}
{"tick": 240, "type": "score", "amount": 2, "reason": "near_miss", "x": 41, "y": 62}
{"tick": 301, "type": "death", "cause": "collision", "object": "hazard", "x": 47, "y": 65, "preceding_input_kind": "escape", "since_last_input_ms": 180}
```

Aggregate at least:

- Death clusters, causes, position distribution, and deaths shortly after input.
- Spawn intervals, position distribution, type distribution, and minimum distance to player when available.
- Scoring triggers, score amounts, score timing, and whether score correlates with raw input count.
- Input pattern summaries such as hold duration, press interval distribution, and dominant simple pattern.
- For policies that declare input kinds: inputs by kind, and deaths by preceding input kind and time since that input.

## 8. Output And Discovery

The skill does not require a universal file path. Prefer the project's existing convention.

Reasonable output targets:

- stdout JSON for CLI tools and CI.
- `logs/balance/*.json`
- `reports/balance/*.json`
- `artifacts/balance/*.json`
- `test-results/balance/*.json`

If adding a new harness to a project, document the command that produces the report and the expected output path near the harness. The evaluator should be able to rerun the same command after a gameplay change.

## 9. Incomplete Reports

Score, elapsed time, and `exploratory_ratio` are useful summary signals, but they are not enough to diagnose balance.

If any of the four telemetry perspectives are missing:

1. Mark the report as insufficient for root-cause balance judgment.
2. Keep the existing summary metrics as baseline signals.
3. Add raw event logging or aggregation for the missing perspective.
4. Rerun the same monotonous and exploratory policies with deterministic seeds.
5. Only then propose structural gameplay fixes.

## 10. Failure Modes

Reject or revise the harness when:

- The renderer and simulator use different gameplay constants.
- Randomness is not seeded.
- Monotonous and exploratory runs use different game settings.
- The exploratory runner gets hidden information that a player cannot perceive.
- A policy's execution profile is undeclared, or difficulty and pacing targets were set from `oracle` or `precise` runs.
- A policy failed a sanity check in section 6 and its runs were still used for conclusions.
- A tuned parameter was measured with a policy defined by that same parameter.
- The public input schema or visible-state schema is undocumented.
- The logger awards score from input facts rather than in-game causal events.
- The report only contains summary score and elapsed time, with no death/spawn/scoring/input breakdown.
- Before/after comparisons use different seeds, budgets, policies, or max ticks without explanation.
