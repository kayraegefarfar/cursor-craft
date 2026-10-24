# Real Cursor acceptance evidence (no telemetry)

**There is currently NO runtime evidence in this repository.** The source linter, static routing cases and offline tests cannot prove real Agent behavior. The test data in `examples/runtime-acceptance-template.json` correctly starts with every case marked `NOT_RUN`.

## Test protocol (manual, opt-in)

1. Use a **disposable project and clean Cursor test scope**, not the user's existing projects or global configuration. Record the Cursor build, OS, selected model/Auto settings, project revision and other applicable rules or plugins as an opaque `environment_key`.
2. Run each T01–T12 case from [acceptance-tests.md](acceptance-tests.md), capturing **real** diffs, console results, approval decisions and tool traces locally. If no test was executed, leave it `NOT_RUN`.
3. Record private logs **outside the public repository**. Check them for private source code, filesystem paths, tokens, credentials, screen content, or personal data before considering any redacted public example.
4. Assign each reviewed local evidence item an opaque `EV-...` reference (e.g., `EV-CASE01-A`). The example JSON contains IDs only, **not the evidence bytes**. Set `reviewer` to a real reviewer identifier (not `test`), `environment_key` to the actual recorded environment, and `status` to `PASS`, `FAIL` or `BLOCKED` as justified. A claim of `PASS` with no evidence reference is rejected by the checker.
5. Run `python tools/release_readiness.py path/to/acceptance.json`. It checks **completeness and structural consistency**, not whether the claimed behavior really happened. Independent reviewers must inspect the private evidence and sign off separately.
6. Treat failing, blocked or not-run cases as open release gates. Do not publish a stable release by silently omitting negative evidence.

## Release boundaries

- No script here launches Cursor, modifies user rules, executes third-party binaries or contacts GitHub.
- Runtime evidence should be gathered only after the user approves setup, and publication still requires an explicit separate owner decision.
- Even 12/12 human-claimed `PASS` does **not** authorize release or certify real security, creativity, test quality or token savings.
- Do not embed confidential screenshots, logs, local inventory or token exports in a public issue or pull request without consent and redaction.
