extends RefCounted

static func push_sample(playback: AudioStreamGeneratorPlayback, sample: float) -> bool:
	var v := clampf(sample, -1.0, 1.0)
	return playback.push_frame(Vector2(v, v))

static func sfx_envelope(t: float, duration: float, attack_ratio: float = 0.1, release_ratio: float = 0.45) -> float:
	if duration <= 0.0:
		return 0.0
	var attack_time: float = maxf(0.001, duration * attack_ratio)
	var release_time: float = maxf(0.001, duration * release_ratio)
	if t < attack_time:
		return t / attack_time
	if t > duration - release_time:
		return max(0.0, (duration - t) / release_time)
	return 1.0

static func sine(phase: float) -> float:
	return sin(phase * TAU)

static func square(phase: float, duty: float = 0.5) -> float:
	return 1.0 if fmod(phase, 1.0) < duty else -1.0

static func triangle(phase: float) -> float:
	var t := fmod(phase, 1.0)
	return 4.0 * absf(t - 0.5) - 1.0

static func noise(audio_rng: RandomNumberGenerator) -> float:
	return audio_rng.randf_range(-1.0, 1.0)
