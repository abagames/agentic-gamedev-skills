# Godot Balance Pattern Examples

Godot/GDScript examples for applying engine-neutral balance patterns after telemetry identifies a balance problem and a structural fix to apply.
This file is self-contained: it summarizes the reusable pattern categories before showing Godot-specific implementations.

## Overview

Balance adjustments fall into several categories:

1. **Difficulty Scaling** - How game parameters change with `difficulty` variable
2. **Scoring Systems** - Risk/reward and combo mechanics
3. **Boundary Behavior** - Wall collision and screen edge handling
4. **Self-Balancing Mechanisms** - Automatic difficulty adjustment
5. **Input Response** - How button states affect game behavior
6. **Spawn Patterns** - Enemy and obstacle placement

Engine-neutral pattern vocabulary used below:

- Diminishing difficulty growth: replace harsh linear scaling with `sqrt(difficulty)` or another decelerating curve.
- Risk-based scoring: reward close calls, precision, route cost, or exposure to danger.
- Visible failure consequence: replace unclear instant death with wrap, bounce, resource loss, or combo loss when that preserves fairness.
- Input state tradeoff: holding, tapping, and idling should each improve one thing while worsening another.
- Spawn fairness: reject hazards that appear inside minimum clearance or repeatedly pressure the same cell.
- State and territory pressure: decay accumulated advantage and let player actions leave world traces that change later decisions.

## Guardrails (Read Before Applying Patterns)

When used inside a repository with an `AGENTS.md`, that file remains the source of truth for project-specific execution rules. This guide only provides reusable balance patterns to apply under those rules.

Quick reminder:

- Validate changes with short human play, not test logs alone.

---

## 1. Difficulty Scaling Patterns

### `difficulty` variable convention

| Property | Value |
|:---------|:------|
| Initial value | `1` |
| Increment | `+1` per elapsed minute |
| Typical range | `1`–`5` (most games end within 5 minutes) |

All patterns in this section assume the above convention. `difficulty = 1` at game start means `sqrt(difficulty) = 1`, so formulas degrade gracefully to base values.

### Pattern 1.1: Linear to Square Root Conversion

**Problem**: Difficulty increases too quickly, game becomes unplayable.

**Diagnosis**: `telemetry.death_analysis` shows deaths concentrated at high difficulty.

**Before**:
```gdscript
var speed := 0.5 + difficulty * 0.1
var spawn_rate := 60.0 - difficulty * 3.0
```

**After**:
```gdscript
var speed := 0.5 * sqrt(difficulty)
var spawn_rate := 60.0 / sqrt(difficulty)
```

**Effect**: Decelerating growth curve - still gets harder but plateaus naturally.

### Pattern 1.2: Multiplicative Difficulty

**Problem**: Game feels the same at all difficulty levels.

**Diagnosis**: `exploratory_ratio` close to 1.0 at all stages.

**Before**:
```gdscript
player.position += player.velocity
blade_angle += rotate_speed
```

**After**:
```gdscript
player.position += player.velocity * sqrt(difficulty)
blade_angle += rotate_speed * sqrt(difficulty)
```

**Effect**: Everything scales together, maintaining consistent feel while increasing challenge.

### Pattern 1.3: Inverse Difficulty for Spawn Intervals

**Problem**: Spawn rate doesn't accelerate enough.

**Diagnosis**: `telemetry.spawn_analysis.average_interval` too high at late game.

**Before**:
```gdscript
spawn_timer = 60.0 - difficulty * 3.0  # Caps at difficulty 20
```

**After**:
```gdscript
spawn_timer = 60.0 / difficulty  # Continuously decreases
```

---

## 2. Scoring System Patterns

### Pattern 2.1: Risk-Based Scoring

**Problem**: Score doesn't reflect skill or risk-taking.

**Diagnosis**: `telemetry.scoring_analysis.triggers` shows only one scoring method.

**Before**:
```gdscript
add_score(10)  # Fixed points
```

**After**:
```gdscript
add_score(obstacles.size())    # More risk = more reward
add_score(ceili(player.size))  # Bigger target = more points
add_score(multiplier)          # Consecutive success rewarded
```

