#!/usr/bin/env python3
"""Conservative, local-only paired benchmark reporter for Cursor Craft.

Uses caller-provided observations. Never invents benchmark data or applies a
universal token-equivalence assumption to cached and noncached tokens.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

VARIANTS = {'baseline', 'candidate'}
TOKEN_FIELDS = ('fresh_input_tokens', 'cache_read_tokens', 'cache_write_tokens', 'output_tokens')
NUMBER_FIELDS = ('elapsed_seconds',) + TOKEN_FIELDS
REQUIRED = {'task_id', 'environment_key', 'prompt_revision', 'variant', 'functional_pass', 'critical_violations'} | set(NUMBER_FIELDS)


def summarize(raw: dict) -> dict:
    """Compare matched runs; reject unsafe/malformed observations explicitly."""
    if not isinstance(raw, dict) or not isinstance(raw.get('runs'), list):
        raise ValueError('Provide a JSON object with runs: []')
    groups: dict[tuple, dict[str, list[dict]]] = defaultdict(lambda: {'baseline': [], 'candidate': []})
    for index, run in enumerate(raw['runs']):
        if not isinstance(run, dict) or not REQUIRED.issubset(run):
            raise ValueError(f'Run {index}: missing required fields')
        if run['variant'] not in VARIANTS:
            raise ValueError(f'Run {index}: variant must be baseline or candidate')
        if type(run['functional_pass']) is not bool:
            raise ValueError(f'Run {index}: functional_pass must be bool')
        if type(run['critical_violations']) is not int or run['critical_violations'] < 0:
            raise ValueError(f'Run {index}: critical_violations must be nonnegative integer')
        for field in NUMBER_FIELDS:
            value = run[field]
            if type(value) not in (int, float) or value < 0 or value != value or value == float('inf'):
                raise ValueError(f'Run {index}: invalid number for {field}')
            if field.endswith('_tokens') and type(value) is not int:
                raise ValueError(f'Run {index}: {field} must be integer')
        for field in ('task_id', 'environment_key', 'prompt_revision'):
            if not isinstance(run[field], str) or not run[field].strip():
                raise ValueError(f'Run {index}: missing string {field}')
        key = (run['task_id'], run['environment_key'], run['prompt_revision'])
        groups[key][run['variant']].append(run)

    pairs: list[dict] = []
    unpaired = 0
    for key, variants in sorted(groups.items()):
        # Do not compare runs if the other variant has a different number of repetitions.
        before = variants['baseline']
        after = variants['candidate']
        if not before or not after or len(before) != len(after):
            unpaired += len(before) + len(after)
            continue
        # Multiple repetitions are summarized per task/env/prompt, not cherry-picked.
        def average(runs: list[dict], field: str) -> float:
            return sum(x[field] for x in runs) / len(runs)
        b_pass = all(x['functional_pass'] and x['critical_violations'] == 0 for x in before)
        c_pass = all(x['functional_pass'] and x['critical_violations'] == 0 for x in after)
        result = {
            'task_id': key[0], 'environment_key': key[1], 'prompt_revision': key[2],
            'repetitions_per_variant': len(before),
            'baseline_gate_pass': b_pass, 'candidate_gate_pass': c_pass,
            'quality_regression_flag': b_pass and not c_pass,
            'baseline_elapsed_seconds': round(average(before, 'elapsed_seconds'), 2),
            'candidate_elapsed_seconds': round(average(after, 'elapsed_seconds'), 2),
            'token_means': {},
        }
        for field in TOKEN_FIELDS:
            result['token_means'][field] = {
                'baseline': round(average(before, field), 2),
                'candidate': round(average(after, field), 2),
            }
        pairs.append(result)
    return {
        'measured': bool(pairs),
        'pairs': pairs,
        'unpaired_run_count': unpaired,
        'warning': 'Only matched observations compared. Cache reads/writes are reported separately; provider billing and output quality need independent evidence.'
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path, help='JSON file with measured runs; empty template is allowed')
    args = p.parse_args()
    try:
        raw = json.loads(args.input.read_text(encoding='utf-8'))
        result = summarize(raw)
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
