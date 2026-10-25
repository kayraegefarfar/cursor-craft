# Development and verification status

**Review date:** 2026-10-25
**Version:** 0.5.0-alpha
**Repository state:** Local development based on public-source commit `80c6001`, with uncommitted improvements. No publication was performed during this review. The owner reports several days of successful use; exact build, revision and per-case coverage were not recorded. See [runtime evidence](runtime-evidence.md) for that report and the separately labeled historical installation mismatch. The current global installation was not inspected.

## Verifiable in this workspace

An uncommitted development update based on `80c6001` adds a read-only payload
comparator and a [runtime validation runbook](runtime-validation.md). These
prepare validation without accessing global Cursor configuration. They do not
close any Cursor runtime gate. See [static checks](static-checks.md) for current
local results; the earlier CI record above does not validate this update.

The update also rejects source links/reparse points before reading content and
rejects ambiguous runtime-attestation JSON. A real Windows junction fixture was
verified; two symlink checks remain unavailable under this host's permissions.

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

The owner reported successful use in normal projects over several days on
2026-10-25. Build, source revision and individual case coverage were not recorded;
the items below remain pending independent or case-level verification, rather
than a claim that nobody has used the plugin.

- Actual Cursor local plugin loading, UI visibility, real Rule/Skill routing, Windows/macOS/Linux compatibility.
- Runtime tool authorization or prompt injection resistance.
- Actual engineering/design results, performance, security of outside analysis tools.
- Token budget effectiveness, session handoff reliability or quality improvement.
- Coexistence with the owner's current active global configuration and safe removal.

## Required for publication

See [release gates](release-gates.md), [manual acceptance cases](acceptance-tests.md), and [publication checklist](publication-checklist.md). No push, installation, automatic remote access or Marketplace submission is implemented in this source package.
