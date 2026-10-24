# Cursor Craft

**Professional software engineering, original interface design and evidence-first analysis for Cursor.**

> **Status: v0.5.0-alpha, international GitHub source preview.** Package structure and offline checks are prepared, but it has **not** been loaded or behavior-tested inside Cursor. It is **not** a verified production release. GitHub source publication is separate from Cursor Marketplace approval.

Cursor Craft is an intentionally small **Cursor Plugin**, not a new model, background service or a set of automatically executing bots. It equips Cursor's Agent with a compact core rule and specialized, on-demand Skill workflows.

## Why it exists

- **Craftsmanship first.** Deliver maintainable, secure, readable, tested software and thoughtful product experiences—not just code that seems to work.
- **Adaptive orchestration.** Keep simple work with the main Agent. Activate specialists only where they add value.
- **Experimental Design Studio.** Build product-appropriate, imaginative interfaces with intentional visual direction, motion and real usability checks.
- **Authorized REA workflow.** Investigate existing code or permitted applications with transparent evidence and safe, license-aware integration choices.
- **Honest verification.** Separate actual test results from guesses and unrun checks.
- **Efficient context.** Target relevant modules, reuse verified decisions, and checkpoint long tasks without flooding the prompt.

## Contents

| Component | Type | When to use |
| --- | --- | --- |
| `professional-core.mdc` | Always-on short rule | All tasks; scope, safety, engineering quality, evidence |
| `design-studio` | On-demand Skill | Major original UI/UX work and redesigns |
| `rea-workflow` | On-demand Skill | Authorized source/app analysis and integration |
| `deep-quality-review` | On-demand Skill | High-risk review and pre-release validation |
| `task-handoff` | On-demand Skill | Long-task summaries and event-based project memory |

The plugin has **no executable hooks, no automatic file scanning, no built-in MCP server, no telemetry and no destructive installer**. It does not ship any third-party reverse-engineering binary. The `morluto/rea` engine is described as an **optional external candidate**, not a dependency.

## Global use and GitHub distribution

The plugin is designed for **user-scope installation**, where one local plugin is available across Cursor projects, rather than copying Rules or Skills into every project. Installation remains opt-in, reversible, and subject to Cursor policy. It does not guarantee that two unrelated projects will share private project memory.

- **Cross-platform setup:** [Installation guide](docs/installation.md) (Windows, macOS, Linux).
- **Cursor Agent-assisted setup:** [English installation prompt](CURSOR_AGENT_INSTALL_PROMPT.md).
- **Publishing as source on GitHub:** [GitHub publication guide](docs/GITHUB_PUBLISHING.md) and [alpha release notes](GITHUB_RELEASE_NOTES.md).
- **Optional GitHub repository import:** `.cursor-plugin/marketplace.json` provides a single-plugin marketplace descriptor; this path has **not** yet been tested in Cursor.

GitHub users do **not** need the prior private trial kit. The entire repository is in English, and no personal usernames, local configuration, secrets or project-specific assets are bundled.

## How to try it (only when you choose)

1. Review [compatibility and limitations](docs/compatibility.md), [safety model](docs/security-model.md) and existing user/project rules/skills for overlap.
2. Follow the **manual, reversible local preview** in [installation](docs/installation.md). It requires your explicit decision; nothing here modifies your machine by itself.
3. Verify the core rule and `SKILL.md` discovery in Cursor. Try trivial and specialist task prompts, then inspect whether correct skills were selected.
4. Run documented [acceptance scenarios](docs/acceptance-tests.md), recording real results before calling the package production-ready.

Skills may also be called explicitly, e.g. `/design-studio`, `/rea-workflow`, `/deep-quality-review`, or `/task-handoff`, subject to installed Cursor support. Natural-language selection remains heuristic—not guaranteed.

## Offline project checks

Requires only Python 3.10+; no network or dependencies:

```bash
python tools/validate_package.py
python -m unittest discover -s tests -v
```

These tests verify the **repository format and policy consistency**, **not** Cursor agent behavior, UI craftsmanship, Windows compatibility or token savings.

## Architecture

```text
User request
   -> Main Cursor Agent (adaptive decisions + permissions)
         |-- basic coding / project inspection (default)
         |-- design-studio         (when creative UI work warrants it)
         |-- rea-workflow         (when authorized research warrants it)
         |-- deep-quality-review  (when risk warrants deep inspection)
         `-- task-handoff         (when meaningful checkpoint is needed)
   -> risk-based evidence/checks
   -> concise report with verified and unverified portions
