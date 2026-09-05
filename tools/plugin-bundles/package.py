#!/usr/bin/env python3
"""Build, validate, and round-trip the complete local plugin release set without publishing."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

from build import build
from plugin_bundles import BundleError, dump_json, file_hash, read_json
from validate import validate_artifact


def write_archive(artifact: Path, destination: Path) -> None:
    # Fixed timestamps/order and normalized modes keep packaging independent of mtime.
    with zipfile.ZipFile(destination, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(artifact.rglob('*')):
            if not path.is_file():
                continue
            entry = zipfile.ZipInfo(f'{artifact.name}/{path.relative_to(artifact).as_posix()}', (1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (0o100755 if path.stat().st_mode & 0o111 else 0o100644) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, path.read_bytes())


def unpack_own_archive(archive_path: Path, destination: Path) -> Path:
    # Only consume archives created above, while checking their path and CRC contract.
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise BundleError('archive CRC check failed')
        roots = set()
        for entry in archive.infolist():
            path = Path(entry.filename)
            if path.is_absolute() or '..' in path.parts or len(path.parts) < 2:
                raise BundleError('archive contains an unsafe path')
            roots.add(path.parts[0])
            output = destination / path
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(archive.read(entry))
            output.chmod(0o755 if (entry.external_attr >> 16) & 0o111 else 0o644)
        if len(roots) != 1:
            raise BundleError('archive must contain exactly one plugin root')
        return destination / roots.pop()


def platform_check(command: list[str], environment: dict[str, str]) -> str:
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            env=environment, timeout=60)
    if result.returncode:
        raise BundleError(f'platform validation failed ({command[0]}):\n{result.stdout}')
    return result.stdout.strip()


def package(repo: Path, output: Path, codex_validator: Path | None, claude_validator: str | None,
            publishable: bool = False) -> None:
    if output.exists():
        raise BundleError('package output already exists; choose a fresh directory')
    compositions = sorted(p for p in (repo / 'plugin-bundles').glob('*.json') if p.name != 'schema.json')
    if len(compositions) != 6:
        raise BundleError('release set must contain exactly six compositions')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.package-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'release'
        stage.mkdir()
        archives = stage / 'archives'
        archives.mkdir()
        report = {'profile': 'committed-candidate' if publishable else 'working-tree-candidate',
                  'published': False, 'strictReproducibleRelease': False, 'artifacts': []}
        with tempfile.TemporaryDirectory(prefix='plugin-package-check-') as verify:
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', CLAUDE_CONFIG_DIR=str(Path(verify) / 'claude-config'))
            for composition in compositions:
                data = read_json(composition)
                if composition.stem != data['slug']:
                    raise BundleError('composition filename must match its slug')
                for target in sorted(data['targets']):
                    artifact = build(repo, composition, target, stage / 'trees', 'publishable' if publishable else 'local')
                    validate_artifact(artifact, composition, repo, publishable)
                    archive = archives / f"{data['slug']}-{data['version']}-{target}.zip"
                    write_archive(artifact, archive)
                    restored = unpack_own_archive(archive, Path(verify) / target / data['slug'])
                    validate_artifact(restored, composition, repo, publishable)
                    official = {'status': 'not-run', 'reason': f'No {target} validator supplied'}
                    if target == 'codex' and codex_validator:
                        command = [sys.executable, str(codex_validator), str(restored)]
                        official = {'status': 'passed', 'validator': str(codex_validator),
                                    'validatorSha256': file_hash(codex_validator),
                                    'output': platform_check(command, environment)}
                    elif target == 'claude' and claude_validator:
                        official = {'status': 'passed', 'validator': claude_validator,
                                    'version': platform_check([claude_validator, '--version'], environment),
                                    'output': platform_check([claude_validator, 'plugin', 'validate', '--strict', str(restored)], environment)}
                    lock = read_json(artifact / 'plugin-lock.json')
                    report['artifacts'].append({'plugin': data['slug'], 'displayName': data['targets'][target]['displayName'],
                                                'version': data['version'], 'target': target,
                                                'skillCount': len(data['skills']), 'fileCount': len(lock['files']) + 1,
                                                'sourceCommit': lock['sourceCommit'], 'sourceTreeState': lock['sourceTreeState'],
                                                'archive': archive.relative_to(stage).as_posix(), 'sha256': file_hash(archive),
                                                'lockSha256': file_hash(artifact / 'plugin-lock.json'),
                                                'baseline': 'passed', 'archiveRoundTrip': 'passed',
                                                'platformValidation': official})
                    print(f"ok: {target}/{data['slug']} ({len(data['skills'])} skills); platform={official['status']}", flush=True)
        dump_json(stage / 'validation-report.json', report)
        (stage / 'SHA256SUMS').write_text(''.join(f"{entry['sha256']}  {entry['archive']}\n" for entry in report['artifacts']), encoding='utf-8')
        stage.rename(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path, required=True, help='New directory; existing results are never overwritten')
    parser.add_argument('--codex-validator', type=Path, help='plugin-creator/scripts/validate_plugin.py')
    parser.add_argument('--claude-validator', help='Path to Claude Code CLI, e.g. claude')
    parser.add_argument('--publishable', action='store_true', help='Require clean effective inputs (not a strict reproducibility claim)')
    args = parser.parse_args()
    try:
        package(args.repo.resolve(), args.output.resolve(), args.codex_validator.resolve() if args.codex_validator else None,
                args.claude_validator, args.publishable)
    except (BundleError, OSError, subprocess.TimeoutExpired) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1
    print(args.output.resolve())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
