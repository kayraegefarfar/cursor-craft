# Cursor Agent: opt-in local install request

> Use this only after you have reviewed the contents of the downloaded repository and explicitly chosen to install Cursor Craft. This is a prompt for a human-controlled Cursor session, **not an automatic installer**.

Please help me install the **Cursor Craft** plugin in my personal Cursor environment for use across my own projects.

1. Locate this checked-out/extracted repository and verify that `.cursor-plugin/plugin.json` declares `cursor-craft`.
2. Before changing files, run `python tools/validate_package.py` and `python -m unittest discover -s tests -v` if Python 3.10+ is available. Report failures; do not proceed on failure.
3. Inspect `~/.cursor/plugins/local/cursor-craft` and the currently active Rules, Skills and plugins. **Do not overwrite, delete, move or consolidate existing files.** If that exact destination already exists, stop and report the collision.
4. Explain potential policy overlap before installation. Do not silently disable any existing global or project rule.
5. Once the inspection is clean, copy **only** `.cursor-plugin/plugin.json`, `rules/`, `skills/` and `LICENSE` into a newly created `~/.cursor/plugins/local/cursor-craft/` directory. Use a staging directory where possible; never modify `~/.cursor/rules`, `~/.cursor/skills`, project repositories or Cursor settings.
6. Restart/reload Cursor **only after I confirm** if it would interrupt work. Open Customize and verify discovery of one rule and four skills.
7. Report exactly what changed, what was actually tested, any unresolved overlap, and a safe uninstall path. **Do not** install MCPs, hooks or external analyzers; do not push to GitHub or publish a Marketplace listing.

If this Cursor version or the organization policy blocks local plugin loading, stop and explain the documented alternative instead of forcing installation.
