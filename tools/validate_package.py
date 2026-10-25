#!/usr/bin/env python3
"""Strict, offline and non-mutating Cursor Craft package preflight.

Validates shape, internal links, descriptions and non-executable alpha policy.
This does NOT exercise Cursor itself and is not a security sandbox.
"""
from __future__ import annotations

import json
import re
import hashlib
import sys
import os
import stat
from pathlib import Path
from archive_security import validate_relative_name

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SKILLS = frozenset({'design-studio', 'rea-workflow', 'deep-quality-review', 'task-handoff'})
REQUIRED_DOCS = frozenset({
    'README.md', 'GITHUB_RELEASE_NOTES.md', 'CURSOR_AGENT_INSTALL_PROMPT.md', 'LICENSE', 'SECURITY.md', 'CONTRIBUTING.md',
    'CHANGELOG.md', 'docs/architecture.md', 'docs/installation.md',
    'docs/compatibility.md', 'docs/acceptance-tests.md', 'docs/benchmarks.md',
    'docs/security-model.md', 'docs/release-gates.md', 'docs/rea-integration.md',
    'docs/handoff-template.md', 'docs/migration.md', 'docs/development-status.md',
    'docs/design-standard.md', 'docs/publication-checklist.md',
    'docs/requirements-traceability.md', 'docs/runtime-evidence.md',
    'docs/maintainer-review.md', 'docs/professional-quality-rubric.md', 'docs/archive-integrity.md', 'docs/GITHUB_PUBLISHING.md',
})
SAFE_EXTENSIONS = frozenset({'.md', '.mdc', '.json', '.py', '.yml', '.yaml', '.txt', '.toml'})
RESERVED_FILES = frozenset({'LICENSE', '.gitignore', '.gitattributes', 'SOURCE-MANIFEST.sha256'})
SKIP_NAMES = frozenset({'.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'dist'})
EXCLUDED_PATHS = frozenset({'mcp.json', 'hooks', 'agents', 'commands', 'SKILL.md'})
LICENSE_IDENTIFIERS = {'MIT'}
PLUGIN_VERSION = '0.5.0-alpha'
PUBLIC_REPOSITORY = 'https://github.com/kayraegefarfar/cursor-craft'
# Cursor plugin schema: X.Y.Z with an optional prerelease suffix. No leading v.
SEMVER = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
    r'(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?$'
)
# Deliberately narrow patterns: catch likely real tokens without flagging docs examples.
SECRET_MARKERS = (
    re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),
    re.compile(r'gh[pousr]_[A-Za-z0-9]{30,}'),
    re.compile(r'AKIA[A-Z0-9]{16}'),
)


def casefold_collision_messages(relative_names: list[str]) -> list[str]:
    """Report slash-separated paths that differ only by case.

    Comparison is textual. Windows path equality would hide the collision.
    """
    errors: list[str] = []
    seen: dict[str, str] = {}
    for name in relative_names:
        folded = name.casefold()
        previous = seen.get(folded)
        if previous is not None and previous != name:
            errors.append(f'Case-insensitive filename collision: {name} vs {previous}')
        else:
            seen[folded] = name
    return errors


def strict_json(text: str) -> object:
    """JSON decode with duplicate-key rejection to avoid parser ambiguity."""
    def checked_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=checked_pairs)


def frontmatter(path: Path) -> dict[str, str]:
    """Parse deliberately limited scalar YAML subset used by plugin files.

    Reject advanced YAML syntax rather than silently misinterpreting it.
    """
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0].strip() != '---':
        raise ValueError(f'{path.name}: missing YAML frontmatter opener')
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == '---')
    except StopIteration as exc:
        raise ValueError(f'{path.name}: missing YAML frontmatter closer') from exc
    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        match = re.fullmatch(r'([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*?)\s*', line)
        if not match:
            raise ValueError(f'{path.name}: unsupported frontmatter: {line[:80]!r}')
        key, value = match.groups()
        if key in data:
            raise ValueError(f'{path.name}: duplicate key: {key}')
        if value.startswith(('|', '>', '[', '{', '&', '*', '!')):
            raise ValueError(f'{path.name}: only simple scalar frontmatter supported')
        if value and value[0] in ("'", '"'):
            if len(value) < 2 or value[-1] != value[0]:
                raise ValueError(f'{path.name}: mismatched quotes for {key}')
            value = value[1:-1]
        if not value:
            raise ValueError(f'{path.name}: empty value for {key}')
        data[key] = value
    if not any(line.startswith('# ') for line in lines[end + 1:]):
        raise ValueError(f'{path.name}: missing level-one markdown heading')
    return data


