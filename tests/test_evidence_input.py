"""Reject ambiguous runtime attestations; these tests do not run Cursor."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from release_readiness import assess, unique_fields


class EvidenceInputTests(unittest.TestCase):
    def test_schema_version_requires_integer_not_bool_or_float(self):
        for invalid in (True, 1.0, '1', None):
            with self.subTest(invalid=invalid):
                raw = json.loads((ROOT / 'examples/runtime-acceptance-template.json').read_text())
                raw['schema_version'] = invalid
                with self.assertRaisesRegex(ValueError, 'schema_version'):
                    assess(raw)

    def test_duplicate_status_cannot_override_failure(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON field'):
            json.loads('{"cases":[{"status":"FAIL","status":"PASS"}]}', object_pairs_hook=unique_fields)

    def test_duplicate_root_field_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON field'):
            json.loads('{"schema_version":2,"schema_version":1}', object_pairs_hook=unique_fields)


if __name__ == '__main__':
    unittest.main()
