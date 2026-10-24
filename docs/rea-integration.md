# Optional REA analysis engine

The `rea-workflow` Skill functions as a policy for targeted, authorized software analysis using tools that already exist. No third-party engine is bundled.

One **candidate** is https://github.com/morluto/rea, which documents a CLI/MCP workflow and multiple analyzer backends. Using that project requires a **separate user choice** and version-specific compatibility, security, permission and license review. Its own MIT license does not automatically govern Ghidra, JADX or other providers.

## When to consider an external engine

- Compiled Electron, .NET, native or APK artifact analysis where regular source inspection cannot answer a specific authorized question.
- Authorized application behavior tracing where appropriate tool isolation exists.
- A specific difficult source-analysis problem with measurable added benefit.

## Before enabling one

1. Identify the target artifact, authority and least-privilege environment.
2. Verify the chosen engine release, OS compatibility, providers and safe operation mode.
3. Inspect dependencies, provider licenses and requested permissions.
4. Obtain explicit approval for new installations, MCP configuration or risky execution.
5. Start with a bounded static read-only task and keep a concise evidence packet.
6. Demonstrate that analyzed data does not make the Agent execute embedded instructions.
7. Compare actual value and context cost with built-in source inspection.

**No integration or analyzer execution is included in v0.5.0-alpha.**
