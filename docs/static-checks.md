# Static check evidence (local source preflight)

## Local development update — 2026-10-25

Based on `80c6001`, with uncommitted installation-comparison and runtime-runbook
changes. On 2026-10-25, Windows / Python 3.15.0: package validator PASS; 81 tests
ran, 79 passed, and 2 symlink tests skipped because this account lacks symlink
privileges.
The source pre-read boundary and installation comparator also passed a real
Windows junction test outside the execution sandbox, using disposable fixture
directories only. The junction itself was removed and its target preserved.
Mocked metadata additionally verifies rejection before any file-content read.
This is filesystem evidence, not a Cursor session.
Tests used a writable workspace TEMP/TMP directory outside the source tree.
The comparator matched all eight files in an isolated workspace copy, explicitly
reporting `runtime_verified: false`. This was not a global installation check.
The runtime evidence template still reports 12 NOT_RUN and zero PASS. The owner
separately reported successful practical use; see [runtime evidence](runtime-evidence.md).
Four additional regression tests cover malformed benchmark variants and ZIP
file/directory conflicts, including reversed order and case-insensitive paths.
The failing behavior was reproduced before the fixes; all four now pass.
Five later regression tests for finite benchmark averages, unrepresentable
numbers, unsafe overlap paths and original ZIP backslashes are included in that
81-test run.

The two symlink tests were retried with the host user's existing permissions and
still skipped with Windows error 1314. No privilege or Developer Mode setting was
changed. The installed WSL launcher failed with `REGDB_E_CLASSNOTREG`, so no Linux
run was available locally. Ubuntu CI is configured to run the symlink tests, but
the current uncommitted changes have not been run on GitHub Actions. Do not count
the junction test as either skipped symlink test passing.

## Historical source preflight

- Review date: **2026-10-24**
- Local Python: **3.15.0** (Windows)
- `python tools/validate_package.py` → **PASS**
- `python -m unittest discover -s tests -v` → **57 tests; 56 passed, 1 skipped** because this Windows account cannot create a symlink
- `python tools/release_readiness.py examples/runtime-acceptance-template.json` → **12 NOT_RUN; 0 PASS** (expected)
- Two release ZIPs built outside the repository were byte-identical. `python tools/verify_archive.py` reported `integrity_verified: true` and `runtime_verified: false`. The archive hash is not copied into this file, because this file is part of the archive.

Test groups: malformed manifests/rules/skills, duplicate JSON keys, unsafe filenames and links, Windows-insensitive name collisions, untrusted-source policy examples, archive reproducibility, negative benchmark values, privacy-preserving runtime attestation schema and alpha optional-tool boundaries.

**Not checked:** actual Cursor plugin loading, real specialist selection, tool permissions, UI output, behavioral safety, claimed token savings or an optional REA executable. A local checker passing is not a security audit.

GitHub Actions run `40132211291` passed on `ubuntu-latest` and `windows-latest` for commit `43262f5`. Cursor runtime discovery, Skill selection, approval behavior, and task handoff are **NOT_RUN** for that commit. A local plugin directory exists, but its rule and Skill files do not match `43262f5`, and it was not replaced. Static checks do not replace runtime tests. The archive verifier rejects unsafe names, ZIP slip, symlink entries, content tampering and Windows path collisions. The release builder refuses to overwrite an existing file.

Tests should be rerun on the final archive contents and the documented number updated for each new release.