**Games using this**: cling-hop, phaserun, geyser-hop

### Pattern 2.2: Score Scale Reduction

**Problem**: Scores inflate too quickly, numbers become meaningless.

**Diagnosis**: Final scores in millions, hard to compare runs.

**Before**:
```gdscript
# Points per action
var points := {&"large": 10, &"medium": 20, &"small": 30}
```

**After**:
```gdscript
# Points per action
var points := {&"large": 1, &"medium": 2, &"small": 3}
```

**Games using this**: splitzig

### Pattern 2.3: Exponential Combo Scoring

**Problem**: Multi-kills don't feel rewarding enough.

**Diagnosis**: `telemetry.scoring_analysis.scoring_rate` flat regardless of combo.

**Before**:
```gdscript
add_score(destroyed_count * base_points)
```

**After**:
```gdscript
add_score(destroyed_count * destroyed_count)
```

**Games using this**: star-eater

### Pattern 2.4: Combo Multiplier System

**Problem**: No incentive for consecutive successes.

**Diagnosis**: `telemetry.input_analysis.pattern` shows no rhythm.

**Implementation**:
```gdscript
var multiplier := 1

# On success
multiplier = mini(multiplier + 1, max_multiplier)
add_score(base_points * multiplier)

# On failure/miss
multiplier = maxi(multiplier - 1, 1)
```

**Games using this**: geyser-hop, geoerase, inkinh

---

## 3. Boundary Behavior Patterns

### Pattern 3.1: Game Over to Screen Wrap

**Problem**: Deaths concentrated at screen edges.

**Diagnosis**: `telemetry.death_analysis.position` clusters near boundaries.

**Before**:
```gdscript
if player.position.x < 5.0 or player.position.x > 95.0:
    end_game()
```

**After**:
```gdscript
player.position.x = wrapf(player.position.x, 0.0, 100.0)
```

**Games using this**: splitzig

### Pattern 3.2: Moving Boundaries

**Problem**: Stationary gameplay, no positional challenge.

**Diagnosis**: `telemetry.input_analysis` shows timing-only patterns.

**Before**:
```gdscript
var gate_pos := Vector2(50.0, 92.0)  # Fixed position
```

**After**:
```gdscript
var gate_pos := Vector2(50.0, 92.0)
var gate_vx := 1.0
# In _process:
gate_pos.x += gate_vx * sqrt(difficulty)
if gate_pos.x > 90.0 or gate_pos.x < 10.0:
    gate_vx *= -1.0
```

**Games using this**: dark_sort

### Pattern 3.3: Bounce Instead of Death

**Problem**: Wall collision ends game too abruptly.

**Before**:
```gdscript
if player.position.x > 90.0:
    end_game()
```

**After**:
```gdscript
if player.position.x > 90.0:
    player.position.x = 90.0
    player_vx *= -1.0
```

**Games using this**: stompshelter

---

## 4. Self-Balancing Mechanisms

### Pattern 4.1: Resource Decay

**Problem**: Accumulated advantage makes game trivial.

**Diagnosis**: Exploratory test easily reaches high scores by accumulating resources.

**Before**:
```gdscript
stack_height += points  # Only increases
```

**After**:
```gdscript
stack_height += points
stack_height *= 0.998  # Constant decay
```

**Games using this**: splitzig

### Pattern 4.2: Cooldown Reduction on Success

**Problem**: Good play should be rewarded with more action.

**Implementation**:
```gdscript
var base_cooldown := 40.0
# On combo success
cooldown = floor(base_cooldown / (1.0 + combo_count * 0.5))
cooldown = maxf(cooldown, min_cooldown)
```

**Games using this**: wipe-blade

### Pattern 4.3: Penalty for Missed Opportunities

**Problem**: No consequence for passive play.

**Constraint**: Penalty must be tied to an in-world missed event, not to "did not press a button."

**Diagnosis**: `telemetry.input_analysis.pattern` shows "no_input" works.

**Implementation**:
```gdscript
# When geyser leaves screen without being stomped
if not g.stomped and g.position.x < -15.0:
    multiplier = maxi(multiplier - 1, 1)
```

