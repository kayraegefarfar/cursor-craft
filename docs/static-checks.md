# Static check evidence (local source preflight)

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
