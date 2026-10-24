"""Offline static/contract tests. Passing is NOT evidence of Cursor agent behavior."""
import json
import sys
import unittest
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate_package import ALLOWED_SKILLS, PLUGIN_VERSION, SEMVER, casefold_collision_messages, frontmatter, validate  # noqa: E402
from build_release import assemble  # noqa: E402
from verify_archive import verify  # noqa: E402
from archive_security import validate_relative_name  # noqa: E402
from compare_runs import summarize  # noqa: E402
from overlap_audit import audit  # noqa: E402
from release_readiness import assess  # noqa: E402


class SourcePackageTests(unittest.TestCase):
    def test_preflight(self):
        self.assertEqual([], validate(ROOT))

    def test_manifest_matches_supported_cursor_plugin_shape(self):
        manifest = json.loads((ROOT / '.cursor-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual('cursor-craft', manifest['name'])
        self.assertEqual(PLUGIN_VERSION, manifest['version'])
        self.assertEqual('https://github.com/kayraegefarfar/cursor-craft', manifest['repository'])
        for forbidden in ('mcpServers', 'hooks', 'agents', 'rules', 'skills', 'variables'):
            self.assertNotIn(forbidden, manifest)

    def test_prerelease_version_matches_cursor_semver(self):
        self.assertEqual('0.5.0-alpha', PLUGIN_VERSION)
        self.assertTrue(SEMVER.fullmatch('0.5.0-alpha'))
        self.assertTrue(SEMVER.fullmatch('1.2.3'))
        self.assertFalse(SEMVER.fullmatch('0.5'))
        self.assertFalse(SEMVER.fullmatch('v0.5.0-alpha'))
        self.assertFalse(SEMVER.fullmatch('0.5.0-'))
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            manifest_path = dest / '.cursor-plugin/plugin.json'
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
            manifest['version'] = '0.5.0'
            manifest_path.write_text(json.dumps(manifest), encoding='utf-8')
            self.assertTrue(any('0.5.0-alpha' in item for item in validate(dest)))

    def test_marketplace_source_dot_is_repository_root(self):
        market = json.loads((ROOT / '.cursor-plugin/marketplace.json').read_text(encoding='utf-8'))
        source = market['plugins'][0]['source']
        self.assertEqual('.', source)
        resolved = (ROOT / source / '.cursor-plugin' / 'plugin.json').resolve()
        self.assertEqual(resolved, (ROOT / '.cursor-plugin' / 'plugin.json').resolve())
        self.assertTrue(resolved.is_file())

    def test_security_policy_matches_public_repository(self):
        policy = (ROOT / 'SECURITY.md').read_text(encoding='utf-8')
        self.assertIn('https://github.com/kayraegefarfar/cursor-craft', policy)
        self.assertIn('Private vulnerability reporting', policy)
        self.assertNotIn('eventually published', policy.lower())
        self.assertNotRegex(policy, r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}')

    def test_github_marketplace_one_plugin_root(self):
        market = json.loads((ROOT / '.cursor-plugin/marketplace.json').read_text(encoding='utf-8'))
        self.assertEqual('cursor-craft-community', market['name'])
        self.assertEqual([('cursor-craft', '.')], [(p['name'], p['source']) for p in market['plugins']])

    def test_missing_github_marketplace_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / '.cursor-plugin/marketplace.json').unlink()
            self.assertTrue(any('marketplace' in x.lower() for x in validate(dest)))

    def test_marketplace_cannot_reference_external_folder(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            p = dest / '.cursor-plugin/marketplace.json'
            raw = json.loads(p.read_text(encoding='utf-8'))
            raw['plugins'][0]['source'] = '../elsewhere'
            p.write_text(json.dumps(raw))
            self.assertTrue(any('marketplace entry' in x.lower() for x in validate(dest)))

    def test_release_english_only_entrypoints(self):
        self.assertFalse((ROOT / 'README.tr.md').exists())
        for rel in ('README.md', 'CURSOR_AGENT_INSTALL_PROMPT.md', 'docs/GITHUB_PUBLISHING.md', 'docs/installation.md'):
            body = (ROOT / rel).read_text(encoding='utf-8')
            self.assertTrue(body.startswith('# '), rel)
            self.assertNotRegex(body, r'[çğıİöşüÇĞÖŞÜ]')
        self.assertIn('~/.cursor/plugins/local/cursor-craft', (ROOT / 'docs/installation.md').read_text())

    def test_each_skill_name_and_description(self):
        for name in ALLOWED_SKILLS:
            meta = frontmatter(ROOT / 'skills' / name / 'SKILL.md')
            self.assertEqual(name, meta['name'])
            self.assertTrue(meta['description'])

    def test_policy_routing_examples(self):
        cases = json.loads((ROOT / 'examples/routing-cases.json').read_text())
        by_id = {c['id']: c for c in cases}
        self.assertGreaterEqual(len(by_id), 18)
        self.assertEqual('none', by_id['S01']['expected_skill'])
        self.assertEqual('design-studio', by_id['S02']['expected_skill'])
        self.assertEqual('rea-workflow', by_id['S03']['expected_skill'])
        self.assertEqual('task-handoff', by_id['S06']['expected_skill'])
        self.assertEqual('ignore-untrusted-instruction', by_id['S08']['expected_action'])
        self.assertFalse(by_id['S08']['approval_required'])
        self.assertTrue(by_id['S07']['approval_required'])
        self.assertTrue(by_id['S13']['approval_required'])

    def test_trust_boundary_text(self):
        core = (ROOT / 'rules/professional-core.mdc').read_text().lower()
        for term in ('untrusted', 'approval', 'secrets', 'never report', 'preserve'):
            self.assertIn(term, core)
        rea = (ROOT / 'skills/rea-workflow/SKILL.md').read_text().lower()
        for term in ('authorized', 'license', 'observed', 'inferred'):
            self.assertIn(term, rea)

    def test_no_automatic_hooks_or_mcp(self):
        for target in ('mcp.json', 'hooks', 'agents'):
            self.assertFalse((ROOT / target).exists())

    def test_ci_permissions_and_immutable_action(self):
        ci = (ROOT / '.github/workflows/validate.yml').read_text()
        self.assertIn('contents: read', ci)
        self.assertIn('persist-credentials: false', ci)
        self.assertIn('actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683', ci)

    def test_missing_manifest_is_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / '.cursor-plugin/plugin.json').unlink()
            self.assertTrue(any('manifest' in x.lower() for x in validate(dest)))

    def test_wrong_skill_name_is_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            target = dest / 'skills/design-studio/SKILL.md'
            target.write_text(target.read_text().replace('name: design-studio', 'name: rea-workflow', 1))
            self.assertTrue(any('name mismatch' in x for x in validate(dest)))

    def test_extra_hook_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / 'hooks').mkdir()
            self.assertTrue(any('active hooks' in x for x in validate(dest)))

    def test_private_file_name_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / 'secrets.txt').write_text('not a secret, just test file')
            self.assertTrue(any('secret file' in x.lower() for x in validate(dest)))

    def test_embedded_secret_fingerprint_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            token = 'ghp_' + 'A' * 40  # Synthetic token pattern; no actual credential.
            (dest / 'README.md').write_text((dest / 'README.md').read_text() + '\n' + token)
            self.assertTrue(any('embedded secret' in x.lower() for x in validate(dest)))

    def test_traversal_link_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / 'README.md').write_text((dest / 'README.md').read_text() + '\n[bad](../../outside.txt)')
            self.assertTrue(any('out-of-tree' in x for x in validate(dest)))

    def test_symlink_to_external_private_data_rejected_without_read(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            outside = Path(td) / 'outside.txt'
            outside.write_text('Confidential file must never enter source package')
            link = dest / 'docs' / 'indirect.md'
            try:
                link.symlink_to(outside)
            except OSError as exc:
                if getattr(exc, 'winerror', None) == 1314:
                    self.skipTest('This Windows account cannot create symlinks')
                raise
            self.assertTrue(any('Symlink forbidden' in x for x in validate(dest)))

    def test_duplicate_frontmatter_key_rejected(self):
        with TemporaryDirectory() as td:
            target = Path(td) / 'SKILL.md'
            target.write_text('---\nname: test\nname: test2\ndescription: valid\n---\n# Heading\n')
            with self.assertRaisesRegex(ValueError, 'duplicate key'):
                frontmatter(target)

    def test_duplicate_manifest_key_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            p = dest / '.cursor-plugin/plugin.json'
            p.write_text('{"name":"cursor-craft","name":"other","version":"0.5.0"}')
            self.assertTrue(any('Duplicate JSON key' in x for x in validate(dest)))

    def test_case_insensitive_filename_collision_rejected(self):
        messages = casefold_collision_messages(['docs/architecture.md', 'docs/ARCHITECTURE.md'])
        self.assertTrue(any('Case-insensitive filename collision' in x for x in messages))
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / 'docs' / 'ARCHITECTURE.md').write_text('Conflicts on Windows')
            names = {path.name for path in (dest / 'docs').iterdir()}
            if {'architecture.md', 'ARCHITECTURE.md'} <= names:
                self.assertTrue(any('Case-insensitive filename collision' in x for x in validate(dest)))

    def test_invalid_routing_field_returns_error_not_crash(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            p = dest / 'examples/routing-cases.json'
            cases = json.loads(p.read_text()); cases[0]['expected_skill'] = []
            p.write_text(json.dumps(cases))
            self.assertTrue(any('unknown expected skill' in x for x in validate(dest)))

    def test_invalid_routing_case_id_returns_error_not_crash(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            p = dest / 'examples/routing-cases.json'
            cases = json.loads(p.read_text()); cases[0]['id'] = []
            p.write_text(json.dumps(cases))
            self.assertTrue(any('Invalid scenario id' in x for x in validate(dest)))

    def test_duplicate_routing_id_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            p = dest / 'examples/routing-cases.json'
            cases = json.loads(p.read_text())
            cases.append(cases[0]); p.write_text(json.dumps(cases))
            self.assertTrue(any('Duplicate scenario ID' in x for x in validate(dest)))


class RuntimeEvidenceTests(unittest.TestCase):
    @staticmethod
    def template():
        return json.loads((ROOT / 'examples/runtime-acceptance-template.json').read_text(encoding='utf-8'))

    def test_template_is_explicitly_unmeasured(self):
        result = assess(self.template())
        self.assertFalse(result['manual_attestation_complete'])
        self.assertEqual(12, result['status_counts']['NOT_RUN'])
        self.assertFalse(result['independently_verified'])
        self.assertFalse(result['public_release_authorized'])

    def test_false_pass_without_evidence_rejected(self):
        raw = self.template()
        raw['cases'][0]['status'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'requires evidence'):
            assess(raw)

    def test_false_pass_with_placeholder_reviewer_rejected(self):
        raw = self.template()
        row = raw['cases'][0]
        row.update(status='PASS', evidence_ids=['EV-CASE01-A'], environment_key='win-3.15-rev123', reviewer='test')
        with self.assertRaisesRegex(ValueError, 'placeholder'):
            assess(raw)

    def test_opaque_evidence_ids_refuse_paths(self):
        raw = self.template()
        row = raw['cases'][0]
        row.update(status='PASS', evidence_ids=['C:/Users/owner/private.log'], environment_key='env', reviewer='reviewer1')
        with self.assertRaisesRegex(ValueError, 'opaque'):
            assess(raw)

    def test_duplicate_runtime_id_rejected(self):
        raw = self.template()
        raw['cases'][1]['id'] = 'T01'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            assess(raw)

    def test_invalid_runtime_status_is_rejected_cleanly(self):
        raw = self.template()
        raw['cases'][0]['status'] = []
        with self.assertRaisesRegex(ValueError, 'invalid status'):
            assess(raw)

    def test_invalid_extra_runtime_field_rejected(self):
        raw = self.template()
        raw['cases'][0]['report_link'] = 'file:///private/path'
        with self.assertRaisesRegex(ValueError, 'fields'):
            assess(raw)

    def test_full_human_attestation_is_not_external_verification(self):
        raw = self.template()
        for row in raw['cases']:
            row.update(status='PASS', evidence_ids=['EV-' + row['id'] + '-ONE'],
                       environment_key='win-cursor-tested', reviewer='independent-human')
        result = assess(raw)
        self.assertTrue(result['manual_attestation_complete'])
        self.assertFalse(result['independently_verified'])
        self.assertFalse(result['public_release_authorized'])

    def test_not_run_with_evidence_rejected(self):
        raw = self.template()
        raw['cases'][0]['evidence_ids'] = ['EV-T01-ONE']
        with self.assertRaisesRegex(ValueError, 'NOT_RUN'):
            assess(raw)

    def test_corrupt_bundled_runtime_template_rejected(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            file = dest / 'examples/runtime-acceptance-template.json'
            obj = json.loads(file.read_text()); obj['cases'][0]['status'] = 'FAIL'
            file.write_text(json.dumps(obj))
            self.assertTrue(any('NOT_RUN only' in x for x in validate(dest)))

    def test_rejects_undocumented_executable_component(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / 'commands').mkdir()
            self.assertTrue(any('active commands' in x for x in validate(dest)))


class BuildTests(unittest.TestCase):
    def test_reproducible_archive_and_safe_entries(self):
        with TemporaryDirectory() as td:
            a, b = Path(td) / 'a.zip', Path(td) / 'b.zip'
            ha = assemble(ROOT, a)
            hb = assemble(ROOT, b)
            self.assertEqual(ha, hb)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with ZipFile(a) as zf:
                names = zf.namelist()
                self.assertTrue(all(s.startswith('cursor-craft/') for s in names))
                self.assertFalse(any('..' in Path(s).parts for s in names))
                self.assertFalse(any('__pycache__' in s or s.endswith('.pyc') for s in names))
                self.assertIn('cursor-craft/.cursor-plugin/plugin.json', names)
                self.assertIn('cursor-craft/rules/professional-core.mdc', names)

    def test_refuses_zip_inside_repo(self):
        with self.assertRaisesRegex(ValueError, 'OUTSIDE'):
            assemble(ROOT, ROOT / 'local-build.zip')


class BenchmarkTests(unittest.TestCase):
    @staticmethod
    def sample(variant, passed=True, critical=0, read=150, out=20):
        return dict(task_id='B01', environment_key='same-platform-and-project',
                    prompt_revision='v1', variant=variant, functional_pass=passed,
                    critical_violations=critical, elapsed_seconds=45.0,
                    fresh_input_tokens=200, cache_read_tokens=read,
                    cache_write_tokens=0, output_tokens=out)

    def test_empty_has_no_measurement(self):
        result = summarize({'runs': []})
        self.assertFalse(result['measured'])
        self.assertEqual([], result['pairs'])

    def test_paired_results_keep_cache_separate(self):
        report = summarize({'runs': [self.sample('baseline'), self.sample('candidate', read=200)]})
        self.assertTrue(report['measured'])
        self.assertEqual(200, report['pairs'][0]['token_means']['cache_read_tokens']['candidate'])
        self.assertEqual(20, report['pairs'][0]['token_means']['output_tokens']['candidate'])

    def test_quality_regression_wins_over_token_saving(self):
        report = summarize({'runs': [self.sample('baseline'), self.sample('candidate', False, 1, 0, 1)]})
        self.assertTrue(report['pairs'][0]['quality_regression_flag'])

    def test_mismatched_environment_not_compared(self):
        before = self.sample('baseline')
        after = self.sample('candidate'); after['environment_key'] = 'changed-revision'
        result = summarize({'runs': [before, after]})
        self.assertFalse(result['measured'])
        self.assertEqual(2, result['unpaired_run_count'])

    def test_invalid_negative_token_rejected(self):
        bad = self.sample('candidate'); bad['output_tokens'] = -1
        with self.assertRaisesRegex(ValueError, 'output_tokens'):
            summarize({'runs': [bad]})

    def test_bool_cannot_count_as_token(self):
        bad = self.sample('candidate'); bad['fresh_input_tokens'] = True
        with self.assertRaisesRegex(ValueError, 'fresh_input_tokens'):
            summarize({'runs': [bad]})


class LegacyOverlapTests(unittest.TestCase):
    def test_archive_names_only_signal_candidates(self):
        with TemporaryDirectory() as td:
            path = Path(td) / 'old.zip'
            with ZipFile(path, 'w') as zf:
                zf.writestr('skills/code-review/SKILL.md', '# review')
                zf.writestr('skills/ui-and-accessibility/SKILL.md', '# ui')
            result = audit([path])
            self.assertTrue(any(x[1] == 'code-review' for x in result['deep-quality-review']))
            self.assertTrue(any(x[1] == 'ui-and-accessibility' for x in result['design-studio']))


class ArchiveVerificationTests(unittest.TestCase):
    def test_build_and_verify_manifest(self):
        with TemporaryDirectory() as td:
            target = Path(td) / 'source.zip'
            digest = assemble(ROOT, target)
            summary = verify(target)
            self.assertEqual(digest, summary['archive_sha256'])
            self.assertTrue(summary['integrity_verified'])
            self.assertFalse(summary['runtime_verified'])
            with ZipFile(target) as archive:
                self.assertIn('cursor-craft/SOURCE-MANIFEST.sha256', archive.namelist())

    def test_extracted_source_validator_checks_manifest_and_rebuilds(self):
        with TemporaryDirectory() as td:
            td = Path(td)
            original, rebuilt = td / 'original.zip', td / 'rebuilt.zip'
            assemble(ROOT, original)
            extracted = td / 'extracted'
            with ZipFile(original) as source:
                source.extractall(extracted)
            tree = extracted / 'cursor-craft'
            self.assertEqual([], validate(tree))
            assemble(tree, rebuilt)
            self.assertEqual(original.read_bytes(), rebuilt.read_bytes())
            (tree / 'README.md').write_text('tampered')
            self.assertTrue(any('hash manifest' in problem for problem in validate(tree)))

    def test_do_not_overwrite_existing_output(self):
        with TemporaryDirectory() as td:
            target = Path(td) / 'source.zip'
            target.write_bytes(b'valuable-existing-file')
            with self.assertRaises(FileExistsError):
                assemble(ROOT, target)
            self.assertEqual(b'valuable-existing-file', target.read_bytes())

    def test_reject_nonportable_source_name(self):
        with TemporaryDirectory() as td:
            dest = Path(td) / 'repo'; copytree(ROOT, dest)
            (dest / 'docs' / 'NUL.md').write_text('dangerous Windows name')
            self.assertTrue(any('Nonportable/unsafe' in x for x in validate(dest)))

    def test_windows_path_policy(self):
        for path in ('COM1.txt', 'docs/CON.md', 'docs/trail. ', 'docs/../secret.txt',
                     'C:/secret.txt', 'folder\\evil.txt', 'docs/data:private.txt'):
            self.assertIsNotNone(validate_relative_name(path), path)
        for path in ('README.md', '.cursor-plugin/plugin.json', 'skills/design-studio/SKILL.md'):
            self.assertIsNone(validate_relative_name(path), path)

    def test_reject_tampered_file_with_original_hash_manifest(self):
        with TemporaryDirectory() as td:
            a, b = Path(td) / 'good.zip', Path(td) / 'tampered.zip'
            assemble(ROOT, a)
            with ZipFile(a) as src, ZipFile(b, 'w') as dst:
                for item in src.infolist():
                    data = src.read(item)
                    if item.filename == 'cursor-craft/README.md':
                        data += b'\nmalicious change'
                    dst.writestr(item, data)
            with self.assertRaisesRegex(ValueError, 'hash manifest'):
                verify(b)

    def test_reject_zip_slip(self):
        with TemporaryDirectory() as td:
            z = Path(td) / 'bad.zip'
            with ZipFile(z, 'w') as archive:
                archive.writestr('cursor-craft/../escape.txt', 'oops')
                archive.writestr('cursor-craft/SOURCE-MANIFEST.sha256', '')
            with self.assertRaisesRegex(ValueError, 'Unsafe archive path'):
                verify(z)

    def test_reject_symlink_zip_entry(self):
        with TemporaryDirectory() as td:
            z = Path(td) / 'bad.zip'
            with ZipFile(z, 'w') as archive:
                link = ZipInfo('cursor-craft/link.txt')
                link.create_system = 3
                link.external_attr = 0o120777 << 16
                archive.writestr(link, 'target')
                archive.writestr('cursor-craft/SOURCE-MANIFEST.sha256', '')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                verify(z)

    def test_reject_archive_windows_name_collision(self):
        with TemporaryDirectory() as td:
            z = Path(td) / 'bad.zip'
            with ZipFile(z, 'w') as archive:
                archive.writestr('cursor-craft/docs/A.md', 'first')
                archive.writestr('cursor-craft/docs/a.md', 'second')
                archive.writestr('cursor-craft/SOURCE-MANIFEST.sha256', '')
            with self.assertRaisesRegex(ValueError, 'colliding'):
                verify(z)


if __name__ == '__main__':
    unittest.main()
