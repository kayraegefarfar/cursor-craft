# Compact session handoff template

The copy that ships with a local plugin install is [skills/task-handoff/template.md](../skills/task-handoff/template.md). Installation copies `skills/` and does not copy this `docs/` directory.

Use the template for meaningful boundaries, not every tiny edit. Keep the result project-local or return it as chat text. Write a project file only when that write is in scope.

```
PROJECT / HEAD REVISION:
USER GOAL AND APPROVED SCOPE:
COMPLETED (verified):
- Path(s), behavior, exact evidence
IMPORTANT DECISIONS / WHY:
- Decision, source, timestamp/revision
WORKSPACE STATE:
- Uncommitted user changes, branch/worktree, files currently owned
TESTS:
- PASS: exact command and result
- FAIL: exact command and failure
- NOT RUN: reason
RISKS / BLOCKERS:
NEXT SAFE ACTION:
```

No raw secrets, full logs or unverifiable claims. On resume, compare this record against the real code and current Git status.
