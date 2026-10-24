# Fair quality and token benchmark plan

**No benchmark results are claimed in alpha.** Compare the current Cursor setup and Cursor Craft against near-identical tasks, same starting Git revision and machine, same environment and explicit approval state. Model Auto selection can change between runs; record it when visible and avoid overclaiming causality.

## Metrics

- Delivered acceptance criteria: pass/fail, not an Agent's self-rating.
- Severe defects/regressions, unresolved security issues and verified test coverage.
- Maintainability and architecture quality: independent reviewer with a rubric, ideally blinded to variant.
- For design: quality of reasoning, originality, task suitability, actual accessibility/interaction and measurable UX failures. Human review complements automated checks.
- Elapsed time, number of attempts/tool calls, avoidable repeated scans and retries.
- Token usage broken down, **when available**, into fresh input, cached reads, cached writes and output. Do not equate cached reads with expensive fresh input.
- Task completions per total measured cost and quality, rather than token count alone.

## Method

1. Select multiple matched tasks at simple, medium and high complexity.
2. Keep original test repo immutable and create separate clean working copies for each variant.
3. Prespecify success criteria before running, capture reproducible logs and failed runs.
4. Record Cursor version, access plan, Auto model variability, instructions already present and external services.
5. Run enough repetitions to distinguish noise; never generalize from one task.
6. Compare resource use **only among comparable quality outcomes**. A shortcut that skips essential verification is a failure, not a win.
7. Publish aggregate evidence, limitations and anonymized logs without secrets or private workspace content.

A 15% token reduction may serve as an exploratory engineering hypothesis, **not** a guaranteed product feature or release gate. Never promise hard context/cost limits the Cursor runtime doesn't expose.

## Local measurement parser (V0.5)

A standard-library-only tool is included for interpreting **user-measured**, matched runs. It does not connect to Cursor, collect token data, estimate token counts, access the network, or write telemetry.

Start from [`examples/benchmarks/empty-measurements.json`](../examples/benchmarks/empty-measurements.json). Every `runs[]` entry must have:

| Field | Meaning |
| --- | --- |
| `task_id` | Stable identifier for the same task |
| `environment_key` | Owner-supplied exact environment identity (OS, Cursor and project revision, hardware, model/Auto setting) |
| `prompt_revision` | Same evaluation prompt and acceptance criteria |
| `variant` | `baseline` or `candidate` |
| `functional_pass` | Actual acceptance result, Boolean |
| `critical_violations` | Measured unresolved blockers/violations, nonnegative integer |
| `elapsed_seconds` | Measured elapsed seconds |
| `fresh_input_tokens` | Uncached/fresh input token count *as reported* |
| `cache_read_tokens` | Cached-read count *as reported* |
| `cache_write_tokens` | Cached-write count *as reported* |
| `output_tokens` | Output token count *as reported* |

Execute:

```bash
python tools/compare_runs.py examples/benchmarks/empty-measurements.json
```

With an empty template, the result states `"measured": false`. A pair is compared only when task, environment and prompt identifiers match, both variants have equal repetition counts, and values are well-formed. The tool separately prints token categories and sets `quality_regression_flag` if the baseline passed its gate but the candidate did not. It **does not calculate a token-saving percentage or cost** because cached token pricing and hidden tool overhead differ, and runtime observability varies. Use a real cost export and independent outcome review for such claims. A user-entered success flag by itself is not proof of a test.

Human product quality scoring is described in [professional-quality-rubric.md](professional-quality-rubric.md). It must accompany any quality or efficiency comparison; the parser cannot judge the actual code.
