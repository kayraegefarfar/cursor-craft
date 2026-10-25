"""Malformed-input regression cases, independent of Cursor runtime."""
import hashlib
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from compare_runs import summarize
from verify_archive import verify


class RegressionEdgeTests(unittest.TestCase):
    def test_non_string_benchmark_variant_is_validation_error(self):
        for variant in ([], {}, None, 42):
            with self.subTest(variant=variant):
                run = dict(task_id='B01', environment_key='fixture', prompt_revision='1',
                           variant=variant, functional_pass=True, critical_violations=0,
                           elapsed_seconds=1, fresh_input_tokens=1, cache_read_tokens=0,
                           cache_write_tokens=0, output_tokens=1)
                with self.assertRaisesRegex(ValueError, 'variant'):
                    summarize({'runs': [run]})

    def check_archive(self, names):
        with TemporaryDirectory() as td:
            path = Path(td) / 'input.zip'
            content = b'fixture'
            with ZipFile(path, 'w') as archive:
                for name in names:
                    archive.writestr('cursor-craft/' + name, content)
                manifest = ''.join(f'{hashlib.sha256(content).hexdigest()}  {name}\n' for name in names)
                archive.writestr('cursor-craft/SOURCE-MANIFEST.sha256', manifest)
            return verify(path)

    def test_archive_file_cannot_be_parent_directory(self):
        for names in (['docs', 'docs/a.md'], ['docs/a.md', 'docs'],
                      ['DOCS', 'docs/a.md'], ['docs/a.md', 'DOCS']):
            with self.subTest(names=names):
                with self.assertRaisesRegex(ValueError, 'file/directory'):
                    self.check_archive(names)

    def test_archive_manifest_cannot_be_parent_directory(self):
        with self.assertRaisesRegex(ValueError, 'file/directory'):
            self.check_archive(['SOURCE-MANIFEST.sha256/child.md'])

    def test_archive_similar_prefixes_remain_valid(self):
        report = self.check_archive(['docs.md', 'docs/a.md', 'docs-other/b.md'])
        self.assertTrue(report['integrity_verified'])
        self.assertFalse(report['runtime_verified'])


if __name__ == '__main__':
    unittest.main()
