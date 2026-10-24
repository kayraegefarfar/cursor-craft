# Development and verification status

**Review date:** 2026-10-24
**Version:** 0.5.0-alpha
**Repository state:** Public source at <https://github.com/kayraegefarfar/cursor-craft>. No `v0.5.0-alpha` git tag and no GitHub Release. Cursor Customize discovery remains **NOT_RUN**.

## Verifiable in this workspace

- Cursor Plugin manifest JSON and documented folder discovery shape.
- Four named Skill frontmatter sections, one core Rule, internal links and structural requirements.
- Explicitly tested rejection of malformed or unsafe archive content and invalid scenarios.
- Deterministic source archive builder and SHA-256 output; no executable installs.
- Conservative benchmark parser with absent-data state and quality regression flag.
- Runtime acceptance evidence format + non-authorizing checker, all bundled test cases explicitly `NOT_RUN`.
- Duplicate JSON key and Windows-insensitive filename collision detection.
- Opt-in archive filename overlap audit; not actual installed Cursor inventory.
- Repository contains **no** executable hooks, bundled MCP analyzer or special subagent.

The exact local test commands and counts must be recorded **after each actual execution**; passing package tests are not Cursor runtime tests.

## Not yet verified

- Actual Cursor local plugin loading, UI visibility, real Rule/Skill routing, Windows/macOS/Linux compatibility.
- Runtime tool authorization or prompt injection resistance.
- Actual engineering/design results, performance, security of outside analysis tools.
- Token budget effectiveness, session handoff reliability or quality improvement.
- Coexistence with the owner's current active global configuration and safe removal.

## Required for publication

See [release gates](release-gates.md), [manual acceptance cases](acceptance-tests.md), and [publication checklist](publication-checklist.md). No push, installation, automatic remote access or Marketplace submission is implemented in this source package.
