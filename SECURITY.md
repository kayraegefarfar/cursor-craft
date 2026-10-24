# Security policy

**Supported stable releases:** none yet. V0.5.0-alpha is an experimental source package, not a production security product.

To report a suspected vulnerability, do not publish credentials, private project code or working exploits in public issues. When this repository is eventually published, prefer GitHub's private vulnerability reporting feature **if enabled**. A maintainer must confirm a private contact channel before a public release; none is configured here.

## Scope

Cursor Craft bundles prompt/rule/Skill guidance and optional **local-only** standard-library inspection tools. It does not enable MCP services, execute analyses, install hooks or send telemetry during normal plugin use. Repository test tools execute only when someone explicitly runs them.

## Limitations

Natural-language instructions are not a sandbox, policy engine or perfect prompt-injection defense. Runtime behavior requires independent verification in Cursor and actual operating-system permissions. Do not place valuable data or secrets in experimental test workspaces. Always obtain owner permission for risk-bearing steps.
