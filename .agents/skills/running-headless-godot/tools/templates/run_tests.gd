extends SceneTree

var _failures := 0

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	# Replace this placeholder with project-specific logic tests.
	_assert_true(true, "replace with a real test")

	if _failures > 0:
		printerr("tests failed: ", _failures)
		quit(1)
		return

	print("tests passed")
	quit(0)

func _assert_true(condition: bool, message: String) -> void:
	if condition:
		return
	_failures += 1
	printerr("assert failed: ", message)
