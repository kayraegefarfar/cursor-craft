# Real Cursor acceptance evidence (no telemetry)

**Owner-reported practical use is available; case-level runtime evidence is not yet recorded.** On 2026-10-25 the owner reported using Cursor Craft in normal projects for several days and said the features worked. The Cursor build, OS, exact source revision and individual Skill/test coverage were not supplied. This is useful user feedback, not a captured T01–T12 acceptance run. No logs or screenshots were supplied or inspected. Do not infer all four Skills or all approval boundaries passed from this report.

The source linter, static routing cases and offline tests cannot prove real Agent behavior. The test data in `examples/runtime-acceptance-template.json` remains an unused template with every case marked `NOT_RUN`; it does not negate the owner's reported practical use.

On 2026-10-25, commit `43262f5` was checked again. GitHub Actions run `40132211291` passed its Ubuntu and Windows static jobs. T01–T12 were left `NOT_RUN`. A local plugin directory existed, but its rule and Skill files did not match that commit and the handoff template was absent. The directory was not replaced, so no Cursor discovery, Skill selection, approval, or handoff session was run.

## Test protocol (manual, opt-in)

Use the [runtime validation runbook](runtime-validation.md) for payload identity,
discovery provenance, fresh-chat routing checks and evidence capture. File
equality, discovery and behavior are separate gates. A disposable project alone
does not isolate global plugin storage; use an authorized disposable OS account
or VM when the owner's global configuration must remain untouched.

1. Use a **disposable project and clean Cursor test scope**, not the user's existing projects or global configuration. Record the Cursor build, OS, selected model/Auto settings, project revision and other applicable rules or plugins as an opaque `environment_key`.
2. Run each T01–T12 case from [acceptance-tests.md](acceptance-tests.md), capturing **real** diffs, console results, approval decisions and tool traces locally. If no test was executed, leave it `NOT_RUN`.
3. Record private logs **outside the public repository**. Check them for private source code, filesystem paths, tokens, credentials, screen content, or personal data before considering any redacted public example.
4. Assign each reviewed local evidence item an opaque `EV-...` reference (e.g., `EV-CASE01-A`). The example JSON contains IDs only, **not the evidence bytes**. Set `reviewer` to a real reviewer identifier (not `test`), `environment_key` to the actual recorded environment, and `status` to `PASS`, `FAIL` or `BLOCKED` as justified. A claim of `PASS` with no evidence reference is rejected by the checker.
5. Run `python tools/release_readiness.py path/to/acceptance.json`. It checks **completeness and structural consistency**, not whether the claimed behavior really happened. Independent reviewers must inspect the private evidence and sign off separately.
6. Treat failing, blocked or not-run cases as open release gates. Do not publish a stable release by silently omitting negative evidence.

## Release boundaries

The attestation reader rejects duplicate JSON fields and requires an integer
schema version. This prevents ambiguous input interpretation; it does not prove
that a supplied PASS or its evidence references are authentic.

- No script here launches Cursor, modifies user rules, executes third-party binaries or contacts GitHub.
- Runtime evidence should be gathered only after the user approves setup, and publication still requires an explicit separate owner decision.
- Even 12/12 human-claimed `PASS` does **not** authorize release or certify real security, creativity, test quality or token savings.
- Do not embed confidential screenshots, logs, local inventory or token exports in a public issue or pull request without consent and redaction.
