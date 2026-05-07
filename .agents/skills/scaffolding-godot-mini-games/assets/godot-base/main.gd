extends Node2D

# Template stub: replace with game-specific state and systems.
const MetricsTracker = preload("res://metrics_tracker.gd")

var test_mode := false
var test_action_a := false
var test_action_b := false
var test_action_c := false

# Neutral placeholders. Implement project-specific semantics in game scripts.
var score := 0
var elapsed := 0.0
var game_over := false
var active_entities: Array = []

var entity_type_counts: Dictionary = {}
var behavior_event_counts: Dictionary = {}
var max_single_type_ratio := 0.0
var avg_active_entities_30s := 0.0
var untelegraphed_fail_count := 0

func _ready() -> void:
	_reset_game()

func _physics_process(delta: float) -> void:
	if test_mode:
		return
	_simulate_frame(delta)

func _simulate_frame(delta: float) -> void:
	if game_over:
		return
	elapsed += delta
	# Template intentionally has no gameplay logic.
	# TODO(game): implement world-event based scoring and fail conditions.
	_update_test_metrics()

func _reset_game() -> void:
	score = 0
	elapsed = 0.0
	game_over = false
	active_entities.clear()
	var m := MetricsTracker.reset_metric_trackers({}, [])
	entity_type_counts = m["entity_type_counts"]
	behavior_event_counts = m["behavior_event_counts"]
	max_single_type_ratio = float(m["max_single_type_ratio"])
	avg_active_entities_30s = float(m["avg_active_entities_30s"])
	untelegraphed_fail_count = int(m["untelegraphed_fail_count"])

func _update_test_metrics() -> void:
	var update := MetricsTracker.update_test_metrics(elapsed, active_entities, 0.0, 0, max_single_type_ratio)
	max_single_type_ratio = float(update["max_single_type_ratio"])
	avg_active_entities_30s = float(update["avg_active_entities_30s"])

# --- test hooks (interface stub for agents) ---
func enable_test_mode(enabled: bool) -> void:
	test_mode = enabled

func force_reset_for_test(test_seed: int) -> void:
	seed(test_seed)
	_reset_game()

func step_for_test(delta: float, action_a: bool, action_b: bool, action_c: bool) -> void:
	test_action_a = action_a
	test_action_b = action_b
	test_action_c = action_c
	_simulate_frame(delta)

func get_metrics() -> Dictionary:
	return {
		"score": score,
		"game_over": game_over,
		"elapsed": elapsed,
		"active_entities": active_entities.size(),
		"entity_type_counts": entity_type_counts.duplicate(true),
		"max_single_type_ratio": max_single_type_ratio,
		"behavior_event_counts": behavior_event_counts.duplicate(true),
		"avg_active_entities_30s": avg_active_entities_30s,
		"untelegraphed_fail_count": untelegraphed_fail_count,
	}

func step_for_test_dict(delta: float, inputs: Dictionary) -> void:
	var a := bool(inputs.get("action_a", false))
	var b := bool(inputs.get("action_b", false))
	var c := bool(inputs.get("action_c", false))
	step_for_test(delta, a, b, c)

func get_test_input_channels() -> Array:
	return [
		{"name": "action_a", "type": "bool"},
		{"name": "action_b", "type": "bool"},
		{"name": "action_c", "type": "bool"},
	]

func get_monotonous_policies() -> Array:
	return []

func get_exploration_policies() -> Array:
	return []

func set_wave_for_test(_target_phase: int) -> void:
	# TODO(game): apply phase/segment transition for test scenarios if needed.
	pass
