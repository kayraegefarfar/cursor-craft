# Architecture and operating contract

Cursor Craft is a **policy-and-workflow plugin**, not an orchestrator daemon. The existing Cursor Agent does the actual routing. The instructions describe desired behavior; any advanced capability must be supported by actual Cursor tools and verified in the target runtime.

## Layers

1. **Core rule (`rules/`)**: Brief, frequent instructions for safety, professional judgment, scope and evidence.
2. **Optional Skills (`skills/`)**: Deeper instructions pulled in only when relevant; skill choice is heuristic and can be manual.
3. **Project truth**: The code, tests, accepted architecture and project-specific Design DNA—not an unverified prior AI summary.
4. **Tool boundary**: Terminal/browser/MCP permissions enforced by the environment, not by text promises. No hooks, MCP or special agents ship in alpha.

## Task state machine

`INTAKE → SCOPED → [PLAN → AWAITING_APPROVAL] → EXECUTING → VERIFYING → COMPLETED`

`EXECUTING` or `VERIFYING` can move to `RECOVERING` and then to `EXECUTING`, `VERIFYING` or `BLOCKED`.

- **INTAKE:** Identify the concrete request, affected project and known constraints.
- **SCOPED:** Define deliverable, non-goals, risks, acceptance tests and whether authorization exists.
- **PLAN:** Only when complexity, ambiguity or risks justify planning overhead.
- **AWAITING_APPROVAL:** Require explicit permission for significant architecture/scope changes, destructive changes, sensitive security changes, global agent configuration, publication and remote pushes.
- **EXECUTING:** Work within the approved scope and preserve other changes.
- **VERIFYING:** Collect actual test/inspection evidence, not merely an Agent self-claim.
- **RECOVERING:** Identify root cause; bounded attempts, new strategy and safe pause if no progress.
- **COMPLETED:** Verified or accurately labeled partially verified result.
- **BLOCKED:** Preserve workspace, explain obstacle and next safe step.

## Adaptive routing decision

| Situation | Recommended path | Additional gate |
| --- | --- | --- |
| Trivial cosmetic or local bug | Main Agent | Focused check |
| Moderate feature | Main Agent, relevant existing Skill | Appropriate tests |
| Substantial original interface | `design-studio` | Concept approval if direction changes |
| External licensed code or authorized app analysis | `rea-workflow` | Permission / license / safe-tool check |
| Architecture-critical or security-sensitive change | Main Agent + `deep-quality-review` or built-in review | Approval + expanded verification |
| Session transfer after meaningful progress | `task-handoff` | Verify status against actual diff |

The route table is **guidance**, not a deterministic model router or a guarantee of subagent spawning. Never call specialists merely to fulfill a template.

## Specialist handoff contract

```
GOAL: one bounded outcome
SCOPE: allowed files/actions, explicit exclusions
VERIFIED CONTEXT: referenced paths/observed facts
UNCERTAINTY: unknowns and assumptions
LIMITS: risk, permissions, license, product design constraints
DELIVERABLE: concise evidence packet or approved change
ACCEPTANCE: checks and expected result
BUDGET: inexpensive-first strategy and stop/escalate criteria
```

## Coordination

- By default run sequentially; parallelize only truly independent reads or isolated edits.
- Never have two workers edit the same file concurrently in a shared tree.
- A Git worktree isolates checkout state, **not** dangerous processes or network access; use stronger isolation where necessary.
- Read only relevant source files and the minimum verified decision records; expand when risk or evidence demands it.
- Avoid unbounded log propagation. Experts return succinct findings and pointers to raw evidence.
- Event-based memory updates are **not** automatic in alpha. Use `task-handoff` with explicit project write permission or produce a text handoff.

## Professional quality standard

A credible result integrates correctness, architecture, reliability, security, usability, performance and documentation in proportion to real risk. The UI should be original and purposeful, not merely ornamental. Cost optimization is subordinate to correctness and safety. Evidence must be observable; no invisible or invented checks.

## No implied capabilities

Cursor Craft does not implement separate models, guaranteed isolated agents, guaranteed automatic routing, cross-session persistent memory, hard token counters, executable validators in Cursor, or arbitrary EXE/APK inspection. Optional tools require separate user review and authorization.
