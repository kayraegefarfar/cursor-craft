---
name: deep-quality-review
description: Use for high-risk architectural modifications, pre-release readiness, significant regressions or requests for independent deep review. Skip for routine tiny changes; leverage built-in Cursor review facilities when sufficient.
---
# Evidence-Based Quality Review

## Objective
Find consequential, reproducible problems in an actual change without producing speculative noise or claiming nonexistent test results.

## Procedure
1. Confirm scope, acceptance criteria, base state, intended behavior and changed files. Respect uncommitted work.
2. Identify highest-risk paths: correctness and state transitions, permissions/secrets, unsafe external inputs, data persistence, backward compatibility, memory/CPU hot paths, UI interaction and accessibility where applicable.
3. Read the relevant diff and immediate dependencies. Request deeper context only if a specific risk requires it.
4. Run appropriate existing tests or inspections **only with permission and suitable environment**. Use more expensive integration/regression checks only when risk warrants them.
5. Categorize findings: `BLOCKER`, `IMPORTANT`, `MINOR`; annotate each with reproduction steps, affected files and actual evidence. Keep guesses separately labeled `UNCONFIRMED`.
6. Recommend the smallest reliable fix, avoid unrelated refactors and do not overwrite user changes. Recheck the implicated behavior after a fix when possible.
7. Clearly distinguish passed, failed and not-run checks; a clean diff or compilation alone does not prove functional success.

## Completion decision
- `PASS`: scoped acceptance and necessary tests verified with no unresolved blockers.
- `CONDITIONAL`: no known blockers, but important verification unavailable or documented issues remain.
- `BLOCKED`: critical regression, permission breach or unverifiable high-risk behavior; do not say completed.

When Cursor's built-in review covers the same need, prefer that over duplicate agent calls. Avoid repeating unsuccessful test loops.
