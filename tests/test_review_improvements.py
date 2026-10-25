"""Regression coverage for numeric reporting and portable overlap inspection."""
import math
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from compare_runs import summarize
from overlap_audit import audit
from verify_archive import verify


class ReviewImprovementTests(unittest.TestCase):
    @staticmethod
    def run_data(variant, elapsed):
        return dict(task_id='B01', environment_key='same', prompt_revision='1',
                    variant=variant, functional_pass=True, critical_violations=0,
                    elapsed_seconds=elapsed, fresh_input_tokens=10,
                    cache_read_tokens=0, cache_write_tokens=0, output_tokens=1)

    def test_finite_measurements_do_not_overflow_while_averaging(self):
        runs = [self.run_data(variant, 1e308) for variant in ('baseline', 'candidate') for _ in range(2)]
        pair = summarize({'runs': runs})['pairs'][0]
        self.assertTrue(math.isfinite(pair['baseline_elapsed_seconds']))
        self.assertEqual(1e308, pair['candidate_elapsed_seconds'])

    def test_unrepresentable_integer_rejected_cleanly(self):
        run = self.run_data('baseline', 10**400)
        with self.assertRaisesRegex(ValueError, 'elapsed_seconds'):
            summarize({'runs': [run]})

    def test_nonfinite_and_boolean_times_rejected(self):
        for elapsed in (float('nan'), float('inf'), -float('inf'), True, -1):
            with self.subTest(elapsed=elapsed), self.assertRaises(ValueError):
                summarize({'runs': [self.run_data('baseline', elapsed)]})

    def test_overlap_audit_ignores_unsafe_zip_paths(self):
        with TemporaryDirectory() as td:
            archive = Path(td) / 'fixture.zip'
            with ZipFile(archive, 'w') as zf:
                for name in ('../code-review/SKILL.md', '/code-review/SKILL.md',
                             'bad\\code-review/SKILL.md', 'C:/code-review/SKILL.md'):
                    # Preserve the deliberately malformed ZIP name on Windows;
                    # constructing ZipInfo(name) would normalize backslashes.
                    info = ZipInfo()
                    info.filename = name
                    zf.writestr(info, '# unsafe candidate')
                zf.writestr('skills/code-review/SKILL.md', '# valid candidate')
            results = audit([archive])['deep-quality-review']
            self.assertEqual(1, len(results))
            self.assertEqual('code-review', results[0][1])

    def test_verifier_rejects_original_backslash_before_host_normalization(self):
        with TemporaryDirectory() as td:
            archive = Path(td) / 'bad.zip'
            with ZipFile(archive, 'w') as zf:
                info = ZipInfo()
                info.filename = 'cursor-craft/docs\\bad.md'
                zf.writestr(info, 'fixture')
                zf.writestr('cursor-craft/SOURCE-MANIFEST.sha256', '')
            with self.assertRaisesRegex(ValueError, 'Unsafe archive path'):
                verify(archive)


if __name__ == '__main__':
    unittest.main()
