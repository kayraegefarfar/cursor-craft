# Changelog

## 0.5.0-alpha — 2026-10-24

- Ship the task-handoff template inside the Skill, and describe the main Agent instead of agents that are not in the package.
- Record the public repository in the security policy and use `0.5.0-alpha` in the Cursor manifests, which accept that prerelease form.
- Keep published source as LF on Windows so `SOURCE-MANIFEST.sha256` matches checkout, and test case-only filename collisions without requiring two directory entries.
- Prepared English-only, GitHub-repository-ready source with cross-platform user-scope installation documentation.
- Added one-entry Cursor marketplace manifest for repository import experimentation; **not runtime verified**.
- Replaced the Turkish trial-kit installation handoff with a fully English, opt-in Cursor Agent prompt.
- Added GitHub publication and safer community documentation, while retaining an explicit alpha/runtime-unverified status.
- Removed the Turkish README and updated static tests to check international release metadata.

## 0.4.0-alpha — 2026-10-24

- Added non-extracting, bounded ZIP verifier with embedded SHA-256 file manifest.
- Refuse accidental release ZIP overwrite; stage archive before exclusive final creation.
- Reject non-portable Windows filenames, path traversal and symlink entries.
- Added tampering/ZIP-slip/symlink/overwrite negative tests and cross-platform CI job configuration.
- Documented archive-integrity threat model, Windows CI unverified status and actual runtime limitations.


## 0.3.0-alpha — 2026-10-24

- Added strict offline release evidence attestation checker with twelve deliberately unrun Cursor acceptance cases. It never grants publication permission or verifies external logs.
- Added runtime evidence procedure and maintainer threat-model review.
- Strengthened source validation: reject duplicate manifest JSON keys, Windows case-fold filename collisions, malformed routing fixture fields, and symlinks without following their contents.
- Expanded Python negative-path tests and CI source reproducibility checks.
- Added a human-reviewed professional craftsmanship rubric with explicit safety and evidence gates.
- Clarified bilingual documentation in the historical alpha and preserved no-install/no-publish defaults.
- No claims of real Cursor runtime behavior, measured token savings or professional UI output.

## 0.2.0-alpha — 2026-10-24

- Hardened dependency-free package validation, including unsafe links, malformed frontmatter, symlinks, unexpected executable components, duplicated routing cases and suspicious filenames.
- Fixed prompt-injection routing test: ignore external hostile instructions **without requesting approval to follow them**.
- Expanded illustrative policy-routing cases from 10 to 18; these are design assertions, **not Cursor runtime passes**.
- Added reproducible, fixed-timestamp source ZIP builder and SHA-256 reporting.
- Added opt-in **ZIP filename-only** legacy overlap audit. It does not inspect or change active Cursor configuration.
- Added conservative paired benchmark data interpreter. No invented observations or token-savings claims.
- Added publication checklist, enhanced bilingual docs and least-privilege CI with full-SHA-pinned checkout.
- No auto-installers, background daemons, executable hooks, MCP servers or special subagents.

## 0.1.0-alpha — 2026-10-24

- Introduced Cursor Plugin manifest and concise always-on engineering rule.
- Added on-demand Design Studio, authorized REA, Deep Quality Review and Task Handoff Skills.
- Documented adaptive routing, controlled autonomy, evidence and trust boundaries.
- Added compatibility, safety, migration, benchmark, acceptance and release-gate documentation.
- Added dependency-free repository validator, tests and optional CI workflow.

**Not included:** actual subagents, hooks, remote services, MCP configurations, live Cursor testing, measured performance or public release.
