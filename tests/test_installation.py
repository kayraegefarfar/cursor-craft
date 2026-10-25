"""Filesystem fixture tests, not Cursor runtime evidence."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from check_installation import checked_path, compare, inventory


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.candidate = Path(self.temp.name) / 'candidate'
        self.candidate.mkdir()
        (self.candidate / '.cursor-plugin').mkdir()
        shutil.copyfile(ROOT / '.cursor-plugin/plugin.json', self.candidate / '.cursor-plugin/plugin.json')
        shutil.copyfile(ROOT / 'LICENSE', self.candidate / 'LICENSE')
        for folder in ('rules', 'skills'):
            shutil.copytree(ROOT / folder, self.candidate / folder)

    def test_exact_payload_is_not_runtime_evidence(self):
        report = compare(ROOT, self.candidate)
        self.assertTrue(report['payload_matches'])
        self.assertFalse(report['runtime_verified'])
        self.assertEqual(8, report['expected_file_count'])

    def test_missing_template_changed_rule_and_extra_file(self):
        (self.candidate / 'skills/task-handoff/template.md').unlink()
        (self.candidate / 'rules/professional-core.mdc').write_text('stale rule')
        (self.candidate / 'unexpected.txt').write_text('private contents')
        before = {p.relative_to(self.candidate): p.read_bytes() for p in self.candidate.rglob('*') if p.is_file()}
        report = compare(ROOT, self.candidate)
        self.assertFalse(report['payload_matches'])
        self.assertEqual(['skills/task-handoff/template.md'], report['missing'])
        self.assertEqual(['rules/professional-core.mdc'], report['changed'])
        self.assertEqual(['unexpected.txt'], report['extra'])
        self.assertNotIn('private contents', json.dumps(report))
        after = {p.relative_to(self.candidate): p.read_bytes() for p in self.candidate.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_source_identity_changes_when_payload_changes(self):
        before = compare(ROOT, self.candidate)['source_payload_sha256']
        (self.candidate / 'LICENSE').write_text('changed')
        after = compare(self.candidate, self.candidate)['source_payload_sha256']
        self.assertNotEqual(before, after)

    def test_missing_candidate_is_not_created(self):
        missing = self.candidate / 'absent'
        with self.assertRaises(OSError):
            compare(ROOT, missing)
        self.assertFalse(missing.exists())

    def test_incomplete_source_rejected(self):
        (self.candidate / 'skills/task-handoff/template.md').unlink()
        with self.assertRaisesRegex(ValueError, 'required'):
            compare(self.candidate, self.candidate)

    def test_size_and_entry_limits(self):
        with patch('check_installation.MAX_FILE_BYTES', 1):
            with self.assertRaisesRegex(ValueError, 'size limit'):
                inventory(self.candidate, ('LICENSE',))
        with patch('check_installation.MAX_ENTRIES', 1):
            with self.assertRaisesRegex(ValueError, 'entry limit'):
                inventory(self.candidate, ('skills',))

    def test_link_ancestor_rejected(self):
        link = Path(self.temp.name) / 'link'
        try:
            link.symlink_to(self.candidate, target_is_directory=True)
        except OSError as exc:
            if getattr(exc, 'winerror', None) == 1314:
                self.skipTest('This Windows account cannot create symlinks')
            raise
        with self.assertRaisesRegex(ValueError, 'reparse'):
            inventory(link / 'skills', ('task-handoff',))

    def test_windows_reparse_attribute_rejected_without_following(self):
        original = Path.lstat
        def reparse_info(path):
            if path == self.candidate:
                info = original(path)
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return original(path)
        with patch.object(Path, 'lstat', reparse_info):
            with self.assertRaisesRegex(ValueError, 'reparse'):
                checked_path(self.candidate / 'skills')

    def test_cli_exit_codes_and_no_implicit_candidate(self):
        command = [sys.executable, str(ROOT / 'tools/check_installation.py')]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        def run(*args):
            return subprocess.run(command + list(args), env=env, capture_output=True, text=True)
        self.assertEqual(2, run().returncode)
        result = run('--candidate', str(self.candidate))
        self.assertEqual(0, result.returncode)
        self.assertFalse(json.loads(result.stdout)['runtime_verified'])
        (self.candidate / 'LICENSE').unlink()
        self.assertEqual(1, run('--candidate', str(self.candidate)).returncode)
        self.assertEqual(2, run('--candidate', str(self.candidate / 'missing')).returncode)


if __name__ == '__main__':
    unittest.main()
