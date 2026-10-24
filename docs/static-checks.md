# Static check evidence (local source preflight)

- Review date: **2026-10-24**
- Local Python: **3.15.0** (Windows)
- `python tools/validate_package.py` → **PASS**
- `python -m unittest discover -s tests -v` → **56 tests; 55 passed, 1 skipped** because this Windows account cannot create a symlink
- `python tools/release_readiness.py examples/runtime-acceptance-template.json` → **12 NOT_RUN; 0 PASS** (expected)
- Two release ZIPs built outside the repository were byte-identical. `python tools/verify_archive.py` reported `integrity_verified: true` and `runtime_verified: false`. The archive hash is not copied into this file, because this file is part of the archive.

Test groups: malformed manifests/rules/skills, duplicate JSON keys, unsafe filenames and links, Windows-insensitive name collisions, untrusted-source policy examples, archive reproducibility, negative benchmark values, privacy-preserving runtime attestation schema and alpha optional-tool boundaries.

**Not checked:** actual Cursor plugin loading, real specialist selection, tool permissions, UI output, behavioral safety, claimed token savings or an optional REA executable. A local checker passing is not a security audit.

GitHub Actions run `40111616058` passed on `ubuntu-latest` and `windows-latest` for commit `8902ca8`. That run does not cover later unpushed commits. The archive verifier rejects unsafe names, ZIP slip, symlink entries, content tampering and Windows path collisions. The release builder refuses to overwrite an existing file.

Tests should be rerun on the final archive contents and the documented number updated for each new release.
