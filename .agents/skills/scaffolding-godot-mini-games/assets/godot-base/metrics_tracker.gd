extends RefCounted

# Template contract:
# - Keep the core KPI-facing keys stable.
# - Add game-specific counters under `custom_metrics` via helper functions below.
const CORE_METRIC_KEYS := {
	"entity_type_counts": true,
	"behavior_event_counts": true,
	"max_single_type_ratio": true,
	"avg_active_entities_30s": true,
	"active_entity_sample_sum": true,
	"active_entity_sample_frames": true,
	"untelegraphed_fail_count": true,
}

static func reset_metric_trackers(type_catalog: Dictionary, behavior_event_keys: Array) -> Dictionary:
	var entity_type_counts: Dictionary = {}
	for entity_type in type_catalog.keys():
		entity_type_counts[str(entity_type)] = 0
	var behavior_counts: Dictionary = {}
	for key in behavior_event_keys:
		behavior_counts[str(key)] = 0
	return {
		"entity_type_counts": entity_type_counts,
		"behavior_event_counts": behavior_counts,
		"max_single_type_ratio": 0.0,
		"avg_active_entities_30s": 0.0,
		"active_entity_sample_sum": 0.0,
		"active_entity_sample_frames": 0,
		"untelegraphed_fail_count": 0,
		"custom_metrics": {},
	}

static func _entity_type_key(entity: Variant) -> String:
	if typeof(entity) == TYPE_DICTIONARY:
		var d := entity as Dictionary
		if d.has("type"):
			return str(d["type"])
	return "default"

static func update_max_single_type_ratio(entities: Array, current_ratio: float) -> float:
	var active_total := entities.size()
	if active_total < 5:
		return current_ratio
	var active_counts: Dictionary = {}
	for entity in entities:
		var key := _entity_type_key(entity)
		active_counts[key] = int(active_counts.get(key, 0)) + 1
	var local_max := 0
	for count in active_counts.values():
		local_max = maxi(local_max, int(count))
	var ratio := float(local_max) / float(active_total)
	return ratio if ratio > current_ratio else current_ratio

static func update_test_metrics(elapsed_time: float, entities: Array, active_entity_sample_sum: float, active_entity_sample_frames: int, max_single_type_ratio: float) -> Dictionary:
	var next_ratio := update_max_single_type_ratio(entities, max_single_type_ratio)
	var next_sum := active_entity_sample_sum
	var next_frames := active_entity_sample_frames
	var next_avg := 0.0
	if elapsed_time <= 30.0:
		next_sum += float(entities.size())
		next_frames += 1
		if next_frames > 0:
			next_avg = next_sum / float(next_frames)
	return {
		"max_single_type_ratio": next_ratio,
		"active_entity_sample_sum": next_sum,
		"active_entity_sample_frames": next_frames,
		"avg_active_entities_30s": next_avg,
	}

static func record_spawned_entity(entity_type_counts: Dictionary, entity_type: String) -> void:
	var key := str(entity_type)
	entity_type_counts[key] = int(entity_type_counts.get(key, 0)) + 1

static func inc_behavior_event(behavior_event_counts: Dictionary, key: String) -> void:
	behavior_event_counts[key] = int(behavior_event_counts.get(key, 0)) + 1

static func inc_custom_metric(custom_metrics: Dictionary, key: String, amount: int = 1) -> void:
	var metric_key := str(key)
	custom_metrics[metric_key] = int(custom_metrics.get(metric_key, 0)) + amount

static func set_custom_metric(custom_metrics: Dictionary, key: String, value: Variant) -> void:
	custom_metrics[str(key)] = value

static func get_core_metric_keys() -> Dictionary:
	return CORE_METRIC_KEYS.duplicate(true)

static func is_event_telegraphed(_event_payload: Dictionary) -> bool:
	return true
