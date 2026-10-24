#!/usr/bin/env python3
"""Read-only, bounded verification of Cursor Craft source ZIP; never extracts files.

This verifies ZIP structure, per-file hashes and archive integrity. It is not
proof of publisher identity, authenticity, or Cursor runtime behavior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
import zipfile
from pathlib import Path
from archive_security import (MAX_ENTRIES, MAX_ENTRY_SIZE, MAX_TOTAL_SIZE,
                              validate_relative_name)

PREFIX = 'cursor-craft/'
HASH_FILE = PREFIX + 'SOURCE-MANIFEST.sha256'


def verify(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size > MAX_TOTAL_SIZE:
        raise ValueError('Archive missing or exceeds maximum compressed size')
    try:
        with zipfile.ZipFile(path) as archive:
            entries = archive.infolist()
            if not 2 <= len(entries) <= MAX_ENTRIES:
                raise ValueError('Unexpected archive entry count')
            names: set[str] = set()
            hashes: dict[str, str] = {}
            total_size = 0
            manifest_bytes = None
            for item in entries:
                name = item.filename
                if item.is_dir() or not name.startswith(PREFIX):
                    raise ValueError('Non-file or non-rooted archive entry')
                relative = name[len(PREFIX):]
                path_error = validate_relative_name(relative)
                if path_error:
                    raise ValueError(f'Unsafe archive path: {relative!r}: {path_error}')
                folded = relative.casefold()
                if folded in names:
                    raise ValueError(f'Duplicate or Windows-colliding entry: {relative}')
                names.add(folded)
                if item.flag_bits & 1:
                    raise ValueError('Encrypted archives are unsupported')
                mode = item.external_attr >> 16
                if item.create_system == 3 and stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                    raise ValueError(f'Nonregular/symlink entry: {relative}')
                if item.file_size > MAX_ENTRY_SIZE:
                    raise ValueError('Oversized archive entry')
                total_size += item.file_size
                if total_size > MAX_TOTAL_SIZE:
                    raise ValueError('Archive expanded-size limit exceeded')
                # Bounded per-file read, verifies CRC and actual content hash.
                with archive.open(item, 'r') as fp:
                    data = fp.read(MAX_ENTRY_SIZE + 1)
                    if len(data) != item.file_size or fp.read(1):
                        raise ValueError('Archive content/size mismatch')
                if name == HASH_FILE:
                    manifest_bytes = data
                else:
                    hashes[relative] = hashlib.sha256(data).hexdigest()
            if manifest_bytes is None:
                raise ValueError('Missing SOURCE-MANIFEST.sha256')
            try:
                lines = manifest_bytes.decode('utf-8').splitlines()
            except UnicodeError as exc:
                raise ValueError('Invalid UTF-8 hash manifest') from exc
            declared: dict[str, str] = {}
            for line in lines:
                if len(line) < 67 or line[64:66] != '  ':
                    raise ValueError('Malformed hash manifest line')
                digest, name = line[:64], line[66:]
                if len(digest) != 64 or any(ch not in '0123456789abcdef' for ch in digest):
                    raise ValueError('Invalid SHA-256 hex digest')
                if validate_relative_name(name) or name in declared:
                    raise ValueError('Invalid or duplicated hash manifest name')
                declared[name] = digest
            if declared != hashes:
                raise ValueError('Archive content does not match hash manifest')
            return {
                'archive_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'file_count': len(hashes),
                'integrity_verified': True,
                'runtime_verified': False,
                'publisher_authenticated': False,
            }
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile, EOFError) as exc:
        raise ValueError(f'Unreadable/damaged ZIP: {exc}') from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.archive), indent=2))
    except ValueError as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
