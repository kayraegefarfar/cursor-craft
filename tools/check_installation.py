#!/usr/bin/env python3
"""Compare an explicitly selected plugin copy; never install or launch Cursor."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 500_000
MAX_ENTRIES = 512


def checked_path(path: Path) -> Path:
    """Reject link/reparse ancestors before traversing the selected location."""
    path = Path(os.path.abspath(path))
    for component in reversed((path, *path.parents)):
        info = component.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('Symlinks and reparse points are not supported')
    return path


def inventory(root: Path, selections: tuple[str, ...]) -> dict[str, str]:
    root = checked_path(root)
    if not root.is_dir():
        raise ValueError('Selected root must be a directory')
    result: dict[str, str] = {}
    folded: set[str] = set()
    count = 0

    def visit(path: Path) -> None:
        nonlocal count
        count += 1
        if count > MAX_ENTRIES:
            raise ValueError('Selected tree exceeds the entry limit')
        checked_path(path)
        info = path.lstat()
        relative = path.relative_to(root).as_posix()
        if relative.casefold() in folded:
            raise ValueError('Case-insensitive path collision')
        folded.add(relative.casefold())
        if stat.S_ISDIR(info.st_mode):
            for child in sorted(path.iterdir()):
                visit(child)
        elif stat.S_ISREG(info.st_mode):
            if info.st_size > MAX_FILE_BYTES:
                raise ValueError('Selected file exceeds the size limit')
            with path.open('rb') as stream:
                data = stream.read(MAX_FILE_BYTES + 1)
            if len(data) > MAX_FILE_BYTES:
                raise ValueError('Selected file exceeds the size limit')
            result[relative] = hashlib.sha256(data).hexdigest()
        else:
            raise ValueError('Only regular files and directories are supported')

    for selection in selections:
        visit(root / selection)
    return result


def compare(source: Path, candidate: Path) -> dict:
    # Inspect only the documented installation payload, not source .git or docs.
    expected = inventory(source, ('.cursor-plugin/plugin.json', 'rules', 'skills', 'LICENSE'))
    required = {'rules/professional-core.mdc', 'skills/task-handoff/template.md'}
    required.update(f'skills/{name}/SKILL.md' for name in
                    ('design-studio', 'rea-workflow', 'deep-quality-review', 'task-handoff'))
    if not required <= expected.keys():
        raise ValueError('Source is missing required Cursor Craft payload files')
    candidate = checked_path(candidate)
    if not candidate.is_dir():
        raise ValueError('Candidate must be an existing directory')
    actual = inventory(candidate, tuple(p.name for p in sorted(candidate.iterdir())))
    missing = sorted(expected.keys() - actual.keys())
    extra = sorted(actual.keys() - expected.keys())
    changed = sorted(name for name in expected.keys() & actual.keys() if expected[name] != actual[name])
    identity = ''.join(f'{digest}  {name}\n' for name, digest in sorted(expected.items()))
    return {
        'schema_version': 1,
        'payload_matches': not (missing or extra or changed),
        'source_payload_sha256': hashlib.sha256(identity.encode('utf-8')).hexdigest(),
        'expected_file_count': len(expected),
        'candidate_file_count': len(actual),
        'missing': missing, 'changed': changed, 'extra': extra,
        'runtime_verified': False,
        'warning': 'File equality only. Cursor discovery, active plugin provenance, Skill routing and permissions require a real session.',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT, help='Reviewed source root (default: this repository)')
    parser.add_argument('--candidate', type=Path, required=True, help='Explicitly authorized plugin copy; no automatic global lookup')
    args = parser.parse_args()
    try:
        report = compare(args.source, args.candidate)
    except (OSError, ValueError):
        # OS exceptions can expose private absolute paths. Keep diagnostics local.
        parser.exit(2, 'ERROR: Cannot safely compare selected trees. Check existence, permissions, required source files, links/reparse points and size limits.\n')
    print(json.dumps(report, indent=2))
    return 0 if report['payload_matches'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
