# Cursor Craft

A small Cursor plugin for careful software work: one always-on engineering rule and four on-demand Skills. The main Cursor Agent stays in charge. Skills add procedure only when the task needs them.

Public source: <https://github.com/kayraegefarfar/cursor-craft>

Manifest version: `0.5.0-alpha`. A later git tag would be named `v0.5.0-alpha`; the leading `v` is not part of `plugin.json`. This repository is not a GitHub Release and not a Cursor Marketplace listing.

## What you get

| Piece | When the main Agent should use it | What it does not do |
| --- | --- | --- |
| `professional-core` | Every task | It does not replace Cursor permissions or run tests by itself |
| `design-studio` | A new screen, visual identity, or substantial interaction redesign | Minor CSS, copy, or spacing edits |
| `rea-workflow` | Authorized inspection of code or a permitted application before integrating behavior | Casual navigation of the current repository |
| `deep-quality-review` | A risky change, a serious regression, or a pre-release review | Routine typo fixes |
| `task-handoff` | A long task needs a compact resume note | Short tasks that already fit in the current chat |

Examples:

- "Rename this label" stays with the main Agent.
- "Redesign the onboarding flow" calls `design-studio`.
- "How does this owned desktop build implement export, and what can we safely reimplement?" calls `rea-workflow`.
- "Review this migration before release" calls `deep-quality-review`.
- "I am stopping for today; leave a resume note" calls `task-handoff`.

You can also invoke a Skill directly, when Cursor supports it: `/design-studio`, `/rea-workflow`, `/deep-quality-review`, `/task-handoff`. Selection from ordinary language is heuristic.

The package has no hooks, no MCP server, no telemetry, and no installer that edits Cursor settings. `morluto/rea` is an optional external tool, not included here.

## Install

Full steps, Windows paths, and the stop conditions are in [docs/installation.md](docs/installation.md). Summary:

1. Clone or download this repository and read the source.
2. If `~/.cursor/plugins/local/cursor-craft/` already exists, stop. Do not overwrite it.
3. Copy only `.cursor-plugin/plugin.json`, `rules/`, `skills/`, and `LICENSE` into a new `~/.cursor/plugins/local/cursor-craft/` directory.
4. Reload Cursor and look in Customize for one rule and four Skills.

`skills/task-handoff/template.md` is included in that copy. The `docs/` directory is not.

## Remove

If Cursor installed the plugin, disable it from Customize. If you copied it yourself, delete only `~/.cursor/plugins/local/cursor-craft/` when that folder has no files you added, then reload Cursor. Removal does not undo edits already made in projects.

## Verification status

Offline package checks and GitHub Actions run `40132211291` for commit `43262f5` passed on Ubuntu and Windows. Those checks do not show that Cursor loads the plugin, chooses the right Skill, or saves tokens.

Cursor runtime scenarios for discovery, trivial routing, each Skill, and approval boundaries are **NOT_RUN** in this revision. The bundled evidence file stays `NOT_RUN` until a real Cursor session records results. See [docs/runtime-evidence.md](docs/runtime-evidence.md) and [docs/acceptance-tests.md](docs/acceptance-tests.md).

## Limitations

- Instructions cannot force operating-system permissions, model routing, or isolation.
- No measured quality or token improvement is claimed.
- Behavior depends on the Cursor version and on rules you already have. Do not replace those rules from this package.
- Inspecting a compiled application needs the owner's authorization. This plugin does not bundle an analyzer.

## Maintainer documentation

- [Architecture](docs/architecture.md)
- [Release gates](docs/release-gates.md)
- [Publication checklist](docs/publication-checklist.md)
- [Static checks](docs/static-checks.md)
- [Archive integrity](docs/archive-integrity.md)
- [Security model](docs/security-model.md)
- [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [CHANGELOG.md](CHANGELOG.md), [LICENSE](LICENSE)

Offline checks, Python 3.10+, no network:

```bash
python tools/validate_package.py
python -m unittest discover -s tests -v
```
