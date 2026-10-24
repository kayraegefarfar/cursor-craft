---
name: task-handoff
description: Use when a long implementation needs an accurate compact handoff, session/context transition, stalled-work recovery or meaningful decision-memory checkpoint. Avoid on short routine tasks.
---
# Long Task Handoff & Event-Based Memory

## When needed
- A long approved task crosses a stable milestone or is about to switch sessions.
- Relevant context is getting hard to retrieve, a problem persists, or work is safely blocked.
- Significant architectural decisions, tested root causes or module ownership changed.

## Method
1. Prefer the actual project state, current diff and test logs to memory or earlier chat claims.
2. Write a **compact** handoff only when authorized to write to this project, or return the handoff in chat. Do not alter global config or silently create unrelated files.
3. Record approved goal and scope; completed changes with paths; tested evidence; uncommitted state; significant decisions; known blockers; pending tests; and exact next safe step.
4. Tag critical assertions as `verified` or `unverified`, cite source files/commands and do not include secrets or raw large logs.
5. Reconcile prior handoff against current code before reusing; update only changed facts. Keep project memory separate for each workspace.
6. Suggest a clean new session when context is unwieldy, but do not promise automatic chat transfer or exact remaining token counts.

## Output template
Use [template.md](template.md) in this Skill directory. Local installation copies `skills/`, so the template is available without the repository `docs/` folder. The handoff should be practical enough to resume without rereading the entire chat, and small enough not to inflate every future task.
