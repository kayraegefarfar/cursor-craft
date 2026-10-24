# Publishing the source on GitHub

The public source repository is <https://github.com/kayraegefarfar/cursor-craft>. GitHub publication is not the same as Cursor Marketplace certification, a git tag, or a GitHub Release. This alpha is **not** a proven production-grade automation system. `v0.5.0-alpha` has not been tagged.

## Before creating the repository

1. Review source ownership and confirm the MIT copyright statement is accurate for all included work. Replace generic maintainer identity and security contact details with your actual project details when available.
2. Review `SECURITY.md`, `LICENSE`, `.github/workflows/validate.yml`, and the four `SKILL.md` files. Never publish secrets, private project code, personal Cursor settings or test logs.
3. Run `python tools/validate_package.py` then `python -m unittest discover -s tests -v`. Those are **static checks only**.
4. Test the local plugin in Cursor and record real acceptance evidence before claiming verified runtime support. See [release gates](release-gates.md).
5. Review the proposed public GitHub repository name, license attribution, and visibility before making it public.

## Source repository layout

The **contents of the extracted `cursor-craft/` folder are the repository root**. Keep `.cursor-plugin/`, `.github/`, `rules/`, `skills/`, `tools/`, `tests/` and documentation at the root. Do not commit an enclosing download kit directory.

Suggested GitHub description:

> Cursor Craft — open-source, risk-adaptive engineering, original interface design, authorized analysis, and evidence-based quality workflows for Cursor.

Suggested topics: `cursor`, `cursor-plugin`, `agent-skills`, `developer-tools`, `code-quality`, `ui-ux`.

## Ways others may install

**Local user-scope preview (cross-platform):** download/clone, inspect source, then follow [installation](installation.md) for the local plugin path. On Windows, macOS and Linux, `~/.cursor/plugins/local/cursor-craft` resolves under the current user home. Local imports may be restricted by workplace policy.

**GitHub repository import:** Cursor documentation describes importing a repository marketplace that has `.cursor-plugin/marketplace.json`. This repo includes one entry whose `source` is `.`, the repository root. The documented resolver then reads `<source>/.cursor-plugin/plugin.json`, which is this repository's manifest. Actual importer behavior must be verified in a real Cursor session before promising one-click installation.

**Cursor Marketplace:** optional later submission via https://cursor.com/marketplace/publish; Cursor reviews each submission. Do not imply listing before approval.

## Source archive

`python tools/build_release.py --output ../cursor-craft-v0.5.0-alpha.zip`

Verify with `python tools/verify_archive.py ../cursor-craft-v0.5.0-alpha.zip`. SHA-256 is a corruption/integrity check, **not** an authenticity signature.

## Versioning and claims

Use pre-release tags until real Cursor behavior, portability, coexistence, safe removal, accessibility and representative quality benchmarks are checked. Static test counts do **not** certify agent behavior, token savings or marketplace compatibility. Publish GitHub alpha only with clear limitations and explicit owner authorization.
