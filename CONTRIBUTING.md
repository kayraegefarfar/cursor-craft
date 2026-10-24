# Contributing

Thanks for considering an improvement. Cursor Craft values small, testable changes more than new agent labels.

1. Before a large proposal, open an issue explaining the user need, alternatives, safety and context costs.
2. Keep always-on core guidance concise. New specialized workflows belong in Skills only when clearly distinct from existing or built-in facilities.
3. Never silently add hooks, MCP servers, auto-downloaders, network telemetry or permission-changing scripts.
4. Extend `docs/acceptance-tests.md` for new behavior; include reproduction evidence and explicit `NOT_RUN` where tests were not possible.
5. Run `python tools/validate_package.py` and `python -m unittest discover -s tests -v` before proposing a change.
6. Don't submit proprietary prompts, copied paid skills, user account settings, private project data, embedded secrets or third-party code without compatible rights and attribution.
7. Explain compatibility, migration behavior and rollback for changes affecting existing installations.

A passing validator proves file/format checks only. Human review and Cursor runtime tests remain required for behavior claims.
