#!/usr/bin/env python3
"""Non-overwriting, reproducible source ZIP packager; no installations."""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from archive_security import validate_relative_name  # noqa: E402
from validate_package import validate  # noqa: E402

EXCLUDED = frozenset({'.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'dist'})
FIXED_DATE = (2026, 10, 24, 0, 0, 0)


def _add(archive: ZipFile, relative: str, data: bytes) -> None:
    info = ZipInfo('cursor-craft/' + relative, FIXED_DATE)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    info.create_system = 3
    archive.writestr(info, data, compress_type=ZIP_DEFLATED, compresslevel=9)


def assemble(root: Path, output: Path) -> str:
    problems = validate(root)
    if problems:
        raise ValueError('Preflight failed:\n' + '\n'.join(problems))
    if output.resolve().is_relative_to(root.resolve()):
        raise ValueError('Output must be OUTSIDE repository to prevent self-inclusion')
    if output.exists() or output.is_symlink():
        raise FileExistsError('Refusing to overwrite an existing output or symlink')
    files = sorted(p for p in root.rglob('*') if p.is_file() and
                   p.relative_to(root).as_posix() != 'SOURCE-MANIFEST.sha256' and
                   not any(part in EXCLUDED for part in p.relative_to(root).parts))
    file_data = []
    hashes = []
    for file in files:
        rel = file.relative_to(root).as_posix()
        if validate_relative_name(rel):
            raise ValueError(f'Unsafe source path: {rel}')
        data = file.read_bytes()
        file_data.append((rel, data))
        hashes.append(f'{hashlib.sha256(data).hexdigest()}  {rel}')
    manifest = ('\n'.join(hashes) + '\n').encode('utf-8')
    output.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.cursor-craft-', suffix='.tmp',
                                         dir=output.parent, delete=False) as tmp:
            temp_path = Path(tmp.name)
        with ZipFile(temp_path, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for rel, data in file_data:
                _add(archive, rel, data)
            _add(archive, 'SOURCE-MANIFEST.sha256', manifest)
        # Hard-link only if the named output does not exist: no race-prone replace.
        # Filesystem may not support hard links; exclusive create is the safe fallback.
        try:
            os.link(temp_path, output)
        except (OSError, NotImplementedError):
            with output.open('xb') as dst, temp_path.open('rb') as src:
                try:
                    shutil.copyfileobj(src, dst)
                except BaseException:
                    dst.close()
                    output.unlink(missing_ok=True)
                    raise
        return hashlib.sha256(output.read_bytes()).hexdigest()
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New ZIP path outside repository; existing file is never overwritten')
    args = parser.parse_args()
    try:
        digest = assemble(ROOT, args.output)
    except (OSError, ValueError) as exc:
        print('ERROR:', exc, file=sys.stderr)
        return 1
    print(f'Source ZIP: {args.output}')
    print(f'SHA256: {digest}')
    print('Offline source validation only; this build does not verify Cursor runtime.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
