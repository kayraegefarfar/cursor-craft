# Static check evidence (local source preflight)

- Review date: **2026-10-24**
- Local Python: **3.13.5** (Linux sandbox)
- `python tools/validate_package.py` → **PASS**
- `python -m unittest discover -s tests -v` → **49 tests passed**
- `python tools/release_readiness.py examples/runtime-acceptance-template.json` → **12 NOT_RUN; 0 PASS** (expected)
- `python tools/build_release.py --output ../cursor-craft-v0.5.0-alpha.zip` → **PASS** after source validation
- Clean extracted source was also verified and rebuilt byte-identically in local tests. ZIP structural, SHA-256 file manifest and integrity via `python tools/verify_archive.py <zip>` → **PASS** (offline)

Test groups: malformed manifests/rules/skills, duplicate JSON keys, unsafe filenames and links, Windows-insensitive name collisions, untrusted-source policy examples, archive reproducibility, negative benchmark values, privacy-preserving runtime attestation schema and alpha optional-tool boundaries.

**Not checked:** actual Cursor plugin loading, real specialist selection, tool permissions, OS-specific compatibility, UI output, behavioral safety, claimed token savings or an optional REA executable. CI has not yet run on GitHub. A local checker passing is not a security audit.

The new archive verifier rejects unsafe names, ZIP slip, symlink entries, content tampering and Windows path collisions. The release builder refuses to overwrite an existing file. Windows CI job is configured but **not yet executed on GitHub**.

Tests should be rerun on the final archive contents and the documented number updated for each new release.
