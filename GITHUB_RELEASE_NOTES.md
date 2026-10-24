# Cursor Craft v0.5.0-alpha — English source preview

Cursor Craft is an **open-source Cursor Plugin** for risk-adaptive engineering workflows, original UI/UX design, evidence-based quality reviews, authorized software analysis and concise task handoffs.

## In this alpha

- One compact, always-on engineering rule and four on-demand Skills.
- English-only documentation and installation request, intended for international users.
- Cross-platform manual local-plugin preview instructions.
- Experimental single-plugin GitHub marketplace descriptor.
- Offline source validation, reproducible ZIP archive creation and integrity checks.
- No bundled MCP service, active hooks, telemetry, automatic downloads or remote publication.

## Verification status

The included Python static test suite has been checked locally. **Actual Cursor plugin discovery, agent routing, UI/UX outcomes, operating-system compatibility and token savings have NOT been validated.** Treat this as an experimental alpha, not a proven production release.

## Quickstart

1. Read [`README.md`](README.md), [`docs/installation.md`](docs/installation.md) and [`SECURITY.md`](SECURITY.md).
2. Review existing Cursor Rules/Skills/Plugins for overlap.
3. Run `python tools/validate_package.py` and `python -m unittest discover -s tests -v` with Python 3.10+ if available.
4. Use a disposable project for the first local user-scope preview and record actual results.

> GitHub source publication and Cursor Marketplace approval are separate. Publishing a GitHub alpha should not be described as an approved Marketplace listing.
