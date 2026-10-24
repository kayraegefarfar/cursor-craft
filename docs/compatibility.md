# Compatibility and known boundaries

**Documentation review date: 2026-10-24.** This file describes expectations, not a verified compatibility matrix.

| Concern | Status |
| --- | --- |
| Cursor Plugin manifest `.cursor-plugin/plugin.json` | Uses documented format; local loading not yet tested |
| Rules in `rules/*.mdc` | Uses documented frontmatter; real application not yet verified |
| Four skills at `skills/*/SKILL.md` | Uses documented required fields; discovery not yet runtime-tested |
| Built-in Cursor Auto model selection | Unmodified; exact model routing is controlled by Cursor |
| Subagent-specific models or parallelism | No subagents shipped; no unsupported routing promises |
| Windows, macOS, Linux | Text components may be portable; test on each before claiming support |
| Cloud Cursor use | Unverified; check which personal/project plugins sync or load |
| Existing Skills/Rules | Can conflict; user must inspect before enabling |
| External MCP / `morluto/rea` | Optional, not installed or configured here |
| Offline behavior | Instructions and static checks require no internet; some tasks might |

Official references:
- https://cursor.com/docs/plugins
- https://cursor.com/docs/reference/plugins
- https://cursor.com/docs/rules
- https://cursor.com/docs/skills

Important: prompt guidance cannot guarantee reproducible LLM behavior, automatic token capping, cross-session continuity or technical sandboxing. Features not supported by a user's current Cursor version should not be represented as working.
