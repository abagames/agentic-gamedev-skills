#!/usr/bin/env python3
"""Validate a composition or generated plugin bundle artifact."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from build import target_manifest, bundle_readme
from plugin_bundles import (BundleError, GENERATOR_VERSION, SLUG, SEMVER, artifact_inventory, composition_hash, directory_hash,
                            file_hash, generator_hash, read_json, source_commit,
                            source_tree_state, validate_composition, validate_schema_parity,
                            validate_skill_tree)


def validate_artifact(path: Path, composition: Path | None = None, repo: Path | None = None,
                      publishable: bool = False) -> None:
    if publishable and (composition is None or repo is None):
        raise BundleError("publishable validation requires --artifact, --composition, and --repo")
    actual_files = artifact_inventory(path)
    lock = read_json(path / "plugin-lock.json")
    allowed = {"lockVersion", "plugin", "pluginVersion", "sourceCommit", "sourceTreeState",
               "compositionHash", "licenseSha256", "generatorVersion", "generatorSha256",
               "target", "skills", "files"}
    unknown = sorted(set(lock) - allowed)
    if unknown:
        raise BundleError(f"lock: unknown field(s): {', '.join(unknown)}")
    if set(lock) != allowed or type(lock["lockVersion"]) is not int or lock["lockVersion"] != 3:
        raise BundleError("lock: missing fields or unsupported lockVersion")
    for field, pattern in (("plugin", SLUG), ("pluginVersion", SEMVER), ("generatorVersion", SEMVER)):
        if not isinstance(lock[field], str) or not pattern.fullmatch(lock[field]):
            raise BundleError(f"lock: invalid {field}")
    if lock["sourceTreeState"] not in ("clean", "dirty") or not isinstance(lock["sourceCommit"], str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", lock["sourceCommit"]):
        raise BundleError("lock: invalid source provenance")
    for field in ("compositionHash", "licenseSha256", "generatorSha256"):
        if not isinstance(lock[field], str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", lock[field]):
            raise BundleError(f"lock: invalid {field}")
    if not isinstance(lock["files"], dict) or lock["files"] != actual_files:
        raise BundleError("artifact: payload file inventory/hash/mode mismatch")
    target = lock["target"]
    if target not in ("codex", "claude"):
        raise BundleError("lock: invalid target")
    manifest = path / (".codex-plugin" if target == "codex" else ".claude-plugin") / "plugin.json"
    data = read_json(manifest)
    if data.get("name") != lock["plugin"] or data.get("version") != lock["pluginVersion"]:
        raise BundleError("manifest identity does not match lock")
    if not (path / "LICENSE").is_file():
        raise BundleError("artifact: missing LICENSE")
    if lock["licenseSha256"] != f"sha256:{file_hash(path / 'LICENSE')}":
        raise BundleError("artifact: LICENSE hash mismatch")
    entries = lock["skills"]
    if not isinstance(entries, list) or not entries:
        raise BundleError("lock: skills must be a non-empty array")
    names = [entry.get("name") for entry in entries if isinstance(entry, dict)]
    actual = sorted(p.name for p in (path / "skills").iterdir() if p.is_dir())
    if (len(names) != len(entries) or any(not isinstance(name, str) or not SLUG.fullmatch(name) for name in names)
            or len(names) != len(set(names)) or sorted(names) != actual):
        raise BundleError("artifact: duplicate, missing, or untracked skill directory")
    for entry in entries:
        if set(entry) != {"name", "directorySha256"}:
            raise BundleError("lock skill: unknown or missing field")
        skill = path / "skills" / entry["name"]
        validate_skill_tree(skill)
        if entry["directorySha256"] != f"sha256:{directory_hash(skill)}":
            raise BundleError(f"artifact: skill hash mismatch: {entry['name']}")
    root_files = {"LICENSE", "README.md", manifest.relative_to(path).as_posix()}
    for name in actual_files:
        if name not in root_files and not any(name.startswith(f"skills/{skill}/") for skill in names):
            raise BundleError(f"artifact: unexpected payload path: {name}")
    if not root_files.issubset(actual_files):
        raise BundleError("artifact: missing required payload files")
    if (composition is None) != (repo is None):
        raise BundleError("artifact: --composition and --repo must be supplied together")
    if composition is not None and repo is not None:
        composition_data = read_json(composition)
        validate_schema_parity(repo / "plugin-bundles" / "schema.json")
        validate_composition(composition_data, repo)
        expected = {
            "plugin": composition_data["slug"], "pluginVersion": composition_data["version"],
            "compositionHash": f"sha256:{composition_hash(composition)}",
            "licenseSha256": f"sha256:{file_hash(repo / 'LICENSE')}",
            "generatorVersion": GENERATOR_VERSION, "generatorSha256": f"sha256:{generator_hash()}",
            "sourceCommit": source_commit(repo),
            "sourceTreeState": source_tree_state(repo, composition, composition_data["skills"]),
        }
        for field, value in expected.items():
            if lock[field] != value:
                raise BundleError(f"artifact: effective input mismatch: {field}")
        if publishable and lock["sourceTreeState"] != "clean":
            raise BundleError("publishable validation requires clean committed effective inputs")
        if lock["target"] not in composition_data["targets"]:
            raise BundleError("artifact: target is not enabled by composition")
        if data != target_manifest(composition_data, lock["target"]):
            raise BundleError("artifact: target manifest does not match effective composition")
        if (path / "README.md").read_text(encoding="utf-8") != bundle_readme(composition_data, target):
            raise BundleError("artifact: README does not match effective composition")
        expected_names = composition_data["skills"]
        if names != expected_names:
            raise BundleError("artifact: skill order/membership does not match composition")
        for entry in entries:
            canonical = repo / ".agents" / "skills" / entry["name"]
            if entry["directorySha256"] != f"sha256:{directory_hash(canonical)}":
                raise BundleError(f"artifact: canonical skill mismatch: {entry['name']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--composition", type=Path)
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--publishable", action="store_true")
    args = parser.parse_args()
    try:
        if not args.artifact and not args.composition:
            parser.error("one of --composition or --artifact is required")
        if args.publishable and not (args.artifact and args.composition and args.repo):
            parser.error("--publishable requires --artifact, --composition, and --repo")
        if not args.artifact:
            repo = (args.repo or Path(__file__).resolve().parents[2]).resolve()
            validate_schema_parity(repo / "plugin-bundles" / "schema.json")
            validate_composition(read_json(args.composition), repo)
        else:
            validate_artifact(args.artifact.resolve(), args.composition.resolve() if args.composition else None,
                              args.repo.resolve() if args.repo else None, args.publishable)
    except (BundleError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
