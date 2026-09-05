#!/usr/bin/env python3
"""Shared validation and deterministic inventory helpers for plugin bundles."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

GENERATOR_VERSION = "3.0.0"
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
ROOT_FIELDS = {"schemaVersion", "slug", "version", "description", "author", "repository", "license", "keywords", "requirements", "skills", "targets"}
AUTHOR_FIELDS = {"name", "url"}
TARGET_FIELDS = {"displayName", "shortDescription", "category", "defaultPrompts"}
TARGETS = {"codex", "claude"}
FORBIDDEN_PARTS = {".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", "coverage", "probe-output", "probe-outputs"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


class BundleError(ValueError):
    pass


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BundleError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BundleError(f"{path}: root must be an object")
    return value


def reject_unknown(value: dict, allowed: set[str], where: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise BundleError(f"{where}: unknown field(s): {', '.join(unknown)}")


def validate_composition(data: dict, repo: Path) -> None:
    reject_unknown(data, ROOT_FIELDS, "composition")
    required = {"schemaVersion", "slug", "version", "description", "author", "skills", "targets"}
    missing = sorted(required - set(data))
    if missing:
        raise BundleError(f"composition: missing field(s): {', '.join(missing)}")
    if type(data["schemaVersion"]) is not int or data["schemaVersion"] != 1:
        raise BundleError("composition: schemaVersion must be 1")
    slug = data["slug"]
    if not isinstance(slug, str) or len(slug) > 64 or not SLUG.fullmatch(slug):
        raise BundleError("composition: invalid slug")
    if not isinstance(data["version"], str) or not SEMVER.fullmatch(data["version"]):
        raise BundleError("composition: invalid strict semantic version")
    if not isinstance(data["description"], str) or not data["description"].strip():
        raise BundleError("composition: description must be non-empty")
    author = data["author"]
    if not isinstance(author, dict):
        raise BundleError("composition: author must be an object")
    reject_unknown(author, AUTHOR_FIELDS, "author")
    if not isinstance(author.get("name"), str) or not author["name"].strip():
        raise BundleError("author: name is required")
    if "url" in author and (not isinstance(author["url"], str) or not author["url"].startswith("https://")):
        raise BundleError("author: url must use https")
    for field in ("repository",):
        if field in data and (not isinstance(data[field], str) or not data[field].startswith("https://")):
            raise BundleError(f"composition: {field} must use https")
    if "license" in data and (not isinstance(data["license"], str) or not data["license"].strip()):
        raise BundleError("composition: license must be non-empty")
    for field in ("keywords", "requirements"):
        values = data.get(field, [])
        if (not isinstance(values, list) or
                any(not isinstance(value, str) or not value.strip() for value in values) or
                len(values) != len(set(values))):
            raise BundleError(f"composition: {field} must be unique non-empty strings")
    skills = data["skills"]
    if not isinstance(skills, list) or not skills:
        raise BundleError("composition: skills must be a non-empty array")
    if any(not isinstance(skill, str) for skill in skills):
        raise BundleError("composition: skill slugs must be strings")
    if len(skills) != len(set(skills)):
        raise BundleError("composition: duplicate skills")
    for skill in skills:
        if not isinstance(skill, str) or len(skill) > 64 or not SLUG.fullmatch(skill):
            raise BundleError(f"composition: invalid skill slug: {skill!r}")
        validate_skill_tree(repo / ".agents" / "skills" / skill)
    targets = data["targets"]
    if not isinstance(targets, dict) or not targets:
        raise BundleError("composition: targets must be a non-empty object")
    reject_unknown(targets, TARGETS, "targets")
    for name, target in targets.items():
        if not isinstance(target, dict):
            raise BundleError(f"targets.{name}: must be an object")
        reject_unknown(target, TARGET_FIELDS, f"targets.{name}")
        if not isinstance(target.get("displayName"), str) or not target["displayName"].strip():
            raise BundleError(f"targets.{name}: displayName is required")
        for field in ("shortDescription", "category"):
            if field in target and (not isinstance(target[field], str) or not target[field].strip()):
                raise BundleError(f"targets.{name}: {field} must be non-empty")
        prompts = target.get("defaultPrompts", [])
        if not isinstance(prompts, list) or any(not isinstance(p, str) or not p.strip() or len(p) > 128 for p in prompts):
            raise BundleError(f"targets.{name}: invalid default prompt")
        if len(prompts) > 3 or len(prompts) != len(set(prompts)):
            raise BundleError(f"targets.{name}: defaultPrompts must contain at most 3 unique strings")


def validate_schema_parity(schema_path: Path) -> None:
    """Guard the stdlib validator constants/constraints against schema drift."""
    schema = read_json(schema_path)
    props = schema.get("properties", {})
    if set(props) != ROOT_FIELDS or set(schema.get("required", [])) != {"schemaVersion", "slug", "version", "description", "author", "skills", "targets"}:
        raise BundleError("schema/runtime parity: root fields or required fields drifted")
    if props.get("slug", {}).get("pattern") != SLUG.pattern or props.get("slug", {}).get("maxLength") != 64:
        raise BundleError("schema/runtime parity: slug constraint drifted")
    if props.get("version", {}).get("pattern") != SEMVER.pattern:
        raise BundleError("schema/runtime parity: version constraint drifted")
    if set(props.get("author", {}).get("properties", {})) != AUTHOR_FIELDS:
        raise BundleError("schema/runtime parity: author fields drifted")
    target = schema.get("$defs", {}).get("target", {})
    if set(target.get("properties", {})) != TARGET_FIELDS or set(props.get("targets", {}).get("properties", {})) != TARGETS:
        raise BundleError("schema/runtime parity: target fields drifted")
    prompts = target.get("properties", {}).get("defaultPrompts", {})
    if prompts.get("maxItems") != 3 or prompts.get("items", {}).get("maxLength") != 128:
        raise BundleError("schema/runtime parity: prompt limits drifted")
    for node in (props.get("description", {}), props.get("license", {}),
                 props.get("keywords", {}).get("items", {}),
                 props.get("author", {}).get("properties", {}).get("name", {}),
                 target.get("properties", {}).get("displayName", {}),
                 target.get("properties", {}).get("shortDescription", {}),
                 target.get("properties", {}).get("category", {}), prompts.get("items", {})):
        if node.get("pattern") != r"\S":
            raise BundleError("schema/runtime parity: non-whitespace string constraint drifted")


def inventory(root: Path) -> list[Path]:
    if root.is_symlink() or not root.is_dir() or not (root / "SKILL.md").is_file():
        raise BundleError(f"missing skill or SKILL.md: {root}")
    result = []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = path.relative_to(root)
        if path.is_symlink():
            raise BundleError(f"symlink is not allowed: {root.name}/{rel}")
        if any(part in FORBIDDEN_PARTS for part in rel.parts) or path.suffix in FORBIDDEN_SUFFIXES:
            raise BundleError(f"cache, VCS, or probe output is not allowed: {root.name}/{rel}")
        if path.is_file():
            result.append(path)
        elif not path.is_dir():
            raise BundleError(f"special file is not allowed: {root.name}/{rel}")
    return result


def validate_skill_tree(root: Path) -> None:
    files = inventory(root)
    for path in files:
        if path.suffix.lower() not in {".md", ".markdown"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for raw in LINK.findall(text):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "skill://")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError as exc:
                raise BundleError(f"reference escapes skill directory: {path}: {raw}") from exc
            if not resolved.exists():
                raise BundleError(f"broken skill-local reference: {path}: {raw}")


def directory_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in inventory(root):
        rel = path.relative_to(root).as_posix().encode()
        content = path.read_bytes()
        digest.update(len(rel).to_bytes(8, "big"))
        digest.update(rel)
        digest.update(b"x" if path.stat().st_mode & 0o111 else b"-")
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def composition_hash(path: Path) -> str:
    data = read_json(path)
    canonical = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_inventory(root: Path) -> dict:
    """Hash every payload file and executable bit; reject extra empty directories too.

    The lock is excluded to avoid a self-hash cycle. This is consistency evidence,
    not a signature: full validation still needs trusted source inputs.
    """
    result = {}
    directories = set()
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise BundleError(f"artifact: symlink is not allowed: {rel}")
        if path.is_dir():
            directories.add(rel)
        elif path.is_file():
            if rel != "plugin-lock.json":
                result[rel] = {"sha256": file_hash(path), "executable": bool(path.stat().st_mode & 0o111)}
        else:
            raise BundleError(f"artifact: special file is not allowed: {rel}")
    parents = {p.as_posix() for name in result for p in PurePosixPath(name).parents if p.as_posix() != "."}
    if directories != parents:
        raise BundleError("artifact: unexpected empty directory")
    return result


def generator_hash() -> str:
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for name in ("build.py", "plugin_bundles.py"):
        content = (root / name).read_bytes()
        digest.update(name.encode() + b"\0" + content)
    return digest.hexdigest()


def source_commit(repo: Path) -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo, text=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise BundleError("cannot determine source commit") from exc


def source_tree_state(repo: Path, composition: Path, skills: list[str]) -> str:
    paths = [composition.resolve(), (repo / "LICENSE").resolve(),
             (Path(__file__).resolve().parent / "build.py").resolve(), Path(__file__).resolve()]
    paths.extend((repo / ".agents" / "skills" / skill).resolve() for skill in skills)
    rels = []
    for path in paths:
        try:
            rels.append(str(path.relative_to(repo.resolve())))
        except ValueError as exc:
            raise BundleError(f"effective input is outside repository: {path}") from exc
    try:
        result = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all", "--", *rels],
                                cwd=repo, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise BundleError("cannot determine effective-input tree state") from exc
    return "dirty" if result.stdout else "clean"


def dump_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
