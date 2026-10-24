# Maintainer publication checklist (V0.5.0 pre-release)

**Status: GitHub alpha source may be published only with owner approval after source ownership/security review. NOT APPROVED as a stable or marketplace-verified release.** A valid source ZIP is not proof that Cursor executes the instructions as expected. No GitHub account or local Cursor installation is controlled by this repository.

## Before any public alpha tag

- [ ] Confirm correct ownership and copyright wording for `LICENSE` and README. Only original/authorized source included.
- [ ] Decide and test a private vulnerability intake channel; see `SECURITY.md`.
- [ ] Inspect `plugin.json` against the current official Cursor plugin format.
- [ ] Run `python tools/validate_package.py` and `python -m unittest discover -s tests -v`.
- [ ] Inspect resulting ZIP and its SHA-256 checksum (produced by `tools/build_release.py`).
- [ ] Enable Actions on GitHub only after reviewing workflow permissions and pinned dependencies.
- [ ] Ensure documentation makes no claims about successful Cursor runtime tests or verified performance savings.
- [ ] Obtain explicit consent from the owner to publish repository or release; no automatic pushes.

- [ ] Confirm runtime evidence template remains `NOT_RUN` in the distributed source; actual case data lives privately.
- [ ] Run `python tools/release_readiness.py examples/runtime-acceptance-template.json` to confirm the initial state is unmeasured.

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
