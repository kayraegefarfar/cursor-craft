# v0.5.0-alpha prerelease checklist

**Source repository:** public at <https://github.com/kayraegefarfar/cursor-craft>
**Git tag `v0.5.0-alpha`:** not created
**GitHub Release:** not created
**Cursor Marketplace:** not submitted

A valid source ZIP is not proof that Cursor executes the instructions as expected. Do not create the tag, the GitHub Release, or a Marketplace submission until the owner explicitly approves that action.

## Already true for the public source

- [x] The source repository is public and includes the MIT license.
- [x] `plugin.json` uses name `cursor-craft` and version `0.5.0-alpha`. That prerelease form matches the Cursor plugin semver pattern. The git tag, if created later, would be `v0.5.0-alpha`; the leading `v` is not part of the manifest.
- [x] Marketplace `source` is `.`, the repository root. Documented resolution reads `<source>/.cursor-plugin/plugin.json`.
- [x] No hooks, MCP server, or agents are bundled.
- [x] The workflow requests `contents: read` and pins `actions/checkout`. Actions run `40132211291` passed on `ubuntu-latest` and `windows-latest` for commit `43262f5`.
- [x] Documentation does not claim Cursor runtime discovery or measured token savings.

## Still required before tagging v0.5.0-alpha

- [ ] Owner explicitly authorizes the annotated tag and a GitHub prerelease.
- [ ] Enable GitHub Private Vulnerability Reporting. It was disabled on 2026-10-24. See `SECURITY.md`. Enabling it changes a repository security setting.
- [ ] Confirm the copyright line is the wording the owner wants to keep. It currently says "Cursor Craft contributors".
- [ ] Re-run `python tools/validate_package.py` and `python -m unittest discover -s tests -v` on the commit that will be tagged.
- [ ] Build the ZIP outside the repository, verify it, and put the archive SHA-256 only in release text the owner approves.
- [ ] Confirm the tagged commit's Actions run is green on both Ubuntu and Windows. The `8902ca8` run does not cover later commits.
- [ ] Confirm the bundled runtime evidence template is still `NOT_RUN` only: `python tools/release_readiness.py examples/runtime-acceptance-template.json`.

## Not part of this alpha tag

- [ ] Cursor Customize discovery of one rule and four skills.
- [ ] Behavioral cases T01–T12.
- [ ] Marketplace review.

## Before declaring stable V1

- [ ] Install only in a disposable test scope and verify plugin/rule/skill discovery.
- [ ] Test coexistence and safe removal with at least one nontrivial existing Cursor configuration.
- [ ] Run T01–T12 behavioral acceptance cases; store **redacted** evidence, failures included. Use the [runtime evidence protocol](runtime-evidence.md); the checker alone cannot verify authenticity.
- [ ] Check design result through actual UI interactions and screen renders, not prompt claims.
- [ ] Check authorizations, privacy boundaries, security controls and README prompt-injection behavior using harmless mock fixtures.
- [ ] Verify optional REA tools are *not required* for built-in source analysis.
- [ ] Test Windows, macOS and Linux only if the project claims support for them.
- [ ] Run paired baseline/candidate benchmark tasks with environment and model info recorded.
- [ ] Inspect critical defects, rollback results, licenses, security channel and independent review.

## User data boundary

Do not commit installation inventories, private project code, logs, API credentials, local paths, or benchmark recordings from a user's personal workspace without explicit review and redaction. Never auto-upload diagnostics.

## Publishing channels

A GitHub repository release and Cursor Marketplace listing are **different actions**. Marketplace requires its own process and review. Neither is authorized by the existence of this document.

- [ ] Check the produced ZIP with `tools/verify_archive.py`, compare its SHA-256 with the trusted release announcement, and confirm the source provenance.
- [ ] Review GitHub CI Linux **and Windows** results, not only local test success.
- [ ] Ensure the release builder did not overwrite an unrelated existing file.
