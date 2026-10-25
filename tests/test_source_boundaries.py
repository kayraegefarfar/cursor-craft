"""Pre-read boundary regressions; synthetic fixtures only."""
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_package import validate
from check_installation import checked_path


class SourceBoundaryTests(unittest.TestCase):
    def test_required_manifest_link_rejected_before_any_content_read(self):
        # Exercise the pre-read ordering even on hosts without symlink privilege.
        original = Path.lstat
        target = ROOT / '.cursor-plugin/plugin.json'
        def linked_metadata(path):
            if path == target:
                info = original(path)
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return original(path)
        with patch.object(Path, 'lstat', linked_metadata), \
                patch.object(Path, 'read_text', side_effect=AssertionError('content read')), \
                patch.object(Path, 'read_bytes', side_effect=AssertionError('content read')):
            self.assertTrue(any('Symlink forbidden' in error for error in validate(ROOT)))

    def test_oversized_file_rejected_before_content_read(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / 'large.md').write_bytes(b'x' * 500_001)
            with patch.object(Path, 'read_text', side_effect=AssertionError('content read')):
                self.assertTrue(any('large' in error for error in validate(root)))

    def test_real_windows_junction_rejected_before_content_read(self):
        if os.name != 'nt':
            self.skipTest('Windows junction test; POSIX runs the real symlink tests')
        with TemporaryDirectory() as td:
            root = Path(td) / 'repo'
            outside = Path(td) / 'outside'
            root.mkdir()
            outside.mkdir()
            (outside / 'private.md').write_text('Synthetic private fixture')
            junction = root / 'linked'
            # Fixed command syntax, environment variables carry only fixture paths.
            env = dict(os.environ, CRAFT_LINK=str(junction), CRAFT_TARGET=str(outside))
            result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command',
                'New-Item -ItemType Junction -Path $env:CRAFT_LINK -Target $env:CRAFT_TARGET | Out-Null'],
                env=env, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            try:
                with patch.object(Path, 'read_text', side_effect=AssertionError('content read')), \
                        patch.object(Path, 'read_bytes', side_effect=AssertionError('content read')):
                    self.assertTrue(any('Symlink forbidden' in error for error in validate(root)))
                    with self.assertRaisesRegex(ValueError, 'reparse'):
                        checked_path(junction / 'private.md')
            finally:
                # Remove the link itself, never its target tree.
                junction.rmdir()
            self.assertTrue((outside / 'private.md').exists())


if __name__ == '__main__':
    unittest.main()
