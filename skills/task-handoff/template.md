# Compact session handoff template

Use this file from the `task-handoff` Skill. Local installation copies `skills/`, so this template is present even when the repository `docs/` directory is not.

Use it for meaningful boundaries, not every tiny edit. Keep the result project-local or return it as chat text. Write a project file only when that write is in scope.

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
