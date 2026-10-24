# Maintainer engineering review — release boundaries

This is a human review checklist for the **source code**, not a claim of an audited product. No network, user account or Cursor permissions are used by the included tools.

## Threat model and release controls

| Surface | Threat | V0.5 mitigation | Not guaranteed |
| --- | --- | --- | --- |
| Always-on instructions | Unexpected impact on unrelated projects | One short core rule; scope and manual installation docs | Prompt priority and behavioral enforcement |
| Skills | Wrong Skill selection, excessive context | Explicit use/exclude descriptions; 18 policy routing scenarios | Cursor model picks the right skill every time |
| External repositories | Prompt injection and arbitrary commands | Treat as untrusted *data*, avoid executable analyzers by default | Model always obeys instruction hierarchy |
| Optional REA tools | Malware, permissions, licensing | No bundled MCP, no automatic installation; authorization/isolation guidance | Safety of tools installed by user |
| Existing configurations | Conflicting duplicated rules | Read-only optional name-level audit; manual conflict review | Detection of actual user's full setup |
| Local benchmark exports | Private user/project data | Explicit local file input, no network; cached tokens separate | Values supplied are accurate or complete |
| Runtime evidence | Fabricated pass claims | Opaque evidence IDs + reviewer/environment required for PASS | Authenticity of referenced evidence |
| Source archives | Unsafe file inclusion or path traversal | Bounded source validator, symlink rejection, deterministic ZIP | External GitHub or client installer integrity |

## Maintainer acceptance before stable release

- Inspect actual source permissions, project/third-party licenses, origin and provenance; do not reuse user-installed packs without a documented right to redistribute.
- Check the specific Cursor version and install flow against current official docs; an offline JSON/YAML parser is only an approximation, not Cursor's parser.
- Validate policy conflicts with real installed rules and Skills in an isolated opt-in scope, and test removal without changing anything else.
- Review T01–T12 real runs and failures. Assess Design Studio output visually and via interaction, not just by reading the Skill.
- Check that target application tests, regression tests and security/permission boundaries behave correctly in practice.
- Compare matched baseline/candidate runs, including failed trials and separate fresh/cache-read/cache-write/output token counts; do not assert savings without observed evidence.
- Obtain explicit repository owner confirmation for the final license notice, security intake channel, intended publication, repository visibility and release wording.

**Current position:** Source-only alpha with offline validation; not cleared for stable public release.

### V0.5 archive verification

The new source archive includes file hashes, size limits and portable paths. It cannot prove maintainer authenticity or the absence of malicious but syntactically valid code. Verify with `tools/verify_archive.py`, confirm a trusted release origin, then review the actual source; never run untrusted hook scripts or external analyzers automatically.