def _relative_markdown_links(root: Path, errors: list[str]) -> None:
    docs = [p for p in root.rglob('*')
            if not any(part in SKIP_NAMES for part in p.relative_to(root).parts)
            and p.is_file() and p.suffix in {'.md', '.mdc'}]
    for path in docs:
        data = path.read_text(encoding='utf-8')
        # Simple inline links; documentation uses no reference-style local links.
        for match in re.finditer(r'(?<!!)\[[^]\n]+\]\(([^)]+)\)', data):
            href = match.group(1).split('#', 1)[0].strip()
            if not href or href.startswith(('https://', 'http://', 'mailto:')):
                continue
            if href.startswith(('javascript:', 'data:', 'file:')) or href.startswith('/'):
                errors.append(f'Unsafe local link: {path.relative_to(root)} -> {href}')
                continue
            resolved = (path.parent / href).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append(f'Broken/out-of-tree link: {path.relative_to(root)} -> {href}')


def validate(root: Path = ROOT) -> list[str]:
    """Validate a repository root, returning all static problems (not runtime results)."""
    errors: list[str] = []
    if not root.exists() or not root.is_dir():
        return ['Repository directory does not exist']

    # Inspect metadata before any manifest, Skill, hash or Markdown read. A
    # later rejection is too late if a required file points outside the tree.
    # As with packaging, callers must keep the source quiescent during checks.
    try:
        absolute = Path(os.path.abspath(root))
        for parent in (absolute, *absolute.parents):
            info = parent.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                return ['Symlink forbidden: source root or ancestor is a link/reparse point']
        pending = [root]
        while pending:
            directory = pending.pop()
            for path in directory.iterdir():
                if path.name in SKIP_NAMES:
                    continue
                info = path.lstat()
                if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                    errors.append(f'Symlink forbidden: {path.relative_to(root)} (link/reparse point)')
                elif stat.S_ISDIR(info.st_mode):
                    pending.append(path)
                elif not stat.S_ISREG(info.st_mode):
                    errors.append(f'Nonregular file forbidden: {path.relative_to(root)}')
                elif info.st_size > 500_000:
                    errors.append(f'File suspiciously large for a prompt-only plugin: {path.relative_to(root)}')
        if errors:
            return errors
    except OSError:
        return ['Cannot safely inspect source metadata; check access permissions']

    for rel in sorted(REQUIRED_DOCS):
        if not (root / rel).is_file():
            errors.append(f'Missing documentation: {rel}')

    manifest_path = root / '.cursor-plugin' / 'plugin.json'
    try:
        manifest = strict_json(manifest_path.read_text(encoding='utf-8'))
        if not isinstance(manifest, dict):
            raise ValueError('JSON root must be object')
        if not re.fullmatch(r'[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?', str(manifest.get('name', ''))):
            errors.append('Plugin name must use lowercase letters/numbers/dots/hyphens')
        if manifest.get('name') != 'cursor-craft':
            errors.append('Unexpected plugin name')
        version = str(manifest.get('version', ''))
        if not SEMVER.fullmatch(version):
            errors.append('Plugin version must be semantic X.Y.Z with an optional prerelease suffix')
        elif version != PLUGIN_VERSION:
            errors.append(f'Plugin version must stay {PLUGIN_VERSION} until a new release is declared')
        if manifest.get('repository') != PUBLIC_REPOSITORY:
            errors.append('Plugin repository must be the public GitHub repository')
        if not isinstance(manifest.get('description'), str) or len(manifest['description']) < 30:
            errors.append('Missing/short plugin description')
        if manifest.get('license') not in LICENSE_IDENTIFIERS:
            errors.append('Unknown or missing SPDX license')
        if not isinstance(manifest.get('author'), dict) or not manifest['author'].get('name'):
            errors.append('Plugin author must be an object with name')
        for field in ('rules', 'skills', 'agents', 'commands', 'hooks', 'mcpServers', 'variables'):
            if field in manifest:
                errors.append(f'Alpha uses auto-discovery/no executable integration, remove manifest field {field}')
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f'Invalid/missing plugin manifest: {exc}')

    # Cursor's GitHub repository importer uses a marketplace descriptor. Our
    # root-level one-plugin repository explicitly references its own plugin.
    marketplace_file = root / '.cursor-plugin' / 'marketplace.json'
    try:
        market = strict_json(marketplace_file.read_text(encoding='utf-8'))
        if not isinstance(market, dict) or market.get('name') != 'cursor-craft-community':
            errors.append('Invalid/missing marketplace name')
        owner = market.get('owner', {}) if isinstance(market, dict) else {}
        if not isinstance(owner, dict) or not owner.get('name'):
            errors.append('Invalid/missing marketplace owner')
        entries = market.get('plugins', []) if isinstance(market, dict) else []
        if not isinstance(entries, list) or len(entries) != 1:
            errors.append('Marketplace must reference exactly one plugin')
        elif not isinstance(entries[0], dict) or entries[0].get('name') != 'cursor-craft' or entries[0].get('source') != '.' or entries[0].get('version') != PLUGIN_VERSION:
            errors.append('Marketplace entry does not reference the root Cursor Craft plugin')
        else:
            resolved = (root / entries[0]['source'] / '.cursor-plugin' / 'plugin.json').resolve()
            if not resolved.is_relative_to((root / '.cursor-plugin' / 'plugin.json').resolve().parent.parent):
                errors.append('Marketplace source escapes the repository root')
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f'Invalid/missing marketplace manifest: {exc}')

    rules_dir = root / 'rules'
    rule_paths = sorted(rules_dir.glob('*.mdc')) if rules_dir.is_dir() else []
    if len(rule_paths) != 1:
        errors.append(f'Exactly one core rule required, found {len(rule_paths)}')
    for path in rule_paths:
        try:
            meta = frontmatter(path)
            if meta.get('alwaysApply') != 'true':
                errors.append(f'{path.name}: core must alwaysApply: true')
            if not meta.get('description') or len(meta['description']) > 320:
                errors.append(f'{path.name}: core rule needs concise description')
            if set(meta) != {'description', 'alwaysApply'}:
                errors.append(f'{path.name}: unsupported core rule frontmatter keys')
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    skills_root = root / 'skills'
    skill_dirs = {p.name for p in skills_root.iterdir() if p.is_dir()} if skills_root.is_dir() else set()
    if skill_dirs != ALLOWED_SKILLS:
        errors.append(f'Skill dirs mismatch: missing={sorted(ALLOWED_SKILLS-skill_dirs)}, extra={sorted(skill_dirs-ALLOWED_SKILLS)}')
    for name in sorted(ALLOWED_SKILLS):
        path = skills_root / name / 'SKILL.md'
        if not path.is_file():
            errors.append(f'Missing Skill: {name}/SKILL.md')
            continue
        try:
            meta = frontmatter(path)
            if set(meta) != {'name', 'description'}:
                errors.append(f'{name}: unsupported Skill frontmatter keys')
            if meta.get('name') != name:
                errors.append(f'{name}: Skill name mismatch')
            descr = meta.get('description', '')
            if not 30 <= len(descr) <= 320:
                errors.append(f'{name}: description must be 30–320 characters')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta.get('name', '')):
                errors.append(f'{name}: Skill name must be kebab-case')
        except (OSError, ValueError) as exc:
            errors.append(str(exc))

    for item in EXCLUDED_PATHS:
        if (root / item).exists():
            errors.append(f'Alpha cannot ship an active {item} component')

    relative_names: list[str] = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        relative_names.append(rel.as_posix())
        path_issue = validate_relative_name(rel.as_posix())
        if path_issue:
            errors.append(f'Nonportable/unsafe source path: {rel}: {path_issue}')
        if path.is_symlink():
            errors.append(f'Symlink forbidden: {rel}')
            continue  # Never read or follow a symlink, including one pointing outside this root.
        if any(part in SKIP_NAMES for part in rel.parts):
            continue  # Generated caches are excluded by reproducible packaging.
        if any(part.startswith('.env') for part in rel.parts) or any(part in {'node_modules', '.ssh', '.aws'} for part in rel.parts):
            errors.append(f'Private/unsafe directory name: {rel}')
        if path.is_file():
            if path.suffix not in SAFE_EXTENSIONS and path.name not in RESERVED_FILES:
                errors.append(f'Unexpected file type: {rel}')
            if path.stat().st_size > 500_000:
                errors.append(f'File suspiciously large for a prompt-only plugin: {rel}')
            if path.name.lower().startswith(('.env', 'id_rsa', 'credentials', 'secrets')):
                errors.append(f'Possible secret file: {rel}')
            # Scan published text for high-confidence credential fingerprints.
            if path.suffix in SAFE_EXTENSIONS or path.name in RESERVED_FILES:
                content = path.read_text(encoding='utf-8', errors='replace')
                for marker in SECRET_MARKERS:
                    if marker.search(content):
                        errors.append(f'Possible embedded secret: {rel}')
                        break
    # If validating an extracted source release, also verify its embedded
    # content hashes. Original working trees normally have no hash manifest.
    release_manifest = root / 'SOURCE-MANIFEST.sha256'
    if release_manifest.is_file():
        try:
            declared = {}
            for line in release_manifest.read_text(encoding='utf-8').splitlines():
                if len(line) < 67 or line[64:66] != '  ' or not re.fullmatch(r'[0-9a-f]{64}', line[:64]):
                    raise ValueError('invalid SHA-256 line')
                digest, name = line[:64], line[66:]
                if validate_relative_name(name) or name in declared:
                    raise ValueError('unsafe or duplicate manifest entry')
                declared[name] = digest
            actual = {}
            for path in root.rglob('*'):
                if not path.is_file() or path.is_symlink():
                    continue
                rel = path.relative_to(root)
                if rel.as_posix() == 'SOURCE-MANIFEST.sha256' or any(part in SKIP_NAMES for part in rel.parts):
                    continue
                actual[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            if declared != actual:
                errors.append('Extracted source hash manifest does not match file contents')
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(f'Invalid extracted source hash manifest: {exc}')
    errors.extend(casefold_collision_messages(relative_names))
    _relative_markdown_links(root, errors)

    # Evidence starts at NOT_RUN. Only manually gathered proof may be recorded later.
    try:
        from release_readiness import CASE_IDS, assess
        evidence = strict_json((root / 'examples/runtime-acceptance-template.json').read_text(encoding='utf-8'))
        summary = assess(evidence)
        if summary['manual_attestation_complete'] or summary['status_counts']['NOT_RUN'] != len(CASE_IDS):
            errors.append('Bundled runtime evidence template must contain NOT_RUN only')
    except (OSError, ValueError, TypeError, ImportError) as exc:
        errors.append(f'Invalid runtime evidence template: {exc}')

    try:
        cases = strict_json((root / 'examples' / 'routing-cases.json').read_text(encoding='utf-8'))
        if not isinstance(cases, list):
            raise ValueError('cases must be an array')
        if len(cases) < 14:
            errors.append('Expected >=14 routing policy cases')
        seen: set[str] = set()
        for case in cases:
            if not isinstance(case, dict):
                errors.append('Routing case must be an object')
                continue
            case_id = case.get('id')
            if not isinstance(case_id, str) or not re.fullmatch(r'S\d{2}', case_id):
                errors.append(f'Invalid scenario id: {case_id}')
            if isinstance(case_id, str) and case_id in seen:
                errors.append(f'Duplicate scenario ID: {case_id}')
            if isinstance(case_id, str):
                seen.add(case_id)
            if not isinstance(case.get('expected_skill'), str) or case['expected_skill'] not in ALLOWED_SKILLS | {'none'}:
                errors.append(f'{case_id}: unknown expected skill')
            if type(case.get('approval_required')) is not bool:
                errors.append(f'{case_id}: missing boolean approval_required')
            if not isinstance(case.get('expected_action'), str) or case['expected_action'] not in {'implement', 'analyze', 'review', 'handoff', 'seek-approval', 'ignore-untrusted-instruction', 'report-blocker'}:
                errors.append(f'{case_id}: invalid expected_action')
            if not case.get('request') or not case.get('reason'):
                errors.append(f'{case_id}: missing request/reason')
        untrusted = [c for c in cases if c.get('expected_action') == 'ignore-untrusted-instruction']
        if not untrusted or any(c.get('approval_required') for c in untrusted):
            errors.append('Untrusted prompt injection must be ignored without requesting to approve its payload')
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append(f'Invalid routing cases: {exc}')
    return errors


def main() -> int:
    issues = validate()
    if issues:
        for item in issues:
            print(f'FAIL: {item}', file=sys.stderr)
        print(f'FAILED: {len(issues)} static issue(s)', file=sys.stderr)
        return 1
    print('PASS: Cursor plugin structure, rule/Skill frontmatter, documentation links, route policies, no active executable integrations.')
    print('UNVERIFIED: Actual Cursor runtime, specialist invocation, tool permissions, token reduction, UI quality and Windows behavior.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
