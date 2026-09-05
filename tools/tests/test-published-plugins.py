#!/usr/bin/env python3
"""Mutation regressions for the tracked distribution (no host or account needed)."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools/plugin-bundles"))
from plugin_bundles import BundleError, artifact_inventory
from published import CATALOGS, LINEUP, published


class PublishedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        shutil.copytree(REPO / "plugin-bundles", self.repo / "plugin-bundles")
        shutil.copyfile(REPO / "LICENSE", self.repo / "LICENSE")
        # Small six-plugin fixture: preserve real composition metadata; replace payloads.
        for composition in (self.repo / "plugin-bundles").glob("*.json"):
            if composition.name == "schema.json":
                continue
            data = json.loads(composition.read_text())
            data["skills"] = ["fixture-skill"]
            composition.write_text(json.dumps(data))
        skill = self.repo / ".agents/skills/fixture-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text('---\nname: fixture-skill\ndescription: "Tests a fixture. Use in tests."\n---\n# Fixture\n')
        (skill / "run.sh").write_text("#!/bin/sh\nexit 0\n")
        (skill / "run.sh").chmod(0o755)
        published(self.repo, write=True)
        self.plugin = self.repo / "plugins" / LINEUP[0]

    def reject(self):
        with self.assertRaises((BundleError, OSError)):
            published(self.repo)

    def test_deterministic_without_git_and_repairs_known_payload(self):
        before = artifact_inventory(self.plugin)
        published(self.repo)
        (self.plugin / "README.md").write_text("stale")
        self.reject()
        published(self.repo, write=True)
        self.assertEqual(before, artifact_inventory(self.plugin))
        published(self.repo, write=True)
        self.assertEqual(before, artifact_inventory(self.plugin))

    def test_missing_extra_and_renamed_roots(self):
        self.plugin.rename(self.repo / "plugins/renamed")
        self.reject()
        with self.assertRaises(BundleError):
            published(self.repo, write=True)
        (self.repo / "plugins/renamed").rename(self.plugin)
        shutil.rmtree(self.plugin)
        self.reject()

    def test_payload_file_membership_bytes_and_modes(self):
        for relative in ("README.md", "LICENSE", "skills/fixture-skill/SKILL.md", "skills/fixture-skill/run.sh"):
            with self.subTest(relative=relative):
                path = self.plugin / relative
                content, mode = path.read_bytes(), path.stat().st_mode
                path.write_bytes(content + b"changed")
                self.reject()
                path.write_bytes(content)
                path.chmod(0o644 if mode & 0o111 else 0o755)
                self.reject()
                path.chmod(mode)
                path.unlink()
                self.reject()
                path.write_bytes(content)
                path.chmod(mode)
        for relative in ("extra.txt", "plugin-lock.json", "skills/fixture-skill/extra.txt"):
            path = self.plugin / relative
            path.write_text("extra")
            self.reject()
            path.unlink()
        (self.plugin / "empty").mkdir()
        self.reject()

    def test_manifest_identity_version_and_metadata(self):
        for target in ("codex", "claude"):
            path = self.plugin / f".{target}-plugin/plugin.json"
            original = path.read_bytes()
            for field, value in (("name", "other"), ("version", "9.0.0"), ("description", "stale")):
                data = json.loads(original)
                data[field] = value
                path.write_text(json.dumps(data))
                self.reject()
            path.write_bytes(original)

    def test_all_catalogs_reject_membership_path_and_policy_drift(self):
        for relative in CATALOGS:
            path = self.repo / relative
            original = path.read_bytes()
            mutations = [lambda d: d["plugins"].pop(),
                         lambda d: d["plugins"].append(d["plugins"][0]),
                         lambda d: d.update(name="wrong")]
            for source in ("../outside", "./plugins/../../outside", "/tmp/outside", ".", "./plugins/missing", "./plugins/" + LINEUP[1]):
                mutations.append(lambda d, s=source: d["plugins"][0].update(source=s))
                if relative != CATALOGS[2]:
                    mutations.append(lambda d, s=source: d["plugins"][0]["source"].update(path=s))
            if relative != CATALOGS[2]:
                mutations.append(lambda d: d["plugins"][0]["policy"].update(installation="NOT_AVAILABLE"))
            for mutate in mutations:
                data = json.loads(original)
                mutate(data)
                path.write_text(json.dumps(data))
                self.reject()
            path.write_bytes(original)

    def test_symlinks_at_output_and_input_boundaries_preserve_destination(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        sentinel = outside / "sentinel"
        sentinel.write_text("untouched")
        for relative in ("plugins", f"plugins/{LINEUP[0]}", ".agents/plugins", CATALOGS[0],
                         ".agents/skills", "plugin-bundles", "LICENSE"):
            path = self.repo / relative
            saved = path.with_name(path.name + ".saved")
            path.rename(saved)
            path.symlink_to(outside)
            self.reject()
            with self.assertRaises(BundleError):
                published(self.repo, write=True)
            self.assertEqual(sentinel.read_text(), "untouched")
            path.unlink()
            saved.rename(path)
        (self.plugin / "escape").symlink_to(outside)
        self.reject()

    def test_changed_canonical_inputs_require_regeneration(self):
        for relative in (".agents/skills/fixture-skill/SKILL.md", "LICENSE"):
            path = self.repo / relative
            path.write_text(path.read_text() + "\nchanged\n")
            self.reject()
            published(self.repo, write=True)
        path = self.repo / "plugin-bundles" / f"{LINEUP[0]}.json"
        data = json.loads(path.read_text())
        data["version"] = "0.2.0"
        path.write_text(json.dumps(data))
        self.reject()
        published(self.repo, write=True)

    def test_wrong_composition_set_identity_and_targets(self):
        path = self.repo / "plugin-bundles" / f"{LINEUP[0]}.json"
        original = path.read_bytes()
        for mutation in (lambda d: d.update(slug="other"), lambda d: d["targets"].pop("claude")):
            data = json.loads(original)
            mutation(data)
            path.write_text(json.dumps(data))
            self.reject()
        path.write_bytes(original)
        extra = self.repo / "plugin-bundles/extra.json"
        extra.write_bytes(original)
        self.reject()
        extra.unlink()
        path.unlink()
        self.reject()


if __name__ == "__main__":
    unittest.main()
