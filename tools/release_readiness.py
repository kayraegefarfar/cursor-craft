#!/usr/bin/env python3
"""Review user-supplied Cursor runtime acceptance *attestations* (no Cursor access).

This reads only the specified JSON; does not read referenced logs, change files,
fetch network resources, or publish anything. A PASS is a human claim, NOT
independent verification. Stable release also requires separate maintainer review.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CASE_IDS = tuple(f'T{number:02d}' for number in range(1, 13))
STATUSES = frozenset({'NOT_RUN', 'PASS', 'FAIL', 'BLOCKED'})
EVIDENCE_PATTERN = re.compile(r'EV-[A-Z0-9][A-Z0-9-]{2,63}')
ALLOWED_CASE_FIELDS = frozenset({'id', 'status', 'evidence_ids', 'environment_key', 'reviewer', 'note'})


def assess(raw: dict) -> dict:
    """Evaluate coverage and consistency of manually entered release evidence."""
    if not isinstance(raw, dict) or set(raw) != {'schema_version', 'cases'} or raw['schema_version'] != 1:
        raise ValueError('Root must contain schema_version: 1 and cases only')
    cases = raw['cases']
    if not isinstance(cases, list) or len(cases) != len(CASE_IDS):
        raise ValueError(f'Expected exactly {len(CASE_IDS)} runtime acceptance cases')
    ids = set()
    counted = {status: 0 for status in ('PASS', 'FAIL', 'BLOCKED', 'NOT_RUN')}
    problems = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or set(case) != ALLOWED_CASE_FIELDS:
            raise ValueError(f'Case index {index}: fields must be {sorted(ALLOWED_CASE_FIELDS)}')
        case_id = case['id']
        if not isinstance(case_id, str) or case_id not in CASE_IDS or case_id in ids:
            raise ValueError(f'Invalid/duplicate case ID: {case_id!r}')
        ids.add(case_id)
        status = case['status']
        if not isinstance(status, str) or status not in STATUSES:
            raise ValueError(f'{case_id}: invalid status')
        counted[status] += 1
        evidence = case['evidence_ids']
        if not isinstance(evidence, list) or len(evidence) > 12 or any(
            not isinstance(item, str) or not EVIDENCE_PATTERN.fullmatch(item) for item in evidence
        ) or len(set(evidence)) != len(evidence):
            raise ValueError(f'{case_id}: evidence_ids must be unique opaque EV- IDs (no paths or secrets)')
        for field in ('environment_key', 'reviewer', 'note'):
            if not isinstance(case[field], str) or len(case[field]) > 500:
                raise ValueError(f'{case_id}: {field} must be short text')
        if status == 'PASS':
            if not evidence or not case['environment_key'].strip() or not case['reviewer'].strip():
                raise ValueError(f'{case_id}: PASS requires evidence IDs, environment key and reviewer')
            if case['reviewer'].strip().lower() in ('test', 'unknown', 'none'):
                raise ValueError(f'{case_id}: reviewer cannot be a placeholder')
        elif evidence and status == 'NOT_RUN':
            raise ValueError(f'{case_id}: NOT_RUN must not cite evidence; choose other status')
        if status != 'PASS':
            problems.append({'id': case_id, 'status': status})
    missing = set(CASE_IDS) - ids
    if missing:
        raise ValueError(f'Missing cases: {sorted(missing)}')
    return {
        'schema_version': 1,
        'manual_attestation_complete': counted['PASS'] == len(CASE_IDS),
        'status_counts': counted,
        'unpassed_cases': problems,
        'independently_verified': False,
        'public_release_authorized': False,
        'warning': 'These are owner-entered attestations only. External evidence, licenses, real Cursor behavior, compatibility, security and publisher consent require independent review.'
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='User-supplied JSON following examples/runtime-acceptance-template.json')
    args = parser.parse_args()
    try:
        result = assess(json.loads(args.input.read_text(encoding='utf-8')))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
