"""Shared portable path safety checks for source packaging and archive verification."""
from __future__ import annotations

import re
from pathlib import PurePosixPath

WINDOWS_DEVICES = frozenset({'CON', 'PRN', 'AUX', 'NUL'} | {f'{x}{n}' for x in ('COM', 'LPT') for n in range(1, 10)})
MAX_ENTRY_SIZE = 500_000
MAX_ENTRIES = 200
MAX_TOTAL_SIZE = 6_000_000


def validate_relative_name(name: str) -> str | None:
    """Reject dangerous/ambiguous path components across Windows, macOS, Linux.

    Input uses slash-separated paths relative to repository root (no extraction).
    """
    if not isinstance(name, str) or not name or '\\' in name or '\x00' in name:
        return 'invalid path separator or empty path'
    if name.startswith('/') or re.match(r'^[A-Za-z]:', name) or '//' in name:
        return 'absolute, drive or malformed path'
    parts = name.split('/')
    if any(p in ('', '.', '..') for p in parts):
        return 'path traversal or noncanonical path'
    if len(name) > 300:
        return 'path too long'
    for p in parts:
        if len(p) > 120 or p.endswith((' ', '.')):
            return 'Windows-incompatible component'
        if re.search(r'[<>:"|?*\x00-\x1f]', p):
            return 'Windows-invalid character'
        if p.split('.')[0].upper() in WINDOWS_DEVICES:
            return 'reserved Windows device name'
    if PurePosixPath(name).as_posix() != name:
        return 'noncanonical path'
    return None
