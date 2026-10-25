# Installation — user-scope preview

**Cursor Craft is currently an alpha source preview, not a Cursor-verified installer.** Review the source, official [Cursor Plugin docs](https://cursor.com/docs/plugins) and your installed rules/skills before trying it.

## Cross-platform: manual local plugin preview

1. Extract the distribution archive or clone the source repository into a folder you control. Do not run unknown scripts automatically.
2. Optional offline checks (Python 3.10+):

   ```bash
   python tools/validate_package.py
   python -m unittest discover -s tests -v
   ```

3. Back up your existing configuration and uncommitted project changes, and inspect Customize → Rules, Skills and Plugins for overlaps.
4. Ensure this exact destination **does not already exist**: `~/.cursor/plugins/local/cursor-craft/`. On Windows this means the `C:\Users\<your-user>\.cursor\plugins\local\cursor-craft\` directory in the current account's home. On macOS/Linux it is under `$HOME/.cursor/plugins/local/cursor-craft/`.
5. Manually **copy only** these items from the **repository root** into that new folder:

   ```text
   .cursor-plugin/plugin.json
   rules/
   skills/
   LICENSE
   ```

   Never write into existing global `~/.cursor/rules`, `~/.cursor/skills`, or project `.cursor/rules`. Never overwrite another plugin. Avoid symbolic-link installs outside the local plugins directory. The handoff template is `skills/task-handoff/template.md`, so it is included when `skills/` is copied. The `docs/` tree is not part of this copy.
6. In Cursor, use `Developer: Reload Window` (or restart Cursor), then check **Customize** for **one core rule** and **four Skills**. Actual discovery is version/permission-dependent.
7. Try a small coding task and a design or review task in a disposable repository; record failures and side effects before wider use. See [acceptance tests](acceptance-tests.md).

If your environment blocks local plugin imports or a name collision exists, **stop**. Follow organizational policy and read the current official documentation; do not force a configuration edit.

## Requesting installation from Cursor Agent

Before a real test session, use the [runtime validation runbook](runtime-validation.md).
`python tools/check_installation.py --candidate /path/to/authorized/test-copy`
reports missing, changed and extra files without modifying the selected copy.
It does not establish that Cursor loaded those files. Never point it at a user's
global installation without authorization. A same-name Marketplace installation
can take precedence over the local copy; confirm the active origin in Customize.

If you prefer agent assistance, review and paste the English [Cursor Agent install prompt](../CURSOR_AGENT_INSTALL_PROMPT.md). It includes safety constraints and explicit stop conditions. It is not itself an executed installer.

## Removal and rollback

Disable/uninstall via Customize when Cursor manages the installation. For a **manually copied local preview**, inspect the exact `~/.cursor/plugins/local/cursor-craft/` directory and remove **only that folder** if it contains no user-created work; then reload Cursor. Do not reset or delete unrelated global/plugin folders. Plugin removal does not revert edits already made to projects; manage those changes separately via normal version control.

## GitHub / Marketplace

See [GitHub source publishing](GITHUB_PUBLISHING.md). A public source repository does not mean Cursor Marketplace approval or runtime certification.
