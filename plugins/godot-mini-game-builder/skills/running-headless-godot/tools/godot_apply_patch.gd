extends SceneTree

func _init() -> void:
	var dry_run := false
	var allow_delete := false
	var patch_path := ""
	for a in OS.get_cmdline_user_args():
		if a == "--dry-run":
			dry_run = true
		elif a == "--allow-delete":
			allow_delete = true
		elif patch_path == "":
			patch_path = a

	if patch_path == "":
		_die("usage: godot ... --script godot_apply_patch.gd -- <PATCH_JSON_PATH> [--dry-run] [--allow-delete]")
		return
	if not _is_abs_or_res(patch_path):
		_die("patch path must be absolute or res:// (no relative paths): ", patch_path)
		return

	var patch_v: Variant = _read_json(patch_path)
	if patch_v == null or typeof(patch_v) != TYPE_DICTIONARY:
		_die("patch JSON must be an object: ", patch_path)
		return
	var patch: Dictionary = patch_v

	var scene_path_v: Variant = patch.get("scene_path", "")
	if typeof(scene_path_v) != TYPE_STRING:
		_die("patch must include scene_path (string)")
		return
	var scene_path: String = scene_path_v
	if scene_path == "":
		_die("patch must include scene_path (string)")
		return
	if not _is_abs_or_res(scene_path):
		_die("scene_path must be absolute or res://: ", scene_path)
		return

	var ops_v: Variant = patch.get("operations", [])
	if typeof(ops_v) != TYPE_ARRAY:
		_die("operations must be an array")
		return
	var ops: Array = ops_v

	var packed := load(scene_path)
	if packed == null or not (packed is PackedScene):
		_die("failed to load PackedScene: ", scene_path)
		return

	var root := (packed as PackedScene).instantiate()
	if root == null:
		_die("failed to instantiate scene: ", scene_path)
		return

	var res: Dictionary = _apply_ops(root, ops, allow_delete)
	if res["err"] != OK:
		root.free()
		quit(1)
		return
	var applied: int = res["applied"]

	if dry_run:
		print("dry-run ok ops=", applied)
		root.free()
		quit(0)
		return

	var bak: String = scene_path + ".bak"
	if _copy_file(scene_path, bak) != OK:
		root.free()
		_die("failed to create backup: ", bak)
		return

	var out := PackedScene.new()
	if out.pack(root) != OK:
		_copy_file(bak, scene_path)
		root.free()
		_die("PackedScene.pack failed")
		return
	if ResourceSaver.save(out, scene_path) != OK:
		_copy_file(bak, scene_path)
		root.free()
		_die("ResourceSaver.save failed: ", scene_path)
		return

	print("ok ops=", applied, " scene=", scene_path)
	root.free()
	quit(0)

func _die(msg: String, ctx: Variant = null) -> void:
	if ctx == null:
		printerr(msg)
	else:
		printerr(msg, ctx)
	quit(1)

func _is_abs_or_res(p: String) -> bool:
	return p.begins_with("res://") or p.begins_with("/") or (p.length() >= 3 and p.substr(1, 1) == ":" and (p.substr(2, 1) == "/" or p.substr(2, 1) == "\\"))

func _read_json(path: String) -> Variant:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		printerr("failed to open JSON: ", path)
		return null
	var v: Variant = JSON.parse_string(f.get_as_text())
	if v == null:
		printerr("failed to parse JSON: ", path)
	return v

func _node_from(root: Node, p: String) -> Node:
	return root if (p == "" or p == ".") else root.get_node_or_null(NodePath(p))

func _fail(applied: int, err: int, msg: String, ctx: Variant = null) -> Dictionary:
	if ctx == null:
		printerr(msg)
	else:
		printerr(msg, ctx)
	return {"err": err, "applied": applied}

func _apply_ops(root: Node, ops: Array, allow_delete: bool) -> Dictionary:
	var applied := 0
	for opv in ops:
		if typeof(opv) != TYPE_DICTIONARY:
			return _fail(applied, ERR_INVALID_DATA, "op must be an object: ", opv)
		var op := opv as Dictionary
		var kind := str(op.get("op", ""))

		if kind == "set_property":
			var n := _node_from(root, str(op.get("node", "")))
			if n == null:
				return _fail(applied, ERR_DOES_NOT_EXIST, "node not found: ", op.get("node", ""))
			var prop := str(op.get("property", ""))
			if prop == "":
				return _fail(applied, ERR_INVALID_PARAMETER, "property required")
			var value: Variant = op.get("value", null)
			if op.has("value_variant"):
				value = str_to_var(str(op.get("value_variant")))
			n.set(prop, value)
			applied += 1
			continue

		if kind == "rename_node":
			var n2 := _node_from(root, str(op.get("node", "")))
			if n2 == null:
				return _fail(applied, ERR_DOES_NOT_EXIST, "node not found: ", op.get("node", ""))
			var new_name := str(op.get("new_name", ""))
			if new_name == "":
				return _fail(applied, ERR_INVALID_PARAMETER, "new_name required")
			n2.name = new_name
			applied += 1
			continue

		if kind == "add_child_scene":
			var parent := _node_from(root, str(op.get("parent", "")))
			if parent == null:
				return _fail(applied, ERR_DOES_NOT_EXIST, "parent not found: ", op.get("parent", ""))
			var child_scene := str(op.get("child_scene", ""))
			if not _is_abs_or_res(child_scene):
				return _fail(applied, ERR_INVALID_PARAMETER, "child_scene must be absolute or res://: ", child_scene)
			var child_packed := load(child_scene)
			if child_packed == null or not (child_packed is PackedScene):
				return _fail(applied, ERR_CANT_OPEN, "failed to load child PackedScene: ", child_scene)
			var child := (child_packed as PackedScene).instantiate()
			if child == null:
				return _fail(applied, ERR_CANT_CREATE, "failed to instantiate child: ", child_scene)
			var name_override := str(op.get("name", ""))
			if name_override != "":
				var existing := parent.get_node_or_null(NodePath(name_override))
				if existing != null:
					parent.remove_child(existing)
					existing.free()
				child.name = name_override
			parent.add_child(child)
			child.owner = root # persist child while preserving nested instance ownership
			applied += 1
			continue

		if kind == "delete_node":
			if not allow_delete:
				return _fail(applied, ERR_UNAUTHORIZED, "delete_node is disabled (pass --allow-delete)")
			var nd := _node_from(root, str(op.get("node", "")))
			if nd == null:
				return _fail(applied, ERR_DOES_NOT_EXIST, "node not found: ", op.get("node", ""))
			if nd == root:
				return _fail(applied, ERR_INVALID_PARAMETER, "refusing to delete root node")
			var pd := nd.get_parent()
			if pd != null:
				pd.remove_child(nd)
			nd.free()
			applied += 1
			continue

		return _fail(applied, ERR_INVALID_PARAMETER, "unknown op: ", kind)

	return {"err": OK, "applied": applied}

func _copy_file(src: String, dst: String) -> int:
	if FileAccess.file_exists(dst):
		var rm_err := DirAccess.remove_absolute(dst)
		if rm_err != OK:
			return rm_err
	return DirAccess.copy_absolute(src, dst)