**Games using this**: geyser-hop

---

## 5. Input Response Patterns

### Pattern 5.1: State-Dependent Speed

**Problem**: No skill expression through input timing.

**Diagnosis**: `telemetry.input_analysis` shows hold or spam is optimal.

**Before**:
```gdscript
laser_angle += laser_speed  # Constant speed
```

**After**:
```gdscript
var speed_mul := 1.0 if is_pressing else 2.0
laser_angle += laser_speed * speed_mul * sqrt(difficulty)
# Faster rotation when NOT pressing - rewards timing
```

**Games using this**: geoerase, inkinh

### Pattern 5.2: Hold-to-Grow Mechanics

**Problem**: No risk/reward in holding vs tapping.

**Implementation**:
```gdscript
if is_pressing:
    player.target_size += growth_rate  # Grows while holding
# Scoring based on size
add_score(ceili(player.size))  # Bigger = more points but also more vulnerable
```

**Games using this**: phaserun

### Pattern 5.3: Hold Accelerates Danger

**Problem**: Holding has no downside.

**Constraint**: This pattern is invalid if it creates unavoidable damage/death loops or removes meaningful recovery options.

**Implementation**:
```gdscript
# Wall press speed depends on input
var press_rate := 0.2 if is_pressing else 0.05
wall_press += press_rate * sqrt(difficulty)
```

**Games using this**: pressbound

---

## 6. Spawn Patterns

### Pattern 6.1: Safety Distance Check

**Problem**: Unfair instant deaths on spawn.

**Diagnosis**: `telemetry.death_analysis.recent_frames` shows death right after spawn.

**Before**:
```gdscript
asteroids.append({"pos": Vector2(randf() * 100.0, 0.0)})
```

**After**:
```gdscript
var pos := Vector2(randf() * 100.0, 0.0)
if pos.distance_to(player.position) > safe_distance:
    asteroids.append({"pos": pos})
```

**Games using this**: star-eater, inkinh

### Pattern 6.2: Countdown vs Ticks-Based Spawning

**Problem**: Spawn timing is too predictable or too random.

**Before**:
```gdscript
if tick % 60 == 0:
    spawn_enemy()  # Predictable
```

**After**:
```gdscript
next_spawn_ticks -= 1
if next_spawn_ticks <= 0:
    spawn_enemy()
    next_spawn_ticks = int(randf_range(base_interval * 0.8, base_interval * 1.2) / sqrt(difficulty))
```

**Games using this**: star-eater, phaserun, geyser-hop

### Pattern 6.3: Adaptive Spawn Position

**Problem**: Player can camp in safe spot.

**Diagnosis**: `telemetry.death_analysis.position` shows player stays in one area.

**Before**:
```gdscript
var from_left := randf() < 0.5  # Random side
```

**After**:
```gdscript
var from_left := player.position.x > 50.0  # Spawn from opposite side
```

**Games using this**: cling-hop

### Pattern 6.4: Distance-Based Enemy Spawn

**Problem**: Enemy spawn doesn't relate to player progress.

**Before**:
```gdscript
if tick % 100 == 0:
    spawn_enemy()
```

**After**:
```gdscript
next_enemy_dist -= scroll_amount  # Tied to player progress
if next_enemy_dist < 0.0:
    spawn_enemy()
    next_enemy_dist = randf_range(100.0, 200.0) / sqrt(difficulty)
```

**Games using this**: stompshelter

---

## 7. Mechanic Addition Patterns

### Pattern 7.1: Attack/Defense Toggle

**Problem**: Player is purely passive, only avoiding.

**Diagnosis**: `telemetry.input_analysis.pattern` shows "no_input" or evasion only.

**Implementation**: Add ability to destroy obstacles in specific state.

```gdscript
# Player can destroy obstacles when airborne (yellow)
# vs invulnerable when clinging (cyan)
var color := Color.CYAN if cling_target != null else Color.YELLOW
# ... later in obstacle collision:
if is_clinging:
    end_game()
else:
    # Destroy obstacle
    play_sfx("power_up")
    spawn_particles(obs.position, 20, 3.0)
    obs.queue_free()
```