```

See [Architecture](docs/architecture.md), [Public release gates](docs/release-gates.md), [reviewer rubric](docs/professional-quality-rubric.md) and [benchmark plan](docs/benchmarks.md).

## Limitations and release status

- Markdown instructions **do not enforce OS permissions**, hard token quotas, automatic agent/model routing, test execution or true isolation.
- No current real-world claims of quality uplift, agent autonomy or resource savings are made.
- Behavior depends on Cursor version, account and runtime tool availability; local testing is required.
- Existing user rules, Skills and Plugins may conflict. Do not mass-copy or overwrite them.
- Analysis of compiled applications requires explicit authorization and appropriate external tools; those are not included.

## Sources and acknowledgements

- [Cursor Plugins](https://cursor.com/docs/plugins) and [Plugins reference](https://cursor.com/docs/reference/plugins)
- [Cursor Rules](https://cursor.com/docs/rules) and [Cursor Skills](https://cursor.com/docs/skills)
- [morluto/rea](https://github.com/morluto/rea) — optional third-party inspiration/tool; **not vendored, installed or reproduced**

## Community

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [CHANGELOG.md](CHANGELOG.md), and [LICENSE](LICENSE).

## V0.5 tooling (continued from V0.3)

- **Read-only overlap audit:** `python tools/overlap_audit.py your-existing-pack.zip` identifies only likely Skill-topic overlaps from explicitly supplied archives. It cannot identify the actual installed Cursor configuration and never merges files.
- **Conservative benchmark parser:** `python tools/compare_runs.py examples/benchmarks/empty-measurements.json` reports `measured: false` until you supply real paired data. Cached token categories remain separate.
- **Reproducible release ZIP builder:** `python tools/build_release.py --output ../cursor-craft-source.zip` validates then packages the repository and prints SHA-256, without installing anything.
- **Publication checklist:** [docs/publication-checklist.md](docs/publication-checklist.md) separates static alpha preparation from actual release authorization and runtime evidence.

The validation suite tests package structure, negative cases, benchmark math and ZIP reproducibility. It **does not** test Cursor-agent decisions, model routing, React/Electron interfaces or UI production quality.

The [requirements trace](docs/requirements-traceability.md) maps each promised capability to its actual source instructions and future runtime test; no behavioral tests are asserted as passed.

## V0.5 maintainer checks (source-only)

- **Runtime evidence attestations:** [`examples/runtime-acceptance-template.json`](examples/runtime-acceptance-template.json) keeps all 12 real Cursor tests at `NOT_RUN`. After opt-in testing, record externally reviewed evidence identifiers in a **private copy** and inspect its structure with `python tools/release_readiness.py path/to/private-acceptance.json`. The checker neither reads evidence nor certifies authenticity; it **never authorizes publication**. See [runtime evidence instructions](docs/runtime-evidence.md).
- **Hardened validation:** rejects duplicate JSON keys, Windows-insensitive path collisions, unsupported plugin components and malformed scenario fields. See [maintainer security review](docs/maintainer-review.md).
- **Reproducibility CI:** checks the evidence template is not a fabricated pass report and confirms two source release ZIPs are byte-identical.

The code is still **source-preview alpha**, not a completed multi-agent runtime, third-party REA integration or measured product-quality improvement.

## V0.5 source archive integrity (no Cursor installation)

- `python tools/build_release.py --output ../cursor-craft-0.5.0-alpha.zip` refuses to overwrite a pre-existing destination and writes a deterministic `SOURCE-MANIFEST.sha256` inside the archive.
- `python tools/verify_archive.py ../cursor-craft-0.5.0-alpha.zip` checks safe relative paths, Windows filename compatibility, file hashes, ZIP checksums, size bounds and symlink-free entries **without extracting**.
- CI includes a Windows and Linux offline-check job. CI execution still requires GitHub; a local pass is not CI evidence.
- The archive manifest is a **corruption detector, not a digital signature**: an attacker controlling both files and hashes could replace both. Only retrieve from a trusted maintainer release.
- See [archive threat model](docs/archive-integrity.md) and [static check limitations](docs/static-checks.md).
