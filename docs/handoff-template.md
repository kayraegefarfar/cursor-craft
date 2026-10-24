# Compact session handoff template

Use for meaningful boundaries, not every tiny edit. Keep it project-local or return as chat text; write only with user permission.

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