**Games using this**: cling-hop

### Pattern 7.2: Movement Control Addition

**Problem**: Player movement is purely automatic.

**Implementation**:
```gdscript
# Original: fixed horizontal position
player.position.x += (50.0 - player.position.x) * 0.01

# Revised: add player control
var move_mul := 1.0 if is_pressing else 0.1
player.position.x += player_vx * move_mul
if player.position.x > 90.0 or player.position.x < 10.0:
    player_vx *= -1.0
```

**Games using this**: stompshelter

## 8. Timing & Rhythm Patterns

### Pattern 8.1: Window-Based Scoring

**Problem**: Score doesn't reflect timing precision.

**Diagnosis**: `telemetry.scoring_analysis.triggers` shows fixed points regardless of timing.

**Implementation**:
```gdscript
var window_center := target_beat_time
var delta_t := absf(input_time - window_center)

if delta_t < perfect_window:
    add_score(base_points * 3)  # Perfect
elif delta_t < good_window:
    add_score(base_points * 1)  # Good
else:
    multiplier = 1  # Miss resets combo
```

### Pattern 8.2: Tempo Escalation

**Problem**: Rhythm game feels static across difficulty levels.

**Implementation**:
```gdscript
var bpm := base_bpm + difficulty * 8.0
var beat_interval := 60.0 / bpm
# Introduce syncopation at higher difficulty
if difficulty > 3:
    beat_interval *= (1.0 if beat_index % 4 != 3 else 0.75)
```

---

## 9. State Management Patterns

### Pattern 9.1: State Decay Pressure

**Problem**: Player can maintain a safe state indefinitely.

**Diagnosis**: `hold_action` score equals or exceeds exploratory score.

**Implementation**:
```gdscript
# Maintaining current state has escalating cost
state_stability -= delta * (1.0 + state_duration * 0.3)
if state_stability <= 0.0:
    force_state_transition()
```

### Pattern 9.2: Multi-Resource Tension

**Problem**: Single resource makes optimal play obvious.

**Implementation**:
```gdscript
# Two resources with inverse relationship
func consume_action():
    energy -= action_cost
    heat += action_heat
    if heat > overheat_threshold:
        enter_cooldown_state()  # Locked out temporarily
    # Score scales with heat risk
    add_score(base_points * (1.0 + heat / overheat_threshold))
```

### Pattern 9.3: Toggle State Trade-off

**Problem**: State toggle (reverse_state) has no meaningful cost.

**Implementation**:
```gdscript
# Each state has advantages and vulnerabilities
match current_state:
    State.ALPHA:
        can_collect_alpha_items = true
        vulnerable_to_beta_hazards = true
    State.BETA:
        can_collect_beta_items = true
        vulnerable_to_alpha_hazards = true
# Switching has brief vulnerability window
if just_switched:
    vulnerable_to_all = true
    switch_cooldown = 0.3
```

---

## 10. Spatial & Territory Patterns

### Pattern 10.1: Coverage Scoring

**Problem**: No incentive for spatial exploration.

**Diagnosis**: Player stays in one area.

**Implementation**:
```gdscript
var visited_cells: Dictionary = {}
const CELL_SIZE := 40.0

func _on_player_moved(pos: Vector2) -> void:
    var cell_key := Vector2i(int(pos.x / CELL_SIZE), int(pos.y / CELL_SIZE))
    if not visited_cells.has(cell_key):
        visited_cells[cell_key] = true
        add_score(coverage_bonus)
```

### Pattern 10.2: Territory Pressure

**Problem**: Painted/claimed territory is permanent — no tension.

**Implementation**:
```gdscript
# Territory decays over time, requiring re-engagement
for cell_key in owned_territory.keys():
    owned_territory[cell_key] -= decay_rate * delta
    if owned_territory[cell_key] <= 0.0:
        owned_territory.erase(cell_key)
# Score based on territory held, not territory ever claimed
add_score(owned_territory.size() * hold_bonus * delta)
```

---

## 11. Construction & Puzzle Patterns

### Pattern 11.1: Placement Quality Scoring

