extends SceneTree

func _init() -> void:
	var root := Node2D.new()
	root.name = "Main"
	root.set_script(load("res://main.gd"))

	var packed := PackedScene.new()
	var result := packed.pack(root)
	if result != OK:
		printerr("pack failed: ", result)
		quit(1)
		return

	var save_result := ResourceSaver.save(packed, "res://main.tscn")
	if save_result != OK:
		printerr("save failed: ", save_result)
		quit(1)
		return

	print("main.tscn created")
	quit(0)
