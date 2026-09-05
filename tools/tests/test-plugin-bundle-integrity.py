#!/usr/bin/env python3
"""Regression probes for payload tampering, malformed inputs, and packaging."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tools/plugin-bundles'))
from build import build, target_manifest
from package import write_archive, unpack_own_archive
from plugin_bundles import BundleError, artifact_inventory, read_json, validate_composition
from validate import validate_artifact


class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.composition = REPO / 'plugin-bundles/godot-mini-game-builder.json'
        self.artifact = build(REPO, self.composition, 'codex', self.root / 'out', 'local')

    def assertRejected(self):
        with self.assertRaises(BundleError):
            validate_artifact(self.artifact)
        with self.assertRaises(BundleError):
            validate_artifact(self.artifact, self.composition, REPO)

    def test_valid_payload_and_archive_keep_bytes_modes_and_plugin_name(self):
        validate_artifact(self.artifact, self.composition, REPO)
        self.assertEqual(self.artifact.name, 'godot-mini-game-builder')
        archive = self.root / 'bundle.zip'
        write_archive(self.artifact, archive)
        restored = unpack_own_archive(archive, self.root / 'installed')
        validate_artifact(restored, self.composition, REPO)
        self.assertEqual(artifact_inventory(self.artifact), artifact_inventory(restored))
        # Verify mode flags in the actual archive, independent of the unpack helper.
        with zipfile.ZipFile(archive) as contents:
            for path in self.artifact.glob('skills/*/tools/*.sh'):
                entry = contents.getinfo(f'{self.artifact.name}/{path.relative_to(self.artifact)}')
                source = REPO / '.agents' / path.relative_to(self.artifact)
                self.assertEqual(bool((entry.external_attr >> 16) & 0o111), bool(source.stat().st_mode & 0o111))
        second = self.root / 'again.zip'
        write_archive(self.artifact, second)
        self.assertEqual(archive.read_bytes(), second.read_bytes())

    def test_manifest_tamper(self):
        path = self.artifact / '.codex-plugin/plugin.json'
        data = read_json(path); data['description'] = 'Changed'
        path.write_text(json.dumps(data))
        self.assertRejected()

    def test_extra_payload_files_and_empty_directory(self):
        for relative, is_dir in [('unexpected.txt', False), ('.codex-plugin/extra.json', False), ('empty', True)]:
            with self.subTest(relative=relative):
                path = self.artifact / relative
                if is_dir: path.mkdir()
                else: path.write_text('extra')
                self.assertRejected()
                if is_dir: path.rmdir()
                else: path.unlink()

    def test_symlinked_payload(self):
        path = self.artifact / 'extra'; path.symlink_to(self.root)
        self.assertRejected()

    def test_executable_mode_tamper(self):
        path = self.artifact / 'skills/scaffolding-godot-mini-games/SKILL.md'
        path.chmod(0o755)
        self.assertRejected()

    def test_full_validation_rejects_rehashed_manifest_tamper(self):
        path = self.artifact / '.codex-plugin/plugin.json'
        data = read_json(path); data['description'] = 'Changed'; path.write_text(json.dumps(data))
        lock = read_json(self.artifact / 'plugin-lock.json'); lock['files'] = artifact_inventory(self.artifact)
        (self.artifact / 'plugin-lock.json').write_text(json.dumps(lock))
        with self.assertRaisesRegex(BundleError, 'target manifest'):
            validate_artifact(self.artifact, self.composition, REPO)

    def test_publishable_cannot_skip_source_validation(self):
        with self.assertRaisesRegex(BundleError, 'requires'):
            validate_artifact(self.artifact, publishable=True)

    def test_malformed_fields_raise_validation_errors(self):
        base = read_json(self.composition)
        cases = [('schemaVersion', True), ('keywords', [{}]), ('skills', [[]]), ('requirements', [None])]
        for field, value in cases:
            with self.subTest(field=field):
                data = copy.deepcopy(base); data[field] = value
                with self.assertRaises(BundleError): validate_composition(data, REPO)
        data = copy.deepcopy(base); data['targets']['codex']['defaultPrompts'] = [{}]
        with self.assertRaises(BundleError): validate_composition(data, REPO)

    def test_optional_repository_omitted_and_default_prompt_present(self):
        data = read_json(self.composition); del data['repository']; del data['targets']['codex']['defaultPrompts']
        manifest = target_manifest(data, 'codex')
        self.assertNotIn('repository', manifest)
        self.assertTrue(manifest['interface']['defaultPrompt'])

    def test_existing_artifact_and_symlink_output_preserved(self):
        before = artifact_inventory(self.artifact)
        with self.assertRaises(BundleError):
            build(REPO, self.composition, 'codex', self.root / 'out', 'local')
        self.assertEqual(before, artifact_inventory(self.artifact))
        (self.root / 'linked').mkdir(); (self.root / 'linked/codex').symlink_to(self.root / 'out/codex')
        with self.assertRaisesRegex(BundleError, 'symlinked output'):
            build(REPO, self.composition, 'codex', self.root / 'linked', 'dev-overwrite')
        self.assertEqual(before, artifact_inventory(self.artifact))


if __name__ == '__main__':
    unittest.main()