**Problem**: Any placement scores equally.

**Implementation**:
```gdscript
func score_placement(piece_pos: Vector2, existing_pieces: Array) -> int:
    var adjacency_bonus := 0
    var alignment_bonus := 0
    for p in existing_pieces:
        if p.pos.distance_to(piece_pos) < snap_distance:
            adjacency_bonus += 1
        if is_aligned(p, piece_pos):
            alignment_bonus += 2
    return base_points + adjacency_bonus * 3 + alignment_bonus * 5
```

### Pattern 11.2: Time Pressure with Grace

**Problem**: Construction has no urgency.

**Implementation**:
```gdscript
# Deadline approaches, but good play extends it
var time_remaining := base_time
func on_successful_build():
    time_remaining += time_extension  # Reward extends deadline
func _process(delta):
    time_remaining -= delta * (1.0 + difficulty * 0.15)
    if time_remaining <= 0.0:
        end_round()
```

---

## Quick Reference: Problem → Pattern

| Problem | Pattern |
|:--------|:--------|
| Deaths at screen edges | 3.1 Screen Wrap or 3.3 Bounce |
| Deaths at high difficulty | 1.1 sqrt() Conversion |
| No skill expression | 5.1 State-Dependent Speed |
| Spam is optimal | 4.3 Miss Penalty, 5.3 Hold Danger |
| Hold is optimal | 5.1 State Speed, 2.1 Risk Scoring |
| No input is optimal | 4.3 Miss Penalty, 7.2 Movement Control |
| Instant deaths on spawn | 6.1 Safety Distance |
| Score inflation | 2.2 Score Reduction |
| No combo incentive | 2.4 Multiplier System |
| Static gameplay | 3.2 Moving Boundaries, 6.3 Adaptive Spawn |
| Timing doesn't matter | 8.1 Window Scoring |
| Rhythm feels static | 8.2 Tempo Escalation |
| Safe state is permanent | 9.1 State Decay, 9.3 Toggle Trade-off |
| Single resource trivializes play | 9.2 Multi-Resource Tension |
| No spatial exploration incentive | 10.1 Coverage Scoring |
| Territory has no tension | 10.2 Territory Pressure |
| All placements equal | 11.1 Placement Quality |
| No urgency in construction | 11.2 Time Pressure with Grace |

---

## Implementation Checklist

When applying balance patterns:

1. **Run the repeatable balance test first** to identify problems
2. **Check the problem → pattern table** above
3. **Apply ONE pattern at a time**
4. **Re-run headless test** to verify improvement
5. **Run a 2-minute human play sanity check**
6. **If `exploratory_ratio` still ≤ 1.5**, apply additional patterns only when sanity check passes

### Telemetry Analysis Focus Areas

```text
// From logs/test.json → telemetry:

// 1. Death Analysis
telemetry.death_analysis.position       // Where deaths occur
telemetry.death_analysis.recent_frames  // What happened before death

// 2. Input Analysis
telemetry.input_analysis.pattern        // "spam", "hold_heavy", "no_input", "varied"
telemetry.input_analysis.total_presses  // How many inputs in a run

// 3. Scoring Analysis
telemetry.scoring_analysis.triggers     // What causes scoring
telemetry.scoring_analysis.scoring_rate // Score distribution over time

// 4. Spawn Analysis
telemetry.spawn_analysis.spatial_distribution // Where things spawn
telemetry.spawn_analysis.average_interval     // How often things spawn
```

---

## Example: Full Balance Pass

Given a game with `exploratory_ratio` = 0.8:

1. **Check input pattern**: "spam" → Apply Pattern 5.1 (State-Dependent Speed)
2. **Re-test**: `exploratory_ratio` = 1.1
3. **Check death positions**: clustered at edges → Apply Pattern 3.1 (Screen Wrap)
4. **Re-test**: `exploratory_ratio` = 1.3
5. **Check scoring**: single source → Apply Pattern 2.4 (Combo Multiplier)
6. **Re-test**: `exploratory_ratio` = 1.8 ✓

This systematic approach helps improve balance while preserving play experience through iterative pattern application.
