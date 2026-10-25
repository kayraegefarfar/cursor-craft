#!/usr/bin/env python3
"""Read-only inspection of explicitly supplied legacy Skill ZIP archives.

This checks directory names only, not descriptions or installed Cursor state.
No files are extracted; no paths on the host are scanned without CLI input.
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path, PurePosixPath
from archive_security import validate_relative_name

CANDIDATES = {
    'design-studio': {'ui', 'ux', 'frontend', 'accessibility', 'creative', 'browser-ui', 'motion', 'visual'},
    'rea-workflow': {'research', 'architecture', 'reverse', 'analysis', 'discovery', 'modernization', 'codebase'},
    'deep-quality-review': {'review', 'security', 'test', 'testing', 'release', 'quality', 'verification'},
    'task-handoff': {'handoff', 'memory', 'docs', 'documentation'},
}
SYNONYMS = {
    'frontend-implementation': {'frontend', 'ui'},
    'ui-and-accessibility': {'ui', 'accessibility'},
    'budget-handoff': {'handoff', 'budget'},
    'architecture-review': {'architecture', 'review'},
    'code-review': {'review', 'quality'},
    'engineering-research': {'research', 'analysis'},
    'research-and-verification': {'research', 'verification'},
    'browser-ui-ux': {'browser-ui', 'ui', 'ux'},
    'open-source-release': {'release'},
    'docs-and-handoff': {'docs', 'handoff'},
}


def audit(archives: list[Path]) -> dict[str, list[tuple[str, str, int]]]:
    scores: dict[str, list[tuple[str, str, int]]] = {k: [] for k in CANDIDATES}
    for archive in archives:
        if not archive.is_file() or archive.stat().st_size > 50_000_000:
            raise ValueError(f'Archive missing or >50 MB: {archive}')
        try:
            with zipfile.ZipFile(archive) as zf:
                items = zf.infolist()
                if len(items) > 2500:
                    raise ValueError(f'Too many entries in {archive.name}')
                for item in items:
                    if not item.filename.endswith('/SKILL.md') or item.file_size > 100_000:
                        continue
                    if validate_relative_name(item.orig_filename):
                        continue
                    path = PurePosixPath(item.filename)
                    skill_name = path.parent.name.lower()
                    if not re.fullmatch(r'[a-z0-9-]{2,80}', skill_name):
                        continue
                    # Names and metadata only; avoid exposure of arbitrary source content.
                    title_tokens = set(skill_name.split('-')) | SYNONYMS.get(skill_name, set())
                    for current, terms in CANDIDATES.items():
                        score = len(title_tokens & terms)
                        if skill_name == current:
                            score += 10
                        if score:
                            scores[current].append((archive.name, skill_name, score))
        except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
            raise ValueError(f'Unreadable ZIP {archive}: {exc}') from exc
    for name in scores:
        scores[name].sort(key=lambda item: (-item[2], item[0], item[1]))
    return scores


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archives', nargs='+', type=Path, help='Archive files explicitly selected by owner')
    args = parser.parse_args()
    try:
        result = audit(args.archives)
    except ValueError as exc:
        parser.error(str(exc))
    print('POTENTIAL OVERLAPS ONLY — filename-based; not proof of identical behavior or installed configuration.')
    for name, entries in result.items():
        print(f'\n{name}:')
        for archive, legacy, score in entries[:10]:
            print(f'  {archive}: {legacy} (keyword score {score})')
        if not entries:
            print('  no name-level overlap found')
    print('\nNo configuration was read from Cursor or modified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
