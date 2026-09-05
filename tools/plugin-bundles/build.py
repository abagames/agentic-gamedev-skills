#!/usr/bin/env python3
"""Build self-contained Codex and Claude plugin bundle artifacts."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from plugin_bundles import (BundleError, GENERATOR_VERSION, composition_hash,
                            directory_hash, dump_json, file_hash, generator_hash,
                            artifact_inventory, inventory, read_json, source_commit, source_tree_state,
                            validate_composition, validate_schema_parity)


def copy_skill(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True)
    for path in inventory(source):
        relative = path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        target.chmod(0o755 if path.stat().st_mode & 0o111 else 0o644)


def target_manifest(data: dict, target: str) -> dict:
    info = data["targets"][target]
    if target == "codex":
        interface = {
            "displayName": info["displayName"],
            "shortDescription": info.get("shortDescription", data["description"]),
            "longDescription": data["description"],
            "developerName": data["author"]["name"],
            "category": info.get("category", "Developer Tools"),
            "capabilities": ["Interactive", "Write"]
        }
        interface["defaultPrompt"] = info.get("defaultPrompts") or [info["displayName"][:128]]
        manifest = {
            "name": data["slug"], "version": data["version"],
            "description": data["description"], "author": data["author"],
            "license": data.get("license", "MIT"),
            "keywords": data.get("keywords", []), "skills": "./skills/", "interface": interface
        }
        if "repository" in data:
            manifest["repository"] = data["repository"]
        return manifest
    return {
        "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
        "name": data["slug"], "displayName": info["displayName"],
        "version": data["version"], "description": data["description"],
        "author": data["author"], "skills": ["./skills/"],
        "license": data.get("license", "MIT"), "keywords": data.get("keywords", []),
        **({"repository": data["repository"]} if "repository" in data else {})
    }


def bundle_readme(data: dict, target: str) -> str:
    info = data["targets"][target]
    lines = [f"# {info['displayName']}", "", data["description"], "",
             f"Version: {data['version']} · Target: {target} · Publisher: {data['author']['name']}", "",
             "## Included skills", ""]
    lines.extend(f"- [{name}](skills/{name}/SKILL.md)" for name in data["skills"])
    lines.extend(["", "Each skill directory includes its supporting references, scripts, and assets.", "",
                  "## Requirements and use", "",
                  "Install this directory as a plugin through the target host. Keep the hidden manifest directory and the complete skills tree together.", "",
                  "Resolve skill-local paths against the installed SKILL.md directory, not the game project's working directory.", ""])
    lines.extend(f"- {item}" for item in data.get("requirements", []))
    lines.extend(["", "Tools, engines, model access, and optional companion skills are not installed by this package. Check each skill's prerequisites before use.", "",
                  "Shared skills may also appear in other bundles. Install the bundles you need and select the intended plugin when the host exposes duplicate skills.", "",
                  "## License", "", f"{data.get('license', 'MIT')}; see [LICENSE](LICENSE)."])
    if "repository" in data:
        lines.extend(["", f"Source and release instructions: {data['repository']}"])
    return "\n".join(lines) + "\n"


def build(repo: Path, composition: Path, target: str, output: Path, mode: str) -> Path:
    data = read_json(composition)
    validate_schema_parity(repo / "plugin-bundles" / "schema.json")
    validate_composition(data, repo)
    if target not in data["targets"]:
        raise BundleError(f"target {target!r} is not enabled by composition")
    artifact = output / target / data["version"] / data["slug"]
    for path in (output / target, artifact.parent, artifact):
        if path.is_symlink():
            raise BundleError(f"refusing symlinked output path: {path}")
    identity_existed = artifact.exists()
    state = source_tree_state(repo, composition, data["skills"])
    if mode == "publishable" and state != "clean":
        raise BundleError("publishable build requires clean committed effective inputs")
    if artifact.exists() and mode == "local":
        raise BundleError("artifact identity already exists; use a disposable output or --dev-overwrite")
    final_artifact = artifact
    artifact.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".build-", dir=artifact.parent) as temporary:
        artifact = Path(temporary) / data["slug"]
        _write_artifact(repo, composition, target, artifact, data, state)
        if identity_existed and mode == "publishable":
            if (artifact_inventory(final_artifact) != artifact_inventory(artifact) or
                    (final_artifact / "plugin-lock.json").read_bytes() != (artifact / "plugin-lock.json").read_bytes()):
                raise BundleError("publishable identity already exists with different effective content; bump version")
            return final_artifact
        if final_artifact.exists():
            shutil.rmtree(final_artifact)
        artifact.rename(final_artifact)
    return final_artifact


def _write_artifact(repo: Path, composition: Path, target: str, artifact: Path, data: dict, state: str) -> None:
    artifact.mkdir()
    hashes = {}
    for skill in data["skills"]:
        source = repo / ".agents" / "skills" / skill
        hashes[skill] = directory_hash(source)
        copy_skill(source, artifact / "skills" / skill)
    shutil.copyfile(repo / "LICENSE", artifact / "LICENSE")
    manifest_dir = ".codex-plugin" if target == "codex" else ".claude-plugin"
    dump_json(artifact / manifest_dir / "plugin.json", target_manifest(data, target))
    (artifact / "README.md").write_text(bundle_readme(data, target), encoding="utf-8")
    lock = {
        "lockVersion": 3, "plugin": data["slug"], "pluginVersion": data["version"],
        "sourceCommit": source_commit(repo), "compositionHash": f"sha256:{composition_hash(composition)}",
        "sourceTreeState": state, "licenseSha256": f"sha256:{file_hash(repo / 'LICENSE')}",
        "generatorVersion": GENERATOR_VERSION, "generatorSha256": f"sha256:{generator_hash()}", "target": target,
        "skills": [{"name": name, "directorySha256": f"sha256:{hashes[name]}"} for name in data["skills"]],
        "files": artifact_inventory(artifact)
    }
    dump_json(artifact / "plugin-lock.json", lock)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("composition", type=Path)
    parser.add_argument("--target", choices=("codex", "claude"), required=True)
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dev-overwrite", action="store_true")
    modes.add_argument("--publishable", action="store_true")
    args = parser.parse_args()
    try:
        mode = "publishable" if args.publishable else ("dev-overwrite" if args.dev_overwrite else "local")
        artifact = build(args.repo.resolve(), args.composition.resolve(), args.target, args.output.resolve(), mode)
    except (BundleError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(artifact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
