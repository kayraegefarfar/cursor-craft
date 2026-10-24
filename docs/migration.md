# Existing global configuration migration policy

Users may already have dozens of Rules/Skills and multiple overlapping packages. Cursor Craft must not bundle, scan, overwrite or uninstall them automatically.

## Inventory (opt-in; without scripts)

1. Review global User Rules inside Cursor settings and file-backed project/user Rules.
2. Review installed plugins and Skills using Customize, noting which are Active/Manual/Agent-Decides.
3. List any names overlapping: `design-studio`, `rea-workflow`, `deep-quality-review`, `task-handoff`, professional-core rules or similarly purposed packages.
4. Compare instruction **meaning**, not just same filenames: the same safety/approval clauses should not be repeated many times with conflicting scopes.
5. Retain current configuration as the rollback reference. Any proposed deactivation or merge requires explicit owner approval.

## Precedence principle

Do not assume package content overrides stronger Cursor/Team/Project/Developer policies. When guidance conflicts, respect actual host hierarchy and report the conflict rather than trying to force a custom priority.

## Compatibility recommendation

First preview this plugin in a separate noncritical scope. Measure routing with and without existing helpers. In a mature environment some included Skills may add no value; prefer **disabling only the redundant component**, using Cursor controls, after explicit review.

## Optional offline overlap audit (explicit archive input only)

The repository includes a read-only archive metadata helper:

```bash
python tools/overlap_audit.py path/to/one-existing-pack.zip path/to/other-pack.zip
```

It reads **only the ZIP files explicitly supplied** and compares Skill directory names against Cursor Craft's Skill topics. It does not extract files, invoke Cursor, change settings or log Skill bodies. **Keyword overlap is only a review candidate**, never evidence that two Skills behave identically or that either exists on the user's actual computer. There is no automatic deletion, merge, or migration.
