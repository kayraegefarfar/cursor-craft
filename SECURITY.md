# Security policy

**Supported stable releases:** none. The public repository is <https://github.com/kayraegefarfar/cursor-craft>. It currently contains the v0.5.0-alpha source preview only. That preview is an experimental Cursor plugin, not a production security product. No git tag or GitHub Release has been published.

## Reporting a vulnerability

Do not open a public GitHub issue, pull request, or discussion for a suspected vulnerability. Do not include credentials, private project code, access tokens, or a working exploit in any public text.

Use GitHub Private Vulnerability Reporting when it is available: repository **Security** tab, then **Report a vulnerability**. Reports stay private between the reporter and the maintainers. This project will acknowledge a private report as soon as practical and will not ask the reporter to move proof-of-concept details into a public issue.

Private vulnerability reporting was **disabled** when last checked on 2026-10-24. Until a maintainer enables it, this repository has no private security inbox. Do not send vulnerability details to a personal address or a public issue in the meantime.

Maintainer action, which changes a GitHub security setting and therefore needs the owner's approval:

1. Open `kayraegefarfar/cursor-craft` → **Settings** → **Advanced Security** (or **Code security**).
2. Enable **Private vulnerability reporting**.
3. Confirm the Security tab shows **Report a vulnerability**.

## Scope

Cursor Craft bundles prompt, rule, and Skill guidance plus optional local-only Python inspection tools from the standard library. Normal plugin use does not enable an MCP server, install hooks, execute an external analyzer, or send telemetry. The Python tools run only when someone explicitly invokes them.

In scope for a private report:

- A flaw in the packaged rules, skills, or Python tools that can cause unintended secret disclosure, unsafe archive extraction, or execution of repository content as instructions.
- A release or archive build that includes credentials, private project files, or an undisclosed executable component.

## Out of scope

- Limitations of natural-language instructions. They are not a sandbox or a complete prompt-injection defense.
- Behavior of Cursor itself, of optional third-party tools such as `morluto/rea`, or of plugins the user installed separately.
- Findings that require access to a private user project.

## Limitations

Runtime behavior depends on Cursor and on operating-system permissions. Do not place valuable data or secrets in experimental test workspaces. Obtain the owner's permission before risk-bearing steps.
